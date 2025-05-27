#  Copyright (c) 2024. Alexander Baskikh
#
#  MIT License (MIT), http://opensource.org/licenses/MIT
#  Full license can be found in the LICENSE-MIT file
#
#  SPDX-License-Identifier: MIT

import datetime as dt

import construct

from SatsDecoder.systems import ax25, common
from SatsDecoder.systems.image_receiver import ImageReceiver

__all__ = 'RoseyProtocol',

proto_name = 'roseycubesat'


IMG = 0x0CA4
MSG = 0xFFFF

message = construct.Struct(
    '_name' / construct.Computed('message'),
    'name' / construct.Computed('Periodic Message'),
    'text' / construct.PaddedString(30, 'utf-8'),
    'Time' / common.UNIXTimestampAdapter(construct.Int32ul),
    'vbat' / construct.Int16ul,
    'ibat' / construct.Int16sl,
    'temp' / construct.Int16sl,
    'mode' / construct.Hex(construct.Int8ul),
    'eps_boot_cnt' / construct.Int16ul,
    'cmd_cnt' / construct.Int16ul,
)

image = construct.Struct(
    'pad0' / construct.Hex(construct.Int16ul),
    'id' / construct.Hex(construct.Int8ul),
    'pnum' / construct.Hex(construct.Int16ub),
    'data' / construct.GreedyBytes,
    # 'data' / construct.Bytes(construct.this._.pl_size - 7),  # 80b?
)

packet_map = {
    MSG: message,
    IMG: image,
}

frame = construct.Struct(
    'pl_size' / construct.Int8ul,
    'pl_to' / construct.Int8ul,
    'packet_id' / construct.Hex(construct.Int16ul),
    'packet' / construct.Switch(construct.this.packet_id, packet_map, default=construct.GreedyBytes),
    # 'packet' / construct.Switch(construct.this.packet_id, packet_map, default=construct.Bytes(construct.this.pl_size - 2)),
)

rosey = construct.Struct(
    'ax25' / construct.Peek(ax25.ax25_header),
    'ax25' / construct.If(construct.this.ax25, ax25.ax25_header),
    'rosey' / construct.If(lambda this: (bool(this.ax25) and this.ax25.pid == 0xF0), frame),
)


class RoseyImageReceiver(ImageReceiver):
    PACKET_LEN = 80
    MAX_PACKETS = 2160

    def __init__(self, outdir):
        super().__init__(outdir, '.raw')
        self.prev_off = 0

    def generate_fid(self):
        if not (self.current_fid and self.merge_mode):
            self.last_date = now = dt.datetime.now()
            self.current_fid = f'RoseyCubesat-1_{now.strftime("%Y-%m-%d_%H-%M-%S,%f")}'
        return self.current_fid

    def new_file(self, fid, sz=None):
        img = super().new_file(fid)
        img.f.truncate(self.MAX_PACKETS * self.PACKET_LEN)
        img.mode = 'bytes'
        img.mode_kw = dict(
            mode='L',
            size=(480, 360),
            decoder_name='raw',
            args=('L',),
        )
        img.first_data_offset = 0
        img.mosaic = 'bayer;grbg'
        return img

    def push_data(self, data, **kw):
        if data.packet.id != 0x00:
            # this is thumbnail 48x36
            return

        off = data.packet.pnum * self.PACKET_LEN
        f = self.get_image(off < self.prev_off)
        self.prev_off = off
        with f.lock:
            f.push_data(off, data.packet.data)

        return 1


class RoseyProtocol(common.Protocol):
    columns = 'msg_id',
    c_width = 60,
    has_ax25 = 1

    tlm_table = {
        'message': {
            'table': (
                ('name', 'Name'),
                ('text', 'Message'),
                ('Time', 'Onboard Time'),
                ('vbat', 'Battery Voltage'),
                ('ibat', 'Battery Current'),
                ('temp', 'Temperature'),
                ('mode', 'Mode'),
                ('eps_boot_cnt', 'EPS Boot Counter'),
                ('cmd_cnt', 'Command Counter'),
            ),
        },
    }

    def __init__(self, outdir):
        super().__init__(RoseyImageReceiver(outdir))

    def recognize(self, bb):
        data = rosey.parse(bb)
        if not data.rosey:
            return

        name = self.get_sender_callsign(data)
        if data.rosey.packet_id == IMG:
            x = self.ir.push_data(data.rosey)
            if x:
                yield 'img', name, '0x%04X' % data.rosey.packet_id, (x, self.ir.cur_img)

        elif data.rosey.packet_id == MSG:
            yield 'tlm', name, '0x%04X' % data.rosey.packet_id, (data, data.rosey.packet)

        else:
            yield 'raw', name, '0x%04X' % data.rosey.packet_id, data.rosey.packet

    def create_new_image(self):
        return (-1,) + super().create_new_image()
