#  Copyright (c) 2024. Alexander Baskikh
#
#  MIT License (MIT), http://opensource.org/licenses/MIT
#  Full license can be found in the LICENSE-MIT file
#
#  SPDX-License-Identifier: MIT

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
        ('beacon_name', 'TRX Beacon', 0),
        ('beacon_id', 'ID', 0),
        ('beacon_uptime', 'Uptime', 0),
        ('beacon_vbus', 'Battery voltage, V', 0),
        ('beacon_reset_total_cnt', 'Resets total', 0),
        ('beacon_reset_iwdg_cnt', 'Resets IWDG', 0),
        ('beacon_reset_iwdg_time', 'Reset IWDG time', 0),
        ('beacon_pamp_temp', 'Pamp temperature, °C', 0),
        ('beacon_rx_settings', 'Rx settings', 0),
        ('beacon_rx_period_on', 'Rx period on', 0),
        ('beacon_rx_seqnum', 'Rx seqnum', 0),
        ('beacon_rx_cnt_total', 'Rx total count', 0),
        ('beacon_rx_cnt_valid', 'Rx valid count', 0),
        ('beacon_tx_settings', 'Tx settings', 0),
        ('beacon_tx_pwr', 'Tx power', 0),
        ('beacon_tx_cnt', 'Tx count', 0),
    )

    tlm_table = {
        'cdm_version_get_ans': {
            'table': (
                *_beacon,
                ('tlm_name', 'Version', 0),
                ('version_githash', 'Git hash', 0),
            ),
        },
        'cdm_telemetry_get_ans_motherboard': {
            'table': (
                *_beacon,
                ('tlm_name', 'Motherboard telemetry', 0),
                ('time', 'Time', 0),
                ('mcusr', 'MCUSR', 0),
                ('rst_cnt_total', 'Total resets', 0),
                ('rst_cnt_iwdg', 'IWDG resets', 0),
                ('adc_status', 'ADC status', 0),
                ('adc_temp_1', 'ADC #1 temperature, °C', 0),
                ('adc_temp_2', 'ADC #2 temperature, °C', 0),
                ('ant_1_v', ' Ant #1 voltage, V', 0),
                ('ant_2_v', ' Ant #2 voltage, V', 0),
                ('solar_common_v', 'Solar panel voltage, V', 0),
                ('sat_bus_v', 'Sat bus voltage, V', 0),
                ('sat_bus_c', 'Sat bus current, A', 0),
                ('uc_v', 'UC voltage, V', 0),
                ('uc_c', 'UC current, A', 0),
                ('battery_pack_0', 'Battery pack #1', 0),
                ('battery_pack_0/voltage', '... voltage, V', 0),
                ('battery_pack_0/element0', '... element #1', 0),
                ('battery_pack_0/element0/voltage', '... voltage, V', 0),
                ('battery_pack_0/element0/current', '... current, A', 0),
                ('battery_pack_0/element0/temp', '... temp, °C', 0),
                ('battery_pack_0/element1', '... element #2', 0),
                ('battery_pack_0/element1/voltage', '... voltage, V', 0),
                ('battery_pack_0/element1/current', '... current, A', 0),
                ('battery_pack_0/element1/temp', '... temp, °C', 0),
                ('battery_pack_1', 'Battery pack #2', 0),
                ('battery_pack_1/voltage', '... voltage, V', 0),
                ('battery_pack_1/element0', '... element #1', 0),
                ('battery_pack_1/element0/voltage', '... voltage, V', 0),
                ('battery_pack_1/element0/current', '... current, A', 0),
                ('battery_pack_1/element0/temp', '... temp, °C', 0),
                ('battery_pack_1/element1', '... element #2', 0),
                ('battery_pack_1/element1/voltage', '... voltage, V', 0),
                ('battery_pack_1/element1/current', '... current, A', 0),
                ('battery_pack_1/element1/temp', '... temp, °C', 0),
                ('solarpanel_0/vals', 'Solar panel #1 [curr, volt+, volt-]', 0),
                ('solarpanel_1/vals', 'Solar panel #2 [curr, volt+, volt-]', 0),
                ('solarpanel_2/vals', 'Solar panel #3 [curr, volt+, volt-]', 0),
                ('solarpanel_3/vals', 'Solar panel #4 [curr, volt+, volt-]', 0),
                ('solarpanel_4/vals', 'Solar panel #5 [curr, volt+, volt-]', 0),
                ('solarpanel_5/vals', 'Solar panel #6 [curr, volt+, volt-]', 0),
                ('slot_0', 'Slot #1', 0),
                ('slot_0/voltage', '... voltage, V', 0),
                ('slot_0/current', '... current, A', 0),
                ('slot_0/oc_cnt', '... OC cnt', 0),
                ('slot_1', 'Slot #2', 0),
                ('slot_1/voltage', '... voltage, V', 0),
                ('slot_1/current', '... current, A', 0),
                ('slot_1/oc_cnt', '... OC cnt', 0),
                ('slot_2', 'Slot #3', 0),
                ('slot_2/voltage', '... voltage, V', 0),
                ('slot_2/current', '... current, A', 0),
                ('slot_2/oc_cnt', '... OC cnt', 0),
                ('slot_3', 'Slot #4', 0),
                ('slot_3/voltage', '... voltage, V', 0),
                ('slot_3/current', '... current, A', 0),
                ('slot_3/oc_cnt', '... OC cnt', 0),
                ('slot_4', 'Slot #5', 0),
                ('slot_4/voltage', '... voltage, V', 0),
                ('slot_4/current', '... current, A', 0),
                ('slot_4/oc_cnt', '... OC cnt', 0),
                ('slot_5', 'Slot #6', 0),
                ('slot_5/voltage', '... voltage, V', 0),
                ('slot_5/current', '... current, A', 0),
                ('slot_5/oc_cnt', '... OC cnt', 0),
                ('slot_6', 'Slot #7', 0),
                ('slot_6/voltage', '... voltage, V', 0),
                ('slot_6/current', '... current, A', 0),
                ('slot_6/oc_cnt', '... OC cnt', 0),
                ('slot_7', 'Slot #8', 0),
                ('slot_7/voltage', '... voltage, V', 0),
                ('slot_7/current', '... current, A', 0),
                ('slot_7/oc_cnt', '... OC cnt', 0),
                ('slot_8', 'Slot #9', 0),
                ('slot_8/voltage', '... voltage, V', 0),
                ('slot_8/current', '... current, A', 0),
                ('slot_8/oc_cnt', '... OC cnt', 0),
                ('solar_temp_0/temp', 'Solar panel #1 temp, °C', 0),
                ('solar_temp_1/temp', 'Solar panel #2 temp, °C', 0),
                ('solar_bus_oc_cnt', 'Solar bus OC cnt', 0),
                ('batt_pack_oc_cnt', 'Battery pack OC cnt', 0),
                ('power_switch_trx', 'Power switch TRX', 0),
                ('power_switch_state/raw', 'Power switch state', 0),
            ),
        },
        'cdm_telemetry_get_ans_trx': {
            'table': (
                *_beacon,
                ('tlm_name', 'TRX telemetry', 0),
                ('sub_tlm_name0', 'Common', 0),
                ('common_trx/board_id_cdm', 'Board CMD', 0),
                ('common_trx/board_rst_total_cnt', 'Board total resets', 0),
                ('common_trx/board_rst_iwdg_cnt', 'Board IWDG resets', 0),
                ('common_trx/board_rst_iwdg_timestamp', 'Board IWDG reset time', 0),
                ('common_trx/mcu_rcc_csr', 'RCC CSR', 0),
                ('common_trx/mcu_uptime', 'MCU uptime', 0),
                ('common_trx/rtc_unixtime', 'RTC time', 0),
                ('common_trx/rtc_bat', 'RTC battery, V', 0),
                ('common_trx/mcu_temp', 'MCU temperature, °C', 0),
                ('sub_tlm_name1', '}', 0),

                ('board_id_modem', 'Board ID modem', 0),
                ('board_vbus', 'Board voltage, V', 0),
                ('startup_unixtime_previous', 'Previous startup time', 0),
                ('startup_unixtime_current', 'Current startup time', 0),
                ('ds600_inited', 'DS600 inited', 0),
                ('ds600_enabled', 'DS600 enabled', 0),
                ('ds600_temp', 'DS600 temperature, °C', 0),
                ('tmp75_inited', 'TMP75 inited', 0),
                ('tmp75_temp', 'TMP75 temperature, °C', 0),
                ('ina226_pamp_inited', 'INA226 pamp inited', 0),
                ('ina226_pamp_current', 'INA226 pamp current, A', 0),
                ('ina226_temp_current_tx', 'INA226 temp current TX, A', 0),
                ('ina226_pamp_voltage', 'INA226 pamp voltage, V', 0),
                ('ina226_temp_voltage_tx', 'INA226 temp voltage TX, V', 0),
                ('tps2042_inited', 'TPS2042 inited', 0),
                ('tps2042_ch1_enabled', 'TPS2042 ch1 enabled', 0),
                ('tps2042_ch1_oc', 'TPS2042 ch1 OC', 0),
                ('tps2042_ch2_enabled', 'TPS2042 ch2 enabled', 0),
                ('tps2042_ch2_oc', 'TPS2042 ch2 OC', 0),
                ('tps2032_inited', 'TPS2032 inited', 0),
                ('tps2032_oc', 'TPS2032 OC', 0),
                ('tps61078_inited', 'TPS61078 inited', 0),
                ('tps61078_enabled', 'TPS61078 enabled', 0),
                ('modem_inited', 'Modem inited', 0),
                ('modem_state', 'Modem state', 0),
                ('modem_pwr_fwd', 'Modem pwr fwd', 0),
                ('modem_pwr_rev', 'Modem pwr rev', 0),
                ('modem_rx_freq', 'Modem RX freq, Hz', 0),
                ('modem_rx_datarate', 'Modem RX datarate, bps', 0),
                ('modem_rx_mode', 'Modem RX mode', 0),
                ('modem_rx_period_on', 'Modem RX period on', 0),
                ('modem_rx_period_off', 'Modem RX period off', 0),
                ('modem_rx_cnt_all', 'Modem RX cnt all', 0),
                ('modem_rx_cnt_valid', 'Modem RX cnt valid', 0),
                ('modem_rx_seqnum', 'Modem RX seqnum', 0),
                ('modem_tx_freq', 'Modem TX freq, Hz', 0),
                ('modem_tx_datarate', 'Modem TX datarate, bps', 0),
                ('modem_tx_pwr', 'Modem TX pwr', 0),
                ('modem_tx_cnt_all', 'Modem TX cnt all', 0),
                ('modem_cnt_digipeater_ax25', 'Modem cnt digipeater ax25', 0),
                ('modem_cnt_digipeater_greencube_rx', 'Modem cnt digipeater Greencube RX', 0),
                ('modem_cnt_digipeater_greencube_tx', 'Modem cnt digipeater Greencube TX', 0),
                ('text_msg', 'Message', 0),
            ),
        },
        'cdm_config_motherboard_ans': {
            'table': (
                *_beacon,
                ('tlm_name', 'Motherboard config', 0),
                ('record_mb', 'MB record', 0),
            ),
        },
        'cdm_config_trx_ans': {
            'table': (
                *_beacon,
                ('tlm_name', 'TRX config', 0),
                ('record_trx', 'TRX record', 0),
            ),
        },
        'cdm_trx_rfreply_ans': {
            'table': (
                *_beacon,
                ('tlm_name', 'TRX RF reply', 0),
                ('ax5043_timer', 'AX5043 timer', 0),
                ('ax5043_track_rf_freq', 'AX5043 track rf freq Hz', 0),
                ('ax5043_datarate', 'AX5043 datarate, bps', 0),
                ('ax5043_track_freq', 'AX5043 track freq, Hz', 0),
                ('ax5043_rssi', 'AX5043 rssi', 0),
                ('ax5043_agc', 'AX5043 agc', 0),
                ('ax5043_background_noise', 'AX5043 background noise', 0),
                ('command_hash', 'Command hash', 0),
                ('command_key_idx', 'Command key idx', 0),
                ('command_seq_enabled', 'Command seq enabled', 0),
                ('command_seq_valid', 'Command seq valid', 0),
                ('command_seq_num', 'Command seq num', 0),
            ),
        },
        'unknown': {
            'table': (
                *_beacon,
                ('tlm_name', 'Unknown', 0),
                ('data', 'Data', 0),
            ),
        },
    }

    def recognize(self, bb, t=None):
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
