import datetime as dt

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
# ASCII = 0xFFF1

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
    '_reserved0' / construct.BitsInteger(7),
    'charger' / construct.Flag,
    '_reserved1' / construct.BitsInteger(8),
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
    'Ich_fault4' / construct.Flag,
    'Ich_fault3' / construct.Flag,
    'Ich_fault2' / construct.Flag,
    'Ich_fault1' / construct.Flag,
    '_reserved0' / construct.BitsInteger(3),
    'add_channelon3' / construct.Flag,
    'add_channelon2' / construct.Flag,
    'add_channelon1' / construct.Flag,
    'fsb' / construct.Flag,
    'charger' / construct.Flag,
    '_reserved1' / construct.BitsInteger(8),
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


class UspProtocol:
    columns = 'msg-id',
    c_width = 60,
    tlm_table = {
        u'Regular': {
            'table': (
                ('name', 'Name'),
                ('Usb1', 'Voltage SB #1, V'),
                ('Usb2', 'Voltage SB #2, V'),
                ('Usb3', 'Voltage SB #3, V'),
                ('Isb1', 'Current SB #1, mA'),
                ('Isb2', 'Current SB #2, mA'),
                ('Isb3', 'Current SB #3, mA'),
                ('Iab', 'Current battery, mA'),
                ('Ich1', 'Current Ch #1, mA'),
                ('Ich2', 'Current Ch #2, mA'),
                ('Ich3', 'Current Ch #3, mA'),
                ('Ich4', 'Current Ch #4, mA'),
                ('t1_pw', 'Temperature battery #1, °C'),
                ('t2_pw', 'Temperature battery #2, °C'),
                ('t3_pw', 'Temperature battery #3, °C'),
                ('t4_pw', 'Temperature battery #4, °C'),
                ('Uab', 'Voltage battery, V'),
                ('reg_tel_id', 'Telemetry SN'),
                ('Time', 'Time'),
                ('Nres', 'Reloads'),
                ('FL', 'Flags UHF'),
            ),
            'flags': (
                ('Uab_crit', 'Critical battery voltage'),
                ('Uab_min', 'Minimal battery voltage'),
                ('heater2_manual', 'Heater #2 manual'),
                ('heater1_manual', 'Heater #1 manual'),
                ('heater2_on', 'Heater #2 ON'),
                ('heater1_on', 'Heater #1 ON'),
                ('Tab_max', 'Maximal battery Temperature'),
                ('Tab_min', 'Minimal battery Temperature'),
                ('channelon4', 'Channel #4 ON'),
                ('channelon3', 'Channel #3 ON'),
                ('channelon2', 'Channel #2 ON'),
                ('channelon1', 'Channel #1 ON'),
                ('Ich_fault4', 'Channel #4 Fault'),
                ('Ich_fault3', 'Channel #3 Fault'),
                ('Ich_fault2', 'Channel #2 Fault'),
                ('Ich_fault1', 'Channel #1 Fault'),
                ('add_channelon3', 'Additional channel #3 ON'),
                ('add_channelon2', 'Additional channel #2 ON'),
                ('add_channelon1', 'Additional channel #1 ON'),
                ('fsb', 'Switch Error'),
                ('charger', 'Charger connected'),
            ),
        },
        u'Beacon': {
            'table': ...,
        }
    }
    tlm_table[u'Beacon']['table'] = tlm_table[u'Regular']['table'] + (
        ('t_amp', 'Temperature UHF amp, °C'),
        ('t_uhf', 'Temperature UHF, °C'),
        ('RSSIrx', 'RSSI Received, dBm'),
        ('RSSIidle', 'RSSI Idle, dBm'),
        ('Pf', 'Direct radiation power'),
        ('Pb', 'Back radiation power'),
        ('Nres_uhf', 'Reloads UHF'),
        ('Fl_uhf', 'Flags UHF'),
        ('Time_uhf', 'Time UHF'),
        ('UpTime', 'Uptime'),
        ('Current', 'Current UHF, mA'),
        ('Uuhf', 'Voltage UHF, V'),
    )
    tlm_table[u'Beacon']['flags'] = (
        ('Uab_crit', 'Critical battery voltage'),
        ('Uab_min', 'Minimal battery voltage'),
        ('heater2_manual', 'Heater #2 manual'),
        ('heater1_manual', 'Heater #1 manual'),
        ('heater2_on', 'Heater #2 ON'),
        ('heater1_on', 'Heater #1 ON'),
        ('Tab_max', 'Maximal battery Temperature'),
        ('Tab_min', 'Minimal battery Temperature'),
        ('channelon4', 'Channel #4 ON'),
        ('channelon3', 'Channel #3 ON'),
        ('channelon2', 'Channel #2 ON'),
        ('channelon1', 'Channel #1 ON'),
        ('Ich_limit4', 'Exceeding channel #4 current'),
        ('Ich_limit3', 'Exceeding channel #3 current'),
        ('Ich_limit2', 'Exceeding channel #2 current'),
        ('Ich_limit1', 'Exceeding channel #1 current'),
        ('charger', 'Charger connected'),
    )

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

            else:
                ty = 'raw'

            yield ty, self.get_sender_callsign(data), '0x%04X' % i.message, p_data
