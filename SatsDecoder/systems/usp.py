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
PSU_REGULAR5 = 0x0085
ACK = 0x0118
NACK = 0x0119
INFO = 0x011A
REGULAR_TEMPERATURE = 0x0440
GET_PAYLOAD_TELEMETRY = 0x0A00
RATESENS_REGULAR_X = 0x0B10
RATESENS_REGULAR_Y = 0x0B11
RATESENS_REGULAR_Z = 0x0B12
MAGNSENS_REGULAR_X = 0x0B13
MAGNSENS_REGULAR_Y = 0x0B14
MAGNSENS_REGULAR_Z = 0x0B15
VECTOR_X = 0x0B21
VECTOR_Y = 0x0B22
VECTOR_Z = 0x0B23
BRIGHTNESS = 0x0B24
COMMON_TELEMETRY = 0x0BF3
VHF_SETTINGS = 0x4201
BEACON = 0x4216
EXTENDED_BEACON = 0x4217
TIME_REQUEST = 0x421A
UHF_BEACON = 0x4246
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
ACKNOWLEDGE = 0xDE24
OVERCURRENT = 0xDE25
SWITCH_STATUS = 0xDE27
REGULAR_TELEMETRY6U = 0xDF25
PS_REGULAR_TELEMETRY_5CH = 0xED21
TM_ADCS_BEACON_OLD = 0xF204
TM_ADCS_BEACON = 0xF210
TM_ADCS_BEACON_6_WHEELS = 0xF212
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
FILETRANSFER_INIT = 0x0C20
FILETRANSFER_FILESIZE = 0x0C2B
FILETRANSFER_DATA = 0x0C24


# tlm
# 0x000E
regular_common_flags0 = construct.BitStruct(
    'current_invalid' / construct.Flag,  # Current invalid
    'voltage_invalid' / construct.Flag,  # Voltage invalid
    '_reserved' / construct.BitsInteger(6),  # reserved
)
regular_common = construct.Struct(
    '_name' / construct.Computed('regular_common'),
    'name' / construct.Computed('Regular common'),
    'desc' / construct.Computed('Common current and voltage telemetry'),
    'current' / construct.Int16sl,  # Current, mA
    'voltage' / construct.Int16sl,  # Voltage, mV
    'flags0' / regular_common_flags0,
)

# 0x000F
regular_x_flags0 = construct.BitStruct(
    'current_invalid' / construct.Flag,  # Current invalid
    'voltage_invalid' / construct.Flag,  # Voltage invalid
    '_reserved' / construct.BitsInteger(6),  # reserved
)
regular_x = construct.Struct(
    '_name' / construct.Computed('regular_x'),
    'name' / construct.Computed('Regular X'),
    'desc' / construct.Computed('Current and voltage telemetry, X-axis'),
    'current' / construct.Int16sl,  # Current, mA
    'voltage' / construct.Int16sl,  # Voltage, mV
    'flags0' / regular_x_flags0,
)

# 0x0010
regular_y_flags0 = construct.BitStruct(
    'current_invalid' / construct.Flag,  # Current invalid
    'voltage_invalid' / construct.Flag,  # Voltage invalid
    '_reserved' / construct.BitsInteger(6),  # reserved
)
regular_y = construct.Struct(
    '_name' / construct.Computed('regular_y'),
    'name' / construct.Computed('Regular Y'),
    'desc' / construct.Computed('Current and voltage telemetry, Y-axis'),
    'current' / construct.Int16sl,  # Current, mA
    'voltage' / construct.Int16sl,  # Voltage, mV
    'flags0' / regular_y_flags0,
)

# 0x0011
regular_z_flags0 = construct.BitStruct(
    'current_invalid' / construct.Flag,  # Current invalid
    'voltage_invalid' / construct.Flag,  # Voltage invalid
    '_reserved' / construct.BitsInteger(6),  # reserved
)
regular_z = construct.Struct(
    '_name' / construct.Computed('regular_z'),
    'name' / construct.Computed('Regular Z'),
    'desc' / construct.Computed('Current and voltage telemetry, Z-axis'),
    'current' / construct.Int16sl,  # Current, mA
    'voltage' / construct.Int16sl,  # Voltage, mV
    'flags0' / regular_z_flags0,
)

# 0x0080
psu_regular0_flags0 = construct.BitStruct(
    'current_invalid' / construct.Flag,  # Current invalid
    'voltage_invalid' / construct.Flag,  # Voltage invalid
    '_reserved' / construct.BitsInteger(6),  # reserved
)
psu_regular0 = construct.Struct(
    '_name' / construct.Computed('psu_regular0'),
    'name' / construct.Computed('PSU Regular #0'),
    'desc' / construct.Computed('LP-MCU 3.3V power\'s telemetry'),
    'current' / construct.Int16sl,  # Current, mA
    'voltage' / construct.Int16sl,  # Voltage, mV
    'flags0' / psu_regular0_flags0,
)

# 0x0081
psu_regular1_flags0 = construct.BitStruct(
    'current_invalid' / construct.Flag,  # Current invalid
    'voltage_invalid' / construct.Flag,  # Voltage invalid
    '_reserved' / construct.BitsInteger(6),  # reserved
)
psu_regular1 = construct.Struct(
    '_name' / construct.Computed('psu_regular1'),
    'name' / construct.Computed('PSU Regular #1'),
    'desc' / construct.Computed('Raspberry 3.3V power\'s telemetry'),
    'current' / construct.Int16sl,  # Current, mA
    'voltage' / construct.Int16sl,  # Voltage, mV
    'flags0' / psu_regular1_flags0,
)

# 0x0082
psu_regular2_flags0 = construct.BitStruct(
    'current_invalid' / construct.Flag,  # Current invalid
    'voltage_invalid' / construct.Flag,  # Voltage invalid
    '_reserved' / construct.BitsInteger(6),  # reserved
)
psu_regular2 = construct.Struct(
    '_name' / construct.Computed('psu_regular2'),
    'name' / construct.Computed('PSU Regular #2'),
    'desc' / construct.Computed('Raspberry 1.8V power\'s telemetry'),
    'current' / construct.Int16sl,  # Current, mA
    'voltage' / construct.Int16sl,  # Voltage, mV
    'flags0' / psu_regular2_flags0,
)

# 0x0083
psu_regular3_flags0 = construct.BitStruct(
    'current_invalid' / construct.Flag,  # Current invalid
    'voltage_invalid' / construct.Flag,  # Voltage invalid
    '_reserved' / construct.BitsInteger(6),  # reserved
)
psu_regular3 = construct.Struct(
    '_name' / construct.Computed('psu_regular3'),
    'name' / construct.Computed('PSU Regular #3'),
    'desc' / construct.Computed('Raspberry 5.0V power\'s telemetry'),
    'current' / construct.Int16sl,  # Current, mA
    'voltage' / construct.Int16sl,  # Voltage, mV
    'flags0' / psu_regular3_flags0,
)

# 0x0084
psu_regular4_flags0 = construct.BitStruct(
    'current_invalid' / construct.Flag,  # Current invalid
    'voltage_invalid' / construct.Flag,  # Voltage invalid
    '_reserved' / construct.BitsInteger(6),  # reserved
)
psu_regular4 = construct.Struct(
    '_name' / construct.Computed('psu_regular4'),
    'name' / construct.Computed('PSU Regular #4'),
    'desc' / construct.Computed('Sun sensors power\'s telemetry'),
    'current' / construct.Int16sl,  # Current, mA
    'voltage' / construct.Int16sl,  # Voltage, mV
    'flags0' / psu_regular4_flags0,
)

# 0x0085
psu_regular5_flags0 = construct.BitStruct(
    'current_invalid' / construct.Flag,  # Current invalid
    'voltage_invalid' / construct.Flag,  # Voltage invalid
    '_reserved' / construct.BitsInteger(6),  # reserved
)
psu_regular5 = construct.Struct(
    '_name' / construct.Computed('psu_regular5'),
    'name' / construct.Computed('PSU Regular #5'),
    'desc' / construct.Computed('ADCS MCU 3.3V power\'s telemetry'),
    'current' / construct.Int16sl,  # Current, mA
    'voltage' / construct.Int16sl,  # Voltage, mV
    'flags0' / psu_regular5_flags0,
)

# 0x0118
ack = construct.Struct(
    '_name' / construct.Computed('ack'),
    'name' / construct.Computed('ACK'),
    'desc' / construct.Computed('Successful command confirmation'),
    'value' / construct.Hex(construct.Int16ul),  # Value
)

# 0x0119
nack = construct.Struct(
    '_name' / construct.Computed('nack'),
    'name' / construct.Computed('NACK'),
    'desc' / construct.Computed('Command error'),
    'value' / construct.Hex(construct.Int16ul),  # Value
)

# 0x011A
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

# 0x0440
regular_temperature_flags0 = construct.BitStruct(
    'temperature0_invalid' / construct.Flag,  # temperature0_invalid
    'temperature1_invalid' / construct.Flag,  # temperature1_invalid
    '_pad0' / construct.BitsInteger(6),
)
regular_temperature = construct.Struct(
    '_name' / construct.Computed('regular_temperature'),
    'name' / construct.Computed('Regular Temperature'),
    'desc' / construct.Computed('Temperature telemetry'),
    'temperature0' / construct.Int8sl,  # temperature0
    'temperature1' / construct.Int8sl,  # temperature1
    'flags0' / regular_temperature_flags0,
)

# 0x0A00
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

# 0x0B10
ratesens_regular_x_flags0 = construct.BitStruct(
    'counter' / construct.BitsInteger(7),  # Counter - the number of the logical link of messages.
    'invalid' / construct.Flag,  # Invalid flag.
)
ratesens_regular_x = construct.Struct(
    '_name' / construct.Computed('ratesens_regular_x'),
    'name' / construct.Computed('Ratesens regular X'),
    'desc' / construct.Computed('X-axis VMS data'),
    'velocity' / construct.Float32l,  # Value
    'temperature' / construct.Int8sl,  # Value
    'flags0' / ratesens_regular_x_flags0,
)

# 0x0B11
ratesens_regular_y_flags0 = construct.BitStruct(
    'counter' / construct.BitsInteger(7),  # Counter - the number of the logical link of messages.
    'invalid' / construct.Flag,  # Invalid flag.
)
ratesens_regular_y = construct.Struct(
    '_name' / construct.Computed('ratesens_regular_y'),
    'name' / construct.Computed('Ratesens regular Y'),
    'desc' / construct.Computed('Y-axis VMS data'),
    'velocity' / construct.Float32l,  # Value
    'temperature' / construct.Int8sl,  # Value
    'flags0' / ratesens_regular_y_flags0,
)

# 0x0B12
ratesens_regular_z_flags0 = construct.BitStruct(
    'counter' / construct.BitsInteger(7),  # Counter - the number of the logical link of messages.
    'invalid' / construct.Flag,  # Invalid flag.
)
ratesens_regular_z = construct.Struct(
    '_name' / construct.Computed('ratesens_regular_z'),
    'name' / construct.Computed('Ratesens regular Z'),
    'desc' / construct.Computed('Z-axis VMS data'),
    'velocity' / construct.Float32l,  # Value
    'temperature' / construct.Int8sl,  # Value
    'flags0' / ratesens_regular_z_flags0,
)

# 0x0B13
magnsens_regular_x_flags0 = construct.BitStruct(
    'counter' / construct.BitsInteger(7),  # Counter - the number of the logical link of messages.
    'invalid' / construct.Flag,  # Invalid flag.
)
magnsens_regular_x = construct.Struct(
    '_name' / construct.Computed('magnsens_regular_x'),
    'name' / construct.Computed('Magnsens regular X'),
    'desc' / construct.Computed('X-axis magnetometer data'),
    'field' / construct.Float32l,  # Value
    'temperature' / construct.Int8sl,  # Value
    'flags0' / magnsens_regular_x_flags0,
)

# 0x0B14
magnsens_regular_y_flags0 = construct.BitStruct(
    'counter' / construct.BitsInteger(7),  # Counter - the number of the logical link of messages.
    'invalid' / construct.Flag,  # Invalid flag.
)
magnsens_regular_y = construct.Struct(
    '_name' / construct.Computed('magnsens_regular_y'),
    'name' / construct.Computed('Magnsens regular Y'),
    'desc' / construct.Computed('Y-axis magnetometer data'),
    'field' / construct.Float32l,  # Value
    'temperature' / construct.Int8sl,  # Value
    'flags0' / magnsens_regular_y_flags0,
)

# 0x0B15
magnsens_regular_z_flags0 = construct.BitStruct(
    'counter' / construct.BitsInteger(7),  # Counter - the number of the logical link of messages.
    'invalid' / construct.Flag,  # Invalid flag.
)
magnsens_regular_z = construct.Struct(
    '_name' / construct.Computed('magnsens_regular_z'),
    'name' / construct.Computed('Magnsens regular Z'),
    'desc' / construct.Computed('Z-axis magnetometer data'),
    'field' / construct.Float32l,  # Value
    'temperature' / construct.Int8sl,  # Value
    'flags0' / magnsens_regular_z_flags0,
)

# 0x0B21
Vector_X_flags0 = construct.BitStruct(
    'invalid' / construct.Flag,  # Данные актуальны
    '_Reserv' / construct.BitsInteger(7),  # _Reserv
)
Vector_X = construct.Struct(
    '_name' / construct.Computed('Vector_X'),
    'name' / construct.Computed('Vector X'),
    'desc' / construct.Computed('X-axis regular telemetry'),
    'vector' / construct.Int32sl,  # Направление по X, град
    'temperature' / construct.Int8sl,  # Температура, градусы Цельсия
    'flags0' / Vector_X_flags0,
)

# 0x0B22
Vector_Y_flags0 = construct.BitStruct(
    'invalid' / construct.Flag,  # Данные актуальны
    '_Reserv' / construct.BitsInteger(7),  # _Reserv
)
Vector_Y = construct.Struct(
    '_name' / construct.Computed('Vector_Y'),
    'name' / construct.Computed('Vector Y'),
    'desc' / construct.Computed('Y-axis regular telemetry'),
    'vector' / construct.Int32sl,  # Направление по Y, град
    'temperature' / construct.Int8sl,  # Температура, градусы Цельсия
    'flags0' / Vector_Y_flags0,
)

# 0x0B23
Vector_Z_flags0 = construct.BitStruct(
    'invalid' / construct.Flag,  # Данные актуальны
    '_Reserv' / construct.BitsInteger(7),  # _Reserv
)
Vector_Z = construct.Struct(
    '_name' / construct.Computed('Vector_Z'),
    'name' / construct.Computed('Vector Z'),
    'desc' / construct.Computed('Z-axis regular telemetry'),
    'vector' / construct.Int32sl,  # Направление по Z, град
    'temperature' / construct.Int8sl,  # Температура, градусы Цельсия
    'flags0' / Vector_Z_flags0,
)

# 0x0B24
Brightness = construct.Struct(
    '_name' / construct.Computed('Brightness'),
    'name' / construct.Computed('Brightness'),
    'desc' / construct.Computed('Total brightness regular telemetry'),
    'Sum' / construct.Float32l,  # Суммарная яркость каналов
    '_Reserved' / construct.BitsInteger(16),  # Резерв
)

# 0x0BF3
common_telemetry = construct.Struct(
    '_name' / construct.Computed('common_telemetry'),
    'name' / construct.Computed('Common telemetry'),
    'desc' / construct.Computed('Common one-time telemetry (issued on request) (tested)'),
    'Data' / construct.Bytes(48),  # Data
)

# 0x4201
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
    'CallSign' / construct.PaddedString(56, 'utf-8'),  # CallSign
    'SSID' / construct.Int8ul,  # SSID
    'EarthCallSign' / construct.PaddedString(56, 'utf-8'),  # EarthCallSign
    'EarthSSID' / construct.Int8ul,  # EarthSSID
    'TLocation' / construct.Int8ul,  # TLocation
    'UNIcanID' / construct.Int16ul,  # UNIcanID
    'EnableBridge' / construct.Int8ul,  # EnableBridge
    'BeaconStartupDelay' / construct.Int16ul,  # BeaconStartupDelay
)

# 0x4216
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
    '_reserved0' / construct.BitsInteger(3),  # Резерв
    'Additional_channel_3_on' / construct.Flag,  # Флаг включения дополнительного канала 3
    'Additional_channel_2_on' / construct.Flag,  # Флаг включения дополнительного канала 2
    'Additional_channel_1_on' / construct.Flag,  # Флаг включения дополнительного канала 1
    'FSB' / construct.Flag,  # Флаг ошибки коммутатора
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
    'FL' / construct.Hex(construct.Int8ul),  # Флаги PS.
    't_amp' / construct.Int8sl,  # Температура усилителя УКВ (гр. С)
    't_uhf' / construct.Int8sl,  # Температура УКВ (гр. С)
    'RSSIrx' / common.LinearAdapter(-1, construct.Int8ul),  # RSSI при приеме
    'RSSIidle' / common.LinearAdapter(-1, construct.Int8ul),  # RSSI в ожидании
    'Pf' / construct.Int8sl,  # Мощность прямого излучения
    'Pb' / construct.Int8sl,  # Мощность обратного излучения
    'Nres_uhf' / construct.Int8ul,  # Количество перезагрузок УКВ
    'FL_uhf' / construct.Hex(construct.Int8ul),  # Флаги УКВ
    'Time_uhf' / common.UNIXTimestampAdapter(construct.Int32sl),  # Время последней телеметрии УКВ
    'UpTime' / TimeDeltaAdapter(construct.Int32ul),  # Uptime в секундах
    'Current' / construct.Int16ul,  # Ток потребления УКВ
    'Uuhf' / construct.Int16sl,  # Напряжение УКВ (мВ)
)

# 0x4217
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

# 0x421A
time_request = construct.Struct(
    '_name' / construct.Computed('time_request'),
    'name' / construct.Computed('TIME_REQUEST'),
    'desc' / construct.Computed('Acknowledge of completed data transmission'),
)

# 0x4246
uhf_beacon_flags0 = construct.BitStruct(
    'NumActiveSchedules' / construct.BitsInteger(5),  # Number of Active Schedules in executor.
    'ResetOccurredDuringExecution' / construct.Flag,  # Reboot occurred during schedule execution.
    'BackupScheduleActive' / construct.Flag,  # Backup schedule execution in progress.
    '_Reserved' / construct.Flag,  # Value
)
uhf_beacon = construct.Struct(
    '_name' / construct.Computed('uhf_beacon'),
    'name' / construct.Computed('UHF Beacon'),
    'desc' / construct.Computed('UHF Beacon'),
    't_amp' / construct.Int8sl,  # UHF amp temperature, °C
    't_uhf' / construct.Int8sl,  # UHF temperature, °C
    'RSSIrx' / common.LinearAdapter(-1, construct.Int8ul),  # RX RSSI (-dBm)
    'RSSIidle' / common.LinearAdapter(-1, construct.Int8ul),  # idle RSSI (-dBm)
    'Pf' / construct.Int8sl,  # Forward wave power(dBm)
    'Pb' / construct.Int8sl,  # Reflected wave power(dBm)
    'uhf_reset_counter' / construct.Int8ul,  # UHF reset counter
    'FL' / construct.Hex(construct.Int8ul),  # UHF flags
    'Time' / common.UNIXTimestampAdapter(construct.Int32sl),  # UHF timestamp
    'UpTime' / TimeDeltaAdapter(construct.Int32ul),  # Uptime(sec)
    'RxBitrate' / construct.Int32ul,  # Uplink bitrate (Receive)
    'CurrentConsumption' / construct.Int16ul,  # UHF consumption current
    'InputVoltage' / construct.Int16sl,  # UHF voltage(mV)
    'flags0' / uhf_beacon_flags0,
)

# 0x5430
detector_transmits = construct.Struct(
    '_name' / construct.Computed('detector_transmits'),
    'name' / construct.Computed('DETECTOR_TRANSMITS'),
    'desc' / construct.Computed('Detector mod data'),
)

# 0x5439
data_massive_addr_rpl = construct.Struct(
    '_name' / construct.Computed('data_massive_addr_rpl'),
    'name' / construct.Computed('DATA_MASSIVE_ADDR_RPL'),
    'desc' / construct.Computed('Massive addr mod data'),
)

# 0x543A
data_event_addr_rpl = construct.Struct(
    '_name' / construct.Computed('data_event_addr_rpl'),
    'name' / construct.Computed('DATA_EVENT_ADDR_RPL'),
    'desc' / construct.Computed('Event addr mod data'),
)

# 0x543B
data_monitor_addr_rpl = construct.Struct(
    '_name' / construct.Computed('data_monitor_addr_rpl'),
    'name' / construct.Computed('DATA_MONITOR_ADDR_RPL'),
    'desc' / construct.Computed('Monitor addr mod data'),
)

# 0x543C
data_massive_rpl = construct.Struct(
    '_name' / construct.Computed('data_massive_rpl'),
    'name' / construct.Computed('DATA_MASSIVE_RPL'),
    'desc' / construct.Computed('Massive mod data'),
)

# 0x543D
data_event_rpl = construct.Struct(
    '_name' / construct.Computed('data_event_rpl'),
    'name' / construct.Computed('DATA_EVENT_RPL'),
    'desc' / construct.Computed('Event mod ata'),
)

# 0x543E
data_monitor_rpl = construct.Struct(
    '_name' / construct.Computed('data_monitor_rpl'),
    'name' / construct.Computed('DATA_MONITOR_RPL'),
    'desc' / construct.Computed('Monitor mod data'),
)

# 0xABD1
get_Payload_FW_MSG = construct.Struct(
    '_name' / construct.Computed('get_Payload_FW_MSG'),
    'name' / construct.Computed('Payload FW MSG'),
    'desc' / construct.Computed('Payload FW MSG'),
    'Modification' / construct.Int8ul,  # Modification
    'Version' / construct.Int8ul,  # Version
    'Release_Number' / construct.Int8ul,  # Release Number
)

# 0xABD4
no_monitor_data = construct.Struct(
    '_name' / construct.Computed('no_monitor_data'),
    'name' / construct.Computed('NO_MONITOR_DATA'),
    'desc' / construct.Computed('There is no enought corresponding data'),
)

# 0xABD5
no_event_data = construct.Struct(
    '_name' / construct.Computed('no_event_data'),
    'name' / construct.Computed('NO_EVENT_DATA'),
    'desc' / construct.Computed('There is no enought corresponding data'),
)

# 0xABD6
no_massive_data = construct.Struct(
    '_name' / construct.Computed('no_massive_data'),
    'name' / construct.Computed('NO_MASSIVE_DATA'),
    'desc' / construct.Computed('There is no enought corresponding data'),
)

# 0xABD9
compl_monitor_data = construct.Struct(
    '_name' / construct.Computed('compl_monitor_data'),
    'name' / construct.Computed('COMPL_MONITOR_DATA'),
    'desc' / construct.Computed('Acknowledge of completed data transmission'),
)

# 0xABDA
compl_event_data = construct.Struct(
    '_name' / construct.Computed('compl_event_data'),
    'name' / construct.Computed('COMPL_EVENT_DATA'),
    'desc' / construct.Computed('Acknowledge of completed data transmission'),
)

# 0xABDB
compl_massive_data = construct.Struct(
    '_name' / construct.Computed('compl_massive_data'),
    'name' / construct.Computed('COMPL_MASSIVE_DATA'),
    'desc' / construct.Computed('Acknowledge of completed data transmission'),
)

# 0xABDD
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

# 0xDE21
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
    'desc' / construct.Computed('PSS Regular telemetry'),
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

# 0xDE22
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
    'DEPLOY_START_TIMER' / construct.Int16ul,  # Value
    'DEPLOY_STOP_TIMER' / construct.Int8ul,  # Value
    'DEPLOY_MODE' / construct.Hex(construct.Int8ul),  # Value
)

# 0xDE24
acknowledge = construct.Struct(
    '_name' / construct.Computed('acknowledge'),
    'name' / construct.Computed('Acknowledge'),
    'desc' / construct.Computed('Command acceptence confirmation'),
)

# 0xDE25
overcurrent = construct.Struct(
    '_name' / construct.Computed('overcurrent'),
    'name' / construct.Computed('Overcurrent'),
    'desc' / construct.Computed('Overcurrent'),
    'Channel' / construct.Int8ul,  # Номер канала
)

# 0xDE27
switch_status = construct.Struct(
    '_name' / construct.Computed('switch_status'),
    'name' / construct.Computed('Switch status'),
    'desc' / construct.Computed('Switch status'),
    'Ch0Status' / construct.Hex(construct.Int16ul),  # Статус канала 0
    'Ch1Status' / construct.Hex(construct.Int16ul),  # Статус канала 1
    'Ch2Status' / construct.Hex(construct.Int16ul),  # Статус канала 2
    'Ch3Status' / construct.Hex(construct.Int16ul),  # Статус канала 3
)

# 0xDF25
regular_telemetry6u_flags0 = construct.BitStruct(
    'ch1_status' / construct.Flag,  # Value
    'ch2_status' / construct.Flag,  # Value
    'ch3_status' / construct.Flag,  # Value
    'ch4_status' / construct.Flag,  # Value
    'ch5_status' / construct.Flag,  # Value
    'ch6_status' / construct.Flag,  # Value
    'ch7_status' / construct.Flag,  # Value
    'ch8_status' / construct.Flag,  # Value
    'ch9_status' / construct.Flag,  # Value
    'ch10_status' / construct.Flag,  # Value
    'ch11_status' / construct.Flag,  # Value
    'ch12_status' / construct.Flag,  # Value
    'ch13_status' / construct.Flag,  # Value
    'ch14_status' / construct.Flag,  # Value
    'ch15_status' / construct.Flag,  # Value
    'ch16_status' / construct.Flag,  # Value
    'ch17_status' / construct.Flag,  # Value
    'ch18_status' / construct.Flag,  # Value
    'ch19_status' / construct.Flag,  # Value
    'ch20_status' / construct.Flag,  # Value
    'ch21_status' / construct.Flag,  # Value
    'ch22_status' / construct.Flag,  # Value
    'ch23_status' / construct.Flag,  # Value
    'ch24_status' / construct.Flag,  # Value
    'ch25_status' / construct.Flag,  # Value
    'ch26_status' / construct.Flag,  # Value
    'ch27_status' / construct.Flag,  # Value
    'ch28_status' / construct.Flag,  # Value
    'ch29_status' / construct.Flag,  # Value
    'ch30_status' / construct.Flag,  # Value
    '_reserved' / construct.BitsInteger(2),  # Value
    'Tab_min' / construct.Flag,  # none
    'Tab_max' / construct.Flag,  # none
    'heater1_on' / construct.Flag,  # none
    'heater2_on' / construct.Flag,  # none
    'heater1_manual' / construct.Flag,  # none
    'heater2_manual' / construct.Flag,  # none
    'Uab_min' / construct.Flag,  # none
    'Uab_crit' / construct.Flag,  # none
    'Ich_limit1' / construct.Flag,  # none
    'Ich_limit2' / construct.Flag,  # none
    'Ich_limit3' / construct.Flag,  # none
    'Ich_limit4' / construct.Flag,  # none
    'channelon1' / construct.Flag,  # none
    'channelon2' / construct.Flag,  # none
    'channelon3' / construct.Flag,  # none
    'channelon4' / construct.Flag,  # none
    'charger' / construct.Flag,  # none
    'FSB' / construct.Flag,  # Power switch error.
    'AuxCH1_enabled_flag' / construct.Flag,  # Additional_channel_1_on.
    'AuxCH2_enabled_flag' / construct.Flag,  # Additional_channel_2_on.
    'AuxCH3_enabled_flag' / construct.Flag,  # Additional_channel_3_on.
    '_reserved0' / construct.BitsInteger(3),  # Reserved.
    '_reserved1' / construct.BitsInteger(8),  # Reserved.
)
regular_telemetry6u = construct.Struct(
    '_name' / construct.Computed('Regular_telemetry6U'),
    'name' / construct.Computed('Regular telemetry 6U'),
    'desc' / construct.Computed('Regular_telemetry6U'),
    'Usb1' / construct.Int16ul,  # Solar Panel 1 Voltage(mV)
    'Usb2' / construct.Int16ul,  # Solar Panel 2 Voltage(mV)
    'Usb3' / construct.Int16ul,  # Solar Panel 3 Voltage(mV)
    'Isb1' / construct.Int16ul,  # Solar Panel 1 Current(mA)
    'Isb2' / construct.Int16ul,  # Solar Panel 2 Current(mA)
    'Isb3' / construct.Int16ul,  # Solar Panel 3 Current(mA)
    'Iab' / construct.Int16sl,  # Battery Current(mA)
    'Uab' / construct.Int16ul,  # Voltage on cell 1.
    'Uab1' / construct.Int16ul,  # Voltage on cell 1.
    'Uab2' / construct.Int16ul,  # Voltage on cell 2.
    't1_pw' / RegTemp,  # Battery temperature 1(deg. С)
    't2_pw' / RegTemp,  # Battery temperature 2(deg. С)
    'capacity' / construct.Int8ul,  # Value
    'flags0' / regular_telemetry6u_flags0,
    'reg_tel_id' / construct.Int32ul,  # PSS telemetry number.
    'Time' / common.UNIXTimestampAdapter(construct.Int32sl),  # PSS last telemetry timestamp.
    'ps_reset_counter' / construct.Int8ul,  # PSS reset counter.
    'FL' / construct.Hex(construct.Int8ul),  # PS flags.
)

# 0xED21
ps_regular_telemetry_5ch_flags0 = construct.BitStruct(
    'Tab_min' / construct.Flag,  # none
    'Tab_max' / construct.Flag,  # none
    'heater1_on' / construct.Flag,  # none
    'heater2_on' / construct.Flag,  # none
    'heater1_manual' / construct.Flag,  # none
    'heater2_manual' / construct.Flag,  # none
    'Uab_min' / construct.Flag,  # none
    'Uab_crit' / construct.Flag,  # none
    'Ich_limit1' / construct.Flag,  # none
    'Ich_limit2' / construct.Flag,  # none
    'Ich_limit3' / construct.Flag,  # none
    'Ich_limit4' / construct.Flag,  # none
    'Ich_limit5' / construct.Flag,  # none
    'channelon1' / construct.Flag,  # none
    'channelon2' / construct.Flag,  # none
    'channelon3' / construct.Flag,  # none
    'channelon4' / construct.Flag,  # none
    'channelon5' / construct.Flag,  # none
    'charger' / construct.Flag,  # none
    'FSB' / construct.Flag,  # Power switch error.
    'AuxCH1_enabled_flag' / construct.Flag,  # Additional_channel_1_on.
    'AuxCH2_enabled_flag' / construct.Flag,  # Additional_channel_2_on.
    'AuxCH3_enabled_flag' / construct.Flag,  # Additional_channel_3_on.
    '_reserved0' / construct.Flag,  # Reserved.
    '_reserved1' / construct.BitsInteger(8),  # Reserved.
)
ps_regular_telemetry_5ch = construct.Struct(
    '_name' / construct.Computed('ps_regular_telemetry_5ch'),
    'name' / construct.Computed('PS Regular telemetry 5ch'),
    'desc' / construct.Computed('Regular telemetry for PSS with 5 ch'),
    'VTG_SOL1' / construct.Int16ul,  # Solar Panel 1 Voltage(mV)
    'VTG_SOL2' / construct.Int16ul,  # Solar Panel 2 Voltage(mV)
    'VTG_SOL3' / construct.Int16ul,  # Solar Panel 3 Voltage(mV)
    'CUR_SOL1' / construct.Int16ul,  # Solar Panel 1 Current(mA)
    'CUR_SOL2' / construct.Int16ul,  # Solar Panel 2 Current(mA)
    'CUR_SOL3' / construct.Int16ul,  # Solar Panel 3 Current(mA)
    'CUR_BAT' / construct.Int16sl,  # Battery Current(mA)
    'CUR_PCH1' / construct.Int16ul,  # Channel 1 Current(mA)
    'CUR_PCH2' / construct.Int16ul,  # Channel 2 Current(mA)
    'CUR_PCH3' / construct.Int16ul,  # Channel 3 Current(mA)
    'CUR_PCH4' / construct.Int16ul,  # Channel 4 Current(mA)
    'CUR_PCH5' / construct.Int16ul,  # Channel 5 Current(mA)
    'TMP_BAT1' / RegTemp,  # Battery temperature 1(deg. С)
    'TMP_BAT2' / RegTemp,  # Battery temperature 2(deg. С)
    'TMP_BAT3' / RegTemp,  # Battery temperature 3(deg. С)
    'TMP_BAT4' / RegTemp,  # Battery temperature 4(deg. С)
    'flags0' / ps_regular_telemetry_5ch_flags0,
    'VBAT' / construct.Int16sl,  # Battery voltage(mV)
    'REC_ID' / construct.Int32ul,  # PSS telemetry number.
    'Time' / common.UNIXTimestampAdapter(construct.Int32sl),  # PSS last telemetry timestamp.
    'ps_reset_counter' / construct.Int8ul,  # PSS reset counter.
    'reset_reason' / construct.Hex(construct.Int8ul),  # PS flags.
)

# 0xF204
_tm_adcs_beacon_old_policies = construct.Hex(construct.Enum(construct.BitsInteger(7), **{'None': 0, 'Integrator': 1, 'Integrator AVS shifts': 2, 'Triad': 3, 'Triad AVS shifts': 4, 'Kalman BWS': 5, 'Star tracker': 6, 'Star_tracker AVS shifts': 7, 'Kalman Q': 8, 'Kalman WQ': 9}))
tm_adcs_beacon_old_flags0 = construct.BitStruct(
    'eci_policy' / _tm_adcs_beacon_old_policies,
    'eci_invalid' / construct.Flag,  # Value
)
tm_adcs_beacon_old_flags1 = construct.BitStruct(
    'orb_policy' / _tm_adcs_beacon_old_policies,
    'orb_invalid' / construct.Flag,  # Value
)
tm_adcs_beacon_old_flags2 = construct.BitStruct(
    'forced_policy' / _tm_adcs_beacon_old_policies,
    'forced_invalid' / construct.Flag,  # Value
)
tm_adcs_beacon_old_flags3 = construct.BitStruct(
    'mfs_invalid' / construct.Flag,  # Value
    'avs_invalid' / construct.Flag,  # Value
    '_reserved' / construct.BitsInteger(6),  # Value
)
tm_adcs_beacon_old = construct.Struct(
    '_name' / construct.Computed('tm_adcs_beacon_old'),
    'name' / construct.Computed('TM ADCS beacon old'),
    'desc' / construct.Computed('TM ADCS beacon old'),
    'Time' / common.UNIXTimestampAdapter(construct.Int64sl),  # Value
    'eci_quat_w' / construct.Float32l,  # Value
    'eci_quat_vect_x' / construct.Float32l,  # Value
    'eci_quat_vect_y' / construct.Float32l,  # Value
    'eci_quat_vect_z' / construct.Float32l,  # Value
    'eci_ave_x' / construct.Float32l,  # Value
    'eci_ave_y' / construct.Float32l,  # Value
    'eci_ave_z' / construct.Float32l,  # Value
    'flags0' / tm_adcs_beacon_old_flags0,
    'orb_time' / common.UNIXTimestampAdapter(construct.Int64sl),  # Value
    'orb_quat_w' / construct.Float32l,  # Value
    'orb_quat_vect_x' / construct.Float32l,  # Value
    'orb_quat_vect_y' / construct.Float32l,  # Value
    'orb_quat_vect_z' / construct.Float32l,  # Value
    'orb_ave_x' / construct.Float32l,  # Value
    'orb_ave_y' / construct.Float32l,  # Value
    'orb_ave_z' / construct.Float32l,  # Value
    'flags1' / tm_adcs_beacon_old_flags1,
    'forced_time' / common.UNIXTimestampAdapter(construct.Int64sl),  # Value
    'forced_quat_w' / construct.Float32l,  # Value
    'forced_quat_vect_x' / construct.Float32l,  # Value
    'forced_quat_vect_y' / construct.Float32l,  # Value
    'forced_quat_vect_z' / construct.Float32l,  # Value
    'forced_ave_x' / construct.Float32l,  # Value
    'forced_ave_y' / construct.Float32l,  # Value
    'forced_ave_z' / construct.Float32l,  # Value
    'flags2' / tm_adcs_beacon_old_flags2,
    'ss_invalids' / construct.Int16ul,  # Value
    'wheel_invalids' / construct.Int8ul,  # Value
    'flags3' / tm_adcs_beacon_old_flags3,
)

# 0xF210
_tm_adcs_beacon_policies = construct.Hex(construct.Enum(construct.BitsInteger(7), **{'None': 0, 'Integrator': 1, 'Integrator + AV shifts': 2, 'Triad': 3, 'Triad + AV shifts': 4, 'Kalman BWS': 5, 'Star tracker': 6, 'Star tracker + AV shifts': 7, 'Kalman Q': 8, 'Kalman WQ': 9, 'Kalman WQP': 10}))
tm_adcs_beacon_flags0 = construct.BitStruct(
    'eci_policy' / _tm_adcs_beacon_policies,
    'eci_invalid' / construct.Flag,  # Invalidity flag.
)
tm_adcs_beacon_flags1 = construct.BitStruct(
    'orb_policy' / _tm_adcs_beacon_policies,
    'orb_invalid' / construct.Flag,  # Invalidity flag.
)
tm_adcs_beacon_flags2 = construct.BitStruct(
    'eci_forced_policy' / _tm_adcs_beacon_policies,
    'eci_forced_invalid' / construct.Flag,  # Invalidity flag.
)
tm_adcs_beacon_flags3 = construct.BitStruct(
    'ballistics_policy' / construct.Hex(construct.Enum(construct.BitsInteger(3), **{'Propagator': 0, 'GNSS': 1, 'GNSS + estimation by speed': 2})),
    'gnss_invalid' / construct.Flag,  # GNSS invalidity.
    'auto_ballistics_polity' / construct.Hex(construct.Enum(construct.BitsInteger(2), Disabled=0, Enabled=1)),  # Auto ballistics policy
    'auto_control_policy' / construct.Hex(construct.Enum(construct.BitsInteger(2), **{'Disabled': 0, 'Enabled set 1': 1, 'Enabled set 2': 2})),  # Set angular motion auto control policy
)
tm_adcs_beacon_flags4 = construct.BitStruct(
    'ss_active' / construct.BitsInteger(6),  # Active sun sensor.
    'ss_invalid_x_plus' / construct.Flag,  # Sun sensors invalidity flags.
    'ss_invalid_x_minus' / construct.Flag,  # Value
    'ss_invalid_y_plus' / construct.Flag,  # Value
    'ss_invalid_y_minus' / construct.Flag,  # Value
    'ss_invalid_z_plus' / construct.Flag,  # Value
    'ss_invalid_z_minus' / construct.Flag,  # Value
    'ss_invalid_extra' / construct.Flag,  # Value
    'star_tracker_invalid' / construct.Flag,  # Star tracker invalidity flag.
    'avs_invalid' / construct.Flag,  # AVS invalidity flag.
    'mfs_invalid' / construct.Flag,  # MFS invalidity flag.
    'wheel_invalid_x_plus' / construct.Flag,  # Wheels invalidity flags.
    'wheel_invalid_x_minus' / construct.Flag,  # Value
    'wheel_invalid_y_plus' / construct.Flag,  # Value
    'wheel_invalid_y_minus' / construct.Flag,  # Value
    'reset_reason' / construct.Hex(construct.BitsInteger(4)),  # Last reset reason.
)
tm_adcs_beacon = construct.Struct(
    '_name' / construct.Computed('tm_adcs_beacon'),
    'name' / construct.Computed('TM ADCS beacon'),
    'desc' / construct.Computed('TM ADCS beacon'),
    'Time' / common.UNIXTimestampAdapter(construct.Int64sl),  # Current system time.
    'uptime' / TimeDeltaAdapter(construct.Int32ul),  # Time from last reboot, [sec].
    'eci_quat_w' / construct.Float32l,  # Value
    'eci_quat_vect_x' / construct.Float32l,  # Value
    'eci_quat_vect_y' / construct.Float32l,  # Value
    'eci_quat_vect_z' / construct.Float32l,  # Value
    'eci_AV_x' / construct.Float32l,  # Angular velocity, [deg/sec].
    'eci_AV_y' / construct.Float32l,  # Value
    'eci_AV_z' / construct.Float32l,  # Value
    'flags0' / tm_adcs_beacon_flags0,
    'orb_quat_w' / construct.Float32l,  # Value
    'orb_quat_vect_x' / construct.Float32l,  # Value
    'orb_quat_vect_y' / construct.Float32l,  # Value
    'orb_quat_vect_z' / construct.Float32l,  # Value
    'orb_AV_x' / construct.Float32l,  # Angular velocity, [deg/sec].
    'orb_AV_y' / construct.Float32l,  # Value
    'orb_AV_z' / construct.Float32l,  # Value
    'flags1' / tm_adcs_beacon_flags1,
    'eci_forced_quat_w' / construct.Float32l,  # Value
    'eci_forced_quat_vect_x' / construct.Float32l,  # Value
    'eci_forced_quat_vect_y' / construct.Float32l,  # Value
    'eci_forced_quat_vect_z' / construct.Float32l,  # Value
    'eci_forced_AV_x' / construct.Float32l,  # Angular velocity, [deg/sec].
    'eci_forced_AV_y' / construct.Float32l,  # Value
    'eci_forced_AV_z' / construct.Float32l,  # Value
    'flags2' / tm_adcs_beacon_flags2,
    'latitude' / construct.Float32l,  # Latitude, [deg].
    'longitude' / construct.Float32l,  # Longitude, [deg].
    'altitude' / construct.Float32l,  # Altitude, [m].
    'flags3' / tm_adcs_beacon_flags3,
    'adcs_task_type' / construct.Hex(construct.Enum(construct.Int8ul, **{'Idle': 0, 'B_dot': 1, 'Orientation ECI + unload wheels': 2, 'Orientation ORB + unload wheels': 3, 'Battery recharging': 4, 'Orientation ECI': 5, 'Orientation ORB': 6, 'Watch ECI point': 7, 'Watch LLA point': 8, 'Watch Sun': 9, 'None': 10})),  # Current task type
    'adcs_task_quantity' / construct.Int8ul,  # Tasks quantity in scheduler.
    'wheel_rpm_x_plus' / construct.Int16sl,  # Wheels angular velocities, [rpm].
    'wheel_rpm_x_minus' / construct.Int16sl,  # Value
    'wheel_rpm_y_plus' / construct.Int16sl,  # Value
    'wheel_rpm_y_minus' / construct.Int16sl,  # Value
    'flags4' / tm_adcs_beacon_flags4,
)

# 0xF212
tm_adcs_beacon_6_wheels_flags4 = construct.BitStruct(
    'ss_active' / construct.BitsInteger(6),  # Active sun sensor.
    'ss_invalid_x_plus' / construct.Flag,  # Sun sensors invalidity flags.
    'ss_invalid_x_minus' / construct.Flag,  # Value
    'ss_invalid_y_plus' / construct.Flag,  # Value
    'ss_invalid_y_minus' / construct.Flag,  # Value
    'ss_invalid_z_plus' / construct.Flag,  # Value
    'ss_invalid_z_minus' / construct.Flag,  # Value
    'ss_invalid_extra' / construct.Flag,  # Value
    'star_tracker_invalid' / construct.Flag,  # Star tracker invalidity flag.
    'avs_invalid' / construct.Flag,  # AVS invalidity flag.
    'mfs_invalid' / construct.Flag,  # MFS invalidity flag.
    'wheel_invalid_1' / construct.Flag,  # Wheels invalidity flags.
    'wheel_invalid_2' / construct.Flag,  # Value
    'wheel_invalid_3' / construct.Flag,  # Value
    'wheel_invalid_4' / construct.Flag,  # Value
    'wheel_invalid_5' / construct.Flag,  # Value
    'wheel_invalid_6' / construct.Flag,  # Value
    '_reserved' / construct.BitsInteger(2),  # Value
)
tm_adcs_beacon_6_wheels = construct.Struct(
    '_name' / construct.Computed('tm_adcs_beacon_6_wheels'),
    'name' / construct.Computed('TM ADCS beacon 6 wheels'),
    'desc' / construct.Computed('TM ADCS beacon 6 wheels'),
    'Time' / common.UNIXTimestampAdapter(construct.Int64sl),  # Current system time.
    'uptime' / TimeDeltaAdapter(construct.Int32ul),  # Time from last reboot, [sec].
    'eci_quat_w' / construct.Float32l,  # Value
    'eci_quat_vect_x' / construct.Float32l,  # Value
    'eci_quat_vect_y' / construct.Float32l,  # Value
    'eci_quat_vect_z' / construct.Float32l,  # Value
    'eci_AV_x' / construct.Float32l,  # Angular velocity, [deg/sec].
    'eci_AV_y' / construct.Float32l,  # Value
    'eci_AV_z' / construct.Float32l,  # Value
    'flags0' / tm_adcs_beacon_flags0,
    'orb_quat_w' / construct.Float32l,  # Value
    'orb_quat_vect_x' / construct.Float32l,  # Value
    'orb_quat_vect_y' / construct.Float32l,  # Value
    'orb_quat_vect_z' / construct.Float32l,  # Value
    'orb_AV_x' / construct.Float32l,  # Angular velocity, [deg/sec].
    'orb_AV_y' / construct.Float32l,  # Value
    'orb_AV_z' / construct.Float32l,  # Value
    'flags1' / tm_adcs_beacon_flags1,
    'eci_forced_quat_w' / construct.Float32l,  # Value
    'eci_forced_quat_vect_x' / construct.Float32l,  # Value
    'eci_forced_quat_vect_y' / construct.Float32l,  # Value
    'eci_forced_quat_vect_z' / construct.Float32l,  # Value
    'eci_forced_AV_x' / construct.Float32l,  # Angular velocity, [deg/sec].
    'eci_forced_AV_y' / construct.Float32l,  # Value
    'eci_forced_AV_z' / construct.Float32l,  # Value
    'flags2' / tm_adcs_beacon_flags2,
    'latitude' / construct.Float32l,  # Latitude, [deg].
    'longitude' / construct.Float32l,  # Longitude, [deg].
    'altitude' / construct.Float32l,  # Altitude, [m].
    'flags3' / tm_adcs_beacon_flags3,
    'adcs_task_type' / construct.Int8ul,  # Current task type. 0 - Idle, 1 - B_dot, 2 - Orientation ECI + unload wheels, 3 - Orientation ORB + unload wheels, 4 - Battery recharging, 5 - Orientation ECI, 6 - Orientation ORB, 7 - Watch ECI point, 8 - Watch LLA point, 9 - Watch Sun, 10 - None.
    'adcs_task_quantity' / construct.Int8ul,  # Tasks quantity in scheduler.
    'wheel_rpm_1' / construct.Int16sl,  # Wheels angular velocities, [rpm].
    'wheel_rpm_2' / construct.Int16sl,  # Value
    'wheel_rpm_3' / construct.Int16sl,  # Value
    'wheel_rpm_4' / construct.Int16sl,  # Value
    'wheel_rpm_5' / construct.Int16sl,  # Value
    'wheel_rpm_6' / construct.Int16sl,  # Value
    'flags4' / tm_adcs_beacon_6_wheels_flags4,
    'reset_reason' / construct.Hex(construct.Int8ul),  # Last reset reason.
)

# 0xFB21
ch_adc_X1 = construct.Struct(
    '_name' / construct.Computed('ch_adc_X1'),
    'name' / construct.Computed('ADC Ch#X1'),
    'desc' / construct.Computed('ADC data packet on detector channel X1'),
    'ADC_X1' / construct.Int32sl,  # Значение по каналу X1
    'Temp_Ext' / RegTemp,  # Температура датчика у детектора, градусы Цельсия * 100
)

# 0xFB22
ch_adc_X2 = construct.Struct(
    '_name' / construct.Computed('ch_adc_X2'),
    'name' / construct.Computed('ADC Ch#X2'),
    'desc' / construct.Computed('ADC data packet on detector channel X2'),
    'ADC_X2' / construct.Int32sl,  # Значение по каналу X2
    'Temp_Int' / RegTemp,  # Температура датчика МК, градусы Цельсия * 100
)

# 0xFB23
ch_adc_Y1 = construct.Struct(
    '_name' / construct.Computed('ch_adc_Y1'),
    'name' / construct.Computed('ADC Ch#Y1'),
    'desc' / construct.Computed('ADC data packet on detector channel Y1'),
    'ADC_Y1' / construct.Int32sl,  # Значение по каналу Y1
    'ADC_Ext' / construct.Int16ul,  # Отсчеты внешнего температурного датчика
)

# 0xFB24
ch_adc_Y2 = construct.Struct(
    '_name' / construct.Computed('ch_adc_Y2'),
    'name' / construct.Computed('ADC Ch#Y2'),
    'desc' / construct.Computed('ADC data packet on detector channel Y2'),
    'ADC_Y2' / construct.Int32sl,  # Значение по каналу Y2
    'ADC_Int' / construct.Int16ul,  # Отсчеты внутреннего температурного датчика
)

# 0xFC21
temp_cur_X1 = construct.Struct(
    '_name' / construct.Computed('temp_cur_X1'),
    'name' / construct.Computed('Temperature/current X1'),
    'desc' / construct.Computed('ADC data packet on detector channel X1'),
    'ADC_X1' / construct.Int32sl,  # Значение по каналу X1
    'Temp_Ext' / RegTemp,  # Температура датчика у детектора, градусы Цельсия * 100
)

# 0xFC22
temp_cur_X2 = construct.Struct(
    '_name' / construct.Computed('temp_cur_X2'),
    'name' / construct.Computed('Temperature/current X2'),
    'desc' / construct.Computed('ADC data packet on detector channel X2'),
    'ADC_X2' / construct.Int32sl,  # Значение по каналу X2
    'Temp_Int' / RegTemp,  # Температура датчика МК, градусы Цельсия * 100
)

# 0xFC23
temp_cur_Y1 = construct.Struct(
    '_name' / construct.Computed('temp_cur_Y1'),
    'name' / construct.Computed('Temperature/current Y1'),
    'desc' / construct.Computed('ADC data packet on detector channel Y1'),
    'ADC_Y1' / construct.Int32sl,  # Значение по каналу Y1
    'ADC_Ext' / construct.Int16ul,  # Отсчеты внешнего температурного датчика
)

# 0xFC24
temp_cur_Y2 = construct.Struct(
    '_name' / construct.Computed('temp_cur_Y2'),
    'name' / construct.Computed('Temperature/current Y2'),
    'desc' / construct.Computed('ADC data packet on detector channel Y2'),
    'ADC_Y2' / construct.Int32sl,  # Значение по каналу Y2
    'ADC_Int' / construct.Int16ul,  # Отсчеты внутреннего температурного датчика
)

# 0xFFE1
version_sw = construct.Struct(
    '_name' / construct.Computed('version_sw'),
    'name' / construct.Computed('VERSION SW'),
    'desc' / construct.Computed('VERSION SW'),
    'major' / construct.Int8ul,  # major
    'minor' / construct.Int8ul,  # minor
    'extra' / construct.Int8ul,  # extra
)

# other
filetransfer_init = construct.Struct(
    '_name' / construct.Computed('filetransfer_init'),
    'name' / construct.Computed('filetransfer_init'),
    'mode' / construct.Hex(construct.Enum(construct.Int8ul, **{'Receive': 0, 'Send': 1, 'No-query mode': 2, 'File list': 3, 'CRC': 4})),
    'ses_id' / construct.Int8ul,
    'bs' / construct.Int16ul,
    'offset' / construct.Int32ul,
    'reserved' / construct.Int16ul,     # mb string size?
    'file_name' / construct.GreedyString('utf-8'),
)

filetransfer_filesize = construct.Struct(
    '_name' / construct.Computed('filetransfer_filesize'),
    'name' / construct.Computed('filetransfer_filesize'),
    'size' / construct.Int32ul,
)

filetransfer_data = construct.Struct(
    '_name' / construct.Computed('filetransfer_data'),
    'name' / construct.Computed('filetransfer_data'),
    'session_id' / construct.Int8ul,
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
    PSU_REGULAR5: 'psu_regular5' / psu_regular5,
    ACK: 'ack' / ack,
    NACK: 'nack' / nack,
    INFO: 'Info' / Info,
    REGULAR_TEMPERATURE: 'regular_temperature' / regular_temperature,
    GET_PAYLOAD_TELEMETRY: 'get_Payload_telemetry' / get_Payload_telemetry,
    RATESENS_REGULAR_X: 'ratesens_regular_x' / ratesens_regular_x,
    RATESENS_REGULAR_Y: 'ratesens_regular_y' / ratesens_regular_y,
    RATESENS_REGULAR_Z: 'ratesens_regular_z' / ratesens_regular_z,
    MAGNSENS_REGULAR_X: 'magnsens_regular_x' / magnsens_regular_x,
    MAGNSENS_REGULAR_Y: 'magnsens_regular_y' / magnsens_regular_y,
    MAGNSENS_REGULAR_Z: 'magnsens_regular_z' / magnsens_regular_z,
    VECTOR_X: 'Vector_X' / Vector_X,
    VECTOR_Y: 'Vector_Y' / Vector_Y,
    VECTOR_Z: 'Vector_Z' / Vector_Z,
    BRIGHTNESS: 'Brightness' / Brightness,
    COMMON_TELEMETRY: 'common_telemetry' / common_telemetry,
    VHF_SETTINGS: 'vhf_settings' / vhf_settings,
    BEACON: 'beacon' / beacon,
    EXTENDED_BEACON: 'extended_beacon' / extended_beacon,
    TIME_REQUEST: 'time_request' / time_request,
    UHF_BEACON: 'uhf_beacon' / uhf_beacon,
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
    ACKNOWLEDGE: 'acknowledge' / acknowledge,
    OVERCURRENT: 'overcurrent' / overcurrent,
    SWITCH_STATUS: 'switch_status' / switch_status,
    REGULAR_TELEMETRY6U: 'regular_telemetry6u' / regular_telemetry6u,
    PS_REGULAR_TELEMETRY_5CH: 'ps_regular_telemetry_5ch' / ps_regular_telemetry_5ch,
    TM_ADCS_BEACON_OLD: 'tm_adcs_beacon_old' / tm_adcs_beacon_old,
    TM_ADCS_BEACON: 'tm_adcs_beacon' / tm_adcs_beacon,
    TM_ADCS_BEACON_6_WHEELS: 'tm_adcs_beacon_6_wheels' / tm_adcs_beacon_6_wheels,
    CH_ADC_X1: 'ch_adc_X1' / ch_adc_X1,
    CH_ADC_X2: 'ch_adc_X2' / ch_adc_X2,
    CH_ADC_Y1: 'ch_adc_Y1' / ch_adc_Y1,
    CH_ADC_Y2: 'ch_adc_Y2' / ch_adc_Y2,
    TEMP_CUR_X1: 'temp_cur_X1' / temp_cur_X1,
    TEMP_CUR_X2: 'temp_cur_X2' / temp_cur_X2,
    TEMP_CUR_Y1: 'temp_cur_Y1' / temp_cur_Y1,
    TEMP_CUR_Y2: 'temp_cur_Y2' / temp_cur_Y2,
    VERSION_SW: 'version_sw' / version_sw,

}

filetransfer = {
    FILETRANSFER_INIT: 'filetransfer_init' / filetransfer_init,
    FILETRANSFER_FILESIZE: 'filetransfer_filesize' / filetransfer_filesize,
    FILETRANSFER_DATA: 'filetransfer_data' / filetransfer_data,
}


_msg_map = tlm_map.copy()
_msg_map.update(filetransfer)
Data = construct.Struct(
    'message' / Addr,
    'sender' / Addr,
    'receiver' / Addr,
    'size' / construct.Int16ul,
    'packet' / construct.Switch(construct.this.message, _msg_map, default=construct.Bytes(construct.this.size)),
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

        if data.message == FILETRANSFER_DATA:
            img = self.get_image()
            with img.lock:
                img.push_data(packet.offset, packet.data[:data.size - 5])
                if packet.offset < img.first_data_offset:
                    img.first_data_offset = packet.offset

        elif data.message == FILETRANSFER_INIT:
            self.generate_fid(packet.file_name)
            img = self.get_image()
            with img.lock:
                img.has_starter = 1

        elif data.message == FILETRANSFER_FILESIZE:
            img = self.get_image()
            with img.lock:
                img.open().truncate(packet.size)

        else:
            return
        return 1


class UspProtocol:
    columns = 'msg-id',
    c_width = 60,

    _regular_tmpl = {
        'table': (
            ('name', 'Name'),
            ('desc', 'Description'),
            ('current', 'Current, mA'),
            ('voltage', 'Voltage, mV'),
        ),
        'flags': (
            ('current_invalid', 'Current invalid'),
            ('voltage_invalid', 'Voltage invalid'),
        ),
    }
    _ack_tmpl = {
        'table': (
            ('name', 'Name'),
            ('desc', 'Description'),
            ('value', 'Value'),
        ),
    }
    _ratesens_regular_tmpl = {
        'table': (
            ('name', 'Name'),
            ('desc', 'Description'),
            ('velocity', 'Velocity, deg/s'),
            ('temperature', 'Temperature, °C'),
        ),
        'flags': (
            ('counter', 'Counter'),
            ('invalid', 'Data is not valid'),
        ),
    }
    _magnsens_regular_tmpl = {
        'table': (
            ('name', 'Name'),
            ('desc', 'Description'),
            ('field', 'Magnetic field, nT'),
            ('temperature', 'Temperature, °C'),
        ),
        'flags': (
            ('counter', 'Counter'),
            ('invalid', 'Data is not valid'),
        ),
    }
    _vector_tmpl = {
        'table': (
            ('name', 'Name'),
            ('desc', 'Description'),
            ('vector', 'Direction, deg'),
            ('temperature', 'Temperature, °C'),
        ),
        'flags': (
            ('invalid', 'Data is not valid'),
        ),
    }
    _zerolen_tmpl = {
        'table': (
            ('name', 'Name'),
            ('desc', 'Description'),
        ),
    }

    tlm_table = {
        'regular_common': _regular_tmpl,
        'regular_x': _regular_tmpl,
        'regular_y': _regular_tmpl,
        'regular_z': _regular_tmpl,
        'psu_regular0': _regular_tmpl,
        'psu_regular1': _regular_tmpl,
        'psu_regular2': _regular_tmpl,
        'psu_regular3': _regular_tmpl,
        'psu_regular4': _regular_tmpl,
        'psu_regular5': _regular_tmpl,
        'ack': _ack_tmpl,
        'nack': _ack_tmpl,
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
                ('temperature1_invalid', 'Temperature #1 invalid'),
                ('temperature0_invalid', 'Temperature #0 invalid'),
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
        'ratesens_regular_x': _ratesens_regular_tmpl,
        'ratesens_regular_y': _ratesens_regular_tmpl,
        'ratesens_regular_z': _ratesens_regular_tmpl,
        'magnsens_regular_x': _magnsens_regular_tmpl,
        'magnsens_regular_y': _magnsens_regular_tmpl,
        'magnsens_regular_z': _magnsens_regular_tmpl,
        'Vector_X': _vector_tmpl,
        'Vector_Y': _vector_tmpl,
        'Vector_Z': _vector_tmpl,
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
                ('Usb1', 'Solar Panel #1 voltage, mV'),
                ('Usb2', 'Solar Panel #2 voltage, mV'),
                ('Usb3', 'Solar Panel #3 voltage, mV'),
                ('Isb1', 'Solar Panel #1 current, mA'),
                ('Isb2', 'Solar Panel #2 current, mA'),
                ('Isb3', 'Solar Panel #3 current, mA'),
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
                ('reg_tel_id', 'PSS telemetry SN'),
                ('Time', 'PSS telemetry time'),
                ('Nres', 'PSS reset counter'),
                ('FL', 'PS flags'),
                ('t_amp', 'UHF amp temperature, °C'),
                ('t_uhf', 'UHF temperature, °C'),
                ('RSSIrx', 'RX RSSI, dBm'),
                ('RSSIidle', 'Idle RSSI, dBm'),
                ('Pf', 'Forward wave power, dBm'),
                ('Pb', 'Reflected wave power, dBm'),
                ('Nres_uhf', 'UHF reset counter'),
                ('FL_uhf', 'UHF flags'),
                ('Time_uhf', 'UHF telemetry time'),
                ('UpTime', 'Uptime'),
                ('Current', 'UHF consumption current, mA'),
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
                ('Additional_channel_3_on', 'Aux Ch#3 ON'),
                ('Additional_channel_2_on', 'Aux Ch#2 ON'),
                ('Additional_channel_1_on', 'Aux Ch#1 ON'),
                ('FSB', 'Power switch error'),
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
        'time_request': _zerolen_tmpl,
        'uhf_beacon': {
            'table': (
                ('name', 'Name'),
                ('desc', 'Description'),
                ('t_amp', 'UHF amp temperature, °C'),
                ('t_uhf', 'UHF temperature, °C'),
                ('RSSIrx', 'RX RSSI, dBm'),
                ('RSSIidle', 'idle RSSI, dBm'),
                ('Pf', 'Forward wave power, dBm'),
                ('Pb', 'Reflected wave power, dBm'),
                ('uhf_reset_counter', 'UHF reset counter'),
                ('FL', 'UHF flags'),
                ('Time', 'UHF time'),
                ('UpTime', 'Uptime'),
                ('RxBitrate', 'Uplink bitrate (Receive)'),
                ('CurrentConsumption', 'UHF consumption current, mA'),
                ('InputVoltage', 'UHF voltage, mV'),
            ),
            'flags': (
                ('NumActiveSchedules', 'Number of Active Schedules in executor'),
                ('ResetOccurredDuringExecution', 'Reboot occurred during schedule execution'),
                ('BackupScheduleActive', 'Backup schedule execution in progress'),
            ),
        },
        'detector_transmits': _zerolen_tmpl,
        'data_massive_addr_rpl': _zerolen_tmpl,
        'data_event_addr_rpl': _zerolen_tmpl,
        'data_monitor_addr_rpl': _zerolen_tmpl,
        'data_massive_rpl': _zerolen_tmpl,
        'data_event_rpl': _zerolen_tmpl,
        'data_monitor_rpl': _zerolen_tmpl,
        'get_Payload_FW_MSG': {
            'table': (
                ('name', 'Name'),
                ('desc', 'Description'),
                ('Modification', 'Modification'),
                ('Version', 'Version'),
                ('Release_Number', 'Release Number'),
            ),
        },
        'no_monitor_data': _zerolen_tmpl,
        'no_event_data': _zerolen_tmpl,
        'no_massive_data': _zerolen_tmpl,
        'compl_monitor_data': _zerolen_tmpl,
        'compl_event_data': _zerolen_tmpl,
        'compl_massive_data': _zerolen_tmpl,
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
                ('VTG_S1', 'Solar Panel #1 voltage, mV'),
                ('VTG_S2', 'Solar Panel #2 voltage, mV'),
                ('VTG_S3', 'Solar Panel #3 voltage, mV'),
                ('CUR_S1', 'Solar Panel #1 current, mA'),
                ('CUR_S2', 'Solar Panel #2 current, mA'),
                ('CUR_S3', 'Solar Panel #3 current, mA'),
                ('CUR_BAT', 'Battery current, mA'),
                ('CUR_S1O', 'Channel #1 current, mA'),
                ('CUR_S2O', 'Channel #2 current, mA'),
                ('CUR_S3O', 'Channel #3 current, mA'),
                ('CUR_S4O', 'Channel #4 current, mA'),
                ('TMP_BAT1', 'Battery #1 temperature, °C'),
                ('TMP_BAT2', 'Battery #2 temperature, °C'),
                ('TMP_BAT3', 'Battery #3 temperature, °C'),
                ('TMP_BAT4', 'Battery #4 temperature, °C'),
                ('VBAT', 'Battery voltage, mV'),
                ('REC_ID', 'PSS Telemetry SN'),
                ('Time', 'PSS Time'),
                ('launch_number', 'PSS reset counter'),
                ('reset_reason', 'PSS Reset reason'),
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
                ('Additional_channel_3_on', 'Aux Ch#3 ON'),
                ('Additional_channel_2_on', 'Aux Ch#2 ON'),
                ('Additional_channel_1_on', 'Aux Ch#1 ON'),
                ('FSB', 'Power switch error'),
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
                ('DEV_ADDR', 'Device UniCAN address'),
                ('SRC_ADDR', 'Base station UniCAN address'),
                ('TEL_PER', 'Regular telemetry period, ms'),
                ('ETEL_PER', 'Extended telemetry period, s'),
                ('REC_ID', 'Packet SN'),
                ('ST_DELAY', 'Startup delay, s'),
                ('SW_VER', 'MCU firmware version'),
                ('DEPLOY_START_TIMER', 'Deploy start timer'),
                ('DEPLOY_STOP_TIMER', 'Deploy stop timer'),
                ('DEPLOY_MODE', 'Deploy mode'),
            ),
        },
        'acknowledge' : _zerolen_tmpl,
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
        'regular_telemetry6u': {
            'table': (
                ('name', 'Name'),
                ('desc', 'Description'),
                ('Usb1', 'Solar Panel #1 voltage, mV'),
                ('Usb2', 'Solar Panel #2 voltage, mV'),
                ('Usb3', 'Solar Panel #3 voltage, mV'),
                ('Isb1', 'Solar Panel #1 current, mA'),
                ('Isb2', 'Solar Panel #2 current, mA'),
                ('Isb3', 'Solar Panel #3 current, mA'),
                ('Iab', 'Battery current, mA'),
                ('Uab', 'Battery voltage, mV'),
                ('Uab1', 'Voltage on cell #1, mV'),
                ('Uab2', 'Voltage on cell #2, mV'),
                ('t1_pw', 'Battery #1 temperature, °C'),
                ('t2_pw', 'Battery #2 temperature, °C'),
                ('capacity', 'Capacity'),
                ('reg_tel_id', 'PSS telemetry number'),
                ('Time', 'PSS telemetry time'),
                ('ps_reset_counter', 'PSS reset counter'),
                ('FL', 'PS flags'),
            ),
            'flags': (
                ('ch1_status', 'Ch#1 Status'),
                ('ch2_status', 'Ch#2 Status'),
                ('ch3_status', 'Ch#3 Status'),
                ('ch4_status', 'Ch#4 Status'),
                ('ch5_status', 'Ch#5 Status'),
                ('ch6_status', 'Ch#6 Status'),
                ('ch7_status', 'Ch#7 Status'),
                ('ch8_status', 'Ch#8 Status'),
                ('ch9_status', 'Ch#9 Status'),
                ('ch10_status', 'Ch#10 Status'),
                ('ch11_status', 'Ch#11 Status'),
                ('ch12_status', 'Ch#12 Status'),
                ('ch13_status', 'Ch#13 Status'),
                ('ch14_status', 'Ch#14 Status'),
                ('ch15_status', 'Ch#15 Status'),
                ('ch16_status', 'Ch#16 Status'),
                ('ch17_status', 'Ch#17 Status'),
                ('ch18_status', 'Ch#18 Status'),
                ('ch19_status', 'Ch#19 Status'),
                ('ch20_status', 'Ch#20 Status'),
                ('ch21_status', 'Ch#21 Status'),
                ('ch22_status', 'Ch#22 Status'),
                ('ch23_status', 'Ch#23 Status'),
                ('ch24_status', 'Ch#24 Status'),
                ('ch25_status', 'Ch#25 Status'),
                ('ch26_status', 'Ch#26 Status'),
                ('ch27_status', 'Ch#27 Status'),
                ('ch28_status', 'Ch#28 Status'),
                ('ch29_status', 'Ch#29 Status'),
                ('ch30_status', 'Ch#30 Status'),
                ('Tab_min', 'Minimal battery Temperature'),
                ('Tab_max', 'Maximal battery Temperature'),
                ('heater1_on', 'Heater #1 ON'),
                ('heater2_on', 'Heater #2 ON'),
                ('heater1_manual', 'Heater #1 manual'),
                ('heater2_manual', 'Heater #2 manual'),
                ('Uab_min', 'Minimal battery voltage'),
                ('Uab_crit', 'Critical battery voltage'),
                ('Ich_limit1', 'Exceeding channel #1 current'),
                ('Ich_limit2', 'Exceeding channel #2 current'),
                ('Ich_limit3', 'Exceeding channel #3 current'),
                ('Ich_limit4', 'Exceeding channel #4 current'),
                ('channelon1', 'Ch#1 ON'),
                ('channelon2', 'Ch#2 ON'),
                ('channelon3', 'Ch#3 ON'),
                ('channelon4', 'Ch#4 ON'),
                ('charger', 'Charger connected'),
                ('FSB', 'Power switch error'),
                ('AuxCH1_enabled_flag', 'Aux Ch#1 ON'),
                ('AuxCH2_enabled_flag', 'Aux Ch#2 ON'),
                ('AuxCH3_enabled_flag', 'Aux Ch#3 ON'),
            ),
        },
        'ps_regular_telemetry_5ch': {
            'table': (
                ('name', 'Name'),
                ('desc', 'Description'),
                ('VTG_SOL1', 'Solar Panel #1 Voltage, mV'),
                ('VTG_SOL2', 'Solar Panel #2 Voltage, mV'),
                ('VTG_SOL3', 'Solar Panel #3 Voltage, mV'),
                ('CUR_SOL1', 'Solar Panel #1 Current, mA'),
                ('CUR_SOL2', 'Solar Panel #2 Current, mA'),
                ('CUR_SOL3', 'Solar Panel #3 Current, mA'),
                ('CUR_BAT', 'Battery Current, mA'),
                ('CUR_PCH1', 'Ch#1 Current, mA'),
                ('CUR_PCH2', 'Ch#2 Current, mA'),
                ('CUR_PCH3', 'Ch#3 Current, mA'),
                ('CUR_PCH4', 'Ch#4 Current, mA'),
                ('CUR_PCH5', 'Ch#5 Current, mA'),
                ('TMP_BAT1', 'Battery #1 temperature, °C'),
                ('TMP_BAT2', 'Battery #2 temperature, °C'),
                ('TMP_BAT3', 'Battery #3 temperature, °C'),
                ('TMP_BAT4', 'Battery #4 temperature, °C'),
                ('VBAT', 'Battery voltage, mV'),
                ('REC_ID', 'PSS telemetry SN'),
                ('Time', 'PSS telemetry time'),
                ('ps_reset_counter', 'PSS reset counter'),
                ('reset_reason', 'PS reset reason'),
            ),
            'flags': (
                ('Tab_min', 'Minimal battery Temperature'),
                ('Tab_max', 'Maximal battery Temperature'),
                ('heater1_on', 'Heater #1 ON'),
                ('heater2_on', 'Heater #2 ON'),
                ('heater1_manual', 'Heater #1 manual'),
                ('heater2_manual', 'Heater #2 manual'),
                ('Uab_min', 'Minimal battery voltage'),
                ('Uab_crit', 'Critical battery voltage'),
                ('Ich_limit1', 'Exceeding channel #1 current'),
                ('Ich_limit2', 'Exceeding channel #2 current'),
                ('Ich_limit3', 'Exceeding channel #3 current'),
                ('Ich_limit4', 'Exceeding channel #4 current'),
                ('Ich_limit5', 'Exceeding channel #5 current'),
                ('channelon1', 'Ch#1 ON'),
                ('channelon2', 'Ch#2 ON'),
                ('channelon3', 'Ch#3 ON'),
                ('channelon4', 'Ch#4 ON'),
                ('channelon5', 'Ch#5 ON'),
                ('charger', 'Charger connected'),
                ('FSB', 'Power switch error'),
                ('AuxCH1_enabled_flag', 'Aux Ch#1 ON'),
                ('AuxCH2_enabled_flag', 'Aux Ch#2 ON'),
                ('AuxCH3_enabled_flag', 'Aux Ch#3 ON'),
            ),
        },
        'tm_adcs_beacon_old': {
            'table': (
                ('name', 'Name'),
                ('desc', 'Description'),
                ('Time', 'ECI time'),
                ('eci_quat_w', 'ECI quat w'),
                ('eci_quat_vect_x', 'ECI quat vect x'),
                ('eci_quat_vect_y', 'ECI quat vect y'),
                ('eci_quat_vect_z', 'ECI quat vect z'),
                ('eci_ave_x', 'ECI ave x'),
                ('eci_ave_y', 'ECI ave y'),
                ('eci_ave_z', 'ECI ave z'),
                ('orb_time', 'ORB time'),
                ('orb_quat_w', 'ORB quat w'),
                ('orb_quat_vect_x', 'ORB quat vect x'),
                ('orb_quat_vect_y', 'ORB quat vect y'),
                ('orb_quat_vect_z', 'ORB quat vect z'),
                ('orb_ave_x', 'ORB ave x'),
                ('orb_ave_y', 'ORB ave y'),
                ('orb_ave_z', 'ORB ave z'),
                ('forced_time', 'Forced time'),
                ('forced_quat_w', 'Forced quat w'),
                ('forced_quat_vect_x', 'Forced quat vect x'),
                ('forced_quat_vect_y', 'Forced quat vect y'),
                ('forced_quat_vect_z', 'Forced quat vect z'),
                ('forced_ave_x', 'Forced ave x'),
                ('forced_ave_y', 'Forced ave y'),
                ('forced_ave_z', 'Forced ave z'),
                ('ss_invalids', 'SS invalids'),
                ('wheel_invalids', 'Wheel invalids'),
            ),
            'flags': (
                ('eci_policy', 'ECI policy'),
                ('eci_invalid', 'ECI invalid'),
                ('orb_policy', 'ORB policy'),
                ('orb_invalid', 'ORB invalid'),
                ('forced_policy', 'Forced policy'),
                ('forced_invalid', 'Forced invalid'),
                ('mfs_invalid', 'MFS invalid'),
                ('avs_invalid', 'AVS invalid'),
            ),
        },
        'tm_adcs_beacon': {
            'table': (
                ('name', 'Name'),
                ('desc', 'Description'),
                ('Time', 'Current system time'),
                ('uptime', 'Uptime'),
                ('eci_quat_w', 'ECI quat w'),
                ('eci_quat_vect_x', 'ECI quat vect x'),
                ('eci_quat_vect_y', 'ECI quat vect y'),
                ('eci_quat_vect_z', 'ECI quat vect z'),
                ('eci_AV_x', 'ECI X Angular velocity, deg/s'),
                ('eci_AV_y', 'ECI Y Angular velocity, deg/s'),
                ('eci_AV_z', 'ECI Z Angular velocity, deg/s'),
                ('orb_quat_w', 'ORB quat w'),
                ('orb_quat_vect_x', 'ORB quat vect x'),
                ('orb_quat_vect_y', 'ORB quat vect y'),
                ('orb_quat_vect_z', 'ORB quat vect z'),
                ('orb_AV_x', 'ORB X Angular velocity, deg/s'),
                ('orb_AV_y', 'ORB Y Angular velocity, deg/s'),
                ('orb_AV_z', 'ORB Z Angular velocity, deg/s'),
                ('eci_forced_quat_w', 'ECI forced quat w'),
                ('eci_forced_quat_vect_x', 'ECI forced quat vect x'),
                ('eci_forced_quat_vect_y', 'ECI forced quat vect y'),
                ('eci_forced_quat_vect_z', 'ECI forced quat vect z'),
                ('eci_forced_AV_x', 'ECI forced X Angular velocity, deg/s'),
                ('eci_forced_AV_y', 'ECI forced Y Angular velocity, deg/s'),
                ('eci_forced_AV_z', 'ECI forced Z Angular velocity, deg/s'),
                ('latitude', 'Latitude, deg'),
                ('longitude', 'Longitude, deg'),
                ('altitude', 'Altitude, m'),
                ('adcs_task_type', 'Current task type'),
                ('adcs_task_quantity', 'Tasks quantity in scheduler'),
                ('wheel_rpm_x_plus', 'Wheels X+ angular velocity, rpm'),
                ('wheel_rpm_x_minus', 'Wheels X- angular velocity, rpm'),
                ('wheel_rpm_y_plus', 'Wheels Y+ angular velocity, rpm'),
                ('wheel_rpm_y_minus', 'Wheels Y- angular velocity, rpm'),
            ),
            'flags': (
                ('eci_policy', 'ECI policy'),
                ('eci_invalid', 'ECI invalid'),
                ('orb_policy', 'ORB policy'),
                ('orb_invalid', 'ORB invalid'),
                ('eci_forced_policy', 'ECI forced policy'),
                ('eci_forced_invalid', 'ECI forced invalid'),
                ('ballistics_policy', 'Ballistics policy'),
                ('gnss_invalid', 'GNSS invalid'),
                ('auto_ballistics_polity', 'Auto ballistics policy'),
                ('auto_control_policy', 'Auto control policy'),
                ('ss_active', 'Active sun sensor'),
                ('ss_invalid_x_plus', 'X+ Sun sensors invalid'),
                ('ss_invalid_x_minus', 'X- Sun sensors invalid'),
                ('ss_invalid_y_plus', 'Y+ Sun sensors invalid'),
                ('ss_invalid_y_minus', 'Y- Sun sensors invalid'),
                ('ss_invalid_z_plus', 'Z+ Sun sensors invalid'),
                ('ss_invalid_z_minus', 'Z- Sun sensors invalid'),
                ('ss_invalid_extra', 'Extra Sun sensors invalid'),
                ('star_tracker_invalid', 'Star tracker invalid'),
                ('avs_invalid', 'AVS invalid'),
                ('mfs_invalid', 'MFS invalid'),
                ('wheel_invalid_x_plus', 'Wheels X+ invalid'),
                ('wheel_invalid_x_minus', 'Wheels X- invalid'),
                ('wheel_invalid_y_plus', 'Wheels Y+ invalid'),
                ('wheel_invalid_y_minus', 'Wheels Y- invalid'),
                ('reset_reason', 'Last reset reason'),
            ),
        },
        'tm_adcs_beacon_6_wheels': {
            'table': (
                ('name', 'Name'),
                ('desc', 'Description'),
                ('Time', 'Current system time'),
                ('uptime', 'Uptime'),
                ('eci_quat_w', 'ECI quat w'),
                ('eci_quat_vect_x', 'ECI quat vect x'),
                ('eci_quat_vect_y', 'ECI quat vect y'),
                ('eci_quat_vect_z', 'ECI quat vect z'),
                ('eci_AV_x', 'ECI X Angular velocity, deg/s'),
                ('eci_AV_y', 'ECI Y Angular velocity, deg/s'),
                ('eci_AV_z', 'ECI Z Angular velocity, deg/s'),
                ('orb_quat_w', 'ORB quat w'),
                ('orb_quat_vect_x', 'ORB quat vect x'),
                ('orb_quat_vect_y', 'ORB quat vect y'),
                ('orb_quat_vect_z', 'ORB quat vect z'),
                ('orb_AV_x', 'ORB X Angular velocity, deg/s'),
                ('orb_AV_y', 'ORB Y Angular velocity, deg/s'),
                ('orb_AV_z', 'ORB Z Angular velocity, deg/s'),
                ('eci_forced_quat_w', 'ECI forced quat w'),
                ('eci_forced_quat_vect_x', 'ECI forced quat vect x'),
                ('eci_forced_quat_vect_y', 'ECI forced quat vect y'),
                ('eci_forced_quat_vect_z', 'ECI forced quat vect z'),
                ('eci_forced_AV_x', 'ECI forced X Angular velocity, deg/s'),
                ('eci_forced_AV_y', 'ECI forced Y Angular velocity, deg/s'),
                ('eci_forced_AV_z', 'ECI forced Z Angular velocity, deg/s'),
                ('latitude', 'Latitude, deg'),
                ('longitude', 'Longitude, deg'),
                ('altitude', 'Altitude, m'),
                ('adcs_task_type', 'Current task type'),
                ('adcs_task_quantity', 'Tasks quantity in scheduler'),
                ('wheel_rpm_1', 'Wheels #1 angular velocity, rpm'),
                ('wheel_rpm_2', 'Wheels #2 angular velocity, rpm'),
                ('wheel_rpm_3', 'Wheels #3 angular velocity, rpm'),
                ('wheel_rpm_4', 'Wheels #4 angular velocity, rpm'),
                ('wheel_rpm_5', 'Wheels #5 angular velocity, rpm'),
                ('wheel_rpm_6', 'Wheels #6 angular velocity, rpm'),
                ('reset_reason', 'Last reset reason'),
            ),
            'flags': (
                ('eci_policy', 'ECI policy'),
                ('eci_invalid', 'ECI invalid'),
                ('orb_policy', 'ORB policy'),
                ('orb_invalid', 'ORB invalid'),
                ('eci_forced_policy', 'ECI forced policy'),
                ('eci_forced_invalid', 'ECI forced invalid'),
                ('ballistics_policy', 'Ballistics policy'),
                ('gnss_invalid', 'GNSS invalid'),
                ('auto_ballistics_polity', 'Auto ballistics policy'),
                ('auto_control_policy', 'Auto control policy'),
                ('ss_active', 'Active sun sensor'),
                ('ss_invalid_x_plus', 'X+ Sun sensors invalid'),
                ('ss_invalid_x_minus', 'X- Sun sensors invalid'),
                ('ss_invalid_y_plus', 'Y+ Sun sensors invalid'),
                ('ss_invalid_y_minus', 'Y- Sun sensors invalid'),
                ('ss_invalid_z_plus', 'Z+ Sun sensors invalid'),
                ('ss_invalid_z_minus', 'Z- Sun sensors invalid'),
                ('ss_invalid_extra', 'Extra Sun sensors invalid'),
                ('star_tracker_invalid', 'Star tracker invalid'),
                ('avs_invalid', 'AVS invalid'),
                ('mfs_invalid', 'MFS invalid'),
                ('wheel_invalid_1', 'Wheels #1 invalid'),
                ('wheel_invalid_2', 'Wheels #2 invalid'),
                ('wheel_invalid_3', 'Wheels #3 invalid'),
                ('wheel_invalid_4', 'Wheels #4 invalid'),
                ('wheel_invalid_5', 'Wheels #5 invalid'),
                ('wheel_invalid_6', 'Wheels #6 invalid'),
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

            if i.message in filetransfer:
                ty = 'img'
                p_data = self.ir.push_data(i), self.ir.cur_img

            elif i.message in tlm_map:
                ty = 'tlm'
                p_data = data, p_data

            else:
                ty = 'raw'

            yield ty, self.get_sender_callsign(data), '0x%04X' % i.message, p_data
