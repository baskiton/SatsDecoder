#  Copyright (c) 2024. Alexander Baskikh
#
#  MIT License (MIT), http://opensource.org/licenses/MIT
#  Full license can be found in the LICENSE-MIT file
#
#  SPDX-License-Identifier: MIT

import construct

from SatsDecoder.systems import csp, common
from SatsDecoder.systems.image_receiver import ImageReceiver

__all__ = 'WtcSimbaProtocol',

proto_name = 'wtc-simba'

"""
https://www.s5lab.space/index.php/decoding-simba/
"""


val_x10 = common.LinearAdapter(10, construct.Int16sb)
val_x100 = common.LinearAdapter(100, construct.Int16sb)

simba_tlm = construct.Struct(
    '_name' / construct.Computed('simba_tlm'),
    'name' / construct.Computed('Telemetry'),

    'id' / construct.Hex(construct.Int16ub),  # 2, Telemetry Identifier
    'time_ms' / construct.Int16ub,  # 2, Millisecond part of the unix time, ms
    'Time' / common.UNIXTimestampAdapter(construct.Int32ub),  # 4, On-board unix time, s
    'proceed_ms' / construct.Int16ub,  # 2, Time taken to process the telemetry, ms
    'spx_u' / construct.Int16sb,  # 2, Voltage of X axis solar panels, mV
    'spy_u' / construct.Int16sb,  # 2, Voltage of Y axis solar panels, mV
    'spx_i' / construct.Int16sb,  # 2, Current of X axis solar panels, mA
    'spy_i' / construct.Int16sb,  # 2, Current of Y axis solar panels, mA
    'esp_bootcause' / construct.Hex(construct.Int8ub),  # 1, EPS bootcause
    'esp_bat_mode' / construct.Hex(construct.Int8ub),  # 1, EPS battery mode
    'mpptx_t' / construct.Int16sb,  # 2, Temperature of X axis MPPT, °C
    'mppty_t' / construct.Int16sb,  # 2, Temperature of Y axis MPPT, °C
    'esp_t' / construct.Int16sb,  # 2, Temperature of EPS board, °C
    'bat_t' / construct.Int16sb,  # 2, Temperature of batteries, °C
    'in_i' / construct.Int16sb,  # 2, Total current coming from solar panels, mA
    'absorbed_i' / construct.Int16sb,  # 2, Total current absorbed by system, mA
    'bat_u' / construct.Int16sb,  # 2, Battery voltage, mV
    'esp_boots' / construct.Int16ub,  # 2, EPS boot count
    'esp_status' / construct.Hex(construct.Int8ub),  # 1, Status of EPS outputs
    'esp1_i' / construct.Int16sb,  # 2, EPS output #1 current
    'esp2_i' / construct.Int16sb,  # 2, EPS output #2 current
    'esp3_i' / construct.Int16sb,  # 2, EPS output #3 current
    'esp4_i' / construct.Int16sb,  # 2, EPS output #4 current
    'esp5_i' / construct.Int16sb,  # 2, EPS output #5 current
    'esp6_i' / construct.Int16sb,  # 2, EPS output #6 current
    'pa_tx_t' / val_x10,  # 2, Temperature of transceiver PA, °C x10
    'tx_cnt' / construct.Int32ub,  # 4, Transceiver total TX count
    'rx_cnt' / construct.Int32ub,  # 4, Transceiver total RX count
    'rssi' / construct.Int16sb,  # 2, Last radio-contact RSSI, dBm
    'radio_boots' / construct.Int16ub,  # 2, Radio bootcounter
    'att_mode' / construct.Hex(construct.Int8ub),  # 1, Current attitude mode
    '_pad0' / construct.Bytes(3),  # 3, Unused
    'pl_rx_cnt' / construct.Int32ub,  # 4, Payload RX count
    'obc_boots' / construct.Int16ub,  # 2, OBC bootcounter
    'obc_t' / val_x10,  # 2, OBC temperature, °C x10
    'gyro_x' / val_x100,  # 2, Gyroscope X, °/s x100
    'gyro_y' / val_x100,  # 2, Gyroscope Y, °/s x100
    'gyro_z' / val_x100,  # 2, Gyroscope Z, °/s x100
    'mag_x' / construct.Int16sb,  # 2, Magnetometer X, mG
    'mag_y' / construct.Int16sb,  # 2, Magnetometer Y, mG
    'mag_z' / construct.Int16sb,  # 2, Magnetometer Z, mG
    'sp+x_t' / val_x100,  # 2, Temperature of +X solar panel, °C x100
    'sp+y_t' / val_x100,  # 2, Temperature of +Y solar panel, °C x100
    'sp-x_t' / val_x100,  # 2, Temperature of -X solar panel, °C x100
    'sp-y_t' / val_x100,  # 2, Temperature of -Y solar panel, °C x100
    'ss+x' / construct.Int16sb,  # 2, Coarse Sun sensor +X, mV
    'ss+y' / construct.Int16sb,  # 2, Coarse Sun sensor +Y, mV
    'ss+z' / construct.Int16sb,  # 2, Coarse Sun sensor +Z, mV
    'ss-x' / construct.Int16sb,  # 2, Coarse Sun sensor -X, mV
    'ss-y' / construct.Int16sb,  # 2, Coarse Sun sensor -Y, mV
    'ss-z' / construct.Int16sb,  # 2, Coarse Sun sensor -Z, mV
    'leds_stat' / construct.Hex(construct.Int8ub),  # 1, Status of the LEDs
    'int_rweel_t' / val_x100,  # 2, Temperature of the Reaction Wheel (internal), °C x100
    'ext_rweel_t' / val_x100,  # 2, Temperature of the Reaction Wheel (external), °C x100
    'rweel_rpm' / common.LinearAdapter(10, construct.Int32sb),  # 4, Speed of the Reaction Wheel, RPM x10
    'rweel_ref_rpm' / construct.Int16sb,  # 2, Reference speed of the Reaction Wheel, RPM
    'rweel_ref_torque' / construct.Int16sb,  # 2, Reference torque of the Reaction Wheel
    'rweel_stat' / construct.Hex(construct.Int8ub),  # 1, Status of the Reaction Wheel
)

SIMBA_IMG_PLEN = 128
SIMBA_LIMG_PLEN = 185

simba_img = construct.Struct(
    'plen' / construct.Computed(SIMBA_IMG_PLEN),
    'pnum' / construct.Int16ub,
    'data' / construct.Bytes(SIMBA_IMG_PLEN),
)

simba_large_img = construct.Struct(
    'plen' / construct.Computed(SIMBA_LIMG_PLEN),
    'pnum' / construct.Int32ub,
    'data' / construct.Bytes(SIMBA_LIMG_PLEN),
)

simba_named_value = construct.Struct(
    '_name' / construct.Computed('simba_named_value'),
    'name' / construct.Computed('Named value'),
    'pnum' / construct.Int16ub,
    'key' / construct.PaddedString(51, 'ascii'),
    'val' / construct.Int32ub,
)

SIMBA_NAMED_ID = 0x09
SIMBA_LIMG_ID = 0x10
ids_map = {
    SIMBA_NAMED_ID: simba_named_value,
    SIMBA_LIMG_ID: simba_large_img,
}

simba_default_packet = construct.Struct(
    '_name' / construct.Computed('default_packet'),
    'id' / construct.Int8ub,
    'data' / construct.Switch(construct.this.id, ids_map, default=construct.GreedyBytes),
)

SIMBA_TLM_DPORT = 8
SIMBA_IMG_DPORT = 11
packets_map = {
    SIMBA_TLM_DPORT: simba_tlm,
    SIMBA_IMG_DPORT: simba_img,
}

simba = construct.Struct(
    'packet' / construct.Switch(construct.this._params.csp_hdr.dest_port, packets_map, default=simba_default_packet),
)


class WtcSimbaImageReceiver(ImageReceiver):
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
            self.current_fid = f'WildTrackCube-SIMBA_{self.strftime(t)}{large}'
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


class WtcSimbaProtocol(common.Protocol):
    NAME = 'WildTrackCube-SIMBA'
    columns = 'from', 'to', 'id'
    c_width = 40, 40, 20

    tlm_table = {
        'simba_tlm': {
            'table': (
                ('name', 'Name', 0),
                ('id', 'Telemetry Identifier', 0),
                ('time_ms', 'Millisecond part of the unix time, ms', 0),
                ('Time', 'On-board unix time, s', 0),
                ('proceed_ms', 'Time taken to process the telemetry, ms', 0),
                ('spx_u', 'Voltage of X axis solar panels, mV', 1),
                ('spy_u', 'Voltage of Y axis solar panels, mV', 2),
                ('spx_i', 'Current of X axis solar panels, mA', 2),
                ('spy_i', 'Current of Y axis solar panels, mA', 2),
                ('esp_bootcause', 'EPS bootcause', 0),
                ('esp_bat_mode', 'EPS battery mode', 0),
                ('mpptx_t', 'Temperature of X axis MPPT, °C', 1),
                ('mppty_t', 'Temperature of Y axis MPPT, °C', 2),
                ('esp_t', 'Temperature of EPS board, °C', 2),
                ('bat_t', 'Temperature of batteries, °C', 2),
                ('in_i', 'Total current coming from solar panels, mA', 1),
                ('absorbed_i', 'Total current absorbed by system, mA', 2),
                ('bat_u', 'Battery voltage, mV', 1),
                ('esp_boots', 'EPS boot count', 0),
                ('esp_status', 'Status of EPS outputs', 0),
                ('esp1_i', 'EPS output #1 current', 1),
                ('esp2_i', 'EPS output #2 current', 2),
                ('esp3_i', 'EPS output #3 current', 2),
                ('esp4_i', 'EPS output #4 current', 2),
                ('esp5_i', 'EPS output #5 current', 2),
                ('esp6_i', 'EPS output #6 current', 2),
                ('pa_tx_t', 'Temperature of transceiver PA, °C', 1),
                ('tx_cnt', 'Transceiver total TX count', 0),
                ('rx_cnt', 'Transceiver total RX count', 0),
                ('rssi', 'Last radio-contact RSSI, dBm', 1),
                ('radio_boots', 'Radio bootcounter', 0),
                ('att_mode', 'Current attitude mode', 0),
                ('pl_rx_cnt', 'Payload RX count', 0),
                ('obc_boots', 'OBC bootcounter', 0),
                ('obc_t', 'OBC temperature, °C', 1),
                ('gyro_x', 'Gyroscope X, deg/s', 1),
                ('gyro_y', 'Gyroscope Y, deg/s', 2),
                ('gyro_z', 'Gyroscope Z, deg/s', 2),
                ('mag_x', 'Magnetometer X, mG', 1),
                ('mag_y', 'Magnetometer Y, mG', 2),
                ('mag_z', 'Magnetometer Z, mG', 2),
                ('sp+x_t', 'Temperature of +X solar panel, °C', 1),
                ('sp+y_t', 'Temperature of +Y solar panel, °C', 2),
                ('sp-x_t', 'Temperature of -X solar panel, °C', 2),
                ('sp-y_t', 'Temperature of -Y solar panel, °C', 2),
                ('ss+x', 'Coarse Sun sensor +X, mV', 1),
                ('ss+y', 'Coarse Sun sensor +Y, mV', 2),
                ('ss+z', 'Coarse Sun sensor +Z, mV', 2),
                ('ss-x', 'Coarse Sun sensor -X, mV', 2),
                ('ss-y', 'Coarse Sun sensor -Y, mV', 2),
                ('ss-z', 'Coarse Sun sensor -Z, mV', 2),
                ('leds_stat', 'Status of the LEDs', 0),
                ('int_rweel_t', 'Temperature of the Reaction Wheel (internal), °C', 1),
                ('ext_rweel_t', 'Temperature of the Reaction Wheel (external), °C', 2),
                ('rweel_rpm', 'Speed of the Reaction Wheel, RPM', 1),
                ('rweel_ref_rpm', 'Reference speed of the Reaction Wheel, RPM', 2),
                ('rweel_ref_torque', 'Reference torque of the Reaction Wheel', 1),
                ('rweel_stat', 'Status of the Reaction Wheel', 0),
                ('_tail', 'Tail', 0),
            ),
        },
        'simba_named_value': {
            'table': (
                ('name', 'Name', 0),
                ('pnum', 'pnum', 0),
                ('key', 'Key', 0),
                ('val', 'Value', 0),
            ),
        },
        'default_packet': {
            'table': (
                ('id', 'ID', 0),
                ('data', 'Data', 0),
            ),
        },
    }

    def __init__(self, outdir):
        super().__init__(WtcSimbaImageReceiver(outdir))
        self.files = {}

    def recognize(self, bb, t=None):
        csp_packet = csp.csp.parse(bb)
        raw_simba = csp_packet.data
        if not (csp_packet.hdr and raw_simba):
            return

        csp_packet.data = s = simba.parse(raw_simba, csp_hdr=csp_packet.hdr)
        args = [
            'raw',
            self.NAME,
            f'{csp_packet.hdr.src}-{csp_packet.hdr.src_port}',
            f'{csp_packet.hdr.dest}-{csp_packet.hdr.dest_port}',
            hasattr(s.packet, 'id') and f'{s.packet.id:02X}' or None,
            raw_simba,
        ]

        if csp_packet.hdr.dest_port == SIMBA_IMG_DPORT:
            x = self.ir.push_data(s.packet, t=t)
            if x:
                args[0] = 'img'
                args[-1] = x, self.ir.cur_img
                yield tuple(args)

        elif csp_packet.hdr.dest_port in packets_map:
            args[0] = 'tlm'
            args[-1] = csp_packet, s.packet
            yield tuple(args)

        elif s.packet.id == SIMBA_LIMG_ID:
            z = args[2:4]
            if csp_packet.rdp:
                z.append(str(csp_packet.rdp.ack_nr))
            x = self.ir.push_data(s.packet.data, large=tuple(z), t=t)
            if x:
                args[0] = 'img'
                args[-1] = x, self.ir.cur_img
                yield tuple(args)

        elif s.packet.id in ids_map:
            args[0] = 'tlm'
            args[-1] = csp_packet, s.packet.data
            yield tuple(args)

        else:
            yield tuple(args)

    def create_new_image(self):
        return (-1, -1, -1) + super().create_new_image()
