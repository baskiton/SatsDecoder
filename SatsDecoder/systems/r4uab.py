#  Copyright (c) 2026. Alexander Baskikh
#
#  MIT License (MIT), http://opensource.org/licenses/MIT
#  Full license can be found in the LICENSE-MIT file
#
#  SPDX-License-Identifier: MIT

import pathlib

import construct

from SatsDecoder import utils
from SatsDecoder.systems import ax25, common
from SatsDecoder.systems.image_receiver import ImageReceiver

__all__ = 'R4uabProtocol',

proto_name = 'r4uab'

# marker-variants:
#   FF01: jpg 640x480
#   FF02: jpg 320x240
#   FF03: png 640x480
#   FF04: png 320x240

# ptype-variant
#   00: jpg
#   01: png
ptype_suff = {
    0: '.jpg',
    1: '.png',
}

FILETRANSFER_FILESIZE = 0x07
FILETRANSFER_DATA = 0x08

ptype_map = {
    FILETRANSFER_FILESIZE: construct.Struct(
        'size' / construct.Int16ul,
    ),
    FILETRANSFER_DATA: construct.Struct(
        'pnum' / construct.Int16ul,
        'data' / construct.GreedyBytes,
    ),
}

packet = construct.Struct(
    'hdr' / construct.Hex(construct.Const(0xC100E000, construct.Int32ub)),
    'marker' / construct.Hex(construct.Int8ub),
    'marker_variant' / construct.Hex(construct.Int8ub),
    'ptype' / construct.Hex(construct.Int8ub),
    'ptype_variant' / construct.Hex(construct.Int8ub),
    'payload' / construct.Switch(construct.this.ptype, ptype_map, default=None),
)

r4uab = construct.Struct(
    'ax25' / construct.Peek(ax25.ax25_header),
    'ax25' / construct.If(lambda this: bool(this.ax25), ax25.ax25_header),
    'packet' / construct.Peek(packet),
    'packet' / construct.If(lambda this: (bool(this.ax25) and this.ax25.pid == 0xF0),
                            construct.IfThenElse(lambda this: bool(this.packet) and this.packet.payload is not None, packet, construct.GreedyBytes)),
)


class R4uabImageReceiver(ImageReceiver):
    DATA_LEN = 200

    def __init__(self, outdir):
        super().__init__(outdir)
        self.last_transfer_id = None

    def generate_fid(self, ptype_variant, t=None):
        if not (self.current_fid and self.merge_mode):
            self.current_fid = f'R4UAB_{self.strftime(t)}'
        return self.current_fid

    def transfer_id_process(self, transfer_id, ptype_variant):
        if self.last_transfer_id != transfer_id:
            self.last_transfer_id = transfer_id
            self.suff = ptype_suff.get(ptype_variant, '.bin')
            return 1

    def push_data(self, packet, t=None, **kw):
        if packet.marker != 0xFF:
            return

        transfer_id = (packet.marker << 16) | (packet.marker_variant << 8) | packet.ptype_variant

        if packet.ptype == FILETRANSFER_DATA:
            force = self.transfer_id_process(transfer_id, packet.ptype_variant)
            if not self.suff:
                self.suff = ptype_suff.get(packet.ptype_variant, '.bin')
            off = self.DATA_LEN * (packet.payload.pnum - 1)
            img = self.get_image(force, t=t, ptype_variant=packet.ptype_variant)
            with img.lock:
                img.push_data(off, packet.payload.data[:self.DATA_LEN])
                if off < img.first_data_offset:
                    img.first_data_offset = off

        elif packet.ptype == FILETRANSFER_FILESIZE:
            force = self.transfer_id_process(transfer_id, packet.ptype_variant)
            img = self.get_image(force, t=t, ptype_variant=packet.ptype_variant)
            with img.lock:
                img.has_starter = 1
                img.open().truncate(packet.payload.size)

        else:
            return

        return 1


class R4uabProtocol(common.Protocol):

    def __init__(self, outdir):
        super().__init__(R4uabImageReceiver(outdir))

    def recognize(self, bb, t=None):
        try:
            frame = r4uab.parse(bb)
            if not frame.packet:
                return
        except construct.ConstError:
            return
        except construct.StreamError as e:
            print(e)
            print(bb)
            return

        ty = 'raw'
        data = frame.packet
        if not isinstance(frame.packet, bytes):
            x = self.ir.push_data(frame.packet, t=t)
            if x:
                ty = 'img'
                data = (x, self.ir.cur_img)
        yield ty, self.get_sender_callsign(frame), data


if __name__ == '__main__':
    bb = (
        'C100E000FF010700848F0000',
        'C100E000FF0108000100FFD8FFDB0084000D09090B0A080D0B0A0B0E0E0D0F13201513121213271C1E17202E2931302E292D2C333A4A3E333646372C2D405741464C4E525352323E5A615A50604A51524F010E0E0E131113261515264F352D354F4F4F4F4F4F4F4F4F4F4F4F4F4F4F4F4F4F4F4F4F4F4F4F4F4F4F4F4F4F4F4F4F4F4F4F4F4F4F4F4F4F4F4F4F4F4F4F4F4FFFC401A20000010501010101010100000000000000000102030405060708090A0B100002010303020403050504040000017D0102030004110512213141061351',
        'DEADBEEF',
        'C100E000FF0103E0'
    )
    for b in bb:
        b = bytes.fromhex(b)
        try:
            x = r4uab.parse(b)
        except construct.ConstError:
            continue
        print(x)
        xx = x.packet
        transfer_id = (xx.marker << 16) | (xx.marker_variant << 8) | xx.ptype_variant
        print(hex(transfer_id))
        print(f'{xx.marker:02X}{xx.marker_variant:02X}{xx.ptype_variant:02X}')
