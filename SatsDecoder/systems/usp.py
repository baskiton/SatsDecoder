import datetime as dt
import tkinter as tk

from tkinter import ttk

import construct
from SatsDecoder.systems import common
from SatsDecoder.systems.image_receiver import ImageReceiver

__all__ = 'UspProtocol',


class TimeDeltaAdapter(construct.Adapter):
    def _encode(self, obj, context, path=None):
        return round(obj.total_seconds())

    def _decode(self, obj, context, path=None):
        return dt.timedelta(seconds=obj)


Addr = construct.Hex(construct.Int16ul)
RegTemp = common.LinearAdapter(100, construct.Int16sl)
Voltage = common.LinearAdapter(1000, construct.Int16ul)
VoltageS = common.LinearAdapter(1000, construct.Int16sl)

BEACON = 0x4216
REGULAR = 0xDE21
IMG_START = 0x0C20
IMG_SIZE = 0x0C2B
IMG_DATA = 0x0C24
ASCII = 0xFFF1

# XF210 = 0xF210
# X4235 = 0x4235
# X0118 = 0x0118
# XDF3D = 0xDF3D

beacon_flags = construct.BitStruct(
    'Uab_crit' / construct.Flag,
    'Uab_min' / construct.Flag,
    'heater2_manual' / construct.Flag,
    'heater1_manual' / construct.Flag,
    'heater2_on' / construct.Flag,
    'heater1_on' / construct.Flag,
    'Tab_max' / construct.Flag,
    'Tab_min' / construct.Flag,
    'channelon4' / construct.Flag,
    'channelon3' / construct.Flag,
    'channelon2' / construct.Flag,
    'channelon1' / construct.Flag,
    'Ich_limit4' / construct.Flag,
    'Ich_limit3' / construct.Flag,
    'Ich_limit2' / construct.Flag,
    'Ich_limit1' / construct.Flag,
    'reserved0' / construct.BitsInteger(7),
    'charger' / construct.Flag,
    'reserved1' / construct.BitsInteger(8),
)

Beacon = construct.Struct(
    'name' / construct.Computed(u'Beacon'),
    'Usb1' / Voltage,
    'Usb2' / Voltage,
    'Usb3' / Voltage,
    'Isb1' / construct.Int16ul,
    'Isb2' / construct.Int16ul,
    'Isb3' / construct.Int16ul,
    'Iab' / construct.Int16sl,
    'Ich1' / construct.Int16ul,
    'Ich2' / construct.Int16ul,
    'Ich3' / construct.Int16ul,
    'Ich4' / construct.Int16ul,
    't1_pw' / construct.Int16sl,
    't2_pw' / construct.Int16sl,
    't3_pw' / construct.Int16sl,
    't4_pw' / construct.Int16sl,
    'flags' / beacon_flags,
    'Uab' / VoltageS,
    'reg_tel_id' / construct.Int32ul,
    'Time' / common.UNIXTimestampAdapter(construct.Int32sl),
    'Nres' / construct.Int8ul,
    'FL' / construct.Int8ul,
    't_amp' / construct.Int8sl,
    't_uhf' / construct.Int8sl,
    'RSSIrx' / construct.Int8sl,
    'RSSIidle' / construct.Int8sl,
    'Pf' / construct.Int8sl,
    'Pb' / construct.Int8sl,
    'Nres_uhf' / construct.Int8ul,
    'Fl_uhf' / construct.Int8ul,
    'Time_uhf' / common.UNIXTimestampAdapter(construct.Int32sl),
    'UpTime' / TimeDeltaAdapter(construct.Int32ul),
    'Current' / construct.Int16ul,
    'Uuhf' / VoltageS,
)

regular_flags = construct.BitStruct(
    'Uab_crit' / construct.Flag,
    'Uab_min' / construct.Flag,
    'heater2_manual' / construct.Flag,
    'heater1_manual' / construct.Flag,
    'heater2_on' / construct.Flag,
    'heater1_on' / construct.Flag,
    'Tab_max' / construct.Flag,
    'Tab_min' / construct.Flag,
    'channelon4' / construct.Flag,
    'channelon3' / construct.Flag,
    'channelon2' / construct.Flag,
    'channelon1' / construct.Flag,
    'Ich_limit4' / construct.Flag,
    'Ich_limit3' / construct.Flag,
    'Ich_limit2' / construct.Flag,
    'Ich_limit1' / construct.Flag,
    'reserved0' / construct.BitsInteger(3),
    'add_channelon3' / construct.Flag,
    'add_channelon2' / construct.Flag,
    'add_channelon1' / construct.Flag,
    'fsb' / construct.Flag,
    'charger' / construct.Flag,
    'reserved1' / construct.BitsInteger(8),
)

Regular = construct.Struct(
    'name' / construct.Computed(u'Regular'),
    'Usb1' / construct.Int16ul,
    'Usb2' / construct.Int16ul,
    'Usb3' / construct.Int16ul,
    'Isb1' / construct.Int16ul,
    'Isb2' / construct.Int16ul,
    'Isb3' / construct.Int16ul,
    'Iab' / construct.Int16sl,
    'Ich1' / construct.Int16ul,
    'Ich2' / construct.Int16ul,
    'Ich3' / construct.Int16ul,
    'Ich4' / construct.Int16ul,
    't1_pw' / RegTemp,
    't2_pw' / RegTemp,
    't3_pw' / RegTemp,
    't4_pw' / RegTemp,
    'flags' / regular_flags,
    'Uab' / VoltageS,
    'reg_tel_id' / construct.Int32ul,
    'Time' / common.UNIXTimestampAdapter(construct.Int32sl),
    'Nres' / construct.Int8ul,
    'FL' / construct.Int8ul,
)

ImgStart = construct.Struct(
    'name' / construct.Computed(u'ImgStart'),
    'mode' / construct.Int8ul,
    'ses_id' / construct.Int8ul,
    'bs' / construct.Int16ul,
    'offset' / construct.Int32ul,
    'reserved' / construct.Int16ul,     # mb string size?
    'file_name' / construct.GreedyString('utf-8'),
)

ImgSize = construct.Struct(
    'name' / construct.Computed(u'ImgSize'),
    'size' / construct.Int32ul,
)

ImgData = construct.Struct(
    'name' / construct.Computed(u'ImgData'),
    'reserved0' / construct.Int8ul,
    'offset' / construct.Int32ul,
    'data' / construct.GreedyBytes,
)

tlm_map = {
    BEACON: 'Beacon' / Beacon,
    REGULAR: 'Regular' / Regular,
    IMG_START: 'ImgStart' / ImgStart,
    IMG_SIZE: 'ImgSize' / ImgSize,
    IMG_DATA: 'ImgData' / ImgData,
}


Data = construct.Struct(
    'message' / Addr,
    'sender' / Addr,
    'receiver' / Addr,
    'size' / construct.Int16ul,
    'packet' / construct.Switch(construct.this.message, tlm_map, default=construct.Bytes(construct.this.size)),
)

Frame = construct.Struct(
    'data' / construct.GreedyRange(Data),
    'lost' / construct.GreedyBytes
)

usp = construct.Struct(
    'ax25' / construct.Peek(common.ax25_header),
    'ax25' / construct.If(lambda this: bool(this.ax25), common.ax25_header),
    'usp' / construct.If(lambda this: (bool(this.ax25) and this.ax25.pid == 0xF0), Frame)
)


def usp_get_sender_callsign(tlm):
    return common.ax25_get_sender_callsign(tlm.ax25)


class UspImageReceiver(ImageReceiver):
    def __init__(self, outdir):
        super().__init__(outdir)

    def generate_fid(self, fname='unknown'):
        if not (self.current_fid and self.merge_mode):
            self.current_fid = fname
        return self.current_fid

    def push_data(self, data):
        packet = data.packet

        if data.message == IMG_DATA:
            img = self.get_image()
            with img.lock:
                img.push_data(packet.offset, packet.data)
                if packet.offset < img.first_data_offset:
                    img.first_data_offset = packet.offset

        elif data.message == IMG_START:
            self.generate_fid(packet.file_name)
            img = self.get_image()
            with img.lock:
                img.has_starter = 1

        elif data.message == IMG_SIZE:
            img = self.get_image()
            with img.lock:
                img.open().truncate(packet.size)

        else:
            return
        return 1


class _UspTlmCommon(ttk.Treeview):
    def __init__(self, master):
        super().__init__(master, columns='x val', selectmode='browse', show='tree')

        self.column('#0', anchor='e')
        self.column('x', width=10, stretch=tk.NO)

        self.vsb = ttk.Scrollbar(self.master, orient='vertical', command=self.yview)
        self.configure(yscrollcommand=self.vsb.set)

    def fill(self, tlm):
        for k, v in tlm.items():
            if not k.startswith('_'):
                self.set(k, 'val', v)


class _UspRegular(_UspTlmCommon):
    def __init__(self, master):
        super().__init__(master)

        self.insert('', 'end', 'name', text='Name')
        self.insert('', 'end', 'Usb1', text='Voltage SB #1, V')
        self.insert('', 'end', 'Usb2', text='Voltage SB #2, V')
        self.insert('', 'end', 'Usb3', text='Voltage SB #3, V')
        self.insert('', 'end', 'Isb1', text='Current SB #1, mA')
        self.insert('', 'end', 'Isb2', text='Current SB #2, mA')
        self.insert('', 'end', 'Isb3', text='Current SB #3, mA')
        self.insert('', 'end', 'Iab', text='Current battery, mA')
        self.insert('', 'end', 'Ich1', text='Current Ch #1, mA')
        self.insert('', 'end', 'Ich2', text='Current Ch #2, mA')
        self.insert('', 'end', 'Ich3', text='Current Ch #3, mA')
        self.insert('', 'end', 'Ich4', text='Current Ch #4, mA')
        self.insert('', 'end', 't1_pw', text='Temperature battery 1, °C')
        self.insert('', 'end', 't2_pw', text='Temperature battery 2, °C')
        self.insert('', 'end', 't3_pw', text='Temperature battery 3, °C')
        self.insert('', 'end', 't4_pw', text='Temperature battery 4, °C')
        self.insert('', 'end', 'Uab', text='Voltage battery, V')
        self.insert('', 'end', 'reg_tel_id', text='Telemetry SN')
        self.insert('', 'end', 'Time', text='Time')
        self.insert('', 'end', 'Nres', text='Reloads')
        self.insert('', 'end', 'FL', text='Flags UHF')

        # TODO
        self.insert('', 'end', 'flags', text='Flags')


class _UspBeacon(_UspRegular):
    def __init__(self, master):
        super().__init__(master)

        self.delete('flags')
        self.insert('', 'end', 't_amp', text='Temperature UHF amp, °C')
        self.insert('', 'end', 't_uhf', text='Temperature UHF, °C')
        self.insert('', 'end', 'RSSIrx', text='RSSI Received, dBm')
        self.insert('', 'end', 'RSSIidle', text='RSSI Idle, dBm')
        self.insert('', 'end', 'Pf', text='Direct radiation power')
        self.insert('', 'end', 'Pb', text='Back radiation power')
        self.insert('', 'end', 'Nres_uhf', text='Reloads UHF')
        self.insert('', 'end', 'Fl_uhf', text='Flags UHF')
        self.insert('', 'end', 'Time_uhf', text='Time UHF')
        self.insert('', 'end', 'UpTime', text='Uptime')
        self.insert('', 'end', 'Current', text='Current UHF, mA')
        self.insert('', 'end', 'Uuhf', text='Voltage UHF, V')

        # TODO
        self.insert('', 'end', 'flags', text='Flags')


class _UspTlmView(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.tlm_frames = {
            u'Beacon': _UspBeacon(self),
            u'Regular': _UspRegular(self),
        }

        self.tlm_name_l = ttk.Label(self)
        self.tlm_name_l.grid(row=1, sticky=tk.EW, pady=3)

    def fill(self, tlm, filename):
        table = self.tlm_frames[tlm.name]
        table.fill(tlm)
        for f in self.tlm_frames.values():
            f.grid_forget()
            f.vsb.grid_forget()

        table.grid(column=0, row=0, sticky=tk.NSEW)
        table.vsb.grid(column=1, row=0, sticky=tk.NSEW)

        self.tlm_name_l.config(text=filename)


class UspProtocol:
    columns = 'msg-id',
    c_width = 60,
    tlm_view = _UspTlmView

    def __init__(self, outdir):
        self.ir = UspImageReceiver(outdir)

    @staticmethod
    def get_sender_callsign(data):
        return common.ax25_get_sender_callsign(data.ax25)

    def recognize(self, data):
        data = usp.parse(data)
        if not data.usp:
            return

        for i in data.usp.data:
            p_data = i.packet

            if i.message in (IMG_DATA, IMG_START, IMG_SIZE):
                ty = 'img'
                p_data = self.ir.push_data(i), self.ir.cur_img.fn

            elif i.message in (BEACON, REGULAR):
                ty = 'tlm'
                p_data = data, p_data

            elif i.message == ASCII:
                ty = 'ascii'
                p_data = p_data.decode('ascii', 'replace')

            else:
                ty = 'raw'

            yield ty, self.get_sender_callsign(data), '0x%04X' % i.message, p_data
