#  Copyright (c) 2024. Alexander Baskikh
#
#  MIT License (MIT), http://opensource.org/licenses/MIT
#  Full license can be found in the LICENSE-MIT file
#
#  SPDX-License-Identifier: MIT

import construct

from SatsDecoder.systems import csp, common
from SatsDecoder.systems.image_receiver import ImageReceiver

__all__ = 'LedsatProtocol',

proto_name = 'ledsat'

"""
https://www.s5lab.space/index.php/decoding-ledsat/
"""


val_x10 = common.LinearAdapter(10, construct.Int16sb)
val_x10neg = common.LinearAdapter(-10, construct.Int16sb)
val_x100 = common.LinearAdapter(100, construct.Int16sb)
val_x100neg = common.LinearAdapter(-100, construct.Int16sb)
val_x1000000 = common.LinearAdapter(1000000, construct.Int32sb)

tlm_id_enums_v1 = {
    'Current telemetry': 0x1628,
    'Stored telemetry': 0x1629,
    'Beacon': 0x162A,
}

ledsat_tlm = construct.Struct(
    '_name' / construct.Computed('ledsat_tlm'),
    'name' / construct.Computed('Telemetry'),

    'id' / construct.Hex(construct.Enum(construct.Int16ub, **tlm_id_enums_v1)),  # U, 2, Telemetry Identifier
    'time_ms' / construct.Int16ub,  # U, 2, Millisecond part of the unix time, ms
    'Time' / common.UNIXTimestampAdapter(construct.Int32ub),  # U, 4, On-board unix time, s
    'proctime' / construct.Int16ub,  # U, 2, Time taken to process the telemetry, ms
    'eps_vboost_0' / construct.Int16ub,  # U, 2, Voltage of the X axis solar panels, mV
    'eps_vboost_1' / construct.Int16ub,  # U, 2, Voltage of the Y axis solar panels, mV
    'eps_vboost_2' / construct.Int16ub,  # U, 2, Voltage of the Z axis solar panels, mV
    'eps_cboost_0' / construct.Int16ub,  # U, 2, Current of the X axis solar panels, mA
    'eps_cboost_1' / construct.Int16ub,  # U, 2, Current of the Y axis solar panels, mA
    'eps_cboost_2' / construct.Int16ub,  # U, 2, Current of the Z axis solar panels, mA
    'eps_bootcause' / construct.Int8ub,  # U, 1, EPS bootcause
    'eps_battmode' / construct.Int8ub,  # U, 1, EPS battery mode
    'eps_temp_0' / construct.Int16sb,  # S, 2, Temperature of the X axis MPPT, °C
    'eps_temp_1' / construct.Int16sb,  # S, 2, Temperature of the Y axis MPPT, °C
    'eps_temp_2' / construct.Int16sb,  # S, 2, Temperature of the Z axis MPPT, °C
    'eps_temp_3' / construct.Int16sb,  # S, 2, Temperature of battery pack #1, °C
    'eps_temp_4' / construct.Int16sb,  # S, 2, Temperature of battery pack #2, °C
    'eps_temp_5' / construct.Int16sb,  # S, 2, Temperature of battery pack #3, °C
    'eps_cursun' / construct.Int16ub,  # U, 2, Total current coming from solar panels, mA
    'eps_cursys' / construct.Int16ub,  # U, 2, Total current absobred by system, mA
    'eps_vbatt' / construct.Int16ub,  # U, 2, Battery voltage, mV
    'eps_gpscur' / common.LinearAdapter(0.15, construct.Int8ub),  # U, 1, GPS current draw, x0,15, mA
    '_pad0' / construct.Int8ub,  # U, 1, Padding
    'eps_bootcounter' / construct.Int16ub,  # U, 2, EPS bootcount
    'radio_temp_pa' / construct.Int16sb,  # S, 2, Temperature of transceiver PA, 10, °C
    'radio_tx_count' / construct.Int32ub,  # U, 4, Transceiver total TX count
    'radio_rx_count' / construct.Int32ub,  # U, 4, Transceiver total RX count
    'radio_last_rssi' / construct.Int16sb,  # S, 2, Last radio-contact RSSI, dBm
    'radio_bootcounter' / construct.Int16ub,  # U, 2, Radio bootcounter
    'obc_temp_0' / construct.Int16sb,  # S, 2, OBC temperature #1, 10, °C
    'obc_temp_1' / construct.Int16sb,  # S, 2, OBC temperature #2, 10, °C
    'obc_gyro_0' / val_x100,  # S, 2, Gyroscope X, x100, °/s
    'obc_gyro_1' / val_x100,  # S, 2, Gyroscope Y, x100, °/s
    'obc_gyro_2' / val_x100,  # S, 2, Gyroscope Z, x100, °/s
    'obc_mag_0' / val_x10,  # S, 2, Magnetometer X, x10, mG
    'obc_mag_1' / val_x10,  # S, 2, Magnetometer Y, x10, mG
    'obc_mag_2' / val_x10,  # S, 2, Magnetometer Z, x10, mG
    'pan_spt_0' / val_x100,  # S, 2, Temperature of the +X solar panel, x100, °C
    'pan_spt_1' / val_x100,  # S, 2, Temperature of the +Y solar panel, x100, °C
    'pan_spt_2' / val_x100,  # S, 2, Temperature of the -X solar panel, x100, °C
    'pan_spt_3' / val_x100,  # S, 2, Temperature of the -Y solar panel, x100, °C
    'pan_spt_4' / val_x100,  # S, 2, Temperature of the +Z solar panel, x100, °C
    'pan_spt_5' / val_x100,  # S, 2, Temperature of the -Z solar panel, x100, °C
    'pan_css_0' / construct.Int16ub,  # U, 2, Coarse Sun Sensor +X, mV
    'pan_css_1' / construct.Int16ub,  # U, 2, Coarse Sun Sensor +Y, mV
    'pan_css_2' / construct.Int16ub,  # U, 2, Coarse Sun Sensor +Z, mV
    'pan_css_3' / construct.Int16ub,  # U, 2, Coarse Sun Sensor -X, mV
    'pan_css_4' / construct.Int16ub,  # U, 2, Coarse Sun Sensor -Y, mV
    'pan_css_5' / construct.Int16ub,  # U, 2, Coarse Sun Sensor -Z, mV
    'eps_outputs' / construct.Int8ub,  # U, 1, EPS output status
    '_pad1' / construct.Int8ub,  # U, 1, Padding
    'obc_bootcounter' / construct.Int16sb,  # S, 2, OBC bootcounter
    'led_status' / construct.Int8ub,  # U, 1, Status of the LEDs
    'gps_status_flag' / construct.Int8ub,  # U, 1, GPS Status Flag
    '_pad2' / construct.Int8ub,  # U, 1, Padding
    '_pad3' / construct.Int8ub,  # U, 1, Padding
    'gps_fix_time' / construct.Int32ub,  # U, 4, GPS fix time (UNIX)
    'gps_lat' / val_x1000000,  # S, 4, GPS Latitude, x1000000, °
    'gps_lon' / val_x1000000,  # S, 4, GPS Longitude, x1000000, °
    'gps_alt' / construct.Int32sb,  # S, 4, GPS Altitude, m
    'software_status' / construct.Int8ub,  # U, 1, Software status flag
    '_pad4' / construct.Int8ub,  # U, 1, Padding
    'ext_gyro_0' / val_x100neg,  # S, 2, External Gyroscope X, x-100, °/s
    'ext_gyro_1' / val_x100neg,  # S, 2, External Gyroscope Y, x-100, °/s
    'ext_gyro_2' / val_x100,  # S, 2, External Gyroscope Z, x100, °/s
    'ext_mag_0' / val_x10neg,  # S, 2, External Magnetometer X, x-10, mG
    'ext_mag_1' / val_x10neg,  # S, 2, External Magnetometer Y, x-10, mG
    'ext_mag_2' / val_x10,  # S, 2, External Magnetometer Z, x10, mG
    '_pad5' / construct.Int16ub,  # U, 2, Padding

)

ledsat_default_packet = construct.Struct(
    '_name' / construct.Computed('ledsat_default_packet'),

    'id' / construct.Hex(construct.Int16ub),
    'data' / construct.GreedyBytes,
)

LEDSAT_IMG_PLEN = 128

ledsat_img = construct.Struct(
    'plen' / construct.Computed(LEDSAT_IMG_PLEN),
    'pnum' / construct.Int16ub,
    'data' / construct.Bytes(LEDSAT_IMG_PLEN),
)

LEDSAT_TLM_DPORT = 8
LEDSAT_IMG_DPORT = 11
packets_map = {
    LEDSAT_TLM_DPORT: ledsat_tlm,
    LEDSAT_IMG_DPORT: ledsat_img,
}

ledsat = construct.Struct(
    'packet' / construct.Switch(construct.this._params.csp_hdr.dest_port, packets_map, default=ledsat_default_packet),
)


class LedsatImageReceiver(ImageReceiver):
    def __init__(self, outdir):
        super().__init__(outdir, '.jpg')
        self.prev_plen = self.prev_pnum = 0
        self.last_addr = 0
        self.unreliable_addr = set()

    def clear(self):
        super().clear()
        self.prev_plen = self.prev_pnum = 0
        self.unreliable_addr.clear()

    def generate_fid(self, large='', t=None):
        if not (self.current_fid and self.merge_mode):
            large = large and f'_LARGE-({",".join(large)})'
            self.current_fid = f'LEDSAT_{self.strftime(t)}{large}'
        return self.current_fid

    def push_data(self, data, large='', t=None, **kw):
        off = data.pnum * data.plen
        soi = not data.pnum and data.data.startswith(b'\xff\xd8') and (b'JFIF' in data.data, b'JFXX' in data.data)
        if not (data.pnum or soi):
            # TODO: log it. it's not image
            if large:
                self.unreliable_addr.add(large)
            return
        if data.pnum and large and large in self.unreliable_addr:
            # TODO: log it. no-image data
            return
        if soi and large:
            self.unreliable_addr.discard(large)

        if not self.last_addr and large or self.last_addr and not large:
            # 100% it's new image. dont merged it
            self.current_fid = ''
            force_new = 1
        else:
            force_new = not data.pnum or soi or data.plen != self.prev_plen or large != self.last_addr
        self.prev_plen = data.plen
        self.prev_pnum = data.pnum
        self.last_addr = large

        img = self.get_image(force_new, large=large, t=t)

        with img.lock:
            if soi:
                img.has_soi = soi
            if off < img.first_data_offset:
                img.first_data_offset = off

            img.push_data(off, data.data)
            if b'\xff\xd9' in data.data:
                img.flush()
                return 2

        return 1


class LedsatProtocol(common.Protocol):
    NAME = 'LEDSAT'
    columns = 'from', 'to', 'id'
    c_width = 40, 40, 40

    tlm_table = {
        'ledsat_tlm': {
            'table': (
                ('name', 'Name'),
                ('id', 'Telemetry Identifier'),
                ('time_ms', 'Millisecond part of the unix time, ms'),
                ('Time', 'On-board unix time'),
                ('proctime', 'Time taken to process the telemetry, ms'),
                ('eps_vboost_0', 'Voltage of the X axis solar panels, mV'),
                ('eps_vboost_1', 'Voltage of the Y axis solar panels, mV'),
                ('eps_vboost_2', 'Voltage of the Z axis solar panels, mV'),
                ('eps_cboost_0', 'Current of the X axis solar panels, mA'),
                ('eps_cboost_1', 'Current of the Y axis solar panels, mA'),
                ('eps_cboost_2', 'Current of the Z axis solar panels, mA'),
                ('eps_bootcause', 'EPS bootcause'),
                ('eps_battmode', 'EPS battery mode'),
                ('eps_temp_0', 'Temperature of the X axis MPPT, °C'),
                ('eps_temp_1', 'Temperature of the Y axis MPPT, °C'),
                ('eps_temp_2', 'Temperature of the Z axis MPPT, °C'),
                ('eps_temp_3', 'Temperature of battery pack #1, °C'),
                ('eps_temp_4', 'Temperature of battery pack #2, °C'),
                ('eps_temp_5', 'Temperature of battery pack #3, °C'),
                ('eps_cursun', 'Total current coming from solar panels, mA'),
                ('eps_cursys', 'Total current absobred by system, mA'),
                ('eps_vbatt', 'Battery voltage, mV'),
                ('eps_gpscur', 'GPS current draw, mA'),
                ('eps_bootcounter', 'EPS bootcount'),
                ('radio_temp_pa', 'Temperature of transceiver PA, °C'),
                ('radio_tx_count', 'Transceiver total TX count'),
                ('radio_rx_count', 'Transceiver total RX count'),
                ('radio_last_rssi', 'Last radio-contact RSSI, dBm'),
                ('radio_bootcounter', 'Radio bootcounter'),
                ('obc_temp_0', 'OBC temperature #1, °C'),
                ('obc_temp_1', 'OBC temperature #2, °C'),
                ('obc_gyro_0', 'Gyroscope X, °/s'),
                ('obc_gyro_1', 'Gyroscope Y, °/s'),
                ('obc_gyro_2', 'Gyroscope Z, °/s'),
                ('obc_mag_0', 'Magnetometer X, mG'),
                ('obc_mag_1', 'Magnetometer Y, mG'),
                ('obc_mag_2', 'Magnetometer Z, mG'),
                ('pan_spt_0', 'Temperature of the +X solar panel, °C'),
                ('pan_spt_1', 'Temperature of the +Y solar panel, °C'),
                ('pan_spt_2', 'Temperature of the -X solar panel, °C'),
                ('pan_spt_3', 'Temperature of the -Y solar panel, °C'),
                ('pan_spt_4', 'Temperature of the +Z solar panel, °C'),
                ('pan_spt_5', 'Temperature of the -Z solar panel, °C'),
                ('pan_css_0', 'Coarse Sun Sensor +X, mV'),
                ('pan_css_1', 'Coarse Sun Sensor +Y, mV'),
                ('pan_css_2', 'Coarse Sun Sensor +Z, mV'),
                ('pan_css_3', 'Coarse Sun Sensor -X, mV'),
                ('pan_css_4', 'Coarse Sun Sensor -Y, mV'),
                ('pan_css_5', 'Coarse Sun Sensor -Z, mV'),
                ('eps_outputs', 'EPS output status'),
                ('obc_bootcounter', 'OBC bootcounter'),
                ('led_status', 'Status of the LEDs'),
                ('gps_status_flag', 'GPS Status Flag'),
                ('gps_fix_time', 'GPS fix time (UNIX)'),
                ('gps_lat', 'GPS Latitude, °'),
                ('gps_lon', 'GPS Longitude, °'),
                ('gps_alt', 'GPS Altitude, m'),
                ('software_status', 'Software status flag'),
                ('ext_gyro_0', 'External Gyroscope X, °/s'),
                ('ext_gyro_1', 'External Gyroscope Y, °/s'),
                ('ext_gyro_2', 'External Gyroscope Z, °/s'),
                ('ext_mag_0', 'External Magnetometer X, mG'),
                ('ext_mag_1', 'External Magnetometer Y, mG'),
                ('ext_mag_2', 'External Magnetometer Z, mG'),
            ),
        },
        'ledsat_default_packet': {
            'table': (
                ('id', 'ID'),
                ('data', 'Data'),
            ),
        },
    }

    def __init__(self, outdir):
        super().__init__(LedsatImageReceiver(outdir))

    def recognize(self, bb, t=None):
        csp_packet = csp.csp.parse(bb)
        raw_ledsat = csp_packet.data
        if not (csp_packet.hdr and raw_ledsat):
            return

        csp_packet.data = s = ledsat.parse(raw_ledsat, csp_hdr=csp_packet.hdr)
        args = [
            'raw',
            self.NAME,
            f'{csp_packet.hdr.src}-{csp_packet.hdr.src_port}',
            f'{csp_packet.hdr.dest}-{csp_packet.hdr.dest_port}',
            hasattr(s.packet, 'id') and f'{int(s.packet.id):04X}' or None,
            raw_ledsat,
        ]

        if csp_packet.hdr.dest_port == LEDSAT_IMG_DPORT:
            x = self.ir.push_data(s.packet, t=t)
            if x:
                args[0] = 'img'
                args[-1] = x, self.ir.cur_img
                yield tuple(args)

        # elif csp_packet.hdr.dest_port in packets_map:
        #     args[0] = 'tlm'
        #     args[-1] = csp_packet, s.packet
        #     yield tuple(args)

        else:
            args[0] = 'tlm'
            args[-1] = csp_packet, s.packet
            yield tuple(args)
