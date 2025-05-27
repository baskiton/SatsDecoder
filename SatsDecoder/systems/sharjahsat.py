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

__all__ = 'SharjahProtocol',

proto_name = 'sharjahsat'


common_enum = construct.Enum(construct.Flag, **{n: i for i, n in enumerate(['Error', 'Working Correctly'])})
antennas_enum = construct.Enum(construct.Flag, **{n: i for i, n in enumerate(['Non-Deployed', 'All Deployed'])})
op_mode_enum = construct.Enum(construct.BitsInteger(4),
                              **{n: i for i, n in enumerate(['Startup', 'Nominal', 'Safe',
                                                             'ADCS Calibration', 'Recovery', 'Sun Pointing',
                                                             'Camera Operation', 'XRD Operation', 'Diagnostics', ])}
                              )

op_mode_f = construct.BitStruct(
    'cam5mp' / common_enum,
    'cam2mp' / common_enum,
    'ixrd' / common_enum,
    'sband' / common_enum,
    'uv_modem' / common_enum,
    'adcs' / common_enum,
    'eps' / common_enum,
    'battery' / common_enum,

    'op_mode' / op_mode_enum,
    'antennas' / antennas_enum,
    'beacon' / common_enum,
    'rtc' / common_enum,
    'if_board' / common_enum,
)

sharjah_tlm = construct.Struct(
    '_name' / construct.Computed('eser'),
    'name' / construct.Computed('ESER Telemetry'),

    # system info
    'flags0' / op_mode_f,
    'restart_count' / construct.Int16ul,
    'last_reset_cause' / construct.Hex(construct.Int8ul),
    'uptime' / common.TimeDeltaAdapter(construct.Int32ul),
    'Time' / common.UNIXTimestampAdapter(construct.Int32ul),

    # obc
    'board_temp1' / common.LinearAdapter(100, construct.Int16sl),   # deg C
    'board_temp2' / common.LinearAdapter(100, construct.Int16sl),   # deg C
    'board_temp3' / common.LinearAdapter(100, construct.Int16sl),   # deg C
    'vbat_v' / common.LinearAdapter(1000, construct.Int16ul),       # V
    'vbat_i' / common.LinearAdapter(1000, construct.Int16ul),       # A
    'vbat_plat_v' / common.LinearAdapter(1000, construct.Int16ul),  # V
    '3v3_plat_v' / common.LinearAdapter(1000, construct.Int16ul),   # V
    'vbat_periph_i' / common.LinearAdapter(100, construct.Int16ul), # A
    '3v3_periph_i' / common.LinearAdapter(100, construct.Int16ul),  # A
    'vbat_periph_v' / common.LinearAdapter(1000, construct.Int16ul),  # V
    '3v3_periph_v' / common.LinearAdapter(1000, construct.Int16ul),   # V

    # rtc
    'rtc_hh' / construct.Int8ul,
    'rtc_mm' / construct.Int8ul,
    'rtc_ss' / construct.Int8ul,
    'rtc_dd' / construct.Int8ul,
    'rtc_mo' / construct.Int8ul,
    'rtc_yy' / construct.Int8ul,
    'rtc_dow' / construct.Int8ul,
    'rtc_temp' / common.LinearAdapter(100, construct.Int16sl),
    'antenna_status' / construct.Hex(construct.Int8ul),

    # battery
    'vbat' / common.EvalAdapter('x*0.008993', construct.Int16ul),       # V
    'ibat' / common.EvalAdapter('x*14.662757', construct.Int16sl),     # mA
    'vpcm3v3' / common.EvalAdapter('x*0.004311', construct.Int16ul),    # V
    'vpcm5v' / common.EvalAdapter('x*0.005865', construct.Int16ul),     # V
    'ipcm3v3' / common.EvalAdapter('x*1.327547', construct.Int16ul),   # mA
    'ipcm5v' / common.EvalAdapter('x*1.327547', construct.Int16ul),    # mA
    'tbrd' / common.EvalAdapter('(x*0.372434)-273.15', construct.Int16sl),   # deg C
    'tbat1' / common.EvalAdapter('(x*0.3976)-238.57', construct.Int16sl),    # deg C
    'tbat2' / common.EvalAdapter('(x*0.3976)-238.57', construct.Int16sl),    # deg C
    'tbat3' / common.EvalAdapter('(x*0.3976)-238.57', construct.Int16sl),    # deg C

    # eps
    'eps_vpcmbatv' / common.EvalAdapter('x*0.008978', construct.Int16ul),       # V
    'eps_ipcmbatv' / common.EvalAdapter('x*0.00681988679', construct.Int16sl),  # A
    'eps_vpcm3v3' / common.EvalAdapter('x*0.004311', construct.Int16ul),        # V
    'eps_ipcm3v3' / common.EvalAdapter('x*0.00681988679', construct.Int16ul),   # A
    'eps_vpcm5v' / common.EvalAdapter('x*0.005865', construct.Int16ul),         # V
    'eps_ipcm5v' / common.EvalAdapter('x*0.00681988679', construct.Int16ul),    # A
    'eps_i3v3drw' / common.EvalAdapter('x*0.001327547', construct.Int16ul),     # A
    'eps_i5vdrw' / common.EvalAdapter('x*0.001327547', construct.Int16ul),      # A
    'eps_tbrd' / common.EvalAdapter('(x*0.372434)-273.15', construct.Int16ul),  # deg C
    'eps_tbrd_db' / common.EvalAdapter('(x*0.372434)-273.15', construct.Int16ul),    # deg C
    'eps_ipcm12v' / common.EvalAdapter('x*0.002066632361', construct.Int16ul),  # A
    'eps_vpcm12v' / common.EvalAdapter('x*0.01349', construct.Int16ul),         # V

    # adcs
    'adcs_state' / construct.Hex(construct.Int8ul),
    'sat_pos_llh_lat' / common.EvalAdapter('x*0.01', construct.Int16sl),  # deg
    'sat_pos_llh_lon' / common.EvalAdapter('x*0.01', construct.Int16sl),  # deg
    'sat_pos_llh_alt' / common.EvalAdapter('x*0.01', construct.Int16sl),   # km
    'estm_att_angle_yaw' / common.EvalAdapter('x*0.01', construct.Int16sl),   # deg
    'estm_att_angle_pitch' / common.EvalAdapter('x*0.01', construct.Int16sl), # deg
    'estm_att_angle_roll' / common.EvalAdapter('x*0.01', construct.Int16sl),  # deg
    'estm_ang_rate_yaw' / common.EvalAdapter('x*0.01', construct.Int16sl),  # deg/s
    'estm_ang_rate_pitch' / common.EvalAdapter('x*0.01', construct.Int16sl),    # deg/s
    'estm_ang_rate_roll' / common.EvalAdapter('x*0.01', construct.Int16sl), # deg/s
    'gps' / construct.Bytes(18),    # ECEF Position & Velocity Vectors

    # uhf/vhf modem
    'smps_temp' / construct.Int8sl,  # deg C
    'pa_temp' / construct.Int8sl,    # deg C
    'current_3v3' / common.EvalAdapter('x*3', construct.Int16ul),   # uA
    'voltage_3v3' / common.EvalAdapter('x*4', construct.Int16ul),   # mV
    'current_5v' / common.EvalAdapter('x*62', construct.Int16ul),   # uA
    'voltage_5v' / common.EvalAdapter('x*4', construct.Int16ul),    # mV

    # S-Band modem
    'battery_current' / common.EvalAdapter('x*40', construct.Int16ul),  # uA
    'pa_current' / common.EvalAdapter('x*40', construct.Int16ul),       # uA
    'battery_voltage' / common.EvalAdapter('x*4', construct.Int16ul),   # mV
    'pa_voltage' / common.EvalAdapter('x*4', construct.Int16ul),        # mV
    'pa_temperature' / common.EvalAdapter('((x*3/4096)-0.5)*100', construct.Int16ul),   # deg C
    'rf_output_power' / common.EvalAdapter('x*0.00113932291', construct.Int16ul),   # V det
    'board_temp_top' / common.EvalAdapter('x*0.00390625', construct.Int16sl),       # deg C
    'board_temp_bottom' / common.EvalAdapter('x*0.00390625', construct.Int16sl),    # deg C

    # solar panels
    'vbcr1' / common.EvalAdapter('x*0.0322581', construct.Int16ul),     # V
    'vbcr2' / common.EvalAdapter('x*0.0322581', construct.Int16ul),     # V
    'vbcr3' / common.EvalAdapter('x*0.0099706', construct.Int16ul),     # V
    'vbcr4' / common.EvalAdapter('x*0.0322581', construct.Int16ul),     # V
    'vbcr5' / common.EvalAdapter('x*0.0322581', construct.Int16ul),     # V
    'vbcr6' / common.EvalAdapter('x*0.0322581', construct.Int16ul),     # V
    'vbcr7' / common.EvalAdapter('x*0.0322581', construct.Int16ul),     # V
    'vbcr8' / common.EvalAdapter('x*0.0322581', construct.Int16ul),     # V
    'vbcr9' / common.EvalAdapter('x*0.0322581', construct.Int16ul),     # V
    'ibcra1' / common.EvalAdapter('x*0.0009775', construct.Int16ul),    # A
    'ibcra2' / common.EvalAdapter('x*0.0009775', construct.Int16ul),    # A
    'ibcra3' / common.EvalAdapter('x*0.0009775', construct.Int16ul),    # A
    'ibcra4' / common.EvalAdapter('x*0.0009775', construct.Int16ul),    # A
    'ibcra5' / common.EvalAdapter('x*0.0009775', construct.Int16ul),    # A
    'ibcra6' / common.EvalAdapter('x*0.0009775', construct.Int16ul),    # A
    'ibcra7' / common.EvalAdapter('x*0.0009775', construct.Int16ul),    # A
    'ibcra8' / common.EvalAdapter('x*0.0009775', construct.Int16ul),    # A
    'ibcra9' / common.EvalAdapter('x*0.0009775', construct.Int16ul),    # A
    'ibcrb1' / common.EvalAdapter('x*0.0009775', construct.Int16ul),    # A
    'ibcrb2' / common.EvalAdapter('x*0.0009775', construct.Int16ul),    # A
    'ibcrb3' / common.EvalAdapter('x*0.0009775', construct.Int16ul),    # A
    'ibcrb4' / common.EvalAdapter('x*0.0009775', construct.Int16ul),    # A
    'ibcrb5' / common.EvalAdapter('x*0.0009775', construct.Int16ul),    # A
    'ibcrb6' / common.EvalAdapter('x*0.0009775', construct.Int16ul),    # A
    'ibcrb7' / common.EvalAdapter('x*0.0009775', construct.Int16ul),    # A
    'ibcrb8' / common.EvalAdapter('x*0.0009775', construct.Int16ul),    # A
    'ibcrb9' / common.EvalAdapter('x*0.0009775', construct.Int16ul),    # A
    'tbcra1' / common.EvalAdapter('(x*0.4963)-273.15', construct.Int16sl),  # deg C
    'tbcra2' / common.EvalAdapter('(x*0.4963)-273.15', construct.Int16sl),  # deg C
    'tbcra3' / common.EvalAdapter('(x*0.4963)-273.15', construct.Int16sl),  # deg C
    'tbcra4' / common.EvalAdapter('(x*0.4963)-273.15', construct.Int16sl),  # deg C
    'tbcra5' / common.EvalAdapter('(x*0.4963)-273.15', construct.Int16sl),  # deg C
    'tbcra6' / common.EvalAdapter('(x*0.4963)-273.15', construct.Int16sl),  # deg C
    'tbcra7' / common.EvalAdapter('(x*0.4963)-273.15', construct.Int16sl),  # deg C
    'tbcra8' / common.EvalAdapter('(x*0.4963)-273.15', construct.Int16sl),  # deg C
    'tbcra9' / common.EvalAdapter('(x*0.4963)-273.15', construct.Int16sl),  # deg C
    'tbcrb1' / common.EvalAdapter('(x*0.4963)-273.15', construct.Int16sl),  # deg C
    'tbcrb2' / common.EvalAdapter('(x*0.4963)-273.15', construct.Int16sl),  # deg C
    'tbcrb3' / common.EvalAdapter('(x*0.4963)-273.15', construct.Int16sl),  # deg C
    'tbcrb4' / common.EvalAdapter('(x*0.4963)-273.15', construct.Int16sl),  # deg C
    'tbcrb5' / common.EvalAdapter('(x*0.4963)-273.15', construct.Int16sl),  # deg C
    'tbcrb6' / common.EvalAdapter('(x*0.4963)-273.15', construct.Int16sl),  # deg C
    'tbcrb7' / common.EvalAdapter('(x*0.4963)-273.15', construct.Int16sl),  # deg C
    'tbcrb8' / common.EvalAdapter('(x*0.4963)-273.15', construct.Int16sl),  # deg C
    'tbcrb9' / common.EvalAdapter('(x*0.4963)-273.15', construct.Int16sl),  # deg C
    'vidiodeout' / common.EvalAdapter('x*0.008993157', construct.Int16ul),  # V
    'iidiodeout' / common.EvalAdapter('x*0.014662757', construct.Int16ul),  # A
)

IMG_ID = 0x41
TLM_ID = 0x50

_data_map = {
    IMG_ID: construct.Bytes(construct.this.hdr.data_length),
    TLM_ID: sharjah_tlm,
}

eser_hdr = construct.Struct(
    'iden' / construct.OneOf(construct.PaddedString(4, 'ascii'), ['ESER']),
    'tm_id' / construct.Hex(construct.Int8ul),
    'data_length' / construct.Int8ul,
    'packet_counter' / construct.Int32ul,
)

rese_hdr = construct.Struct(
    'iden' / construct.OneOf(construct.PaddedString(4, 'ascii'), ['RESE']),
    'tm_id' / construct.Hex(construct.Int8ul),  # 0xff
    # 'data_length' / construct.Computed(4),
    'data' / construct.Bytes(4),
)

sharjah = construct.Struct(
    'ax25' / construct.Peek(ax25.ax25_header),
    'ax25' / construct.If(construct.this.ax25, ax25.ax25_header),
    '_id' / construct.If(construct.this.ax25, construct.Peek(construct.PaddedString(4, 'ascii'))),
    'hdr' / construct.Switch(construct.this._id, {'ESER': eser_hdr, 'RESE': rese_hdr}),
    'data' / construct.If(construct.this._id == 'ESER', construct.Switch(construct.this.hdr.tm_id, _data_map)),
    '_tail' / construct.GreedyBytes
)


class SharjahImageReceiver(ImageReceiver):
    PACKET_SIZE = 246

    def __init__(self, outdir):
        super().__init__(outdir, '.jpg')

    def generate_fid(self):
        if not (self.current_fid and self.merge_mode):
            self.last_date = now = dt.datetime.now()
            self.current_fid = f'SharjahSat-1_{now.strftime("%Y-%m-%d_%H-%M-%S,%f")}'
        return self.current_fid

    def get_image(self, force_new=0, soi=0, pnum=0, **kwargs):
        fid = self.current_fid
        img = self.images.get(fid)
        if img:
            if pnum > img.packets:
                if img.has_soi:
                    self.current_fid = fid = ''
                    force_new = 1
                else:
                    img.shift_image((pnum - img.packets) * self.PACKET_SIZE)
                    img.packets = pnum

            elif soi and pnum < img.packets:
                self.current_fid = fid = ''
                force_new = 1

        if force_new or not img:
            if not fid:
                fid = self.generate_fid()
            img = self.new_file(fid)
            img.packets = pnum
            img.first_data_offset = 0

        img.has_soi |= soi
        return img

    def push_data(self, data, **kw):
        pack_num = data.hdr.packet_counter
        soi = data.data.startswith(b'\xff\xd8')
        eoi = pack_num == 1

        img = self.get_image(soi, soi, pack_num)
        with img.lock:
            off = (img.packets - pack_num) * self.PACKET_SIZE
            img.push_data(off, data.data)
            if eoi:
                img.flush()
                return 2

        return 1

    def reset(self):
        img = self.cur_img
        if img:
            img.flush()
        if not self.merge_mode:
            self.current_fid = ''


class SharjahProtocol(common.Protocol):
    columns = ()
    c_width = ()
    has_ax25 = 1

    tlm_table = {
        'eser': {
            'table': (
                ('name', 'Name'),
                ('restart_count', 'Restart count'),
                ('last_reset_cause', 'Last Reset Cause'),
                ('uptime', 'Uptime'),
                ('Time', 'Time'),

                ('board_temp1', 'Board Temp #1, °C'),
                ('board_temp2', 'Board Temp #2, °C'),
                ('board_temp3', 'Board Temp #3, °C'),
                ('vbat_v', 'vbat_v, V'),
                ('vbat_i', 'vbat_i, A'),
                ('vbat_plat_v', 'vbat_plat_v, V'),
                ('3v3_plat_v', '3v3_plat_v, V'),
                ('vbat_periph_i', 'vbat_periph_i, A'),
                ('3v3_periph_i', '3v3_periph_i, A'),
                ('vbat_periph_v', 'vbat_periph_v, V'),
                ('3v3_periph_v', '3v3_periph_v, V'),

                ('rtc_hh', 'RTC HH'),
                ('rtc_mm', 'RTC MM'),
                ('rtc_ss', 'RTC SS'),
                ('rtc_dd', 'RTC DD'),
                ('rtc_mo', 'RTC MO'),
                ('rtc_yy', 'RTC YY'),
                ('rtc_dow', 'RTC DOW'),
                ('rtc_temp', 'RTC Temperature, °C'),
                ('antenna_status', 'Antenna Status'),

                ('vbat', 'Battery Voltage, V'),
                ('ibat', 'Battery Current, mA'),
                ('vpcm3v3', 'PCM 3v3 Voltage, V'),
                ('vpcm5v', 'PCM 5v Voltage, V'),
                ('ipcm3v3', 'PCM 3v3 Current, mA'),
                ('ipcm5v', 'PCM 5v Current, mA'),
                ('tbrd', 'Board Temperature, °C'),
                ('tbat1', 'Battery #1 Temperature, °C'),
                ('tbat2', 'Battery #2 Temperature, °C'),
                ('tbat3', 'Battery #3 Temperature, °C'),

                ('eps_vpcmbatv', 'EPS PCM Battery Voltage, V'),
                ('eps_ipcmbatv', 'EPS PCM Battery Current, A'),
                ('eps_vpcm3v3', 'EPS PCM 3v3 Voltage, V'),
                ('eps_ipcm3v3', 'EPS PCM 3v3 Current, A'),
                ('eps_vpcm5v', 'EPS PCM 5v Voltage, V'),
                ('eps_ipcm5v', 'EPS PCM 5v Current, A'),
                ('eps_i3v3drw', 'EPS PCM 3v3 DRW Current, A'),
                ('eps_i5vdrw', 'EPS PCM 5v DRW Current, A'),
                ('eps_tbrd', 'EPS Board Temperature, °C'),
                ('eps_tbrd_db', 'EPS Board DB Temperature, °C'),
                ('eps_ipcm12v', 'EPS PCM 12v Current, A'),
                ('eps_vpcm12v', 'EPS PCM 12v Voltage, V'),

                ('adcs_state', 'ADCS State'),
                ('sat_pos_llh_lat', 'Sat llh lat, deg'),
                ('sat_pos_llh_lon', 'Sat llh lon, deg'),
                ('sat_pos_llh_alt', 'Sat llh alt, km'),
                ('estm_att_angle_yaw', 'Yaw, deg'),
                ('estm_att_angle_pitch', 'Pitch, deg'),
                ('estm_att_angle_roll', 'Roll, deg'),
                ('estm_ang_rate_yaw', 'Yaw rate, deg/s'),
                ('estm_ang_rate_pitch', 'Pitch rate, deg/s'),
                ('estm_ang_rate_roll', 'Roll rate, deg/s'),
                ('gps', 'ECEF Pos&Vel Vectors'),

                ('smps_temp', 'UHF/VHF SMPS Temperature, °C'),
                ('pa_temp', 'UHF/VHF PA Temperature, °C'),
                ('current_3v3', 'UHF/VHF 3v3 Current, uA'),
                ('voltage_3v3', 'UHF/VHF 3v3 Voltage, mV'),
                ('current_5v', 'UHF/VHF 5v Current, uA'),
                ('voltage_5v', 'UHF/VHF 5v Voltage, mV'),

                ('battery_current', 'S-Band Battery Current, uA'),
                ('pa_current', 'S-Band PA Current, uA'),
                ('battery_voltage', 'S-Band Battery Voltage, mV'),
                ('pa_voltage', 'S-Band PA Voltage, mV'),
                ('pa_temperature', 'S-Band PA Temperature, °C'),
                ('rf_output_power', 'S-Band RF Output power, Vdet'),
                ('board_temp_top', 'S-Band Board Temp top, °C'),
                ('board_temp_bottom', 'S-Band Board Temp bottom, °C'),

                ('vbcr1', 'SP #1 Voltage, V'),
                ('vbcr2', 'SP #2 Voltage, V'),
                ('vbcr3', 'SP #3 Voltage, V'),
                ('vbcr4', 'SP #4 Voltage, V'),
                ('vbcr5', 'SP #5 Voltage, V'),
                ('vbcr6', 'SP #6 Voltage, V'),
                ('vbcr7', 'SP #7 Voltage, V'),
                ('vbcr8', 'SP #8 Voltage, V'),
                ('vbcr9', 'SP #9 Voltage, V'),
                ('ibcra1', 'SP #a1 Current, A'),
                ('ibcra2', 'SP #a2 Current, A'),
                ('ibcra3', 'SP #a3 Current, A'),
                ('ibcra4', 'SP #a4 Current, A'),
                ('ibcra5', 'SP #a5 Current, A'),
                ('ibcra6', 'SP #a6 Current, A'),
                ('ibcra7', 'SP #a7 Current, A'),
                ('ibcra8', 'SP #a8 Current, A'),
                ('ibcra9', 'SP #a9 Current, A'),
                ('ibcrb1', 'SP #b1 Current, A'),
                ('ibcrb2', 'SP #b2 Current, A'),
                ('ibcrb3', 'SP #b3 Current, A'),
                ('ibcrb4', 'SP #b4 Current, A'),
                ('ibcrb5', 'SP #b5 Current, A'),
                ('ibcrb6', 'SP #b6 Current, A'),
                ('ibcrb7', 'SP #b7 Current, A'),
                ('ibcrb8', 'SP #b8 Current, A'),
                ('ibcrb9', 'SP #b9 Current, A'),
                ('tbcra1', 'SP #a1 Temperature, °C'),
                ('tbcra2', 'SP #a2 Temperature, °C'),
                ('tbcra3', 'SP #a3 Temperature, °C'),
                ('tbcra4', 'SP #a4 Temperature, °C'),
                ('tbcra5', 'SP #a5 Temperature, °C'),
                ('tbcra6', 'SP #a6 Temperature, °C'),
                ('tbcra7', 'SP #a7 Temperature, °C'),
                ('tbcra8', 'SP #a8 Temperature, °C'),
                ('tbcra9', 'SP #a9 Temperature, °C'),
                ('tbcrb1', 'SP #b1 Temperature, °C'),
                ('tbcrb2', 'SP #b2 Temperature, °C'),
                ('tbcrb3', 'SP #b3 Temperature, °C'),
                ('tbcrb4', 'SP #b4 Temperature, °C'),
                ('tbcrb5', 'SP #b5 Temperature, °C'),
                ('tbcrb6', 'SP #b6 Temperature, °C'),
                ('tbcrb7', 'SP #b7 Temperature, °C'),
                ('tbcrb8', 'SP #b8 Temperature, °C'),
                ('tbcrb9', 'SP #b9 Temperature, °C'),
                ('vidiodeout', 'I-Diode Voltage, V'),
                ('iidiodeout', 'I-Diode Current, A'),
            ),
            'flags': (
                ('battery', 'Battery'),
                ('eps', 'EPS'),
                ('adcs', 'ADCS'),
                ('uv_modem', 'U/V Modem'),
                ('sband', 'S-Band'),
                ('ixrd', 'iXRD'),
                ('cam2mp', 'CAM2MP'),
                ('cam5mp', 'CAM5MP'),
                ('if_board', 'IF Board'),
                ('rtc', 'RTC'),
                ('beacon', 'Beacon'),
                ('antennas', 'Antennas'),
                ('op_mode', 'Op Mode'),
            ),
        },
    }

    def __init__(self, outdir):
        super().__init__(SharjahImageReceiver(outdir))

    def recognize(self, bb):
        while bb:
            data = sharjah.parse(bb)
            if not data.ax25:
                return

            if not data.hdr:
                return

            name = self.get_sender_callsign(data)
            bb = data._tail
            if data.hdr.tm_id == IMG_ID:
                x = self.ir.push_data(data)
                if x:
                    yield 'img', name, (x, self.ir.cur_img)

            elif data.hdr.tm_id == TLM_ID:
                yield 'tlm', name, (data, data.data)

            elif data._id == 'RESE':
                self.ir.reset()
