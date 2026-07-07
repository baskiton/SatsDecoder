#  Copyright (c) 2025. Alexander Baskikh
#
#  MIT License (MIT), http://opensource.org/licenses/MIT
#  Full license can be found in the LICENSE-MIT file
#
#  SPDX-License-Identifier: MIT

import datetime as dt
import math

import construct

from SatsDecoder.systems import csp, common

__all__ = 'SnugliteProtocol',

proto_name = 'snuglite'

"""
https://snuglitecubesat.wixsite.com/website/post/snuglite-beacon-structure
"""


address = construct.Struct(
        'callsign' / construct.Const(b'DS0DH'),
        'ssid' / construct.Int16ul,
)

pseudo_ax25 = construct.Struct(
    'addresses' / construct.Array(2, address),
    'control' / construct.Hex(construct.Int8ub),
    'pid' / construct.Hex(construct.Int8ub),
)


class TimeAdapter(construct.Adapter):
    # def _encode(self, obj, context, path=None):
    #     return round(obj.timestamp())

    def _decode(self, obj, context, path=None):
        return dt.datetime.fromisoformat('20%i-%02i-%02i %02i:%02i:%02i' % tuple(obj))


start_id = construct.PaddedString(6, 'ascii')
end_id = construct.PaddedString(4, 'ascii')
sat_name = construct.Computed(lambda ctx: ctx.start_id[:-1] + ctx.end_id[1:])
pos_vel_flag = construct.Enum(construct.Int8ub, **{'TLE (ECI-frame)': 0, 'GPS (ECEF-frame)': 1, 'not used': 255})
pos_vel_arr = construct.Array(3, construct.Int32sb)
calculated_height = construct.Computed(lambda ctx: -1 if int(ctx.pos_vel_flag) == 255 else math.sqrt(ctx.pos_vel_pos[0]**2 + ctx.pos_vel_pos[1]**2 + ctx.pos_vel_pos[2]**2) / 100000 - 6371)
calculated_vel = construct.Computed(lambda ctx: -1 if int(ctx.pos_vel_flag) == 255 else math.sqrt(ctx.pos_vel_vel[0]**2 + ctx.pos_vel_vel[1]**2 + ctx.pos_vel_vel[2]**2) / 100)
battery_mode = construct.Enum(construct.Int8ub, **dict(initial=0, undervoltage=1, safemode=2, nominal=3, full=4))
voltage = construct.Int16ub
current = construct.Int16ub
psw_status = construct.Enum(construct.Flag, **dict(ON=True, OFF=False))
quaternion = construct.Array(4, construct.Float32b)
rpy = construct.Array(3, construct.Float32b)
temperature = construct.Int8sb
deploy_status = construct.Enum(construct.Flag, **{'released': True, 'not': False})

simple = construct.Struct(
    '_name' / construct.Computed('simple'),
    'name' / construct.Computed('Simple Beacon'),

    'start_id' / start_id,  # satellite name
    'firmware' / construct.Int8ub,  # firmware version
    'Time' / TimeAdapter(construct.Bytes(6)),   # UTC

    'pos_vel_flag' / pos_vel_flag,
    'pos_vel_pos' / pos_vel_arr,  # XYZ, cm
    'pos_vel_vel' / pos_vel_arr,  # XYZ, cm/s
    'calculated_height' / calculated_height,    # m
    'calculated_vel' / calculated_vel,  # m/s

    'battery_mode' / battery_mode,
    'battery_voltage' / voltage,    # mV

    'end_id' / end_id,  # satellite name
    'sat_name' / sat_name
)

full = construct.Struct(
    '_name' / construct.Computed('full'),
    'name' / construct.Computed('Full Beacon'),

    'start_id' / start_id,  # satellite name
    'firmware' / construct.Int8ub,  # firmware version
    'Time' / TimeAdapter(construct.Bytes(6)),   # UTC

    'pos_vel_flag' / pos_vel_flag,
    'pos_vel_pos' / pos_vel_arr,  # XYZ, cm
    'pos_vel_vel' / pos_vel_arr,  # XYZ, cm/s
    'calculated_height' / calculated_height,    # m
    'calculated_vel' / calculated_vel,  # m/s

    'battery_mode' / battery_mode,
    'battery_voltage' / voltage,    # mV
    'battery_current' / current,  # mA
    'power_sw_status' / construct.BitStruct(
        'not_used0' / psw_status,
        'not_used1' / psw_status,
        'gps_side' / psw_status,
        'magnetometer' / psw_status,
        'sd_card' / psw_status,
        'gps_up' / psw_status,
        'uhf' / psw_status,
        'boom' / psw_status,
    ),
    'ps_current' / construct.Struct(    # mA
        'boom' / current,
        'uhf' / current,
        'gps_up' / current,
        'sd_card' / current,
        'magnetometer' / current,
        'gps_side' / current,
    ),
    'solar_cell_inp_voltage' / construct.Struct(    # mV
        'x' / voltage,
        'y' / voltage,
        'z' / voltage,
    ),
    'solar_cell_inp_curr' / construct.Struct(    # mA
        'x' / current,
        'y' / current,
        'z' / current,
    ),

    'estimated_attitude' / quaternion,  # q0 q1 q2 q3
    'estimated_gyro_bias' / rpy,    # roll, pitch, yaw
    'estimated_angular_rate' / rpy,    # roll, pitch, yaw
    'measured_angular_rate' / rpy,    # roll, pitch, yaw (gyro)
    'att_status' / construct.BitStruct(
        'not_used0' / construct.Flag,
        'not_used1' / construct.Flag,
        'not_used2' / construct.Flag,
        'not_used3' / construct.Flag,
        'not_used4' / construct.Flag,
        'not_used5' / construct.Flag,
        'sun_ecl' / construct.Enum(construct.Flag, **{'sun': True, 'exlipse': False}),
        'attitude_convergence' / construct.Enum(construct.Flag, **{'conv': True, 'not': False}),
    ),
    'attitude_variance' / quaternion,   # q0 q1 q2 q3

    'curr_opmode' / construct.Enum(construct.Int8ub, **{'init': 0, 'standby': 1}),
    'elapsed_time' / construct.Int32sb, # min

    'sp_temp' / construct.Array(5, temperature),    # +X +Y -X -I -Z
    'onboard_computer_temp' / construct.Array(2, temperature),
    'eps_temp' / construct.Array(4, temperature),
    'uhf_temp' / construct.Array(2, temperature),

    'deploy_status' / construct.BitStruct(
        'not_used0' / deploy_status,
        'not_used1' / deploy_status,
        'not_used2' / deploy_status,
        'not_used3' / deploy_status,
        'not_used4' / deploy_status,
        'not_used5' / deploy_status,
        'boom' / deploy_status,
        'uhf_antenna' / deploy_status,
    ),
    'uhf_ant_trial_num' / construct.Int8ub,
    'boom_release_trial_num' / construct.Int8ub,

    'end_id' / end_id,  # satellite name
    'sat_name' / sat_name
)

tlm_map = {
    11: simple,
    15: full,
}

snuglite = construct.Struct(
    'ax25_hdr' / pseudo_ax25,
    'csp_hdr' / csp.csp_hdr,
    'data' / construct.Switch(construct.this.csp_hdr.dest_port, tlm_map, default=construct.GreedyBytes),
    '_csp_rs' / construct.Bytes(32),
)


class SnugliteProtocol(common.Protocol):
    tlm_table = {
        'simple': {
            'table': (
                ('name', 'Name', 0),
                ('sat_name', 'Satellite name', 0),
                ('firmware', 'Firmware version', 0),
                ('Time', 'Time', 0),
                ('pos_vel_flag', 'Positioning flag', 0),
                ('pos_vel_pos', 'Position, cm', 0),
                ('pos_vel_vel', 'Velocity, cm/s', 0),
                ('calculated_height', 'Calculated height, km', 0),
                ('calculated_vel', 'Calculated velocity, m/s', 0),
                ('battery_mode', 'Battery mode', 0),
                ('battery_voltage', 'Battery voltage, mV', 0),
            ),
        },
        'full': {
            'table': (
                ('name', 'Name', 0),
                ('sat_name', 'Satellite name', 0),
                ('firmware', 'Firmware version', 0),
                ('Time', 'Time', 0),

                ('pos_vel_flag', 'Positioning flag', 0),
                ('pos_vel_pos', 'Position, cm', 0),
                ('pos_vel_vel', 'Velocity, cm/s', 0),
                ('calculated_height', 'Calculated height, km', 0),
                ('calculated_vel', 'Calculated velocity, m/s', 0),

                ('battery_mode', 'Battery mode', 0),
                ('battery_voltage', 'Battery voltage, mV', 0),
                ('battery_current', 'Battery current, mA', 0),
                ('power_sw_status/boom', 'PS Switch boom', 0),
                ('power_sw_status/uhf', 'PS Switch UHF', 0),
                ('power_sw_status/gps_up', 'PS Switch GPS-up', 0),
                ('power_sw_status/sd_card', 'PS Switch SD-card', 0),
                ('power_sw_status/magnetometer', 'PS Switch magnetometer', 0),
                ('power_sw_status/gps_side', 'PS Switch GPS-side', 0),
                ('ps_current/boom', 'PS boom current, mA', 0),
                ('ps_current/uhf', 'PS UHF current, mA', 0),
                ('ps_current/gps_up', 'PS GPS-up current, mA', 0),
                ('ps_current/sd_card', 'PS SD-card current, mA', 0),
                ('ps_current/magnetometer', 'PS magnetometer current, mA', 0),
                ('ps_current/gps_side', 'PS GPS-side current, mA', 0),
                ('solar_cell_inp_voltage/x', '±X solar cell Voltage, mV', 0),
                ('solar_cell_inp_voltage/y', '±Y solar cell Voltage, mV', 0),
                ('solar_cell_inp_voltage/z', '-Z solar cell Voltage, mV', 0),
                ('solar_cell_inp_curr/x', '±X solar cell current, mA', 0),
                ('solar_cell_inp_curr/y', '±Y solar cell current, mA', 0),
                ('solar_cell_inp_curr/z', '-Z solar cell current, mA', 0),

                ('estimated_attitude', 'Estimated attitude, quaternion', 0),
                ('estimated_gyro_bias', 'Estimated gyro bias (row, pitch, yaw)', 0),
                ('estimated_angular_rate', 'Estimated angular rate (row, pitch, yaw)', 0),
                ('measured_angular_rate', 'Measured angular rate (gyro) (row, pitch, yaw)', 0),
                ('att_status/sun_ecl', 'Sun/Eclipse', 0),
                ('att_status/attitude_convergence', 'Attitude convergence', 0),
                ('attitude_variance', 'Attitude variance, quaternion', 0),

                ('curr_opmode', 'Current operation mode', 0),
                ('elapsed_time', 'elapsed time, min', 0),

                ('sp_temp', 'Solar panel temperature, °C', 0),
                ('onboard_computer_temp', 'Onboard computer temperature, °C', 0),
                ('eps_temp', 'EPS module temperature, °C', 0),
                ('uhf_temp', 'UHF module temperature, °C', 0),

                ('deploy_status/boom', 'Boom release status', 0),
                ('deploy_status/uhf_antenna', 'UHF ant release status', 0),
                ('uhf_ant_trial_num', 'UHF ant release trial number', 0),
                ('boom_release_trial_num', 'Boom release trial number', 0),
            ),
        },
    }

    @staticmethod
    def get_sender_callsign(packet):
        x = packet.ax25_hdr.addresses[1]
        return '%s-%s' % (x.callsign.decode(), x.ssid)

    def recognize(self, bb, t=None):
        x = snuglite.parse(bb)
        name = self.get_sender_callsign(x) or 'unknown'

        if x.data and hasattr(x.data, '_name'):
            yield 'tlm', name, (x, x.data)
        else:
            yield 'raw', name, x.data or bb
