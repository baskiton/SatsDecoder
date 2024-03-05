import datetime as dt

import construct


# AX.25

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


def ax25_get_sender_callsign(ax25):
    if ax25:
        x = ax25.addresses[1]
        return '%s-%s' % (x.callsign, x.ssid.ssid)


###############################################################################


class UNIXTimestampAdapter(construct.Adapter):
    def _encode(self, obj, context, path=None):
        return round(obj.timestamp())

    def _decode(self, obj, context, path=None):
        return dt.datetime.utcfromtimestamp(obj)


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
