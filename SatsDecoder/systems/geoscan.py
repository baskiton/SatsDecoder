import datetime as dt

import construct

from SatsDecoder import utils
from SatsDecoder.systems import common
from SatsDecoder.systems.image_receiver import ImageReceiver

__all__ = 'GeoscanProtocol',

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

    'Tx_plus' / construct.Int8ul,   # deg C
    'Tx_minus' / construct.Int8ul,  # deg C
    'Ty_plus' / construct.Int8ul,   # deg C
    'Ty_minus' / construct.Int8ul,  # deg C
    'Tz_plus' / construct.Int8ul,   # undef
    'Tz_minus' / construct.Int8ul,  # deg C
    'Tab1' / construct.Int8ul,      # deg C
    'Tab2' / construct.Int8ul,      # deg C
    'CPU_load' / construct.Int8ul,  # %
    'Nres_osc' / SubAdapter(7476, construct.Int16ul),
    'Nres_CommU' / SubAdapter(1505, construct.Int16ul),
    'RSSI' / SubAdapter(99, construct.Int8ul),  # dBm

    'pad' / construct.GreedyBytes
)

geoscan = construct.Struct(
    'ax25' / construct.Peek(common.ax25_header),
    'ax25' / construct.If(lambda this: (bool(this.ax25)
                                        and this.ax25.addresses[0].callsign == u'BEACON'),
                          common.ax25_header),
    'geoscan' / construct.If(lambda this: (bool(this.ax25)
                                           and this.ax25.pid == 0xF0),
                             geoscan_frame),
)


_frame = construct.Struct(
    'marker' / construct.Int16ul,  # #0
    'dlen' / construct.Int8ul,              # #2
    'mtype' / construct.Int16ul,            # #3
    'offset' / construct.Int16ul,           # #5
    'subsystem_num' / construct.Int8ul,     # #7
    # 'data' / construct.Bytes(construct.this.dlen - 6)
    'data' / construct.Bytes(56)
)


class GeoscanImageReceiver(ImageReceiver):
    MARKER_IMG = 0x0001, 0x0002
    CMD_IMG_START = 0x0901
    CMD_IMG_FRAME = 0x0905

    def __init__(self, outdir):
        super().__init__(outdir, '.jpg')
        self._prev_data_sz = -1
        self._miss_cnt = 0

    def generate_fid(self):
        if not (self.current_fid and self.merge_mode):
            self.current_fid = f'GEOSCAN_{dt.datetime.now()}'.replace(' ', '_').replace(':', '-')
        return self.current_fid

    def force_new(self):
        return super().force_new()

    def push_data(self, data):
        try:
            data = _frame.parse(data)
        except construct.ConstructError:
            return

        if data.marker not in self.MARKER_IMG:
            self._miss_cnt += 1
            return

        if data.mtype == self.CMD_IMG_START:
            img = self.get_image(1)

            with img.lock:
                if data.data.startswith(b'\xff\xd8'):
                    img.has_soi = data.offset
                img.has_starter = 1
                img.base_offset = data.offset
                img.first_data_offset = data.offset = 0

                img.push_data(data.offset, data.data[:data.dlen - 6])

        elif data.mtype == self.CMD_IMG_FRAME:
            force = data.data.startswith(b'\xff\xd8')
            img = self.get_image(force)
            with img.lock:
                if force:
                    img.base_offset = img.has_soi = data.offset

                x = data.offset - img.base_offset
                if x < 0:
                    img = self.force_new()
                    img.base_offset = img.BASE_OFFSET
                    x = data.offset - img.base_offset
                data.offset = x
                if x < img.first_data_offset:
                    img.first_data_offset = x

                x = data.data[:data.dlen - 6]
                img.push_data(data.offset, x)
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
    }

    def __init__(self, outdir):
        self.ir = GeoscanImageReceiver(outdir)
        self.last_fn = None

    @staticmethod
    def get_sender_callsign(data):
        return common.ax25_get_sender_callsign(data.ax25)

    def recognize(self, data):
        tlm = geoscan.parse(data)
        name = self.get_sender_callsign(tlm) or 'geoscan'

        if tlm.geoscan:
            yield 'tlm', name, (tlm, tlm.geoscan)
            return

        x = self.ir.push_data(data)
        if x:
            if x != 2:
                self.last_fn = self.ir.cur_img.fn
            yield 'img', name, (x, self.ir.cur_img)
            return

        try:
            frame = _frame.parse(data)
        except construct.ConstructError:
            yield 'raw', name, data
            return

        yield 'frame', name, f'{str(frame)}\n\nHex:\n{utils.bytes2hex(data)}'
