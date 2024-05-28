#  Copyright (c) 2024. Alexander Baskikh
#  #  MIT License (MIT), http://opensource.org/licenses/MIT  #  Full license can be found in the LICENSE-MIT file
#  #  SPDX-License-Identifier: MIT

import construct

from SatsDecoder.systems import csp, common

__all__ = 'GreenCubeProtocol',

proto_name = 'greencube'

"""
https://www.s5lab.space/index.php/decoding-ledsat-2/
"""


val_x10 = common.LinearAdapter(10, construct.Int16sb)
val_x100 = common.LinearAdapter(100, construct.Int16sb)
val_x1000000 = common.LinearAdapter(1000000, construct.Int32sb)

tlm_id_enums_v1 = {
    'Current telemetry': 0x3610,
    'Stored telemetry': 0x3611,
    'Beacon': 0x3612,
}

greencube_tlm = construct.Struct(
    '_name' / construct.Computed('greencube_tlm'),
    'name' / construct.Computed('Telemetry'),

    'id' / construct.Hex(construct.Enum(construct.Int16ub, **tlm_id_enums_v1)),  # U, 2, Telemetry Identifier
    'time_ms' / construct.Int16ub,  # U, 2, Millisecond part of the unix time, ms
    'Time' / common.UNIXTimestampAdapter(construct.Int32ub),  # U, 4, On-board unix time, s
    'proctime' / construct.Int16ub,  # U, 2, Time taken to process the telemetry, ms
    'eps_vboost_0' / construct.Int16ub,  # U, 2, Voltage of X axis solar panels, mV
    'eps_vboost_1' / construct.Int16ub,  # U, 2, Voltage of Y axis solar panels, mV
    'eps_cboost_0' / construct.Int16ub,  # U, 2, Current of X axis solar panels, mA
    'eps_cboost_1' / construct.Int16ub,  # U, 2, Current of Y axis solar panels, mA
    'eps_bootcause' / construct.Hex(construct.Int8ub),  # U, 1, EPS bootcause
    'eps_temp_0' / construct.Int8sb,  # S, 1, Temperature of X axis MPPT, °C
    'eps_temp_1' / construct.Int8sb,  # S, 1, Temperature of Y axis MPPT, °C
    'eps_temp_2' / construct.Int8sb,  # S, 1, Temperature of EPS board, °C
    'eps_temp_3' / construct.Int8sb,  # S, 1, Temperature of battery pack #1, °C
    'eps_temp_4' / construct.Int8sb,  # S, 1, Temperature of battery pack #2, °C
    'eps_temp_5' / construct.Int8sb,  # S, 1, Temperature of battery pack #3, °C
    'eps_cursun' / construct.Int16ub,  # U, 2, Total current from the solar panels, mA
    'eps_cursys' / construct.Int16ub,  # U, 2, Total current absorbed by the system, mA
    'eps_vbatt' / construct.Int16ub,  # U, 2, Battery voltage, mV
    'eps_outputs' / construct.Hex(construct.Int8ub),  # U, 1, Status of EPS outputs
    'radio_temp_pa' / construct.Int8sb,  # S, 1, Temperature of transceiver PA, °C
    'radio_tx_count' / construct.Int16ub,  # U, 2, Transceiver total TX count
    'radio_rx_count' / construct.Int16ub,  # U, 2, Transceiver total RX count
    'radio_last_rssi' / construct.Int16sb,  # S, 2, Last radio-contact RSSI, dBm
    'obc_bootcounter' / construct.Int16ub,  # U, 2, OBC bootcounter
    'radio_bootcounter' / construct.Int16ub,  # U, 2, Radio bootcounter
    'eps_bootcounter' / construct.Int16ub,  # U, 2, EPS bootcounter
    'payload_rx_count' / construct.Int8ub,  # U, 1, Packets from the payload
    'payload_tx_count' / construct.Int8ub,  # U, 1, Packets to the payload
    'software_status' / construct.Hex(construct.Int8ub),  # U, 1, Software status flag
    'heater_status' / construct.Hex(construct.Int8ub),  # U, 1, Heater status flag
    'obc_temp_0' / construct.Int8ub,  # U, 1, OBC temperature, °C
    'obc_gyro_0' / val_x100,  # S, 2, Gyroscope X, x100, °/s
    'obc_gyro_1' / val_x100,  # S, 2, Gyroscope Y, x100, °/s
    'obc_gyro_2' / val_x100,  # S, 2, Gyroscope Z, x100, °/s
    'obc_mag_0' / val_x10,  # S, 2, Magnetometer X, x10, mG
    'obc_mag_1' / val_x10,  # S, 2, Magnetometer Y, x10, mG
    'obc_mag_2' / val_x10,  # S, 2, Magnetometer Z, x10, mG
    'pan_spt_0' / construct.Int8sb,  # S, 1, Temperature of +X solar panel, °C
    'pan_spt_1' / construct.Int8sb,  # S, 1, Temperature of +Y solar panel, °C
    'pan_spt_2' / construct.Int8sb,  # S, 1, Temperature of -X solar panel, °C
    'pan_spt_3' / construct.Int8sb,  # S, 1, Temperature of -Y solar panel, °C
    'pan_css_0' / construct.Int16ub,  # U, 2, Coarse Sun sensor +X, mV
    'pan_css_1' / construct.Int16ub,  # U, 2, Coarse Sun sensor +Y, mV
    'pan_css_2' / construct.Int16ub,  # U, 2, Coarse Sun sensor +Z, mV
    'pan_css_3' / construct.Int16ub,  # U, 2, Coarse Sun sensor -X, mV
    'gps_status_flag' / construct.Hex(construct.Int8ub),  # U, 1, GPS status flag
    'gps_fix_time' / construct.Int32ub,  # U, 4, GPS fix time
    'gps_lat' / val_x1000000,  # I, 4, GPS Latitude, x1000000
    'gps_lon' / val_x1000000,  # I, 4, GPS Longitude, x1000000
    'gps_alt' / val_x1000000,  # I, 4, GPS Altitude, x1000000, km
    'sband_tx_cnt' / construct.Int16ub,  # U, 2, S-Band TX Count
    'antenna_status' / construct.Hex(construct.Int16ub),  # U, 2, Antenna status flag
    'acs_state' / construct.Hex(construct.Int8ub),  # U, 1, ACS state flag
    'acs_param' / construct.Hex(construct.Int8ub),  # U, 1, ACS parameters flag
)

greencube_msg = construct.Struct(
    '_name' / construct.Computed('greencube_msg'),
    'name' / construct.Computed('Message'),

    'msg' / construct.GreedyString('utf-8'),
)

GREENCUBE_NAMED_ID = 0x1D03
ids_map = {
    GREENCUBE_NAMED_ID: greencube_msg,
}

greencube_default_packet = construct.Struct(
    '_name' / construct.Computed('greencube_default_packet'),

    'id' / construct.Hex(construct.Int16ub),
    'data' / construct.Switch(construct.this.id, ids_map, default=construct.GreedyBytes),
)

GREENCUBE_TLM_DPORT = 8
packets_map = {
    GREENCUBE_TLM_DPORT: greencube_tlm,
}

greencube = construct.Struct(
    'packet' / construct.Switch(construct.this._params.csp_hdr.dest_port, packets_map, default=greencube_default_packet),
)


class GreenCubeProtocol(common.Protocol):
    NAME = 'GreenCube'
    columns = 'from', 'to', 'id'
    c_width = 40, 40, 40

    tlm_table = {
        'greencube_tlm': {
            'table': (
                ('name', 'Name'),
                ('id', 'Telemetry Identifier'),
                ('time_ms', 'Millisecond part of the unix time, ms'),
                ('Time', 'On-board unix time'),
                ('proctime', 'Time taken to process the telemetry, ms'),
                ('eps_vboost_0', 'Voltage of X axis solar panels, mV'),
                ('eps_vboost_1', 'Voltage of Y axis solar panels, mV'),
                ('eps_cboost_0', 'Current of X axis solar panels, mA'),
                ('eps_cboost_1', 'Current of Y axis solar panels, mA'),
                ('eps_bootcause', 'EPS bootcause'),
                ('eps_temp_0', 'Temperature of X axis MPPT, °C'),
                ('eps_temp_1', 'Temperature of Y axis MPPT, °C'),
                ('eps_temp_2', 'Temperature of EPS board, °C'),
                ('eps_temp_3', 'Temperature of battery pack #1, °C'),
                ('eps_temp_4', 'Temperature of battery pack #2, °C'),
                ('eps_temp_5', 'Temperature of battery pack #3, °C'),
                ('eps_cursun', 'Total current from the solar panels, mA'),
                ('eps_cursys', 'Total current absorbed by the system, mA'),
                ('eps_vbatt', 'Battery voltage, mV'),
                ('eps_outputs', 'Status of EPS outputs'),
                ('radio_temp_pa', 'Temperature of transceiver PA, °C'),
                ('radio_tx_count', 'Transceiver total TX count'),
                ('radio_rx_count', 'Transceiver total RX count'),
                ('radio_last_rssi', 'Last radio-contact RSSI, dBm'),
                ('obc_bootcounter', 'OBC bootcounter'),
                ('radio_bootcounter', 'Radio bootcounter'),
                ('eps_bootcounter', 'EPS bootcounter'),
                ('payload_rx_count', 'Packets from the payload'),
                ('payload_tx_count', 'Packets to the payload'),
                ('software_status', 'Software status flag'),
                ('heater_status', 'Heater status flag'),
                ('obc_temp_0', 'OBC temperature, °C'),
                ('obc_gyro_0', 'Gyroscope X, °/s'),
                ('obc_gyro_1', 'Gyroscope Y, °/s'),
                ('obc_gyro_2', 'Gyroscope Z, °/s'),
                ('obc_mag_0', 'Magnetometer X, mG'),
                ('obc_mag_1', 'Magnetometer Y, mG'),
                ('obc_mag_2', 'Magnetometer Z, mG'),
                ('pan_spt_0', 'Temperature of +X solar panel, °C'),
                ('pan_spt_1', 'Temperature of +Y solar panel, °C'),
                ('pan_spt_2', 'Temperature of -X solar panel, °C'),
                ('pan_spt_3', 'Temperature of -Y solar panel, °C'),
                ('pan_css_0', 'Coarse Sun sensor +X, mV'),
                ('pan_css_1', 'Coarse Sun sensor +Y, mV'),
                ('pan_css_2', 'Coarse Sun sensor +Z, mV'),
                ('pan_css_3', 'Coarse Sun sensor -X, mV'),
                ('gps_status_flag', 'GPS status flag'),
                ('gps_fix_time', 'GPS fix time'),
                ('gps_lat', 'GPS Latitude'),
                ('gps_lon', 'GPS Longitude'),
                ('gps_alt', 'GPS Altitude, km'),
                ('sband_tx_cnt', 'S-Band TX Count'),
                ('antenna_status', 'Antenna status flag'),
                ('acs_state', 'ACS state flag'),
                ('acs_param', 'ACS parameters flag'),
            ),
        },
        'greencube_msg': {
            'table': (
                ('name', 'Name'),
                ('msg', 'Message'),
            ),
        },
        'greencube_default_packet': {
            'table': (
                ('id', 'ID'),
                ('data', 'Data'),
            ),
        },
    }

    def recognize(self, bb):
        csp_packet = csp.csp.parse(bb)
        raw_greencube = csp_packet.data
        if not (csp_packet.hdr and raw_greencube):
            return

        csp_packet.data = s = greencube.parse(raw_greencube, csp_hdr=csp_packet.hdr)
        args = [
            'raw',
            self.NAME,
            f'{csp_packet.hdr.src}-{csp_packet.hdr.src_port}',
            f'{csp_packet.hdr.dest}-{csp_packet.hdr.dest_port}',
            hasattr(s.packet, 'id') and f'{s.packet.id:02X}' or None,
            raw_greencube,
        ]

        if csp_packet.hdr.dest_port in packets_map:
            args[0] = 'tlm'
            args[-1] = csp_packet, s.packet
            yield tuple(args)

        elif s.packet.id in ids_map:
            args[0] = 'tlm'
            args[-1] = csp_packet, s.packet.data
            yield tuple(args)

        else:
            yield tuple(args)
