import pathlib

import construct

from SatsDecoder import utils
from SatsDecoder.systems import ax25, common

from SatsDecoder.systems.image_receiver import ImageReceiver
from SatsDecoder.systems.usp import tlm_map, filetransfer
from SatsDecoder.systems.usp import UspProtocol as UspProtocolBase

__all__ = 'UspRS18SProtocol',

proto_name = 'usp_rs18s'

def _flags(*names):
    return construct.BitStruct(*[
        ('_reserved%d' % i if n is None else n) / construct.Flag
        for i, n in enumerate(names)
    ])

pl_status_flags = _flags(
    'speed_step', 'sstv_held', 'sstv_event', 'orbit_valid', 'overcurrent', 'time_lock', 'low_power', 'safe_mode',
)

pl_adcs_flags = _flags(
    None, None, None, None, None, 'adcs_bdot', 'adcs_valid', 'adcs_on',
)

pl_mfs_flags = _flags(
    'mfs_replay', 'mfs_on_air', 'mfs_more', 'mfs_ax25', 'mfs_locked', 'mfs_scanning', 'mfs_ready', 'mfs_enabled',
)

pl_sstv_flags = _flags(
    None, None, None, 'sstv_on_air', 'sstv_fix', 'sstv_grid', 'sstv_area', 'sstv_set',
)

sbc_beacon_flags = _flags(
    'hv_trip', 'frozen', 'diag_mode', 'drift_step', 'saturated', 'product_ready', 'event', 'sensing',
)

sbc_beacon_tlm_flags = _flags(
    None, 'tlm_hv_trip', 'tlm_frozen', 'tlm_diag_mode', 'tlm_drift_compensation', 'tlm_product_ready', 'tlm_event', 'tlm_sensing',
)

attitude_flags = _flags(
    'rate_high', 'angle', 'eclipse', 'triad', 'sun_valid', 'light', 'mag', 'orbit', 
    None, None, None, None, 'run', 'eop', 'point_sample', 'bdot',
)

PL_MAIN_BEACON = 0x1C1C
PL_ALT_BEACON = 0x1C1D
SBC_BEACON = 0x1033
ATTITUDE = 0x0876
MSG_ECHO = 0x0881
MSG_LONG_CHAT_STORED = 0x0849
MSG_LONG_NODE_TEXT = 0x0824
MSG_LONG_MSG_DIGITAL = 0x0847

# SAKHACUBE-CHOLBON definitions:
# https://tdas.tmtc.yksa.space/packets/definitions/1/export.xtce
pl_main_beacon = construct.Struct(
    '_name' / construct.Computed('pl_main_beacon'),
    'name' / construct.Computed('Primary payload supervisor beacon'),
    'Time' / common.UNIXTimestampAdapter(construct.Int32ul),
    'last_gs_contact' / common.UNIXTimestampAdapter(construct.Int32ul),
    'flags0' / pl_status_flags,
    'nodes_present' / construct.Int8ul,
    'muxpos' / construct.Int8ul,
    'node_pwr_status' / construct.Int8ul,
    'node_rst_status' / construct.Int8ul,
    'cluster_tx_bytes' / construct.Int32ul,
    'cluster_rx_bytes' / construct.Int32ul,
    'sbc_last_reply' / common.UNIXTimestampAdapter(construct.Int32ul),
    'flash_used_blocks' / construct.Int16ul,
    'flash_free_blocks' / construct.Int16ul,
    'active_schedules' / construct.Int8ul,
    'scheduler_queue_len' / construct.Int8ul,
    'bus_current' / construct.Int16ul,
    'bus_current_max' / construct.Int16ul,
    'adcs_rate_x' / construct.Float32l,
    'adcs_rate_y' / construct.Float32l,
    'adcs_rate_z' / construct.Float32l,
    'adcs_mag_x' / construct.Float32l,
    'adcs_mag_y' / construct.Float32l,
    'adcs_mag_z' / construct.Float32l,
    'flags1' / pl_adcs_flags,
    'adcs_last_bdot' / common.UNIXTimestampAdapter(construct.Int32ul),
)

pl_alt_beacon = construct.Struct(
    '_name' / construct.Computed('pl_alt_beacon'),
    'name' / construct.Computed('Secondary payload supervisor beacon'),
    'Time' / common.UNIXTimestampAdapter(construct.Int32ul),
    'last_gs_contact' / common.UNIXTimestampAdapter(construct.Int32ul),
    'flags0' / pl_status_flags,
    'nodes_present' / construct.Int8ul,
    'muxpos' / construct.Int8ul,
    'node_pwr_status' / construct.Int8ul,
    'node_rst_status' / construct.Int8ul,
    'cluster_tx_bytes' / construct.Int32ul,
    'cluster_rx_bytes' / construct.Int32ul,
    'sbc_last_reply' / construct.Int32ul, # always 0 on 0x1D payload
    'flash_used_blocks' / construct.Int16ul,
    'flash_free_blocks' / construct.Int16ul,
    'active_schedules' / construct.Int8ul,
    'scheduler_queue_len' / construct.Int8ul,
    'bus_current' / construct.Int16ul,
    'bus_current_max' / construct.Int16ul,
    'flags1' / pl_mfs_flags,
    'mfs_cached' / construct.Int8ul,
    'mfs_sent' / construct.Int16ul,
    'mfs_failed' / construct.Int16ul,
    'mfs_next_id' / construct.Int16ul,
    'mfs_next_slot' / construct.Int32ul,
    'sstv_state' / construct.Int8ul,
    'flags2' / pl_sstv_flags,
    'sstv_next_file' / construct.Int8ul,
    'sstv_sent' / construct.Int16ul,
    'sstv_refused' / construct.Int16ul,
    'sstv_out_of_area' / construct.Int16ul,
    'sstv_last_tx' / common.UNIXTimestampAdapter(construct.Int32ul),
)

u24 = construct.Struct(
    'lo' / construct.Int16ul,
    'hi' / construct.Int8ul,
    'value' / construct.Computed(lambda this: this.lo | (this.hi << 16)),
)

sbc_beacon = construct.Struct(
    '_name' / construct.Computed('sbc_beacon'),
    'name' / construct.Computed('Gamma Spectrometer beacon'),
    'flags0' / sbc_beacon_flags,
    'interval_ms' / construct.Int32ul,
    'counts_raw' / u24,
    'triggers_raw' / u24,
    'n_bands' / construct.Int8ul,
    'band_raw' / construct.Array(8, u24),
    'hv_temp_raw' / construct.Int16sl,
    'amp_temp_raw' / construct.Int16sl,
    'sipm_temp_raw' / construct.Int16sl,
    'mcu_temp_raw' / construct.Int16sl,
    'vbias' / construct.Int16ul,
    'pot_hv' / construct.Int8ul,
    'pot_amp' / construct.Int8ul,
    'pot_det' / construct.Int8ul,
    'rest_mv_raw' / construct.Int16ul,
    'rest_noise_raw' / construct.Int8ul,
    'baseline_cps' / construct.Int16ul,
    'product_id' / construct.Int16ul,
    'product_len' / construct.Int16ul,
    'product_age_ms' / construct.Int32ul,
    'light_xn' / construct.Int16ul,
    'light_xp' / construct.Int16ul,
    'light_yn' / construct.Int16ul,
    'light_yp' / construct.Int16ul,
    'light_zn' / construct.Int16ul,
    'light_zp' / construct.Int16ul,
    'below_threshold_raw' / u24,
    'pileup_raw' / u24,
    'live_ms' / construct.Int32ul,
    'stat_triggers' / construct.Int32ul,
    'stat_accepted' / construct.Int32ul,
    'stat_below_threshold' / construct.Int32ul,
    'stat_pileup' / construct.Int32ul,
    'stat_busy' / construct.Int32ul,
    'stat_live_ms' / construct.Int32ul,
    'stat_edge_delay' / construct.Array(8, construct.Int32ul),
    'uptime' / common.TimeDeltaAdapter(construct.Int32ul),
    'flags1' / sbc_beacon_tlm_flags,
    'tlm_total_counts' / construct.Int32ul,
    'counts' / construct.Computed(lambda this: this.counts_raw.value),
    'triggers' / construct.Computed(lambda this: this.triggers_raw.value),
    'below_threshold' / construct.Computed(lambda this: this.below_threshold_raw.value),
    'pileup' / construct.Computed(lambda this: this.pileup_raw.value),
    'band0' / construct.Computed(lambda this: this.band_raw[0].value),
    'band1' / construct.Computed(lambda this: this.band_raw[1].value),
    'band2' / construct.Computed(lambda this: this.band_raw[2].value),
    'band3' / construct.Computed(lambda this: this.band_raw[3].value),
    'band4' / construct.Computed(lambda this: this.band_raw[4].value),
    'band5' / construct.Computed(lambda this: this.band_raw[5].value),
    'band6' / construct.Computed(lambda this: this.band_raw[6].value),
    'band7' / construct.Computed(lambda this: this.band_raw[7].value),
    'hv_temp' / construct.Computed(lambda this: this.hv_temp_raw * 0.1),
    'amp_temp' / construct.Computed(lambda this: this.amp_temp_raw * 0.1),
    'sipm_temp' / construct.Computed(lambda this: this.sipm_temp_raw * 0.1),
    'mcu_temp' / construct.Computed(lambda this: this.mcu_temp_raw * 0.1),
    'rest_mv' / construct.Computed(lambda this: this.rest_mv_raw * 0.1),
    'rest_noise_mv' / construct.Computed(lambda this: this.rest_noise_raw * 0.1),
)

attitude = construct.Struct(
    '_name' / construct.Computed('attitude'),
    'name' / construct.Computed('TRIAD Attitude solution'),
    'Time' / common.UNIXTimestampAdapter(construct.Int32ul),
    'flags0' / attitude_flags,
    'frame' / construct.Enum(construct.Int8ul, J2000=0, ITRF=1),
    'point_status' / construct.Int8ul,
    'set_id' / construct.Int16ul,
    'r_x' / construct.Float32l,
    'r_y' / construct.Float32l,
    'r_z' / construct.Float32l,
    'v_x' / construct.Float32l,
    'v_y' / construct.Float32l,
    'v_z' / construct.Float32l,
    'q_w' / construct.Float32l,
    'q_x' / construct.Float32l,
    'q_y' / construct.Float32l,
    'q_z' / construct.Float32l,
    'sun_x_raw' / construct.Int16sl,
    'sun_y_raw' / construct.Int16sl,
    'sun_z_raw' / construct.Int16sl,
    'mag_x_raw' / construct.Int16sl,
    'mag_y_raw' / construct.Int16sl,
    'mag_z_raw' / construct.Int16sl,
    'rate_x_raw' / construct.Int16sl,
    'rate_y_raw' / construct.Int16sl,
    'rate_z_raw' / construct.Int16sl,
    'field_ref_raw' / construct.Int16ul,
    'field_check_raw' / construct.Int16sl,
    'field_sun_angle' / construct.Int8ul,
    'nadir_angle' / construct.Int8ul,
    'sun_x' / construct.Computed(lambda this: this.sun_x_raw * 0.0001),
    'sun_y' / construct.Computed(lambda this: this.sun_y_raw * 0.0001),
    'sun_z' / construct.Computed(lambda this: this.sun_z_raw * 0.0001),
    'mag_x' / construct.Computed(lambda this: this.mag_x_raw * 0.01),
    'mag_y' / construct.Computed(lambda this: this.mag_y_raw * 0.01),
    'mag_z' / construct.Computed(lambda this: this.mag_z_raw * 0.01),
    'rate_x' / construct.Computed(lambda this: this.rate_x_raw * 0.001),
    'rate_y' / construct.Computed(lambda this: this.rate_y_raw * 0.001),
    'rate_z' / construct.Computed(lambda this: this.rate_z_raw * 0.001),
    'field_ref' / construct.Computed(lambda this: this.field_ref_raw * 0.01),
    'field_check' / construct.Computed(lambda this: this.field_check_raw * 0.01),
)

chat_message = construct.Struct(
    'magic' / construct.Const(0xC2, construct.Int8ul),
    'msg_seq' / construct.Int16ul,
    'from_len' / construct.Int8ul,
    'to_len' / construct.Int8ul,
    'call_from' / construct.Bytes(construct.this.from_len),
    'call_to' / construct.Bytes(construct.this.to_len),
    'text' / construct.GreedyBytes,
)

def _chat_fields(data):
    def text(b):
        return bytes(b).decode('utf-8', errors='replace')

    try:
        msg = chat_message.parse(data)
    except construct.ConstructError:
        msg = None
    # if the message is invalid, return raw text and empty fields
    if msg is None or not 1 <= msg.from_len <= 10 or msg.to_len > 10:
        return {'msg_seq': '', 'call_from': '', 'call_to': '', 'text': text(data)}
    return {
        'msg_seq': msg.msg_seq,
        'call_from': text(msg.call_from),
        'call_to': text(msg.call_to) or 'all',
        'text': text(msg.text),
    }

chat_fields = (
    '_chat' / construct.Computed(lambda this: _chat_fields(this.data)),
    'msg_seq' / construct.Computed(lambda this: this._chat['msg_seq']),
    'call_from' / construct.Computed(lambda this: this._chat['call_from']),
    'call_to' / construct.Computed(lambda this: this._chat['call_to']),
    'text' / construct.Computed(lambda this: this._chat['text']),
)

echo = construct.Struct(
    '_name' / construct.Computed('echo'),
    'name' / construct.Computed('Echo message'),
    'data' / construct.GreedyBytes,
    *chat_fields,
)

chat_stored = construct.Struct(
    '_name' / construct.Computed('chat_stored'),
    'name' / construct.Computed('Chat message'),
    'seq' / construct.Int32ul,
    'page' / construct.Int8ul,
    'offset' / construct.Int8ul,
    'timestamp' / common.UNIXTimestampAdapter(construct.Int32ul),
    'data' / construct.GreedyBytes,
    *chat_fields,
)

node_text = construct.Struct(
    '_name' / construct.Computed('node_text'),
    'name' / construct.Computed('Node text message'),
    'node_id' / construct.Int8ul,
    'timestamp' / common.UNIXTimestampAdapter(construct.Int32ul),
    'data' / construct.GreedyBytes,
    'text' / construct.Computed(lambda this: bytes(this.data).decode('utf-8', errors='replace')),
)

message_digital = construct.Struct(
    '_name' / construct.Computed('message_digital'),
    'name' / construct.Computed('Message from Space (MFS)'),
    'id' / construct.Int16ul,
    'data' / construct.GreedyBytes,
    'text' / construct.Computed(lambda this: bytes(this.data).decode('utf-8', errors='replace')),
)

rs18s_tlm_map = {
    PL_MAIN_BEACON: pl_main_beacon._name / pl_main_beacon,
    PL_ALT_BEACON: pl_alt_beacon._name / pl_alt_beacon,
    SBC_BEACON: sbc_beacon._name / sbc_beacon,
    ATTITUDE: attitude._name / attitude,
    MSG_ECHO: echo._name / echo,
    MSG_LONG_CHAT_STORED: chat_stored._name / chat_stored,
    MSG_LONG_NODE_TEXT: node_text._name / node_text,
    MSG_LONG_MSG_DIGITAL: message_digital._name / message_digital,
}

rs18s_msg_map = tlm_map.copy()
rs18s_msg_map.update(filetransfer)
rs18s_msg_map.update(rs18s_tlm_map)

rs18s_sender_msg_map = {
    (0x1C << 16) | PL_MAIN_BEACON: pl_main_beacon._name / pl_main_beacon,
    (0x1D << 16) | PL_MAIN_BEACON: pl_alt_beacon._name / pl_alt_beacon,
    (0x1C << 16) | PL_ALT_BEACON: pl_alt_beacon._name / pl_alt_beacon,
    (0x1D << 16) | PL_ALT_BEACON: pl_alt_beacon._name / pl_alt_beacon,
}

Data = construct.Struct(
    'message' / construct.Hex(construct.Int16ul),
    'sender' / construct.Hex(construct.Int16ul),
    'receiver' / construct.Hex(construct.Int16ul),
    'size' / construct.Int16ul,
    'packet' / construct.Switch(
        lambda this: (this.sender << 16) | this.message,
        rs18s_sender_msg_map,
        default=construct.Switch(
            construct.this.message,
            rs18s_msg_map,
            default=construct.Bytes(construct.this.size),
        ),
    ),
)

Frame = construct.Struct(
    'data' / construct.GreedyRange(Data),
    '_tail' / construct.GreedyBytes,
)

usp = construct.Struct(
    'ax25' / construct.Peek(ax25.ax25_header),
    'ax25' / construct.If(lambda this: bool(this.ax25), ax25.ax25_header),
    'usp' / construct.If(lambda this: (bool(this.ax25) and this.ax25.pid == 0xF0), Frame),
)

usp_range = construct.GreedyRange(usp)

class UspRS18SProtocol(UspProtocolBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.tlm_table = UspProtocolBase.tlm_table.copy()
        self.tlm_table.update({
            'pl_main_beacon': {
                'table': (
                    ('name', 'Name', 0),
                    ('Time', 'Supervisor time', 0),
                    ('last_gs_contact', 'Last ground station contact', 0),
                    ('nodes_present', 'Node presence mask', 0),
                    ('muxpos', 'Node UART multiplexer position', 0),
                    ('node_pwr_status', 'Node power status', 0),
                    ('node_rst_status', 'Node reset status', 0),
                    ('cluster_tx_bytes', 'Cluster TX bytes', 1),
                    ('cluster_rx_bytes', 'Cluster RX bytes', 2),
                    ('sbc_last_reply', 'Last spectrometer reply', 0),
                    ('flash_used_blocks', 'Used flash blocks', 1),
                    ('flash_free_blocks', 'Free flash blocks', 2),
                    ('active_schedules', 'Active schedules', 0),
                    ('scheduler_queue_len', 'Scheduler queue length', 0),
                    ('bus_current', 'Bus current, mA', 1),
                    ('bus_current_max', 'Peak bus current, mA', 2),
                    ('adcs_rate_x', 'ADCS rate X, deg/s', 1),
                    ('adcs_rate_y', 'ADCS rate Y, deg/s', 2),
                    ('adcs_rate_z', 'ADCS rate Z, deg/s', 2),
                    ('adcs_mag_x', 'ADCS magnetic field X, nT', 1),
                    ('adcs_mag_y', 'ADCS magnetic field Y, nT', 2),
                    ('adcs_mag_z', 'ADCS magnetic field Z, nT', 2),
                    ('adcs_last_bdot', 'Last B-dot time', 0),
                ),
                'flags': (
                    ('safe_mode', 'Safe mode', 0),
                    ('low_power', 'Low power', 0),
                    ('time_lock', 'Time lock', 0),
                    ('overcurrent', 'Overcurrent', 0),
                    ('orbit_valid', 'Orbit valid', 0),
                    ('sstv_event', 'SSTV event', 0),
                    ('sstv_held', 'SSTV held', 0),
                    ('speed_step', 'Speed step', 0),
                    ('adcs_on', 'ADCS on', 0),
                    ('adcs_valid', 'ADCS valid', 0),
                    ('adcs_bdot', 'B-dot active', 0),
                ),
            },
            'pl_alt_beacon': {
                'table': (
                    ('name', 'Name', 0),
                    ('Time', 'Supervisor time', 0),
                    ('last_gs_contact', 'Last ground station contact', 0),
                    ('nodes_present', 'Node presence mask', 0),
                    ('muxpos', 'Node UART multiplexer position', 0),
                    ('node_pwr_status', 'Node power status', 0),
                    ('node_rst_status', 'Node reset status', 0),
                    ('cluster_tx_bytes', 'Cluster TX bytes', 1),
                    ('cluster_rx_bytes', 'Cluster RX bytes', 2),
                    ('flash_used_blocks', 'Used flash blocks', 1),
                    ('flash_free_blocks', 'Free flash blocks', 2),
                    ('active_schedules', 'Active schedules', 0),
                    ('scheduler_queue_len', 'Scheduler queue length', 0),
                    ('bus_current', 'Bus current, mA', 1),
                    ('bus_current_max', 'Peak bus current, mA', 2),
                    ('mfs_cached', 'Cached messages', 0),
                    ('mfs_sent', 'Messages sent', 0),
                    ('mfs_failed', 'Messages failed', 0),
                    ('mfs_next_id', 'Next message ID', 0),
                    ('mfs_next_slot', 'Next message time', 0),
                    ('sstv_state', 'SSTV state', 0),
                    ('sstv_next_file', 'Next SSTV file', 0),
                    ('sstv_sent', 'SSTV images sent', 0),
                    ('sstv_refused', 'SSTV transmissions refused', 0),
                    ('sstv_out_of_area', 'SSTV transmissions out of area', 0),
                    ('sstv_last_tx', 'Last SSTV transmission', 0),
                ),
                'flags': (
                    ('safe_mode', 'Safe mode', 0),
                    ('low_power', 'Low power', 0),
                    ('time_lock', 'Time lock', 0),
                    ('overcurrent', 'Overcurrent', 0),
                    ('orbit_valid', 'Orbit valid', 0),
                    ('mfs_enabled', 'MFS enabled', 0),
                    ('mfs_ready', 'MFS ready', 0),
                    ('mfs_ax25', 'AX.25 window open', 0),
                    ('mfs_on_air', 'Message on air', 0),
                    ('sstv_set', 'SSTV event set', 0),
                    ('sstv_on_air', 'SSTV on air', 0),
                ),
            },
            'sbc_beacon': {
                'table': (
                    ('name', 'Name', 0),
                    ('interval_ms', 'Poll interval, ms', 0),
                    ('counts', 'Accepted events', 0),
                    ('triggers', 'Triggers', 0),
                    ('n_bands', 'Band count', 0),
                    ('hv_temp', 'High voltage temperature, C', 0),
                    ('amp_temp', 'Amplifier temperature, C', 0),
                    ('sipm_temp', 'SiPM temperature, C', 0),
                    ('mcu_temp', 'MCU temperature, C', 0),
                    ('vbias', 'SiPM bias voltage, mV', 0),
                    ('rest_mv', 'Preamp resting level, mV', 0),
                    ('rest_noise_mv', 'Resting level noise, mV', 0),
                    ('live_ms', 'Live time, ms', 0),
                    ('uptime', 'Spectrometer uptime, s', 0),
                    ('tlm_total_counts', 'Spectrometer total counts', 0),
                    ('band0', 'Band 0', 0),
                    ('band1', 'Band 1', 0),
                    ('band2', 'Band 2', 0),
                    ('band3', 'Band 3', 0),
                    ('band4', 'Band 4', 0),
                    ('band5', 'Band 5', 0),
                    ('band6', 'Band 6', 0),
                    ('band7', 'Band 7', 0),
                ),
                'flags': (
                    ('sensing', 'Sensing', 0),
                    ('event', 'Event', 0),
                    ('product_ready', 'Product ready', 0),
                    ('saturated', 'Saturated', 0),
                    ('drift_step', 'Drift step', 0),
                    ('diag_mode', 'Diagnostic mode', 0),
                    ('frozen', 'Frozen', 0),
                    ('hv_trip', 'HV guard trip', 0),
                ),
            },
            'attitude': {
                'table': (
                    ('name', 'Name', 0),
                    ('Time', 'Sample time', 0),
                    ('frame', 'Reference frame', 0),
                    ('r_x', 'Position X, km', 0),
                    ('r_y', 'Position Y, km', 0),
                    ('r_z', 'Position Z, km', 0),
                    ('v_x', 'Velocity X, km/s', 0),
                    ('v_y', 'Velocity Y, km/s', 0),
                    ('v_z', 'Velocity Z, km/s', 0),
                    ('q_w', 'Quaternion W', 0),
                    ('q_x', 'Quaternion X', 0),
                    ('q_y', 'Quaternion Y', 0),
                    ('q_z', 'Quaternion Z', 0),
                    ('nadir_angle', 'Nadir angle, deg', 1),
                ),
                'flags': (
                    ('orbit', 'Orbit valid', 0),
                    ('mag', 'Magnetic sample valid', 0),
                    ('sun_valid', 'Sun vector valid', 0),
                    ('triad', 'TRIAD solution valid', 0),
                    ('eclipse', 'Earth shadow', 0),
                    ('bdot', 'B-dot active', 0),
                ),
            },
            'echo': {'table': (
                ('name', 'Name', 0),
                ('call_from', 'From', 0),
                ('call_to', 'To', 0),
                ('msg_seq', 'Message number', 0),
                ('text', 'Text', 0),
            )},
            'chat_stored': {'table': (
                ('name', 'Name', 0),
                ('seq', 'Sequence number', 0),
                ('page', 'Page number', 0),
                ('offset', 'Offset in page', 0),
                ('timestamp', 'Message time', 0),
                ('call_from', 'From', 0),
                ('call_to', 'To', 0),
                ('msg_seq', 'Message number', 0),
                ('text', 'Text', 0),
            )},
            'node_text': {'table': (
                ('name', 'Name', 0),
                ('node_id', 'Node ID', 0),
                ('timestamp', 'Message time', 0),
                ('text', 'Text', 0),
            )},
            'message_digital': {'table': (
                ('name', 'Name', 0),
                ('id', 'Message ID', 0),
                ('text', 'Text', 0),
            )},
        })

    def recognize(self, bb, t=None):
        while bb:
            data = usp.parse(bb)
            if not data.usp:
                return

            bb = data.usp._tail
            for i in data.usp.data:
                p_data = i.packet

                if i.message in filetransfer:
                    ty = 'img'
                    p_data = self.ir.push_data(i, t), self.ir.cur_img

                elif i.message in rs18s_tlm_map or i.message in tlm_map:
                    ty = 'tlm'
                    p_data = data, p_data

                else:
                    ty = 'raw'

                yield ty, self.get_sender_callsign(data), '0x%04X' % i.message, p_data

