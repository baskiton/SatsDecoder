# Parts of this file borrowed from gr-satellites
# https://github.com/daniestevez/gr-satellites/blob/main/python/telemetry/ax25.py

# Copyright 2019 Daniel Estevez <daniel@destevez.net>
#
# This file is part of gr-satellites
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

import construct


class CallsignAdapter(construct.Adapter):
    def _encode(self, obj, context, path=None):
        return bytes([x << 1 for x in bytes(
            (obj.upper() + ' '*6)[:6], encoding='ascii')])

    def _decode(self, obj, context, path=None):
        return str(bytes([x >> 1 for x in obj]), encoding='ascii').strip()


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
    'header' / ax25_header,
    'info' / construct.GreedyBytes
)


def get_sender_callsign(ax25_hdr):
    if ax25_hdr:
        x = ax25_hdr.addresses[1]
        return '%s-%s' % (x.callsign, x.ssid.ssid)
