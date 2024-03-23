#  Copyright (c) 2024. Alexander Baskikh
#
#  MIT License (MIT), http://opensource.org/licenses/MIT
#  Full license can be found in the LICENSE-MIT file
#
#  SPDX-License-Identifier: MIT

import construct

from SatsDecoder import utils

__all__ = 'CspProtocol',

proto_name = 'csp'

"""
https://github.com/libcsp/libcsp/blob/87006959696c78f70535ab382b0bcd4cb5a6558d/include/csp/csp_types.h#L144
"""

_csp_addr = construct.Hex(construct.BitsInteger(5))
_csp_port = construct.BitsInteger(6)

csp_hdr = construct.BitStruct(
    'priority' / construct.BitsInteger(2),
    'src' / _csp_addr,
    'dest' / _csp_addr,
    'dest_port' / _csp_port,
    'src_port' / _csp_port,
    '_rsrv' / construct.BitsInteger(3),
    'frag' / construct.Flag,    # Use fragmentation
    'hmac' / construct.Flag,    # Use HMAC verification
    'xtea' / construct.Flag,    # Use XTEA encryption
    'rdp' / construct.Flag,     # Use RDP protocol
    'crc' / construct.Flag,     # Use CRC32 checksum
)

csp = construct.Struct(
    '_name' / construct.Computed('frame'),
    'hdr' / csp_hdr,
    'data' / construct.GreedyBytes,
    # 'crc' / construct.Bytes(4),
)


class CspProtocol:
    columns = ()
    c_width = ()

    tlm_table = {
        'frame': {
            'table': (
                ('priority', 'Priority'),
                ('src', 'Source address'),
                ('src_port', 'Source port'),
                ('dest', 'Destination address'),
                ('dest_port', 'Destination port'),
                ('frag', 'Use fragmentation'),
                ('hmac', 'Use HMAC verification'),
                ('xtea', 'Use XTEA encryption'),
                ('rdp', 'Use RDP protocol'),
                ('crc', 'Use CRC32 checksum'),
                ('data', 'Data'),
                ('hex', 'Data (HEX)'),
            ),
        },
    }

    def __init__(self, outdir):
        self.ir = None

    def recognize(self, bb):
        frame = csp.parse(bb)
        if not frame:
            yield 'raw', 'unknown', bb
            return

        d = utils.Dict(data=str(frame.data), hex=utils.bytes2hex(frame.data),
                       _name=frame._name, **frame.hdr)
        d.pop('_io', 0)

        yield 'tlm', 'unknown', (frame, d)
