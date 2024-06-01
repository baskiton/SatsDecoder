#  Copyright (c) 2024. Alexander Baskikh
#
#  MIT License (MIT), http://opensource.org/licenses/MIT
#  Full license can be found in the LICENSE-MIT file
#
#  SPDX-License-Identifier: MIT

import datetime as dt

import construct

from SatsDecoder import utils
from SatsDecoder.systems import common
from SatsDecoder.systems.image_receiver import ImageReceiver

__all__ = 'Lucky7Protocol',

proto_name = 'lucky-7'

"""
https://www.lucky7satellite.org/radioamateurs
https://www.lucky7satellite.org/download/Lucky-7_-_Amateur_Radio_Information.pdf
"""

ang_rate_enum = construct.Enum(construct.Int16sb, **{'Gyro off': 0x07d1})
voltage = common.LinearAdapter(50, construct.Int8ub)

lucky7_tlm = construct.Struct(
    '_name' / construct.Computed('lucky7_tlm'),
    'name' / construct.Computed('Beacon'),
    'obc_id' / construct.Hex(construct.Int24ub),
    'mission_cnt' / construct.Int24ub,
    'callsign' / construct.PaddedString(6, 'ascii'),
    'sat_name' / construct.PaddedString(6, 'ascii'),
    'tot_resets' / construct.Int16ub,
    'swap_resets' / construct.Int16ub,
    'bat_u' / voltage,
    'mcu_t' / construct.Int8sb,
    'pa_t' / construct.Int8sb,
    'cpu_i' / construct.Int8ub,
    'mcu_3v3_u' / voltage,
    'mcu_1v2_u' / voltage,
    'ang_x' / ang_rate_enum,
    'ang_y' / ang_rate_enum,
    'ang_z' / ang_rate_enum,
    'ant_burnware' / construct.Hex(construct.Enum(construct.Int8sb, **{'Enabled': 1, 'Disabled': 0})),
)

lucky7_img = construct.Struct(
    'obc_id' / construct.Hex(construct.Int8ub),
    'obc_cnt' / construct.Hex(construct.Int16ub),
    'pnum' / construct.Int16ub,
    'packets' / construct.Int16ub,
    'data' / construct.Bytes(28),
)

lucky7_hdr = construct.Struct(
    'obc_id' / construct.Hex(construct.Int8ub),
    'obc_cnt' / construct.Hex(construct.Int16ub),
)


class Lucky7ImageReceiver(ImageReceiver):
    PACKET_LEN = 28

    def __init__(self, outdir):
        super().__init__(outdir, '.jpg')

    def generate_fid(self):
        if not (self.current_fid and self.merge_mode):
            self.last_date = now = dt.datetime.now()
            self.current_fid = f'LUCKY7_{now.strftime("%Y-%m-%d_%H-%M-%S,%f")}'
        return self.current_fid

    def get_image(self, force_new=0, packets=0, **kwargs):
        soi = force_new
        fid = self.current_fid
        img = self.images.get(fid)
        if img:
            if packets != img.packets:
                self.current_fid = fid = ''
                force_new = 1

        if force_new or not img:
            if not fid:
                fid = self.generate_fid()

            img = self.new_file(fid)
            img.packets = packets
            img.first_data_offset = 0
            img.f.truncate(self.PACKET_LEN * packets)

        img.has_soi |= soi
        return img

    def push_data(self, data, **kw):
        off = self.PACKET_LEN * data.pnum

        img = self.get_image(not data.pnum, data.packets)
        with img.lock:
            eoi = data.pnum == img.packets
            img.push_data(off, data.data)
            if eoi:
                img.flush()
                return 2

        return 1


class Lucky7Protocol(common.Protocol):
    columns = ()
    c_width = ()

    tlm_table = {
        'lucky7_tlm': {
            'table': (
                ('name', 'Name'),
                ('obc_id', 'OBC ID'),
                ('mission_cnt', 'Mission counter'),
                ('callsign', 'Callsign'),
                ('sat_name', 'Satellite Name'),
                ('tot_resets', 'Total Reset Counter'),
                ('swap_resets', 'Swap Reset Counter'),
                ('bat_u', 'Battery voltage, mV'),
                ('mcu_t', 'MCU Temperature, °C'),
                ('pa_t', 'PA Temperature, °C'),
                ('cpu_i', 'Processor Current, mA'),
                ('mcu_3v3_u', 'MCU Voltage 3V3, mV'),
                ('mcu_1v2_u', 'MCU Voltage 1V2, mV'),
                ('ang_x', 'Angular rate X axis, deg/s'),
                ('ang_y', 'Angular rate Y axis, deg/s'),
                ('ang_z', 'Angular rate Z axis, deg/s'),
                ('ant_burnware', 'Antenna Burnwire'),
            ),
        },
    }

    def __init__(self, outdir):
        super().__init__(Lucky7ImageReceiver(outdir))

    def recognize(self, bb):
        hdr = lucky7_hdr.parse(bb)
        if hdr.obc_id not in (0x00, 0x80):
            return

        if hdr.obc_cnt == 0:
            try:
                p = lucky7_tlm.parse(bb)
            except construct.StringError:
                return
            yield 'tlm', p.sat_name, (p, p)

        elif 0xC000 <= hdr.obc_cnt:
            x = self.ir.push_data(lucky7_img.parse(bb))
            if x:
                yield 'img', 'LUCKY7', (x, self.ir.cur_img)
