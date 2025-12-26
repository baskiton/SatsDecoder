# Parts of this file borrowed from gr-satellites
# https://github.com/daniestevez/gr-satellites/blob/main/python/telemetry/ax25.py

# Copyright 2019 Daniel Estevez <daniel@destevez.net>
#
# This file is part of gr-satellites
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from collections import namedtuple as nt

import construct

from SatsDecoder import utils
from SatsDecoder.systems import common


__all__ = 'Ax25Protocol',

proto_name = 'ax25'


class CallsignAdapter(construct.Adapter):
    def _encode(self, obj, context, path=None):
        return bytes([x << 1 for x in bytes(
            (obj.upper() + ' '*6)[:6], encoding='ascii')])

    def _decode(self, obj, context, path=None):
        return str(bytes([x >> 1 for x in obj]), encoding='ascii').strip(' \0')


callsign = CallsignAdapter(construct.Bytes(6))
ssid = construct.BitStruct(
    'ch' / construct.Flag,  # C / H bit
    construct.Default(construct.BitsInteger(2), 3),  # reserved bits
    'ssid' / construct.BitsInteger(4),
    'extension' / construct.Flag  # last address bit
)

address = construct.Struct(
        'callsign' / callsign,
        'ssid' / ssid
)

control = construct.Hex(construct.Int8ub)

pid = construct.Hex(construct.Int8ub)

ax25_header = construct.Struct(
    'addresses' / construct.RepeatUntil(lambda x, lst, ctx: x.ssid.extension, address),
    'control' / control,
    'pid' / pid
)

ax25 = construct.Struct(
    '_name' / construct.Computed('frame'),
    'header' / ax25_header,
    'info' / construct.GreedyBytes
)


def get_callsign(ax25_hdr, idx):
    if ax25_hdr and len(ax25_hdr.addresses) >= 2:
        x = ax25_hdr.addresses[idx]
        return '%s-%s' % (x.callsign, x.ssid.ssid)


def get_sender_callsign(ax25_hdr):
    return get_callsign(ax25_hdr, 1)


def get_receiver_callsign(ax25_hdr):
    return get_callsign(ax25_hdr, 0)


class Ax25Protocol(common.Protocol):
    columns = ()
    c_width = ()
    has_ax25 = 1
    dd = nt('Ax25Tlm', ('receiver_cs', 'sender_cs', 'control', 'pid', 'data', 'hex'))
    tlm_table = {
        'frame': {
            'table': (
                ('receiver_cs', 'Receiver Callsign'),
                ('sender_cs', 'Sender Callsign'),
                ('control', 'Control'),
                ('pid', 'PID'),
                ('data', 'Data'),
                ('hex', 'Data (HEX)'),
            ),
        },
    }

    @staticmethod
    def get_sender_callsign(data):
        return get_sender_callsign(data.header)

    def recognize(self, bb, t=None):
        frame = ax25.parse(bb)
        if not frame:
            yield 'raw', 'unknown', bb
            return

        d = utils.Dict(self.dd(get_receiver_callsign(frame.header),
                       self.get_sender_callsign(frame),
                       str(frame.header.control),
                       str(frame.header.pid),
                       repr(frame.info),
                       utils.bytes2hex(frame.info),
        )._asdict())
        d._name = frame._name

        yield 'tlm', d.sender_cs, (frame, d)
