import datetime as dt

import construct

from SatsDecoder.systems import common
from SatsDecoder.systems.image_receiver import ImageReceiver

__all__ = 'UspProtocol',


class TimeDeltaAdapter(construct.Adapter):
    def _encode(self, obj, context, path=None):
        return round(obj.total_seconds())

    def _decode(self, obj, context, path=None):
        return dt.timedelta(seconds=obj)


Addr = construct.Hex(construct.Int16ul)
RegTemp = common.LinearAdapter(100, construct.Int16sl)
Voltage = common.LinearAdapter(1000, construct.Int16ul)
VoltageS = common.LinearAdapter(1000, construct.Int16sl)


# tlm
REGULAR_COMMON = 0x000E
REGULAR_X = 0x000F
REGULAR_Y = 0x0010
REGULAR_Z = 0x0011
PSU_REGULAR0 = 0x0080
PSU_REGULAR1 = 0x0081
PSU_REGULAR2 = 0x0082
PSU_REGULAR3 = 0x0083
PSU_REGULAR4 = 0x0084
INFO = 0x011A
REGULAR_TEMPERATURE = 0x0440
GET_PAYLOAD_TELEMETRY = 0x0A00
ARS_X_VEL = 0x0B10
ARS_Y_VEL = 0x0B11
ARS_Z_VEL = 0x0B12
MAG_X = 0x0B13
MAG_Y = 0x0B14
MAG_Z = 0x0B15
VECTOR_X = 0x0B21
VECTOR_Y = 0x0B22
VECTOR_Z = 0x0B23
BRIGHTNESS = 0x0B24
COMMON_TELEMETRY = 0x0BF3
VHF_SETTINGS = 0x4201
BEACON = 0x4216
EXTENDED_BEACON = 0x4217
TIME_REQUEST = 0x421A
DETECTOR_TRANSMITS = 0x5430
DATA_MASSIVE_ADDR_RPL = 0x5439
DATA_EVENT_ADDR_RPL = 0x543A
DATA_MONITOR_ADDR_RPL = 0x543B
DATA_MASSIVE_RPL = 0x543C
DATA_EVENT_RPL = 0x543D
DATA_MONITOR_RPL = 0x543E
GET_PAYLOAD_FW_MSG = 0xABD1
NO_MONITOR_DATA = 0xABD4
NO_EVENT_DATA = 0xABD5
NO_MASSIVE_DATA = 0xABD6
COMPL_MONITOR_DATA = 0xABD9
COMPL_EVENT_DATA = 0xABDA
COMPL_MASSIVE_DATA = 0xABDB
GET_PAYLOAD_CURRENT_CONFIG = 0xABDD
REGULAR_TELEMETRY = 0xDE21
EXTENDED_TELEMETRY = 0xDE22
OVERCURRENT = 0xDE25
SWITCH_STATUS = 0xDE27
CH_ADC_X1 = 0xFB21
CH_ADC_X2 = 0xFB22
CH_ADC_Y1 = 0xFB23
CH_ADC_Y2 = 0xFB24
TEMP_CUR_X1 = 0xFC21
TEMP_CUR_X2 = 0xFC22
TEMP_CUR_Y1 = 0xFC23
TEMP_CUR_Y2 = 0xFC24
VERSION_SW = 0xFFE1

# other
IMG_START = 0x0C20
IMG_SIZE = 0x0C2B
IMG_DATA = 0x0C24


# tlmasd
regular_common_flags0 = construct.BitStruct(
    '_pad0' / construct.BitsInteger(6),
    'voltage_invalid' / construct.Flag,  # voltage invalid
    'current_invalid' / construct.Flag,  # current invalid
)
regular_common = construct.Struct(
    '_name' / construct.Computed('regular_common'),
    'name' / construct.Computed('Regular common'),
    'desc' / construct.Computed('Common current and voltage telemetry'),
    'current' / construct.Int16sl,  # current
    'voltage' / construct.Int16sl,  # voltage
    'flags0' / regular_common_flags0,
)

regular_x_flags0 = construct.BitStruct(
    '_pad0' / construct.BitsInteger(6),
    'voltage_invalid' / construct.Flag,  # voltage invalid
    'current_invalid' / construct.Flag,  # current invalid
)
regular_x = construct.Struct(
    '_name' / construct.Computed('regular_x'),
    'name' / construct.Computed('Regular X'),
    'desc' / construct.Computed('Current and voltage telemetry, X'),
    'current' / construct.Int16sl,  # current
    'voltage' / construct.Int16sl,  # voltage
    'flags0' / regular_x_flags0,
)

regular_y_flags0 = construct.BitStruct(
    '_pad0' / construct.BitsInteger(6),
    'voltage_invalid' / construct.Flag,  # voltage invalid
    'current_invalid' / construct.Flag,  # current invalid
)
regular_y = construct.Struct(
    '_name' / construct.Computed('regular_y'),
    'name' / construct.Computed('Regular Y'),
    'desc' / construct.Computed('Current and voltage telemetry, Y'),
    'current' / construct.Int16sl,  # current
    'voltage' / construct.Int16sl,  # voltage
    'flags0' / regular_y_flags0,
)

regular_z_flags0 = construct.BitStruct(
    '_pad0' / construct.BitsInteger(6),
    'voltage_invalid' / construct.Flag,  # voltage invalid
    'current_invalid' / construct.Flag,  # current invalid
)
regular_z = construct.Struct(
    '_name' / construct.Computed('regular_z'),
    'name' / construct.Computed('Regular Z'),
    'desc' / construct.Computed('Current and voltage telemetry, Z'),
    'current' / construct.Int16sl,  # current
    'voltage' / construct.Int16sl,  # voltage
    'flags0' / regular_z_flags0,
)

psu_regular0_flags0 = construct.BitStruct(
    '_pad0' / construct.BitsInteger(6),
    'voltage_invalid' / construct.Flag,  # voltage invalid
    'current_invalid' / construct.Flag,  # current invalid
)
psu_regular0 = construct.Struct(
    '_name' / construct.Computed('psu_regular0'),
    'name' / construct.Computed('PSU Regular #0'),
    'desc' / construct.Computed('PSU Regular #0'),
    'current' / construct.Int16sl,  # current
    'voltage' / construct.Int16sl,  # voltage
    'flags0' / psu_regular0_flags0,
)

psu_regular1_flags0 = construct.BitStruct(
    '_pad0' / construct.BitsInteger(6),
    'voltage_invalid' / construct.Flag,  # voltage invalid
    'current_invalid' / construct.Flag,  # current invalid
)
psu_regular1 = construct.Struct(
    '_name' / construct.Computed('psu_regular1'),
    'name' / construct.Computed('PSU Regular #1'),
    'desc' / construct.Computed('PSU Regular #1'),
    'current' / construct.Int16sl,  # current
    'voltage' / construct.Int16sl,  # voltage
    'flags0' / psu_regular1_flags0,
)

psu_regular2_flags0 = construct.BitStruct(
    '_pad0' / construct.BitsInteger(6),
    'voltage_invalid' / construct.Flag,  # voltage invalid
    'current_invalid' / construct.Flag,  # current invalid
)
psu_regular2 = construct.Struct(
    '_name' / construct.Computed('psu_regular2'),
    'name' / construct.Computed('PSU Regular #2'),
    'desc' / construct.Computed('PSU Regular #2'),
    'current' / construct.Int16sl,  # current
    'voltage' / construct.Int16sl,  # voltage
    'flags0' / psu_regular2_flags0,
)

psu_regular3_flags0 = construct.BitStruct(
    '_pad0' / construct.BitsInteger(6),
    'voltage_invalid' / construct.Flag,  # voltage invalid
    'current_invalid' / construct.Flag,  # current invalid
)
psu_regular3 = construct.Struct(
    '_name' / construct.Computed('psu_regular3'),
    'name' / construct.Computed('PSU Regular #3'),
    'desc' / construct.Computed('PSU Regular #3'),
    'current' / construct.Int16sl,  # current
    'voltage' / construct.Int16sl,  # voltage
    'flags0' / psu_regular3_flags0,
)

psu_regular4_flags0 = construct.BitStruct(
    '_pad0' / construct.BitsInteger(6),
    'voltage_invalid' / construct.Flag,  # voltage invalid
    'current_invalid' / construct.Flag,  # current invalid
)
psu_regular4 = construct.Struct(
    '_name' / construct.Computed('psu_regular4'),
    'name' / construct.Computed('PSU Regular #4'),
    'desc' / construct.Computed('PSU Regular #4'),
    'current' / construct.Int16sl,  # current
    'voltage' / construct.Int16sl,  # voltage
    'flags0' / psu_regular4_flags0,
)

Info = construct.Struct(
    '_name' / construct.Computed('Info'),
    'name' / construct.Computed('Info'),
    'desc' / construct.Computed('Device information'),
    'SW_VER' / construct.Int16ul,  # Версия встроенного ПО
    'SERIAL' / construct.Int16ul,  # Серийный номер платы
    'CANTEL' / construct.Hex(construct.Enum(construct.Int8ul, **{'OFF': 0, 'SUN': 1, 'ADC': 2, 'ADC-compressed': 3})),  # Режим телеметрии CAN Режим телеметрии (0 - откл., 1 - вектор на солнце, 2 - данные АЦП, 3 - компенсированные данные АЦП)
    'UARTTEL' / construct.Hex(construct.Int8ul),  # Режим телеметрии UART
    'ADC_REF' / construct.Int16ul,  # Опорное значение АЦП, мВ
    'THRESHOLD' / construct.Int16ul,  # Порог яркости
    'SET_STAT' / construct.Hex(construct.Enum(construct.Int32ul, MEM=0, DEFAULT=0x8000200)),  # Результат загрузки параметров (0 - из памяти, 0x8000200 - по умолчанию)
    'LM70_STAT' / construct.Hex(construct.Int32ul),  # Результат загрузки полинома температуры
    'VECT_STAT' / construct.Hex(construct.Int32ul),  # Результат загрузки полинома вектора
)

regular_temperature_flags0 = construct.BitStruct(
    '_pad0' / construct.BitsInteger(6),
    'temperature1_invalid' / construct.Flag,  # temperature1_invalid
    'temperature0_invalid' / construct.Flag,  # temperature0_invalid
)
regular_temperature = construct.Struct(
    '_name' / construct.Computed('regular_temperature'),
    'name' / construct.Computed('Regular Temperature'),
    'desc' / construct.Computed('Temperature telemetry'),
    'temperature0' / construct.Int8sl,  # temperature0
    'temperature1' / construct.Int8sl,  # temperature1
    'flags0' / regular_temperature_flags0,
)

get_Payload_telemetry = construct.Struct(
    '_name' / construct.Computed('get_Payload_telemetry'),
    'name' / construct.Computed('Payload telemetry'),
    'desc' / construct.Computed('Payload telemetry'),
    'FL' / construct.Hex(construct.Int8ul),  # Флаги ПН
    'Time' / common.UNIXTimestampAdapter(construct.Int32sl),  # Время последней телеметрии ПН
    'T_Plate' / construct.Int16sl,  # Температура платы ПН
    'T_CPU' / construct.Int16sl,  # Температура микроконтроллера ПН
    'CurSens1' / construct.Int16ul,  # Датчик тока 1.
    'CurSens2' / construct.Int16ul,  # Датчик тока 2.
    'NRst' / construct.Int8ul,  # Количество перезагрузок
    'TimeRst' / common.UNIXTimestampAdapter(construct.Int32sl),  # Время последней перезагрузки
    'CH1Rate' / construct.Int16ul,  # Скорость счёта в 1м канале
    'CH2Rate' / construct.Int16ul,  # Скорость счёта в 2м канале
    'CH3Rate' / construct.Int16ul,  # Скорость счёта в 3м канале
    'CH4Rate' / construct.Int16ul,  # Скорость счёта в 4м канале
    'CH5Rate' / construct.Int16ul,  # Скорость счёта в 5м канале
    'CH6Rate' / construct.Int16ul,  # Скорость счёта в 6м канале
    '_pad0' / construct.BitsInteger(16),
    'PtrEnd1' / construct.Hex(construct.Int16ul),  # Указатель последнего переданного блока из сегмента 1.
    'PtrCrt1' / construct.Hex(construct.Int16ul),  # Указатель записываемого блока из сегмента 1.
    'PtrEnd2' / construct.Hex(construct.Int16ul),  # Указатель последнего переданного блока из сегмента 2.
    'PtrCrt2' / construct.Hex(construct.Int16ul),  # Указатель записываемого блока из сегмента 2.
    'PtrEnd3' / construct.Hex(construct.Int16ul),  # Указатель последнего переданного блока из сегмента 3.
    'PtrCrt3' / construct.Hex(construct.Int16ul),  # Указатель записываемого блока из сегмента 3.
    'LastEvent_CH1_1' / construct.Hex(construct.Int8ul),  # Последние событие канал 1 M1L1.
    'LastEvent_CH1_2' / construct.Hex(construct.Int8ul),  # Последние событие канал 1 L2H1.
    'LastEvent_CH1_3' / construct.Hex(construct.Int8ul),  # Последние событие канал 1 H2M2.
    'LastEvent_CH2_1' / construct.Hex(construct.Int8ul),  # Последние событие канал 2 M1L1.
    'LastEvent_CH2_2' / construct.Hex(construct.Int8ul),  # Последние событие канал 2 L2H1.
    'LastEvent_CH2_3' / construct.Hex(construct.Int8ul),  # Последние событие канал 2 H2M2.
)

ars_X_vel_flags0 = construct.BitStruct(
    'Valid_X' / construct.Flag,  # Данные не актуальны
    '_Reserv' / construct.BitsInteger(7),  # Резерв
)
ars_X_vel = construct.Struct(
    '_name' / construct.Computed('ars_X_vel'),
    'name' / construct.Computed('ARS X velolicy'),
    'desc' / construct.Computed('Angular Rate Sensor regular telemetry for angular velocity by X (tested)'),
    'Velocity_X' / construct.Float32l,  # Скорость, град/с
    'Temp_X' / construct.Int8sl,  # Температура, градусы Цельсия
    'flags0' / ars_X_vel_flags0,
)

ars_Y_vel_flags0 = construct.BitStruct(
    'Valid_Y' / construct.Flag,  # Данные не актуальны
    '_Reserv' / construct.BitsInteger(7),  # Резерв
)
ars_Y_vel = construct.Struct(
    '_name' / construct.Computed('ars_Y_vel'),
    'name' / construct.Computed('ARS Y velolicy'),
    'desc' / construct.Computed('Angular Rate Sensor regular telemetry for angular velocity by Y (tested)'),
    'Velocity_Y' / construct.Float32l,  # Скорость, град/с
    'Temp_Y' / construct.Int8sl,  # Температура, градусы Цельсия
    'flags0' / ars_Y_vel_flags0,
)

ars_Z_vel_flags0 = construct.BitStruct(
    'Valid_Z' / construct.Flag,  # Данные не актуальны
    '_Reserv' / construct.BitsInteger(7),  # Резерв
)
ars_Z_vel = construct.Struct(
    '_name' / construct.Computed('ars_Z_vel'),
    'name' / construct.Computed('ARS Z velolicy'),
    'desc' / construct.Computed('Angular Rate Sensor regular telemetry for angular velocity by Z (tested)'),
    'Velocity_Z' / construct.Float32l,  # Скорость, град/с
    'Temp_Z' / construct.Int8sl,  # Температура, градусы Цельсия
    'flags0' / ars_Z_vel_flags0,
)

mag_X_flags0 = construct.BitStruct(
    'Valid_X' / construct.Flag,  # Данные не актуальны
    '_Reserv' / construct.BitsInteger(7),  # Резерв
)
mag_X = construct.Struct(
    '_name' / construct.Computed('mag_X'),
    'name' / construct.Computed('Magnetometer - X-field'),
    'desc' / construct.Computed('Magnetometer regular telemetry along X-field (tested)'),
    'Field_X' / construct.Float32l,  # Магнитное поле, нТл
    'Temp_X' / construct.Int8ul,  # Температура, градусы Цельсия
    'flags0' / mag_X_flags0,
)

mag_Y_flags0 = construct.BitStruct(
    'Valid_Y' / construct.Flag,  # Данные не актуальны
    '_Reserv' / construct.BitsInteger(7),  # Резерв
)
mag_Y = construct.Struct(
    '_name' / construct.Computed('mag_Y'),
    'name' / construct.Computed('Magnetometer - Y-field'),
    'desc' / construct.Computed('Magnetometer regular telemetry along Y-field (tested)'),
    'Field_Y' / construct.Float32l,  # Магнитное поле, нТл
    'Temp_Y' / construct.Int8sl,  # Температура, градусы Цельсия
    'flags0' / mag_Y_flags0,
)

mag_Z_flags0 = construct.BitStruct(
    'Valid_Z' / construct.Flag,  # Данные не актуальны
    '_Reserv' / construct.BitsInteger(7),  # Резерв
)
mag_Z = construct.Struct(
    '_name' / construct.Computed('mag_Z'),
    'name' / construct.Computed('Magnetometer - Z-field'),
    'desc' / construct.Computed('Magnetometer regular telemetry along Z-field (tested)'),
    'Field_Z' / construct.Float32l,  # Магнитное поле, нТл
    'Temp_Z' / construct.Int8sl,  # Температура, градусы Цельсия
    'flags0' / mag_Z_flags0,
)

Vector_X_flags0 = construct.BitStruct(
    'Invalid_X' / construct.Flag,  # Данные актуальны
    '_Reserv' / construct.BitsInteger(7),  # _Reserv
)
Vector_X = construct.Struct(
    '_name' / construct.Computed('Vector_X'),
    'name' / construct.Computed('Vector X'),
    'desc' / construct.Computed('X-axis regular telemetry'),
    'Vect_X' / construct.Int32sl,  # Направление по X, град
    'Temp_X' / construct.Int8sl,  # Температура, градусы Цельсия
    'flags0' / Vector_X_flags0,
)

Vector_Y_flags0 = construct.BitStruct(
    'Invalid_Y' / construct.Flag,  # Данные актуальны
    '_Reserv' / construct.BitsInteger(7),  # _Reserv
)
Vector_Y = construct.Struct(
    '_name' / construct.Computed('Vector_Y'),
    'name' / construct.Computed('Vector Y'),
    'desc' / construct.Computed('Y-axis regular telemetry'),
    'Vect_Y' / construct.Int32sl,  # Направление по Y, град
    'Temp_Y' / construct.Int8sl,  # Температура, градусы Цельсия
    'flags0' / Vector_Y_flags0,
)

Vector_Z_flags0 = construct.BitStruct(
    '_Reserved' / construct.BitsInteger(8),  # Резерв
    'Invalid_Z' / construct.Flag,  # Данные актуальны
    '_Reserv' / construct.BitsInteger(7),  # _Reserv
)
Vector_Z = construct.Struct(
    '_name' / construct.Computed('Vector_Z'),
    'name' / construct.Computed('Vector Z'),
    'desc' / construct.Computed('Z-axis regular telemetry'),
    'Vect_Z' / construct.Int32sl,  # Направление по Z, град
    'flags0' / Vector_Z_flags0,
)

Brightness = construct.Struct(
    '_name' / construct.Computed('Brightness'),
    'name' / construct.Computed('Brightness'),
    'desc' / construct.Computed('Total brightness regular telemetry'),
    'Sum' / construct.Float32l,  # Суммарная яркость каналов
    '_Reserved' / construct.BitsInteger(16),  # Резерв
)

common_telemetry = construct.Struct(
    '_name' / construct.Computed('common_telemetry'),
    'name' / construct.Computed('Common telemetry'),
    'desc' / construct.Computed('Common one-time telemetry (issued on request) (tested)'),
    'Data' / construct.Bytes(48),  # Data
)

vhf_settings = construct.Struct(
    '_name' / construct.Computed('vhf_settings'),
    'name' / construct.Computed('VHF Settings'),
    'desc' / construct.Computed('VHF Settings'),
    'Magic' / construct.Hex(construct.Int32ul),  # Magic
    'Frequency' / construct.Int32ul,  # Frequency
    'BitRate' / construct.Int32ul,  # BitRate
    'DAC1Setting' / construct.Int16sl,  # DAC1Setting
    'DAC2Setting' / construct.Int16sl,  # DAC2Setting
    'TPacketMode' / construct.Int8ul,  # TPacketMode
    'EnableBeacon' / construct.Int8ul,  # EnableBeacon
    'BeaconInterval' / construct.Int16ul,  # BeaconInterval
    'CallSign' / construct.PaddedString(56, 'utf8'),  # CallSign
    'SSID' / construct.Int8ul,  # SSID
    'EarthCallSign' / construct.PaddedString(56, 'utf8'),  # EarthCallSign
    'EarthSSID' / construct.Int8ul,  # EarthSSID
    'TLocation' / construct.Int8ul,  # TLocation
    'UNIcanID' / construct.Int16ul,  # UNIcanID
    'EnableBridge' / construct.Int8ul,  # EnableBridge
    'BeaconStartupDelay' / construct.Int16ul,  # BeaconStartupDelay
)

beacon_flags0 = construct.BitStruct(
    'Uab_crit' / construct.Flag,  # Флаг "Батарея разряжена до критического уровня".
    'Uab_min' / construct.Flag,  # Флаг "Батарея разряжена до минимального уровня".
    'heater2_manual' / construct.Flag,  # Флаг ручного управления нагревателем 2.
    'heater1_manual' / construct.Flag,  # Флаг ручного управления нагревателем 1.
    'heater2_on' / construct.Flag,  # Флаг включения нагревателя 2.
    'heater1_on' / construct.Flag,  # Флаг включения нагревателя 1.
    'Tab_max' / construct.Flag,  # Флаг превышения максимальной температуры
    'Tab_min' / construct.Flag,  # Флаг "Низкая температура батареи".
    'channelon4' / construct.Flag,  # Флаг состояния канала 4.
    'channelon3' / construct.Flag,  # Флаг состояния канала 3.
    'channelon2' / construct.Flag,  # Флаг состояния канала 2.
    'channelon1' / construct.Flag,  # Флаг состояния канала 1.
    'Ich_limit4' / construct.Flag,  # Флаг превышения тока по каналу 4.
    'Ich_limit3' / construct.Flag,  # Флаг превышения тока по каналу 3.
    'Ich_limit2' / construct.Flag,  # Флаг превышения тока по каналу 2.
    'Ich_limit1' / construct.Flag,  # Флаг превышения тока по каналу 1.
    '_reserved0' / construct.BitsInteger(7),  # Резерв
    'charger' / construct.Flag,  # Флаг наличия напряжения на разъёме для зарядки
    '_reserved1' / construct.BitsInteger(8),  # Резерв
)
beacon = construct.Struct(
    '_name' / construct.Computed('beacon'),
    'name' / construct.Computed('Beacon'),
    'desc' / construct.Computed('Beacon with integrated telemetry'),
    'Usb1' / construct.Int16ul,  # Напряжение СБ 1 (мВ)
    'Usb2' / construct.Int16ul,  # Напряжение СБ 2 (мВ)
    'Usb3' / construct.Int16ul,  # Напряжение СБ 3 (мВ)
    'Isb1' / construct.Int16ul,  # Ток СБ1 (мА)
    'Isb2' / construct.Int16ul,  # Ток СБ2 (мА)
    'Isb3' / construct.Int16ul,  # Ток СБ3 (мА)
    'Iab' / construct.Int16sl,  # Ток АКБ (мА)
    'Ich1' / construct.Int16ul,  # Ток канала 1 (мА)
    'Ich2' / construct.Int16ul,  # Ток канала 2 (мА)
    'Ich3' / construct.Int16ul,  # Ток канала 3 (мА)
    'Ich4' / construct.Int16ul,  # Ток канала 4 (мА)
    't1_pw' / construct.Int16sl,  # Температура АКБ 1 (гр. С)
    't2_pw' / construct.Int16sl,  # Температура АКБ 2 (гр. С)
    't3_pw' / construct.Int16sl,  # Температура АКБ 3 (гр. С)
    't4_pw' / construct.Int16sl,  # Температура АКБ 4 (гр. С)
    'flags0' / beacon_flags0,
    'Uab' / construct.Int16sl,  # Напряжение АКБ (мВ)
    'reg_tel_id' / construct.Int32ul,  # Порядковый номер телеметрии PS.
    'Time' / common.UNIXTimestampAdapter(construct.Int32sl),  # Время последней телеметрии PS.
    'Nres' / construct.Int8ul,  # Количество перезагрузок PS.
    'FL' / construct.Int8ul,  # Флаги PS.
    't_amp' / construct.Int8sl,  # Температура усилителя УКВ (гр. С)
    't_uhf' / construct.Int8sl,  # Температура УКВ (гр. С)
    'RSSIrx' / construct.Int8sl,  # RSSI при приеме
    'RSSIidle' / construct.Int8sl,  # RSSI в ожидании
    'Pf' / construct.Int8sl,  # Мощность прямого излучения
    'Pb' / construct.Int8sl,  # Мощность обратного излучения
    'Nres_uhf' / construct.Int8ul,  # Количество перезагрузок УКВ
    'FL_uhf' / construct.Int8ul,  # Флаги УКВ
    'Time_uhf' / common.UNIXTimestampAdapter(construct.Int32sl),  # Время последней телеметрии УКВ
    'UpTime' / TimeDeltaAdapter(construct.Int32ul),  # Uptime в секундах
    'Current' / construct.Int16ul,  # Ток потребления УКВ
    'Uuhf' / construct.Int16sl,  # Напряжение УКВ (мВ)
)

extended_beacon = construct.Struct(
    '_name' / construct.Computed('extended_beacon'),
    'name' / construct.Computed('Extended Beacon'),
    'desc' / construct.Computed('Beacon with extended integrated telemetry'),
    't_mb' / construct.Int16sl,  # Температура материнской платы (гр. С)
    'Mx' / construct.Float32l,  # Вектор магнитного поля по оси X.
    'My' / construct.Float32l,  # Вектор магнитного поля по оси Y.
    'Mz' / construct.Float32l,  # Вектор магнитного поля по оси Z.
    'Vx' / construct.Float32l,  # Скорость по оси X.
    'Vy' / construct.Float32l,  # Скорость по оси Y.
    'Vz' / construct.Float32l,  # Скорость по оси Z.
    'Nres' / construct.Int8ul,  # Количество перезагрузок
    'Rcon' / construct.Hex(construct.Int8ul),  # Причина последней перезагрузки
    'FL' / construct.Hex(construct.Int8ul),  # ФЛАГИ
    'Time' / common.UNIXTimestampAdapter(construct.Int32sl),  # Время последней телеметрии
    'FL_PL' / construct.Hex(construct.Int8ul),  # Флаги ПН
    'TimeSend' / common.UNIXTimestampAdapter(construct.Int32sl),  # Время последней телеметрии ПН
    'T_Plate' / construct.Int16sl,  # Температура платы ПН
    'T_CPU' / construct.Int16sl,  # Температура микроконтроллера ПН
    'CurSens1' / construct.Int16ul,  # Датчик тока 1.
    'CurSens2' / construct.Int16ul,  # Датчик тока 2.
    'NRst' / construct.Int8ul,  # Количество перезагрузок
    'TimeRst' / common.UNIXTimestampAdapter(construct.Int32sl),  # Время последней перезагрузки
    'CH1Rate' / construct.Int16ul,  # Скорость счёта в 1м канале
    'CH2Rate' / construct.Int16ul,  # Скорость счёта в 2м канале
    'CH3Rate' / construct.Int16ul,  # Скорость счёта в 3м канале
    'CH4Rate' / construct.Int16ul,  # Скорость счёта в 4м канале
    'CH5Rate' / construct.Int16ul,  # Скорость счёта в 5м канале
    'CH6Rate' / construct.Int16ul,  # Скорость счёта в 6м канале
    'PtrEnd1' / construct.Hex(construct.Int16ul),  # Указатель последнего переданного блока из сегмента 1.
    'PtrCrt1' / construct.Hex(construct.Int16ul),  # Указатель записываемого блока из сегмента 1.
    'PtrEnd2' / construct.Hex(construct.Int16ul),  # Указатель последнего переданного блока из сегмента 2.
    'PtrCrt2' / construct.Hex(construct.Int16ul),  # Указатель записываемого блока из сегмента 2.
    'PtrEnd3' / construct.Hex(construct.Int16ul),  # Указатель последнего переданного блока из сегмента 3.
    'PtrCrt3' / construct.Hex(construct.Int16ul),  # Указатель записываемого блока из сегмента 3.
    'LastEvent_CH1_1' / construct.Hex(construct.Int8ul),  # Последние событие канал 1 M1L1.
    'LastEvent_CH1_2' / construct.Hex(construct.Int8ul),  # Последние событие канал 1 L2H1.
    'LastEvent_CH1_3' / construct.Hex(construct.Int8ul),  # Последние событие канал 1 H2M2.
    'LastEvent_CH2_1' / construct.Hex(construct.Int8ul),  # Последние событие канал 2 M1L1.
    'LastEvent_CH2_2' / construct.Hex(construct.Int8ul),  # Последние событие канал 2 L2H1.
    'LastEvent_CH2_3' / construct.Hex(construct.Int8ul),  # Последние событие канал 2 H2M2.
)

time_request = construct.Struct(
    '_name' / construct.Computed('time_request'),
    'name' / construct.Computed('TIME_REQUEST'),
    'desc' / construct.Computed('Acknowledge of completed data transmission'),
)

detector_transmits = construct.Struct(
    '_name' / construct.Computed('detector_transmits'),
    'name' / construct.Computed('DETECTOR_TRANSMITS'),
    'desc' / construct.Computed('Detector mod data'),
)

data_massive_addr_rpl = construct.Struct(
    '_name' / construct.Computed('data_massive_addr_rpl'),
    'name' / construct.Computed('DATA_MASSIVE_ADDR_RPL'),
    'desc' / construct.Computed('Massive addr mod data'),
)

data_event_addr_rpl = construct.Struct(
    '_name' / construct.Computed('data_event_addr_rpl'),
    'name' / construct.Computed('DATA_EVENT_ADDR_RPL'),
    'desc' / construct.Computed('Event addr mod data'),
)

data_monitor_addr_rpl = construct.Struct(
    '_name' / construct.Computed('data_monitor_addr_rpl'),
    'name' / construct.Computed('DATA_MONITOR_ADDR_RPL'),
    'desc' / construct.Computed('Monitor addr mod data'),
)

data_massive_rpl = construct.Struct(
    '_name' / construct.Computed('data_massive_rpl'),
    'name' / construct.Computed('DATA_MASSIVE_RPL'),
    'desc' / construct.Computed('Massive mod data'),
)

data_event_rpl = construct.Struct(
    '_name' / construct.Computed('data_event_rpl'),
    'name' / construct.Computed('DATA_EVENT_RPL'),
    'desc' / construct.Computed('Event mod ata'),
)

data_monitor_rpl = construct.Struct(
    '_name' / construct.Computed('data_monitor_rpl'),
    'name' / construct.Computed('DATA_MONITOR_RPL'),
    'desc' / construct.Computed('Monitor mod data'),
)

get_Payload_FW_MSG = construct.Struct(
    '_name' / construct.Computed('get_Payload_FW_MSG'),
    'name' / construct.Computed('Payload FW MSG'),
    'desc' / construct.Computed('Payload FW MSG'),
    'Modification' / construct.Int8ul,  # Modification
    'Version' / construct.Int8ul,  # Version
    'Release_Number' / construct.Int8ul,  # Release Number
)

no_monitor_data = construct.Struct(
    '_name' / construct.Computed('no_monitor_data'),
    'name' / construct.Computed('NO_MONITOR_DATA'),
    'desc' / construct.Computed('There is no enought corresponding data'),
)

no_event_data = construct.Struct(
    '_name' / construct.Computed('no_event_data'),
    'name' / construct.Computed('NO_EVENT_DATA'),
    'desc' / construct.Computed('There is no enought corresponding data'),
)

no_massive_data = construct.Struct(
    '_name' / construct.Computed('no_massive_data'),
    'name' / construct.Computed('NO_MASSIVE_DATA'),
    'desc' / construct.Computed('There is no enought corresponding data'),
)

compl_monitor_data = construct.Struct(
    '_name' / construct.Computed('compl_monitor_data'),
    'name' / construct.Computed('COMPL_MONITOR_DATA'),
    'desc' / construct.Computed('Acknowledge of completed data transmission'),
)

compl_event_data = construct.Struct(
    '_name' / construct.Computed('compl_event_data'),
    'name' / construct.Computed('COMPL_EVENT_DATA'),
    'desc' / construct.Computed('Acknowledge of completed data transmission'),
)

compl_massive_data = construct.Struct(
    '_name' / construct.Computed('compl_massive_data'),
    'name' / construct.Computed('COMPL_MASSIVE_DATA'),
    'desc' / construct.Computed('Acknowledge of completed data transmission'),
)

get_Payload_CURRENT_CONFIG = construct.Struct(
    '_name' / construct.Computed('get_Payload_CURRENT_CONFIG'),
    'name' / construct.Computed('Payload CURRENT CONFIG'),
    'desc' / construct.Computed('Payload CURRENT CONFIG'),
    'cur_seg2_write' / construct.Hex(construct.Int32ul),  # Текущий номер ячейки в сегменте памяти 1 (Монитор), в которую производится запись
    'cur_seg2_last_transmitted' / construct.Hex(construct.Int32ul),  # Номер последней переданной ячейки в сегменте памяти 1 (Монитор)
    'cur_seg2_min' / construct.Hex(construct.Int32ul),  # Начальный адрес 1го сегмента в памяти (Монитор)
    'cur_seg2_max' / construct.Hex(construct.Int32ul),  # Конечный адрес 1го сегмента в памяти (Монитор)
    'cur_seg2_num' / construct.Hex(construct.Int32ul),  # "Сквозной" номер для 1го сегмента в памяти (Монитор)
    'cur_seg3_write' / construct.Hex(construct.Int32ul),  # Текущий номер ячейки в сегменте памяти 2 (Событие), в которую производится запись
    'cur_seg3_last_transmitted' / construct.Hex(construct.Int32ul),  # Номер последней переданной ячейки в сегменте памяти 2 (Событие)
    'cur_seg3_min' / construct.Hex(construct.Int32ul),  # Начальный адрес 2го сегмента в памяти (Событие)
    'cur_seg3_max' / construct.Hex(construct.Int32ul),  # Конечный адрес 2го сегмента в памяти (Событие)
    'cur_seg3_num' / construct.Hex(construct.Int32ul),  # "Сквозной" номер для 2го сегмента в памяти (Событие)
    'cur_seg4_write' / construct.Hex(construct.Int32ul),  # Текущий номер ячейки в сегменте памяти 3 (Массив), в которую производится запись
    'cur_seg4_last_transmitted' / construct.Hex(construct.Int32ul),  # Номер последней переданной ячейки в сегменте памяти 3 (Массив)
    'cur_seg4_min' / construct.Hex(construct.Int32ul),  # Начальный адрес 3го сегмента в памяти (Массив)
    'cur_seg4_max' / construct.Hex(construct.Int32ul),  # Конечный адрес 3го сегмента в памяти (Массив)
    'cur_seg4_num' / construct.Hex(construct.Int32ul),  # "Сквозной" номер для 3го сегмента в памяти (Массив)
    'time_start_massive_write' / common.UNIXTimestampAdapter(construct.Int32ul),  # Время старта для отложенной записи в Массив
    'status_massive_write_enable' / construct.Hex(construct.Int8ul),  # Флаг включения записи в Массив
    'time_monitor_x100ms' / common.LinearAdapter(100, construct.Int8ul),  # Множитель для внутреннего таймера, формирующего события для записи в блок Монитор х100 мс
    'can_device_id' / construct.Hex(construct.Int8ul),  # Текущий адрес ПН в CAN-шине
    'can_station_id' / construct.Hex(construct.Int8ul),  # Текущий адрес Базовой Станции в CAN-шине
    'can_tranciever_id' / construct.Hex(construct.Int8ul),  # Текущий адрес Трансивера на борту в CAN-шине
    'TimeRst' / common.UNIXTimestampAdapter(construct.Int32ul),  # Текущее время, которое становится временем перезагрузки в период сохранения текущей конфигурации
    'NRst' / construct.Int8ul,  # Количество перезагрузок
    'max_zagruz' / construct.Int16ul,  # Настраиваемая максимальная загрузка ПН по числу срабатываний, необходима для балансировки нагрузки
    'ch1_summ_threshold' / construct.Int16ul,  # Порог срабатывания для 1го дополнитльеного канала счёта (CH1Rate в структуре Beacon)
    'ch2_summ_threshold' / construct.Int16ul,  # Порог срабатывания для 2го дополнитльеного канала счёта (CH2Rate в структуре Beacon)
    'num_counter_channels' / construct.Int8ul,  # Число каналов для скоростей счёта, deault value 0x03 (TotalRate, CH1Rate, CH2Rate)
    'time_save_configure' / construct.Int16ul,  # Интервал времени, через который происходит сохранение текущей конфигурации, сек
    'data_correct' / construct.Hex(construct.Int8ul),  # Флаг подтверждения корректности (грубо) текущей конфигурации, default value 0x01
)

regular_telemetry_flags0 = construct.BitStruct(
    'VTG_BAT_CRIT' / construct.Flag,  # Флаг критического напр. АКБ
    'VTG_BAT_MIN' / construct.Flag,  # Флаг минимального напр. АКБ
    'HEATER2_Manual' / construct.Flag,  # Флаг нагреватель 2 ручное управление
    'HEATER1_Manual' / construct.Flag,  # Флаг нагреватель 1 ручное управление
    'HEATER2_ON' / construct.Flag,  # Флаг нагреватель 2 вкл
    'HEATER1_ON' / construct.Flag,  # Флаг нагреватель 1 вкл
    'TMP_MAX' / construct.Flag,  # Флаг макс. темп. АКБ
    'TMP_MIN' / construct.Flag,  # Флаг мин. темп. АКБ
    'CHANNEL4_ON' / construct.Flag,  # Флаг включения канала 4
    'CHANNEL3_ON' / construct.Flag,  # Флаг включения канала 3
    'CHANNEL2_ON' / construct.Flag,  # Флаг включения канала 2
    'CHANNEL1_ON' / construct.Flag,  # Флаг включения канала 1
    'ICH_FAULT_4' / construct.Flag,  # Флаг неисправности канала 4
    'ICH_FAULT_3' / construct.Flag,  # Флаг неисправности канала 3
    'ICH_FAULT_2' / construct.Flag,  # Флаг неисправности канала 2
    'ICH_FAULT_1' / construct.Flag,  # Флаг неисправности канала 1
    '_pad0' / construct.BitsInteger(3),
    'Additional_channel_3_on' / construct.Flag,  # Флаг включения дополнительного канала 3
    'Additional_channel_2_on' / construct.Flag,  # Флаг включения дополнительного канала 2
    'Additional_channel_1_on' / construct.Flag,  # Флаг включения дополнительного канала 1
    'FSB' / construct.Flag,  # Флаг ошибки коммутатора
    'CHAGER' / construct.Flag,  # Флаг подключния зарядного устройства
    '_pad1' / construct.BitsInteger(8),
)
regular_telemetry = construct.Struct(
    '_name' / construct.Computed('regular_telemetry'),
    'name' / construct.Computed('Regular'),
    'desc' / construct.Computed('Regular telemetry for PSS'),
    'VTG_S1' / construct.Int16ul,  # Напряжение на входе 1, мВ
    'VTG_S2' / construct.Int16ul,  # Напряжение на входе 2, мВ
    'VTG_S3' / construct.Int16ul,  # Напряжение на входе 3, мВ
    'CUR_S1' / construct.Int16ul,  # Ток на входе 1, мА
    'CUR_S2' / construct.Int16ul,  # Ток на входе 2, мА
    'CUR_S3' / construct.Int16ul,  # Ток на входе 3, мА
    'CUR_BAT' / construct.Int16sl,  # Ток АКБ, мА
    'CUR_S1O' / construct.Int16ul,  # Ток на выходе 1, мА
    'CUR_S2O' / construct.Int16ul,  # Ток на выходе 2, мА
    'CUR_S3O' / construct.Int16ul,  # Ток на выходе 3, мА
    'CUR_S4O' / construct.Int16ul,  # Ток на выходе 4, мА
    'TMP_BAT1' / RegTemp,  # Температура АКБ 1, град*100
    'TMP_BAT2' / RegTemp,  # Температура АКБ 2, град*100
    'TMP_BAT3' / RegTemp,  # Температура АКБ 3, град*100
    'TMP_BAT4' / RegTemp,  # Температура АКБ 4, град*100
    'flags0' / regular_telemetry_flags0,
    'VBAT' / construct.Int16ul,  # Напр. АКБ
    'REC_ID' / construct.Int32ul,  # Порядковый номер пакета
    'Time' / common.UNIXTimestampAdapter(construct.Int32sl),  # Время (time_t)
    'launch_number' / construct.Int8ul,  # Количество загрузок
    'reset_reason' / construct.Hex(construct.Int8ul),  # причина перезагрузки
)

extended_telemetry = construct.Struct(
    '_name' / construct.Computed('extended_telemetry'),
    'name' / construct.Computed('Extended'),
    'desc' / construct.Computed('Extended telemetry packet'),
    'CHRG_LIM' / construct.Int16sl,  # Огр. зар. тока, мА
    'TMP_MIN' / RegTemp,  # Мин. температура АКБ, град*100
    'TMP_MAX' / RegTemp,  # Макс. температура АКБ, град*100
    'VTG_BAT' / construct.Int16ul,  # Напр. просадки АКБ, мВ
    'TIME_BAT' / construct.Int16ul,  # Время. просадки АКБ, мсек
    'CUR_LIM1' / construct.Int16ul,  # Огр. тока канала 1
    'CUR_LIM2' / construct.Int16ul,  # Огр. тока канала 2
    'CUR_LIM3' / construct.Int16ul,  # Огр. тока канала 3
    'CUR_LIM4' / construct.Int16ul,  # Огр. тока канала 4
    'DEV_ADDR' / construct.Hex(construct.Int16ul),  # Адрес устройства
    'SRC_ADDR' / construct.Hex(construct.Int16ul),  # Адрес получателя
    'TEL_PER' / construct.Int16ul,  # Период регулярной телеметрии, мсек
    'ETEL_PER' / construct.Int16ul,  # Период расширенной телеметрии, сек
    'REC_ID' / construct.Int32ul,  # Порядковый номер пакета
    'ST_DELAY' / construct.Int16ul,  # Задержка старта питания аппарата
    'SW_VER' / construct.Int16ul,  # PPS firmware version
)

overcurrent = construct.Struct(
    '_name' / construct.Computed('overcurrent'),
    'name' / construct.Computed('Overcurrent'),
    'desc' / construct.Computed('Overcurrent'),
    'Channel' / construct.Int8ul,  # Номер канала
)

switch_status = construct.Struct(
    '_name' / construct.Computed('switch_status'),
    'name' / construct.Computed('Switch status'),
    'desc' / construct.Computed('Switch status'),
    'Ch0Status' / construct.Hex(construct.Int16ul),  # Статус канала 0
    'Ch1Status' / construct.Hex(construct.Int16ul),  # Статус канала 1
    'Ch2Status' / construct.Hex(construct.Int16ul),  # Статус канала 2
    'Ch3Status' / construct.Hex(construct.Int16ul),  # Статус канала 3
)

ch_adc_X1 = construct.Struct(
    '_name' / construct.Computed('ch_adc_X1'),
    'name' / construct.Computed('ADC Ch#X1'),
    'desc' / construct.Computed('ADC data packet on detector channel X1'),
    'ADC_X1' / construct.Int32sl,  # Значение по каналу X1
    'Temp_Ext' / RegTemp,  # Температура датчика у детектора, градусы Цельсия * 100
)

ch_adc_X2 = construct.Struct(
    '_name' / construct.Computed('ch_adc_X2'),
    'name' / construct.Computed('ADC Ch#X2'),
    'desc' / construct.Computed('ADC data packet on detector channel X2'),
    'ADC_X2' / construct.Int32sl,  # Значение по каналу X2
    'Temp_Int' / RegTemp,  # Температура датчика МК, градусы Цельсия * 100
)

ch_adc_Y1 = construct.Struct(
    '_name' / construct.Computed('ch_adc_Y1'),
    'name' / construct.Computed('ADC Ch#Y1'),
    'desc' / construct.Computed('ADC data packet on detector channel Y1'),
    'ADC_Y1' / construct.Int32sl,  # Значение по каналу Y1
    'ADC_Ext' / construct.Int16ul,  # Отсчеты внешнего температурного датчика
)

ch_adc_Y2 = construct.Struct(
    '_name' / construct.Computed('ch_adc_Y2'),
    'name' / construct.Computed('ADC Ch#Y2'),
    'desc' / construct.Computed('ADC data packet on detector channel Y2'),
    'ADC_Y2' / construct.Int32sl,  # Значение по каналу Y2
    'ADC_Int' / construct.Int16ul,  # Отсчеты внутреннего температурного датчика
)

temp_cur_X1 = construct.Struct(
    '_name' / construct.Computed('temp_cur_X1'),
    'name' / construct.Computed('Temperature/current X1'),
    'desc' / construct.Computed('ADC data packet on detector channel X1'),
    'ADC_X1' / construct.Int32sl,  # Значение по каналу X1
    'Temp_Ext' / RegTemp,  # Температура датчика у детектора, градусы Цельсия * 100
)

temp_cur_X2 = construct.Struct(
    '_name' / construct.Computed('temp_cur_X2'),
    'name' / construct.Computed('Temperature/current X2'),
    'desc' / construct.Computed('ADC data packet on detector channel X2'),
    'ADC_X2' / construct.Int32sl,  # Значение по каналу X2
    'Temp_Int' / RegTemp,  # Температура датчика МК, градусы Цельсия * 100
)

temp_cur_Y1 = construct.Struct(
    '_name' / construct.Computed('temp_cur_Y1'),
    'name' / construct.Computed('Temperature/current Y1'),
    'desc' / construct.Computed('ADC data packet on detector channel Y1'),
    'ADC_Y1' / construct.Int32sl,  # Значение по каналу Y1
    'ADC_Ext' / construct.Int16ul,  # Отсчеты внешнего температурного датчика
)

temp_cur_Y2 = construct.Struct(
    '_name' / construct.Computed('temp_cur_Y2'),
    'name' / construct.Computed('Temperature/current Y2'),
    'desc' / construct.Computed('ADC data packet on detector channel Y2'),
    'ADC_Y2' / construct.Int32sl,  # Значение по каналу Y2
    'ADC_Int' / construct.Int16ul,  # Отсчеты внутреннего температурного датчика
)

version_sw = construct.Struct(
    '_name' / construct.Computed('version_sw'),
    'name' / construct.Computed('VERSION SW'),
    'desc' / construct.Computed('VERSION SW'),
    'major' / construct.Int8ul,  # major
    'minor' / construct.Int8ul,  # minor
    'extra' / construct.Int8ul,  # extra
)

# other
ImgStart = construct.Struct(
    '_name' / construct.Computed('ImgStart'),
    'name' / construct.Computed('ImgStart'),
    'mode' / construct.Int8ul,
    'ses_id' / construct.Int8ul,
    'bs' / construct.Int16ul,
    'offset' / construct.Int32ul,
    'reserved' / construct.Int16ul,     # mb string size?
    'file_name' / construct.GreedyString('utf-8'),
)

ImgSize = construct.Struct(
    '_name' / construct.Computed('ImgSize'),
    'name' / construct.Computed('ImgSize'),
    'size' / construct.Int32ul,
)

ImgData = construct.Struct(
    '_name' / construct.Computed('ImgData'),
    'name' / construct.Computed('ImgData'),
    'reserved0' / construct.Int8ul,
    'offset' / construct.Int32ul,
    'data' / construct.GreedyBytes,
)

tlm_map = {
    # tlm
    REGULAR_COMMON: 'regular_common' / regular_common,
    REGULAR_X: 'regular_x' / regular_x,
    REGULAR_Y: 'regular_y' / regular_y,
    REGULAR_Z: 'regular_z' / regular_z,
    PSU_REGULAR0: 'psu_regular0' / psu_regular0,
    PSU_REGULAR1: 'psu_regular1' / psu_regular1,
    PSU_REGULAR2: 'psu_regular2' / psu_regular2,
    PSU_REGULAR3: 'psu_regular3' / psu_regular3,
    PSU_REGULAR4: 'psu_regular4' / psu_regular4,
    INFO: 'Info' / Info,
    REGULAR_TEMPERATURE: 'regular_temperature' / regular_temperature,
    GET_PAYLOAD_TELEMETRY: 'get_Payload_telemetry' / get_Payload_telemetry,
    ARS_X_VEL: 'ars_X_vel' / ars_X_vel,
    ARS_Y_VEL: 'ars_Y_vel' / ars_Y_vel,
    ARS_Z_VEL: 'ars_Z_vel' / ars_Z_vel,
    MAG_X: 'mag_X' / mag_X,
    MAG_Y: 'mag_Y' / mag_Y,
    MAG_Z: 'mag_Z' / mag_Z,
    VECTOR_X: 'Vector_X' / Vector_X,
    VECTOR_Y: 'Vector_Y' / Vector_Y,
    VECTOR_Z: 'Vector_Z' / Vector_Z,
    BRIGHTNESS: 'Brightness' / Brightness,
    COMMON_TELEMETRY: 'common_telemetry' / common_telemetry,
    VHF_SETTINGS: 'vhf_settings' / vhf_settings,
    BEACON: 'beacon' / beacon,
    EXTENDED_BEACON: 'extended_beacon' / extended_beacon,
    TIME_REQUEST: 'time_request' / time_request,
    DETECTOR_TRANSMITS: 'detector_transmits' / detector_transmits,
    DATA_MASSIVE_ADDR_RPL: 'data_massive_addr_rpl' / data_massive_addr_rpl,
    DATA_EVENT_ADDR_RPL: 'data_event_addr_rpl' / data_event_addr_rpl,
    DATA_MONITOR_ADDR_RPL: 'data_monitor_addr_rpl' / data_monitor_addr_rpl,
    DATA_MASSIVE_RPL: 'data_massive_rpl' / data_massive_rpl,
    DATA_EVENT_RPL: 'data_event_rpl' / data_event_rpl,
    DATA_MONITOR_RPL: 'data_monitor_rpl' / data_monitor_rpl,
    GET_PAYLOAD_FW_MSG: 'get_Payload_FW_MSG' / get_Payload_FW_MSG,
    NO_MONITOR_DATA: 'no_monitor_data' / no_monitor_data,
    NO_EVENT_DATA: 'no_event_data' / no_event_data,
    NO_MASSIVE_DATA: 'no_massive_data' / no_massive_data,
    COMPL_MONITOR_DATA: 'compl_monitor_data' / compl_monitor_data,
    COMPL_EVENT_DATA: 'compl_event_data' / compl_event_data,
    COMPL_MASSIVE_DATA: 'compl_massive_data' / compl_massive_data,
    GET_PAYLOAD_CURRENT_CONFIG: 'get_Payload_CURRENT_CONFIG' / get_Payload_CURRENT_CONFIG,
    REGULAR_TELEMETRY: 'regular_telemetry' / regular_telemetry,
    EXTENDED_TELEMETRY: 'extended_telemetry' / extended_telemetry,
    OVERCURRENT: 'overcurrent' / overcurrent,
    SWITCH_STATUS: 'switch_status' / switch_status,
    CH_ADC_X1: 'ch_adc_X1' / ch_adc_X1,
    CH_ADC_X2: 'ch_adc_X2' / ch_adc_X2,
    CH_ADC_Y1: 'ch_adc_Y1' / ch_adc_Y1,
    CH_ADC_Y2: 'ch_adc_Y2' / ch_adc_Y2,
    TEMP_CUR_X1: 'temp_cur_X1' / temp_cur_X1,
    TEMP_CUR_X2: 'temp_cur_X2' / temp_cur_X2,
    TEMP_CUR_Y1: 'temp_cur_Y1' / temp_cur_Y1,
    TEMP_CUR_Y2: 'temp_cur_Y2' / temp_cur_Y2,
    VERSION_SW: 'version_sw' / version_sw,

    # other
    IMG_START: 'ImgStart' / ImgStart,
    IMG_SIZE: 'ImgSize' / ImgSize,
    IMG_DATA: 'ImgData' / ImgData,
}


Data = construct.Struct(
    'message' / Addr,
    'sender' / Addr,
    'receiver' / Addr,
    'size' / construct.Int16ul,
    'packet' / construct.Switch(construct.this.message, tlm_map, default=construct.Bytes(construct.this.size)),
)

Frame = construct.Struct(
    'data' / construct.GreedyRange(Data),
    'lost' / construct.GreedyBytes
)

usp = construct.Struct(
    'ax25' / construct.Peek(common.ax25_header),
    'ax25' / construct.If(lambda this: bool(this.ax25), common.ax25_header),
    'usp' / construct.If(lambda this: (bool(this.ax25) and this.ax25.pid == 0xF0), Frame)
)


def usp_get_sender_callsign(tlm):
    return common.ax25_get_sender_callsign(tlm.ax25)


class UspImageReceiver(ImageReceiver):
    def __init__(self, outdir):
        super().__init__(outdir)

    def generate_fid(self, fname='unknown'):
        if not (self.current_fid and self.merge_mode):
            self.current_fid = fname
        return self.current_fid

    def push_data(self, data):
        packet = data.packet

        if data.message == IMG_DATA:
            img = self.get_image()
            with img.lock:
                img.push_data(packet.offset, packet.data[:data.size - 5])
                if packet.offset < img.first_data_offset:
                    img.first_data_offset = packet.offset

        elif data.message == IMG_START:
            self.generate_fid(packet.file_name)
            img = self.get_image()
            with img.lock:
                img.has_starter = 1

        elif data.message == IMG_SIZE:
            img = self.get_image()
            with img.lock:
                img.open().truncate(packet.size)

        else:
            return
        return 1


class UspProtocol:
    columns = 'msg-id',
    c_width = 60,
    tlm_table = {
        'regular_common': {
            'table': (
                ('name', 'Name'),
                ('desc', 'Description'),
                ('current', 'Current'),
                ('voltage', 'Voltage'),
            ),
            'flags': (
                ('voltage_invalid', 'Voltage inval'),
                ('current_invalid', 'Current inval'),
            ),
        },
        'regular_x': {
            'table': (
                ('name', 'Name'),
                ('desc', 'Description'),
                ('current', 'Current'),
                ('voltage', 'Voltage'),
            ),
            'flags': (
                ('voltage_invalid', 'Voltage inval'),
                ('current_invalid', 'Current inval'),
            ),
        },
        'regular_y': {
            'table': (
                ('name', 'Name'),
                ('desc', 'Description'),
                ('current', 'Current'),
                ('voltage', 'Voltage'),
            ),
            'flags': (
                ('voltage_invalid', 'Voltage inval'),
                ('current_invalid', 'Current inval'),
            ),
        },
        'regular_z': {
            'table': (
                ('name', 'Name'),
                ('desc', 'Description'),
                ('current', 'Current'),
                ('voltage', 'Voltage'),
            ),
            'flags': (
                ('voltage_invalid', 'Voltage inval'),
                ('current_invalid', 'Current inval'),
            ),
        },
        'psu_regular0': {
            'table': (
                ('name', 'Name'),
                ('desc', 'Description'),
                ('current', 'Current'),
                ('voltage', 'Voltage'),
            ),
            'flags': (
                ('voltage_invalid', 'Voltage inval'),
                ('current_invalid', 'Current inval'),
            ),
        },
        'psu_regular1': {
            'table': (
                ('name', 'Name'),
                ('desc', 'Description'),
                ('current', 'Current'),
                ('voltage', 'Voltage'),
            ),
            'flags': (
                ('voltage_invalid', 'Voltage inval'),
                ('current_invalid', 'Current inval'),
            ),
        },
        'psu_regular2': {
            'table': (
                ('name', 'Name'),
                ('desc', 'Description'),
                ('current', 'Current'),
                ('voltage', 'Voltage'),
            ),
            'flags': (
                ('voltage_invalid', 'Voltage inval'),
                ('current_invalid', 'Current inval'),
            ),
        },
        'psu_regular3': {
            'table': (
                ('name', 'Name'),
                ('desc', 'Description'),
                ('current', 'Current'),
                ('voltage', 'Voltage'),
            ),
            'flags': (
                ('voltage_invalid', 'Voltage inval'),
                ('current_invalid', 'Current inval'),
            ),
        },
        'psu_regular4': {
            'table': (
                ('name', 'Name'),
                ('desc', 'Description'),
                ('current', 'Current'),
                ('voltage', 'Voltage'),
            ),
            'flags': (
                ('voltage_invalid', 'Voltage inval'),
                ('current_invalid', 'Current inval'),
            ),
        },
        'Info': {
            'table': (
                ('name', 'Name'),
                ('desc', 'Description'),
                ('SW_VER', 'Firmware version'),
                ('SERIAL', 'Board serial number'),
                ('CANTEL', 'CAN Telemetry mode'),
                ('UARTTEL', 'UART Telemetry mode'),
                ('ADC_REF', 'ADC reference value, mV'),
                ('THRESHOLD', 'Brightness threshold'),
                ('SET_STAT', 'Parameters loading result'),
                ('LM70_STAT', 'Temperature polynomial loading result'),
                ('VECT_STAT', 'Vector polynomial loading result'),
            ),
        },
        'regular_temperature': {
            'table': (
                ('name', 'Name'),
                ('desc', 'Description'),
                ('temperature0', 'Temperature #0'),
                ('temperature1', 'Temperature #1'),
            ),
            'flags': (
                ('temperature1_invalid', 'Temperature #1 inval'),
                ('temperature0_invalid', 'Temperature #0 inval'),
            ),
        },
        'get_Payload_telemetry': {
            'table': (
                ('name', 'Name'),
                ('desc', 'Description'),
                ('FL', 'PL flags'),
                ('Time', 'PL last telemetry time'),
                ('T_Plate', 'PL board temperature'),
                ('T_CPU', 'PL microcontroller temperature'),
                ('CurSens1', 'Current sensor #1'),
                ('CurSens2', 'Current sensor #2'),
                ('NRst', 'Reboots count'),
                ('TimeRst', 'Last reboot time'),
                ('CH1Rate', 'Ch#1 counting speed'),
                ('CH2Rate', 'Ch#2 counting speed'),
                ('CH3Rate', 'Ch#3 counting speed'),
                ('CH4Rate', 'Ch#4 counting speed'),
                ('CH5Rate', 'Ch#5 counting speed'),
                ('CH6Rate', 'Ch#6 counting speed'),
                ('PtrEnd1', 'Last block pointer transferred from segment #1'),
                ('PtrCrt1', 'Block pointer to be written from segment #1'),
                ('PtrEnd2', 'Last block pointer transferred from segment #2'),
                ('PtrCrt2', 'Block pointer to be written from segment #2'),
                ('PtrEnd3', 'Last block pointer transferred from segment #3'),
                ('PtrCrt3', 'Block pointer to be written from segment #3'),
                ('LastEvent_CH1_1', 'Last event Ch#1 M1L1'),
                ('LastEvent_CH1_2', 'Last event Ch#1 L2H1'),
                ('LastEvent_CH1_3', 'Last event Ch#1 H2M2'),
                ('LastEvent_CH2_1', 'Last event Ch#2 M1L1'),
                ('LastEvent_CH2_2', 'Last event Ch#2 L2H1'),
                ('LastEvent_CH2_3', 'Last event Ch#2 H2M2'),
            ),
        },
        'ars_X_vel': {
            'table': (
                ('name', 'Name'),
                ('desc', 'Description'),
                ('Velocity_X', 'Velocity, deg/s'),
                ('Temp_X', 'Temperature, °C'),
            ),
            'flags': (
                ('Valid_X', 'Data is not valid'),
            ),
        },
        'ars_Y_vel': {
            'table': (
                ('name', 'Name'),
                ('desc', 'Description'),
                ('Velocity_Y', 'Velocity, deg/s'),
                ('Temp_Y', 'Temperature, °C'),
            ),
            'flags': (
                ('Valid_Y', 'Data is not valid'),
            ),
        },
        'ars_Z_vel': {
            'table': (
                ('name', 'Name'),
                ('desc', 'Description'),
                ('Velocity_Z', 'Velocity, deg/s'),
                ('Temp_Z', 'Temperature, °C'),
            ),
            'flags': (
                ('Valid_Z', 'Data is not valid'),
            ),
        },
        'mag_X': {
            'table': (
                ('name', 'Name'),
                ('desc', 'Description'),
                ('Field_X', 'Magnetic field, nT'),
                ('Temp_X', 'Temperature, °C'),
            ),
            'flags': (
                ('Valid_X', 'Data is not valid'),
            ),
        },
        'mag_Y': {
            'table': (
                ('name', 'Name'),
                ('desc', 'Description'),
                ('Field_Y', 'Magnetic field, nT'),
                ('Temp_Y', 'Temperature, °C'),
            ),
            'flags': (
                ('Valid_Y', 'Data is not valid'),
            ),
        },
        'mag_Z': {
            'table': (
                ('name', 'Name'),
                ('desc', 'Description'),
                ('Field_Z', 'Magnetic field, nT'),
                ('Temp_Z', 'Temperature, °C'),
            ),
            'flags': (
                ('Valid_Z', 'Data is not valid'),
            ),
        },
        'Vector_X': {
            'table': (
                ('name', 'Name'),
                ('desc', 'Description'),
                ('Vect_X', 'X direction, deg'),
                ('Temp_X', 'Temperature, °C'),
            ),
            'flags': (
                ('Invalid_X', 'Data is valid'),
            ),
        },
        'Vector_Y': {
            'table': (
                ('name', 'Name'),
                ('desc', 'Description'),
                ('Vect_Y', 'Y direction, deg'),
                ('Temp_Y', 'Temperature, °C'),
            ),
            'flags': (
                ('Invalid_Y', 'Data is valid'),
            ),
        },
        'Vector_Z': {
            'table': (
                ('name', 'Name'),
                ('desc', 'Description'),
                ('Vect_Z', 'Z direction, deg'),
            ),
            'flags': (
                ('Invalid_Z', 'Data is valid'),
            ),
        },
        'Brightness': {
            'table': (
                ('name', 'Name'),
                ('desc', 'Description'),
                ('Sum', 'Channels total brightness'),
            ),
        },
        'common_telemetry': {
            'table': (
                ('name', 'Name'),
                ('desc', 'Description'),
                ('Data', 'Data'),
            ),
        },
        'vhf_settings': {
            'table': (
                ('name', 'Name'),
                ('desc', 'Description'),
                ('Magic', 'Magic'),
                ('Frequency', 'Frequency'),
                ('BitRate', 'Bitrate'),
                ('DAC1Setting', 'DAC #1 Setting'),
                ('DAC2Setting', 'DAC #2 Setting'),
                ('TPacketMode', 'TPacket Mode'),
                ('EnableBeacon', 'Enable Beacon'),
                ('BeaconInterval', 'Beacon Interval'),
                ('CallSign', 'Callsign'),
                ('SSID', 'SSID'),
                ('EarthCallSign', 'Earth Callsign'),
                ('EarthSSID', 'Earth SSID'),
                ('TLocation', 'TLocation'),
                ('UNIcanID', 'UNIcan ID'),
                ('EnableBridge', 'Enable Bridge'),
                ('BeaconStartupDelay', 'Beacon Startup Delay'),
            ),
        },
        'beacon': {
            'table': (
                ('name', 'Name'),
                ('desc', 'Description'),
                ('Usb1', 'SB #1 voltage, mV'),
                ('Usb2', 'SB #2 voltage, mV'),
                ('Usb3', 'SB #3 voltage, mV'),
                ('Isb1', 'SB #1 current, mA'),
                ('Isb2', 'SB #2 current, mA'),
                ('Isb3', 'SB #3 current, mA'),
                ('Iab', 'Battery current, mA'),
                ('Ich1', 'Ch#1 current, mA'),
                ('Ich2', 'Ch#2 current, mA'),
                ('Ich3', 'Ch#3 current, mA'),
                ('Ich4', 'Ch#4 current, mA'),
                ('t1_pw', 'Battery #1 temperature, °C'),
                ('t2_pw', 'Battery #2 temperature, °C'),
                ('t3_pw', 'Battery #3 temperature, °C'),
                ('t4_pw', 'Battery #4 temperature, °C'),
                ('Uab', 'Battery voltage, mV'),
                ('reg_tel_id', 'Telemetry SN'),
                ('Time', 'PS telemetry time'),
                ('Nres', 'PS Reloads'),
                ('FL', 'PS flags'),
                ('t_amp', 'UHF amp temperature, °C'),
                ('t_uhf', 'UHF temperature, °C'),
                ('RSSIrx', 'RSSI Received, dBm'),
                ('RSSIidle', 'RSSI Idle, dBm'),
                ('Pf', 'Direct radiation power'),
                ('Pb', 'Back radiation power'),
                ('Nres_uhf', 'UHF reloads'),
                ('FL_uhf', 'UHF flags'),
                ('Time_uhf', 'UHF telemetry time'),
                ('UpTime', 'Uptime'),
                ('Current', 'UHF current, mA'),
                ('Uuhf', 'UHF voltage, mV'),
            ),
            'flags': (
                ('Uab_crit', 'Critical battery voltage'),
                ('Uab_min', 'Minimal battery voltage'),
                ('heater2_manual', 'Heater #2 manual'),
                ('heater1_manual', 'Heater #1 manual'),
                ('heater2_on', 'Heater #2 ON'),
                ('heater1_on', 'Heater #1 ON'),
                ('Tab_max', 'Maximal battery Temperature'),
                ('Tab_min', 'Minimal battery Temperature'),
                ('channelon4', 'Ch#4 ON'),
                ('channelon3', 'Ch#3 ON'),
                ('channelon2', 'Ch#2 ON'),
                ('channelon1', 'Ch#1 ON'),
                ('Ich_limit4', 'Exceeding channel #4 current'),
                ('Ich_limit3', 'Exceeding channel #3 current'),
                ('Ich_limit2', 'Exceeding channel #2 current'),
                ('Ich_limit1', 'Exceeding channel #1 current'),
                ('charger', 'Charger connected'),
            ),
        },
        'extended_beacon': {
            'table': (
                ('name', 'Name'),
                ('desc', 'Description'),
                ('t_mb', 'Motherboard temperature, °C'),
                ('Mx', 'X magnetic field vector'),
                ('My', 'Y magnetic field vector'),
                ('Mz', 'Z magnetic field vector'),
                ('Vx', 'X velocity'),
                ('Vy', 'Y velocity'),
                ('Vz', 'Z velocity'),
                ('Nres', 'Reloads'),
                ('Rcon', 'Last Reload reason'),
                ('FL', 'Flags'),
                ('Time', 'Telemetry time'),
                ('FL_PL', 'PL Flags'),
                ('TimeSend', 'PL telemetry time'),
                ('T_Plate', 'PL Plate temperature'),
                ('T_CPU', 'PL microcontroller temperature'),
                ('CurSens1', 'Current sensor #1'),
                ('CurSens2', 'Current sensor #2'),
                ('NRst', 'Resets'),
                ('TimeRst', 'Last reset time'),
                ('CH1Rate', 'Ch#1 counting speed'),
                ('CH2Rate', 'Ch#2 counting speed'),
                ('CH3Rate', 'Ch#3 counting speed'),
                ('CH4Rate', 'Ch#4 counting speed'),
                ('CH5Rate', 'Ch#5 counting speed'),
                ('CH6Rate', 'Ch#6 counting speed'),
                ('PtrEnd1', 'Last block pointer transferred from segment #1'),
                ('PtrCrt1', 'Block pointer to be written from segment #1'),
                ('PtrEnd2', 'Last block pointer transferred from segment #2'),
                ('PtrCrt2', 'Block pointer to be written from segment #2'),
                ('PtrEnd3', 'Last block pointer transferred from segment #3'),
                ('PtrCrt3', 'Block pointer to be written from segment #3'),
                ('LastEvent_CH1_1', 'Last event Ch#1 M1L1'),
                ('LastEvent_CH1_2', 'Last event Ch#1 L2H1'),
                ('LastEvent_CH1_3', 'Last event Ch#1 H2M2'),
                ('LastEvent_CH2_1', 'Last event Ch#2 M1L1'),
                ('LastEvent_CH2_2', 'Last event Ch#2 L2H1'),
                ('LastEvent_CH2_3', 'Last event Ch#2 H2M2'),
            ),
        },
        'TIME_REQUEST': {
            'table': (
                ('name', 'Name'),
                ('desc', 'Description'),
            ),
        },
        'DETECTOR_TRANSMITS': {
            'table': (
                ('name', 'Name'),
                ('desc', 'Description'),
            ),
        },
        'DATA_MASSIVE_ADDR_RPL': {
            'table': (
                ('name', 'Name'),
                ('desc', 'Description'),
            ),
        },
        'DATA_EVENT_ADDR_RPL': {
            'table': (
                ('name', 'Name'),
                ('desc', 'Description'),
            ),
        },
        'DATA_MONITOR_ADDR_RPL': {
            'table': (
                ('name', 'Name'),
                ('desc', 'Description'),
            ),
        },
        'DATA_MASSIVE_RPL': {
            'table': (
                ('name', 'Name'),
                ('desc', 'Description'),
            ),
        },
        'DATA_EVENT_RPL': {
            'table': (
                ('name', 'Name'),
                ('desc', 'Description'),
            ),
        },
        'DATA_MONITOR_RPL': {
            'table': (
                ('name', 'Name'),
                ('desc', 'Description'),
            ),
        },
        'get_Payload_FW_MSG': {
            'table': (
                ('name', 'Name'),
                ('desc', 'Description'),
                ('Modification', 'Modification'),
                ('Version', 'Version'),
                ('Release_Number', 'Release Number'),
            ),
        },
        'NO_MONITOR_DATA': {
            'table': (
                ('name', 'Name'),
                ('desc', 'Description'),
            ),
        },
        'NO_EVENT_DATA': {
            'table': (
                ('name', 'Name'),
                ('desc', 'Description'),
            ),
        },
        'NO_MASSIVE_DATA': {
            'table': (
                ('name', 'Name'),
                ('desc', 'Description'),
            ),
        },
        'COMPL_MONITOR_DATA': {
            'table': (
                ('name', 'Name'),
                ('desc', 'Description'),
            ),
        },
        'COMPL_EVENT_DATA': {
            'table': (
                ('name', 'Name'),
                ('desc', 'Description'),
            ),
        },
        'COMPL_MASSIVE_DATA': {
            'table': (
                ('name', 'Name'),
                ('desc', 'Description'),
            ),
        },
        'get_Payload_CURRENT_CONFIG': {
            'table': (
                ('name', 'Name'),
                ('desc', 'Description'),
                ('cur_seg2_write', 'Write addr in seg#1 (Monitor)'),
                ('cur_seg2_last_transmitted', 'Last transmitted addr in seg#1'),
                ('cur_seg2_min', 'First addr in seg#1'),
                ('cur_seg2_max', 'Last addr in seg#1'),
                ('cur_seg2_num', '"Through" number seg#1'),
                ('cur_seg3_write', 'Write addr in seg#2 (Event)'),
                ('cur_seg3_last_transmitted', 'Last transmitted addr in seg#2'),
                ('cur_seg3_min', 'First addr in seg#2'),
                ('cur_seg3_max', 'Last addr in seg#2'),
                ('cur_seg3_num', '"Through" number seg#2'),
                ('cur_seg4_write', 'Write addr in seg#3 (Array)'),
                ('cur_seg4_last_transmitted', 'Last transmitted addr in seg#3'),
                ('cur_seg4_min', 'First addr in seg#3'),
                ('cur_seg4_max', 'Last addr in seg#3'),
                ('cur_seg4_num', '"Through" number seg#3'),
                ('time_start_massive_write', 'Start time of deferred write to Array'),
                ('status_massive_write_enable', 'Array write enable flag'),
                ('time_monitor_x100ms', 'Monitor writing internal timer multiplier, ms'),
                ('can_device_id', 'CAN-payload ID'),
                ('can_station_id', 'CAN-station ID'),
                ('can_tranciever_id', 'CAN-tranciever ID'),
                ('TimeRst', 'Last reset time'),
                ('NRst', 'Resets'),
                ('max_zagruz', 'Configurable max PL load by activations number'),
                ('ch1_summ_threshold', 'Ch#1 trigger threshold (CH1Rate in Beacon)'),
                ('ch2_summ_threshold', 'Ch#2 trigger threshold (CH2Rate in Beacon)'),
                ('num_counter_channels', 'Channels for counting speed (TotalRate, CH1Rate, CH2Rate)'),
                ('time_save_configure', 'Save configure timeout, s'),
                ('data_correct', 'Config is correct'),
            ),
        },
        'regular_telemetry': {
            'table': (
                ('name', 'Name'),
                ('desc', 'Description'),
                ('VTG_S1', 'Input #1 voltage, mV'),
                ('VTG_S2', 'Input #2 voltage, mV'),
                ('VTG_S3', 'Input #3 voltage, mV'),
                ('CUR_S1', 'Input #1 current, mA'),
                ('CUR_S2', 'Input #2 current, mA'),
                ('CUR_S3', 'Input #3 current, mA'),
                ('CUR_BAT', 'Battery current, mA'),
                ('CUR_S1O', 'Output #1 current, mA'),
                ('CUR_S2O', 'Output #2 current, mA'),
                ('CUR_S3O', 'Output #3 current, mA'),
                ('CUR_S4O', 'Output #4 current, mA'),
                ('TMP_BAT1', 'Battery #1 temperature, °C'),
                ('TMP_BAT2', 'Battery #2 temperature, °C'),
                ('TMP_BAT3', 'Battery #3 temperature, °C'),
                ('TMP_BAT4', 'Battery #4 temperature, °C'),
                ('VBAT', 'Battery voltage, mV'),
                ('REC_ID', 'Telemetry SN'),
                ('Time', 'Time'),
                ('launch_number', 'Launches'),
                ('reset_reason', 'Reset reason'),
            ),
            'flags': (
                ('VTG_BAT_CRIT', 'Critical battery voltage'),
                ('VTG_BAT_MIN', 'Minimal battery voltage'),
                ('HEATER2_Manual', 'Heater #2 manual'),
                ('HEATER1_Manual', 'Heater #1 manual'),
                ('HEATER2_ON', 'Heater #2 ON'),
                ('HEATER1_ON', 'Heater #1 ON'),
                ('TMP_MAX', 'Maximal battery Temperature'),
                ('TMP_MIN', 'Minimal battery Temperature'),
                ('CHANNEL4_ON', 'Ch#4 ON'),
                ('CHANNEL3_ON', 'Ch#3 ON'),
                ('CHANNEL2_ON', 'Ch#2 ON'),
                ('CHANNEL1_ON', 'Ch#1 ON'),
                ('ICH_FAULT_4', 'Ch#4 Fault'),
                ('ICH_FAULT_3', 'Ch#3 Fault'),
                ('ICH_FAULT_2', 'Ch#2 Fault'),
                ('ICH_FAULT_1', 'Ch#1 Fault'),
                ('Additional_channel_3_on', 'Additional Ch#3 ON'),
                ('Additional_channel_2_on', 'Additional Ch#2 ON'),
                ('Additional_channel_1_on', 'Additional Ch#1 ON'),
                ('FSB', 'Switch Error'),
                ('CHAGER', 'Charger connected'),
            ),
        },
        'extended_telemetry': {
            'table': (
                ('name', 'Name'),
                ('desc', 'Description'),
                ('CHRG_LIM', 'Charger current limit, mA'),
                ('TMP_MIN', 'Battery min temperature, °C'),
                ('TMP_MAX', 'Battery max temperature, °C'),
                ('VTG_BAT', 'Battery drawdown voltage, mV'),
                ('TIME_BAT', 'Battery drawdown time, ms'),
                ('CUR_LIM1', 'Ch#1 current limit'),
                ('CUR_LIM2', 'Ch#2 current limit'),
                ('CUR_LIM3', 'Ch#3 current limit'),
                ('CUR_LIM4', 'Ch#4 current limit'),
                ('DEV_ADDR', 'Device address'),
                ('SRC_ADDR', 'Source address'),
                ('TEL_PER', 'Regular telemetry period, ms'),
                ('ETEL_PER', 'Extended telemetry period, s'),
                ('REC_ID', 'Packet SN'),
                ('ST_DELAY', 'Startup delay'),
                ('SW_VER', 'PPS firmware version'),
            ),
        },
        'overcurrent': {
            'table': (
                ('name', 'Name'),
                ('desc', 'Description'),
                ('Channel', 'Channel'),
            ),
        },
        'switch_status': {
            'table': (
                ('name', 'Name'),
                ('desc', 'Description'),
                ('Ch0Status', 'Ch#0 status'),
                ('Ch1Status', 'Ch#1 status'),
                ('Ch2Status', 'Ch#2 status'),
                ('Ch3Status', 'Ch#3 status'),
            ),
        },
        'ch_adc_X1': {
            'table': (
                ('name', 'Name'),
                ('desc', 'Description'),
                ('ADC_X1', 'Ch#X1 value'),
                ('Temp_Ext', 'Sensor temperature at detector, °C'),
            ),
        },
        'ch_adc_X2': {
            'table': (
                ('name', 'Name'),
                ('desc', 'Description'),
                ('ADC_X2', 'Ch#X2 value'),
                ('Temp_Int', 'MCU sensor temperature, °C'),
            ),
        },
        'ch_adc_Y1': {
            'table': (
                ('name', 'Name'),
                ('desc', 'Description'),
                ('ADC_Y1', 'Ch#Y1 value'),
                ('ADC_Ext', 'External temperature sensor readings'),
            ),
        },
        'ch_adc_Y2': {
            'table': (
                ('name', 'Name'),
                ('desc', 'Description'),
                ('ADC_Y2', 'Ch#Y2 value'),
                ('ADC_Int', 'Internal temperature sensor readings'),
            ),
        },
        'temp_cur_X1': {
            'table': (
                ('name', 'Name'),
                ('desc', 'Description'),
                ('ADC_X1', 'Ch#X1 value'),
                ('Temp_Ext', 'Sensor temperature at detector, °C'),
            ),
        },
        'temp_cur_X2': {
            'table': (
                ('name', 'Name'),
                ('desc', 'Description'),
                ('ADC_X2', 'Ch#X2 value'),
                ('Temp_Int', 'MCU sensor temperature, °C'),
            ),
        },
        'temp_cur_Y1': {
            'table': (
                ('name', 'Name'),
                ('desc', 'Description'),
                ('ADC_Y1', 'Ch#Y1 value'),
                ('ADC_Ext', 'External temperature sensor readings'),
            ),
        },
        'temp_cur_Y2': {
            'table': (
                ('name', 'Name'),
                ('desc', 'Description'),
                ('ADC_Y2', 'Ch#Y2 value'),
                ('ADC_Int', 'Internal temperature sensor readings'),
            ),
        },
        'version_sw': {
            'table': (
                ('name', 'Name'),
                ('desc', 'Description'),
                ('major', 'major'),
                ('minor', 'minor'),
                ('extra', 'extra'),
            ),
        },
    }

    def __init__(self, outdir):
        self.ir = UspImageReceiver(outdir)

    @staticmethod
    def get_sender_callsign(data):
        return common.ax25_get_sender_callsign(data.ax25)

    def recognize(self, data):
        data = usp.parse(data)
        if not data.usp:
            return

        for i in data.usp.data:
            p_data = i.packet

            if i.message in (IMG_DATA, IMG_START, IMG_SIZE):
                ty = 'img'
                p_data = self.ir.push_data(i), self.ir.cur_img

            elif i.message in tlm_map:
                ty = 'tlm'
                p_data = data, p_data

            else:
                ty = 'raw'

            yield ty, self.get_sender_callsign(data), '0x%04X' % i.message, p_data
