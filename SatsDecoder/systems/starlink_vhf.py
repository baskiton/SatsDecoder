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


tlm_a = construct.Struct(
    'unkn_a0' / construct.Hex(construct.Bytes(14)),
    'gps_week' / construct.Int16ul,
    'gps_sec' / common.LinearAdapter(100, construct.Int32ul),
    'gps_time' / construct.Computed(lambda ctx: utils.gps_to_utc(ctx.gps_week, ctx.gps_sec)),
)

tlm_b = construct.Struct(
    'unkn_b0' / construct.Hex(construct.Bytes(29)),
)

tlm_c = construct.Struct(
    'unkn_c0' / construct.Hex(construct.Bytes(6)),
)

tlm_d = construct.Struct(
    'unkn_d0' / construct.Hex(construct.Bytes(8)),
)

ephemeris = construct.Struct(
    'lat' / construct.Float32l,
    'lon' / construct.Float32l,
    'alt' / construct.Int32ul,
    'unkn_eph0' / construct.Hex(construct.Bytes(9)),
)

beacon3 = construct.Struct(
    '_name' / construct.Computed('beacon3'),
    'name' / construct.Computed('Beacon #3'),

    'Time' / common.UNIXTimestampAdapter(construct.Int32ul),

    'eph' / ephemeris,
    'tlm_a' / tlm_a,
    'tlm_b' / tlm_b,
)

beacon4 = construct.Struct(
    '_name' / construct.Computed('beacon4'),
    'name' / construct.Computed('Beacon #4'),

    'flag' / construct.Hex(construct.Byte),
    'Time' / common.UNIXTimestampAdapter(construct.Int32ul),
    'tlm_a' / tlm_a,
    'tlm_b' / tlm_b,
    'tlm_c' / tlm_c,
)

beacon5 = construct.Struct(
    '_name' / construct.Computed('beacon5'),
    'name' / construct.Computed('Beacon #5'),

    'flag' / construct.Hex(construct.Byte),
    'Time' / common.UNIXTimestampAdapter(construct.Int32ul),
    'tlm_a' / tlm_a,
    'tlm_b' / tlm_b,
    'tlm_c' / tlm_c,
    'tlm_d' / tlm_d,
)

IDS = {
    0x034B: beacon3,
    0x043D: beacon4,
    0x0545: beacon5,
}

starlink_hdr = construct.Struct(
    'msg_num' / construct.Int24ul,
    'sc_num' / construct.Hex(construct.Int16ul),
    'ptype' / construct.Hex(construct.Byte),
    'unkn0' / construct.Hex(construct.Bytes(3)),
    'unkn1' / construct.Hex(construct.Bytes(2)),
    'msg_id' / construct.Hex(construct.Int16ul),
)

starlink = construct.Struct(
    'hdr' / starlink_hdr,
    'data' / construct.Switch(construct.this.hdr.msg_id, IDS, construct.GreedyBytes),
)


class StarlinkProtocol:
    columns = 'msg_id',
    c_width = 60,

    _hdr = (
        ('msg_num', 'Message Number'),
        ('sc_num', 'Spacecraft Number'),
        ('ptype', 'Packet Type'),
        ('unkn0', 'unkn0'),
        ('unkn1', 'unkn1'),
        ('msg_id', 'MSG ID'),
    )
    _eph = (
        ('lat', 'Latitude'),
        ('lon', 'Longitude'),
        ('alt', 'Altitude'),
        ('unkn_eph0', 'Undefine #0'),
    )
    _tlm_a = (
        ('unkn_a0', 'Undefine A#0'),
        ('gps_week', 'GPS Week Number'),
        ('gps_sec', 'GPS Seconds'),
        ('gps_time', 'GPS Time'),
    )
    _tlm_b = (
        ('unkn_b0', 'Undefine B#0'),
    )
    _tlm_c = (
        ('unkn_c0', 'Undefine C#0'),
    )
    _tlm_d = (
        ('unkn_d0', 'Undefine D#0'),
    )

    tlm_table = {
        'beacon3': {
            'table': (
                ('name', 'Name'),
                ('Time', 'Time'),
                ('_break0', '---'),
                *_hdr,
                ('_break1', '---'),
                *_eph,
                ('_break2', '---'),
                *_tlm_a,
                ('_break3', '---'),
                *_tlm_b,
            ),
        },
        'beacon4': {
            'table': (
                ('name', 'Name'),
                ('Time', 'Time'),
                ('flag', 'Flag'),
                ('_break0', '---'),
                *_hdr,
                ('_break1', '---'),
                *_tlm_a,
                ('_break2', '---'),
                *_tlm_b,
                ('_break3', '---'),
                *_tlm_c,
            ),
        },
        'beacon5': {
            'table': (
                ('name', 'Name'),
                ('Time', 'Time'),
                ('flag', 'Flag'),
                ('_break0', '---'),
                *_hdr,
                ('_break1', '---'),
                *_tlm_a,
                ('_break2', '---'),
                *_tlm_b,
                ('_break3', '---'),
                *_tlm_c,
                ('_break4', '---'),
                *_tlm_d,
            ),
        },
        'raw': {
            'table': (
                *_hdr,
                ('_break0', '---'),
                ('data', 'Data'),
                ('hex', 'HEX'),
            ),
        }
    }

    def __init__(self, outdir):
        self.ir = None

    def recognize(self, bb):
        x = starlink.parse(bb)
        if not x:
            return

        d = utils.Dict(_name='raw', **x.hdr)
        if x.hdr.msg_id in IDS:
            for k, v in x.data.items():
                if isinstance(v, construct.Container):
                    d.update(v)
                else:
                    d[k] = v
        else:
            d['data'] = x.data
            d['hex'] = utils.bytes2hex(x.data)

        d.pop('_io', 0)

        yield 'tlm', 'Starlink #%i' % x.hdr.sc_num, '0x%02X' % x.hdr.msg_id, (x, d)
        yield 'tlm', 'Starlink #%i' % x.hdr.sc_num, '0x%04X' % x.hdr.msg_id, (x, d)
