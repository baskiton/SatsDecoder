#  Copyright (c) 2026. Alexander Baskikh
#
#  MIT License (MIT), http://opensource.org/licenses/MIT
#  Full license can be found in the LICENSE-MIT file
#
#  SPDX-License-Identifier: MIT


import construct

from SatsDecoder.systems import ax25, common
from SatsDecoder.systems.image_receiver import ImageReceiver

__all__ = 'MarinaProtocol',

proto_name = 'marina'

# based on https://community.libre.space/t/marina-image-decoder-observation-14504799/15024


data_hdr = construct.Struct(
    'marker0' / construct.Hex(construct.Const(0x87, construct.Int8ub)),
    'res0' / construct.Bytes(2),
    'zero' / construct.Const(0, construct.Int8ub),
    'marker1' / construct.Hex(construct.Int8ub),
    'id' / construct.Bytes(8),
    'marker2' / construct.Hex(construct.Int8ub),
    'data' / construct.GreedyBytes
)

img_init = construct.Struct(
    'sz' / construct.Int16ub,
    'crc' / construct.Bytes(9)
)

img_firsts = construct.Struct(
    'off' / construct.Int8ub,
    'res' / construct.Const(0x58, construct.Int8ub),
    'sz' / construct.Int8ub,
    'data' / construct.Bytes(construct.this.sz),
    'crc' / construct.Bytes(9)
)

img_general = construct.Struct(
    'marker0' / construct.Const(0x19, construct.Int8ub),
    'off' / construct.Int16ub,
    'res' / construct.Const(0x58, construct.Int8ub),
    'sz' / construct.Int8ub,
    'data' / construct.Bytes(construct.this.sz),
    'crc' / construct.Bytes(9)
)


class MarinaImageReceiver(ImageReceiver):
    FULL_DATA_SZ = 142

    def __init__(self, outdir):
        super().__init__(outdir, '.jpg')
        self._fids = {}

    def generate_fid(self, id_, force=0, t=None):
        if force or not (self.current_fid and self.merge_mode):
            self.current_fid = self._fids.get(id_)
            if not self.current_fid:
                self.current_fid = f'Marina_{id_.hex()}_{self.strftime(t)}'
                self._fids[id_] = self.current_fid
        return self.current_fid

    def push_data(self, data, t=None, **kw):
        try:
            hdr = data_hdr.parse(data)
        except construct.StreamError:
            return

        if hdr.marker1 == 0x83:     # image init
            x = img_init.parse(hdr.data)
            img = self.get_image(1, id_=hdr.id, force=1, t=t)
            print(hdr.id, self.current_fid)

            with img.lock:
                img.has_starter = 1
                img.open().truncate(x.sz)

        elif hdr.marker1 == 0x84:   # image transfer
            img = self.get_image(id_=hdr.id, t=t)
            with img.lock:
                if len(hdr.data) == (self.FULL_DATA_SZ - 2) and hdr.data[:2] == b'\x00\x58' and hdr.data[3:5] == b'\xff\xd8':
                    x = img_firsts.parse(hdr.data)
                    img.has_soi |= 0b01
                elif len(hdr.data) == (self.FULL_DATA_SZ - 1) and hdr.data[0] == 0x18 and hdr.data[2] == 0x58:
                    x = img_firsts.parse(hdr.data[1:])
                    img.has_soi |= 0b10
                else:
                    x = img_general.parse(hdr.data)

                img.push_data(x.off, x.data)
                if x.off < img.first_data_offset:
                    img.first_data_offset = x.off

        else:
            return
        return 1


class MarinaProtocol(common.Protocol):

    def __init__(self, outdir):
        super().__init__(MarinaImageReceiver(outdir))

    def recognize(self, bb, t=None):
        try:
            frame = ax25.ax25.parse(bb)
        except construct.StreamError as e:
            frame = 0

        if frame and frame.header.pid == 0xF0: #and ax25.get_sender_callsign(frame.header).startswith('OM9MAR'):
            yield 'raw', ax25.get_sender_callsign(frame.header), frame.info
        elif self.ir.push_data(bb, t):
            yield 'img', 'Marina', (1, self.ir.cur_img)
        else:
            yield 'raw', 'Marina', bb[4:-4]
