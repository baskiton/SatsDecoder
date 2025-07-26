#  Copyright (c) 2024. Alexander Baskikh
#
#  MIT License (MIT), http://opensource.org/licenses/MIT
#  Full license can be found in the LICENSE-MIT file
#
#  SPDX-License-Identifier: MIT

import datetime as dt

from itertools import chain

import construct

from SatsDecoder import utils
from SatsDecoder.systems import ax25, common
from SatsDecoder.systems.image_receiver import ImageReceiver

__all__ = 'GeoscanProtocol',

proto_name = 'geoscan'

# GEOSCAN Telemetry Protocol
# https://download.geoscan.aero/site-files/%D0%9F%D1%80%D0%BE%D1%82%D0%BE%D0%BA%D0%BE%D0%BB%20%D0%BF%D0%B5%D1%80%D0%B5%D0%B4%D0%B0%D1%87%D0%B8%20%D1%82%D0%B5%D0%BB%D0%B5%D0%BC%D0%B5%D1%82%D1%80%D0%B8%D0%B8.pdf
# (https://download.geoscan.aero/site-files/Протокол передачи телеметрии.pdf)
#
# GEOSCAN2 Protocol
# https://download.geoscan.ru/site-files/Protokol_radio_3U.pdf


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


geoscan_tlm = construct.Struct(
    '_name' / construct.Computed('geoscan_beacon'),
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

stratosat_tlm = construct.Struct(
    '_name' / construct.Computed('stratosat_beacon'),
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

geoscan2_tlm = construct.Struct(
    '_name' / construct.Computed('geoscan2_beacon'),
    'name' / construct.Computed('Beacon'),

    'mayak_id' / construct.Hex(construct.Int8ul),   # must be 0x01

    # EPS
    'eps_name' / construct.Computed('EPS'),
    'Time' / common.UNIXTimestampAdapter(construct.Int32ul),
    'eps_mode' / construct.Hex(construct.Int8ul),
    '_reserved_eps0' / construct.Bytes(1),
    'Ipl' / construct.Int16ul,      # mA
    'Isp' / construct.Int16ul,      # mA
    'Uab_per' / construct.Int16ul,  # mV
    'Uab_sum' / construct.Int16ul,  # mV
    '_reserved_eps_bitfield0' / construct.Bytes(2),
    'Tab1' / construct.Int8sl,      # °C
    'Tab2' / construct.Int8sl,      # °C
    '_reserved_eps2' / construct.Bytes(2),
    '_reserved_eps_bitfield1' / construct.Bytes(1),
    '_reserved_eps3' / construct.Bytes(2),

    # OBC
    'obc_name' / construct.Computed('OBC'),
    '_reserved_obc0' / construct.Bytes(2),
    'obc_act' / construct.BitStruct(
        'flyweel' / construct.Flag,
        'coil' / construct.Flag,
        'ins' / construct.Flag,
        'cam' / construct.Flag,
        'x_plus' / construct.Flag,
        'x_minus' / construct.Flag,
        'y_plus' / construct.Flag,
        'y_minus' / construct.Flag,
    ),
    'Tx_plus' / construct.Int8sl,   # °C
    'Tx_minus' / construct.Int8sl,  # °C
    'Ty_plus' / construct.Int8sl,   # °C
    'Ty_minus' / construct.Int8sl,  # °C
    'gnss_num' / construct.Int8ul,
    '_reserved_obc1' / construct.Bytes(1),
    '_reserved_obc_sois' / construct.Int8ul,
    'camera_files' / construct.Int8ul,
    '_reserved_obc2' / construct.Bytes(1),
    '_reserved_obc3' / construct.Bytes(4),

    # COMMU 1/2
    'commu_name' / construct.Computed('COMMU 1/2'),
    '_reserved_commu0' / construct.Bytes(1),
    'Uvbus' / construct.Int16ul,    # mV
    '_reserved_commu1' / construct.Bytes(2),
    'rssi_last' / construct.Int8sl, # dBm
    'rssi_min' / construct.Int8sl, # dBm
    '_reserved_commu2' / construct.Bytes(1),
    '_reserved_commu3' / construct.Bytes(1),
    'tx_num' / construct.Int8ul,
    '_reserved_commu4' / construct.Bytes(1),
    '_reserved_commu5' / construct.Bytes(1),
    '_reserved_commu6' / construct.Bytes(1),
    'qso_num' / construct.Int8ul,
    '_reserved_commu7' / construct.Bytes(2),
)

tlm_map = {
    'RS20S': geoscan_tlm,
    'RS52S': stratosat_tlm,
}

geoscan = construct.Struct(
    'ax25' / construct.Peek(ax25.ax25_header),
    'ax25' / construct.If(lambda this: (bool(this.ax25) and this.ax25.addresses[0].callsign == u'BEACON'),
                          ax25.ax25_header),
    'packet' / construct.If(lambda this: (bool(this.ax25) and this.ax25.pid == 0xF0),
                            construct.Switch(construct.this.ax25.addresses[1].callsign, tlm_map, default=geoscan2_tlm)),
)


# sats numbers
GEOSCAN = 0x01
STRATOSAT = 0x02
HORIZON = 0x03
RTU_MIREA_1 = 0x04
TUSUR_GO = 0x05
COLIBRI_S = 0x06
VIZARD_ION = 0x07
ALFEROV239 = 0x09
INNOSAT3 = 0x0A
GEOSCAN1 = 0x0B
GEOSCAN2 = 0x0C
GEOSCAN3 = 0x0D
GEOSCAN4 = 0x0E
GEOSCAN5 = 0x0F
GEOSCAN6 = 0x10
INNOSAT16 = 0x11

_satnum = construct.Enum(
    construct.Int8ul,
    GEOSCAN=GEOSCAN,
    STRATOSAT=STRATOSAT,
    HORIZON=HORIZON,
    RTU_MIREA_1=RTU_MIREA_1,
    TUSUR_GO=TUSUR_GO,
    COLIBRI_S=COLIBRI_S,
    VIZARD_ION=VIZARD_ION,
    ALFEROV239=ALFEROV239,
    INNOSAT3=INNOSAT3,
    GEOSCAN1=GEOSCAN1,
    GEOSCAN2=GEOSCAN2,
    GEOSCAN3=GEOSCAN3,
    GEOSCAN4=GEOSCAN4,
    GEOSCAN5=GEOSCAN5,
    GEOSCAN6=GEOSCAN6,
    INNOSAT16=INNOSAT16,
)

_frame_hdr = construct.Struct(
    'sat_num' / _satnum,
    'reserved' / construct.Int8ul,
    'dlen' / construct.Int8ul,
)

_frame1 = construct.Struct(
    'sat_num' / _satnum,
    'reserved' / construct.Int8ul,
    'dlen' / construct.Int8ul,
    'mtype' / construct.Hex(construct.Int16ul),
    'offset' / construct.Int16ul,
    'subsystem_num' / construct.Int8ul,
    # 'data' / construct.Bytes(construct.this.dlen - 6)
    # 'data' / construct.Bytes(56),
    'data' / construct.GreedyBytes,
    # 'pad' / construct.Bytes(8),
)

_frame2 = construct.Struct(
    'sat_num' / _satnum,
    'reserved' / construct.Int8ul,
    'dlen' / construct.Int8ul,
    'reserved' / construct.Bytes(2),
    'marker' / construct.Hex(construct.Int32ul),
    'offset' / construct.Int32ul,
    'fnum' / construct.Int16ul,
    'data' / construct.Bytes(54),
    'tail' / construct.GreedyBytes,
)

sat_names = {
    GEOSCAN: 'geoscan-img',
    STRATOSAT: 'stratosat-img',
    HORIZON: 'horizon-img',
    RTU_MIREA_1: 'rtu-mirea-1-img',
    TUSUR_GO: 'tusur-go-img',
    COLIBRI_S: 'colibri-s-img',
    VIZARD_ION: 'vizard-ion-img',
    ALFEROV239: '239alferov-img',
    INNOSAT3: 'innosat3-img',
    GEOSCAN1: 'geoscan-1-img',
    GEOSCAN2: 'geoscan-2-img',
    GEOSCAN3: 'geoscan-3-img',
    GEOSCAN4: 'geoscan-4-img',
    GEOSCAN5: 'geoscan-5-img',
    GEOSCAN6: 'geoscan-6-img',
    INNOSAT16: 'innosat16-img',
}


def get_sat_name(sat_num):
    return sat_names.get(sat_num, 'geoscan-common')


class GeoscanImageReceiver(ImageReceiver):
    CMD_IMG_START = 0x0901
    CMD_IMG_FRAME = 0x0905, 0x0920,
    CMD_IMG_HR_FRAME = 0x9820, 0x411C
    MARKER_V2_IMG = 0x6F6B6F31

    def __init__(self, outdir):
        super().__init__(outdir, '.jpg')
        self._prev_data_sz = -1
        self._miss_cnt = 0
        self._last_sat_num = -1
        self._last_is_hr = 0
        self._last_fnum = -1

    def generate_fid(self, sat_num=None):
        if not (self.current_fid and self.merge_mode):
            self.last_date = now = dt.datetime.now()
            pfx = get_sat_name(sat_num).rpartition('-')[0]
            hr = self._last_is_hr and '_hr' or ''
            fnum = (self._last_fnum > -1) and ('_N' + str(self._last_fnum)) or ''
            self.current_fid = f'{pfx.upper()}{hr}{fnum}_{now.strftime("%Y-%m-%d_%H-%M-%S,%f")}'
        return self.current_fid

    def force_new(self, *args, **kwargs):
        return super().force_new(*args, **kwargs)

    def push_data(self, data, is_v2=0, **kw):
        if int(data.sat_num) not in sat_names:
            self._miss_cnt += 1
            return

        if is_v2:
            x = self._push_data2(data)
        else:
            x = self._push_data1(data)
        return x

    def _push_data1(self, data):
        sat_num = int(data.sat_num)
        off = (data.subsystem_num << 16) | data.offset

        if data.mtype == self.CMD_IMG_START:
            force = 0
            if sat_num != self._last_sat_num:
                self._last_sat_num = sat_num
                force = 1
            if self._last_is_hr:
                self._last_is_hr = 0
                force = 1

            if force:
                img = self.force_new(sat_num=sat_num)
            else:
                img = self.get_image(1, sat_num=sat_num)

            with img.lock:
                if data.data.startswith(b'\xff\xd8'):
                    img.has_soi = 1
                img.has_starter = 1
                img.base_offset = off
                img.first_data_offset = off = 0

                img.push_data(off, data.data[:data.dlen - 6])

        elif data.mtype in chain(self.CMD_IMG_FRAME, self.CMD_IMG_HR_FRAME):
            has_soi = data.data.startswith(b'\xff\xd8')
            force = 0
            if sat_num != self._last_sat_num:
                self._last_sat_num = sat_num
                force = 1
            is_hr = data.mtype in self.CMD_IMG_HR_FRAME
            if is_hr != self._last_is_hr:
                self._last_is_hr = is_hr
                force = 1

            if force:
                img = self.force_new(sat_num=sat_num)
            else:
                img = self.get_image(has_soi, sat_num=sat_num)
                if has_soi and not img.has_soi:
                    img.rebase_offset(off)

            with img.lock:
                if has_soi:
                    img.has_soi = 1
                    img.base_offset = off

                x = off - img.base_offset
                if x < 0:
                    img = self.force_new(sat_num=sat_num)
                    img.base_offset = img.BASE_OFFSET
                    if has_soi:
                        img.has_soi = 1
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
                    # self.current_fid = ''
                    return 2

        else:
            return

        return 1

    def is_last_data(self, data):
        prev_sz = self._prev_data_sz
        self._prev_data_sz = len(data)
        return (self._prev_data_sz < prev_sz) and b'\xff\xd9' in data

    def _push_data2(self, data):
        sat_num = int(data.sat_num)
        if data.marker != self.MARKER_V2_IMG:
            return

        has_soi = data.data.startswith(b'\xff\xd8')
        off = data.offset
        force = 0
        if sat_num != self._last_sat_num:
            self._last_sat_num = sat_num
            force = 1
        if data.fnum != self._last_fnum:
            self._last_fnum = data.fnum
            force = 1

        if force:
            img = self.force_new(sat_num=sat_num)
        else:
            img = self.get_image(has_soi, sat_num=sat_num)

        with img.lock:
            if has_soi:
                img.has_soi = 1
                img.has_starter = 1
                img.base_offset = off
                img.first_data_offset = off = 0
            if off < img.first_data_offset:
                img.first_data_offset = off

            img.push_data(off, data.data)

        return 1


class GeoscanProtocol(common.Protocol):
    PACKETSIZE = 64
    columns = ()
    c_width = ()
    has_ax25 = 1
    tlm_table = {
        'geoscan_beacon': {
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
        'stratosat_beacon': {
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
        'geoscan2_beacon': {
            'table': (
                ('name', 'Name'),
                ('Time', 'Time'),

                ('eps_name', '#'),
                ('eps_mode', 'EPS mode'),
                ('Ipl', 'Current total, mA'),
                ('Isp', 'Current SP, mA'),
                ('Uab_per', 'Voltage per battery, mV'),
                ('Uab_sum', 'Voltage total, mV'),
                ('Tab1', 'Temperature battery #1, °C'),
                ('Tab2', 'Temperature battery #2, °C'),

                ('obc_name', '#'),
                ('obc_act/flyweel', 'Flyweels act'),
                ('obc_act/coil', 'Coils act'),
                ('obc_act/ins', 'INS act'),
                ('obc_act/cam', 'Cam act'),
                ('obc_act/x_plus', 'Panel X+ act'),
                ('obc_act/x_minus', 'Panel X- act'),
                ('obc_act/y_plus', 'Panel Y+ act'),
                ('obc_act/y_minus', 'Panel Y- act'),
                ('Tx_plus', 'Temperature X+, °C'),
                ('Tx_minus', 'Temperature X-, °C'),
                ('Ty_plus', 'Temperature Y+, °C'),
                ('Ty_minus', 'Temperature Y-, °C'),
                ('gnss_num', 'GNSS satellites'),
                ('camera_files', 'Camera files'),

                ('commu_name', '#'),
                ('Uvbus', 'VBUS voltage, mV'),
                ('rssi_last', 'RSSI last, dBm'),
                ('rssi_min', 'RSSI min, dBm'),
                ('tx_num', 'TX packets'),
                ('qso_num', 'QSO numbers'),
            ),
        },
    }

    def __init__(self, outdir):
        super().__init__(GeoscanImageReceiver(outdir))
        self.last_fn = None

    def recognize(self, data):
        # raw_packet, data = data[:self.PACKETSIZE], data[self.PACKETSIZE:]
        tlm = geoscan.parse(data)
        name = self.get_sender_callsign(tlm)

        if tlm.packet:
            yield 'tlm', name, (tlm, tlm.packet)
            return

        is_v2 = 0
        try:
            hdr = _frame_hdr.parse(data)
            if int(hdr.sat_num) in (GEOSCAN, STRATOSAT):
                frame = _frame1.parse(data)
            else:
                is_v2 = 1
                frame = _frame2.parse(data)
        except construct.ConstructError:
            yield 'raw', get_sat_name(None), data
            return

        name = get_sat_name(int(frame.sat_num))

        x = self.ir.push_data(frame, is_v2)
        if x:
            if x != 2:
                self.last_fn = self.ir.cur_img.fn
            yield 'img', name, (x, self.ir.cur_img)
            return

        yield 'frame', name, f'{str(frame)}\n\nHex:\n{utils.bytes2hex(data)}'
