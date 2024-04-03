#  Copyright (c) 2024. Alexander Baskikh
#
#  MIT License (MIT), http://opensource.org/licenses/MIT
#  Full license can be found in the LICENSE-MIT file
#
#  SPDX-License-Identifier: MIT

import construct

from SatsDecoder import utils
from SatsDecoder.systems import common

__all__ = 'StarlinkProtocol',

proto_name = 'starlink-vhf'


"""
https://emitters.space/Starlink.pdf
"""


starlink_beacon = construct.Struct(
    '_name' / construct.Computed('starlink_beacon'),
    'name' / construct.Computed('Beacon'),

    # header
    'msg_num' / construct.Int24ul,
    'sc_num' / construct.Hex(construct.Int16ul),
    'ptype' / construct.Hex(construct.Byte),
    'semi_fixed' / construct.Bytes(7),
    'Time' / common.UNIXTimestampAdapter(construct.Int32ul),

    # ephemeris
    'lat' / construct.Float32l,
    'lon' / construct.Float32l,
    'alt' / construct.Int32ul,
    'semi_fixed_tbd' / construct.Bytes(8),

    # telemetry-A
    'tbd_a' / construct.Bytes(15),
    'gps_week' / construct.Int16ul,
    'gps_sec' / common.LinearAdapter(100, construct.Int32ul),
    'gps_time' / construct.Computed(lambda ctx: utils.gps_to_utc(ctx.gps_week, ctx.gps_sec)),

    # telemetry-B
    'tbd_b' / construct.Bytes(29),
)


class StarlinkProtocol:
    columns = 'ptype',
    c_width = 40,

    tlm_table = {
        'starlink_beacon': {
            'table': (
                ('name', 'Name'),
                ('msg_num', 'Message Number'),
                ('sc_num', 'Spacecraft Number'),
                ('ptype', 'Packet Type'),
                ('semi_fixed', 'Semi-fixed'),
                ('Time', 'Time'),
                ('lat', 'Latitude'),
                ('lon', 'Longitude'),
                ('alt', 'Altitude'),
                ('semi_fixed_tbd', 'Semi-fixed TBD'),
                ('tbd_a', 'TBD-A'),
                ('gps_week', 'GPS Week Number'),
                ('gps_sec', 'GPS Seconds'),
                ('gps_time', 'GPS Time'),
                ('tbd_b', 'TBD-B'),
            ),
        },
    }

    def __init__(self, outdir):
        self.ir = None

    def recognize(self, bb):
        x = starlink_beacon.parse(bb)
        if not x:
            return

        yield 'tlm', 'Starlink #%i' % x.sc_num, '0x%02X' % x.ptype, (x, x)


if __name__ == '__main__':
    a = 'ae803e5109cc0000d0eb4e4b036d765564313d06c262100f4319530600000098a31400043090fc21ba0403000082ca660e060800d408c0ba090318b601e58f2f4b1481d8bce93eb3fcff2b74f6ff674afbff1e10d2dc07'
    b = bytes.fromhex(a)
    x = starlink_beacon.parse(b)
    print(x)
    print('Starlink #%i' % x.sc_num)
