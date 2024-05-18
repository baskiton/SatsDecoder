#  Copyright (c) 2024. Alexander Baskikh
#
#  MIT License (MIT), http://opensource.org/licenses/MIT
#  Full license can be found in the LICENSE-MIT file
#
#  SPDX-License-Identifier: MIT

import enum

import construct

from SatsDecoder import utils
from SatsDecoder.systems import common

__all__ = 'CspProtocol',

proto_name = 'csp'

"""
https://github.com/libcsp/libcsp/blob/87006959696c78f70535ab382b0bcd4cb5a6558d/include/csp/csp_types.h#L144
"""

# _csp_addr = construct.Hex(construct.BitsInteger(5))
_csp_addr = construct.BitsInteger(5)
_csp_port = construct.BitsInteger(6)


class CspRdpFlags(enum.IntFlag):
    RDP_RST = 1
    RDP_EAK = 2
    RDP_ACK = 4
    RDP_SYN = 8


csp_rdp_hdr = construct.Struct(
    'flags' / construct.Hex(construct.Int8ub),
    'seq_nr' / construct.Int16ub,
    'ack_nr' / construct.Int16ub,
)

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
    'use_rdp' / construct.Flag,     # Use RDP protocol
    'use_crc' / construct.Flag,     # Use CRC32 checksum
)

csp = construct.Struct(
    '_name' / construct.Computed('frame'),
    'hdr' / csp_hdr,
    'data' / construct.Peek(construct.GreedyBytes),
    'data' / construct.Bytes(lambda this: len(this.data) - (this.hdr.use_rdp and csp_rdp_hdr.sizeof()) - (this.hdr.use_crc and 4)),
    'rdp' / construct.If(construct.this.hdr.use_rdp, csp_rdp_hdr),
    'crc32' / construct.If(construct.this.hdr.use_crc, construct.Hex(construct.Bytes(4))),
)


class CspProtocol(common.Protocol):
    columns = 'from', 'to'
    c_width = 40, 40

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
                ('use_rdp', 'Use RDP protocol'),
                ('use_crc', 'Use CRC32 checksum'),
                ('data', 'Data'),
                ('hex', 'Data (HEX)'),
                # ('crc32', 'CRC32 (HEX)'),
            ),
        },
    }

    def recognize(self, bb):
        frame = csp.parse(bb)
        if not frame:
            yield 'raw', 'unknown', None, None, bb
            return

        d = utils.Dict(data=str(frame.data), hex=utils.bytes2hex(frame.data),
                       # crc32=utils.bytes2hex(frame.crc32),
                       _name=frame._name, **frame.hdr)
        d.pop('_io', 0)

        yield ('tlm', 'unknown',
               f'{frame.hdr.src}:{frame.hdr.src_port}',
               f'{frame.hdr.dest}:{frame.hdr.dest_port}',
               (frame, d))
