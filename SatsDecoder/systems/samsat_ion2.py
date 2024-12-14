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

reg_temp = common.LinearAdapter(256, construct.Int16sl)

unkn = construct.Struct(
    '_name' / construct.Computed('samsat_unkn'),
    'name' / construct.Computed('Unknown'),
    'data' / construct.GreedyBytes,
)
packet = construct.Struct(
    '_name' / construct.Computed('samsat_beacon'),
    'name' / construct.Computed('Beacon'),
    'msg' / construct.PaddedString(6, 'ascii'),
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
    'Tmag' / common.AffineAdapter(333.87, 21.0, construct.Int16sl),
    '_tail' / construct.GreedyBytes,
)

samsat = construct.Struct(
    'ax25' / construct.Peek(ax25.ax25_header),
    'ax25' / construct.If(lambda this: bool(this.ax25), ax25.ax25_header),
    'packet' / construct.Peek(packet),
    'packet' / construct.If(lambda this: (bool(this.ax25) and this.ax25.pid == 0xF0),
                            construct.IfThenElse(lambda this: bool(this.packet), packet, unkn)),
)


class SamSatIon2Protocol(common.Protocol):
    columns = ()
    c_width = ()
    tlm_table = {
        'samsat_beacon': {
            'table': (
                ('name', 'Name'),
                ('msg', 'Message'),
                ('Tbat1', 'Battery #1 temperature, °C'),
                ('Tbat2', 'Battery #2 temperature, °C'),
                ('Mrecv', 'Messages received'),
                ('Ttx1', 'Transceiver #1 temperature, °C'),
                ('Ttx2', 'Transceiver #2 temperature, °C'),
                ('Ttx3', 'Transceiver #3 temperature, °C'),
                ('Tmag', 'Magnetometer temperature, °C'),
            )
        },
        'samsat_unkn': {
            'table': (
                ('name', 'Name'),
                ('data', 'Data'),
            )
        }
    }

    def recognize(self, bb: bytes):
        x = samsat.parse(bb)
        name = self.get_sender_callsign(x) or 'unknown'
        if not x.packet:
            yield 'raw', name, bb
            return

        yield 'tlm', name, (x, x.packet)
