#  Copyright (c) 2024. Alexander Baskikh
#
#  MIT License (MIT), http://opensource.org/licenses/MIT
#  Full license can be found in the LICENSE-MIT file
#
#  SPDX-License-Identifier: MIT

import construct

from SatsDecoder.systems import common

__all__ = 'DStarOneProtocol',

proto_name = 'd-start one'

"""
https://web.archive.org/web/20190807184852/http://www.d-star.one/downloads/D-Star%20ONE%20telemetry%20frame%20format.pdf
"""


def dstar_curr(v, m=1000):
    return common.LinearAdapter(1 / ((2.5 * m) / (4096 * 20 * v)), construct.Int16ub)


def dstar_voltage(a, b=18.2):
    return common.LinearAdapter(1 / ((2.5 / 4096) * ((a + b) / b)), construct.Int16ub)


dstar_one = construct.Struct(
    '_name' / construct.Computed('dstar_one'),
    'name' / construct.Computed('Telemetry'),

    'p_len' / construct.Const(0x6c, construct.Int8ul),  # packet length
    'p_id' / construct.Const(0xa3, construct.Hex(construct.Int8ul)),    # packet ID
    'Time' / common.UNIXTimestampAdapter(construct.Int32ul),    # system clock time, s
    'reboots' / construct.Int32ul,      # reboots counter
    'rtc_val' / common.UNIXTimestampAdapter(construct.Int32ul),     # RTC value
    'adc0_0' / dstar_curr(0.05),      # Bat charge in, mA
    'adc0_1' / dstar_curr(0.033),     # Bat charge out, mA
    'adc0_2' / dstar_voltage(124, 27.4),    # Bat voltage, V
    'adc0_3' / dstar_voltage(30.1),     # 5V supply, V
    'adc0_4' / dstar_voltage(18.2),     # 3V3 supply, V
    'adc0_5' / dstar_curr(1),           # PCU total curr, mA
    'adc0_6' / dstar_curr(0.1),         # Solar +X curr, mA
    'adc0_7' / dstar_curr(0.1),         # Solar -X curr, mA
    'adc0_8' / dstar_curr(0.1),         # Solar +Y curr, mA
    'adc0_9' / dstar_curr(0.1),         # Solar -Y curr, mA
    'adc0_10' / dstar_curr(0.1),        # Solar +Z curr, mA
    'adc0_11' / dstar_curr(0.1),        # Solar -Z curr, mA
    'adc0_12' / dstar_voltage(30.1),    # Solar total voltage, V
    'adc0_13' / dstar_curr(0.1),        # VCC out0 curr, mA
    'adc0_14' / dstar_curr(0.1),        # VCC out1 curr, mA
    'adc0_15' / dstar_curr(0.1),        # VCC out2 curr, mA
    'adc1_0' / dstar_curr(0.1),         # VCC out3 curr, mA
    'adc1_1' / dstar_curr(0.05),        # VCC out4 curr, mA
    'adc1_2' / dstar_curr(0.05),        # VCC out5 curr, mA
    'adc1_3' / dstar_curr(0.05),        # VCC out6 curr, mA
    'adc1_4' / dstar_curr(0.05),        # VCC out7 curr, mA
    'adc1_5' / dstar_curr(0.1),         # SS total curr, mA
    'adc1_6' / dstar_curr(0.2),         # EEPROM1 curr, mA
    'adc1_7' / dstar_curr(1),           # EEPROM2 curr, mA
    'adc1_8' / dstar_curr(1),           # Ext ADC1 curr, mA
    'adc1_9' / dstar_curr(1),           # Ext ADC2 curr, mA
    'adc1_10' / dstar_curr(1),          # Ext ADC3 curr, mA
    'adc1_11' / dstar_curr(1),          # Ext ADC4 curr, mA
    'adc1_12' / dstar_curr(1),          # RTC curr, mA
    'adc1_13' / dstar_curr(0.1, 1),     # Charger DCDC voltage, V
    'adc1_14' / dstar_curr(0.1, 1),     # System V, V
    'adc1_15' / dstar_curr(0.1),        # OBC curr, mA
    'switches' / construct.Bytes(3),    # mask of system power switches
    'rsrv0' / construct.Bytes(1),
    'batt_temp' / construct.Int16sl,    # Temperature sensor of battery pack
    'schedule' / construct.Int8ul,      # Count of scheduled commands
    'rsrv1' / construct.Bytes(10),
    'mode' / construct.Hex(construct.Enum(construct.Int8ul, Safe=1, Nominal=2, Experimental=3)),    # current satellite mode
    'filler' / construct.Bytes(10),
    'crc' / construct.Hex(construct.Int16ub),
)

# TODO: separate MOBITEX
mobitex = construct.Struct(
    'hdr' / construct.Bytes(10),
    'data' / dstar_one,
    'tail' / construct.GreedyBytes,
)


class DStarOneProtocol(common.Protocol):

    tlm_table = {
        'dstar_one': {
            'table': (
                ('name', 'Name'),
                ('p_len', 'Packet length'),
                ('p_id', 'Packet ID'),
                ('Time', 'System clock time, s'),
                ('reboots', 'Reboots counter'),
                ('rtc_val', 'RTC value'),
                ('adc0_0', 'Bat charge in, mA'),
                ('adc0_1', 'Bat charge out, mA'),
                ('adc0_2', 'Bat voltage, V'),
                ('adc0_3', '5V supply, V'),
                ('adc0_4', '3V3 supply, V'),
                ('adc0_5', 'PCU total curr, mA'),
                ('adc0_6', 'Solar +X curr, mA'),
                ('adc0_7', 'Solar -X curr, mA'),
                ('adc0_8', 'Solar +Y curr, mA'),
                ('adc0_9', 'Solar -Y curr, mA'),
                ('adc0_10', 'Solar +Z curr, mA'),
                ('adc0_11', 'Solar -Z curr, mA'),
                ('adc0_12', 'Solar total voltage, V'),
                ('adc0_13', 'VCC out0 curr, mA'),
                ('adc0_14', 'VCC out1 curr, mA'),
                ('adc0_15', 'VCC out2 curr, mA'),
                ('adc1_0', 'VCC out3 curr, mA'),
                ('adc1_1', 'VCC out4 curr, mA'),
                ('adc1_2', 'VCC out5 curr, mA'),
                ('adc1_3', 'VCC out6 curr, mA'),
                ('adc1_4', 'VCC out7 curr, mA'),
                ('adc1_5', 'SS total curr, mA'),
                ('adc1_6', 'EEPROM1 curr, mA'),
                ('adc1_7', 'EEPROM2 curr, mA'),
                ('adc1_8', 'Ext ADC1 curr, mA'),
                ('adc1_9', 'Ext ADC2 curr, mA'),
                ('adc1_10', 'Ext ADC3 curr, mA'),
                ('adc1_11', 'Ext ADC4 curr, mA'),
                ('adc1_12', 'RTC curr, mA'),
                ('adc1_13', 'Charger DCDC voltage, V'),
                ('adc1_14', 'System V, V'),
                ('adc1_15', 'OBC curr, mA'),
                ('switches', 'Mask of system power switches'),
                ('rsrv0', 'Reserved'),
                ('batt_temp', 'Temperature sensor of battery pack'),
                ('schedule', 'Count of scheduled commands'),
                ('rsrv1', 'Reserved'),
                ('mode', 'Current satellite mode'),
                ('filler', 'Filler'),
                ('crc', 'CRC16'),
            ),
        },
    }

    def recognize(self, bb):
        x = mobitex.parse(bb)
        if not x:
            yield 'raw', 'unknown', bb
            return

        yield 'tlm', 'D-Star ONE', (x, x.data)
