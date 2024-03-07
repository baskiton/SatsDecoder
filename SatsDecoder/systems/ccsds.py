import construct

from SatsDecoder.systems import ax25, common


# Transfer Frame

vcid = construct.Enum(construct.BitsInteger(3),
                      **{'Online STD HK': 0,
                         'Online EXT HK': 1,
                         'Offline STD HK': 2,
                         'Offline EXT HK': 3,
                         'OBDH Bin': 4,
                         'Payload Bin': 5,
                         'Payoad Bin': 6,
                         'Bin': 7})

tf_hdr = construct.BitStruct(
    'TFVN' / construct.BitsInteger(2),      # Transfer frame version number
    'SCID' / construct.Hex(construct.BitsInteger(10)),     # Spacecraft Identifier
    'VCID' / construct.BitsInteger(3),      # Virtual channel identifier
    'OCFF' / construct.Flag,                # Operational control field flag
    'MCFC' / construct.BitsInteger(8),      # Master channel frame count
    'VCFC' / construct.BitsInteger(8),      # Virtual channel frame count
    'TF_SHF' / construct.Flag,              # TF secondary header flag
    'SYNCHFLAG' / construct.Flag,           # Synchronisation flag
    'POF' / construct.Flag,                 # Packet order flag
    'SLID' / construct.BitsInteger(2),      # Segment length identifier
    'FHP' / construct.BitsInteger(11),      # First header pointer
)

ocf_trailer = construct.BitStruct(
    'control_word_type' / construct.Flag,
    'clcw_version_number' / construct.BitsInteger(2),
    'status_field' / construct.BitsInteger(3),
    'cop_in_effect' / construct.BitsInteger(2),
    'virtual_channel_identification' / construct.BitsInteger(6),
    'rsvd_spare1' / construct.BitsInteger(2),
    'no_rf_avail' / construct.Flag,
    'no_bit_lock' / construct.Flag,
    'lockout' / construct.Flag,
    'wait' / construct.Flag,
    'retransmit' / construct.Flag,
    'farmb_counter' / construct.BitsInteger(2),
    'rsvd_spare2' / construct.Flag,
    'report_value' / construct.BitsInteger(8),
)

transfer_frame = construct.Struct(
    'TFHead' / tf_hdr,
    '_pad' / construct.If(0 < construct.this.TFHead.FHP < 0x7FF, construct.Bytes(construct.this.TFHead.FHP)),
    'payload' / construct.Bytes(construct.this._.size),
    'ocf_trailer' / construct.If(construct.this.TFHead.OCFF == 1, ocf_trailer),
    'FECFD' / construct.Hex(construct.Int16ul),    # Frame Error Control Field Data
)

# Space Packet

sec_hdr_1 = construct.BitStruct(
    'TS' / common.UNIXTimestampAdapter(construct.BitsInteger(32)),  # data creation timestamp
    # 'TS' / construct.BitsInteger(32),  # data creation timestamp
    'CRC_OK' / construct.Flag,          # CRC of data was ok on board
    'INT' / construct.BitsInteger(7),   # frame interval
    'length' / construct.Computed(5),
)
sec_hdr_2 = construct.BitStruct(
    'TL' / construct.BitsInteger(16),   # total number of space packets used for this binary stream - 1
    'length' / construct.Computed(2),
)

sp_hdr = construct.BitStruct(
    'PVN' / construct.BitsInteger(3),       # Packet version number
    'PT' / construct.BitsInteger(1),        # Packet Type Indicator
    'SHF' / construct.Flag,                 # Packet Secondary header flag
    'APID' / construct.Hex(construct.BitsInteger(11)),     # Application process identifier
    'SEQFLAG' / construct.BitsInteger(2),   # GroupingFlags: 0 - next Source Packet of the current Group, 1 - first Source Packet of a new Group, 2 - last Source Packet of the current Group, 3 - no Grouping
    'PSC' / construct.BitsInteger(14),      # Source Sequence Count
    'PDL' / construct.BitsInteger(16),      # Packet data length - 1
)

sp_frame = construct.Struct(
    'SPHead' / sp_hdr,
    'sec_hdr' / construct.If(construct.this.SPHead.SHF, construct.IfThenElse(construct.this._._.VCID < 4, sec_hdr_1, sec_hdr_2)),
    'data' / construct.Bytes(construct.this.SPHead.PDL + 1 - (construct.this.sec_hdr and construct.this.sec_hdr.length or 0)),  # up to 239
)


def parse_transfer_frame(data):
    _ax25 = ax25.ax25.parse(data)
    if _ax25.header.pid != 0xF0:
        return

    sz = len(_ax25.info) - 8
    tf = tf_hdr.parse(_ax25.info)
    if tf.FHP == 0x7FF:
        tf.FHP = 0

    sz -= tf.FHP
    if tf.OCFF == 1:
        sz -= 4

    _ax25.info = transfer_frame.parse(_ax25.info, size=sz)

    return _ax25


sp_packets = construct.Struct(
    'packets' / construct.GreedyRange(sp_frame),
    'lost' / construct.GreedyBytes,
)


def parse_space_packet(data):
    packet = parse_transfer_frame(data)
    if not packet:
        return

    packet.info.payload = sp_packets.parse(packet.info.payload, VCID=packet.info.TFHead.VCID)
    return packet


def get_time_from_sp(sp):
    if sp.sec_hdr:
        return sp.sec_hdr.get('TS')
