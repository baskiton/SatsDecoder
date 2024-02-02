import datetime as dt
import tkinter as tk

from tkinter import ttk

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

                img.push_data(data.offset, data.data[:data.dlen - 6])
                if self.is_last_data(data) and not self.merge_mode:
                    img.close()
                    self.current_fid = None
                    return 2

        else:
            return

        return 1

    def is_last_data(self, data):
        prev_sz = self._prev_data_sz
        self._prev_data_sz = len(data.data)
        return (self._prev_data_sz < prev_sz) and b'\xff\xd9' in data.data


class _GeoscanTlmView(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.rowconfigure(0, weight=1)

        self.tlm_table = ttk.Treeview(self, columns='x val', selectmode='browse', show='tree')
        self.tlm_table.column('#0', anchor='e')
        self.tlm_table.column('x', width=10, stretch=tk.NO)

        self.tlm_table.insert('', 'end', 'Time', text='Time')
        self.tlm_table.insert('', 'end', 'Iab', text='Current total, mA')
        self.tlm_table.insert('', 'end', 'Isp', text='Current SP, mA')
        self.tlm_table.insert('', 'end', 'Uab_per', text='Voltage per battery, V')
        self.tlm_table.insert('', 'end', 'Uab_sum', text='Voltage total, V')
        self.tlm_table.insert('', 'end', 'Tx_plus', text='Temperature SP X+, °C')
        self.tlm_table.insert('', 'end', 'Tx_minus', text='Temperature SP X-, °C')
        self.tlm_table.insert('', 'end', 'Ty_plus', text='Temperature SP Y+, °C')
        self.tlm_table.insert('', 'end', 'Ty_minus', text='Temperature SP Y-, °C')
        self.tlm_table.insert('', 'end', 'Tz_plus', text='Temperature SP Z+, °C')
        self.tlm_table.insert('', 'end', 'Tz_minus', text='Temperature SP Z-, °C')
        self.tlm_table.insert('', 'end', 'Tab1', text='Temperature battery 1, °C')
        self.tlm_table.insert('', 'end', 'Tab2', text='Temperature battery 2, °C')
        self.tlm_table.insert('', 'end', 'CPU_load', text='CPU load, %')
        self.tlm_table.insert('', 'end', 'Nres_osc', text='Reloads spacecraft')
        self.tlm_table.insert('', 'end', 'Nres_CommU', text='Reloads CommU')
        self.tlm_table.insert('', 'end', 'RSSI', text='RSSI, dBm')
        self.tlm_table.insert('', 'end', 'pad', text='pad')

        self.tlm_table.grid(sticky=tk.NSEW)

        self.tlm_name_l = ttk.Label(self)
        self.tlm_name_l.grid(sticky=tk.EW, pady=3)

    def fill(self, tlm, filename):
        for k, v in tlm.items():
            if not k.startswith('_'):
                self.tlm_table.set(k, 'val', v)

        self.tlm_name_l.config(text=filename)


class GeoscanProtocol:
    columns = ()
    c_width = ()
    tlm_view = _GeoscanTlmView

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
            if x == 2:
                fn = self.last_fn
            else:
                fn = self.ir.cur_img.fn
                self.last_fn = fn
            yield 'img', name, (x, fn)
            return

        try:
            frame = _frame.parse(data)
        except construct.ConstructError:
            yield 'raw', name, data
            return

        yield 'frame', name, f'{str(frame)}\n\nHex:\n{utils.bytes2hex(data)}'
