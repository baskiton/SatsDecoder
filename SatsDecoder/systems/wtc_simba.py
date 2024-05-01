#  Copyright (c) 2024. Alexander Baskikh
#
#  MIT License (MIT), http://opensource.org/licenses/MIT
#  Full license can be found in the LICENSE-MIT file
#
#  SPDX-License-Identifier: MIT

import datetime as dt

import construct

from SatsDecoder.systems import csp, common
from SatsDecoder.systems.image_receiver import ImageReceiver

__all__ = 'WtcSimbaProtocol',

proto_name = 'wtc-simba'

"""
https://www.s5lab.space/index.php/decoding-simba/
"""

SIMBA_TLM = 8
SIMBA_IMG = 11

val_x10 = common.LinearAdapter(10, construct.Int16sb)
val_x100 = common.LinearAdapter(100, construct.Int16sb)

simba_tlm = construct.Struct(
    '_name' / construct.Computed('simba_tlm'),
    'name' / construct.Computed('Telemetry'),

    'tid' / construct.Hex(construct.Int16ub),  # 2	Telemetry Identifier
    'time_ms' / construct.Int16ub,  # 2	Millisecond part of the unix time	ms
    'Time' / common.UNIXTimestampAdapter(construct.Int32ub),  # 4	On-board unix time	s
    'proceed_ms' / construct.Int16ub,  # 2	Time taken to process the telemetry	ms
    'spx_u' / construct.Int16sb,  # 2	Voltage of X axis solar panels	mV
    'spy_u' / construct.Int16sb,  # 2	Voltage of Y axis solar panels	mV
    'spx_i' / construct.Int16sb,  # 2	Current of X axis solar panels	mA
    'spy_i' / construct.Int16sb,  # 2	Current of Y axis solar panels	mA
    'esp_bootcause' / construct.Hex(construct.Int8ub),  # 1	EPS bootcause
    'esp_bat_mode' / construct.Hex(construct.Int8ub),  # 1	EPS battery mode
    'mpptx_t' / construct.Int16sb,  # 2	Temperature of X axis MPPT	°C
    'mppty_t' / construct.Int16sb,  # 2	Temperature of Y axis MPPT	°C
    'esp_t' / construct.Int16sb,  # 2	Temperature of EPS board	°C
    'bat_t' / construct.Int16sb,  # 2	Temperature of batteries	°C
    'in_i' / construct.Int16sb,  # 2	Total current coming from solar panels	mA
    'absorbed_i' / construct.Int16sb,  # 2	Total current absorbed by system	mA
    'bat_u' / construct.Int16sb,  # 2	Battery voltage	mV
    'esp_boots' / construct.Int16ub,  # 2	EPS boot count
    'esp_status' / construct.Hex(construct.Int8ub),  # 1	Status of EPS outputs
    'esp1_i' / construct.Int16sb,  # 2	EPS output #1 current
    'esp2_i' / construct.Int16sb,  # 2	EPS output #2 current
    'esp3_i' / construct.Int16sb,  # 2	EPS output #3 current
    'esp4_i' / construct.Int16sb,  # 2	EPS output #4 current
    'esp5_i' / construct.Int16sb,  # 2	EPS output #5 current
    'esp6_i' / construct.Int16sb,  # 2	EPS output #6 current
    'pa_tx_t' / val_x10,  # 2	Temperature of transceiver PA	°C x10
    'tx_cnt' / construct.Int32ub,  # 4	Transceiver total TX count
    'rx_cnt' / construct.Int32ub,  # 4	Transceiver total RX count
    'rssi' / construct.Int16sb,  # 2	Last radio-contact RSSI	dBm
    'radio_boots' / construct.Int16ub,  # 2	Radio bootcounter
    'att_mode' / construct.Hex(construct.Int8ub),  # 1	Current attitude mode
    '_pad0' / construct.Bytes(3),  # 3	Unused
    'pl_rx_cnt' / construct.Int32ub,  # 4	Payload RX count
    'obc_boots' / construct.Int16ub,  # 2	OBC bootcounter
    'obc_t' / val_x10,  # 2	OBC temperature	°C x10
    'gyro_x' / val_x100,  # 2	Gyroscope X	°/s x100
    'gyro_y' / val_x100,  # 2	Gyroscope Y	°/s x100
    'gyro_z' / val_x100,  # 2	Gyroscope Z	°/s x100
    'mag_x' / construct.Int16sb,  # 2	Magnetometer X	mG
    'mag_y' / construct.Int16sb,  # 2	Magnetometer Y	mG
    'mag_z' / construct.Int16sb,  # 2	Magnetometer Z	mG
    'sp+x_t' / val_x100,  # 2	Temperature of +X solar panel	°C x100
    'sp+y_t' / val_x100,  # 2	Temperature of +Y solar panel	°C x100
    'sp-x_t' / val_x100,  # 2	Temperature of -X solar panel	°C x100
    'sp-y_t' / val_x100,  # 2	Temperature of -Y solar panel	°C x100
    'ss+x' / construct.Int16sb,  # 2	Coarse Sun sensor +X	mV
    'ss+y' / construct.Int16sb,  # 2	Coarse Sun sensor +Y	mV
    'ss+z' / construct.Int16sb,  # 2	Coarse Sun sensor +Z	mV
    'ss-x' / construct.Int16sb,  # 2	Coarse Sun sensor -X	mV
    'ss-y' / construct.Int16sb,  # 2	Coarse Sun sensor -Y	mV
    'ss-z' / construct.Int16sb,  # 2	Coarse Sun sensor -Z	mV
    'leds_stat' / construct.Hex(construct.Int8ub),  # 1	Status of the LEDs
    'int_rweel_t' / val_x100,  # 2	Temperature of the Reaction Wheel (internal)	°C x100
    'ext_rweel_t' / val_x100,  # 2	Temperature of the Reaction Wheel (external)	°C x100
    'rweel_rpm' / common.LinearAdapter(10, construct.Int32sb),  # 4	Speed of the Reaction Wheel	RPM x10
    'rweel_ref_rpm' / construct.Int16sb,  # 2	Reference speed of the Reaction Wheel	RPM
    'rweel_ref_torque' / construct.Int16sb,  # 2	Reference torque of the Reaction Wheel
    'rweel_stat' / construct.Hex(construct.Int8ub),  # 1	Status of the Reaction Wheel

    '_tail' / construct.GreedyBytes
)

simba_img = construct.Struct(
    'pnum' / construct.Int16ub,
    'data' / construct.GreedyBytes,
)


simba_file_unknown0_data = construct.Struct(
    'str' / construct.PaddedString(51, 'ascii'),
    'val' / construct.Int32ub,
)

simba_file_unknown0 = construct.Struct(
    '_name' / construct.Computed('file_unknown0'),
    'id' / construct.Int8ub,
    'pnum' / construct.Int16ub,
    'data' / construct.Switch(construct.this.id,
                              {8: construct.Int8ub,
                               9: simba_file_unknown0_data},
                              construct.GreedyBytes)
)
packets_map = {
    SIMBA_TLM: simba_tlm,
    SIMBA_IMG: simba_img,
    # 36: simba_file_unknown0,
    # 45: simba_file_unknown0,
}

simba = construct.Struct(
    'csp' / construct.Peek(csp.csp_hdr),
    'csp' / construct.If(lambda this: bool(this.csp), csp.csp_hdr),
    'simba' / construct.Switch(construct.this.csp.dest_port, packets_map, default=construct.GreedyBytes)
    # 'simba' / construct.If(lambda this: bool(this.csp), frame)
)


class WtcSimbaImageReceiver(ImageReceiver):
    PACKET_LEN = 128

    def __init__(self, outdir):
        super().__init__(outdir, '.jpg')
        self.prev_off = 0

    def generate_fid(self):
        if not (self.current_fid and self.merge_mode):
            self.last_date = now = dt.datetime.now()
            self.current_fid = f'WildTrackCube-SIMBA_{now.strftime("%Y-%m-%d_%H-%M-%S,%f")}'
        return self.current_fid

    def push_data(self, data):
        off = data.pnum * self.PACKET_LEN
        soi = data.data.startswith(b'\xff\xd8')
        force_new = off < self.prev_off or soi

        img = self.get_image(force_new)
        self.prev_off = off

        with img.lock:
            if soi:
                img.has_soi = soi
                img.first_data_offset = off

            img.push_data(off, data.data)
            if b'\xff\xd9' in data.data:
                img.flush()
                return 2

        return 1


class WtcSimbaProtocol(common.Protocol):
    columns = ('d_port',)
    c_width = (60,)

    tlm_table = {
        'simba_tlm': {
            'table': (
                ('name', 'Name'),
                ('tid', 'Telemetry Identifier'),
                ('time_ms', 'Millisecond part of the unix time, ms'),
                ('Time', 'On-board unix time, s'),
                ('proceed_ms', 'Time taken to process the telemetry, ms'),
                ('spx_u', 'Voltage of X axis solar panels, mV'),
                ('spy_u', 'Voltage of Y axis solar panels, mV'),
                ('spx_i', 'Current of X axis solar panels, mA'),
                ('spy_i', 'Current of Y axis solar panels, mA'),
                ('esp_bootcause', 'EPS bootcause'),
                ('esp_bat_mode', 'EPS battery mode'),
                ('mpptx_t', 'Temperature of X axis MPPT, °C'),
                ('mppty_t', 'Temperature of Y axis MPPT, °C'),
                ('esp_t', 'Temperature of EPS board, °C'),
                ('bat_t', 'Temperature of batteries, °C'),
                ('in_i', 'Total current coming from solar panels, mA'),
                ('absorbed_i', 'Total current absorbed by system, mA'),
                ('bat_u', 'Battery voltage, mV'),
                ('esp_boots', 'EPS boot count'),
                ('esp_status', 'Status of EPS outputs'),
                ('esp1_i', 'EPS output #1 current'),
                ('esp2_i', 'EPS output #2 current'),
                ('esp3_i', 'EPS output #3 current'),
                ('esp4_i', 'EPS output #4 current'),
                ('esp5_i', 'EPS output #5 current'),
                ('esp6_i', 'EPS output #6 current'),
                ('pa_tx_t', 'Temperature of transceiver PA, °C'),
                ('tx_cnt', 'Transceiver total TX count'),
                ('rx_cnt', 'Transceiver total RX count'),
                ('rssi', 'Last radio-contact RSSI, dBm'),
                ('radio_boots', 'Radio bootcounter'),
                ('att_mode', 'Current attitude mode'),
                ('pl_rx_cnt', 'Payload RX count'),
                ('obc_boots', 'OBC bootcounter'),
                ('obc_t', 'OBC temperature, °C'),
                ('gyro_x', 'Gyroscope X, deg/s'),
                ('gyro_y', 'Gyroscope Y, deg/s'),
                ('gyro_z', 'Gyroscope Z, deg/s'),
                ('mag_x', 'Magnetometer X, mG'),
                ('mag_y', 'Magnetometer Y, mG'),
                ('mag_z', 'Magnetometer Z, mG'),
                ('sp+x_t', 'Temperature of +X solar panel, °C'),
                ('sp+y_t', 'Temperature of +Y solar panel, °C'),
                ('sp-x_t', 'Temperature of -X solar panel, °C'),
                ('sp-y_t', 'Temperature of -Y solar panel, °C'),
                ('ss+x', 'Coarse Sun sensor +X, mV'),
                ('ss+y', 'Coarse Sun sensor +Y, mV'),
                ('ss+z', 'Coarse Sun sensor +Z, mV'),
                ('ss-x', 'Coarse Sun sensor -X, mV'),
                ('ss-y', 'Coarse Sun sensor -Y, mV'),
                ('ss-z', 'Coarse Sun sensor -Z, mV'),
                ('leds_stat', 'Status of the LEDs'),
                ('int_rweel_t', 'Temperature of the Reaction Wheel (internal), °C'),
                ('ext_rweel_t', 'Temperature of the Reaction Wheel (external), °C'),
                ('rweel_rpm', 'Speed of the Reaction Wheel, RPM'),
                ('rweel_ref_rpm', 'Reference speed of the Reaction Wheel, RPM'),
                ('rweel_ref_torque', 'Reference torque of the Reaction Wheel'),
                ('rweel_stat', 'Status of the Reaction Wheel'),
                ('_tail', 'Tail'),
            ),
        },
        'file_unknown0': {
            'table': (
                ('id', 'id'),
                ('pnum', 'pnum'),
                ('data', 'data'),
            )
        },
    }

    def __init__(self, outdir):
        super().__init__(WtcSimbaImageReceiver(outdir))
        self.files = {}

    def recognize(self, bb):
        data = simba.parse(bb)
        if not data.csp:
            return

        name = 'WildTrackCube-SIMBA'
        if data.csp.dest_port == SIMBA_IMG:
            x = self.ir.push_data(data.simba)
            if x:
                yield 'img', name, data.csp.dest_port, (x, self.ir.cur_img)

        elif data.csp.dest_port in packets_map:
            yield 'tlm', name, data.csp.dest_port, (data, data.simba)

        else:
            yield 'raw', name, data.csp.dest_port, data.simba
        #     t = data.csp.priority, data.csp.src, data.csp.src_port, data.csp.dest, data.csp.dest_port
        #     print('% 22s: %03i: %s' % (t, len(data.simba), data.simba.hex(' ')))
        #     if data.csp.dest_port in (45, 36):
        #         x = simba_file_unknown0.parse(data.simba)
        #         if x.id == 9:
        #             self.files[x.data.str] = x.data.val
        #             print(self.files)
        #     #     print(t, x.id, x.pnum, str(x.data))

    def create_new_image(self):
        return (-1,) + super().create_new_image()
