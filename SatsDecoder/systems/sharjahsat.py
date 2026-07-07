#  Copyright (c) 2024. Alexander Baskikh
#
#  MIT License (MIT), http://opensource.org/licenses/MIT
#  Full license can be found in the LICENSE-MIT file
#
#  SPDX-License-Identifier: MIT

import construct

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

    def generate_fid(self, t=None):
        if not (self.current_fid and self.merge_mode):
            self.current_fid = f'SharjahSat-1_{self.strftime(t)}'
        return self.current_fid

    def get_image(self, force_new=0, soi=0, pnum=0, t=None, **kwargs):
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
                fid = self.generate_fid(t)
            img = self.new_file(fid)
            img.packets = pnum
            img.first_data_offset = 0

        img.has_soi |= soi
        return img

    def push_data(self, data, t=None, **kw):
        pack_num = data.hdr.packet_counter
        soi = data.data.startswith(b'\xff\xd8')
        eoi = pack_num == 1

        img = self.get_image(soi, soi, pack_num, t)
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
                ('name', 'Name', 0),
                ('restart_count', 'Restart count', 0),
                ('last_reset_cause', 'Last Reset Cause', 0),
                ('uptime', 'Uptime', 0),
                ('Time', 'Time', 0),

                ('board_temp1', 'Board Temp #1, °C', 1),
                ('board_temp2', 'Board Temp #2, °C', 2),
                ('board_temp3', 'Board Temp #3, °C', 2),
                ('vbat_v', 'vbat_v, V', 1),
                ('vbat_i', 'vbat_i, A', 1),
                ('vbat_plat_v', 'vbat_plat_v, V', 1),
                ('3v3_plat_v', '3v3_plat_v, V', 2),
                ('vbat_periph_i', 'vbat_periph_i, A', 1),
                ('3v3_periph_i', '3v3_periph_i, A', 2),
                ('vbat_periph_v', 'vbat_periph_v, V', 1),
                ('3v3_periph_v', '3v3_periph_v, V', 2),

                ('rtc_hh', 'RTC HH', 0),
                ('rtc_mm', 'RTC MM', 0),
                ('rtc_ss', 'RTC SS', 0),
                ('rtc_dd', 'RTC DD', 0),
                ('rtc_mo', 'RTC MO', 0),
                ('rtc_yy', 'RTC YY', 0),
                ('rtc_dow', 'RTC DOW', 0),
                ('rtc_temp', 'RTC Temperature, °C', 1),
                ('antenna_status', 'Antenna Status', 0),

                ('vbat', 'Battery Voltage, V', 1),
                ('ibat', 'Battery Current, mA', 1),
                ('vpcm3v3', 'PCM 3v3 Voltage, V', 1),
                ('vpcm5v', 'PCM 5v Voltage, V', 2),
                ('ipcm3v3', 'PCM 3v3 Current, mA', 1),
                ('ipcm5v', 'PCM 5v Current, mA', 2),
                ('tbrd', 'Board Temperature, °C', 1),
                ('tbat1', 'Battery #1 Temperature, °C', 1),
                ('tbat2', 'Battery #2 Temperature, °C', 2),
                ('tbat3', 'Battery #3 Temperature, °C', 2),

                ('eps_vpcmbatv', 'EPS PCM Battery Voltage, V', 1),
                ('eps_ipcmbatv', 'EPS PCM Battery Current, A', 1),
                ('eps_vpcm3v3', 'EPS PCM 3v3 Voltage, V', 1),
                ('eps_ipcm3v3', 'EPS PCM 3v3 Current, A', 1),
                ('eps_vpcm5v', 'EPS PCM 5v Voltage, V', 1),
                ('eps_ipcm5v', 'EPS PCM 5v Current, A', 1),
                ('eps_i3v3drw', 'EPS PCM 3v3 DRW Current, A', 1),
                ('eps_i5vdrw', 'EPS PCM 5v DRW Current, A', 2),
                ('eps_tbrd', 'EPS Board Temperature, °C', 1),
                ('eps_tbrd_db', 'EPS Board DB Temperature, °C', 2),
                ('eps_ipcm12v', 'EPS PCM 12v Current, A', 1),
                ('eps_vpcm12v', 'EPS PCM 12v Voltage, V', 1),

                ('adcs_state', 'ADCS State', 0),
                ('sat_pos_llh_lat', 'Sat llh lat, deg', 0),
                ('sat_pos_llh_lon', 'Sat llh lon, deg', 0),
                ('sat_pos_llh_alt', 'Sat llh alt, km', 1),
                ('estm_att_angle_yaw', 'Yaw, deg', 1),
                ('estm_att_angle_pitch', 'Pitch, deg', 2),
                ('estm_att_angle_roll', 'Roll, deg', 2),
                ('estm_ang_rate_yaw', 'Yaw rate, deg/s', 1),
                ('estm_ang_rate_pitch', 'Pitch rate, deg/s', 2),
                ('estm_ang_rate_roll', 'Roll rate, deg/s', 2),
                ('gps', 'ECEF Pos&Vel Vectors', 0),

                ('smps_temp', 'UHF/VHF SMPS Temperature, °C', 1),
                ('pa_temp', 'UHF/VHF PA Temperature, °C', 2),
                ('current_3v3', 'UHF/VHF 3v3 Current, uA', 1),
                ('voltage_3v3', 'UHF/VHF 3v3 Voltage, mV', 1),
                ('current_5v', 'UHF/VHF 5v Current, uA', 1),
                ('voltage_5v', 'UHF/VHF 5v Voltage, mV', 1),

                ('battery_current', 'S-Band Battery Current, uA', 1),
                ('pa_current', 'S-Band PA Current, uA', 2),
                ('battery_voltage', 'S-Band Battery Voltage, mV', 1),
                ('pa_voltage', 'S-Band PA Voltage, mV', 2),
                ('pa_temperature', 'S-Band PA Temperature, °C', 1),
                ('rf_output_power', 'S-Band RF Output power, Vdet', 1),
                ('board_temp_top', 'S-Band Board Temp top, °C', 1),
                ('board_temp_bottom', 'S-Band Board Temp bottom, °C', 2),

                ('vbcr1', 'SP #1 Voltage, V', 1),
                ('vbcr2', 'SP #2 Voltage, V', 2),
                ('vbcr3', 'SP #3 Voltage, V', 2),
                ('vbcr4', 'SP #4 Voltage, V', 2),
                ('vbcr5', 'SP #5 Voltage, V', 2),
                ('vbcr6', 'SP #6 Voltage, V', 2),
                ('vbcr7', 'SP #7 Voltage, V', 2),
                ('vbcr8', 'SP #8 Voltage, V', 2),
                ('vbcr9', 'SP #9 Voltage, V', 2),
                ('ibcra1', 'SP #a1 Current, A', 1),
                ('ibcra2', 'SP #a2 Current, A', 2),
                ('ibcra3', 'SP #a3 Current, A', 2),
                ('ibcra4', 'SP #a4 Current, A', 2),
                ('ibcra5', 'SP #a5 Current, A', 2),
                ('ibcra6', 'SP #a6 Current, A', 2),
                ('ibcra7', 'SP #a7 Current, A', 2),
                ('ibcra8', 'SP #a8 Current, A', 2),
                ('ibcra9', 'SP #a9 Current, A', 2),
                ('ibcrb1', 'SP #b1 Current, A', 2),
                ('ibcrb2', 'SP #b2 Current, A', 2),
                ('ibcrb3', 'SP #b3 Current, A', 2),
                ('ibcrb4', 'SP #b4 Current, A', 2),
                ('ibcrb5', 'SP #b5 Current, A', 2),
                ('ibcrb6', 'SP #b6 Current, A', 2),
                ('ibcrb7', 'SP #b7 Current, A', 2),
                ('ibcrb8', 'SP #b8 Current, A', 2),
                ('ibcrb9', 'SP #b9 Current, A', 2),
                ('tbcra1', 'SP #a1 Temperature, °C', 1),
                ('tbcra2', 'SP #a2 Temperature, °C', 2),
                ('tbcra3', 'SP #a3 Temperature, °C', 2),
                ('tbcra4', 'SP #a4 Temperature, °C', 2),
                ('tbcra5', 'SP #a5 Temperature, °C', 2),
                ('tbcra6', 'SP #a6 Temperature, °C', 2),
                ('tbcra7', 'SP #a7 Temperature, °C', 2),
                ('tbcra8', 'SP #a8 Temperature, °C', 2),
                ('tbcra9', 'SP #a9 Temperature, °C', 2),
                ('tbcrb1', 'SP #b1 Temperature, °C', 2),
                ('tbcrb2', 'SP #b2 Temperature, °C', 2),
                ('tbcrb3', 'SP #b3 Temperature, °C', 2),
                ('tbcrb4', 'SP #b4 Temperature, °C', 2),
                ('tbcrb5', 'SP #b5 Temperature, °C', 2),
                ('tbcrb6', 'SP #b6 Temperature, °C', 2),
                ('tbcrb7', 'SP #b7 Temperature, °C', 2),
                ('tbcrb8', 'SP #b8 Temperature, °C', 2),
                ('tbcrb9', 'SP #b9 Temperature, °C', 2),
                ('vidiodeout', 'I-Diode Voltage, V', 1),
                ('iidiodeout', 'I-Diode Current, A', 1),
            ),
            'flags': (
                ('battery', 'Battery', 0),
                ('eps', 'EPS', 0),
                ('adcs', 'ADCS', 0),
                ('uv_modem', 'U/V Modem', 0),
                ('sband', 'S-Band', 0),
                ('ixrd', 'iXRD', 0),
                ('cam2mp', 'CAM2MP', 0),
                ('cam5mp', 'CAM5MP', 0),
                ('if_board', 'IF Board', 0),
                ('rtc', 'RTC', 0),
                ('beacon', 'Beacon', 0),
                ('antennas', 'Antennas', 0),
                ('op_mode', 'Op Mode', 0),
            ),
        },
    }

    def __init__(self, outdir):
        super().__init__(SharjahImageReceiver(outdir))

    def recognize(self, bb, t=None):
        while bb:
            data = sharjah.parse(bb)
            if not data.ax25:
                return

            if not data.hdr:
                return

            name = self.get_sender_callsign(data)
            bb = data._tail
            if data.hdr.tm_id == IMG_ID:
                x = self.ir.push_data(data, t)
                if x:
                    yield 'img', name, (x, self.ir.cur_img)

            elif data.hdr.tm_id == TLM_ID:
                yield 'tlm', name, (data, data.data)

            elif data._id == 'RESE':
                self.ir.reset()
