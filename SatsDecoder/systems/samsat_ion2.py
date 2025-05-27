#  Copyright (c) 2024. Alexander Baskikh
#
#  MIT License (MIT), http://opensource.org/licenses/MIT
#  Full license can be found in the LICENSE-MIT file
#
#  SPDX-License-Identifier: MIT

import construct
from construct import Construct

from SatsDecoder.systems import ax25, common

__all__ = 'SamSatIon2Protocol',

proto_name = 'samsat-ion2'

# SamSat-Ion2 beacon structure
# https://spaceresearch.ssau.ru/doc/SamSat/SamSat-Ion2/SamSat-Ionosphere-beacon.pdf

reg_temp = common.EvalAdapter('x/256', construct.Int16sl)

packet = construct.Struct(
    '_name' / construct.Computed('samsat_beacon'),
    'name' / construct.Computed('Beacon'),
    'sign' / construct.StringEncoded(construct.Const(b'WORLD '), 'ascii'),
    '_pad0' / construct.Bytes(4),
    'Tbat1' / reg_temp,
    'Tbat2' / reg_temp,
    '_pad1' / construct.Bytes(24),
    'Mrecv' / construct.Int32ul,
    '_pad2' / construct.Bytes(8),
    'Ttx1' / reg_temp,
    'Ttx2' / reg_temp,
    'Ttx3' / reg_temp,
    '_pad3' / construct.Bytes(23),
    'Tmag' / common.EvalAdapter('x/333.87+21', construct.Int16sl),
    '_tail' / construct.GreedyBytes,
)

samsat = construct.Struct(
    'ax25' / construct.Peek(ax25.ax25_header),
    'ax25' / construct.If(lambda this: bool(this.ax25), ax25.ax25_header),
    'packet' / construct.Peek(packet),
    'packet' / construct.If(lambda this: (bool(this.ax25) and this.ax25.pid == 0xF0),
                            construct.IfThenElse(lambda this: bool(this.packet), packet, construct.GreedyBytes)),
)


class SamSatIon2Protocol(common.Protocol):
    columns = ()
    c_width = ()
    has_ax25 = 1
    tlm_table = {
        'samsat_beacon': {
            'table': (
                ('name', 'Name'),
                ('sign', 'Signature'),
                ('Tbat1', 'Battery #1 temperature, °C'),
                ('Tbat2', 'Battery #2 temperature, °C'),
                ('Mrecv', 'Messages received'),
                ('Ttx1', 'Transceiver #1 temperature, °C'),
                ('Ttx2', 'Transceiver #2 temperature, °C'),
                ('Ttx3', 'Transceiver #3 temperature, °C'),
                ('Tmag', 'Magnetometer temperature, °C'),
            )
        },
    }

    def recognize(self, bb: bytes):
        x = samsat.parse(bb)
        name = self.get_sender_callsign(x) or 'unknown'

        if x.packet and hasattr(x.packet, '_name'):
            yield 'tlm', name, (x, x.packet)
        else:
            yield 'raw', name, x.packet or bb
