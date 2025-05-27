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

__all__ = 'Cubebel2Protocol',

proto_name = 'cubebel-2'

"""
https://gitlab.com/librespacefoundation/satnogs/satnogs-decoders/-/blob/master/ksy/cubebel2.ksy
"""

voltage16u = common.LinearAdapter(1000, construct.Int16ul)
current16u = common.LinearAdapter(1000, construct.Int16ul)
temperature16u = common.LinearAdapter(100, construct.Int16ul)


mb_batt_element_telemetry = construct.Struct(
    'voltage' / voltage16u,
    'current' / current16u,
    'temp' / temperature16u,
)

mb_batt_telemetry = construct.Struct(
    'element0' / mb_batt_element_telemetry,
    'element1' / mb_batt_element_telemetry,
    'voltage' / voltage16u,
)

mb_solarpanel_telemetry = construct.Struct(
    # 'current' / construct.Int16ul,
    # 'volt_pos' / construct.Int16ul,
    # 'volt_neg' / construct.Int16ul,
    'vals' / construct.Array(3, construct.Int16ul),
)

mb_solarpanel_temp_telemetry = construct.Struct(
    'temp' / construct.Array(4, temperature16u),
)

mb_slot_telemetry = construct.Struct(
    'voltage' / voltage16u,
    'current' / current16u,
    'oc_cnt' / construct.Int8ul,
)

mb_power_switch_state = construct.Struct(
    'raw' / construct.Array(3, construct.Hex(construct.Int8ul)),
)


CDM_VERSION_GET_ANS = 32770
CDM_TELEMETRY_GET_ANS_MOTHERBOARD = 33169
CDM_TELEMETRY_GET_ANS_TRX = 33172
CDM_CONFIG_MOTHERBOARD_ANS_0 = 33179
CDM_CONFIG_TRX_ANS_0 = 33272
CDM_CONFIG_MOTHERBOARD_ANS_1 = 33369
CDM_CONFIG_TRX_ANS_1 = 33372
CDM_TRX_RFREPLY_ANS = 36770

cdm_version_get_ans = construct.Struct(
    '_name' / construct.Computed('cdm_version_get_ans'),
    'name' / construct.Computed('Version'),

    'version_githash' / construct.GreedyString('ascii'),
)

cdm_telemetry_get_ans_motherboard = construct.Struct(
    '_name' / construct.Computed('cdm_telemetry_get_ans_motherboard'),
    'name' / construct.Computed('Motherboard telemetry'),

    'time' / construct.Int16ul,
    'mcusr' / construct.Int8ul,
    'rst_cnt_total' / construct.Int8ul,
    'rst_cnt_iwdg' / construct.Int8ul,
    'adc_status' / construct.Hex(construct.Int8ul),
    'adc_temp_1' / temperature16u,
    'adc_temp_2' / temperature16u,
    'ant_1_v' / voltage16u,
    'ant_2_v' / voltage16u,
    'solar_common_v' / voltage16u,
    'sat_bus_v' / voltage16u,
    'sat_bus_c' / current16u,
    'uc_v' / voltage16u,
    'uc_c' / current16u,
    'battery_pack_0' / mb_batt_telemetry,
    'battery_pack_1' / mb_batt_telemetry,
    'solarpanel_0' / mb_solarpanel_telemetry,
    'solarpanel_1' / mb_solarpanel_telemetry,
    'solarpanel_2' / mb_solarpanel_telemetry,
    'solarpanel_3' / mb_solarpanel_telemetry,
    'solarpanel_4' / mb_solarpanel_telemetry,
    'solarpanel_5' / mb_solarpanel_telemetry,
    'slot_0' / mb_slot_telemetry,
    'slot_1' / mb_slot_telemetry,
    'slot_2' / mb_slot_telemetry,
    'slot_3' / mb_slot_telemetry,
    'slot_4' / mb_slot_telemetry,
    'slot_5' / mb_slot_telemetry,
    'slot_6' / mb_slot_telemetry,
    'slot_7' / mb_slot_telemetry,
    'slot_8' / mb_slot_telemetry,
    'solar_temp_0' / mb_solarpanel_temp_telemetry,
    'solar_temp_1' / mb_solarpanel_temp_telemetry,
    'solar_bus_oc_cnt' / construct.Int8ul,
    'batt_pack_oc_cnt' / construct.Array(2, construct.Int8ul),
    'power_switch_trx' / construct.Int16ul,
    'power_switch_state' / mb_power_switch_state,
)

cdm_telemetry_get_ans_trx = construct.Struct(
    '_name' / construct.Computed('cdm_telemetry_get_ans_trx'),
    'name' / construct.Computed('TRX telemetry'),

    'common_trx' / construct.Struct(
        'board_id_cdm' / construct.Int8ul,
        'board_rst_total_cnt' / construct.Int8ul,
        'board_rst_iwdg_cnt' / construct.Int8ul,
        'board_rst_iwdg_timestamp' / common.UNIXTimestampAdapter(construct.Int32ul),
        'mcu_rcc_csr' / construct.Int8ul,
        'mcu_uptime' / common.TimeDeltaAdapter(construct.Int32ul),
        'rtc_unixtime' / common.UNIXTimestampAdapter(construct.Int64sl),
        'rtc_bat' / construct.Float32l,
        'mcu_temp' / construct.Float32l,
    ),
    'board_id_modem' / construct.Int8ul,
    'board_vbus' / construct.Float32l,
    'startup_unixtime_previous' / common.UNIXTimestampAdapter(construct.Int32ul),
    'startup_unixtime_current' / common.UNIXTimestampAdapter(construct.Int32ul),
    'ds600_inited' / construct.Int8ul,
    'ds600_enabled' / construct.Int8ul,
    'ds600_temp' / construct.Float32l,
    'tmp75_inited' / construct.Int8ul,
    'tmp75_temp' / construct.Float32l,
    'ina226_pamp_inited' / construct.Int8ul,
    'ina226_pamp_current' / construct.Float32l,
    'ina226_temp_current_tx' / construct.Float32l,
    'ina226_pamp_voltage' / construct.Float32l,
    'ina226_temp_voltage_tx' / construct.Float32l,
    'tps2042_inited' / construct.Int8ul,
    'tps2042_ch1_enabled' / construct.Int8ul,
    'tps2042_ch1_oc' / construct.Int8ul,
    'tps2042_ch2_enabled' / construct.Int8ul,
    'tps2042_ch2_oc' / construct.Int8ul,
    'tps2032_inited' / construct.Int8ul,
    'tps2032_oc' / construct.Int8ul,
    'tps61078_inited' / construct.Int8ul,
    'tps61078_enabled' / construct.Int8ul,
    'modem_inited' / construct.Int8ul,
    'modem_state' / construct.Hex(construct.Int8ul),
    'modem_pwr_fwd' / construct.Float32l,
    'modem_pwr_rev' / construct.Float32l,
    'modem_rx_freq' / construct.Int32ul,
    'modem_rx_datarate' / construct.Int32ul,
    'modem_rx_mode' / construct.Hex(construct.Int8ul),
    'modem_rx_period_on' / common.TimeDeltaAdapter(construct.Int32ul),
    'modem_rx_period_off' / common.TimeDeltaAdapter(construct.Int32ul),
    'modem_rx_cnt_all' / construct.Int32ul,
    'modem_rx_cnt_valid' / construct.Int32ul,
    'modem_rx_seqnum' / construct.Int32ul,
    'modem_tx_freq' / construct.Int32ul,
    'modem_tx_datarate' / construct.Int32ul,
    'modem_tx_pwr' / construct.Int8sl,
    'modem_tx_cnt_all' / construct.Int32ul,
    'modem_cnt_digipeater_ax25' / construct.Int32ul,
    'modem_cnt_digipeater_greencube_rx' / construct.Int32ul,
    'modem_cnt_digipeater_greencube_tx' / construct.Int32ul,
    'text_msg' / construct.GreedyString('ascii'),
)

cdm_config_motherboard_record = construct.Struct(
    'id' / construct.Hex(construct.Int8ul),
    'va' / construct.Int16ul,
)

cdm_config_stm32l4_record = construct.Struct(
    'id' / construct.Hex(construct.Int8ul),
    'va' / construct.Hex(construct.Int32ul),
)

cdm_config_motherboard_ans = construct.Struct(
    '_name' / construct.Computed('cdm_config_motherboard_ans'),
    'name' / construct.Computed('Motherboard config'),

    'record_mb' / construct.GreedyRange(cdm_config_motherboard_record),
)

cdm_config_trx_ans = construct.Struct(
    '_name' / construct.Computed('cdm_config_trx_ans'),
    'name' / construct.Computed('TRX config'),

    'record_trx' / construct.GreedyRange(cdm_config_stm32l4_record),
)

cdm_trx_rfreply_ans = construct.Struct(
    '_name' / construct.Computed('cdm_trx_rfreply_ans'),
    'name' / construct.Computed('TRX RF reply'),

    'ax5043_timer' / common.TimeDeltaAdapter(construct.Int32ul),
    'ax5043_track_rf_freq' / construct.Int32ul,
    'ax5043_datarate' / construct.Int32ul,
    'ax5043_track_freq' / construct.Int16sl,
    'ax5043_rssi' / construct.Int8ul,
    'ax5043_agc' / construct.Int8ul,
    'ax5043_background_noise' / construct.Int8ul,
    'command_hash' / construct.Hex(construct.Bytes(28)),
    'command_key_idx' / construct.Int32ul,
    'command_seq_enabled' / construct.Int8ul,
    'command_seq_valid' / construct.Int8ul,
    'command_seq_num' / construct.Int16ul,
)

unknown = construct.Struct(
    '_name' / construct.Computed('unknown'),
    'name' / construct.Computed('Unknown'),

    'data' / construct.Hex(construct.GreedyBytes),
)

payloads = {
    CDM_VERSION_GET_ANS: cdm_version_get_ans,
    CDM_TELEMETRY_GET_ANS_MOTHERBOARD: cdm_telemetry_get_ans_motherboard,
    CDM_TELEMETRY_GET_ANS_TRX: cdm_telemetry_get_ans_trx,
    CDM_CONFIG_MOTHERBOARD_ANS_0: cdm_config_motherboard_ans,
    CDM_CONFIG_TRX_ANS_0: cdm_config_trx_ans,
    CDM_CONFIG_MOTHERBOARD_ANS_1: cdm_config_motherboard_ans,
    CDM_CONFIG_TRX_ANS_1: cdm_config_trx_ans,
    CDM_TRX_RFREPLY_ANS: cdm_trx_rfreply_ans,
}

trx_beacon = construct.Struct(
    'beacon_id' / construct.Int8ul,
    'beacon_uptime' / common.TimeDeltaAdapter(construct.Int32ul),
    'beacon_vbus' / voltage16u,
    'beacon_reset_total_cnt' / construct.Int8ul,
    'beacon_reset_iwdg_cnt' / construct.Int8ul,
    'beacon_reset_iwdg_time' / common.TimeDeltaAdapter(construct.Int32ul),
    'beacon_pamp_temp' / common.LinearAdapter(1000, construct.Int16ul),
    'beacon_rx_settings' / construct.Int8ul,
    'beacon_rx_period_on' / construct.Int16ul,
    'beacon_rx_seqnum' / construct.Int16ul,
    'beacon_rx_cnt_total' / construct.Int8ul,
    'beacon_rx_cnt_valid' / construct.Int8ul,
    'beacon_tx_settings' / construct.Int8ul,
    'beacon_tx_pwr' / construct.Int8sl,
    'beacon_tx_cnt' / construct.Int8ul,
)

cdm_header = construct.Struct(
    'cdm_id' / construct.Hex(construct.Int16ul),
    'cdm_addr_src' / construct.Hex(construct.Int8ul),
    'cdm_addr_dst' / construct.Hex(construct.Int8ul),
    'cdm_priority' / construct.Int8ul,
    'cdm_delay' / construct.Int16ul,
    'cdm_datalen' / construct.Int8ul,
)

frame = construct.Struct(
    'trx_beacon' / trx_beacon,
    'cdm_datalen' / construct.Int8ul,
    'cdm_header' / cdm_header,
    'cdm_payload' / construct.Switch(construct.this.cdm_header.cdm_id, payloads, default=unknown),
    '_tail' / construct.GreedyBytes,
)

cubebel2 = construct.Struct(
    'ax25' / construct.Peek(ax25.ax25_header),
    'ax25' / construct.If(lambda this: bool(this.ax25), ax25.ax25_header),
    'frame' / construct.If(lambda this: (bool(this.ax25) and this.ax25.pid == 0xF0), frame),
)


class Cubebel2Protocol(common.Protocol):
    columns = 'cdm_id',
    c_width = 60,
    has_ax25 = 1

    _beacon = (
        ('beacon_name', 'TRX Beacon'),
        ('beacon_id', 'ID',),
        ('beacon_uptime', 'Uptime',),
        ('beacon_vbus', 'Battery voltage, V',),
        ('beacon_reset_total_cnt', 'Resets total',),
        ('beacon_reset_iwdg_cnt', 'Resets IWDG',),
        ('beacon_reset_iwdg_time', 'Reset IWDG time',),
        ('beacon_pamp_temp', 'Pamp temperature, °C',),
        ('beacon_rx_settings', 'Rx settings',),
        ('beacon_rx_period_on', 'Rx period on',),
        ('beacon_rx_seqnum', 'Rx seqnum',),
        ('beacon_rx_cnt_total', 'Rx total count',),
        ('beacon_rx_cnt_valid', 'Rx valid count',),
        ('beacon_tx_settings', 'Tx settings',),
        ('beacon_tx_pwr', 'Tx power',),
        ('beacon_tx_cnt', 'Tx count',),
    )

    tlm_table = {
        'cdm_version_get_ans': {
            'table': (
                *_beacon,
                ('tlm_name', 'Version'),
                ('version_githash', 'Git hash'),
            ),
        },
        'cdm_telemetry_get_ans_motherboard': {
            'table': (
                *_beacon,
                ('tlm_name', 'Motherboard telemetry'),
                ('time', 'Time'),
                ('mcusr', 'MCUSR'),
                ('rst_cnt_total', 'Total resets'),
                ('rst_cnt_iwdg', 'IWDG resets'),
                ('adc_status', 'ADC status'),
                ('adc_temp_1', 'ADC #1 temperature, °C'),
                ('adc_temp_2', 'ADC #2 temperature, °C'),
                ('ant_1_v', ' Ant #1 voltage, V'),
                ('ant_2_v', ' Ant #2 voltage, V'),
                ('solar_common_v', 'Solar panel voltage, V'),
                ('sat_bus_v', 'Sat bus voltage, V'),
                ('sat_bus_c', 'Sat bus current, A'),
                ('uc_v', 'UC voltage, V'),
                ('uc_c', 'UC current, A'),
                ('battery_pack_0', 'Battery pack #1'),
                ('battery_pack_0/voltage', '... voltage, V'),
                ('battery_pack_0/element0', '... element #1'),
                ('battery_pack_0/element0/voltage', '... voltage, V'),
                ('battery_pack_0/element0/current', '... current, A'),
                ('battery_pack_0/element0/temp', '... temp, °C'),
                ('battery_pack_0/element1', '... element #2'),
                ('battery_pack_0/element1/voltage', '... voltage, V'),
                ('battery_pack_0/element1/current', '... current, A'),
                ('battery_pack_0/element1/temp', '... temp, °C'),
                ('battery_pack_1', 'Battery pack #2'),
                ('battery_pack_1/voltage', '... voltage, V'),
                ('battery_pack_1/element0', '... element #1'),
                ('battery_pack_1/element0/voltage', '... voltage, V'),
                ('battery_pack_1/element0/current', '... current, A'),
                ('battery_pack_1/element0/temp', '... temp, °C'),
                ('battery_pack_1/element1', '... element #2'),
                ('battery_pack_1/element1/voltage', '... voltage, V'),
                ('battery_pack_1/element1/current', '... current, A'),
                ('battery_pack_1/element1/temp', '... temp, °C'),
                ('solarpanel_0/vals', 'Solar panel #1 [curr, volt+, volt-]'),
                ('solarpanel_1/vals', 'Solar panel #2 [curr, volt+, volt-]'),
                ('solarpanel_2/vals', 'Solar panel #3 [curr, volt+, volt-]'),
                ('solarpanel_3/vals', 'Solar panel #4 [curr, volt+, volt-]'),
                ('solarpanel_4/vals', 'Solar panel #5 [curr, volt+, volt-]'),
                ('solarpanel_5/vals', 'Solar panel #6 [curr, volt+, volt-]'),
                ('slot_0', 'Slot #1'),
                ('slot_0/voltage', '... voltage, V'),
                ('slot_0/current', '... current, A'),
                ('slot_0/oc_cnt', '... OC cnt'),
                ('slot_1', 'Slot #2'),
                ('slot_1/voltage', '... voltage, V'),
                ('slot_1/current', '... current, A'),
                ('slot_1/oc_cnt', '... OC cnt'),
                ('slot_2', 'Slot #3'),
                ('slot_2/voltage', '... voltage, V'),
                ('slot_2/current', '... current, A'),
                ('slot_2/oc_cnt', '... OC cnt'),
                ('slot_3', 'Slot #4'),
                ('slot_3/voltage', '... voltage, V'),
                ('slot_3/current', '... current, A'),
                ('slot_3/oc_cnt', '... OC cnt'),
                ('slot_4', 'Slot #5'),
                ('slot_4/voltage', '... voltage, V'),
                ('slot_4/current', '... current, A'),
                ('slot_4/oc_cnt', '... OC cnt'),
                ('slot_5', 'Slot #6'),
                ('slot_5/voltage', '... voltage, V'),
                ('slot_5/current', '... current, A'),
                ('slot_5/oc_cnt', '... OC cnt'),
                ('slot_6', 'Slot #7'),
                ('slot_6/voltage', '... voltage, V'),
                ('slot_6/current', '... current, A'),
                ('slot_6/oc_cnt', '... OC cnt'),
                ('slot_7', 'Slot #8'),
                ('slot_7/voltage', '... voltage, V'),
                ('slot_7/current', '... current, A'),
                ('slot_7/oc_cnt', '... OC cnt'),
                ('slot_8', 'Slot #9'),
                ('slot_8/voltage', '... voltage, V'),
                ('slot_8/current', '... current, A'),
                ('slot_8/oc_cnt', '... OC cnt'),
                ('solar_temp_0/temp', 'Solar panel #1 temp, °C'),
                ('solar_temp_1/temp', 'Solar panel #2 temp, °C'),
                ('solar_bus_oc_cnt', 'Solar bus OC cnt'),
                ('batt_pack_oc_cnt', 'Battery pack OC cnt'),
                ('power_switch_trx', 'Power switch TRX'),
                ('power_switch_state/raw', 'Power switch state'),
            ),
        },
        'cdm_telemetry_get_ans_trx': {
            'table': (
                *_beacon,
                ('tlm_name', 'TRX telemetry'),
                ('sub_tlm_name0', 'Common'),
                ('common_trx/board_id_cdm', 'Board CMD'),
                ('common_trx/board_rst_total_cnt', 'Board total resets'),
                ('common_trx/board_rst_iwdg_cnt', 'Board IWDG resets'),
                ('common_trx/board_rst_iwdg_timestamp', 'Board IWDG reset time'),
                ('common_trx/mcu_rcc_csr', 'RCC CSR'),
                ('common_trx/mcu_uptime', 'MCU uptime'),
                ('common_trx/rtc_unixtime', 'RTC time'),
                ('common_trx/rtc_bat', 'RTC battery, V'),
                ('common_trx/mcu_temp', 'MCU temperature, °C'),
                ('sub_tlm_name1', '}'),

                ('board_id_modem', 'Board ID modem'),
                ('board_vbus', 'Board voltage, V'),
                ('startup_unixtime_previous', 'Previous startup time'),
                ('startup_unixtime_current', 'Current startup time'),
                ('ds600_inited', 'DS600 inited'),
                ('ds600_enabled', 'DS600 enabled'),
                ('ds600_temp', 'DS600 temperature, °C'),
                ('tmp75_inited', 'TMP75 inited'),
                ('tmp75_temp', 'TMP75 temperature, °C'),
                ('ina226_pamp_inited', 'INA226 pamp inited'),
                ('ina226_pamp_current', 'INA226 pamp current, A'),
                ('ina226_temp_current_tx', 'INA226 temp current TX, A'),
                ('ina226_pamp_voltage', 'INA226 pamp voltage, V'),
                ('ina226_temp_voltage_tx', 'INA226 temp voltage TX, V'),
                ('tps2042_inited', 'TPS2042 inited'),
                ('tps2042_ch1_enabled', 'TPS2042 ch1 enabled'),
                ('tps2042_ch1_oc', 'TPS2042 ch1 OC'),
                ('tps2042_ch2_enabled', 'TPS2042 ch2 enabled'),
                ('tps2042_ch2_oc', 'TPS2042 ch2 OC'),
                ('tps2032_inited', 'TPS2032 inited'),
                ('tps2032_oc', 'TPS2032 OC'),
                ('tps61078_inited', 'TPS61078 inited'),
                ('tps61078_enabled', 'TPS61078 enabled'),
                ('modem_inited', 'Modem inited'),
                ('modem_state', 'Modem state'),
                ('modem_pwr_fwd', 'Modem pwr fwd'),
                ('modem_pwr_rev', 'Modem pwr rev'),
                ('modem_rx_freq', 'Modem RX freq, Hz'),
                ('modem_rx_datarate', 'Modem RX datarate, bps'),
                ('modem_rx_mode', 'Modem RX mode'),
                ('modem_rx_period_on', 'Modem RX period on'),
                ('modem_rx_period_off', 'Modem RX period off'),
                ('modem_rx_cnt_all', 'Modem RX cnt all'),
                ('modem_rx_cnt_valid', 'Modem RX cnt valid'),
                ('modem_rx_seqnum', 'Modem RX seqnum'),
                ('modem_tx_freq', 'Modem TX freq, Hz'),
                ('modem_tx_datarate', 'Modem TX datarate, bps'),
                ('modem_tx_pwr', 'Modem TX pwr'),
                ('modem_tx_cnt_all', 'Modem TX cnt all'),
                ('modem_cnt_digipeater_ax25', 'Modem cnt digipeater ax25'),
                ('modem_cnt_digipeater_greencube_rx', 'Modem cnt digipeater Greencube RX'),
                ('modem_cnt_digipeater_greencube_tx', 'Modem cnt digipeater Greencube TX'),
                ('text_msg', 'Message'),
            ),
        },
        'cdm_config_motherboard_ans': {
            'table': (
                *_beacon,
                ('tlm_name', 'Motherboard config'),
                ('record_mb', 'MB record'),
            ),
        },
        'cdm_config_trx_ans': {
            'table': (
                *_beacon,
                ('tlm_name', 'TRX config'),
                ('record_trx', 'TRX record'),
            ),
        },
        'cdm_trx_rfreply_ans': {
            'table': (
                *_beacon,
                ('tlm_name', 'TRX RF reply'),
                ('ax5043_timer', 'AX5043 timer'),
                ('ax5043_track_rf_freq', 'AX5043 track rf freq Hz'),
                ('ax5043_datarate', 'AX5043 datarate, bps'),
                ('ax5043_track_freq', 'AX5043 track freq, Hz'),
                ('ax5043_rssi', 'AX5043 rssi'),
                ('ax5043_agc', 'AX5043 agc'),
                ('ax5043_background_noise', 'AX5043 background noise'),
                ('command_hash', 'Command hash'),
                ('command_key_idx', 'Command key idx'),
                ('command_seq_enabled', 'Command seq enabled'),
                ('command_seq_valid', 'Command seq valid'),
                ('command_seq_num', 'Command seq num'),
            ),
        },
        'unknown': {
            'table': (
                *_beacon,
                ('tlm_name', 'Unknown'),
                ('data', 'Data'),
            ),
        },
    }

    def recognize(self, bb):
        data = cubebel2.parse(bb)
        if not data.frame:
            return

        name = self.get_sender_callsign(data)
        _trx_beacon = {**data.frame.trx_beacon}
        _trx_beacon.pop('_io', 0)
        _cdm_payload = {**data.frame.cdm_payload}
        _cdm_payload.pop('_io', 0)
        if _cdm_payload['_name'] == 'unknown':
            _cdm_payload['data'] = utils.bytes2hex(_cdm_payload['data'])
        d = utils.Dict(
            beacon_name='',
            **_trx_beacon,
            tlm_name='',
            sub_tlm_name0='{',
            sub_tlm_name1='',
            **_cdm_payload,
        )

        yield 'tlm', name, '0x%04X' % data.frame.cdm_header.cdm_id, (data, d)
