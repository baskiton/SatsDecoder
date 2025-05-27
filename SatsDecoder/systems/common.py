# Parts of this file borrowed from gr-satellites
# https://github.com/daniestevez/gr-satellites/blob/main/python/adapters.py

# Copyright 2018 Daniel Estevez <daniel@destevez.net>
#
# This file is part of gr-satellites
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

import datetime as dt

import construct

from SatsDecoder.systems import ax25
from SatsDecoder.systems.image_receiver import ImageReceiver


class UNIXTimestampAdapter(construct.Adapter):
    def _encode(self, obj, context, path=None):
        return round(obj.timestamp())

    def _decode(self, obj, context, path=None):
        return dt.datetime.utcfromtimestamp(obj)


class UNIXTimestampUsAdapter(construct.Adapter):
    def _encode(self, obj, context, path=None):
        return round(obj.timestamp() * 1000000)

    def _decode(self, obj, context, path=None):
        return dt.datetime.utcfromtimestamp(obj / 1000000)


class TimeDeltaAdapter(construct.Adapter):
    def _encode(self, obj, context, path=None):
        return round(obj.total_seconds())

    def _decode(self, obj, context, path=None):
        return dt.timedelta(seconds=obj)


class AffineAdapter(construct.Adapter):
    def __init__(self, c, a, *args, **kwargs):
        self.c = c
        self.a = a
        super().__init__(*args, **kwargs)
        # return construct.Adapter.__init__(self, *args, **kwargs)

    def _encode(self, obj, context, path=None):
        return int(round(obj * self.c + self.a))

    def _decode(self, obj, context, path=None):
        return (float(obj) - self.a) / self.c


class LinearAdapter(AffineAdapter):
    def __init__(self, c, *args, **kwargs):
        super().__init__(c, 0, *args, **kwargs)
        # return AffineAdapter.__init__(self, c, 0, *args, **kwargs)


class EvalAdapter(construct.Adapter):
    def __init__(self, xfunc, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.xfunc = xfunc

    def _decode(self, x, ctx, path=None):
        return eval(self.xfunc)


class Protocol:
    columns = ()
    c_width = ()
    tlm_table = {}
    has_ax25 = 0

    def __init__(self, ir: ImageReceiver = None):
        self.ir = isinstance(ir, ImageReceiver) and ir

    @staticmethod
    def get_sender_callsign(data):
        return ax25.get_sender_callsign(data.ax25)

    @staticmethod
    def get_receiver_callsign(data):
        return ax25.get_receiver_callsign(data.ax25)

    def recognize(self, bb):
        raise NotImplementedError

    def create_new_image(self):
        return self.ir.force_new(),
