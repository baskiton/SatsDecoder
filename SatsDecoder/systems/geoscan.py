#  Copyright (c) 2024. Alexander Baskikh
#
#  MIT License (MIT), http://opensource.org/licenses/MIT
#  Full license can be found in the LICENSE-MIT file
#
#  SPDX-License-Identifier: MIT

import datetime as dt

import construct

from SatsDecoder import utils
from SatsDecoder.systems import ax25, common
from SatsDecoder.systems.image_receiver import ImageReceiver

__all__ = 'GeoscanProtocol',

proto_name = 'geoscan'

# GEOSCAN Telemetry Protocol
# https://download.geoscan.aero/site-files/%D0%9F%D1%80%D0%BE%D1%82%D0%BE%D0%BA%D0%BE%D0%BB%20%D0%BF%D0%B5%D1%80%D0%B5%D0%B4%D0%B0%D1%87%D0%B8%20%D1%82%D0%B5%D0%BB%D0%B5%D0%BC%D0%B5%D1%82%D1%80%D0%B8%D0%B8.pdf
# (https://download.geoscan.aero/site-files/Протокол передачи телеметрии.pdf)


class SubAdapter(construct.Adapter):
    def __init__(self, v, *args, **kwargs):
        self.v = v
        construct.Adapter.__init__(self, *args, **kwargs)

    def _encode(self, obj, context, path=None):
        return int(obj + self.v)

    def _decode(self, obj, context, path=None):
        return obj - self.v


class MulAdapter(construct.Adapter):
    def __init__(self, v, *args, **kwargs):
        self.v = v
        construct.Adapter.__init__(self, *args, **kwargs)

    def _encode(self, obj, context, path=None):
        return int(round(obj / self.v))

    def _decode(self, obj, context, path=None):
        return float(obj) * self.v


geoscan_frame = construct.Struct(
    '_name' / construct.Computed('beacon'),
    'name' / construct.Computed('Beacon'),

    'Time' / common.UNIXTimestampAdapter(construct.Int32ul),
    'Iab' / MulAdapter(0.0766, construct.Int16ul),      # mA
    'Isp' / MulAdapter(0.03076, construct.Int16ul),     # mA

    'Uab_per' / MulAdapter(0.00006928, construct.Int16ul),   # V
    'Uab_sum' / MulAdapter(0.00013856, construct.Int16ul),   # V

    'Tx_plus' / construct.Int8sl,   # deg C
    'Tx_minus' / construct.Int8sl,  # deg C
    'Ty_plus' / construct.Int8sl,   # deg C
    'Ty_minus' / construct.Int8sl,  # deg C
    'Tz_plus' / construct.Int8sl,   # undef
    'Tz_minus' / construct.Int8sl,  # deg C
    'Tab1' / construct.Int8sl,      # deg C
    'Tab2' / construct.Int8sl,      # deg C

    'CPU_load' / MulAdapter(0.390625, construct.Int8ul),  # %
    'Nres_osc' / SubAdapter(7476, construct.Int16ul),
    'Nres_CommU' / SubAdapter(1505, construct.Int16ul),
    'RSSI' / SubAdapter(99, construct.Int8ul),  # dBm

    'pad' / construct.GreedyBytes
)


stratosat_frame = construct.Struct(
    '_name' / construct.Computed('stratosat'),
    'name' / construct.Computed('Beacon'),

    'Time' / common.UNIXTimestampAdapter(construct.Int32ul),
    'Iab' / MulAdapter(0.0766, construct.Int16ul),      # mA
    'Isp' / MulAdapter(0.03076, construct.Int16ul),     # mA

    'Uab_per' / MulAdapter(0.00006928, construct.Int16ul),   # V
    'Uab_sum' / MulAdapter(0.00013856, construct.Int16ul),   # V

    'Ichrg' / MulAdapter(0.03076, construct.Int32ul),  # mA
    'Itotal' / MulAdapter(0.0766, construct.Int32ul),  # mA

    'Tx_plus' / construct.Int8sl,   # deg C
    'Tx_minus' / construct.Int8sl,  # deg C
    'Ty_plus' / construct.Int8sl,   # deg C
    'Ty_minus' / construct.Int8sl,  # deg C
    'Tz_plus' / construct.Int8sl,   # undef
    'Tz_minus' / construct.Int8sl,  # deg C
    'Tab1' / construct.Int8sl,      # deg C
    'Tab2' / construct.Int8sl,      # deg C

    'orient' / construct.Hex(construct.Enum(construct.Int8ul, Off=0, On=1)),
    'CPU_load' / MulAdapter(0.390625, construct.Int8ul),  # %
    'Nres_osc' / SubAdapter(0, construct.Int16ul),
    'Nres_CommU' / SubAdapter(0, construct.Int16ul),
    'RSSI' / SubAdapter(99, construct.Int8ul),  # dBm

    'Rx' / construct.Int16ul,
    'Tx' / construct.Int16ul,

    'pad' / construct.GreedyBytes
)

frames_map = {
    'RS20S': geoscan_frame,
    'RS52S': stratosat_frame,
}

geoscan = construct.Struct(
    'ax25' / construct.Peek(ax25.ax25_header),
    'ax25' / construct.If(lambda this: (bool(this.ax25)
                                        and this.ax25.addresses[0].callsign == u'BEACON'),
                          ax25.ax25_header),
    'packet' / construct.If(lambda this: (bool(this.ax25)
                                           and this.ax25.pid == 0xF0),
                             construct.Switch(construct.this.ax25.addresses[1].callsign, frames_map, default=geoscan_frame)),
)


_frame = construct.Struct(
    'marker' / construct.Hex(construct.Int16ul),    # #0
    'dlen' / construct.Int8ul,                      # #2
    'mtype' / construct.Hex(construct.Int16ul),     # #3
    'offset' / construct.Int16ul,                   # #5
    'subsystem_num' / construct.Int8ul,             # #7
    # 'data' / construct.Bytes(construct.this.dlen - 6)
    'data' / construct.Bytes(56)
)

# mtypes
GEOSKAN_IMG = 0x0001
STRATOSAT_IMG = 0x0002

marker_names = {
    GEOSKAN_IMG: 'geoscan-img',
    STRATOSAT_IMG: 'stratosat-img',
}


def get_marker_name(marker):
    return marker_names.get(marker, 'geoscan-common')


class GeoscanImageReceiver(ImageReceiver):
    MARKERS = GEOSKAN_IMG, STRATOSAT_IMG
    CMD_IMG_START = 0x0901
    CMD_IMG_FRAME = 0x0905, 0x0920

    def __init__(self, outdir):
        super().__init__(outdir, '.jpg')
        self._prev_data_sz = -1
        self._miss_cnt = 0

    def generate_fid(self, marker=None):
        if not (self.current_fid and self.merge_mode):
            self.last_date = now = dt.datetime.now()
            pfx = get_marker_name(marker).split('-')[0]
            self.current_fid = f'{pfx.upper()}_{now.strftime("%Y-%m-%d_%H-%M-%S,%f")}'
        return self.current_fid

    def force_new(self, *args, **kwargs):
        return super().force_new(*args, **kwargs)

    def push_data(self, data):
        if data.marker not in self.MARKERS:
            self._miss_cnt += 1
            return

        off = (data.subsystem_num << 16) | data.offset

        if data.mtype == self.CMD_IMG_START:
            img = self.get_image(1, marker=data.marker)

            with img.lock:
                if data.data.startswith(b'\xff\xd8'):
                    img.has_soi = off
                img.has_starter = 1
                img.base_offset = off
                img.first_data_offset = off = 0

                img.push_data(off, data.data[:data.dlen - 6])

        elif data.mtype in self.CMD_IMG_FRAME:
            force = data.data.startswith(b'\xff\xd8')
            img = self.get_image(force, marker=data.marker)
            with img.lock:
                if force:
                    img.base_offset = img.has_soi = off

                x = off - img.base_offset
                if x < 0:
                    img = self.force_new(marker=data.marker)
                    img.base_offset = img.BASE_OFFSET
                    x = off - img.base_offset
                off = x
                if x < img.first_data_offset:
                    img.first_data_offset = x

                x = data.data[:data.dlen - 6]
                img.push_data(off, x)
                # if self.is_last_data(x) and not self.merge_mode:
                if self.is_last_data(x):
                    img.flush()
                    # img.close()
                    # self.current_fid = None
                    return 2

        else:
            return

        return 1

    def is_last_data(self, data):
        prev_sz = self._prev_data_sz
        self._prev_data_sz = len(data)
        return (self._prev_data_sz < prev_sz) and b'\xff\xd9' in data


class GeoscanProtocol:
    PACKETSIZE = 64
    columns = ()
    c_width = ()
    tlm_table = {
        'beacon': {
            'table': (
                ('name', 'Name'),
                ('Time', 'Time'),
                ('Iab', 'Current total, mA'),
                ('Isp', 'Current SP, mA'),
                ('Uab_per', 'Voltage per battery, V'),
                ('Uab_sum', 'Voltage total, V'),
                ('Tx_plus', 'Temperature SP X+, °C'),
                ('Tx_minus', 'Temperature SP X-, °C'),
                ('Ty_plus', 'Temperature SP Y+, °C'),
                ('Ty_minus', 'Temperature SP Y-, °C'),
                ('Tz_plus', 'Temperature SP Z+, °C'),
                ('Tz_minus', 'Temperature SP Z-, °C'),
                ('Tab1', 'Temperature battery #1, °C'),
                ('Tab2', 'Temperature battery #2, °C'),
                ('CPU_load', 'CPU load, %'),
                ('Nres_osc', 'Reloads spacecraft'),
                ('Nres_CommU', 'Reloads CommU'),
                ('RSSI', 'RSSI, dBm'),
                ('pad', 'pad'),
            )
        },
        'stratosat': {
            'table': (
                ('name', 'Name'),
                ('Time', 'Time'),
                ('Iab', 'Current total, mA'),
                ('Isp', 'Current SP, mA'),
                ('Uab_per', 'Voltage per battery, V'),
                ('Uab_sum', 'Voltage total, V'),
                ('Ichrg', 'Current of Charger, mA'),
                ('Itotal', 'Current amount, mA'),
                ('Tx_plus', 'Temperature SP X+, °C'),
                ('Tx_minus', 'Temperature SP X-, °C'),
                ('Ty_plus', 'Temperature SP Y+, °C'),
                ('Ty_minus', 'Temperature SP Y-, °C'),
                ('Tz_plus', 'Temperature SP Z+, °C'),
                ('Tz_minus', 'Temperature SP Z-, °C'),
                ('Tab1', 'Temperature battery #1, °C'),
                ('Tab2', 'Temperature battery #2, °C'),
                ('orient', 'Orientation'),
                ('CPU_load', 'CPU load, %'),
                ('Nres_osc', 'Reloads spacecraft'),
                ('Nres_CommU', 'Reloads CommU'),
                ('RSSI', 'RSSI, dBm'),
                ('Rx', 'Rx packets'),
                ('Tx', 'Tx packets'),
                ('pad', 'pad'),
            )
        },
    }

    def __init__(self, outdir):
        self.ir = GeoscanImageReceiver(outdir)
        self.last_fn = None

    @staticmethod
    def get_sender_callsign(data):
        return ax25.get_sender_callsign(data.ax25)

    def recognize(self, data):
        while data:
            raw_packet, data = data[:self.PACKETSIZE], data[self.PACKETSIZE:]
            tlm = geoscan.parse(raw_packet)
            name = self.get_sender_callsign(tlm)

            if tlm.packet:
                yield 'tlm', name, (tlm, tlm.packet)
                continue

            try:
                frame = _frame.parse(raw_packet)
            except construct.ConstructError:
                yield 'raw', get_marker_name(None), raw_packet
                continue

            name = get_marker_name(frame.marker)
            x = self.ir.push_data(frame)
            if x:
                if x != 2:
                    self.last_fn = self.ir.cur_img.fn
                yield 'img', name, (x, self.ir.cur_img)
                continue

            yield 'frame', name, f'{str(frame)}\n\nHex:\n{utils.bytes2hex(raw_packet)}'
