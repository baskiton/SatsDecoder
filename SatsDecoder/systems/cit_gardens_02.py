#  Copyright (c) 2024. Alexander Baskikh
#
#  MIT License (MIT), http://opensource.org/licenses/MIT
#  Full license can be found in the LICENSE-MIT file
#
#  SPDX-License-Identifier: MIT

import construct

from SatsDecoder.systems import common
from SatsDecoder.systems.image_receiver import ImageReceiver

__all__ = 'CitGardens02Protocol',

proto_name = 'cit-gardens-02'

"""
https://sites.google.com/view/gardens-02/english_ver/home
https://sites.google.com/view/gardens-02/english_ver/document/transmission-format
https://x.com/CitGardens/status/1810292367527723258
"""


PKT_SEP = b'\xc0\xc0\x00'
PKT_HDR = b'\xf0\xff\xf0\xff'
packets = construct.Struct(
    'tx_id' / construct.Hex(construct.Int8ub),
    'p_num' / construct.Hex(construct.Int16ub),
    'data' / construct.GreedyBytes,
)

hdrs = {
    PKT_HDR: packets,
    # b'\xf0\xaa\x03K': None,
}

gardens_len = 7 + 7 + 1 + 4
gardens = construct.Struct(
    'to_cs' / construct.PaddedString(7, 'ascii'),
    'fr_cs' / construct.PaddedString(7, 'ascii'),
    'const' / construct.Const(b'>', construct.Bytes(1)),
    'hdr' / construct.Bytes(4),
    'data' / construct.GreedyBytes,
    # 'data' / construct.Switch(construct.this.hdr, hdrs, default=construct.GreedyBytes),
)


class Gardens02ImageReceiver(ImageReceiver):
    PKT_SZ = 61

    def __init__(self, outdir):
        super().__init__(outdir, '.jpg')
        self.unreliable_id = set()
        self.last_id = -1

    def generate_fid(self, force=0, name='Gardens-02', tx_id=0, t=None):
        if force or not (self.current_fid and self.merge_mode):
            self.current_fid = f'{name}_{self.strftime(t)}_{tx_id:02X}'
        return self.current_fid

    def push_data(self, pkt, name='Gardens-02', t=None, **kw):
        tx_id = pkt.tx_id
        p_num = pkt.p_num
        soi = not p_num and pkt.data.startswith(b'\xff\xd8')

        if not p_num and not soi:
            # TODO: log it. it's not image
            self.unreliable_id.add(tx_id)
            return

        if tx_id in self.unreliable_id:
            # TODO: log it. no-image data
            return

        if soi:
            self.unreliable_id.discard(tx_id)

        force_new = self.last_id == -1 or self.last_id != tx_id
        self.last_id = tx_id

        img = self.get_image(force_new or soi, force=force_new, name=name, tx_id=tx_id, t=t)
        with img.lock:
            img.has_soi ^= soi
            off = p_num * self.PKT_SZ
            if off < img.first_data_offset:
                img.first_data_offset = off

            img.push_data(off, pkt.data)
            if b'\xff\xd9' in pkt.data:
                img.flush()
                return 2

        return 1


class CitGardens02Protocol(common.Protocol):

    @staticmethod
    def get_sender_callsign(data):
        return data.fr_cs

    def __init__(self, outdir):
        super().__init__(Gardens02ImageReceiver(outdir))

    def recognize(self, bb, t=None):
        try:
            x = gardens.parse(bb)
        except:
            return
        if not x:
            return

        name = self.get_sender_callsign(x)

        if x.hdr == PKT_HDR:
            h = bb[:gardens_len]
            for i in bb.split(h)[1:]:
                if i.endswith(PKT_SEP):     # py3.9 == .removesuffix()
                    i = i[:-len(PKT_SEP)]
                pkt = packets.parse(i)

                if pkt.tx_id == 0xFF and pkt.p_num == 0xFFFF:
                    # invalid packet
                    continue

                if len(pkt.data) == Gardens02ImageReceiver.PKT_SZ:  # image packet
                    yield 'img', name, (self.ir.push_data(pkt, name, t), self.ir.cur_img)
