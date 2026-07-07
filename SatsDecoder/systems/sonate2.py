#  Copyright (c) 2024. Alexander Baskikh
#
#  MIT License (MIT), http://opensource.org/licenses/MIT
#  Full license can be found in the LICENSE-MIT file
#
#  SPDX-License-Identifier: MIT

import construct

from SatsDecoder.systems import ax25, ccsds, common

__all__ = 'SonateProtocol',

proto_name = 'sonate-2'

'''
SONATE-2 telemetry description in xls file:
    https://www.informatik.uni-wuerzburg.de/en/aerospaceinfo/mitarbeiter/kayal/forschungsprojekte/sonate-2/information-for-radio-amateurs/
'''

enum_0 = construct.Enum(construct.BitsInteger(1), **{'OFF': 0, 'ON': 1})
enum_1 = construct.Enum(construct.BitsInteger(3), **{'NO ROLE': 0, 'OBDH PASSIVE 3': 4, 'OBDH PASSIVE 2': 5, 'OBDH PASSIVE 1': 6, 'OBDH ACTIVE': 7, 'PDH ACTIVE': 3, 'BOOTLOADER': 1})
enum_2 = construct.Enum(construct.BitsInteger(6), **{'CONFIG': 1, 'ROLE MANAGER': 2, 'NFM CONTROLLER': 3, 'STD TC EXECUTER': 4, 'STD TC RECEIVER': 5, 'STD TC SAVER': 6, 'SOFTWARE WDG': 7, 'OBDH TC RECEIVER': 8, 'SYSTEM MANAGER': 9, 'CAN 1': 10, 'CAN 2': 11, 'SYNCH 1': 12, 'SYNCH 2': 13, 'SYNCH 3': 14, 'SYNCH 4': 15, 'LINKINTERFACE CAN 1': 16, 'LINKINTERFACE CAN 2': 17, 'NO ERROR': 0, 'HOUSEKEEPER': 18, 'TM DOWNLINK': 19, 'STORAGE MONITOR': 20, 'PARALLEL NOR 1': 21, 'PARALLEL NOR 2': 22, 'SPI NOR ': 23, 'SRAM 1': 24, 'SRAM 2': 25, 'SRAM CONTROLLER': 26, 'PAYLOAD HANDLER': 27, 'SOFTWARE INSTALLER': 28, 'MEMOP MANAGER': 29, 'SOFTWARE UPLOAD': 30, 'REPAIR AND CHECK': 31, 'VHF 1': 32, 'VHF 2': 33, 'UHF 1': 34, 'UHF 2': 35, 'EGSE 1': 36, 'EGSE 2': 37, 'EXP DATA HANDLER': 38, 'SAFE MODE LIMIT': 39, 'BTLDR NO ERROR': 50, 'BTLDR INVLD ADDR': 51, 'BTLDR INVLD SECTOR': 52, 'BTLDR INVLD SIZE': 53, 'BTLDR INVLD CMD': 54, 'BTLDR UNKNOWN CMD': 55, 'BTLDR CAN OVFLW': 56, 'BTLDR INVLD CRC': 57, 'BTLDR APP IMG DEFECT': 58, 'SBAND': 40, 'BOOT MSG HANDLER': 41, 'BTLDR RDP L1 SET': 59, 'BTLDR RDP L2 SET': 60, 'BTLDR WRP SET': 61, 'CAN LISTENER': 42, 'BTLDR DEFECT': 63})
enum_3 = construct.Enum(construct.BitsInteger(6), **{'CONFIG': 1, 'ROLE MANAGER': 2, 'NFM CONTROLLER': 3, 'STD TC EXECUTER': 4, 'STD TC RECEIVER': 5, 'STD TC SAVER': 6, 'SOFTWARE WDG': 7, 'OBDH TC RECEIVER': 8, 'SYSTEM MANAGER': 9, 'CAN 1': 10, 'CAN 2': 11, 'SYNCH 1': 12, 'SYNCH 2': 13, 'SYNCH 3': 14, 'SYNCH 4': 15, 'LINKINTERFACE CAN 1': 16, 'LINKINTERFACE CAN 2': 17, 'NO ERROR': 0, 'HOUSEKEEPER': 18, 'TM DONWLINK': 19, 'STORAGE MONITOR': 20, 'PARALLEL NOR 1': 21, 'PARALLEL NOR 2': 22, 'SPI NOR ': 23, 'SRAM 1': 24, 'SRAM 2': 25, 'SRAM CONTROLLER': 26, 'PAYLOAD HANDLER': 27, 'SOFTWARE INSTALLER': 28, 'MEMOP MANAGER': 29, 'SOFTWARE UPLOAD': 30, 'REPAIR AND CHECK': 31, 'VHF 1': 32, 'VHF 2': 33, 'UHF 1': 34, 'UHF 2': 35, 'EGSE 1': 36, 'EGSE 2': 37, 'EXP DATA HANDLER': 38, 'SAFE MODE LIMIT': 39, 'BTLDR NO ERROR': 50, 'BTLDR INVLD ADDR': 51, 'BTLDR INVLD SECTOR': 52, 'BTLDR INVLD SIZE': 53, 'BTLDR INVLD CMD': 54, 'BTLDR UNKNOWN CMD': 55, 'BTLDR CAN OVFLW': 56, 'BTLDR INVLD CRC': 57, 'BTLDR APP IMG DEFECT': 58, 'SBAND': 40, 'BOOT MSG HANDLER': 41, 'BTLDR RDP L1 SET': 59, 'BTLDR RDP L2 SET': 60, 'BTLDR WRP SET': 61, 'CAN LISTENER': 42, 'BTLDR DEFECT': 63})
enum_4 = construct.Enum(construct.BitsInteger(3), **{'NONE': 0, 'OBDH 1': 4, 'OBDH 2': 5, 'OBDH 3': 6, 'OBDH 4': 7})
enum_5 = construct.Enum(construct.BitsInteger(4), **{'NO ERROR': 0, 'CMD NOT SUPPORTED': 1, 'CMD OVERDUE WARNING': 2, 'CMD OVERDUE ERROR': 3, 'CMD CRC ERROR': 4, 'CMD FLASH BUSY': 5, 'CMD TT ERROR': 6, 'CMD INVALID SINK': 7, 'CMD EXEC FAILED BOTH': 8, 'CMD INVALID LENGTH': 9, 'CMD INVALID TYPE': 10, 'CMD INVALID CODE': 11, 'CMD INVALID EXE SINK': 12, 'CMD EXEC FAILED BUS1': 13, 'CMD EXEC FAILED BUS2': 14})
enum_6 = construct.Enum(construct.BitsInteger(4), **{'NONE': 8, 'EGSE 1': 4, 'VHF 1': 0, 'VHF 2': 1, 'UHF 1': 2, 'UHF 2': 3, 'S-BAND 1': 6, 'S-BAND 2': 7, 'EGSE 2': 5})
enum_7 = construct.Enum(construct.BitsInteger(4), **{'NORMAL': 1, 'WARN SOFT': 2, 'WARN CRITIC': 3, 'PASSIVE': 4, 'OFF': 5, 'NULLPTR': 7, 'NOT INIT': 0})
enum_8 = construct.Enum(construct.BitsInteger(4), **{'BOOT MODE': 0, 'LEOP MODE': 2, 'SAFE MODE': 1, 'NORMAL MODE': 3, 'PROCEDURE MODE': 4, 'USER MODE': 6, 'SIMULATOR': 15, 'BEACON MODE': 5, 'OBC LIGHT UHF': 14, 'OBC LIGHT VHF': 13})
enum_9 = construct.Enum(construct.BitsInteger(4), **{'VHF 1': 0, 'VHF 2': 1, 'UHF 1': 2, 'UHF 2': 3, 'NONE': 8, 'EGSE 1': 4, 'EGSE 2': 5, 'S-BAND 1': 6, 'S-BAND 2': 7, 'VHF 1 + S-BAND': 10, 'VHF 2 + S-BAND': 11, 'UHF 1 + S-BAND': 12, 'UHF 2 + S-BAND': 13, 'EGSE 1 + S-BAND': 14, 'EGSE 2 + S-BAND': 15})
enum_10 = construct.Enum(construct.BitsInteger(3), **{'OBDH 1': 0, 'OBDH 2': 1, 'OBDH 3': 2, 'OBDH 4': 3, 'NONE': 7})
enum_11 = construct.Enum(construct.BitsInteger(3), **{'N/A': 0, 'SSTV': 2, 'CW': 3, 'TMTC': 1, 'APRS': 4, 'DEPLOY': 5, 'DEPLOY OVERRIDE': 6})
enum_12 = construct.Enum(construct.BitsInteger(4), **{'31.5': 15, '31.4': 14, '31.0': 13, '30.0': 12, '28.5': 11, '28.2': 10, '28.1': 9, '27.4': 8, '26.0': 7, '24.0': 6, '21.2': 5, '16.5': 4, '7.0': 3, 'N/A': 1, '0 - PA OFF': 0})
enum_13 = construct.Enum(construct.BitsInteger(5), **{'NO ERROR': 0, 'ILLEGAL CMD': 1, 'ILLEGAL PARAM': 2, 'I²C ERROR': 3, 'TX PACKET ORDER': 4, 'TX PACKET TIMEOUT': 5, 'TX PACKET OVERRUN': 6, 'AUTORANGING RX': 7, 'AUTORANGING TX': 8, 'RX CRC FAIL': 9, 'RX ABORT': 10, 'RX SIZE FAIL': 11, 'RX ADDR FAIL': 12, 'CFG REPAIR 1-2 GOOD': 13, 'RX PACKET OVERRUN': 14, 'APRS RX BUF OVERRUN': 15, 'PREP COMPLETE': 16, 'TC DEC UNEXP LEN': 17, 'TC DEC CRC ERR': 18, 'CAN RX BUF OVERRUN': 19, 'CAN BUSY TIMEOUT': 20, 'UNEXP IMG UPL STATE': 21, 'ILL IMG UPL START': 22, 'IMG UPL ABORT': 23, 'IMG UPL PKT CRC': 24, 'IMG UPL CRC': 25, 'TRX FAIL': 26, 'DEPLOY TIMEOUT': 27, 'CFG TRIPLE RED SUCC': 28, 'CFG TRIPLE RED FAIL': 29, 'OBCL CAN REC OVERRUN': 30, 'UNEXP RX FIFO ERR': 31})
enum_14 = construct.Enum(construct.BitsInteger(3), **{'N/A': 0, 'TMTC': 1, 'SSTV': 2, 'CW': 3, 'APRS': 4, 'DEPLOY': 5, 'DEPLOY_OVERRIDE': 6})
enum_15 = construct.Enum(construct.BitsInteger(4), **{'31.7': 15, '31.6': 14, '31.4': 13, '30.9': 12, '29.7': 11, '29.6': 10, '29.5': 9, '28.9': 8, '28.1': 7, '26.7': 6, '24.9': 5, '21.9': 4, '16.8': 3, '7.0': 2, 'N/A': 1, '0 - PA OFF': 0})
enum_16 = construct.Enum(construct.BitsInteger(4), **{'30.6': 15, '30.0': 14, '28.8': 13, '27.7': 12, '25.7': 11, '24.4': 10, '22.5': 9, '18.3': 8, '3.0': 7, 'N/A': 1, '0 - PA OFF': 0})
enum_17 = construct.Enum(construct.BitsInteger(4), **{'30.7': 15, '30.4': 14, '29.5': 13, '28.4': 12, '27.1': 11, '26.2': 10, '24.3': 9, '20.7': 8, '7.8': 7, 'N/A': 1, '0 - PA OFF': 0})
enum_18 = construct.Enum(construct.BitsInteger(1), **{'YES': 0, 'NO': 1})
enum_19 = construct.Enum(construct.BitsInteger(1), **{'FAULT': 0, 'NO FAULT': 1})
enum_20 = construct.Enum(construct.BitsInteger(1), **{'OFF': 1, 'ON': 0})
enum_21 = construct.Enum(construct.BitsInteger(4), **{'NO ERROR': 0, 'ILLEGAL CMD': 1, 'ILLEGAL PARAM': 2, 'CFG REPAIR 1-2 GOOD': 3, 'I2C ERR': 4, 'CMD RX BUF OVERRUN': 5, 'CFG TRIPLE RED SUCC': 6, 'CFG TRIPLE RED FAIL': 7, 'PWR NOT GOOD 5V->12V': 8})
enum_22 = construct.Enum(construct.BitsInteger(1), **{'RESET': 0, 'SET': 1})
enum_23 = construct.Enum(construct.BitsInteger(1), **{'TRUE': 1, 'FALSE': 0})
enum_24 = construct.Enum(construct.BitsInteger(1), **{'FAULT': 0, 'GOOD': 1})
enum_25 = construct.Enum(construct.BitsInteger(1), **{'NOT AVAILABLE': 0, 'AVAILABLE': 1})
enum_26 = construct.Enum(construct.BitsInteger(1), **{'PFM': 0, 'PWM': 1})
enum_27 = construct.Enum(construct.BitsInteger(4), **{'NO ERROR': 0, 'ILLEGAL CMD': 1, 'ILLEGAL PARAM': 2, 'CFG REPAIR 1-2 GOOD': 3, 'CMD RX BUF OVERRUN': 4, 'CFG TRIPLE RED SUCC': 5, 'CFG TRIPLE RED FAIL': 6})
enum_28 = construct.Enum(construct.BitsInteger(2), **{'UNDEF': 0, 'CHARGING': 1, 'CHARGE COMPL': 2, 'FAULT': 3})
enum_29 = construct.Enum(construct.BitsInteger(2), **{'IDLE': 1, 'DEPLOY_OVERRIDE': 2, 'DEPLOY': 3, 'OFF': 0})
enum_30 = construct.Enum(construct.BitsInteger(4), **{'NO ERROR': 0, 'ILLEGAL CMD': 1, 'ILLEGAL PARAM': 2, 'CFG REPAIR 1-2 GOOD': 3, 'DEPLOY TIMEOUT': 4, 'DEPLOY OVERCURRENT': 5, 'TORQ X FAULT': 6, 'TORQ Y FAULT': 7, 'TORQ Z FAULT': 8, 'TORQ X OVERCURRENT': 9, 'TORQ Y OVERCURRENT': 10, 'TORQ Z OVERCURRENT': 11, 'CFG TRIPLE RED SUCC': 13, 'CFG TRIPLE RED FAIL': 14, 'DEPLOY FAULT': 15, 'TORQ TIMEOUT': 12})
enum_31 = construct.Enum(construct.BitsInteger(3), **{'IDLE': 0, 'SENDING': 1, 'RECEIVING': 2, 'LOCAL MEMCPY': 3, 'ERASING': 4, 'BLANK CHECK': 5})
enum_32 = construct.Enum(construct.BitsInteger(4), **{'NO ERROR': 0, 'ACK TIMEOUT': 1, 'MANAGER BUSY': 2, 'MEM OVERLAP': 3, 'WRITE ERROR': 4, 'READ ERROR': 5, 'ERASE ERROR': 6, 'INVLD PARAM': 7, 'BLNK CHK ERR': 8, 'SUCCESSFUL': 9, 'RX TIMEOUT': 10, 'RETRY LIMIT': 11, 'FORBID ADDR': 12})
enum_33 = construct.Enum(construct.BitsInteger(6), **{'NO ERROR': 0, 'INVLD STATE TRANS': 1, 'INVLD STATE': 2, 'TIMEOUT': 3, 'FLASH ER ERR': 4, 'INVLD PACKET NR': 5, 'INVLD PACKET CRC': 6, 'FLASH WR ERR': 7, 'FLASH RD ERR': 8, 'SRAM RD ERR': 9, 'INVLD ADDR': 10, 'INVLD FILE CRC': 11, 'FILE TO LARGE': 12, 'NACK RESPONSE': 13, 'SUCCESSFUL': 14, 'SPI CRC INVLD': 15, 'HS ENC INIT FAIL': 16, 'HS DEC INIT FAIL': 17, 'DTLS NOT IMPL': 21, 'DTLS OUT OF TO MEM': 22, 'DTLS BAD PATCH TYPE': 23, 'DTLS BAD COMPRESS': 24, 'DTLS INTERNAL ERR': 25, 'DTLS OUT OF SRC MEM': 26, 'DTLS CORRUPT PATCH': 27, 'DTLS ALREADY DONE': 28, 'DTLS SHORT HEADER': 29, 'DTLS PATCH DATA MSNG': 30, 'DTLS HEATHSRINK SINK': 31, 'DTLS HEATSHRINK POLL': 32, 'DTLS HEATSHRINK NULL': 33, 'DTLS ALREADY FAILED': 34, 'DTLS PATCH OVERFLOW': 35, 'DTLS HEATSHRINK HDR': 36, 'DTLS MEM READ FAIL': 37, 'DTLS MEM WRITE FAIL': 38, 'HS HDR FLAG FAIL': 18, 'HS HDR PARAMS FAIL': 19, 'HS HDR SIZE FAIL': 20, 'FORBID ADDR': 39})
enum_34 = construct.Enum(construct.BitsInteger(3), **{'IDLE': 0, 'LOCK CRC': 1, 'W4 START RESPONSE': 3, 'W4 DWNLD ANN': 4, 'W4 DATA XFER DONE': 5, 'END': 6, 'SEND START REQUEST': 2})
enum_35 = construct.Enum(construct.BitsInteger(3), **{'IDLE': 0, 'W4 START RESPONSE': 2, 'W4 ANNOUNCE ACK': 3, 'W4 DATA ACK': 4, 'END': 5, 'SEND START REQUST': 1})
enum_36 = construct.Enum(construct.BitsInteger(2), **{'OBDH 1': 0, 'OBDH 2': 1, 'OBDH 3': 2, 'OBDH 4': 3})
enum_37 = construct.Enum(construct.BitsInteger(1), **{'YES': 1, 'NO': 0})
enum_38 = construct.Enum(construct.BitsInteger(5), **{'IDLE': 0, 'LOAD DATA': 13, 'SEND DATA': 14, 'W4 TRANSFER DONE': 15, 'END': 18, 'SET MODE': 1, 'GET MODE': 2, 'READ MODE': 3, 'SET FILE SIZE': 4, 'GET FILE SIZE': 5, 'READ FILE SIZE': 6, 'SET FILE CRC': 7, 'GET FILE CRC': 8, 'READ FILE CRC': 9, 'SET PACKET SIZE': 10, 'GET PACKET SIZE': 11, 'READ PACKET SIZE': 12, 'GET PACKET STS': 16, 'READ PACKET STS': 17})
enum_39 = construct.Enum(construct.BitsInteger(3), **{'CAN BUS 1': 2, 'CAN BUS 2': 3, 'NONE': 0, 'SPI': 1, 'SSTV': 4, 'COMPRESS': 6, 'DECOMPRESS': 7, 'DELTA UPDATE': 5})
enum_40 = construct.Enum(construct.BitsInteger(5), **{'IDLE': 0, 'LOCK CRC': 1, 'RECEIVE DATA': 15, 'W4 TRANSFER DONE': 16, 'WRITE DATA TO FLASH': 17, 'END': 18, 'SET MODE': 2, 'GET MODE': 3, 'READ MODE': 4, 'GET FILE SIZE': 5, 'READ FILE SIZE': 6, 'GET FILE CRC': 7, 'READ FILE CRC': 8, 'SET PACKET SIZE': 9, 'GET PACKET SIZE': 10, 'READ PACKET SIZE': 11, 'SET PACKET NR': 12, 'GET PACKET NR': 13, 'READ PACKET NR': 14})
enum_41 = construct.Enum(construct.BitsInteger(4), **{'NO ERROR': 0, 'FIFO FULL': 1, 'FLASH WR ERR': 2, 'FLASH ER ERR': 3, 'DATA TOO LARGE': 4, 'BUFFER FULL': 5, 'NO BUFFER FOUND': 6, 'INVLD BUFFER ID': 7, 'FLASH RD ERR': 8, 'BUFFER NOT EMPTY': 9, 'BUF ERASE ONGOING': 10, 'ERASE SUCCESS': 11})
enum_42 = construct.Enum(construct.BitsInteger(1), **{'ACTIVATED': 1, 'DEACTIVATED': 0})
enum_43 = construct.Enum(construct.BitsInteger(1), **{'ARMED': 1, 'DISARMED': 0})
enum_44 = construct.Enum(construct.BitsInteger(2), **{'ARMED': 0, 'EXECUTED': 1, 'DISARMED': 2})
enum_45 = construct.Enum(construct.BitsInteger(1), **{'NOT DEPLOYED': 0, 'DEPLOYED': 1})
enum_46 = construct.Enum(construct.BitsInteger(1), **{'DISABLED': 0, 'ENABLED': 1})
enum_47 = construct.Enum(construct.BitsInteger(1), **{'CLOSING': 0, 'OPENING': 1})
enum_48 = construct.Enum(construct.BitsInteger(1), **{'STBY': 0, 'ON': 1})
enum_49 = construct.Enum(construct.BitsInteger(4), **{'NO ERROR': 0, 'CFG 1 RD ERR': 1, 'CFG 1 CRC INVLD': 4, 'WRITE ERR': 8, 'ERASE ERR': 9, 'INIT FAILED': 10, 'CFG 2 CRC INVLD': 5, 'CFG 3 CRC INVLD': 6, 'CFG R CRC INVLD': 7, 'CFG 2 RD ERR': 2, 'CFG 3 RD ERR': 3, 'INT ADR INVLD': 11, 'INT ERS ERR': 12, 'INT WR ERR': 13})
enum_50 = construct.Enum(construct.BitsInteger(4), **{'NO ERROR': 0, 'CMD NOT KNWN': 1, 'CMD PARAM INVLD': 2, 'STATE INVLD': 3, 'RST PROT NACK': 4, 'UART TX ERROR': 5, 'ROLE COLLISION': 6, 'OBDH REBOOT': 7, 'MON OBDH TO': 8, 'NO FREE ROLE': 9, 'MON PART TO': 10, 'COM SRC UNKN': 11, 'NO RSP FIN': 12, 'NO RSP PRI': 13, 'NO RSP SEC': 14, 'NO RSP TER': 15})
enum_51 = construct.Enum(construct.BitsInteger(5), **{'NO ERROR': 0, 'INVLD ADDR': 1, 'PNOR1 WR TO': 2, 'PNOR2 WR TO': 3, 'SNOR WR TO': 4, 'PNOR1 WR ERR': 5, 'PNOR2 WR ERR': 6, 'SNOR WR ERR': 7, 'PNOR1 RD TO': 8, 'PNOR2 RD TO': 9, 'SNOR RD TO': 10, 'PNOR1 RD ERR': 11, 'PNOR2 RD ERR': 12, 'SNOR RD ERR': 13, 'PNOR1 ERS TO': 14, 'PNOR2 ERS TO': 15, 'SNOR ERS TO': 16, 'PNOR1 ERS ERR': 17, 'PNOR2 ERS ERR': 18, 'SMOR ERS ERR': 19})
enum_52 = construct.Enum(construct.BitsInteger(4), **{'NO ERROR': 0, 'CMD NOT SUP': 1, 'CMD WARN OVD': 2, 'CMD ERR OVD': 3, 'CMD ERR CRC': 4, 'CDM FLASH BUSY': 5, 'CMD TT ERROR': 6, 'CMD INVLD SINK': 7, 'CMD EXE FAILED BOTH': 8, 'CMD INVLD LEN': 9, 'CMD INVLD TYPE': 10, 'CMD INVLD CDE': 11, 'CMD INVLD EXE SINK': 12, 'CMD EXE FAILED BUS1': 13, 'CMD EXE FAILED BUS2': 14})
enum_53 = construct.Enum(construct.BitsInteger(4), **{'NO ERROR': 0, 'CRC INVLD': 1, 'BUFFER FULL': 2, 'INVLD CMD LEN': 6})
enum_54 = construct.Enum(construct.BitsInteger(5), **{'NO ERROR': 0, 'LIST NOT INIT': 1, 'LIST FULL': 2, 'LIST EMPTY': 3, 'WRNG TT TYPE': 4, 'WRNG TIME ORD': 5, 'FLASH WR ERR': 6, 'FLASH RD ERR': 7, 'FLASH PRST ERR': 8, 'FLASH FIN ERR': 9, 'FLASH CLR ERR': 10, 'FLASH ERS ERR': 11, 'CRC INVLD': 12, 'LIST NOT FIN': 13, 'LIST INIT FAIL': 14, 'LIST ALR FIN': 15, 'NO REL TT IN ACT TT': 16, 'INVLD STRT TIME': 17, 'LIST NOT ENUF SP': 18, 'LIST NOT EMPTY': 19, 'SM PROC IMPOS': 20, 'LEOP PROC IMPOS': 21, 'PROC COPY TO SELF': 22})
enum_55 = construct.Enum(construct.BitsInteger(5), **{'NO ERROR': 0, 'WARN WDG': 1, 'WARN ROLE MAN': 2, 'WARN HK': 3, 'WARN GAT CAN1': 6, 'WARN GAT CAN2': 7, 'WARN SYS MAN': 4, 'WARN TC': 5, 'WARN TM DOWN': 8, 'WARN STD CAN': 9, 'WARN STO MON': 10, 'ERR WDG': 16, 'ERR ROLE MAN': 17, 'ERR HK': 18, 'ERR GAT CAN1': 21, 'ERR GAT CAN2': 22, 'ERR SYS MAN': 19, 'ERR TC': 20, 'ERR TM DOWN': 23, 'ERR STD CAN': 24, 'ERR STO MON': 25, 'WARN PLD HDLR': 11, 'WARN SW INST': 12, 'ERR PLD HDLR': 26, 'ERR SW INST': 27, 'WARN S-BAND': 13, 'ERR S-BAND': 28})
enum_56 = construct.Enum(construct.BitsInteger(3), **{'NO ERROR': 0, 'CRC INVLD': 1, 'BUFFER FULL': 2, 'INVLD SW MOD': 3, 'INVLD CMD CDE': 4, 'INVLD CMD PRM LEN': 5, 'INVLD CMD LEN': 6, 'INVLD CMD PARAM': 7})
enum_57 = construct.Enum(construct.BitsInteger(4), **{'NO ERROR': 0, 'CFG 1 RD ERR': 1, 'CFG 2 RD ERR': 2, 'CFG 3 RD ERR': 3, 'CFG 1 CRC INVLD': 4, 'CFG 2 CRC INVLD': 5, 'CFG 3 CRC INVLD': 6, 'CFG R CRC INVLD': 7, 'WRITE ERR': 8, 'ERASE ERR': 9, 'INIT FAILED': 10, 'INT ADR INVLD': 11, 'INT ERS ERR': 12, 'INT WR ERR': 13})
enum_58 = construct.Enum(construct.BitsInteger(5), **{'NO ERROR': 0, 'WARN GAT CAN2': 7, 'WARN TM DOWN': 8, 'WARN STD CAN': 9, 'WARN STO MON': 10, 'WARN PLD HDLR': 11, 'WARN SW INST': 12, 'WARN S-BAND': 13, 'ERR WDG': 16, 'ERR ROLE MAN': 17, 'ERR HK': 18, 'ERR SYS MAN': 19, 'ERR TC': 20, 'ERR GAT CAN1': 21, 'ERR GAT CAN2': 22, 'ERR TM DOWN': 23, 'ERR STD CAN': 24, 'ERR STO MON': 25, 'ERR PLD HDLR': 26, 'ERR SW INST': 27, 'ERR S-BAND': 28, 'WARN HK': 3, 'WARN SYS MAN': 4, 'WARN TC': 5, 'WARN GAT CAN1': 6, 'WARN WDG': 1, 'WARN ROLE MAN': 2})
enum_59 = construct.Enum(construct.BitsInteger(4), **{'NO ERROR': 0, 'TM RTC NEG VALUE': 1, 'TM RTC CNST VALUE': 2, 'FM LEOP BIT FLIP': 7, 'FM ERASE ERR': 8, 'FM LEOP WR ERR': 9, 'FM RST CNT WR ERR': 10, 'TM BUF PUSH FAIL': 4, 'TM BUF INIT FAIL': 5, 'TM BUF ERASE FAIL': 6, 'TM RTC SET FAIL': 3, 'CLK FAILURE': 11, 'TM RTC INIT FAIL': 12, 'TM RTC CALIB FAIL': 13, 'FM LEOP INVLD CHANGE': 14})
enum_60 = construct.Enum(construct.BitsInteger(4), **{'NO ERROR': 0, 'INVLD REQ ST': 1, 'INVLD DWNLK APID': 2, 'INVLD REQ IDX': 3, 'RING BUF INIT FAIL': 4, 'FRAME NULLPTR': 5, 'SEND REQ FAIL': 6, 'INVLD ADR RNG': 7, 'ARCHIVE WR ERR': 8, 'INVLD STRT SEQ NR': 9, 'NO CAN FRAME RCVD': 10, 'SBAND NOT ACTIVE': 11})
enum_61 = construct.Enum(construct.BitsInteger(4), **{'NO ERROR': 0, 'DNLK REQ BUF FULL': 1, 'TF ENC BYTE CPY ERR': 2, 'INVLD VC': 3})
enum_62 = construct.Enum(construct.BitsInteger(4), **{'NO ERROR': 0, 'TC LIST CRC ERR': 1, 'NODE NR ERR': 2, 'HW ID ERR': 3, 'LAST TC REC TIME ERR': 4, 'OBDH MODE ERR': 5, 'OBDH ROLE ERR': 6, 'TM DNLK EN FLAG ERR': 7, 'CMD CTR ERR': 8, 'ACT RDO ERR': 9, 'GPIO CTRL ERR': 10, 'PLD HDLR ACT ERR': 11, 'SW INST FLAG ERR': 12, 'SW UPLD FLAG ERR': 13, 'HK ONL FRWRD ERR': 14, 'INTRNL IMG INVLD': 15})
enum_63 = construct.Enum(construct.BitsInteger(4), **{'NO ERROR': 0, 'INVLD ADR': 1, 'SRAM1 WR ERR': 2, 'SRAM2 WR ERR': 3, 'SRAM1 RD ERR': 4, 'SRAM2 RD ERR': 5})
enum_64 = construct.Enum(construct.BitsInteger(4), **{'NO ERROR': 0, 'WAIT TF ACK TO': 1, 'WAIT TF START TO': 2, 'WAIT TF STOP TO': 3, 'RADIO NACK': 4, 'ALIVE TO': 5, 'RST LIM': 6, 'TF IS NULL': 7})
enum_65 = construct.Enum(construct.BitsInteger(4), **{'NO ERROR': 0, 'FM RST CNT WR ERR': 10, 'TM RTC NEG VALUE': 1, 'TM RTC CNST VALUE': 2, 'TM BUF PUSH FAIL': 4, 'TM BUF INIT FAIL': 5, 'TM BUF ERASE FAIL': 6, 'FM LEOP BIT FLIP': 7, 'FM ERASE ERR': 8, 'FM LEOP WR ERR': 9, 'TM RTC SET FAIL': 3, 'CLK FAILURE': 11, 'TM RTC INIT FAIL': 12, 'TM RTC CALIB FAIL': 13, 'FM LEOP INVLD CHANGE': 14})
enum_66 = construct.Enum(construct.BitsInteger(5), **{'NO ERROR': 0, 'NEW OBDH ACTIVE': 1, 'NO PCU RESPONSE': 2, 'VBAT 5V BUS1 VIOL': 8, 'IBUS 5V BUS1 VIOL': 9, 'IUHF 5V BUS1 VIOL': 10, 'IVHF 5V BUS1 VIOL': 11, 'VBAT 5V BUS2 VIOL': 12, 'IBUS 5V BUS2 VIOL': 13, 'IUHF 5V BUS2 VIOL': 14, 'IVHF 5V BUS2 VIOL': 15, 'VBAT 12V BUS1 VIOL': 16, 'IBUS 12V BUS1 VIOL': 17, 'VBAT 12V BUS2 VIOL': 18, 'IBUS 12V BUS2 VIOL': 19, 'INVLD MODE': 3, 'RADIOS DEAD': 4, 'TC EXECUTION': 5})
enum_67 = construct.Enum(construct.BitsInteger(5), **{'NO ERROR': 0, 'NEW OBDH ACTIVE': 1, 'NO PCU RESPONSE': 2, 'VBAT 5V BUS1 VIOL': 8, 'IBUS 5V BUS1 VIOL': 9, 'IUHF 5V BUS1 VIOL': 10, 'IVHF 5V BUS1 VIOL': 11, 'VBAT 5V BUS2 VIOL': 12, 'IBUS 5V BUS2 VIOL': 13, 'IUHF 5V BUS2 VIOL': 14, 'IVHF 5V BUS2 VIOL': 15, 'VBAT 12V BUS1 VIOL': 16, 'IBUS 12V BUS1 VIOL': 17, 'VBAT 12V BUS2 VIOL': 18, 'IBUS 12V BUS2 VIOL': 19, 'INVLD MODE': 3, 'RADIOS DEAD': 4, 'TC ECECUTION': 5})
enum_68 = construct.Enum(construct.BitsInteger(2), **{'NOT INIT': 0, 'NOT FINAL': 1, 'CRC NOT OK': 3, 'CRC OK': 2})
enum_69 = construct.Enum(construct.BitsInteger(1), **{'NOT INIT': 0, 'INITIALIZED': 1})
enum_70 = construct.Enum(construct.BitsInteger(2), **{'CONFIG 1': 0, 'CONFIG 2': 1, 'CONFIG 3': 2, 'CONFIG IMG': 3})
enum_71 = construct.Enum(construct.BitsInteger(4), **{'NO ERROR': 0, 'RX HW FIFO0 OVRN': 1, 'RX HW FIFO1 OVRN': 2, 'RX SW FIFO0 OVRN': 3, 'RX SW FIFO1 OVRN': 4, 'TX SW FIFO OVRN': 5, 'ERROR WARN': 6, 'ERROR PASSIVE': 7, 'BUS OFF': 8, 'STUFF ERR': 9, 'FORM ERR': 10, 'ACK ERR': 11, 'BIT RECESSIVE ERR': 12, 'BIT DOMINANT ERR': 13, 'CRC ERR': 14})
enum_72 = construct.Enum(construct.BitsInteger(3), **{'NO ERROR': 0, 'OVERUN ERR': 1, 'PARITY ERR': 2, 'FRAMING ERR': 3, 'NOISE ERR': 4, 'RX BUF OVFLW': 5})
enum_73 = construct.Enum(construct.BitsInteger(2), **{'NO ERROR': 0, 'BUFFER FULL': 1, 'RX TIMEOUT': 2, 'TX TIMEOUT': 3})
enum_74 = construct.Enum(construct.BitsInteger(1), **{'NO RESET': 0, 'RESET': 1})
enum_75 = construct.Enum(construct.BitsInteger(1), **{'INITIALIZED': 1, 'NOT INITIALIZED': 0})
enum_76 = construct.Enum(construct.BitsInteger(2), **{'LSE': 0, 'LSI': 1, 'HSE': 2, 'INVALID': 3})
enum_77 = construct.Enum(construct.BitsInteger(2), **{'HSI': 0, 'HSE': 1, 'PLL HSI': 2, 'PLL HSE': 3})
enum_78 = construct.Enum(construct.BitsInteger(2), **{'UART': 0, 'CAN_1': 1, 'CAN_2': 2, 'NONE': 3})
enum_79 = construct.Enum(construct.BitsInteger(3), **{'OBDH 1': 0, 'OBDH 2': 1, 'OBDH 3': 2, 'OBDH 4': 3, 'INVALID': 7})
enum_80 = construct.Enum(construct.BitsInteger(4), **{'NO ERROR': 0, 'NOT INIT': 1, 'ALREADY INIT': 2, 'LL DRIVER NOT EXIST': 3, 'NOT IMPLEMENTED': 4, 'INVALID ADDR': 5, 'DEVICE BUSY': 6, 'WRITE ERR': 7, 'INTERFACE BUSY': 8, 'TIMEOUT': 9, 'INVALID LEN': 10, 'ERASE ERR': 11})
enum_81 = construct.Enum(construct.BitsInteger(4), **{'NO ERROR': 0, 'NOT INIT': 1, 'ALREADY INIT': 2, 'LL DRIVER NOT EXIST': 3, 'INVLD ADDR': 4})
enum_82 = construct.Enum(construct.BitsInteger(1), **{'NO RESET': 1, 'RESET': 0})
enum_83 = construct.Enum(construct.BitsInteger(4), **{'6': 0, '96': 5, '120': 6, '144': 7, '168': 8, '8': 9, '16': 10, '32': 11, '64': 12, '12': 1, '24': 2, '48': 3, '72': 4})
enum_84 = construct.Enum(construct.BitsInteger(2), **{'UHF_VHF_ONLY': 0, 'SBAND_ONLY': 1, 'UHF_VHF_AND_SBAND': 2})
enum_85 = construct.Enum(construct.BitsInteger(4), **{'6': 0, '12': 1, '24': 2, '48': 3, '72': 4, '96': 5, '120': 6, '144': 7, '168': 8, '8': 9, '16': 10, '32': 11, '64': 12})
enum_86 = construct.Enum(construct.BitsInteger(4), **{'IDLE': 0, 'ERASE PAGES': 1, 'W4 SRC ADDR': 2, 'REPAIR IMG': 3, 'LOCKING CRC': 4, 'COMPUTE INT CRC': 6, 'COMPUTE EXT CRC': 5, 'W4_CRC_COMP_DONE': 7, 'PREP MEM TEST': 8, 'WR TEST PATTERN': 9, 'RD TEST PATTERN': 10})
enum_87 = construct.Enum(construct.BitsInteger(4), **{'NO ERROR': 0, 'INVALID STATE': 1, 'INVALID ADDR': 2, 'ERASE ERROR': 3, 'WRITE ERROR': 4, 'READ ERROR': 5, 'CRC INVALID': 6, 'INVALID PARAM': 7, 'PATTERN TEST ERR': 8, 'SUCCESSFUL': 9, 'FORBID ADDR': 10})
enum_88 = construct.Enum(construct.BitsInteger(3), **{'IDLE': 0, 'ERASE PAGES': 1, 'AWAITING DATA': 2, 'AWAITING FINALIZE': 3, 'COMPUTE CRC': 4})
enum_89 = construct.Enum(construct.BitsInteger(4), **{'NO ERROR': 0, 'INVALID STATE': 1, 'WRITE ERROR': 2, 'READ ERROR': 3, 'INVALID ADDR': 4, 'INVALID CRC': 5, 'ERASE ERROR': 6, 'INVALID PARAM': 7, 'INVLD SEGMENT ORDER': 8, 'SUCCESSFUL': 10, 'INVLD SEGMENT NR': 9, 'FORBID ADDR': 11})
enum_90 = construct.Enum(construct.BitsInteger(1), **{'VALID': 1, 'INVALID': 0})
enum_91 = construct.Enum(construct.BitsInteger(4), **{'UNKNOWN': 0, 'LPM RST': 1, 'WWDG RST': 2, 'IWDG RST': 3, 'SW RST': 4, 'BROWN-OUT RST': 5, 'PIN RST': 6, 'OPTN BYTE LD RST': 7, 'FIREWALL RST': 8})
enum_92 = construct.Enum(construct.BitsInteger(4), **{'UNKNOWN': 0, 'JTAG RST': 1, 'WATCHDOG RST': 2, 'BROWN OUT RST': 3, 'EXTERNAL RST': 4, 'POWER ON RST': 5})
enum_93 = construct.Enum(construct.BitsInteger(4), **{'UNKNOWN': 0, 'LPM RST': 1, 'WWDG RST': 2, 'IWDG RST': 3, 'SW RST': 4, 'POR PDR RST': 5, 'PIN RST': 6, 'BOR RST': 7})
enum_94 = construct.Enum(construct.BitsInteger(4), **{'NO ERROR': 0, 'INVLD MIC': 1, 'INVLD SAT BUS': 2, 'INVLD BOOT MSG LEN': 3, 'INVLD SW IMG': 4, 'INVLD BTLDR IMG': 5})
enum_95 = construct.Enum(construct.BitsInteger(4), **{'IDLE': 0, 'COMPUTE CRC': 1, 'CNCT TO BTLDR': 2, 'ERASE IMAGE': 3, 'WRITE IMAGE': 4, 'READ IMAGE': 5, 'START APP': 6, 'END': 7, 'DISCNCT FROM BTLDR': 8})
enum_96 = construct.Enum(construct.BitsInteger(2), **{'STM32 CAN': 0, 'ATMEGA CAN': 1, 'CUSTOM STM32': 2, 'INVALID': 3})
enum_97 = construct.Enum(construct.BitsInteger(4), **{'NO ERROR': 0, 'TIMEOUT': 1, 'NACK': 2, 'READ ERROR': 3, 'INVALID CRC': 4, 'INVALID STATE': 5, 'INVALID RESPONSE': 6, 'INVALID VALUE': 7, 'ERROR RETURNED': 8, 'INVALID MIC': 9, 'INVLD ACK COUNT': 10, 'INT FLAH WR ERR': 11, 'INT FLASH ER ERR': 12, 'INVLD META DATA': 13, 'SUCCESSFUL': 14, 'SELFUPDATE PREP FAIL': 15})
enum_98 = construct.Enum(construct.BitsInteger(6), **{'ADCS BTLDR': 1, 'VHF BTLDR': 2, 'UHF BTLDR': 3, 'SS BTLDR': 4, 'RW BTLDR': 5, 'AI MIC BTLDR': 6, 'MVIEW BTLDR': 7, 'PCU 5V APP': 10, 'PCU 12V APP': 11, 'IFP APP': 12, 'THRUSTER APP': 13, 'OBDH BTLDR': 8, 'OBDH 1 APP': 15, 'OBDH 2 APP': 16, 'OBDH 3 APP': 17, 'OBDH 4 APP': 18, 'VHF APP': 19, 'UHF APP': 20, 'RW X APP': 21, 'RW Y APP': 22, 'RW Z APP': 23, 'SS XP APP': 24, 'SS XN APP': 25, 'SS YP APP': 26, 'SS YN APP': 27, 'SS ZP APP': 28, 'SS ZN APP': 29, 'ADCS APP': 31, 'MVIEW APP': 32, 'AI MIC APP': 33, 'GNSS BTLDR': 9, 'GNSS APP': 30})
enum_99 = construct.Enum(construct.BitsInteger(2), **{'BUS 1': 0, 'BUS 2': 1})
enum_100 = construct.Enum(construct.BitsInteger(3), **{'WRITE TASK': 1, 'READ TASK': 2, 'RUN APP TASK': 3, 'NONE': 0, 'ERASE TASK': 4})
enum_101 = construct.Enum(construct.BitsInteger(1), **{'BOOTLOADER': 1, 'RUN': 0})
enum_102 = construct.Enum(construct.BitsInteger(1), **{'RUN': 0, 'BOOTLOADER': 1})
enum_103 = construct.Enum(construct.BitsInteger(1), **{'RUN': 0, 'PROGRAM': 1})
enum_104 = construct.Enum(construct.BitsInteger(1), **{'RODOS': 0, 'RTC': 1})
enum_105 = construct.Enum(construct.BitsInteger(1), **{'ID MASK': 0, 'ID LIST': 1})
enum_106 = construct.Enum(construct.BitsInteger(1), **{'NOT FINAL': 0, 'FINALIZED': 1})
enum_107 = construct.Enum(construct.BitsInteger(3), **{'BUF PUSH FAIL': 1, 'BUF INIT FAIL': 2, 'BUF FULL': 3, 'BUF ERASE FAIL': 4, 'NO ERROR': 0, 'BUF FINALIZE FAIL': 5})
enum_108 = construct.Enum(construct.BitsInteger(2), **{'CALIB 32s': 0, 'CALIB 16s': 1, 'CALIB 8s': 2})
enum_109 = construct.Enum(construct.BitsInteger(2), **{'UART': 0, 'CAN1': 1, 'CAN2': 2})
enum_110 = construct.Enum(construct.BitsInteger(3), **{'VHF 1': 0, 'VHF 2': 1, 'UHF 1': 2, 'UHF 2': 3})
enum_111 = construct.Enum(construct.BitsInteger(1), **{'ADCS 1': 0, 'ADCS 2': 1})
enum_112 = construct.Enum(construct.BitsInteger(3), **{'IDLE': 1, 'DETERMINATION': 2, 'DETUMBLING': 3, 'SUN POINTING': 4, 'EARTH POINTING': 5, 'TARGET POINTING': 6, 'OFF': 0})
enum_113 = construct.Enum(construct.BitsInteger(8), **{'NONE': 0, 'UNKNOWN': 1, 'NO UTC UPDATE': 2, 'TIME SYNC FAILED': 3, 'CAN TX FIFO FULL': 22, 'DATA FRAME TOO LARGE': 24, 'FLASH ERASE FAILED': 25, 'FLASH WRITING FAILED': 26, 'EXP CHANGE WHILE RUN': 27, 'PAGE 2 FULL': 28, 'ADXRS X INIT FAIL': 32, 'ADXRS Y INIT FAIL': 33, 'ADXRS Z INIT FAIL': 34, 'CRM X INIT FAIL': 35, 'CRM Y INIT FAIL': 36, 'CRM Z INIT FAIL': 37, 'RM INIT FAIL': 38, 'HMC INIT FAIL': 39, 'ADXRS X FAIL': 56, 'ADXRS Y FAIL': 57, 'ADXRS Z FAIL': 58, 'CRM X FAIL': 59, 'CRM Y FAIL': 60, 'CRM Z FAIL': 61, 'RM FAIL': 62, 'HMC FAIL': 63, 'INVALID SS CMD': 77, 'NO SS DATA': 81, 'SUN SENSOR TIMEOUT': 83, 'ADXRS COMPLETE FAIL': 84, 'CRM COMPLETE FAIL': 85, 'GYRO INCONSISTENT': 86, 'GYRO NO DATA': 87, 'MAG INCONSISTENT': 88, 'MAG NO DATA': 89, 'NOT ENOUGH DATA': 90, 'RW X1 FAULT': 111, 'RW Y1 FAULT': 112, 'RW Z1 FAULT': 113, 'RW X2 FAULT': 114, 'RW Y2 FAULT': 115, 'RW Z2 FAULT': 116, 'SGP4 FAULT': 120, 'SGP4 EPOCH IN FUTURE': 121, 'CRC MISMATCH': 129, 'NO VALID SETTINGS': 130, 'ERASE FAILED': 131, 'SAVING FAILED': 132, 'INVALID SLOT NUMBER': 133, 'CRM FAIL': 144, 'CRM PREV CMD FAIL': 145, 'CRM CBIT ENABLED': 146, 'CRM FACTORY FAIL': 147, 'CRM CRC FAIL': 148, 'S': 149})
enum_114 = construct.Enum(construct.BitsInteger(2), **{'NONE': 0, 'GYRO INTEGRATION': 1, 'TRIAD': 2, 'QUEST': 3})
enum_115 = construct.Enum(construct.BitsInteger(2), **{'RM & HMC': 3, 'RM': 2, 'HMC': 1, 'NONE': 0})
enum_116 = construct.Enum(construct.BitsInteger(1), **{'ECI': 0, 'LVLH': 1})
enum_117 = construct.Enum(construct.BitsInteger(1), **{'NONE': 0, 'YES': 1})
enum_118 = construct.Enum(construct.BitsInteger(3), **{'NONE': 0, 'X+': 1, 'X-': 2, 'Y+': 3, 'Y-': 4, 'Z+': 5, 'Z-': 6})
enum_119 = construct.Enum(construct.BitsInteger(1), **{'DAY': 1, 'NIGHT': 0})
enum_120 = construct.Enum(construct.BitsInteger(2), **{'ADXRS & CRM': 3, 'CRM': 1, 'ADXRS': 2, 'NONE': 0})
enum_121 = construct.Enum(construct.BitsInteger(2), **{'NONE': 0, 'SECONDS': 1, 'MILLISECONDS': 2})
enum_122 = construct.Enum(construct.BitsInteger(1), **{'NONE': 0, 'ENABLED': 1})
enum_123 = construct.Enum(construct.BitsInteger(1), **{'FAULT': 0, 'OK': 1})
enum_124 = construct.Enum(construct.BitsInteger(1), **{'CAN1': 0, 'CAN2': 1})
enum_125 = construct.Enum(construct.BitsInteger(1), **{'BDOTBANGBANG': 0, 'RATE DETUMBLING': 1})
enum_126 = construct.Enum(construct.BitsInteger(1), **{'TRIAD': 0, 'QUEST': 1})
enum_127 = construct.Enum(construct.BitsInteger(1), **{'POS': 0, 'NEG': 1})
enum_128 = construct.Enum(construct.BitsInteger(1), **{'HMC5883L': 0, 'RM3100': 1})
enum_129 = construct.Enum(construct.BitsInteger(1), **{'ADXRS453': 0, 'CRM100/200': 1})
enum_130 = construct.Enum(construct.BitsInteger(4), **{'NONE': 0, 'SEPARATE': 1, 'PARALLEL': 2, 'MAXIMUM': 3, 'POLYFIT': 4})
enum_131 = construct.Enum(construct.BitsInteger(1), **{'NEGATIVE': 0, 'POSITIVE': 1})
enum_132 = construct.Enum(construct.BitsInteger(3), **{'TORQUE': 0, 'RATE': 1, 'IDLE': 2})
enum_133 = construct.Enum(construct.BitsInteger(5), **{'NO_ERROR': 0, 'ERR_HAL': 1, 'ERR_CAN_SEND': 5, 'ERR_CAN_RECV': 6, 'ERR_TEST_ERROR': 2, 'ERR_WRONG_PARAMETER': 7, 'ERR_NO_RW_ID': 8, 'ERR_NO_SUCH_CMD': 9, 'ERR_HAL_UART_INIT': 10, 'ERR_CAN_INIT': 11, 'ERR_CFG_ERASE': 12, 'ERR_CFG_WRITE': 13, 'ERR_TC_BUF_FULL': 14, 'ERR_TC_ARG': 15, 'ERR_I2C_READ': 16, 'ERR_I2C_WRITE': 17, 'ERR_CFG_CRC': 18, 'ERR_CFG_SIZE': 19, 'ERR_NO_CFG_FOUND': 20})
enum_134 = construct.Enum(construct.BitsInteger(2), **{'BLOCK COMMUTATION': 0, 'SINE COMMUTATION': 1, 'FIELD ORIENTED': 2, 'NONE': 3})
enum_135 = construct.Enum(construct.BitsInteger(1), **{'BUS1': 0, 'BUS2': 1})
enum_136 = construct.Enum(construct.BitsInteger(1), **{'ENCODER A': 0, 'ENCODER B': 1})
enum_137 = construct.Enum(construct.BitsInteger(2), **{'RW X': 1, 'RW Y': 2, 'RW Z': 3})
enum_138 = construct.Enum(construct.BitsInteger(5), **{'NO ERROR': 0, 'CAN TX TO': 1, 'CAN BUF OVFL': 2, 'SPI TX FAIL': 3, 'SPI RX FAIL': 4, 'TC INVLD LEN': 5, 'TC INVLD CMD CODE': 6, 'TC INVLD CMD PARAM': 7, 'FLASH WRITE ERR': 8, 'FLASH ERASE ERR': 9, 'CFG CRC ERR': 10, 'NO CFG FOUND': 11, 'CFG SIZE INVLD': 12, 'ADC START ERR': 13, 'SPI RX DMA ERR': 14, 'PEAK WIDTH VIOL': 17, 'PEAK UNDEREXPOSED': 18, 'PEAK OVEREXPOSED': 19, 'PROF BUF SIZE INVLD': 15, 'INVLD OPERATION MODE': 16, 'SUN SENSOR BUSY': 24, 'STDBY MODE FAIL': 26, 'SPI WRITE FAIL': 27, 'SUCCESSFUL': 20, 'LOCAL CFG BROKEN': 21, 'MEAS TIMEOUT': 22})
enum_139 = construct.Enum(construct.BitsInteger(2), **{'CMD MODE': 1, 'ADCS TRIGGER MODE': 2, 'CONTINUOUS MODE': 3, 'OFF': 0})
enum_140 = construct.Enum(construct.BitsInteger(2), **{'ERASED': 0, 'FINALIZED': 1, 'WRITE PENDING': 2, 'ERASE PENDING': 3})
enum_141 = construct.Enum(construct.BitsInteger(3), **{'SUN SENSOR XP': 0, 'SUN SENSOR XN': 1, 'SUN SENSOR YP': 2, 'SUN SENSOR YN': 3, 'SUN SENSOR ZP': 4, 'SUN SENSOR ZN': 5})
enum_142 = construct.Enum(construct.BitsInteger(1), **{'EXTERNAL': 0, 'INTERNAL': 1})
enum_143 = construct.Enum(construct.BitsInteger(4), **{'1.85 V': 0, '1.90 V': 1, '1.95 V': 2, '2.00 V': 3, '2.05 V': 4, '2.10 V': 5, '2.15 V': 6, '2.20 V': 7, '2.25 V': 8, '2.30 V': 9, '2.35 V': 10, '2.40 V': 11, '2.45 V': 12, '2.50 V': 13, '2.55 V': 14, '2.60 V': 15})
enum_144 = construct.Enum(construct.BitsInteger(4), **{'0.80 V': 0, '0.85 V': 1, '0.90 V': 2, '0.95 V': 3, '1.00 V': 4, '1.05 V': 5, '1.10 V': 6, '1.15 V': 7, '1.20 V': 8, '1.25 V': 9, '1.30 V': 10, '1.35 V': 11, '1.40 V': 12, '1.45 V': 13, '1.50 V': 14, '1.55 V': 15})
enum_145 = construct.Enum(construct.BitsInteger(2), **{'CAP 0.2 pF': 0, 'CAP 0.4 pF': 1, 'CAP 0.6 pF': 2, 'CAP 0.8 pF': 3})
enum_146 = construct.Enum(construct.BitsInteger(4), **{'GAIN 1.000': 0, 'GAIN 0.500': 1, 'GAIN 0.333': 2, 'GAIN 0.250': 3, 'GAIN 0.200': 4, 'GAIN 0.167': 5, 'GAIN 0.143': 6, 'GAIN 0.125': 7, 'GAIN 0.111': 8, 'GAIN 0.100': 9, 'GAIN 0.091': 10, 'GAIN 0.083': 11, 'GAIN 0.077': 12, 'GAIN 0.071': 13, 'GAIN 0.067': 14, 'GAIN 0.063': 15})
enum_147 = construct.Enum(construct.BitsInteger(2), **{'5 PIXELS': 0, '9 PIXELS': 1, '19 PIXELS': 2, '29 PIXELS': 3})
enum_148 = construct.Enum(construct.BitsInteger(2), **{'CMD MODE': 0, 'CONTINOUS MODE': 2, 'ADCS TRIGGER MODE': 1})
enum_149 = construct.Enum(construct.BitsInteger(1), **{'ENABLED': 0, 'DISABLED': 1})
enum_150 = construct.Enum(construct.BitsInteger(1), **{'AFSK 1K2': 0, 'GMSK 9K6': 1})
enum_151 = construct.Enum(construct.BitsInteger(1), **{'ALL': 1, 'ADDRESSED ONLY': 0})
enum_152 = construct.Enum(construct.BitsInteger(2), **{'ALL FRAMES': 0, 'SELF FILTER PASSED': 1, 'SOURCE FILTER PASSED': 2, 'ALL FILTERS PASSED': 3})
enum_153 = construct.Enum(construct.BitsInteger(1), **{'NOT SYNC': 0, 'SYNC': 1})
enum_154 = construct.Enum(construct.BitsInteger(1), **{'CH0': 0, 'CH1': 1})
enum_155 = construct.Enum(construct.BitsInteger(4), **{'NO MOD': 0, 'BPSK': 1, 'QPSK': 2, '8PSK': 3, '16PSK': 4, '32PSK': 5, '64PSK': 6, 'S-BAND EGSE': 15})
enum_156 = construct.Enum(construct.BitsInteger(4), **{'FEC_1_1': 0, 'FEC_1_2': 1, 'FEC_2_3': 2, 'FEC_3_4': 3, 'FEC_5_6': 4, 'FEC_7_8': 5})
enum_157 = construct.Enum(construct.BitsInteger(4), **{'NO ERROR': 0, 'NO START FOUND': 1, 'NO END FOUND': 2, 'INVLD IDENT RX': 3, 'INVLD MSG LEN': 4, 'NAK RECEIVED': 5, 'SPI TIMEOUT': 6, 'TF INVLD CRC': 7, 'TF FRAME TO SHORT': 8, 'TF INVLD TC LEN': 9, 'TF BUFFER FULL': 10, 'TF FRAME TO LONG': 11, 'NO HK RECEIVED': 12, 'TF INVLD VC': 13, 'TF INVLD SC ID': 14, 'SPI WR BUF REJ': 15})
enum_158 = construct.Enum(construct.BitsInteger(1), **{'UNAVAILABLE': 0, 'AVAILABLE': 1})
enum_159 = construct.Enum(construct.BitsInteger(1), **{'CH 0': 0, 'CH 1': 1})
enum_160 = construct.Enum(construct.BitsInteger(2), **{'NO MOD': 0, 'BPSK': 1, 'QPSK': 2})
enum_161 = construct.Enum(construct.BitsInteger(3), **{'FEC 1/1': 0, 'FEC 1/2': 1, 'FEC 2/3': 2, 'FEC 3/4': 3, 'FEC 5/6': 4, 'FEC 7/8': 5})
enum_162 = construct.Enum(construct.BitsInteger(1), **{'ACCEPT': 1, 'REJECT': 0})
enum_163 = construct.Enum(construct.BitsInteger(7), **{'ALWAYS': 0, 'IN SYNC': 1})
enum_164 = construct.Enum(construct.BitsInteger(8), **{'NO ERROR': 0, 'UNKNOWN TC': 1, 'INVALID_TC': 2, 'PROCESS ALREADY RUN': 3, 'PROCESS NOT RUNNING': 4, 'DB INIT ERROR': 13, 'DB FAILED QUERY': 14, 'DB NO ENTRY': 15, 'DB RESULT EXISTS': 16, 'DB WRITE ERRIR': 17, 'DB READ ERROR': 18, 'DB NO CONFIG': 19, 'DB MISSING TABLE': 20, 'DL DIR ERROR': 21, 'DL FILE ERROR': 22, 'TAR ERROR': 23, 'PACKET OOB': 24, 'CAN UD INV STATE': 25, 'CAN UD INIT ERR': 26, 'CAN UD FORMAT': 27, 'CAN WRITE ERROR': 28, 'WRONG CRC': 29, 'UL_FILE_ERROR': 30, 'SPI_CMD_ERROR': 31, 'SPI_INIT_ERRROR': 32, 'NO_PROCESS_RUNNING': 5, 'PROCESS_FAILED_START': 6, 'PROCESS_CRASHED': 7, 'PROCESS_TIMEDOUT': 8, 'PROCESS_WRITE_ERROR': 9, 'PROCESS_READ_ERROR': 10, 'PROCESS_UKN_ERROR': 11, 'PROCESS_STDERR_OUTPU': 12, 'DB_SUCCESS': 33, 'DIR_NOT_EXIST': 34, 'SUCCESS': 35})
enum_165 = construct.Enum(construct.BitsInteger(6), **{'NO PROCESS RUNNING': 5, 'PROCESS CRASHED': 7, 'PROCESS TIMEOUT': 8, 'PROCESS WRITE ERR': 9, 'PROCESS READ ERR': 10, 'PROCESS UKN ERR': 11, 'STDERR OUTPUT': 12, 'PROCESS FAILED START': 6, 'NO ERROR': 0})
enum_166 = construct.Enum(construct.BitsInteger(8), **{'NO_PROCESS': 0, 'CAM_APP': 1, 'WIDE_SEG': 2, 'NEAR_SEG': 3, 'OBJECT_DET': 4, 'ANO_DET': 5, 'LIGHTNING': 6, 'BASH': 9})
enum_167 = construct.Enum(construct.BitsInteger(4), **{'LOG ONLY': 0, 'IMAGES': 1, 'VIDEOS': 2, 'IMAGE SEG PAIRS': 3})
enum_168 = construct.Enum(construct.BitsInteger(1), **{'ARMED': 1, 'IDLE': 0})
enum_169 = construct.Enum(construct.BitsInteger(8), **{'NO ERROR': 0, 'UART INIT': 10, 'HAL ERROR': 1, 'TEST ERROR': 2, 'FLASH INIT': 3, 'FLASH CORRUPT': 4, 'CAN SEND': 5, 'CAN RECV': 6, 'SPI SEND': 7, 'SPI RECV': 8, 'NO SUCH CMD': 9, 'CAN INIT': 11, 'APP CRASHED': 12, 'OS CRASHED': 13, 'TC BUF FULL': 14, 'TOO MANY REBOOTS': 15, 'FORCE POWEROFF': 16, 'FORCE POWERCYCLE': 17, 'UNEXPECTED STATE': 18, 'CMD PARAMETER': 19, 'NO MMC IF JETSON ON': 20, 'MMC TRANSFER TIMEOUT': 21, 'MMC CRC TIMEOUT': 22, 'MMC CRC FAIL': 23, 'CFG ERASE': 24, 'CFG WRITE': 25, 'CFG CRC': 26, 'CFG SIZE': 27, 'NO CFG FOUND': 28, 'MMC READ': 29, 'MMC WRITE': 30, 'CRC SUCCESS': 31, 'CMD TOO LONG': 32, 'CMD CRC FAIL': 33, 'CMD SUCCESS': 35, 'CMD TIMEOUT': 34, 'CRC INIT FAIL': 36, 'COPY SUCCESS': 37})
enum_170 = construct.Enum(construct.BitsInteger(4), **{'APP RUN': 0, 'APP CHECK': 1, 'APP CRASH': 2, 'OS CHECK': 3, 'OS CRASH': 4, 'OS REBOOT': 5, 'PWR ON': 6, 'BOOT': 7, 'OS SHUTDOWN': 8, 'FORCE PWR OFF': 9, 'POWER CYCLE': 10, 'JETSON STARTUP': 11, 'CMD EXEC': 12})
enum_171 = construct.Enum(construct.BitsInteger(1), **{'ERROR': 0, 'GOOD': 1})
enum_172 = construct.Enum(construct.BitsInteger(1), **{'JETSON': 0, 'STM': 1})
enum_173 = construct.Enum(construct.BitsInteger(2), **{'IDLE': 0, 'COPY': 1, 'CRC CHECK': 2, 'CMD EXEC': 3})
enum_174 = construct.Enum(construct.BitsInteger(1), **{'PRIMARY': 0, 'BACKUP': 1})
enum_175 = construct.Enum(construct.BitsInteger(2), **{'INTERNAL': 0, 'MMC 1': 1, 'MMC 1 Read Only': 2})
enum_176 = construct.Enum(construct.BitsInteger(6), **{'NO ERROR': 0, 'CAN INIT FAIL': 1, 'CAN IS NULLPTR': 2, 'CAN UNKNOWN RX': 3, 'TC INVLD CMD LEN': 4, 'TC INVLD CMD CODE': 5, 'TC INVLD CMD PARAM': 6, 'CFG NOT EXISTING': 7, 'SOCKET DISCONNECTED': 8, 'SOCKET ERROR': 9, 'SOCKET IS NULLPTR': 10, 'SOCKET NOT CONNECTED': 11, 'TCP WRITE FAIL': 12, 'RESULT DIR EXISTS': 13, 'DIR CREATION FAIL': 14, 'LOG CREATION FAIL': 15, 'CAM CFG LOAD FAIL': 16, 'CAM INIT FAIL': 17, 'CAM CMD FAIL': 18, 'CAM IMG SAVE FAIL': 19, 'CAM IMG GRAB FAIL': 20, 'CAM START FAIL': 21, 'CAM STOP FAIL': 22, 'TASK ALREADY RUNNING': 23, 'EXP NOT STARTED': 24, 'EXP ALREADY STARTED': 25, 'TASK_STILL_RUNNING': 26, 'CAM_IFACE_NO_ERROR': 27, 'CAM_IFACE_INVALID': 28, 'CAM_IF_ALRDY_RUNS': 29, 'CAM_IF_START_FAIL': 30, 'CAM_IF_PROP_SET_FAIL': 31, 'CAM_IF_NOT_STARTED': 32, 'CAM_IF_STOP_FAILED': 33, 'CAM_IF_WRONG_MODE': 34, 'CAM_IF_INV_IN_DATA': 35, 'CAM_IF_CAPT_TIMEOUT': 36, 'CAM_IF_NOT_LOADED': 37, 'CAM_IF_NO_CFG_FILE': 38, 'CAM_IF_FAIL_OPEN_CFG': 39, 'CAM_IF_CFG_WRTE_FAIL': 40, 'CAM_IF_INVAL_CAN_ID': 41, 'CAM_IF_INVAL_LENGTH': 42, 'CAM_IF_INVAL_CODE': 43, 'CAM_IF_INVALID_PARA': 44, 'CAM_IF_SCKT_OP_FAIL': 45, 'CAM_IF_BND_SCKT_FAIL': 46, 'CAM_': 47})
enum_177 = construct.Enum(construct.BitsInteger(1), **{'CONNECTED': 1, 'DISCONNECTED': 0})
enum_178 = construct.Enum(construct.BitsInteger(2), **{'IDLE': 0, 'CONTINUOUS': 1, 'TRIGGER': 2, 'VIDEO': 3})
enum_179 = construct.Enum(construct.BitsInteger(1), **{'RUNNING': 1, 'FINISHED': 0})
enum_180 = construct.Enum(construct.BitsInteger(1), **{'STARTED': 1, 'STOPPED': 0})
enum_181 = construct.Enum(construct.BitsInteger(1), **{'ONE_SHOT': 0, 'PRE_CALC': 1})
enum_182 = construct.Enum(construct.BitsInteger(4), **{'NONE': 0, 'IMAGE CAPTURE': 1, 'SINGLE TIMED CAPTURE': 2, 'DUAL TIMED CAPTURE': 3, 'QUAD TIMED CAPTURE': 4, 'MATCHED IMAGE CPTRE': 5, 'MATCHED TIMED CPTRE': 6})
enum_183 = construct.Enum(construct.BitsInteger(4), **{'LOG_ONLY': 0, 'SINGLE_IMAGES': 1, 'VIDEOS': 2, 'IMAGE_SEG_PAIRS': 3, 'IMAGE_PAIRS': 4})
enum_184 = construct.Enum(construct.BitsInteger(1), **{'AUTO_EXP_OFF': 0, 'AUTO_EXP_ON': 1})
enum_185 = construct.Enum(construct.BitsInteger(8), **{'NO_ERROR': 0, 'OVERFLOW': 4, 'ALREADY EXISTS': 6, 'DOES_NOT_EXIST': 8, 'MODEL_NOT_INIT': 9, 'MODEL_NOT EXIST': 11})
enum_186 = construct.Enum(construct.BitsInteger(4), **{'NOT_LOADED': 0, 'LOADING': 1, 'READY': 2, 'BUSY': 3})
enum_187 = construct.Enum(construct.BitsInteger(8), **{'0 - TEST': 0, '1 - OLED': 1, '2 - TEST CNTD': 2, '3 - OLED CNTD': 3, '4 - EVRTH': 4})
enum_188 = construct.Enum(construct.BitsInteger(8), **{'0 - SENTINEL': 0, '1 - LANDSAT': 1, '2 - SENTINEL CNTD': 2, '3 - LANDSAT CNTD': 3})
enum_189 = construct.Enum(construct.BitsInteger(8), **{'COARSE DETECT': 0, 'FINE DETECT': 1})
enum_190 = construct.Enum(construct.BitsInteger(8), **{'NO_ERROR': 0, 'OVERFLOW': 4, 'ALREADY EXISTS': 6, 'SUCCESS': 7, 'DOES_NOT_EXIST': 8, 'MODEL_NOT_INIT': 9, 'TIME_LIMIT': 10, 'MODEL_NOT EXIST': 11, 'CLASS_NOT_EXIST': 12, 'COPY_FAILED': 13})
enum_191 = construct.Enum(construct.BitsInteger(4), **{'NOT_LOADED': 0, 'LOADING': 1, 'READY': 2, 'BUSY': 3, 'TRAINING': 4, 'LOADING DATASET': 5, 'TAKING IMAGES': 6})
enum_192 = construct.Enum(construct.BitsInteger(6), **{'NO ERROR': 0, 'CAN INIT FAIL': 1, 'CAN IS NULL': 2, 'CAN UNKNOWN MSG': 3, 'TC INVLD CMD LEN': 4, 'TC INVLD CMD CODE': 5, 'TC INVLD CMD PARAM': 6, 'CFG NOT EXISTING': 7, 'TCP SOCKET DC': 8, 'TCP SOCKET ERR': 9, 'TCP SOCKET IS NULL': 10, 'TCP SOCKET NC': 11, 'RESULT DIR EXISTS': 12, 'RESULT DIR FAIL': 13, 'LOG FILE FAIL': 14, 'CAM INIT FAIL': 17, 'CAM IS NULL': 18, 'IP INIT FAIL': 19, 'CAM CFG FAIL': 20, 'CAM START FAIL': 21, 'CAM STOP FAIL': 22, 'CAM CMD FAIL': 23, 'EVENT TOO LONG': 24, 'EVENT TOO SHORT': 25, 'CUDA ALLOC FAILED': 26, 'NO CUDA DEVICE FOUND': 27, 'INVLD BACK SUB ALGO': 15, 'LABELING OVERFLOW': 16, 'DEFECT PIXEL FULL': 28, 'CFG WRITE FAIL': 29, 'CFG INVLD SIZE': 30, 'CFG INVLD CRC': 31, 'LD ALREADY RUNNING': 32, 'RESULT DIR DEL FAIL': 33, 'SUCCESSFUL': 34})
enum_193 = construct.Enum(construct.BitsInteger(1), **{'RUNNING': 1, 'STOPPED': 0})
enum_194 = construct.Enum(construct.BitsInteger(2), **{'SIGMA DELTA': 0, 'GAUSSIAN': 1})
enum_195 = construct.Enum(construct.BitsInteger(2), **{'UNKNOWN': 0, 'LIGHTNING': 1, 'METEOR': 2})
enum_196 = construct.Enum(construct.BitsInteger(2), **{'IDLE': 0, 'CONTINUOUS': 1, 'TRIGGER': 2})
enum_197 = construct.Enum(construct.BitsInteger(2), **{'WIDE MONO': 0, 'NARROW MONO': 1, 'WIDE RGB': 2, 'NARROW RGB': 3})
enum_198 = construct.Enum(construct.BitsInteger(5), **{'DEFAULT_0': 0, 'DEFAULT_1': 1, 'DEFAULT_2': 2, 'CAMERA_APP_1': 3, 'CAMERA_APP_2': 4, 'CAMERA_APP_3': 5, 'WIDE_SEGMENTATION_1': 6, 'WIDE_SEGMENTATION_2': 7, 'WIDE_SEGMENTATION_3': 8, 'NEAR_SEGMENTATION_1': 9, 'NEAR_SEGMENTATION_2': 10, 'NEAR_SEGMENTATION_3': 11, 'OBJECT_DETECTION_1': 12, 'OBJECT_DETECTION_2': 13, 'OBJECT_DETECTION_3': 14, 'ANOMALIEDETECTION_1': 15, 'ANOMALIEDETECTION_2': 16, 'ANOMALIEDETECTION_3': 17, 'LIGHT_DETECTION_1': 18, 'LIGHT_DETECTION_2': 19, 'LIGHT_DETECTION_3': 20, 'APP_7_1': 21, 'APP_7_2': 22, 'APP_7_3': 23, 'APP_8_1': 24, 'APP_8_2': 25, 'APP_8_3': 26, 'GENERIC_SHELL_1': 27, 'GENERIC_SHELL_2': 28, 'GENERIC_SHELL_3': 29, 'FREE_1': 30, 'FREE_2': 31})
enum_199 = construct.Enum(construct.BitsInteger(1), **{'PRE CALC': 1, 'ONE SHOT': 0})
enum_200 = construct.Enum(construct.BitsInteger(8), **{'SM TC LEN IVLD': 16, 'SM STATE FOR TC IVLD': 17, 'SM CMD CODE UNKOWN': 18, 'SM TC PARAM IVLD': 19, 'SM TC CAN RX BUF FUL': 20, 'SM CAN MSG TOO SHORT': 21, 'SM CAN BUS ERR': 22, 'SM TC NOT IMPL': 23, 'SM CAN BUS TIMEOUT': 24, 'SM CALIB MODE IVLD': 25, 'SM FLSH OP ERR': 32, 'SM FLSH CFG ERR': 33, 'SM FLSH CRC IVLD': 34, 'SM PARAM ID UNKOWN': 40, 'SM PARAM VALUE IVLD': 41, 'SM CAT RING LIMIT': 42, 'ZE TC IVLD': 128, 'ZE TC LEN IVLD': 129, 'ZE STATE FOR TC IVLD': 130, 'ZE CMD CODE UNKOWN': 131, 'ZE TC PARAM IVLD': 132, 'ZE TC CAN RX BUF FUL': 133, 'ZE CAN BUS ERR': 134, 'MV NO ERR': 0, 'ZE TC NOT IMPL': 135, 'ZE INVLD DEBUG MODE': 136, 'ZE FLSH OP ERR': 144, 'ZE FLSH OP LEN IVLD': 145, 'ZE FLSH CFG ERR': 146, 'ZE FLSH CRC IVLD': 147, 'ZE NO SM ACTIVE': 160, 'ZE SM ID NOT RESP': 161, 'ZE SM ID NO ACT MASK': 162, 'ZE SM ID MARK DEFECT': 163, 'ZE SM ID IVLD': 164, 'ZE NO MCU COORDIN': 168, 'ZE BOTH MCU COORDIN': 169, 'ZE OTHR MCU NOT RESP': 176, 'ZE UART COMM ERR': 177, 'ZE UART PKG LEN IVLD': 178, 'ZE UART CRC IVLD': 179, 'ZE UART TC UNKOWN': 180, 'ZE UART PARAM IVLD': 181, 'ZE UART RX BUF FUL': 182, 'ZE HAL ERR HANDLER': 192, 'ZE TC CAN ID U': 137})
enum_201 = construct.Enum(construct.BitsInteger(1), **{'COORDINATOR': 0, 'FORWARDER': 1})
enum_202 = construct.Enum(construct.BitsInteger(3), **{'ZE_IDLE': 0, 'ZE_ATTI_DET': 1, 'ZE_SM_CHANGE': 2, 'ZE_IMG_CAPT_GRAB': 3, 'ZE_CTLG_OP': 4, 'ZE_SM_SW_APPLY': 5, 'ZE_DATA_UPL_DWNL': 6, 'ZE_RELAY': 7})
enum_203 = construct.Enum(construct.BitsInteger(1), **{'UART IF 1': 0, 'UART IF 2': 1})
enum_204 = construct.Enum(construct.BitsInteger(1), **{'RESPONDING': 1, 'NOT RESPONDING': 0})
enum_205 = construct.Enum(construct.BitsInteger(8), **{'SM TC LEN IVLD': 16, 'SM STATE FOR TC IVLD': 17, 'SM CMD CODE UNKOWN': 18, 'SM TC PARAM IVLD': 19, 'SM TC CAN RX BUF FUL': 20, 'SM CAN MSG TOO SHORT': 21, 'SM CAN BUS ERR': 22, 'SM TC NOT IMPL': 23, 'SM CAN BUS TIMEOUT': 24, 'SM CALIB MODE IVLD': 25, 'SM FLSH OP ERR': 32, 'SM FLSH CFG ERR': 33, 'SM FLSH CRC IVLD': 34, 'SM PARAM ID UNKOWN': 40, 'SM PARAM VALUE IVLD': 41, 'SM CAT RING LIMIT': 42, 'ZE TC IVLD': 128, 'ZE TC LEN IVLD': 129, 'ZE STATE FOR TC IVLD': 130, 'ZE CMD CODE UNKOWN': 131, 'ZE TC PARAM IVLD': 132, 'ZE TC CAN RX BUF FUL': 133, 'ZE CAN BUS ERR': 134, 'MV NO ERR': 0, 'ZE TC NOT IMPL': 135, 'ZE INVLD DEBUG MODE': 136, 'ZE FLSH OP ERR': 144, 'ZE FLSH OP LEN IVLD': 145, 'ZE FLSH CFG ERR': 146, 'ZE FLSH CRC IVLD': 147, 'ZE NO SM ACTIVE': 160, 'ZE SM ID NOT RESP': 161, 'ZE SM ID NO ACT MASK': 162, 'ZE SM ID MARK DEFECT': 163, 'ZE SM ID IVLD': 164, 'ZE NO MCU COORDIN': 168, 'ZE BOTH MCU COORDIN': 169, 'ZE OTHR MCU NOT RESP': 176, 'ZE UART COMM ERR': 177, 'ZE UART PGK LEN IVLD': 178, 'ZE UART CRC IVLD': 179, 'ZE UART TC UNKOWN': 180, 'ZE UART PARAM IVLD': 181, 'ZE UART RX BUF FUL': 182, 'ZE HAL ERR HANDLER': 192, 'ZE TC CAN ID U': 137})
enum_206 = construct.Enum(construct.BitsInteger(6), **{'SM_SLEEP': 0, 'SM_AD': 16, 'SM_DEL_FLASH': 48, 'SM_FLASH_COPY': 49, 'SM_CALC_CRC32': 50, 'SM_REPAIR_HIP': 53, 'SM_CALC_VEC_DB': 54, 'SM_RECV_WRITE_CAT': 51, 'SM_IMG_CAPTURE': 40, 'SM_CHECK_VEC_DB': 57})
enum_207 = construct.Enum(construct.BitsInteger(2), **{'OFF': 0, 'ON': 1, 'AUTO': 2, 'ILLIGAL_AC_MODE': 3})
enum_208 = construct.Enum(construct.BitsInteger(1), **{'AD_SYNC_PIN': 0, 'AD_AUTO_TRIG': 1})
enum_209 = construct.Enum(construct.BitsInteger(1), **{'RDY': 0, 'NONE RDY': 1})
enum_210 = construct.Enum(construct.BitsInteger(3), **{'AD NO ERR': 0, 'AD NO 3 STARS': 1, 'AD NO CENTER STAR': 2, 'AD NO NEIGH STAR1': 3, 'AD NO NEIGH STAR2': 4, 'AD TOO BIG OBJECT': 5, 'AD TOO BRIGHT': 6})
enum_211 = construct.Enum(construct.BitsInteger(1), **{'SM PARAMS NOT AVAIL': 0, 'SM PARAMS AVAIL': 1})
enum_212 = construct.Enum(construct.BitsInteger(5), **{'SM CATAL UPDATE': 0, 'SM SW UPDATE': 1, 'SM CAPTURE IMG': 2, 'SM CHANGE': 3, 'EXT DATA UPLOAD': 4, 'EXT DATA DOWNLOAD': 5, 'ZE FLASH OP TC': 6})
enum_213 = construct.Enum(construct.BitsInteger(3), **{'NOT RUNNING': 0, 'RUNNING': 1, 'SUCCESSFUL': 2, 'ABORTED': 3, 'ERROR': 4})
enum_214 = construct.Enum(construct.BitsInteger(4), **{'NO ERROR': 0, 'ILL CMD': 1, 'ILL PARAM': 2, 'CFG REPAIRED': 3, 'CHARGE NOT EN': 4, 'CHARGE T/O': 5, 'CHARGE TOO SHORT': 6, 'CHARGE HW FAULT': 7, 'CHARGE RET WARN': 8, 'IGNITOR NOT EN': 9, 'TEMP1 LIMIT': 10, 'TEMP2 LIMIT': 11, 'TEMP3 LIMIT': 12, 'TEMPI2C LIMIT': 13, 'I2C ERR': 14, 'CFG REPAIR FAILED': 15})
enum_215 = construct.Enum(construct.BitsInteger(4), **{'NO FIX': 0, 'VALID SPS MODE': 1, 'VALID DIFF MODE': 2, 'VALID PPS MODE': 3, 'FIXED RTK': 4, 'FLOAT RTK': 5, 'ESTIMATED': 6, 'MANUAL': 7, 'SIMULATION': 8})
enum_216 = construct.Enum(construct.BitsInteger(5), **{'NO ERROR': 0, 'ILL CMD': 1, 'CFG REPAIR 1-2 GOOD': 2, 'CFG TRIPLE RED SUCC': 3, 'CFG TRIPLE RED FAIL': 4, 'CAN BUSY TIMEOUT': 5, 'CAN RX BUF OVERRUN': 6, 'GNSS RX BUF OVERRUN': 7, 'GNSS BUF OVERRUN': 8, 'INVALID NMEA': 9, 'NMEA NOT PARSED': 10, 'RMC PARSE FAILED': 11, 'GGA PARSE FAILED': 12, 'GSV PARSE FAILED': 13, 'ZDA PARSE FAILED': 14, 'GSV PARSE ILLEG SYS': 15, 'PREP COMPLETE': 16, 'GNSS MEM NOT ERASE': 17, 'GNSS REC START': 18, 'GNSS REC STOP': 19, 'PREP FAILED': 20})

std_hk = construct.BitStruct(
    '_name' / construct.Computed('std_hk'),
    'name' / construct.Computed('STD HK'),
    'O1UPTM' / common.TimeDeltaAdapter(construct.BitsInteger(24)),
    'O1RSTC' / construct.BitsInteger(6),
    'O1CMDC' / construct.BitsInteger(4),
    'O1PWRS' / enum_0,  # 0=OFF, 1=ON
    'O1ROLE' / enum_1,  # 0=NO ROLE, 4=OBDH PASSIVE 3, 5=OBDH PASSIVE 2, 6=OBDH PASSIVE 1, 7=OBDH ACTIVE, 3=PDH ACTIVE, 1=BOOTLOADER
    'O1ECNT' / construct.BitsInteger(6),
    'O1ECDE' / enum_2,  # 1=CONFIG, 2=ROLE MANAGER, 3=NFM CONTROLLER, 4=STD TC EXECUTER, 5=STD TC RECEIVER, 6=STD TC SAVER, 7=SOFTWARE WDG, 8=OBDH TC RECEIVER, 9=SYSTEM MANAGER, 10=CAN 1, 11=CAN 2, 12=SYNCH 1, 13=SYNCH 2, 14=SYNCH 3, 15=SYNCH 4, 16=LINKINTERFACE CAN 1, 17=LINKINTERFACE CAN 2, 0=NO ERROR, 18=HOUSEKEEPER, 19=TM DOWNLINK, 20=STORAGE MONITOR, 21=PARALLEL NOR 1, 22=PARALLEL NOR 2, 23=SPI NOR , 24=SRAM 1, 25=SRAM 2, 26=SRAM CONTROLLER, 27=PAYLOAD HANDLER, 28=SOFTWARE INSTALLER, 29=MEMOP MANAGER, 30=SOFTWARE UPLOAD, 31=REPAIR AND CHECK, 32=VHF 1, 33=VHF 2, 34=UHF 1, 35=UHF 2, 36=EGSE 1, 37=EGSE 2, 38=EXP DATA HANDLER, 39=SAFE MODE LIMIT, 50=BTLDR NO ERROR, 51=BTLDR INVLD ADDR, 52=BTLDR INVLD SECTOR, 53=BTLDR INVLD SIZE, 54=BTLDR INVLD CMD, 55=BTLDR UNKNOWN CMD, 56=BTLDR CAN OVFLW, 57=BTLDR INVLD CRC, 58=BTLDR APP IMG DEFECT, 40=SBAND, 41=BOOT MSG HANDLER, 59=BTLDR RDP L1 SET, 60=BTLDR RDP L2 SET, 61=BTLDR WRP SET, 42=CAN LISTENER, 63=BTLDR DEFECT
    'O2UPTM' / common.TimeDeltaAdapter(construct.BitsInteger(24)),
    'O2RSTC' / construct.BitsInteger(6),
    'O2CMDC' / construct.BitsInteger(4),
    'O2PWRS' / enum_0,  # 0=OFF, 1=ON
    'O2ROLE' / enum_1,  # 0=NO ROLE, 4=OBDH PASSIVE 3, 5=OBDH PASSIVE 2, 6=OBDH PASSIVE 1, 7=OBDH ACTIVE, 3=PDH ACTIVE, 1=BOOTLOADER
    'O2ECNT' / construct.BitsInteger(6),
    'O2ECDE' / enum_2,  # 1=CONFIG, 2=ROLE MANAGER, 3=NFM CONTROLLER, 4=STD TC EXECUTER, 5=STD TC RECEIVER, 6=STD TC SAVER, 7=SOFTWARE WDG, 8=OBDH TC RECEIVER, 9=SYSTEM MANAGER, 10=CAN 1, 11=CAN 2, 12=SYNCH 1, 13=SYNCH 2, 14=SYNCH 3, 15=SYNCH 4, 16=LINKINTERFACE CAN 1, 17=LINKINTERFACE CAN 2, 0=NO ERROR, 18=HOUSEKEEPER, 19=TM DOWNLINK, 20=STORAGE MONITOR, 21=PARALLEL NOR 1, 22=PARALLEL NOR 2, 23=SPI NOR , 24=SRAM 1, 25=SRAM 2, 26=SRAM CONTROLLER, 27=PAYLOAD HANDLER, 28=SOFTWARE INSTALLER, 29=MEMOP MANAGER, 30=SOFTWARE UPLOAD, 31=REPAIR AND CHECK, 32=VHF 1, 33=VHF 2, 34=UHF 1, 35=UHF 2, 36=EGSE 1, 37=EGSE 2, 39=SAFE MODE LIMIT, 38=EXP DATA HANDLER, 50=BTLDR NO ERROR, 51=BTLDR INVLD ADDR, 52=BTLDR INVLD SECTOR, 53=BTLDR INVLD SIZE, 54=BTLDR INVLD CMD, 55=BTLDR UNKNOWN CMD, 56=BTLDR CAN OVFLW, 57=BTLDR INVLD CRC, 58=BTLDR APP IMG DEFECT, 40=SBAND, 41=BOOT MSG HANDLER, 59=BTLDR RDP L1 SET, 60=BTLDR RDP L2 SET, 61=BTLDR WRP SET, 42=CAN LISTENER, 63=BTLDR DEFECT
    'O3UPTM' / common.TimeDeltaAdapter(construct.BitsInteger(24)),
    'O3RSTC' / construct.BitsInteger(6),
    'O3CMDC' / construct.BitsInteger(4),
    'O3PWRS' / enum_0,  # 0=OFF, 1=ON
    'O3ROLE' / enum_1,  # 0=NO ROLE, 4=OBDH PASSIVE 3, 5=OBDH PASSIVE 2, 6=OBDH PASSIVE 1, 7=OBDH ACTIVE, 3=PDH ACTIVE, 1=BOOTLOADER
    'O3ECNT' / construct.BitsInteger(6),
    'O3ECDE' / enum_2,  # 1=CONFIG, 2=ROLE MANAGER, 3=NFM CONTROLLER, 4=STD TC EXECUTER, 5=STD TC RECEIVER, 6=STD TC SAVER, 7=SOFTWARE WDG, 8=OBDH TC RECEIVER, 9=SYSTEM MANAGER, 10=CAN 1, 11=CAN 2, 12=SYNCH 1, 13=SYNCH 2, 14=SYNCH 3, 15=SYNCH 4, 16=LINKINTERFACE CAN 1, 17=LINKINTERFACE CAN 2, 0=NO ERROR, 18=HOUSEKEEPER, 19=TM DOWNLINK, 20=STORAGE MONITOR, 21=PARALLEL NOR 1, 22=PARALLEL NOR 2, 23=SPI NOR , 24=SRAM 1, 25=SRAM 2, 26=SRAM CONTROLLER, 27=PAYLOAD HANDLER, 28=SOFTWARE INSTALLER, 29=MEMOP MANAGER, 30=SOFTWARE UPLOAD, 31=REPAIR AND CHECK, 32=VHF 1, 33=VHF 2, 34=UHF 1, 35=UHF 2, 36=EGSE 1, 37=EGSE 2, 38=EXP DATA HANDLER, 39=SAFE MODE LIMIT, 50=BTLDR NO ERROR, 51=BTLDR INVLD ADDR, 52=BTLDR INVLD SECTOR, 53=BTLDR INVLD SIZE, 54=BTLDR INVLD CMD, 55=BTLDR UNKNOWN CMD, 56=BTLDR CAN OVFLW, 57=BTLDR INVLD CRC, 58=BTLDR APP IMG DEFECT, 40=SBAND, 41=BOOT MSG HANDLER, 59=BTLDR RDP L1 SET, 60=BTLDR RDP L2 SET, 61=BTLDR WRP SET, 42=CAN LISTENER, 63=BTLDR DEFECT
    'O4UPTM' / common.TimeDeltaAdapter(construct.BitsInteger(24)),
    'O4RSTC' / construct.BitsInteger(6),
    'O4CMDC' / construct.BitsInteger(4),
    'O4PWRS' / enum_0,  # 0=OFF, 1=ON
    'O4ROLE' / enum_1,  # 0=NO ROLE, 4=OBDH PASSIVE 3, 5=OBDH PASSIVE 2, 6=OBDH PASSIVE 1, 7=OBDH ACTIVE, 3=PDH ACTIVE, 1=BOOTLOADER
    'O4ECNT' / construct.BitsInteger(6),
    'O4ECDE' / enum_3,  # 1=CONFIG, 2=ROLE MANAGER, 3=NFM CONTROLLER, 4=STD TC EXECUTER, 5=STD TC RECEIVER, 6=STD TC SAVER, 7=SOFTWARE WDG, 8=OBDH TC RECEIVER, 9=SYSTEM MANAGER, 10=CAN 1, 11=CAN 2, 12=SYNCH 1, 13=SYNCH 2, 14=SYNCH 3, 15=SYNCH 4, 16=LINKINTERFACE CAN 1, 17=LINKINTERFACE CAN 2, 0=NO ERROR, 18=HOUSEKEEPER, 19=TM DONWLINK, 20=STORAGE MONITOR, 21=PARALLEL NOR 1, 22=PARALLEL NOR 2, 23=SPI NOR , 24=SRAM 1, 25=SRAM 2, 26=SRAM CONTROLLER, 27=PAYLOAD HANDLER, 28=SOFTWARE INSTALLER, 29=MEMOP MANAGER, 30=SOFTWARE UPLOAD, 31=REPAIR AND CHECK, 32=VHF 1, 33=VHF 2, 34=UHF 1, 35=UHF 2, 36=EGSE 1, 37=EGSE 2, 38=EXP DATA HANDLER, 39=SAFE MODE LIMIT, 50=BTLDR NO ERROR, 51=BTLDR INVLD ADDR, 52=BTLDR INVLD SECTOR, 53=BTLDR INVLD SIZE, 54=BTLDR INVLD CMD, 55=BTLDR UNKNOWN CMD, 56=BTLDR CAN OVFLW, 57=BTLDR INVLD CRC, 58=BTLDR APP IMG DEFECT, 40=SBAND, 41=BOOT MSG HANDLER, 59=BTLDR RDP L1 SET, 60=BTLDR RDP L2 SET, 61=BTLDR WRP SET, 42=CAN LISTENER, 63=BTLDR DEFECT
    'PDHHWI' / enum_4,  # 0=NONE, 4=OBDH 1, 5=OBDH 2, 6=OBDH 3, 7=OBDH 4
    'CMDACN' / construct.BitsInteger(12),
    'CMDPCN' / construct.BitsInteger(12),
    'CMDEEC' / construct.BitsInteger(4),
    'CMDEED' / enum_5,  # 0=NO ERROR, 1=CMD NOT SUPPORTED, 2=CMD OVERDUE WARNING, 3=CMD OVERDUE ERROR, 4=CMD CRC ERROR, 5=CMD FLASH BUSY, 6=CMD TT ERROR, 7=CMD INVALID SINK, 8=CMD EXEC FAILED BOTH, 9=CMD INVALID LENGTH, 10=CMD INVALID TYPE, 11=CMD INVALID CODE, 12=CMD INVALID EXE SINK, 13=CMD EXEC FAILED BUS1, 14=CMD EXEC FAILED BUS2
    'CMDSRC' / enum_6,  # 8=NONE, 4=EGSE 1, 0=VHF 1, 1=VHF 2, 2=UHF 1, 3=UHF 2, 6=S-BAND 1, 7=S-BAND 2, 5=EGSE 2
    'CMDECE' / construct.BitsInteger(4),
    'CAN1RS' / enum_7,  # 1=NORMAL, 2=WARN SOFT, 3=WARN CRITIC, 4=PASSIVE, 5=OFF, 7=NULLPTR, 0=NOT INIT
    'CAN1TS' / enum_7,  # 1=NORMAL, 2=WARN SOFT, 3=WARN CRITIC, 4=PASSIVE, 5=OFF, 7=NULLPTR, 0=NOT INIT
    'CAN2RS' / enum_7,  # 1=NORMAL, 2=WARN SOFT, 3=WARN CRITIC, 4=PASSIVE, 5=OFF, 7=NULLPTR, 0=NOT INIT
    'CAN2TS' / enum_7,  # 1=NORMAL, 2=WARN SOFT, 3=WARN CRITIC, 4=PASSIVE, 5=OFF, 7=NULLPTR, 0=NOT INIT
    'OBMODE' / enum_8,  # 0=BOOT MODE, 2=LEOP MODE, 1=SAFE MODE, 3=NORMAL MODE, 4=PROCEDURE MODE, 6=USER MODE, 15=SIMULATOR, 5=BEACON MODE, 14=OBC LIGHT UHF, 13=OBC LIGHT VHF
    'TMSINK' / enum_9,  # 0=VHF 1, 1=VHF 2, 2=UHF 1, 3=UHF 2, 8=NONE, 4=EGSE 1, 5=EGSE 2, 6=S-BAND 1, 7=S-BAND 2, 10=VHF 1 + S-BAND, 11=VHF 2 + S-BAND, 12=UHF 1 + S-BAND, 13=UHF 2 + S-BAND, 14=EGSE 1 + S-BAND, 15=EGSE 2 + S-BAND
    'GPCTHW' / enum_10,  # 0=OBDH 1, 1=OBDH 2, 2=OBDH 3, 3=OBDH 4, 7=NONE
    'SWUPHW' / enum_4,  # 0=NONE, 4=OBDH 1, 5=OBDH 2, 6=OBDH 3, 7=OBDH 4
    'SWINHW' / enum_4,  # 0=NONE, 4=OBDH 1, 5=OBDH 2, 6=OBDH 3, 7=OBDH 4
    'SBCTHW' / enum_4,  # 0=NONE, 4=OBDH 1, 5=OBDH 2, 6=OBDH 3, 7=OBDH 4
    'CMDCNT' / construct.BitsInteger(12),
    'VHF1MO' / enum_11,  # 0=N/A, 2=SSTV, 3=CW, 1=TMTC, 4=APRS, 5=DEPLOY, 6=DEPLOY OVERRIDE
    'VHF1TC' / construct.BitsInteger(5),
    'VHF1TM' / common.EvalAdapter('-128*x**0 +  1*x**1', construct.BitsInteger(8)),  # -128*x^0 +  1*x^1
    'VHF1RS' / common.EvalAdapter('-256*x**0 +  1*x**1', construct.BitsInteger(8)),  # -256*x^0 +  1*x^1
    'VHF1RA' / common.EvalAdapter('-256*x**0 +  1*x**1', construct.BitsInteger(8)),  # -256*x^0 +  1*x^1
    'VHF1TO' / enum_12,  # 15=31.5, 14=31.4, 13=31.0, 12=30.0, 11=28.5, 10=28.2, 9=28.1, 8=27.4, 7=26.0, 6=24.0, 5=21.2, 4=16.5, 3=7.0, 2=N/A, 1=N/A, 0=0 - PA OFF
    'VHF1EC' / enum_13,  # 0=NO ERROR, 1=ILLEGAL CMD, 2=ILLEGAL PARAM, 3=I²C ERROR, 4=TX PACKET ORDER, 5=TX PACKET TIMEOUT, 6=TX PACKET OVERRUN, 7=AUTORANGING RX, 8=AUTORANGING TX, 9=RX CRC FAIL, 10=RX ABORT, 11=RX SIZE FAIL, 12=RX ADDR FAIL, 13=CFG REPAIR 1-2 GOOD, 14=RX PACKET OVERRUN, 15=APRS RX BUF OVERRUN, 16=PREP COMPLETE, 17=TC DEC UNEXP LEN, 18=TC DEC CRC ERR, 19=CAN RX BUF OVERRUN, 20=CAN BUSY TIMEOUT, 21=UNEXP IMG UPL STATE, 22=ILL IMG UPL START, 23=IMG UPL ABORT, 24=IMG UPL PKT CRC, 25=IMG UPL CRC, 26=TRX FAIL, 27=DEPLOY TIMEOUT, 28=CFG TRIPLE RED SUCC, 29=CFG TRIPLE RED FAIL, 30=OBCL CAN REC OVERRUN, 31=UNEXP RX FIFO ERR
    'VHF1CC' / construct.BitsInteger(4),
    'VHF1EN' / construct.BitsInteger(4),
    'VHF1RC' / construct.BitsInteger(5),
    'VHF2MO' / enum_14,  # 0=N/A, 1=TMTC, 2=SSTV, 3=CW, 4=APRS, 5=DEPLOY, 6=DEPLOY_OVERRIDE
    'VHF2TC' / construct.BitsInteger(5),
    'VHF2TM' / common.EvalAdapter('-128*x**0 +  1*x**1', construct.BitsInteger(8)),  # -128*x^0 +  1*x^1
    'VHF2RS' / common.EvalAdapter('-256*x**0 +  1*x**1', construct.BitsInteger(8)),  # -256*x^0 +  1*x^1
    'VHF2RA' / common.EvalAdapter('-256*x**0 +  1*x**1', construct.BitsInteger(8)),  # -256*x^0 +  1*x^1
    'VHF2TO' / enum_15,  # 15=31.7, 14=31.6, 13=31.4, 12=30.9, 11=29.7, 10=29.6, 9=29.5, 8=28.9, 7=28.1, 6=26.7, 5=24.9, 4=21.9, 3=16.8, 2=7.0, 1=N/A, 0=0 - PA OFF
    'VHF2EC' / enum_13,  # 0=NO ERROR, 1=ILLEGAL CMD, 2=ILLEGAL PARAM, 3=I²C ERROR, 4=TX PACKET ORDER, 5=TX PACKET TIMEOUT, 6=TX PACKET OVERRUN, 7=AUTORANGING RX, 8=AUTORANGING TX, 9=RX CRC FAIL, 10=RX ABORT, 11=RX SIZE FAIL, 12=RX ADDR FAIL, 13=CFG REPAIR 1-2 GOOD, 14=RX PACKET OVERRUN, 15=APRS RX BUF OVERRUN, 16=PREP COMPLETE, 17=TC DEC UNEXP LEN, 18=TC DEC CRC ERR, 19=CAN RX BUF OVERRUN, 20=CAN BUSY TIMEOUT, 21=UNEXP IMG UPL STATE, 22=ILL IMG UPL START, 23=IMG UPL ABORT, 24=IMG UPL PKT CRC, 25=IMG UPL CRC, 26=TRX FAIL, 27=DEPLOY TIMEOUT, 28=CFG TRIPLE RED SUCC, 29=CFG TRIPLE RED FAIL, 30=OBCL CAN REC OVERRUN, 31=UNEXP RX FIFO ERR
    'VHF2CC' / construct.BitsInteger(4),
    'VHF2EN' / construct.BitsInteger(4),
    'VHF2RC' / construct.BitsInteger(5),
    'UHF1MO' / enum_11,  # 0=N/A, 2=SSTV, 3=CW, 1=TMTC, 4=APRS, 5=DEPLOY, 6=DEPLOY OVERRIDE
    'UHF1TM' / common.EvalAdapter('-128*x**0 +  1*x**1', construct.BitsInteger(8)),  # -128*x^0 +  1*x^1
    'UHF1RS' / common.EvalAdapter('-256*x**0 +  1*x**1', construct.BitsInteger(8)),  # -256*x^0 +  1*x^1
    'UHF1RA' / common.EvalAdapter('-256*x**0 +  1*x**1', construct.BitsInteger(8)),  # -256*x^0 +  1*x^1
    'UHF1TO' / enum_16,  # 15=30.6, 14=30.0, 13=28.8, 12=27.7, 11=25.7, 10=24.4, 9=22.5, 8=18.3, 7=3.0, 6=N/A, 5=N/A, 4=N/A, 3=N/A, 2=N/A, 1=N/A, 0=0 - PA OFF
    'UHF1EC' / enum_13,  # 0=NO ERROR, 1=ILLEGAL CMD, 2=ILLEGAL PARAM, 3=I²C ERROR, 4=TX PACKET ORDER, 5=TX PACKET TIMEOUT, 6=TX PACKET OVERRUN, 7=AUTORANGING RX, 8=AUTORANGING TX, 9=RX CRC FAIL, 10=RX ABORT, 11=RX SIZE FAIL, 12=RX ADDR FAIL, 13=CFG REPAIR 1-2 GOOD, 14=RX PACKET OVERRUN, 15=APRS RX BUF OVERRUN, 16=PREP COMPLETE, 17=TC DEC UNEXP LEN, 18=TC DEC CRC ERR, 19=CAN RX BUF OVERRUN, 20=CAN BUSY TIMEOUT, 21=UNEXP IMG UPL STATE, 22=ILL IMG UPL START, 23=IMG UPL ABORT, 24=IMG UPL PKT CRC, 25=IMG UPL CRC, 26=TRX FAIL, 27=DEPLOY TIMEOUT, 28=CFG TRIPLE RED SUCC, 29=CFG TRIPLE RED FAIL, 30=OBCL CAN REC OVERRUN, 31=UNEXP RX FIFO ERR
    'UHF1CC' / construct.BitsInteger(4),
    'UHF1EN' / construct.BitsInteger(4),
    'UHF1RC' / construct.BitsInteger(5),
    'UHF2MO' / enum_11,  # 0=N/A, 2=SSTV, 3=CW, 1=TMTC, 4=APRS, 5=DEPLOY, 6=DEPLOY OVERRIDE
    'UHF2TM' / common.EvalAdapter('-128*x**0 +  1*x**1', construct.BitsInteger(8)),  # -128*x^0 +  1*x^1
    'UHF2RS' / common.EvalAdapter('-256*x**0 +  1*x**1', construct.BitsInteger(8)),  # -256*x^0 +  1*x^1
    'UHF2RA' / common.EvalAdapter('-256*x**0 +  1*x**1', construct.BitsInteger(8)),  # -256*x^0 +  1*x^1
    'UHF2TO' / enum_17,  # 15=30.7, 14=30.4, 13=29.5, 12=28.4, 11=27.1, 10=26.2, 9=24.3, 8=20.7, 7=7.8, 6=N/A, 5=N/A, 4=N/A, 3=N/A, 2=N/A, 1=N/A, 0=0 - PA OFF
    'UHF2EC' / enum_13,  # 0=NO ERROR, 1=ILLEGAL CMD, 2=ILLEGAL PARAM, 3=I²C ERROR, 4=TX PACKET ORDER, 5=TX PACKET TIMEOUT, 6=TX PACKET OVERRUN, 7=AUTORANGING RX, 8=AUTORANGING TX, 9=RX CRC FAIL, 10=RX ABORT, 11=RX SIZE FAIL, 12=RX ADDR FAIL, 13=CFG REPAIR 1-2 GOOD, 14=RX PACKET OVERRUN, 15=APRS RX BUF OVERRUN, 16=PREP COMPLETE, 17=TC DEC UNEXP LEN, 18=TC DEC CRC ERR, 19=CAN RX BUF OVERRUN, 20=CAN BUSY TIMEOUT, 21=UNEXP IMG UPL STATE, 22=ILL IMG UPL START, 23=IMG UPL ABORT, 24=IMG UPL PKT CRC, 25=IMG UPL CRC, 26=TRX FAIL, 27=DEPLOY TIMEOUT, 28=CFG TRIPLE RED SUCC, 29=CFG TRIPLE RED FAIL, 30=OBCL CAN REC OVERRUN, 31=UNEXP RX FIFO ERR
    'UHF2CC' / construct.BitsInteger(4),
    'UHF2EN' / construct.BitsInteger(4),
    'UHF2RC' / construct.BitsInteger(5),
    'P5V1CC' / construct.BitsInteger(4),
    'P5V1PG' / enum_18,  # 0=YES, 1=NO
    'P5V1PF' / enum_19,  # 0=FAULT, 1=NO FAULT
    'P5V1UE' / enum_20,  # 1=OFF, 0=ON
    'P5V1PE' / enum_20,  # 1=OFF, 0=ON
    'P5V1EO' / enum_21,  # 0=NO ERROR, 1=ILLEGAL CMD, 2=ILLEGAL PARAM, 3=CFG REPAIR 1-2 GOOD, 4=I2C ERR, 5=CMD RX BUF OVERRUN, 6=CFG TRIPLE RED SUCC, 7=CFG TRIPLE RED FAIL, 8=PWR NOT GOOD 5V->12V
    'P5V1EC' / construct.BitsInteger(4),
    'P5V1AV' / common.EvalAdapter('0.020070588*x', construct.BitsInteger(8)),  # 0.020070588*x
    'P5V1AC' / common.EvalAdapter('-7.641924759*x**0 +  0.059702537*x**1', construct.BitsInteger(8)),  # -7.641924759*x^0 +  0.059702537*x^1
    'P5V1UV' / common.EvalAdapter('0.020813943*x', construct.BitsInteger(8)),  # 0.020813943*x
    'P5V1UC' / common.EvalAdapter('0.029734205*x', construct.BitsInteger(8)),  # 0.029734205*x
    'P5V1BV' / common.EvalAdapter('0.024530719*x', construct.BitsInteger(8)),  # 0.024530719*x
    'P5V1BC' / common.EvalAdapter('0.029734205*x', construct.BitsInteger(8)),  # 0.029734205*x
    'P5V2CC' / construct.BitsInteger(4),
    'P5V2PG' / enum_18,  # 0=YES, 1=NO
    'P5V2PF' / enum_19,  # 0=FAULT, 1=NO FAULT
    'P5V2UE' / enum_20,  # 1=OFF, 0=ON
    'P5V2PE' / enum_20,  # 1=OFF, 0=ON
    'P5V2EO' / enum_21,  # 0=NO ERROR, 1=ILLEGAL CMD, 2=ILLEGAL PARAM, 3=CFG REPAIR 1-2 GOOD, 4=I2C ERR, 5=CMD RX BUF OVERRUN, 6=CFG TRIPLE RED SUCC, 7=CFG TRIPLE RED FAIL, 8=PWR NOT GOOD 5V->12V
    'P5V2EC' / construct.BitsInteger(4),
    'P5V2AV' / common.EvalAdapter('0.019882353*x', construct.BitsInteger(8)),  # 0.019882353*x
    'P5V2AC' / common.EvalAdapter('-7.570253718*x**0 +  0.059142607*x**1', construct.BitsInteger(8)),  # -7.570253718*x^0 +  0.059142607*x^1
    'P5V2UV' / common.EvalAdapter('0.020618736*x', construct.BitsInteger(8)),  # 0.020618736*x
    'P5V2UC' / common.EvalAdapter('0.029455338*x', construct.BitsInteger(8)),  # 0.029455338*x
    'P5V2BV' / common.EvalAdapter('0.024300654*x', construct.BitsInteger(8)),  # 0.024300654*x
    'P5V2BC' / common.EvalAdapter('0.029455338*x', construct.BitsInteger(8)),  # 0.029455338*x
    'P5V1BT' / common.EvalAdapter('-47.23889465*x**0 +  0.548218308*x**1 +  0.0000195267*x**2', construct.BitsInteger(8)),  # -47.23889465*x^0 +  0.548218308*x^1 +  0.0000195267*x^2
    '12V1BT' / common.EvalAdapter('-43.91789355*x**0 +  0.0000128733*x**2 +  0.534063389*x**1', construct.BitsInteger(8)),  # -43.91789355*x^0 +  0.0000128733*x^2 +  0.534063389*x^1
    'SXP1PS' / enum_0,  # 1=ON, 0=OFF
    'SXN1PS' / enum_0,  # 1=ON, 0=OFF
    'SYP1PS' / enum_0,  # 1=ON, 0=OFF
    'SYN1PS' / enum_0,  # 1=ON, 0=OFF
    'SZP1PS' / enum_0,  # 1=ON, 0=OFF
    'SZN1PS' / enum_0,  # 1=ON, 0=OFF
    'ADS1PS' / enum_0,  # 1=ON, 0=OFF
    'MVW1PS' / enum_0,  # 1=ON, 0=OFF
    'THR1PS' / enum_0,  # 1=ON, 0=OFF
    'IFP1PS' / enum_0,  # 1=ON, 0=OFF
    'P5V1PS' / enum_22,  # 0=RESET, 1=SET
    'P5V1HA' / enum_23,  # 1=TRUE, 0=FALSE
    'THR1PG' / enum_24,  # 0=FAULT, 1=GOOD
    'P5V1RS' / enum_0,  # 0=OFF, 1=ON
    'P5V1CS' / enum_0,  # 0=OFF, 1=ON
    'P5V111' / enum_25,  # 0=NOT AVAILABLE, 1=AVAILABLE
    'P5V121' / enum_25,  # 0=NOT AVAILABLE, 1=AVAILABLE
    'P5V122' / enum_25,  # 0=NOT AVAILABLE, 1=AVAILABLE
    'P5V1TR' / enum_25,  # 0=NOT AVAILABLE, 1=AVAILABLE
    'P5V1RM' / enum_26,  # 0=PFM, 1=PWM
    'P5V2BT' / common.EvalAdapter('-45.19886296*x**0 +  0.553555222*x**1 +  0.0000198982*x**2', construct.BitsInteger(8)),  # -45.19886296*x^0 +  0.553555222*x^1 +  0.0000198982*x^2
    '12V2BT' / common.EvalAdapter('-44.08916192*x**0 +  0.0000128531*x**2 +  0.53363536*x**1', construct.BitsInteger(8)),  # -44.08916192*x^0 +  0.0000128531*x^2 +  0.53363536*x^1
    'SXP2PS' / enum_0,  # 1=ON, 0=OFF
    'SXN2PS' / enum_0,  # 1=ON, 0=OFF
    'SYP2PS' / enum_0,  # 1=ON, 0=OFF
    'SYN2PS' / enum_0,  # 1=ON, 0=OFF
    'SZP2PS' / enum_0,  # 1=ON, 0=OFF
    'SZN2PS' / enum_0,  # 1=ON, 0=OFF
    'ADS2PS' / enum_0,  # 1=ON, 0=OFF
    'MVW2PS' / enum_0,  # 1=ON, 0=OFF
    'THR2PS' / enum_0,  # 1=ON, 0=OFF
    'IFP2PS' / enum_0,  # 1=ON, 0=OFF
    'P5V2PS' / enum_22,  # 0=RESET, 1=SET
    'P5V2HA' / enum_23,  # 1=TRUE, 0=FALSE
    'THR2PG' / enum_24,  # 0=FAULT, 1=GOOD
    'P5V2RS' / enum_0,  # 0=OFF, 1=ON
    'P5V2CS' / enum_0,  # 0=OFF, 1=ON
    'P5V211' / enum_25,  # 0=NOT AVAILABLE, 1=AVAILABLE
    'P5V221' / enum_25,  # 0=NOT AVAILABLE, 1=AVAILABLE
    'P5V222' / enum_25,  # 0=NOT AVAILABLE, 1=AVAILABLE
    'P5V2TR' / enum_25,  # 0=NOT AVAILABLE, 1=AVAILABLE
    'P5V2RM' / enum_26,  # 0=PFM, 1=PWM
    '12V1CC' / construct.BitsInteger(4),
    '12V1PG' / enum_18,  # 0=YES, 1=NO
    '12V1PF' / enum_19,  # 0=FAULT, 1=NO FAULT
    '12V1UE' / enum_20,  # 1=OFF, 0=ON
    '12V1PE' / enum_20,  # 1=OFF, 0=ON
    '12V1EO' / enum_27,  # 0=NO ERROR, 1=ILLEGAL CMD, 2=ILLEGAL PARAM, 3=CFG REPAIR 1-2 GOOD, 4=CMD RX BUF OVERRUN, 5=CFG TRIPLE RED SUCC, 6=CFG TRIPLE RED FAIL
    '12V1EC' / construct.BitsInteger(4),
    '12V1AV' / common.EvalAdapter('0.019764706*x', construct.BitsInteger(8)),  # 0.019764706*x
    '12V1AC' / common.EvalAdapter('-7.525459318*x**0 +  0.058792651*x**1', construct.BitsInteger(8)),  # -7.525459318*x^0 +  0.058792651*x^1
    '12V1UV' / common.EvalAdapter('0.020496732*x', construct.BitsInteger(8)),  # 0.020496732*x
    '12V1UC' / common.EvalAdapter('0.029281046*x', construct.BitsInteger(8)),  # 0.029281046*x
    '12V1BV' / common.EvalAdapter('0.051930796*x', construct.BitsInteger(8)),  # 0.051930796*x
    '12V1BC' / common.EvalAdapter('0.029281046*x', construct.BitsInteger(8)),  # 0.029281046*x
    '12V2CC' / construct.BitsInteger(4),
    '12V2PG' / enum_18,  # 0=YES, 1=NO
    '12V2PF' / enum_19,  # 0=FAULT, 1=NO FAULT
    '12V2UE' / enum_20,  # 1=OFF, 0=ON
    '12V2PE' / enum_20,  # 1=OFF, 0=ON
    '12V2EO' / enum_27,  # 0=NO ERROR, 1=ILLEGAL CMD, 2=ILLEGAL PARAM, 3=CFG REPAIR 1-2 GOOD, 4=CMD RX BUF OVERRUN, 5=CFG TRIPLE RED SUCC, 6=CFG TRIPLE RED FAIL
    '12V2EC' / construct.BitsInteger(4),
    '12V2AV' / common.EvalAdapter('0.019823529*x', construct.BitsInteger(8)),  # 0.019823529*x
    '12V2AC' / common.EvalAdapter('-7.547856518*x**0 +  0.058967629*x**1', construct.BitsInteger(8)),  # -7.547856518*x^0 +  0.058967629*x^1
    '12V2UV' / common.EvalAdapter('0.020557734*x', construct.BitsInteger(8)),  # 0.020557734*x
    '12V2UC' / common.EvalAdapter('0.029368192*x', construct.BitsInteger(8)),  # 0.029368192*x
    '12V2BV' / common.EvalAdapter('0.052085352*x', construct.BitsInteger(8)),  # 0.052085352*x
    '12V2BC' / common.EvalAdapter('0.029368192*x', construct.BitsInteger(8)),  # 0.029368192*x
    '12V1SS' / enum_28,  # 0=UNDEF, 1=CHARGING, 2=CHARGE COMPL, 3=FAULT
    'AI1PWS' / enum_0,  # 1=ON, 0=OFF
    '12V1HA' / enum_23,  # 1=TRUE, 0=FALSE
    '12V1CS' / enum_20,  # 1=OFF, 0=ON
    '12V1RM' / enum_26,  # 0=PFM, 1=PWM
    '12V2SS' / enum_28,  # 0=UNDEF, 1=CHARGING, 2=CHARGE COMPL, 3=FAULT
    'AI2PWS' / enum_0,  # 1=ON, 0=OFF
    '12V2HA' / enum_23,  # 1=TRUE, 0=FALSE
    '12V2CS' / enum_20,  # 0=ON, 1=OFF
    '12V2RM' / enum_26,  # 0=PFM, 1=PWM
    'IFP1ST' / enum_29,  # 1=IDLE, 2=DEPLOY_OVERRIDE, 3=DEPLOY, 0=OFF
    'SB1RXS' / enum_20,  # 0=ON, 1=OFF
    'SB1ENA' / enum_0,  # 0=OFF, 1=ON
    'RWX1PS' / enum_0,  # 1=ON, 0=OFF
    'RWY1PS' / enum_0,  # 1=ON, 0=OFF
    'RWZ1PS' / enum_0,  # 1=ON, 0=OFF
    'SB1TXS' / enum_0,  # 0=OFF, 1=ON
    'IFP1EN' / construct.BitsInteger(4),
    'IFP1EC' / enum_30,  # 0=NO ERROR, 1=ILLEGAL CMD, 2=ILLEGAL PARAM, 3=CFG REPAIR 1-2 GOOD, 4=DEPLOY TIMEOUT, 5=DEPLOY OVERCURRENT, 6=TORQ X FAULT, 7=TORQ Y FAULT, 8=TORQ Z FAULT, 9=TORQ X OVERCURRENT, 10=TORQ Y OVERCURRENT, 11=TORQ Z OVERCURRENT, 13=CFG TRIPLE RED SUCC, 14=CFG TRIPLE RED FAIL, 15=DEPLOY FAULT, 12=TORQ TIMEOUT
    'IFP1CC' / construct.BitsInteger(4),
    'IFP1AC' / construct.BitsInteger(4),
    'IFP2ST' / enum_29,  # 1=IDLE, 2=DEPLOY_OVERRIDE, 3=DEPLOY, 0=OFF
    'SB2RXS' / enum_20,  # 0=ON, 1=OFF
    'SB2ENA' / enum_0,  # 0=OFF, 1=ON
    'RWX2PS' / enum_0,  # 1=ON, 0=OFF
    'RWY2PS' / enum_0,  # 1=ON, 0=OFF
    'RWZ2PS' / enum_0,  # 1=ON, 0=OFF
    'SB2TXS' / enum_0,  # 0=OFF, 1=ON
    'IFP2EN' / construct.BitsInteger(4),
    'IFP2EC' / enum_30,  # 0=NO ERROR, 1=ILLEGAL CMD, 2=ILLEGAL PARAM, 3=CFG REPAIR 1-2 GOOD, 4=DEPLOY TIMEOUT, 5=DEPLOY OVERCURRENT, 6=TORQ X FAULT, 7=TORQ Y FAULT, 8=TORQ Z FAULT, 9=TORQ X OVERCURRENT, 10=TORQ Y OVERCURRENT, 11=TORQ Z OVERCURRENT, 12=TORQ TIMEOUT, 13=CFG TRIPLE RED SUCC, 14=CFG TRIPLE RED FAIL, 15=DEPLOY FAULT
    'IFP2CC' / construct.BitsInteger(4),
    'IFP2AC' / construct.BitsInteger(4),
    '_pad0' / construct.BitsInteger(3),
)

obdh_ext_mem_ops_hk = construct.BitStruct(
    '_name' / construct.Computed('obdh_ext_mem_ops_hk'),
    'name' / construct.Computed('OBDH EXT MEM OPS HK'),
    'O1MOAV' / enum_25,  # 0=NOT AVAILABLE, 1=AVAILABLE
    'O1MOST' / enum_31,  # 0=IDLE, 1=SENDING, 2=RECEIVING, 3=LOCAL MEMCPY, 4=ERASING, 5=BLANK CHECK
    'O1MOPR' / common.EvalAdapter('0.3921568627*x', construct.BitsInteger(8)),  # 0.3921568627*x
    'O1MOEO' / enum_32,  # 0=NO ERROR, 1=ACK TIMEOUT, 2=MANAGER BUSY, 3=MEM OVERLAP, 4=WRITE ERROR, 5=READ ERROR, 6=ERASE ERROR, 7=INVLD PARAM, 8=BLNK CHK ERR, 9=SUCCESSFUL, 10=RX TIMEOUT, 11=RETRY LIMIT, 12=FORBID ADDR
    'O1MOEC' / construct.BitsInteger(4),
    'O2MOAV' / enum_25,  # 0=NOT AVAILABLE, 1=AVAILABLE
    'O2MOST' / enum_31,  # 0=IDLE, 1=SENDING, 2=RECEIVING, 3=LOCAL MEMCPY, 4=ERASING, 5=BLANK CHECK
    'O2MOPR' / common.EvalAdapter('0.3921568627*x', construct.BitsInteger(8)),  # 0.3921568627*x
    'O2MOEO' / enum_32,  # 0=NO ERROR, 1=ACK TIMEOUT, 2=MANAGER BUSY, 3=MEM OVERLAP, 4=WRITE ERROR, 5=READ ERROR, 6=ERASE ERROR, 7=INVLD PARAM, 8=BLNK CHK ERR, 9=SUCCESSFUL, 10=RX TIMEOUT, 11=RETRY LIMIT, 12=FORBID ADDR
    'O2MOEC' / construct.BitsInteger(4),
    'O3MOAV' / enum_25,  # 0=NOT AVAILABLE, 1=AVAILABLE
    'O3MOST' / enum_31,  # 0=IDLE, 1=SENDING, 2=RECEIVING, 3=LOCAL MEMCPY, 4=ERASING, 5=BLANK CHECK
    'O3MOPR' / common.EvalAdapter('0.3921568627*x', construct.BitsInteger(8)),  # 0.3921568627*x
    'O3MOEO' / enum_32,  # 0=NO ERROR, 1=ACK TIMEOUT, 2=MANAGER BUSY, 3=MEM OVERLAP, 4=WRITE ERROR, 5=READ ERROR, 6=ERASE ERROR, 7=INVLD PARAM, 8=BLNK CHK ERR, 9=SUCCESSFUL, 10=RX TIMEOUT, 11=RETRY LIMIT, 12=FORBID ADDR
    'O3MOEC' / construct.BitsInteger(4),
    'O4MOAV' / enum_25,  # 0=NOT AVAILABLE, 1=AVAILABLE
    'O4MOST' / enum_31,  # 0=IDLE, 1=SENDING, 2=RECEIVING, 3=LOCAL MEMCPY, 4=ERASING, 5=BLANK CHECK
    'O4MOPR' / common.EvalAdapter('0.3921568627*x', construct.BitsInteger(8)),  # 0.3921568627*x
    'O4MOEO' / enum_32,  # 0=NO ERROR, 1=ACK TIMEOUT, 2=MANAGER BUSY, 3=MEM OVERLAP, 4=WRITE ERROR, 5=READ ERROR, 6=ERASE ERROR, 7=INVLD PARAM, 8=BLNK CHK ERR, 9=SUCCESSFUL, 10=RX TIMEOUT, 11=RETRY LIMIT, 12=FORBID ADDR
    'O4MOEC' / construct.BitsInteger(4),
)

pdh_pldt_hk = construct.BitStruct(
    '_name' / construct.Computed('pdh_pldt_hk'),
    'name' / construct.Computed('PDH PLDT HK'),
    'OPECNT' / construct.BitsInteger(4),
    'OPECDE' / enum_33,  # 0=NO ERROR, 1=INVLD STATE TRANS, 2=INVLD STATE, 3=TIMEOUT, 4=FLASH ER ERR, 5=INVLD PACKET NR, 6=INVLD PACKET CRC, 7=FLASH WR ERR, 8=FLASH RD ERR, 9=SRAM RD ERR, 10=INVLD ADDR, 11=INVLD FILE CRC, 12=FILE TO LARGE, 13=NACK RESPONSE, 14=SUCCESSFUL, 15=SPI CRC INVLD, 16=HS ENC INIT FAIL, 17=HS DEC INIT FAIL, 21=DTLS NOT IMPL, 22=DTLS OUT OF TO MEM, 23=DTLS BAD PATCH TYPE, 24=DTLS BAD COMPRESS, 25=DTLS INTERNAL ERR, 26=DTLS OUT OF SRC MEM, 27=DTLS CORRUPT PATCH, 28=DTLS ALREADY DONE, 29=DTLS SHORT HEADER, 30=DTLS PATCH DATA MSNG, 31=DTLS HEATHSRINK SINK, 32=DTLS HEATSHRINK POLL, 33=DTLS HEATSHRINK NULL, 34=DTLS ALREADY FAILED, 35=DTLS PATCH OVERFLOW, 36=DTLS HEATSHRINK HDR, 37=DTLS MEM READ FAIL, 38=DTLS MEM WRITE FAIL, 18=HS HDR FLAG FAIL, 19=HS HDR PARAMS FAIL, 20=HS HDR SIZE FAIL, 39=FORBID ADDR
    'OPCDWS' / enum_34,  # 0=IDLE, 1=LOCK CRC, 3=W4 START RESPONSE, 4=W4 DWNLD ANN, 5=W4 DATA XFER DONE, 6=END, 2=SEND START REQUEST
    'OPCUPS' / enum_35,  # 0=IDLE, 2=W4 START RESPONSE, 3=W4 ANNOUNCE ACK, 4=W4 DATA ACK, 5=END, 1=SEND START REQUST
    'OPHWID' / enum_36,  # 0=OBDH 1, 1=OBDH 2, 2=OBDH 3, 3=OBDH 4
    'OPIFAC' / enum_37,  # 1=YES, 0=NO
    'OPSUPS' / enum_38,  # 0=IDLE, 13=LOAD DATA, 14=SEND DATA, 15=W4 TRANSFER DONE, 18=END, 1=SET MODE, 2=GET MODE, 3=READ MODE, 4=SET FILE SIZE, 5=GET FILE SIZE, 6=READ FILE SIZE, 7=SET FILE CRC, 8=GET FILE CRC, 9=READ FILE CRC, 10=SET PACKET SIZE, 11=GET PACKET SIZE, 12=READ PACKET SIZE, 16=GET PACKET STS, 17=READ PACKET STS
    'OPDHOP' / enum_39,  # 2=CAN BUS 1, 3=CAN BUS 2, 0=NONE, 1=SPI, 4=SSTV, 6=COMPRESS, 7=DECOMPRESS, 5=DELTA UPDATE
    'OPSDWS' / enum_40,  # 0=IDLE, 1=LOCK CRC, 15=RECEIVE DATA, 16=W4 TRANSFER DONE, 17=WRITE DATA TO FLASH, 18=END, 2=SET MODE, 3=GET MODE, 4=READ MODE, 5=GET FILE SIZE, 6=READ FILE SIZE, 7=GET FILE CRC, 8=READ FILE CRC, 9=SET PACKET SIZE, 10=GET PACKET SIZE, 11=READ PACKET SIZE, 12=SET PACKET NR, 13=GET PACKET NR, 14=READ PACKET NR
    'OPPROG' / common.EvalAdapter('0.39215686*x', construct.BitsInteger(8)),  # 0.39215686*x
    'OPECRC' / construct.BitsInteger(32),
    'OPDTSZ' / construct.BitsInteger(32),
)

pdh_expdh_hk = construct.BitStruct(
    '_name' / construct.Computed('pdh_expdh_hk'),
    'name' / construct.Computed('PDH EXPDH HK'),
    'OPEXEC' / construct.BitsInteger(4),
    'OPEXEO' / enum_41,  # 0=NO ERROR, 1=FIFO FULL, 2=FLASH WR ERR, 3=FLASH ER ERR, 4=DATA TOO LARGE, 5=BUFFER FULL, 6=NO BUFFER FOUND, 7=INVLD BUFFER ID, 8=FLASH RD ERR, 9=BUFFER NOT EMPTY, 10=BUF ERASE ONGOING, 11=ERASE SUCCESS
    'OPDHEI' / enum_36,  # 0=OBDH 1, 1=OBDH 2, 2=OBDH 3, 3=OBDH 4
    'OPEXST' / enum_42,  # 1=ACTIVATED, 0=DEACTIVATED
    'OPBERO' / enum_42,  # 0=DEACTIVATED, 1=ACTIVATED
    'OPERES' / construct.BitsInteger(3),
    'OPEIAC' / enum_37,  # 1=YES, 0=NO
    'OPEX0I' / construct.BitsInteger(8),
    'OPEX0S' / enum_43,  # 1=ARMED, 0=DISARMED
    'OPEX0C' / construct.BitsInteger(23),
    'OPEX1I' / construct.BitsInteger(8),
    'OPEX1S' / enum_43,  # 1=ARMED, 0=DISARMED
    'OPEX1C' / construct.BitsInteger(23),
    'OPEX2I' / construct.BitsInteger(8),
    'OPEX2S' / enum_43,  # 1=ARMED, 0=DISARMED
    'OPEX2C' / construct.BitsInteger(23),
    'OPEX3I' / construct.BitsInteger(8),
    'OPEX3S' / enum_43,  # 1=ARMED, 0=DISARMED
    'OPEX3C' / construct.BitsInteger(23),
    'OPEX4I' / construct.BitsInteger(8),
    'OPEX4S' / enum_43,  # 1=ARMED, 0=DISARMED
    'OPEX4C' / construct.BitsInteger(23),
    'OPEX5I' / construct.BitsInteger(8),
    'OPEX5S' / enum_43,  # 1=ARMED, 0=DISARMED
    'OPEX5C' / construct.BitsInteger(23),
    'OPEX6I' / construct.BitsInteger(8),
    'OPEX6S' / enum_43,  # 1=ARMED, 0=DISARMED
    'OPEX6C' / construct.BitsInteger(23),
    'OPEX7I' / construct.BitsInteger(8),
    'OPEX7S' / enum_43,  # 1=ARMED, 0=DISARMED
    'OPEX7C' / construct.BitsInteger(23),
)

leop_hk = construct.BitStruct(
    '_name' / construct.Computed('leop_hk'),
    'name' / construct.Computed('LEOP HK'),
    'O1LEFA' / enum_25,  # 1=AVAILABLE, 0=NOT AVAILABLE
    'O1LEFS' / enum_44,  # 0=ARMED, 1=EXECUTED, 2=DISARMED
    'O2LEFA' / enum_25,  # 1=AVAILABLE, 0=NOT AVAILABLE
    'O2LEFS' / enum_44,  # 0=ARMED, 1=EXECUTED, 2=DISARMED
    'O3LEFA' / enum_25,  # 1=AVAILABLE, 0=NOT AVAILABLE
    'O3LEFS' / enum_44,  # 0=ARMED, 1=EXECUTED, 2=DISARMED
    'O4LEFA' / enum_25,  # 1=AVAILABLE, 0=NOT AVAILABLE
    'O4LEFS' / enum_44,  # 0=ARMED, 1=EXECUTED, 2=DISARMED
    'VA1DFB' / enum_45,  # 0=NOT DEPLOYED, 1=DEPLOYED
    'VA1DEN' / enum_46,  # 0=DISABLED, 1=ENABLED
    'VA1DDR' / enum_47,  # 0=CLOSING, 1=OPENING
    'VA1HAV' / enum_25,  # 0=NOT AVAILABLE, 1=AVAILABLE
    'VA1DPW' / common.EvalAdapter('0.3921569*x', construct.BitsInteger(8)),  # 0.3921569*x
    'VA2DFB' / enum_45,  # 0=NOT DEPLOYED, 1=DEPLOYED
    'VA2DEN' / enum_46,  # 0=DISABLED, 1=ENABLED
    'VA2DDR' / enum_47,  # 0=CLOSING, 1=OPENING
    'VA2HAV' / enum_25,  # 0=NOT AVAILABLE, 1=AVAILABLE
    'VA2DPW' / common.EvalAdapter('0.3921569*x', construct.BitsInteger(8)),  # 0.3921569*x
    'UA1DFB' / enum_45,  # 1=DEPLOYED, 0=NOT DEPLOYED
    'UA1DEN' / enum_46,  # 0=DISABLED, 1=ENABLED
    'UA1DDR' / enum_47,  # 0=CLOSING, 1=OPENING
    'UA1HAV' / enum_25,  # 0=NOT AVAILABLE, 1=AVAILABLE
    'UA1DPW' / common.EvalAdapter('0.3921569*x', construct.BitsInteger(8)),  # 0.3921569*x
    'UA2DFB' / enum_45,  # 1=DEPLOYED, 0=NOT DEPLOYED
    'UA2DEN' / enum_46,  # 0=DISABLED, 1=ENABLED
    'UA2DDR' / enum_47,  # 0=CLOSING, 1=OPENING
    'UA2HAV' / enum_25,  # 0=NOT AVAILABLE, 1=AVAILABLE
    'UA2DPW' / common.EvalAdapter('0.3921569*x', construct.BitsInteger(8)),  # 0.3921569*x
    'IF1DFT' / enum_19,  # 0=FAULT, 1=NO FAULT
    'IF1DFB' / enum_45,  # 1=DEPLOYED, 0=NOT DEPLOYED
    'IF1DEN' / enum_46,  # 1=ENABLED, 0=DISABLED
    'IF1DDR' / enum_47,  # 0=CLOSING, 1=OPENING
    'IF1DSR' / enum_48,  # 0=STBY, 1=ON
    'IF1DCU' / common.EvalAdapter('0.1612903226*x', construct.BitsInteger(10)),  # 0.1612903226*x
    'IF1DPW' / common.EvalAdapter('0.3921569*x', construct.BitsInteger(8)),  # 0.3921569*x
    'IF1LAV' / enum_25,  # 0=NOT AVAILABLE, 1=AVAILABLE
    'IF2DFT' / enum_19,  # 0=FAULT, 1=NO FAULT
    'IF2DFB' / enum_45,  # 1=DEPLOYED, 0=NOT DEPLOYED
    'IF2DEN' / enum_46,  # 0=DISABLED, 1=ENABLED
    'IF2DDR' / enum_47,  # 0=CLOSING, 1=OPENING
    'IF2DSR' / enum_48,  # 0=STBY, 1=ON
    'IF2DCU' / common.EvalAdapter('0.1612903226*x', construct.BitsInteger(10)),  # 0.1612903226*x
    'IF2DPW' / common.EvalAdapter('0.3921569*x', construct.BitsInteger(8)),  # 0.3921569*x
    'IF2LAV' / enum_25,  # 0=NOT AVAILABLE, 1=AVAILABLE
    '_pad0' / construct.BitsInteger(4),
)

obdh_ext_err_cde = construct.BitStruct(
    '_name' / construct.Computed('obdh_ext_err_cde'),
    'name' / construct.Computed('OBDH EXT ERR CDE'),
    'O1EOCF' / enum_49,  # 0=NO ERROR, 1=CFG 1 RD ERR, 4=CFG 1 CRC INVLD, 8=WRITE ERR, 9=ERASE ERR, 10=INIT FAILED, 5=CFG 2 CRC INVLD, 6=CFG 3 CRC INVLD, 7=CFG R CRC INVLD, 2=CFG 2 RD ERR, 3=CFG 3 RD ERR, 11=INT ADR INVLD, 12=INT ERS ERR, 13=INT WR ERR
    'O1ECCF' / construct.BitsInteger(4),
    'O1EORM' / enum_50,  # 0=NO ERROR, 1=CMD NOT KNWN, 2=CMD PARAM INVLD, 3=STATE INVLD, 4=RST PROT NACK, 5=UART TX ERROR, 6=ROLE COLLISION, 7=OBDH REBOOT, 8=MON OBDH TO, 9=NO FREE ROLE, 10=MON PART TO, 11=COM SRC UNKN, 12=NO RSP FIN, 13=NO RSP PRI, 14=NO RSP SEC, 15=NO RSP TER
    'O1ECRM' / construct.BitsInteger(4),
    'O1EONM' / enum_51,  # 0=NO ERROR, 1=INVLD ADDR, 2=PNOR1 WR TO, 3=PNOR2 WR TO, 4=SNOR WR TO, 5=PNOR1 WR ERR, 6=PNOR2 WR ERR, 7=SNOR WR ERR, 8=PNOR1 RD TO, 9=PNOR2 RD TO, 10=SNOR RD TO, 11=PNOR1 RD ERR, 12=PNOR2 RD ERR, 13=SNOR RD ERR, 14=PNOR1 ERS TO, 15=PNOR2 ERS TO, 16=SNOR ERS TO, 17=PNOR1 ERS ERR, 18=PNOR2 ERS ERR, 19=SMOR ERS ERR
    'O1ECNM' / construct.BitsInteger(3),
    'O1EOTE' / enum_52,  # 0=NO ERROR, 1=CMD NOT SUP, 2=CMD WARN OVD, 3=CMD ERR OVD, 4=CMD ERR CRC, 5=CDM FLASH BUSY, 6=CMD TT ERROR, 7=CMD INVLD SINK, 8=CMD EXE FAILED BOTH, 9=CMD INVLD LEN, 10=CMD INVLD TYPE, 11=CMD INVLD CDE, 12=CMD INVLD EXE SINK, 13=CMD EXE FAILED BUS1, 14=CMD EXE FAILED BUS2
    'O1ECTE' / construct.BitsInteger(4),
    'O1EOTR' / enum_53,  # 0=NO ERROR, 1=CRC INVLD, 2=BUFFER FULL, 6=INVLD CMD LEN
    'O1ECTR' / construct.BitsInteger(4),
    'O1EOTS' / enum_54,  # 0=NO ERROR, 1=LIST NOT INIT, 2=LIST FULL, 3=LIST EMPTY, 4=WRNG TT TYPE, 5=WRNG TIME ORD, 6=FLASH WR ERR, 7=FLASH RD ERR, 8=FLASH PRST ERR, 9=FLASH FIN ERR, 10=FLASH CLR ERR, 11=FLASH ERS ERR, 12=CRC INVLD, 13=LIST NOT FIN, 14=LIST INIT FAIL, 15=LIST ALR FIN, 16=NO REL TT IN ACT TT, 17=INVLD STRT TIME, 18=LIST NOT ENUF SP, 19=LIST NOT EMPTY, 20=SM PROC IMPOS, 21=LEOP PROC IMPOS, 22=PROC COPY TO SELF
    'O1ECTS' / construct.BitsInteger(3),
    'O1EOWD' / enum_55,  # 0=NO ERROR, 1=WARN WDG, 2=WARN ROLE MAN, 3=WARN HK, 6=WARN GAT CAN1, 7=WARN GAT CAN2, 4=WARN SYS MAN, 5=WARN TC, 8=WARN TM DOWN, 9=WARN STD CAN, 10=WARN STO MON, 16=ERR WDG, 17=ERR ROLE MAN, 18=ERR HK, 21=ERR GAT CAN1, 22=ERR GAT CAN2, 19=ERR SYS MAN, 20=ERR TC, 23=ERR TM DOWN, 24=ERR STD CAN, 25=ERR STO MON, 11=WARN PLD HDLR, 12=WARN SW INST, 26=ERR PLD HDLR, 27=ERR SW INST, 13=WARN S-BAND, 28=ERR S-BAND
    'O1ECWD' / construct.BitsInteger(3),
    'O1ECAV' / enum_25,  # 0=NOT AVAILABLE, 1=AVAILABLE
    'O1EOOT' / enum_56,  # 0=NO ERROR, 1=CRC INVLD, 2=BUFFER FULL, 3=INVLD SW MOD, 4=INVLD CMD CDE, 5=INVLD CMD PRM LEN, 6=INVLD CMD LEN, 7=INVLD CMD PARAM
    'O1ECOT' / construct.BitsInteger(4),
    'O2EOCF' / enum_57,  # 0=NO ERROR, 1=CFG 1 RD ERR, 2=CFG 2 RD ERR, 3=CFG 3 RD ERR, 4=CFG 1 CRC INVLD, 5=CFG 2 CRC INVLD, 6=CFG 3 CRC INVLD, 7=CFG R CRC INVLD, 8=WRITE ERR, 9=ERASE ERR, 10=INIT FAILED, 11=INT ADR INVLD, 12=INT ERS ERR, 13=INT WR ERR
    'O2ECCF' / construct.BitsInteger(4),
    'O2EORM' / enum_50,  # 0=NO ERROR, 1=CMD NOT KNWN, 2=CMD PARAM INVLD, 3=STATE INVLD, 4=RST PROT NACK, 5=UART TX ERROR, 6=ROLE COLLISION, 7=OBDH REBOOT, 8=MON OBDH TO, 9=NO FREE ROLE, 10=MON PART TO, 11=COM SRC UNKN, 12=NO RSP FIN, 13=NO RSP PRI, 14=NO RSP SEC, 15=NO RSP TER
    'O2ECRM' / construct.BitsInteger(4),
    'O2EONM' / enum_51,  # 0=NO ERROR, 1=INVLD ADDR, 2=PNOR1 WR TO, 3=PNOR2 WR TO, 4=SNOR WR TO, 5=PNOR1 WR ERR, 6=PNOR2 WR ERR, 7=SNOR WR ERR, 8=PNOR1 RD TO, 9=PNOR2 RD TO, 10=SNOR RD TO, 11=PNOR1 RD ERR, 12=PNOR2 RD ERR, 13=SNOR RD ERR, 14=PNOR1 ERS TO, 15=PNOR2 ERS TO, 16=SNOR ERS TO, 17=PNOR1 ERS ERR, 18=PNOR2 ERS ERR, 19=SMOR ERS ERR
    'O2ECNM' / construct.BitsInteger(3),
    'O2EOTE' / enum_52,  # 0=NO ERROR, 1=CMD NOT SUP, 2=CMD WARN OVD, 3=CMD ERR OVD, 4=CMD ERR CRC, 5=CDM FLASH BUSY, 6=CMD TT ERROR, 7=CMD INVLD SINK, 8=CMD EXE FAILED BOTH, 9=CMD INVLD LEN, 10=CMD INVLD TYPE, 11=CMD INVLD CDE, 12=CMD INVLD EXE SINK, 13=CMD EXE FAILED BUS1, 14=CMD EXE FAILED BUS2
    'O2ECTE' / construct.BitsInteger(4),
    'O2EOTR' / enum_53,  # 0=NO ERROR, 1=CRC INVLD, 2=BUFFER FULL, 6=INVLD CMD LEN
    'O2ECTR' / construct.BitsInteger(4),
    'O2EOTS' / enum_54,  # 0=NO ERROR, 1=LIST NOT INIT, 2=LIST FULL, 3=LIST EMPTY, 4=WRNG TT TYPE, 5=WRNG TIME ORD, 6=FLASH WR ERR, 7=FLASH RD ERR, 8=FLASH PRST ERR, 9=FLASH FIN ERR, 10=FLASH CLR ERR, 11=FLASH ERS ERR, 12=CRC INVLD, 13=LIST NOT FIN, 14=LIST INIT FAIL, 15=LIST ALR FIN, 16=NO REL TT IN ACT TT, 17=INVLD STRT TIME, 18=LIST NOT ENUF SP, 19=LIST NOT EMPTY, 20=SM PROC IMPOS, 21=LEOP PROC IMPOS, 22=PROC COPY TO SELF
    'O2ECTS' / construct.BitsInteger(3),
    'O2EOWD' / enum_58,  # 0=NO ERROR, 7=WARN GAT CAN2, 8=WARN TM DOWN, 9=WARN STD CAN, 10=WARN STO MON, 11=WARN PLD HDLR, 12=WARN SW INST, 13=WARN S-BAND, 16=ERR WDG, 17=ERR ROLE MAN, 18=ERR HK, 19=ERR SYS MAN, 20=ERR TC, 21=ERR GAT CAN1, 22=ERR GAT CAN2, 23=ERR TM DOWN, 24=ERR STD CAN, 25=ERR STO MON, 26=ERR PLD HDLR, 27=ERR SW INST, 28=ERR S-BAND, 3=WARN HK, 4=WARN SYS MAN, 5=WARN TC, 6=WARN GAT CAN1, 1=WARN WDG, 2=WARN ROLE MAN
    'O2ECWD' / construct.BitsInteger(3),
    'O2ECAV' / enum_25,  # 0=NOT AVAILABLE, 1=AVAILABLE
    'O2EOOT' / enum_56,  # 0=NO ERROR, 1=CRC INVLD, 2=BUFFER FULL, 3=INVLD SW MOD, 4=INVLD CMD CDE, 5=INVLD CMD PRM LEN, 6=INVLD CMD LEN, 7=INVLD CMD PARAM
    'O2ECOT' / construct.BitsInteger(4),
    'O3EOCF' / enum_57,  # 0=NO ERROR, 1=CFG 1 RD ERR, 2=CFG 2 RD ERR, 3=CFG 3 RD ERR, 4=CFG 1 CRC INVLD, 5=CFG 2 CRC INVLD, 6=CFG 3 CRC INVLD, 7=CFG R CRC INVLD, 8=WRITE ERR, 9=ERASE ERR, 10=INIT FAILED, 11=INT ADR INVLD, 12=INT ERS ERR, 13=INT WR ERR
    'O3ECCF' / construct.BitsInteger(4),
    'O3EORM' / enum_50,  # 0=NO ERROR, 1=CMD NOT KNWN, 2=CMD PARAM INVLD, 3=STATE INVLD, 4=RST PROT NACK, 5=UART TX ERROR, 6=ROLE COLLISION, 7=OBDH REBOOT, 8=MON OBDH TO, 9=NO FREE ROLE, 10=MON PART TO, 11=COM SRC UNKN, 12=NO RSP FIN, 13=NO RSP PRI, 14=NO RSP SEC, 15=NO RSP TER
    'O3ECRM' / construct.BitsInteger(4),
    'O3EONM' / enum_51,  # 0=NO ERROR, 1=INVLD ADDR, 2=PNOR1 WR TO, 3=PNOR2 WR TO, 4=SNOR WR TO, 5=PNOR1 WR ERR, 6=PNOR2 WR ERR, 7=SNOR WR ERR, 8=PNOR1 RD TO, 9=PNOR2 RD TO, 10=SNOR RD TO, 11=PNOR1 RD ERR, 12=PNOR2 RD ERR, 13=SNOR RD ERR, 14=PNOR1 ERS TO, 15=PNOR2 ERS TO, 16=SNOR ERS TO, 17=PNOR1 ERS ERR, 18=PNOR2 ERS ERR, 19=SMOR ERS ERR
    'O3ECNM' / construct.BitsInteger(3),
    'O3EOTE' / enum_52,  # 0=NO ERROR, 1=CMD NOT SUP, 2=CMD WARN OVD, 3=CMD ERR OVD, 4=CMD ERR CRC, 5=CDM FLASH BUSY, 6=CMD TT ERROR, 7=CMD INVLD SINK, 8=CMD EXE FAILED BOTH, 9=CMD INVLD LEN, 10=CMD INVLD TYPE, 11=CMD INVLD CDE, 12=CMD INVLD EXE SINK, 13=CMD EXE FAILED BUS1, 14=CMD EXE FAILED BUS2
    'O3ECTE' / construct.BitsInteger(4),
    'O3EOTR' / enum_53,  # 0=NO ERROR, 1=CRC INVLD, 2=BUFFER FULL, 6=INVLD CMD LEN
    'O3ECTR' / construct.BitsInteger(4),
    'O3EOTS' / enum_54,  # 0=NO ERROR, 1=LIST NOT INIT, 2=LIST FULL, 3=LIST EMPTY, 4=WRNG TT TYPE, 5=WRNG TIME ORD, 6=FLASH WR ERR, 7=FLASH RD ERR, 8=FLASH PRST ERR, 9=FLASH FIN ERR, 10=FLASH CLR ERR, 11=FLASH ERS ERR, 12=CRC INVLD, 13=LIST NOT FIN, 14=LIST INIT FAIL, 15=LIST ALR FIN, 16=NO REL TT IN ACT TT, 17=INVLD STRT TIME, 18=LIST NOT ENUF SP, 19=LIST NOT EMPTY, 20=SM PROC IMPOS, 21=LEOP PROC IMPOS, 22=PROC COPY TO SELF
    'O3ECTS' / construct.BitsInteger(3),
    'O3EOWD' / enum_58,  # 0=NO ERROR, 7=WARN GAT CAN2, 8=WARN TM DOWN, 9=WARN STD CAN, 10=WARN STO MON, 11=WARN PLD HDLR, 12=WARN SW INST, 13=WARN S-BAND, 16=ERR WDG, 17=ERR ROLE MAN, 18=ERR HK, 19=ERR SYS MAN, 20=ERR TC, 21=ERR GAT CAN1, 22=ERR GAT CAN2, 23=ERR TM DOWN, 24=ERR STD CAN, 25=ERR STO MON, 26=ERR PLD HDLR, 27=ERR SW INST, 28=ERR S-BAND, 3=WARN HK, 4=WARN SYS MAN, 5=WARN TC, 6=WARN GAT CAN1, 1=WARN WDG, 2=WARN ROLE MAN
    'O3ECWD' / construct.BitsInteger(3),
    'O3ECAV' / enum_25,  # 0=NOT AVAILABLE, 1=AVAILABLE
    'O3EOOT' / enum_56,  # 0=NO ERROR, 1=CRC INVLD, 2=BUFFER FULL, 3=INVLD SW MOD, 4=INVLD CMD CDE, 5=INVLD CMD PRM LEN, 6=INVLD CMD LEN, 7=INVLD CMD PARAM
    'O3ECOT' / construct.BitsInteger(4),
    'O4EOCF' / enum_57,  # 0=NO ERROR, 1=CFG 1 RD ERR, 2=CFG 2 RD ERR, 3=CFG 3 RD ERR, 4=CFG 1 CRC INVLD, 5=CFG 2 CRC INVLD, 6=CFG 3 CRC INVLD, 7=CFG R CRC INVLD, 8=WRITE ERR, 9=ERASE ERR, 10=INIT FAILED, 11=INT ADR INVLD, 12=INT ERS ERR, 13=INT WR ERR
    'O4ECCF' / construct.BitsInteger(4),
    'O4EORM' / enum_50,  # 0=NO ERROR, 1=CMD NOT KNWN, 2=CMD PARAM INVLD, 3=STATE INVLD, 4=RST PROT NACK, 5=UART TX ERROR, 6=ROLE COLLISION, 7=OBDH REBOOT, 8=MON OBDH TO, 9=NO FREE ROLE, 10=MON PART TO, 11=COM SRC UNKN, 12=NO RSP FIN, 13=NO RSP PRI, 14=NO RSP SEC, 15=NO RSP TER
    'O4ECRM' / construct.BitsInteger(4),
    'O4EONM' / enum_51,  # 0=NO ERROR, 1=INVLD ADDR, 2=PNOR1 WR TO, 3=PNOR2 WR TO, 4=SNOR WR TO, 5=PNOR1 WR ERR, 6=PNOR2 WR ERR, 7=SNOR WR ERR, 8=PNOR1 RD TO, 9=PNOR2 RD TO, 10=SNOR RD TO, 11=PNOR1 RD ERR, 12=PNOR2 RD ERR, 13=SNOR RD ERR, 14=PNOR1 ERS TO, 15=PNOR2 ERS TO, 16=SNOR ERS TO, 17=PNOR1 ERS ERR, 18=PNOR2 ERS ERR, 19=SMOR ERS ERR
    'O4ECNM' / construct.BitsInteger(3),
    'O4EOTE' / enum_52,  # 0=NO ERROR, 1=CMD NOT SUP, 2=CMD WARN OVD, 3=CMD ERR OVD, 4=CMD ERR CRC, 5=CDM FLASH BUSY, 6=CMD TT ERROR, 7=CMD INVLD SINK, 8=CMD EXE FAILED BOTH, 9=CMD INVLD LEN, 10=CMD INVLD TYPE, 11=CMD INVLD CDE, 12=CMD INVLD EXE SINK, 13=CMD EXE FAILED BUS1, 14=CMD EXE FAILED BUS2
    'O4ECTE' / construct.BitsInteger(4),
    'O4EOTR' / enum_53,  # 0=NO ERROR, 1=CRC INVLD, 2=BUFFER FULL, 6=INVLD CMD LEN
    'O4ECTR' / construct.BitsInteger(4),
    'O4EOTS' / enum_54,  # 0=NO ERROR, 1=LIST NOT INIT, 2=LIST FULL, 3=LIST EMPTY, 4=WRNG TT TYPE, 5=WRNG TIME ORD, 6=FLASH WR ERR, 7=FLASH RD ERR, 8=FLASH PRST ERR, 9=FLASH FIN ERR, 10=FLASH CLR ERR, 11=FLASH ERS ERR, 12=CRC INVLD, 13=LIST NOT FIN, 14=LIST INIT FAIL, 15=LIST ALR FIN, 16=NO REL TT IN ACT TT, 17=INVLD STRT TIME, 18=LIST NOT ENUF SP, 19=LIST NOT EMPTY, 20=SM PROC IMPOS, 21=LEOP PROC IMPOS, 22=PROC COPY TO SELF
    'O4ECTS' / construct.BitsInteger(3),
    'O4EOWD' / enum_58,  # 0=NO ERROR, 7=WARN GAT CAN2, 8=WARN TM DOWN, 9=WARN STD CAN, 10=WARN STO MON, 11=WARN PLD HDLR, 12=WARN SW INST, 13=WARN S-BAND, 16=ERR WDG, 17=ERR ROLE MAN, 18=ERR HK, 19=ERR SYS MAN, 20=ERR TC, 21=ERR GAT CAN1, 22=ERR GAT CAN2, 23=ERR TM DOWN, 24=ERR STD CAN, 25=ERR STO MON, 26=ERR PLD HDLR, 27=ERR SW INST, 28=ERR S-BAND, 3=WARN HK, 4=WARN SYS MAN, 5=WARN TC, 6=WARN GAT CAN1, 1=WARN WDG, 2=WARN ROLE MAN
    'O4ECWD' / construct.BitsInteger(3),
    'O4ECAV' / enum_25,  # 0=NOT AVAILABLE, 1=AVAILABLE
    'O4EOOT' / enum_56,  # 0=NO ERROR, 1=CRC INVLD, 2=BUFFER FULL, 3=INVLD SW MOD, 4=INVLD CMD CDE, 5=INVLD CMD PRM LEN, 6=INVLD CMD LEN, 7=INVLD CMD PARAM
    'O4ECOT' / construct.BitsInteger(4),
    'O1EOSM' / enum_59,  # 0=NO ERROR, 1=TM RTC NEG VALUE, 2=TM RTC CNST VALUE, 7=FM LEOP BIT FLIP, 8=FM ERASE ERR, 9=FM LEOP WR ERR, 10=FM RST CNT WR ERR, 4=TM BUF PUSH FAIL, 5=TM BUF INIT FAIL, 6=TM BUF ERASE FAIL, 3=TM RTC SET FAIL, 11=CLK FAILURE, 12=TM RTC INIT FAIL, 13=TM RTC CALIB FAIL, 14=FM LEOP INVLD CHANGE
    'O1ECSM' / construct.BitsInteger(4),
    'O1EOHK' / enum_60,  # 0=NO ERROR, 1=INVLD REQ ST, 2=INVLD DWNLK APID, 3=INVLD REQ IDX, 4=RING BUF INIT FAIL, 5=FRAME NULLPTR, 6=SEND REQ FAIL, 7=INVLD ADR RNG, 8=ARCHIVE WR ERR, 9=INVLD STRT SEQ NR, 10=NO CAN FRAME RCVD, 11=SBAND NOT ACTIVE
    'O1ECHK' / construct.BitsInteger(4),
    'O1EOTD' / enum_61,  # 0=NO ERROR, 1=DNLK REQ BUF FULL, 2=TF ENC BYTE CPY ERR, 3=INVLD VC
    'O1ECTD' / construct.BitsInteger(4),
    'O1EOMM' / enum_62,  # 0=NO ERROR, 1=TC LIST CRC ERR, 2=NODE NR ERR, 3=HW ID ERR, 4=LAST TC REC TIME ERR, 5=OBDH MODE ERR, 6=OBDH ROLE ERR, 7=TM DNLK EN FLAG ERR, 8=CMD CTR ERR, 9=ACT RDO ERR, 10=GPIO CTRL ERR, 11=PLD HDLR ACT ERR, 12=SW INST FLAG ERR, 13=SW UPLD FLAG ERR, 14=HK ONL FRWRD ERR, 15=INTRNL IMG INVLD
    'O1ECMM' / construct.BitsInteger(4),
    'O1EOSC' / enum_63,  # 0=NO ERROR, 1=INVLD ADR, 2=SRAM1 WR ERR, 3=SRAM2 WR ERR, 4=SRAM1 RD ERR, 5=SRAM2 RD ERR
    'O1ECSC' / construct.BitsInteger(4),
    'O1EOV1' / enum_64,  # 0=NO ERROR, 1=WAIT TF ACK TO, 2=WAIT TF START TO, 3=WAIT TF STOP TO, 4=RADIO NACK, 5=ALIVE TO, 6=RST LIM, 7=TF IS NULL
    'O1ECV1' / construct.BitsInteger(4),
    'O1EOV2' / enum_64,  # 0=NO ERROR, 1=WAIT TF ACK TO, 2=WAIT TF START TO, 3=WAIT TF STOP TO, 4=RADIO NACK, 5=ALIVE TO, 6=RST LIM, 7=TF IS NULL
    'O1ECV2' / construct.BitsInteger(4),
    'O1EOU1' / enum_64,  # 0=NO ERROR, 1=WAIT TF ACK TO, 2=WAIT TF START TO, 3=WAIT TF STOP TO, 4=RADIO NACK, 5=ALIVE TO, 6=RST LIM, 7=TF IS NULL
    'O1ECU1' / construct.BitsInteger(4),
    'O2EOSM' / enum_65,  # 0=NO ERROR, 10=FM RST CNT WR ERR, 1=TM RTC NEG VALUE, 2=TM RTC CNST VALUE, 4=TM BUF PUSH FAIL, 5=TM BUF INIT FAIL, 6=TM BUF ERASE FAIL, 7=FM LEOP BIT FLIP, 8=FM ERASE ERR, 9=FM LEOP WR ERR, 3=TM RTC SET FAIL, 11=CLK FAILURE, 12=TM RTC INIT FAIL, 13=TM RTC CALIB FAIL, 14=FM LEOP INVLD CHANGE
    'O2ECSM' / construct.BitsInteger(4),
    'O2EOHK' / enum_60,  # 0=NO ERROR, 1=INVLD REQ ST, 2=INVLD DWNLK APID, 3=INVLD REQ IDX, 4=RING BUF INIT FAIL, 5=FRAME NULLPTR, 6=SEND REQ FAIL, 7=INVLD ADR RNG, 8=ARCHIVE WR ERR, 9=INVLD STRT SEQ NR, 10=NO CAN FRAME RCVD, 11=SBAND NOT ACTIVE
    'O2ECHK' / construct.BitsInteger(4),
    'O2EOTD' / enum_61,  # 0=NO ERROR, 1=DNLK REQ BUF FULL, 2=TF ENC BYTE CPY ERR, 3=INVLD VC
    'O2ECTD' / construct.BitsInteger(4),
    'O2EOMM' / enum_62,  # 0=NO ERROR, 1=TC LIST CRC ERR, 2=NODE NR ERR, 3=HW ID ERR, 4=LAST TC REC TIME ERR, 5=OBDH MODE ERR, 6=OBDH ROLE ERR, 7=TM DNLK EN FLAG ERR, 8=CMD CTR ERR, 9=ACT RDO ERR, 10=GPIO CTRL ERR, 11=PLD HDLR ACT ERR, 12=SW INST FLAG ERR, 13=SW UPLD FLAG ERR, 14=HK ONL FRWRD ERR, 15=INTRNL IMG INVLD
    'O2ECMM' / construct.BitsInteger(4),
    'O2EOSC' / enum_63,  # 0=NO ERROR, 1=INVLD ADR, 2=SRAM1 WR ERR, 3=SRAM2 WR ERR, 4=SRAM1 RD ERR, 5=SRAM2 RD ERR
    'O2ECSC' / construct.BitsInteger(4),
    'O2EOV1' / enum_64,  # 0=NO ERROR, 1=WAIT TF ACK TO, 2=WAIT TF START TO, 3=WAIT TF STOP TO, 4=RADIO NACK, 5=ALIVE TO, 6=RST LIM, 7=TF IS NULL
    'O2ECV1' / construct.BitsInteger(4),
    'O2EOV2' / enum_64,  # 0=NO ERROR, 1=WAIT TF ACK TO, 2=WAIT TF START TO, 3=WAIT TF STOP TO, 4=RADIO NACK, 5=ALIVE TO, 6=RST LIM, 7=TF IS NULL
    'O2ECV2' / construct.BitsInteger(4),
    'O2EOU1' / enum_64,  # 0=NO ERROR, 1=WAIT TF ACK TO, 2=WAIT TF START TO, 3=WAIT TF STOP TO, 4=RADIO NACK, 5=ALIVE TO, 6=RST LIM, 7=TF IS NULL
    'O2ECU1' / construct.BitsInteger(4),
    'O3EOSM' / enum_65,  # 0=NO ERROR, 10=FM RST CNT WR ERR, 1=TM RTC NEG VALUE, 2=TM RTC CNST VALUE, 4=TM BUF PUSH FAIL, 5=TM BUF INIT FAIL, 6=TM BUF ERASE FAIL, 7=FM LEOP BIT FLIP, 8=FM ERASE ERR, 9=FM LEOP WR ERR, 3=TM RTC SET FAIL, 11=CLK FAILURE, 12=TM RTC INIT FAIL, 13=TM RTC CALIB FAIL, 14=FM LEOP INVLD CHANGE
    'O3ECSM' / construct.BitsInteger(4),
    'O3EOHK' / enum_60,  # 0=NO ERROR, 1=INVLD REQ ST, 2=INVLD DWNLK APID, 3=INVLD REQ IDX, 4=RING BUF INIT FAIL, 5=FRAME NULLPTR, 6=SEND REQ FAIL, 7=INVLD ADR RNG, 8=ARCHIVE WR ERR, 9=INVLD STRT SEQ NR, 10=NO CAN FRAME RCVD, 11=SBAND NOT ACTIVE
    'O3ECHK' / construct.BitsInteger(4),
    'O3EOTD' / enum_61,  # 0=NO ERROR, 1=DNLK REQ BUF FULL, 2=TF ENC BYTE CPY ERR, 3=INVLD VC
    'O3ECTD' / construct.BitsInteger(4),
    'O3EOMM' / enum_62,  # 0=NO ERROR, 1=TC LIST CRC ERR, 2=NODE NR ERR, 3=HW ID ERR, 4=LAST TC REC TIME ERR, 5=OBDH MODE ERR, 6=OBDH ROLE ERR, 7=TM DNLK EN FLAG ERR, 8=CMD CTR ERR, 9=ACT RDO ERR, 10=GPIO CTRL ERR, 11=PLD HDLR ACT ERR, 12=SW INST FLAG ERR, 13=SW UPLD FLAG ERR, 14=HK ONL FRWRD ERR, 15=INTRNL IMG INVLD
    'O3ECMM' / construct.BitsInteger(4),
    'O3EOSC' / enum_63,  # 0=NO ERROR, 1=INVLD ADR, 2=SRAM1 WR ERR, 3=SRAM2 WR ERR, 4=SRAM1 RD ERR, 5=SRAM2 RD ERR
    'O3ECSC' / construct.BitsInteger(4),
    'O3EOV1' / enum_64,  # 0=NO ERROR, 1=WAIT TF ACK TO, 2=WAIT TF START TO, 3=WAIT TF STOP TO, 4=RADIO NACK, 5=ALIVE TO, 6=RST LIM, 7=TF IS NULL
    'O3ECV1' / construct.BitsInteger(4),
    'O3EOV2' / enum_64,  # 0=NO ERROR, 1=WAIT TF ACK TO, 2=WAIT TF START TO, 3=WAIT TF STOP TO, 4=RADIO NACK, 5=ALIVE TO, 6=RST LIM, 7=TF IS NULL
    'O3ECV2' / construct.BitsInteger(4),
    'O3EOU1' / enum_64,  # 0=NO ERROR, 1=WAIT TF ACK TO, 2=WAIT TF START TO, 3=WAIT TF STOP TO, 4=RADIO NACK, 5=ALIVE TO, 6=RST LIM, 7=TF IS NULL
    'O3ECU1' / construct.BitsInteger(4),
    'O4EOSM' / enum_65,  # 0=NO ERROR, 10=FM RST CNT WR ERR, 1=TM RTC NEG VALUE, 2=TM RTC CNST VALUE, 4=TM BUF PUSH FAIL, 5=TM BUF INIT FAIL, 6=TM BUF ERASE FAIL, 7=FM LEOP BIT FLIP, 8=FM ERASE ERR, 9=FM LEOP WR ERR, 3=TM RTC SET FAIL, 11=CLK FAILURE, 12=TM RTC INIT FAIL, 13=TM RTC CALIB FAIL, 14=FM LEOP INVLD CHANGE
    'O4ECSM' / construct.BitsInteger(4),
    'O4EOHK' / enum_60,  # 0=NO ERROR, 1=INVLD REQ ST, 2=INVLD DWNLK APID, 3=INVLD REQ IDX, 4=RING BUF INIT FAIL, 5=FRAME NULLPTR, 6=SEND REQ FAIL, 7=INVLD ADR RNG, 8=ARCHIVE WR ERR, 9=INVLD STRT SEQ NR, 10=NO CAN FRAME RCVD, 11=SBAND NOT ACTIVE
    'O4ECHK' / construct.BitsInteger(4),
    'O4EOTD' / enum_61,  # 0=NO ERROR, 1=DNLK REQ BUF FULL, 2=TF ENC BYTE CPY ERR, 3=INVLD VC
    'O4ECTD' / construct.BitsInteger(4),
    'O4EOMM' / enum_62,  # 0=NO ERROR, 1=TC LIST CRC ERR, 2=NODE NR ERR, 3=HW ID ERR, 4=LAST TC REC TIME ERR, 5=OBDH MODE ERR, 6=OBDH ROLE ERR, 7=TM DNLK EN FLAG ERR, 8=CMD CTR ERR, 9=ACT RDO ERR, 10=GPIO CTRL ERR, 11=PLD HDLR ACT ERR, 12=SW INST FLAG ERR, 13=SW UPLD FLAG ERR, 14=HK ONL FRWRD ERR, 15=INTRNL IMG INVLD
    'O4ECMM' / construct.BitsInteger(4),
    'O4EOSC' / enum_63,  # 0=NO ERROR, 1=INVLD ADR, 2=SRAM1 WR ERR, 3=SRAM2 WR ERR, 4=SRAM1 RD ERR, 5=SRAM2 RD ERR
    'O4ECSC' / construct.BitsInteger(4),
    'O4EOV1' / enum_64,  # 0=NO ERROR, 1=WAIT TF ACK TO, 2=WAIT TF START TO, 3=WAIT TF STOP TO, 4=RADIO NACK, 5=ALIVE TO, 6=RST LIM, 7=TF IS NULL
    'O4ECV1' / construct.BitsInteger(4),
    'O4EOV2' / enum_64,  # 0=NO ERROR, 1=WAIT TF ACK TO, 2=WAIT TF START TO, 3=WAIT TF STOP TO, 4=RADIO NACK, 5=ALIVE TO, 6=RST LIM, 7=TF IS NULL
    'O4ECV2' / construct.BitsInteger(4),
    'O4EOU1' / enum_64,  # 0=NO ERROR, 1=WAIT TF ACK TO, 2=WAIT TF START TO, 3=WAIT TF STOP TO, 4=RADIO NACK, 5=ALIVE TO, 6=RST LIM, 7=TF IS NULL
    'O4ECU1' / construct.BitsInteger(4),
    'O1EOU2' / enum_64,  # 0=NO ERROR, 1=WAIT TF ACK TO, 2=WAIT TF START TO, 3=WAIT TF STOP TO, 4=RADIO NACK, 5=ALIVE TO, 6=RST LIM, 7=TF IS NULL
    'O1ECU2' / construct.BitsInteger(4),
    'O1EOSL' / enum_66,  # 0=NO ERROR, 1=NEW OBDH ACTIVE, 2=NO PCU RESPONSE, 8=VBAT 5V BUS1 VIOL, 9=IBUS 5V BUS1 VIOL, 10=IUHF 5V BUS1 VIOL, 11=IVHF 5V BUS1 VIOL, 12=VBAT 5V BUS2 VIOL, 13=IBUS 5V BUS2 VIOL, 14=IUHF 5V BUS2 VIOL, 15=IVHF 5V BUS2 VIOL, 16=VBAT 12V BUS1 VIOL, 17=IBUS 12V BUS1 VIOL, 18=VBAT 12V BUS2 VIOL, 19=IBUS 12V BUS2 VIOL, 3=INVLD MODE, 4=RADIOS DEAD, 5=TC EXECUTION
    'O1ECSL' / construct.BitsInteger(3),
    'O2EOU2' / enum_64,  # 0=NO ERROR, 1=WAIT TF ACK TO, 2=WAIT TF START TO, 3=WAIT TF STOP TO, 4=RADIO NACK, 5=ALIVE TO, 6=RST LIM, 7=TF IS NULL
    'O2ECU2' / construct.BitsInteger(4),
    'O2EOSL' / enum_66,  # 0=NO ERROR, 1=NEW OBDH ACTIVE, 2=NO PCU RESPONSE, 8=VBAT 5V BUS1 VIOL, 9=IBUS 5V BUS1 VIOL, 10=IUHF 5V BUS1 VIOL, 11=IVHF 5V BUS1 VIOL, 12=VBAT 5V BUS2 VIOL, 13=IBUS 5V BUS2 VIOL, 14=IUHF 5V BUS2 VIOL, 15=IVHF 5V BUS2 VIOL, 16=VBAT 12V BUS1 VIOL, 17=IBUS 12V BUS1 VIOL, 18=VBAT 12V BUS2 VIOL, 19=IBUS 12V BUS2 VIOL, 3=INVLD MODE, 4=RADIOS DEAD, 5=TC EXECUTION
    'O2ECSL' / construct.BitsInteger(3),
    'O3EOU2' / enum_64,  # 0=NO ERROR, 1=WAIT TF ACK TO, 2=WAIT TF START TO, 3=WAIT TF STOP TO, 4=RADIO NACK, 5=ALIVE TO, 6=RST LIM, 7=TF IS NULL
    'O3ECU2' / construct.BitsInteger(4),
    'O3EOSL' / enum_66,  # 0=NO ERROR, 1=NEW OBDH ACTIVE, 2=NO PCU RESPONSE, 8=VBAT 5V BUS1 VIOL, 9=IBUS 5V BUS1 VIOL, 10=IUHF 5V BUS1 VIOL, 11=IVHF 5V BUS1 VIOL, 12=VBAT 5V BUS2 VIOL, 13=IBUS 5V BUS2 VIOL, 14=IUHF 5V BUS2 VIOL, 15=IVHF 5V BUS2 VIOL, 16=VBAT 12V BUS1 VIOL, 17=IBUS 12V BUS1 VIOL, 18=VBAT 12V BUS2 VIOL, 19=IBUS 12V BUS2 VIOL, 3=INVLD MODE, 4=RADIOS DEAD, 5=TC EXECUTION
    'O3ECSL' / construct.BitsInteger(3),
    'O4EOU2' / enum_64,  # 0=NO ERROR, 1=WAIT TF ACK TO, 2=WAIT TF START TO, 3=WAIT TF STOP TO, 4=RADIO NACK, 5=ALIVE TO, 6=RST LIM, 7=TF IS NULL
    'O4ECU2' / construct.BitsInteger(4),
    'O4EOSL' / enum_67,  # 0=NO ERROR, 1=NEW OBDH ACTIVE, 2=NO PCU RESPONSE, 8=VBAT 5V BUS1 VIOL, 9=IBUS 5V BUS1 VIOL, 10=IUHF 5V BUS1 VIOL, 11=IVHF 5V BUS1 VIOL, 12=VBAT 5V BUS2 VIOL, 13=IBUS 5V BUS2 VIOL, 14=IUHF 5V BUS2 VIOL, 15=IVHF 5V BUS2 VIOL, 16=VBAT 12V BUS1 VIOL, 17=IBUS 12V BUS1 VIOL, 18=VBAT 12V BUS2 VIOL, 19=IBUS 12V BUS2 VIOL, 3=INVLD MODE, 4=RADIOS DEAD, 5=TC ECECUTION
    'O4ECSL' / construct.BitsInteger(3),
)

obdh_ext_mem_sts = construct.BitStruct(
    '_name' / construct.Computed('obdh_ext_mem_sts'),
    'name' / construct.Computed('OBDH EXT MEM STS'),
    'O1LP1S' / enum_68,  # 0=NOT INIT, 1=NOT FINAL, 3=CRC NOT OK, 2=CRC OK
    'O1LP2S' / enum_68,  # 0=NOT INIT, 1=NOT FINAL, 3=CRC NOT OK, 2=CRC OK
    'O1LP3S' / enum_68,  # 0=NOT INIT, 1=NOT FINAL, 3=CRC NOT OK, 2=CRC OK
    'O1AS1S' / enum_68,  # 0=NOT INIT, 1=NOT FINAL, 3=CRC NOT OK, 2=CRC OK
    'O1AS2S' / enum_68,  # 0=NOT INIT, 1=NOT FINAL, 3=CRC NOT OK, 2=CRC OK
    'O1AS3S' / enum_68,  # 0=NOT INIT, 1=NOT FINAL, 3=CRC NOT OK, 2=CRC OK
    'O1PASS' / enum_68,  # 0=NOT INIT, 1=NOT FINAL, 3=CRC NOT OK, 2=CRC OK
    'O1R01S' / enum_68,  # 0=NOT INIT, 1=NOT FINAL, 3=CRC NOT OK, 2=CRC OK
    'O1R02S' / enum_68,  # 0=NOT INIT, 1=NOT FINAL, 3=CRC NOT OK, 2=CRC OK
    'O1R03S' / enum_68,  # 0=NOT INIT, 1=NOT FINAL, 3=CRC NOT OK, 2=CRC OK
    'O1R04S' / enum_68,  # 0=NOT INIT, 1=NOT FINAL, 3=CRC NOT OK, 2=CRC OK
    'O1R05S' / enum_68,  # 0=NOT INIT, 1=NOT FINAL, 3=CRC NOT OK, 2=CRC OK
    'O1R06S' / enum_68,  # 0=NOT INIT, 1=NOT FINAL, 3=CRC NOT OK, 2=CRC OK
    'O1R07S' / enum_68,  # 0=NOT INIT, 1=NOT FINAL, 3=CRC NOT OK, 2=CRC OK
    'O1R08S' / enum_68,  # 0=NOT INIT, 1=NOT FINAL, 3=CRC NOT OK, 2=CRC OK
    'O1R09S' / enum_68,  # 0=NOT INIT, 1=NOT FINAL, 3=CRC NOT OK, 2=CRC OK
    'O1R10S' / enum_68,  # 0=NOT INIT, 1=NOT FINAL, 3=CRC NOT OK, 2=CRC OK
    'O1R11S' / enum_68,  # 0=NOT INIT, 1=NOT FINAL, 3=CRC NOT OK, 2=CRC OK
    'O1R12S' / enum_68,  # 0=NOT INIT, 1=NOT FINAL, 3=CRC NOT OK, 2=CRC OK
    'O1R13S' / enum_68,  # 0=NOT INIT, 1=NOT FINAL, 3=CRC NOT OK, 2=CRC OK
    'O1R14S' / enum_68,  # 0=NOT INIT, 1=NOT FINAL, 3=CRC NOT OK, 2=CRC OK
    'O1R15S' / enum_68,  # 0=NOT INIT, 1=NOT FINAL, 3=CRC NOT OK, 2=CRC OK
    'O1R16S' / enum_68,  # 0=NOT INIT, 1=NOT FINAL, 3=CRC NOT OK, 2=CRC OK
    'O1CF1S' / enum_68,  # 0=NOT INIT, 1=NOT FINAL, 3=CRC NOT OK, 2=CRC OK
    'O1CF2S' / enum_68,  # 0=NOT INIT, 1=NOT FINAL, 3=CRC NOT OK, 2=CRC OK
    'O1CF3S' / enum_68,  # 0=NOT INIT, 1=NOT FINAL, 3=CRC NOT OK, 2=CRC OK
    'O1PTTS' / enum_69,  # 0=NOT INIT, 1=INITIALIZED
    'O1ATTS' / enum_69,  # 0=NOT INIT, 1=INITIALIZED
    'O1TMBS' / enum_69,  # 0=NOT INIT, 1=INITIALIZED
    'O1MRS1' / enum_69,  # 0=NOT INIT, 1=INITIALIZED
    'O1ACFG' / enum_70,  # 0=CONFIG 1, 1=CONFIG 2, 2=CONFIG 3, 3=CONFIG IMG
    'O1MSAV' / enum_25,  # 0=NOT AVAILABLE, 1=AVAILABLE
    'O1EMBS' / enum_69,  # 1=INITIALIZED, 0=NOT INIT
    'O2LP1S' / enum_68,  # 0=NOT INIT, 1=NOT FINAL, 3=CRC NOT OK, 2=CRC OK
    'O2LP2S' / enum_68,  # 0=NOT INIT, 1=NOT FINAL, 3=CRC NOT OK, 2=CRC OK
    'O2LP3S' / enum_68,  # 0=NOT INIT, 1=NOT FINAL, 3=CRC NOT OK, 2=CRC OK
    'O2AS1S' / enum_68,  # 0=NOT INIT, 1=NOT FINAL, 3=CRC NOT OK, 2=CRC OK
    'O2AS2S' / enum_68,  # 0=NOT INIT, 1=NOT FINAL, 3=CRC NOT OK, 2=CRC OK
    'O2AS3S' / enum_68,  # 0=NOT INIT, 1=NOT FINAL, 3=CRC NOT OK, 2=CRC OK
    'O2PASS' / enum_68,  # 0=NOT INIT, 1=NOT FINAL, 3=CRC NOT OK, 2=CRC OK
    'O2R01S' / enum_68,  # 0=NOT INIT, 1=NOT FINAL, 3=CRC NOT OK, 2=CRC OK
    'O2R02S' / enum_68,  # 0=NOT INIT, 1=NOT FINAL, 3=CRC NOT OK, 2=CRC OK
    'O2R03S' / enum_68,  # 0=NOT INIT, 1=NOT FINAL, 3=CRC NOT OK, 2=CRC OK
    'O2R04S' / enum_68,  # 0=NOT INIT, 1=NOT FINAL, 3=CRC NOT OK, 2=CRC OK
    'O2R05S' / enum_68,  # 0=NOT INIT, 1=NOT FINAL, 3=CRC NOT OK, 2=CRC OK
    'O2R06S' / enum_68,  # 0=NOT INIT, 1=NOT FINAL, 3=CRC NOT OK, 2=CRC OK
    'O2R07S' / enum_68,  # 0=NOT INIT, 1=NOT FINAL, 3=CRC NOT OK, 2=CRC OK
    'O2R08S' / enum_68,  # 0=NOT INIT, 1=NOT FINAL, 3=CRC NOT OK, 2=CRC OK
    'O2R09S' / enum_68,  # 0=NOT INIT, 1=NOT FINAL, 3=CRC NOT OK, 2=CRC OK
    'O2R10S' / enum_68,  # 0=NOT INIT, 1=NOT FINAL, 3=CRC NOT OK, 2=CRC OK
    'O2R11S' / enum_68,  # 0=NOT INIT, 1=NOT FINAL, 3=CRC NOT OK, 2=CRC OK
    'O2R12S' / enum_68,  # 0=NOT INIT, 1=NOT FINAL, 3=CRC NOT OK, 2=CRC OK
    'O2R13S' / enum_68,  # 0=NOT INIT, 1=NOT FINAL, 3=CRC NOT OK, 2=CRC OK
    'O2R14S' / enum_68,  # 0=NOT INIT, 1=NOT FINAL, 3=CRC NOT OK, 2=CRC OK
    'O2R15S' / enum_68,  # 0=NOT INIT, 1=NOT FINAL, 3=CRC NOT OK, 2=CRC OK
    'O2R16S' / enum_68,  # 0=NOT INIT, 1=NOT FINAL, 3=CRC NOT OK, 2=CRC OK
    'O2CF1S' / enum_68,  # 0=NOT INIT, 1=NOT FINAL, 3=CRC NOT OK, 2=CRC OK
    'O2CF2S' / enum_68,  # 0=NOT INIT, 1=NOT FINAL, 3=CRC NOT OK, 2=CRC OK
    'O2CF3S' / enum_68,  # 0=NOT INIT, 1=NOT FINAL, 3=CRC NOT OK, 2=CRC OK
    'O2PTTS' / enum_69,  # 0=NOT INIT, 1=INITIALIZED
    'O2ATTS' / enum_69,  # 0=NOT INIT, 1=INITIALIZED
    'O2TMBS' / enum_69,  # 0=NOT INIT, 1=INITIALIZED
    'O2MRS1' / enum_69,  # 0=NOT INIT, 1=INITIALIZED
    'O2ACFG' / enum_70,  # 0=CONFIG 1, 1=CONFIG 2, 2=CONFIG 3, 3=CONFIG IMG
    'O2MSAV' / enum_25,  # 0=NOT AVAILABLE, 1=AVAILABLE
    'O2EMBS' / enum_69,  # 1=INITIALIZED, 0=NOT INIT
    'O3LP1S' / enum_68,  # 0=NOT INIT, 1=NOT FINAL, 3=CRC NOT OK, 2=CRC OK
    'O3LP2S' / enum_68,  # 0=NOT INIT, 1=NOT FINAL, 3=CRC NOT OK, 2=CRC OK
    'O3LP3S' / enum_68,  # 0=NOT INIT, 1=NOT FINAL, 3=CRC NOT OK, 2=CRC OK
    'O3AS1S' / enum_68,  # 0=NOT INIT, 1=NOT FINAL, 3=CRC NOT OK, 2=CRC OK
    'O3AS2S' / enum_68,  # 0=NOT INIT, 1=NOT FINAL, 3=CRC NOT OK, 2=CRC OK
    'O3AS3S' / enum_68,  # 0=NOT INIT, 1=NOT FINAL, 3=CRC NOT OK, 2=CRC OK
    'O3PASS' / enum_68,  # 0=NOT INIT, 1=NOT FINAL, 3=CRC NOT OK, 2=CRC OK
    'O3R01S' / enum_68,  # 0=NOT INIT, 1=NOT FINAL, 3=CRC NOT OK, 2=CRC OK
    'O3R02S' / enum_68,  # 0=NOT INIT, 1=NOT FINAL, 3=CRC NOT OK, 2=CRC OK
    'O3R03S' / enum_68,  # 0=NOT INIT, 1=NOT FINAL, 3=CRC NOT OK, 2=CRC OK
    'O3R04S' / enum_68,  # 0=NOT INIT, 1=NOT FINAL, 3=CRC NOT OK, 2=CRC OK
    'O3R05S' / enum_68,  # 0=NOT INIT, 1=NOT FINAL, 3=CRC NOT OK, 2=CRC OK
    'O3R06S' / enum_68,  # 0=NOT INIT, 1=NOT FINAL, 3=CRC NOT OK, 2=CRC OK
    'O3R07S' / enum_68,  # 0=NOT INIT, 1=NOT FINAL, 3=CRC NOT OK, 2=CRC OK
    'O3R08S' / enum_68,  # 0=NOT INIT, 1=NOT FINAL, 3=CRC NOT OK, 2=CRC OK
    'O3R09S' / enum_68,  # 0=NOT INIT, 1=NOT FINAL, 3=CRC NOT OK, 2=CRC OK
    'O3R10S' / enum_68,  # 0=NOT INIT, 1=NOT FINAL, 3=CRC NOT OK, 2=CRC OK
    'O3R11S' / enum_68,  # 0=NOT INIT, 1=NOT FINAL, 3=CRC NOT OK, 2=CRC OK
    'O3R12S' / enum_68,  # 0=NOT INIT, 1=NOT FINAL, 3=CRC NOT OK, 2=CRC OK
    'O3R13S' / enum_68,  # 0=NOT INIT, 1=NOT FINAL, 3=CRC NOT OK, 2=CRC OK
    'O3R14S' / enum_68,  # 0=NOT INIT, 1=NOT FINAL, 3=CRC NOT OK, 2=CRC OK
    'O3R15S' / enum_68,  # 0=NOT INIT, 1=NOT FINAL, 3=CRC NOT OK, 2=CRC OK
    'O3R16S' / enum_68,  # 0=NOT INIT, 1=NOT FINAL, 3=CRC NOT OK, 2=CRC OK
    'O3CF1S' / enum_68,  # 0=NOT INIT, 1=NOT FINAL, 3=CRC NOT OK, 2=CRC OK
    'O3CF2S' / enum_68,  # 0=NOT INIT, 1=NOT FINAL, 3=CRC NOT OK, 2=CRC OK
    'O3CF3S' / enum_68,  # 0=NOT INIT, 1=NOT FINAL, 3=CRC NOT OK, 2=CRC OK
    'O3PTTS' / enum_69,  # 0=NOT INIT, 1=INITIALIZED
    'O3ATTS' / enum_69,  # 0=NOT INIT, 1=INITIALIZED
    'O3TMBS' / enum_69,  # 0=NOT INIT, 1=INITIALIZED
    'O3MRS1' / enum_69,  # 0=NOT INIT, 1=INITIALIZED
    'O3ACFG' / enum_70,  # 0=CONFIG 1, 1=CONFIG 2, 2=CONFIG 3, 3=CONFIG IMG
    'O3MSAV' / enum_25,  # 0=NOT AVAILABLE, 1=AVAILABLE
    'O3EMBS' / enum_69,  # 1=INITIALIZED, 0=NOT INIT
    'O4LP1S' / enum_68,  # 0=NOT INIT, 1=NOT FINAL, 3=CRC NOT OK, 2=CRC OK
    'O4LP2S' / enum_68,  # 0=NOT INIT, 1=NOT FINAL, 3=CRC NOT OK, 2=CRC OK
    'O4LP3S' / enum_68,  # 0=NOT INIT, 1=NOT FINAL, 3=CRC NOT OK, 2=CRC OK
    'O4AS1S' / enum_68,  # 0=NOT INIT, 1=NOT FINAL, 3=CRC NOT OK, 2=CRC OK
    'O4AS2S' / enum_68,  # 0=NOT INIT, 1=NOT FINAL, 3=CRC NOT OK, 2=CRC OK
    'O4AS3S' / enum_68,  # 0=NOT INIT, 1=NOT FINAL, 3=CRC NOT OK, 2=CRC OK
    'O4PASS' / enum_68,  # 0=NOT INIT, 1=NOT FINAL, 3=CRC NOT OK, 2=CRC OK
    'O4R01S' / enum_68,  # 0=NOT INIT, 1=NOT FINAL, 3=CRC NOT OK, 2=CRC OK
    'O4R02S' / enum_68,  # 0=NOT INIT, 1=NOT FINAL, 3=CRC NOT OK, 2=CRC OK
    'O4R03S' / enum_68,  # 0=NOT INIT, 1=NOT FINAL, 3=CRC NOT OK, 2=CRC OK
    'O4R04S' / enum_68,  # 0=NOT INIT, 1=NOT FINAL, 3=CRC NOT OK, 2=CRC OK
    'O4R05S' / enum_68,  # 0=NOT INIT, 1=NOT FINAL, 3=CRC NOT OK, 2=CRC OK
    'O4R06S' / enum_68,  # 0=NOT INIT, 1=NOT FINAL, 3=CRC NOT OK, 2=CRC OK
    'O4R07S' / enum_68,  # 0=NOT INIT, 1=NOT FINAL, 3=CRC NOT OK, 2=CRC OK
    'O4R08S' / enum_68,  # 0=NOT INIT, 1=NOT FINAL, 3=CRC NOT OK, 2=CRC OK
    'O4R09S' / enum_68,  # 0=NOT INIT, 1=NOT FINAL, 3=CRC NOT OK, 2=CRC OK
    'O4R10S' / enum_68,  # 0=NOT INIT, 1=NOT FINAL, 3=CRC NOT OK, 2=CRC OK
    'O4R11S' / enum_68,  # 0=NOT INIT, 1=NOT FINAL, 3=CRC NOT OK, 2=CRC OK
    'O4R12S' / enum_68,  # 0=NOT INIT, 1=NOT FINAL, 3=CRC NOT OK, 2=CRC OK
    'O4R13S' / enum_68,  # 0=NOT INIT, 1=NOT FINAL, 3=CRC NOT OK, 2=CRC OK
    'O4R14S' / enum_68,  # 0=NOT INIT, 1=NOT FINAL, 3=CRC NOT OK, 2=CRC OK
    'O4R15S' / enum_68,  # 0=NOT INIT, 1=NOT FINAL, 3=CRC NOT OK, 2=CRC OK
    'O4R16S' / enum_68,  # 0=NOT INIT, 1=NOT FINAL, 3=CRC NOT OK, 2=CRC OK
    'O4CF1S' / enum_68,  # 0=NOT INIT, 1=NOT FINAL, 3=CRC NOT OK, 2=CRC OK
    'O4CF2S' / enum_68,  # 0=NOT INIT, 1=NOT FINAL, 3=CRC NOT OK, 2=CRC OK
    'O4CF3S' / enum_68,  # 0=NOT INIT, 1=NOT FINAL, 3=CRC NOT OK, 2=CRC OK
    'O4PTTS' / enum_69,  # 0=NOT INIT, 1=INITIALIZED
    'O4ATTS' / enum_69,  # 0=NOT INIT, 1=INITIALIZED
    'O4TMBS' / enum_69,  # 0=NOT INIT, 1=INITIALIZED
    'O4MRS1' / enum_69,  # 0=NOT INIT, 1=INITIALIZED
    'O4ACFG' / enum_70,  # 0=CONFIG 1, 1=CONFIG 2, 2=CONFIG 3, 3=CONFIG IMG
    'O4MSAV' / enum_25,  # 0=NOT AVAILABLE, 1=AVAILABLE
    'O4EMBS' / enum_69,  # 1=INITIALIZED, 0=NOT INIT
    'O1STDS' / enum_69,  # 1=INITIALIZED, 0=NOT INIT
    'O1OPES' / enum_69,  # 0=NOT INIT, 1=INITIALIZED
    'O1ADSS' / enum_69,  # 0=NOT INIT, 1=INITIALIZED
    'O1AA1S' / enum_69,  # 0=NOT INIT, 1=INITIALIZED
    'O1AA2S' / enum_69,  # 0=NOT INIT, 1=INITIALIZED
    'O1SS1S' / enum_69,  # 0=NOT INIT, 1=INITIALIZED
    'O1SS2S' / enum_69,  # 0=NOT INIT, 1=INITIALIZED
    'O1THMS' / enum_69,  # 0=NOT INIT, 1=INITIALIZED
    'O1SWIS' / enum_69,  # 0=NOT INIT, 1=INITIALIZED
    'O1PWSS' / enum_69,  # 0=NOT INIT, 1=INITIALIZED
    'O1ADES' / enum_69,  # 0=NOT INIT, 1=INITIALIZED
    'O1PLDS' / enum_69,  # 0=NOT INIT, 1=INITIALIZED
    'O1EXPS' / enum_69,  # 0=NOT INIT, 1=INITIALIZED
    'O1SBDS' / enum_69,  # 0=NOT INIT, 1=INITIALIZED
    'O1MOPS' / enum_69,  # 0=NOT INIT, 1=INITIALIZED
    'O1AISS' / enum_69,  # 0=NOT INIT, 1=INITIALIZED
    'O1A01S' / enum_69,  # 0=NOT INIT, 1=INITIALIZED
    'O1A02S' / enum_69,  # 0=NOT INIT, 1=INITIALIZED
    'O1A03S' / enum_69,  # 0=NOT INIT, 1=INITIALIZED
    'O1A04S' / enum_69,  # 0=NOT INIT, 1=INITIALIZED
    'O1A05S' / enum_69,  # 0=NOT INIT, 1=INITIALIZED
    'O1A06S' / enum_69,  # 0=NOT INIT, 1=INITIALIZED
    'O1A07S' / enum_69,  # 0=NOT INIT, 1=INITIALIZED
    'O1A08S' / enum_69,  # 0=NOT INIT, 1=INITIALIZED
    'O1A09S' / enum_69,  # 0=NOT INIT, 1=INITIALIZED
    'O1A10S' / enum_69,  # 0=NOT INIT, 1=INITIALIZED
    'O1MVSS' / enum_69,  # 0=NOT INIT, 1=INITIALIZED
    'O1THRS' / enum_69,  # 0=NOT INIT, 1=INITIALIZED
    'O1LEOS' / enum_69,  # 0=NOT INIT, 1=INITIALIZED
    'O1OECS' / enum_69,  # 0=NOT INIT, 1=INITIALIZED
    'O1OMSS' / enum_69,  # 0=NOT INIT, 1=INITIALIZED
    'O1OSWS' / enum_69,  # 1=INITIALIZED, 0=NOT INIT
    'O1OSRS' / enum_69,  # 1=INITIALIZED, 0=NOT INIT
    'O1GPSS' / enum_69,  # 1=INITIALIZED, 0=NOT INIT
    'O1RSTS' / enum_69,  # 1=INITIALIZED, 0=NOT INIT
    'O1MVES' / enum_69,  # 1=INITIALIZED, 0=NOT INIT
    'O1RS2S' / enum_69,  # 1=INITIALIZED, 0=NOT INIT
    'O1RS1S' / enum_69,  # 1=INITIALIZED, 0=NOT INIT
    'O2STDS' / enum_69,  # 0=NOT INIT, 1=INITIALIZED
    'O2OPES' / enum_69,  # 0=NOT INIT, 1=INITIALIZED
    'O2ADSS' / enum_69,  # 0=NOT INIT, 1=INITIALIZED
    'O2AA1S' / enum_69,  # 0=NOT INIT, 1=INITIALIZED
    'O2AA2S' / enum_69,  # 0=NOT INIT, 1=INITIALIZED
    'O2SS1S' / enum_69,  # 0=NOT INIT, 1=INITIALIZED
    'O2SS2S' / enum_69,  # 0=NOT INIT, 1=INITIALIZED
    'O2THMS' / enum_69,  # 0=NOT INIT, 1=INITIALIZED
    'O2SWIS' / enum_69,  # 0=NOT INIT, 1=INITIALIZED
    'O2PWSS' / enum_69,  # 0=NOT INIT, 1=INITIALIZED
    'O2ADES' / enum_69,  # 0=NOT INIT, 1=INITIALIZED
    'O2PLDS' / enum_69,  # 0=NOT INIT, 1=INITIALIZED
    'O2EXPS' / enum_69,  # 0=NOT INIT, 1=INITIALIZED
    'O2SBDS' / enum_69,  # 0=NOT INIT, 1=INITIALIZED
    'O2MOPS' / enum_69,  # 0=NOT INIT, 1=INITIALIZED
    'O2AISS' / enum_69,  # 0=NOT INIT, 1=INITIALIZED
    'O2A01S' / enum_69,  # 0=NOT INIT, 1=INITIALIZED
    'O2A02S' / enum_69,  # 0=NOT INIT, 1=INITIALIZED
    'O2A03S' / enum_69,  # 0=NOT INIT, 1=INITIALIZED
    'O2A04S' / enum_69,  # 0=NOT INIT, 1=INITIALIZED
    'O2A05S' / enum_69,  # 0=NOT INIT, 1=INITIALIZED
    'O2A06S' / enum_69,  # 0=NOT INIT, 1=INITIALIZED
    'O2A07S' / enum_69,  # 0=NOT INIT, 1=INITIALIZED
    'O2A08S' / enum_69,  # 0=NOT INIT, 1=INITIALIZED
    'O2A09S' / enum_69,  # 0=NOT INIT, 1=INITIALIZED
    'O2A10S' / enum_69,  # 0=NOT INIT, 1=INITIALIZED
    'O2MVSS' / enum_69,  # 0=NOT INIT, 1=INITIALIZED
    'O2THRS' / enum_69,  # 0=NOT INIT, 1=INITIALIZED
    'O2LEOS' / enum_69,  # 0=NOT INIT, 1=INITIALIZED
    'O2OECS' / enum_69,  # 0=NOT INIT, 1=INITIALIZED
    'O2OMSS' / enum_69,  # 0=NOT INIT, 1=INITIALIZED
    'O2OSWS' / enum_69,  # 1=INITIALIZED, 0=NOT INIT
    'O2OSRS' / enum_69,  # 1=INITIALIZED, 0=NOT INIT
    'O2GPSS' / enum_69,  # 1=INITIALIZED, 0=NOT INIT
    'O2RSTS' / enum_69,  # 1=INITIALIZED, 0=NOT INIT
    'O2MVES' / enum_69,  # 1=INITIALIZED, 0=NOT INIT
    'O2RS2S' / enum_69,  # 1=INITIALIZED, 0=NOT INIT
    'O2RS1S' / enum_69,  # 1=INITIALIZED, 0=NOT INIT
    'O3STDS' / enum_69,  # 0=NOT INIT, 1=INITIALIZED
    'O3OPES' / enum_69,  # 0=NOT INIT, 1=INITIALIZED
    'O3ADSS' / enum_69,  # 0=NOT INIT, 1=INITIALIZED
    'O3AA1S' / enum_69,  # 0=NOT INIT, 1=INITIALIZED
    'O3AA2S' / enum_69,  # 0=NOT INIT, 1=INITIALIZED
    'O3SS1S' / enum_69,  # 0=NOT INIT, 1=INITIALIZED
    'O3SS2S' / enum_69,  # 0=NOT INIT, 1=INITIALIZED
    'O3THMS' / enum_69,  # 0=NOT INIT, 1=INITIALIZED
    'O3SWIS' / enum_69,  # 0=NOT INIT, 1=INITIALIZED
    'O3PWSS' / enum_69,  # 0=NOT INIT, 1=INITIALIZED
    'O3ADES' / enum_69,  # 0=NOT INIT, 1=INITIALIZED
    'O3PLDS' / enum_69,  # 0=NOT INIT, 1=INITIALIZED
    'O3EXPS' / enum_69,  # 0=NOT INIT, 1=INITIALIZED
    'O3SBDS' / enum_69,  # 0=NOT INIT, 1=INITIALIZED
    'O3MOPS' / enum_69,  # 0=NOT INIT, 1=INITIALIZED
    'O3AISS' / enum_69,  # 0=NOT INIT, 1=INITIALIZED
    'O3A01S' / enum_69,  # 0=NOT INIT, 1=INITIALIZED
    'O3A02S' / enum_69,  # 0=NOT INIT, 1=INITIALIZED
    'O3A03S' / enum_69,  # 0=NOT INIT, 1=INITIALIZED
    'O3A04S' / enum_69,  # 0=NOT INIT, 1=INITIALIZED
    'O3A05S' / enum_69,  # 0=NOT INIT, 1=INITIALIZED
    'O3A06S' / enum_69,  # 0=NOT INIT, 1=INITIALIZED
    'O3A07S' / enum_69,  # 0=NOT INIT, 1=INITIALIZED
    'O3A08S' / enum_69,  # 0=NOT INIT, 1=INITIALIZED
    'O3A09S' / enum_69,  # 0=NOT INIT, 1=INITIALIZED
    'O3A10S' / enum_69,  # 0=NOT INIT, 1=INITIALIZED
    'O3MVSS' / enum_69,  # 0=NOT INIT, 1=INITIALIZED
    'O3THRS' / enum_69,  # 0=NOT INIT, 1=INITIALIZED
    'O3LEOS' / enum_69,  # 0=NOT INIT, 1=INITIALIZED
    'O3OECS' / enum_69,  # 0=NOT INIT, 1=INITIALIZED
    'O3OMSS' / enum_69,  # 0=NOT INIT, 1=INITIALIZED
    'O3OSWS' / enum_69,  # 1=INITIALIZED, 0=NOT INIT
    'O3OSRS' / enum_69,  # 1=INITIALIZED, 0=NOT INIT
    'O3GPSS' / enum_69,  # 1=INITIALIZED, 0=NOT INIT
    'O3RSTS' / enum_69,  # 1=INITIALIZED, 0=NOT INIT
    'O3MVES' / enum_69,  # 1=INITIALIZED, 0=NOT INIT
    'O3RS2S' / enum_69,  # 1=INITIALIZED, 0=NOT INIT
    'O3RS1S' / enum_69,  # 1=INITIALIZED, 0=NOT INIT
    'O4STDS' / enum_69,  # 0=NOT INIT, 1=INITIALIZED
    'O4OPES' / enum_69,  # 0=NOT INIT, 1=INITIALIZED
    'O4ADSS' / enum_69,  # 0=NOT INIT, 1=INITIALIZED
    'O4AA1S' / enum_69,  # 0=NOT INIT, 1=INITIALIZED
    'O4AA2S' / enum_69,  # 0=NOT INIT, 1=INITIALIZED
    'O4SS1S' / enum_69,  # 0=NOT INIT, 1=INITIALIZED
    'O4SS2S' / enum_69,  # 0=NOT INIT, 1=INITIALIZED
    'O4THMS' / enum_69,  # 0=NOT INIT, 1=INITIALIZED
    'O4SWIS' / enum_69,  # 0=NOT INIT, 1=INITIALIZED
    'O4PWSS' / enum_69,  # 0=NOT INIT, 1=INITIALIZED
    'O4ADES' / enum_69,  # 0=NOT INIT, 1=INITIALIZED
    'O4PLDS' / enum_69,  # 0=NOT INIT, 1=INITIALIZED
    'O4EXPS' / enum_69,  # 0=NOT INIT, 1=INITIALIZED
    'O4SBDS' / enum_69,  # 0=NOT INIT, 1=INITIALIZED
    'O4MOPS' / enum_69,  # 0=NOT INIT, 1=INITIALIZED
    'O4AISS' / enum_69,  # 0=NOT INIT, 1=INITIALIZED
    'O4A01S' / enum_69,  # 0=NOT INIT, 1=INITIALIZED
    'O4A02S' / enum_69,  # 0=NOT INIT, 1=INITIALIZED
    'O4A03S' / enum_69,  # 0=NOT INIT, 1=INITIALIZED
    'O4A04S' / enum_69,  # 0=NOT INIT, 1=INITIALIZED
    'O4A05S' / enum_69,  # 0=NOT INIT, 1=INITIALIZED
    'O4A06S' / enum_69,  # 0=NOT INIT, 1=INITIALIZED
    'O4A07S' / enum_69,  # 0=NOT INIT, 1=INITIALIZED
    'O4A08S' / enum_69,  # 0=NOT INIT, 1=INITIALIZED
    'O4A09S' / enum_69,  # 0=NOT INIT, 1=INITIALIZED
    'O4A10S' / enum_69,  # 0=NOT INIT, 1=INITIALIZED
    'O4MVSS' / enum_69,  # 0=NOT INIT, 1=INITIALIZED
    'O4THRS' / enum_69,  # 0=NOT INIT, 1=INITIALIZED
    'O4LEOS' / enum_69,  # 0=NOT INIT, 1=INITIALIZED
    'O4OECS' / enum_69,  # 0=NOT INIT, 1=INITIALIZED
    'O4OMSS' / enum_69,  # 0=NOT INIT, 1=INITIALIZED
    'O4OSWS' / enum_69,  # 1=INITIALIZED, 0=NOT INIT
    'O4OSRS' / enum_69,  # 1=INITIALIZED, 0=NOT INIT
    'O4GPSS' / enum_69,  # 1=INITIALIZED, 0=NOT INIT
    'O4RSTS' / enum_69,  # 1=INITIALIZED, 0=NOT INIT
    'O4MVES' / enum_69,  # 1=INITIALIZED, 0=NOT INIT
    'O4RS2S' / enum_69,  # 1=INITIALIZED, 0=NOT INIT
    'O4RS1S' / enum_69,  # 1=INITIALIZED, 0=NOT INIT
)

obdh_ext_periph_sts = construct.BitStruct(
    '_name' / construct.Computed('obdh_ext_periph_sts'),
    'name' / construct.Computed('OBDH EXT PERIPH STS'),
    'O1CN1S' / enum_46,  # 1=ENABLED, 0=DISABLED
    'O1CN2S' / enum_46,  # 1=ENABLED, 0=DISABLED
    'O1SY1S' / enum_46,  # 1=ENABLED, 0=DISABLED
    'O1SY2S' / enum_46,  # 1=ENABLED, 0=DISABLED
    'O1SY3S' / enum_46,  # 1=ENABLED, 0=DISABLED
    'O1SY4S' / enum_46,  # 1=ENABLED, 0=DISABLED
    'O1LC1S' / enum_46,  # 1=ENABLED, 0=DISABLED
    'O1LC2S' / enum_46,  # 1=ENABLED, 0=DISABLED
    'O1RA1S' / enum_46,  # 1=ENABLED, 0=DISABLED
    'O1RA2S' / enum_46,  # 1=ENABLED, 0=DISABLED
    'O1PN1S' / enum_46,  # 1=ENABLED, 0=DISABLED
    'O1PN2S' / enum_46,  # 1=ENABLED, 0=DISABLED
    'O1SNFS' / enum_46,  # 1=ENABLED, 0=DISABLED
    'O1PSAV' / enum_25,  # 0=NOT AVAILABLE, 1=AVAILABLE
    'O1CN1R' / construct.BitsInteger(8),
    'O1CN1T' / construct.BitsInteger(8),
    'O1CN2R' / construct.BitsInteger(8),
    'O1C2TE' / construct.BitsInteger(8),
    'O1LC1B' / construct.BitsInteger(8),
    'O1LC2B' / construct.BitsInteger(8),
    'O2CN1S' / enum_46,  # 1=ENABLED, 0=DISABLED
    'O2CN2S' / enum_46,  # 1=ENABLED, 0=DISABLED
    'O2SY1S' / enum_46,  # 1=ENABLED, 0=DISABLED
    'O2SY2S' / enum_46,  # 1=ENABLED, 0=DISABLED
    'O2SY3S' / enum_46,  # 1=ENABLED, 0=DISABLED
    'O2SY4S' / enum_46,  # 1=ENABLED, 0=DISABLED
    'O2LC1S' / enum_46,  # 1=ENABLED, 0=DISABLED
    'O2LC2S' / enum_46,  # 1=ENABLED, 0=DISABLED
    'O2RA1S' / enum_46,  # 1=ENABLED, 0=DISABLED
    'O2RA2S' / enum_46,  # 1=ENABLED, 0=DISABLED
    'O2PN1S' / enum_46,  # 1=ENABLED, 0=DISABLED
    'O2PN2S' / enum_46,  # 1=ENABLED, 0=DISABLED
    'O2SNFS' / enum_46,  # 1=ENABLED, 0=DISABLED
    'O2PSAV' / enum_25,  # 0=NOT AVAILABLE, 1=AVAILABLE
    'O2CN1R' / construct.BitsInteger(8),
    'O2CN1T' / construct.BitsInteger(8),
    'O2CN2R' / construct.BitsInteger(8),
    'O2C2TE' / construct.BitsInteger(8),
    'O2LC1B' / construct.BitsInteger(8),
    'O2LC2B' / construct.BitsInteger(8),
    'O3CN1S' / enum_46,  # 1=ENABLED, 0=DISABLED
    'O3CN2S' / enum_46,  # 1=ENABLED, 0=DISABLED
    'O3SY1S' / enum_46,  # 1=ENABLED, 0=DISABLED
    'O3SY2S' / enum_46,  # 1=ENABLED, 0=DISABLED
    'O3SY3S' / enum_46,  # 1=ENABLED, 0=DISABLED
    'O3SY4S' / enum_46,  # 1=ENABLED, 0=DISABLED
    'O3LC1S' / enum_46,  # 1=ENABLED, 0=DISABLED
    'O3LC2S' / enum_46,  # 1=ENABLED, 0=DISABLED
    'O3RA1S' / enum_46,  # 1=ENABLED, 0=DISABLED
    'O3RA2S' / enum_46,  # 1=ENABLED, 0=DISABLED
    'O3PN1S' / enum_46,  # 1=ENABLED, 0=DISABLED
    'O3PN2S' / enum_46,  # 1=ENABLED, 0=DISABLED
    'O3SNFS' / enum_46,  # 1=ENABLED, 0=DISABLED
    'O3PSAV' / enum_25,  # 0=NOT AVAILABLE, 1=AVAILABLE
    'O3CN1R' / construct.BitsInteger(8),
    'O3CN1T' / construct.BitsInteger(8),
    'O3CN2R' / construct.BitsInteger(8),
    'O3C2TE' / construct.BitsInteger(8),
    'O3LC1B' / construct.BitsInteger(8),
    'O3LC2B' / construct.BitsInteger(8),
    'O4CN1S' / enum_46,  # 1=ENABLED, 0=DISABLED
    'O4CN2S' / enum_46,  # 1=ENABLED, 0=DISABLED
    'O4SY1S' / enum_46,  # 1=ENABLED, 0=DISABLED
    'O4SY2S' / enum_46,  # 1=ENABLED, 0=DISABLED
    'O4SY3S' / enum_46,  # 1=ENABLED, 0=DISABLED
    'O4SY4S' / enum_46,  # 1=ENABLED, 0=DISABLED
    'O4LC1S' / enum_46,  # 1=ENABLED, 0=DISABLED
    'O4LC2S' / enum_46,  # 1=ENABLED, 0=DISABLED
    'O4RA1S' / enum_46,  # 1=ENABLED, 0=DISABLED
    'O4RA2S' / enum_46,  # 1=ENABLED, 0=DISABLED
    'O4PN1S' / enum_46,  # 1=ENABLED, 0=DISABLED
    'O4PN2S' / enum_46,  # 1=ENABLED, 0=DISABLED
    'O4SNFS' / enum_46,  # 1=ENABLED, 0=DISABLED
    'O4PSAV' / enum_25,  # 0=NOT AVAILABLE, 1=AVAILABLE
    'O4CN1R' / construct.BitsInteger(8),
    'O4CN1T' / construct.BitsInteger(8),
    'O4CN2R' / construct.BitsInteger(8),
    'O4C2TE' / construct.BitsInteger(8),
    'O4LC1B' / construct.BitsInteger(8),
    'O4LC2B' / construct.BitsInteger(8),
    'O1CN1O' / enum_71,  # 0=NO ERROR, 1=RX HW FIFO0 OVRN, 2=RX HW FIFO1 OVRN, 3=RX SW FIFO0 OVRN, 4=RX SW FIFO1 OVRN, 5=TX SW FIFO OVRN, 6=ERROR WARN, 7=ERROR PASSIVE, 8=BUS OFF, 9=STUFF ERR, 10=FORM ERR, 11=ACK ERR, 12=BIT RECESSIVE ERR, 13=BIT DOMINANT ERR, 14=CRC ERR
    'O1CN1C' / construct.BitsInteger(4),
    'O1CN2O' / enum_71,  # 0=NO ERROR, 1=RX HW FIFO0 OVRN, 2=RX HW FIFO1 OVRN, 3=RX SW FIFO0 OVRN, 4=RX SW FIFO1 OVRN, 5=TX SW FIFO OVRN, 6=ERROR WARN, 7=ERROR PASSIVE, 8=BUS OFF, 9=STUFF ERR, 10=FORM ERR, 11=ACK ERR, 12=BIT RECESSIVE ERR, 13=BIT DOMINANT ERR, 14=CRC ERR
    'O1CN2C' / construct.BitsInteger(4),
    'O1SY1O' / enum_72,  # 0=NO ERROR, 1=OVERUN ERR, 2=PARITY ERR, 3=FRAMING ERR, 4=NOISE ERR, 5=RX BUF OVFLW
    'O1SY1C' / construct.BitsInteger(5),
    'O1SY2O' / enum_72,  # 0=NO ERROR, 1=OVERUN ERR, 2=PARITY ERR, 3=FRAMING ERR, 4=NOISE ERR, 5=RX BUF OVFLW
    'O1SY2C' / construct.BitsInteger(5),
    'O1SY3O' / enum_72,  # 0=NO ERROR, 1=OVERUN ERR, 2=PARITY ERR, 3=FRAMING ERR, 4=NOISE ERR, 5=RX BUF OVFLW
    'O1SY3C' / construct.BitsInteger(5),
    'O1SY4O' / enum_72,  # 0=NO ERROR, 1=OVERUN ERR, 2=PARITY ERR, 3=FRAMING ERR, 4=NOISE ERR, 5=RX BUF OVFLW
    'O1SY4C' / construct.BitsInteger(5),
    'O1LC1O' / enum_73,  # 0=NO ERROR, 1=BUFFER FULL, 2=RX TIMEOUT, 3=TX TIMEOUT
    'O1LC1C' / construct.BitsInteger(6),
    'O1LC2O' / enum_73,  # 0=NO ERROR, 1=BUFFER FULL, 2=RX TIMEOUT, 3=TX TIMEOUT
    'O1LC2C' / construct.BitsInteger(6),
    'O2CN1O' / enum_71,  # 0=NO ERROR, 1=RX HW FIFO0 OVRN, 2=RX HW FIFO1 OVRN, 3=RX SW FIFO0 OVRN, 4=RX SW FIFO1 OVRN, 5=TX SW FIFO OVRN, 6=ERROR WARN, 7=ERROR PASSIVE, 8=BUS OFF, 9=STUFF ERR, 10=FORM ERR, 11=ACK ERR, 12=BIT RECESSIVE ERR, 13=BIT DOMINANT ERR, 14=CRC ERR
    'O2CN1C' / construct.BitsInteger(4),
    'O2CN2O' / enum_71,  # 0=NO ERROR, 1=RX HW FIFO0 OVRN, 2=RX HW FIFO1 OVRN, 3=RX SW FIFO0 OVRN, 4=RX SW FIFO1 OVRN, 5=TX SW FIFO OVRN, 6=ERROR WARN, 7=ERROR PASSIVE, 8=BUS OFF, 9=STUFF ERR, 10=FORM ERR, 11=ACK ERR, 12=BIT RECESSIVE ERR, 13=BIT DOMINANT ERR, 14=CRC ERR
    'O2CN2C' / construct.BitsInteger(4),
    'O2SY1O' / enum_72,  # 0=NO ERROR, 1=OVERUN ERR, 2=PARITY ERR, 3=FRAMING ERR, 4=NOISE ERR, 5=RX BUF OVFLW
    'O2SY1C' / construct.BitsInteger(5),
    'O2SY2O' / enum_72,  # 0=NO ERROR, 1=OVERUN ERR, 2=PARITY ERR, 3=FRAMING ERR, 4=NOISE ERR, 5=RX BUF OVFLW
    'O2SY2C' / construct.BitsInteger(5),
    'O2SY3O' / enum_72,  # 0=NO ERROR, 1=OVERUN ERR, 2=PARITY ERR, 3=FRAMING ERR, 4=NOISE ERR, 5=RX BUF OVFLW
    'O2SY3C' / construct.BitsInteger(5),
    'O2SY4O' / enum_72,  # 0=NO ERROR, 1=OVERUN ERR, 2=PARITY ERR, 3=FRAMING ERR, 4=NOISE ERR, 5=RX BUF OVFLW
    'O2SY4C' / construct.BitsInteger(5),
    'O2LC1O' / enum_73,  # 0=NO ERROR, 1=BUFFER FULL, 2=RX TIMEOUT, 3=TX TIMEOUT
    'O2LC1C' / construct.BitsInteger(6),
    'O2LC2O' / enum_73,  # 0=NO ERROR, 1=BUFFER FULL, 2=RX TIMEOUT, 3=TX TIMEOUT
    'O2LC2C' / construct.BitsInteger(6),
    'O3CN1O' / enum_71,  # 0=NO ERROR, 1=RX HW FIFO0 OVRN, 2=RX HW FIFO1 OVRN, 3=RX SW FIFO0 OVRN, 4=RX SW FIFO1 OVRN, 5=TX SW FIFO OVRN, 6=ERROR WARN, 7=ERROR PASSIVE, 8=BUS OFF, 9=STUFF ERR, 10=FORM ERR, 11=ACK ERR, 12=BIT RECESSIVE ERR, 13=BIT DOMINANT ERR, 14=CRC ERR
    'O3CN1C' / construct.BitsInteger(4),
    'O3CN2O' / enum_71,  # 0=NO ERROR, 1=RX HW FIFO0 OVRN, 2=RX HW FIFO1 OVRN, 3=RX SW FIFO0 OVRN, 4=RX SW FIFO1 OVRN, 5=TX SW FIFO OVRN, 6=ERROR WARN, 7=ERROR PASSIVE, 8=BUS OFF, 9=STUFF ERR, 10=FORM ERR, 11=ACK ERR, 12=BIT RECESSIVE ERR, 13=BIT DOMINANT ERR, 14=CRC ERR
    'O3CN2C' / construct.BitsInteger(4),
    'O3SY1O' / enum_72,  # 0=NO ERROR, 1=OVERUN ERR, 2=PARITY ERR, 3=FRAMING ERR, 4=NOISE ERR, 5=RX BUF OVFLW
    'O3SY1C' / construct.BitsInteger(5),
    'O3SY2O' / enum_72,  # 0=NO ERROR, 1=OVERUN ERR, 2=PARITY ERR, 3=FRAMING ERR, 4=NOISE ERR, 5=RX BUF OVFLW
    'O3SY2C' / construct.BitsInteger(5),
    'O3SY3O' / enum_72,  # 0=NO ERROR, 1=OVERUN ERR, 2=PARITY ERR, 3=FRAMING ERR, 4=NOISE ERR, 5=RX BUF OVFLW
    'O3SY3C' / construct.BitsInteger(5),
    'O3SY4O' / enum_72,  # 0=NO ERROR, 1=OVERUN ERR, 2=PARITY ERR, 3=FRAMING ERR, 4=NOISE ERR, 5=RX BUF OVFLW
    'O3SY4C' / construct.BitsInteger(5),
    'O3LC1O' / enum_73,  # 0=NO ERROR, 1=BUFFER FULL, 2=RX TIMEOUT, 3=TX TIMEOUT
    'O3LC1C' / construct.BitsInteger(6),
    'O3LC2O' / enum_73,  # 0=NO ERROR, 1=BUFFER FULL, 2=RX TIMEOUT, 3=TX TIMEOUT
    'O3LC2C' / construct.BitsInteger(6),
    'O4CN1O' / enum_71,  # 0=NO ERROR, 1=RX HW FIFO0 OVRN, 2=RX HW FIFO1 OVRN, 3=RX SW FIFO0 OVRN, 4=RX SW FIFO1 OVRN, 5=TX SW FIFO OVRN, 6=ERROR WARN, 7=ERROR PASSIVE, 8=BUS OFF, 9=STUFF ERR, 10=FORM ERR, 11=ACK ERR, 12=BIT RECESSIVE ERR, 13=BIT DOMINANT ERR, 14=CRC ERR
    'O4CN1C' / construct.BitsInteger(4),
    'O4CN2O' / enum_71,  # 0=NO ERROR, 1=RX HW FIFO0 OVRN, 2=RX HW FIFO1 OVRN, 3=RX SW FIFO0 OVRN, 4=RX SW FIFO1 OVRN, 5=TX SW FIFO OVRN, 6=ERROR WARN, 7=ERROR PASSIVE, 8=BUS OFF, 9=STUFF ERR, 10=FORM ERR, 11=ACK ERR, 12=BIT RECESSIVE ERR, 13=BIT DOMINANT ERR, 14=CRC ERR
    'O4CN2C' / construct.BitsInteger(4),
    'O4SY1O' / enum_72,  # 0=NO ERROR, 1=OVERUN ERR, 2=PARITY ERR, 3=FRAMING ERR, 4=NOISE ERR, 5=RX BUF OVFLW
    'O4SY1C' / construct.BitsInteger(5),
    'O4SY2O' / enum_72,  # 0=NO ERROR, 1=OVERUN ERR, 2=PARITY ERR, 3=FRAMING ERR, 4=NOISE ERR, 5=RX BUF OVFLW
    'O4SY2C' / construct.BitsInteger(5),
    'O4SY3O' / enum_72,  # 0=NO ERROR, 1=OVERUN ERR, 2=PARITY ERR, 3=FRAMING ERR, 4=NOISE ERR, 5=RX BUF OVFLW
    'O4SY3C' / construct.BitsInteger(5),
    'O4SY4O' / enum_72,  # 0=NO ERROR, 1=OVERUN ERR, 2=PARITY ERR, 3=FRAMING ERR, 4=NOISE ERR, 5=RX BUF OVFLW
    'O4SY4C' / construct.BitsInteger(5),
    'O4LC1O' / enum_73,  # 0=NO ERROR, 1=BUFFER FULL, 2=RX TIMEOUT, 3=TX TIMEOUT
    'O4LC1C' / construct.BitsInteger(6),
    'O4LC2O' / enum_73,  # 0=NO ERROR, 1=BUFFER FULL, 2=RX TIMEOUT, 3=TX TIMEOUT
    'O4LC2C' / construct.BitsInteger(6),
    'O1RSTP' / enum_0,  # 0=OFF, 1=ON
    'O1B1RS' / enum_74,  # 0=NO RESET, 1=RESET
    'O1B2RS' / enum_74,  # 0=NO RESET, 1=RESET
    'O1ONFP' / enum_42,  # 0=DEACTIVATED, 1=ACTIVATED
    'O1ONFS' / enum_42,  # 0=DEACTIVATED, 1=ACTIVATED
    'O1RTCI' / enum_75,  # 1=INITIALIZED, 0=NOT INITIALIZED
    'O1RTCS' / enum_76,  # 0=LSE, 1=LSI, 2=HSE, 3=INVALID
    'O1SCLS' / enum_77,  # 0=HSI, 1=HSE, 2=PLL HSI, 3=PLL HSE
    'O1FTEX' / enum_0,  # 0=OFF, 1=ON
    'O2RSTP' / enum_0,  # 0=OFF, 1=ON
    'O2B1RS' / enum_74,  # 0=NO RESET, 1=RESET
    'O2B2RS' / enum_74,  # 0=NO RESET, 1=RESET
    'O2ONFP' / enum_42,  # 0=DEACTIVATED, 1=ACTIVATED
    'O2ONFS' / enum_42,  # 0=DEACTIVATED, 1=ACTIVATED
    'O2RTCI' / enum_75,  # 1=INITIALIZED, 0=NOT INITIALIZED
    'O2RTCS' / enum_76,  # 0=LSE, 1=LSI, 2=HSE, 3=INVALID
    'O2SCLS' / enum_77,  # 0=HSI, 1=HSE, 2=PLL HSI, 3=PLL HSE
    'O2FTEX' / enum_0,  # 0=OFF, 1=ON
    'O3RSTP' / enum_0,  # 0=OFF, 1=ON
    'O3B1RS' / enum_74,  # 0=NO RESET, 1=RESET
    'O3B2RS' / enum_74,  # 0=NO RESET, 1=RESET
    'O3ONFP' / enum_42,  # 0=DEACTIVATED, 1=ACTIVATED
    'O3ONFS' / enum_42,  # 0=DEACTIVATED, 1=ACTIVATED
    'O3RTCI' / enum_75,  # 1=INITIALIZED, 0=NOT INITIALIZED
    'O3RTCS' / enum_76,  # 0=LSE, 1=LSI, 2=HSE, 3=INVALID
    'O3SCLS' / enum_77,  # 0=HSI, 1=HSE, 2=PLL HSI, 3=PLL HSE
    'O3FTEX' / enum_0,  # 0=OFF, 1=ON
    'O4RSTP' / enum_0,  # 0=OFF, 1=ON
    'O4B1RS' / enum_74,  # 0=NO RESET, 1=RESET
    'O4B2RS' / enum_74,  # 0=NO RESET, 1=RESET
    'O4ONFP' / enum_42,  # 0=DEACTIVATED, 1=ACTIVATED
    'O4ONFS' / enum_42,  # 0=DEACTIVATED, 1=ACTIVATED
    'O4RTCI' / enum_75,  # 1=INITIALIZED, 0=NOT INITIALIZED
    'O4RTCS' / enum_76,  # 0=LSE, 1=LSI, 2=HSE, 3=INVALID
    'O4SCLS' / enum_77,  # 0=HSI, 1=HSE, 2=PLL HSI, 3=PLL HSE
    'O4FTEX' / enum_0,  # 0=OFF, 1=ON
    'O1RMC2' / enum_78,  # 0=UART, 1=CAN_1, 2=CAN_2, 3=NONE
    'O1RMC3' / enum_78,  # 0=UART, 1=CAN_1, 2=CAN_2, 3=NONE
    'O1RMC4' / enum_78,  # 0=UART, 1=CAN_1, 2=CAN_2, 3=NONE
    'O1RMHW' / enum_79,  # 0=OBDH 1, 1=OBDH 2, 2=OBDH 3, 3=OBDH 4, 7=INVALID
    'O1RPDS' / enum_42,  # 1=ACTIVATED, 0=DEACTIVATED
    'O1RSIS' / enum_42,  # 1=ACTIVATED, 0=DEACTIVATED
    'O1RSCS' / enum_42,  # 1=ACTIVATED, 0=DEACTIVATED
    'O1RSUS' / enum_42,  # 1=ACTIVATED, 0=DEACTIVATED
    'O2RMC1' / enum_78,  # 0=UART, 1=CAN_1, 2=CAN_2, 3=NONE
    'O2RMC3' / enum_78,  # 0=UART, 1=CAN_1, 2=CAN_2, 3=NONE
    'O2RMC4' / enum_78,  # 0=UART, 1=CAN_1, 2=CAN_2, 3=NONE
    'O2RMHW' / enum_79,  # 0=OBDH 1, 1=OBDH 2, 2=OBDH 3, 3=OBDH 4, 7=INVALID
    'O2RPDS' / enum_42,  # 1=ACTIVATED, 0=DEACTIVATED
    'O2RSIS' / enum_42,  # 1=ACTIVATED, 0=DEACTIVATED
    'O2RSCS' / enum_42,  # 1=ACTIVATED, 0=DEACTIVATED
    'O2RSUS' / enum_42,  # 1=ACTIVATED, 0=DEACTIVATED
    'O3RMC1' / enum_78,  # 0=UART, 1=CAN_1, 2=CAN_2, 3=NONE
    'O3RMC2' / enum_78,  # 0=UART, 1=CAN_1, 2=CAN_2, 3=NONE
    'O3RMC4' / enum_78,  # 0=UART, 1=CAN_1, 2=CAN_2, 3=NONE
    'O3RMHW' / enum_79,  # 0=OBDH 1, 1=OBDH 2, 2=OBDH 3, 3=OBDH 4, 7=INVALID
    'O3RPDS' / enum_42,  # 1=ACTIVATED, 0=DEACTIVATED
    'O3RSIS' / enum_42,  # 1=ACTIVATED, 0=DEACTIVATED
    'O3RSCS' / enum_42,  # 1=ACTIVATED, 0=DEACTIVATED
    'O3RSUS' / enum_42,  # 1=ACTIVATED, 0=DEACTIVATED
    'O4RMC1' / enum_78,  # 0=UART, 1=CAN_1, 2=CAN_2, 3=NONE
    'O4RMC2' / enum_78,  # 0=UART, 1=CAN_1, 2=CAN_2, 3=NONE
    'O4RMC3' / enum_78,  # 0=UART, 1=CAN_1, 2=CAN_2, 3=NONE
    'O4RMHW' / enum_79,  # 0=OBDH 1, 1=OBDH 2, 2=OBDH 3, 3=OBDH 4, 7=INVALID
    'O4RPDS' / enum_42,  # 1=ACTIVATED, 0=DEACTIVATED
    'O4RSIS' / enum_42,  # 1=ACTIVATED, 0=DEACTIVATED
    'O4RSCS' / enum_42,  # 1=ACTIVATED, 0=DEACTIVATED
    'O4RSUS' / enum_42,  # 1=ACTIVATED, 0=DEACTIVATED
    'O1PN1O' / enum_80,  # 0=NO ERROR, 1=NOT INIT, 2=ALREADY INIT, 3=LL DRIVER NOT EXIST, 4=NOT IMPLEMENTED, 5=INVALID ADDR, 6=DEVICE BUSY, 7=WRITE ERR, 8=INTERFACE BUSY, 9=TIMEOUT, 10=INVALID LEN, 11=ERASE ERR
    'O1PN1C' / construct.BitsInteger(4),
    'O1PN2O' / enum_80,  # 0=NO ERROR, 1=NOT INIT, 2=ALREADY INIT, 3=LL DRIVER NOT EXIST, 4=NOT IMPLEMENTED, 5=INVALID ADDR, 6=DEVICE BUSY, 7=WRITE ERR, 8=INTERFACE BUSY, 9=TIMEOUT, 10=INVALID LEN, 11=ERASE ERR
    'O1PN2C' / construct.BitsInteger(4),
    'O1SNFO' / enum_80,  # 0=NO ERROR, 1=NOT INIT, 2=ALREADY INIT, 3=LL DRIVER NOT EXIST, 4=NOT IMPLEMENTED, 5=INVALID ADDR, 6=DEVICE BUSY, 7=WRITE ERR, 8=INTERFACE BUSY, 9=TIMEOUT, 10=INVALID LEN, 11=ERASE ERR
    'O1SNFC' / construct.BitsInteger(4),
    'O1RA1O' / enum_81,  # 0=NO ERROR, 1=NOT INIT, 2=ALREADY INIT, 3=LL DRIVER NOT EXIST, 4=INVLD ADDR
    'O1RA1C' / construct.BitsInteger(4),
    'O1RA2O' / enum_81,  # 0=NO ERROR, 1=NOT INIT, 2=ALREADY INIT, 3=LL DRIVER NOT EXIST, 4=INVLD ADDR
    'O1RA2C' / construct.BitsInteger(4),
    'O2PN1O' / enum_80,  # 0=NO ERROR, 1=NOT INIT, 2=ALREADY INIT, 3=LL DRIVER NOT EXIST, 4=NOT IMPLEMENTED, 5=INVALID ADDR, 6=DEVICE BUSY, 7=WRITE ERR, 8=INTERFACE BUSY, 9=TIMEOUT, 10=INVALID LEN, 11=ERASE ERR
    'O2PN1C' / construct.BitsInteger(4),
    'O2PN2O' / enum_80,  # 0=NO ERROR, 1=NOT INIT, 2=ALREADY INIT, 3=LL DRIVER NOT EXIST, 4=NOT IMPLEMENTED, 5=INVALID ADDR, 6=DEVICE BUSY, 7=WRITE ERR, 8=INTERFACE BUSY, 9=TIMEOUT, 10=INVALID LEN, 11=ERASE ERR
    'O2PN2C' / construct.BitsInteger(4),
    'O2SNFO' / enum_80,  # 0=NO ERROR, 1=NOT INIT, 2=ALREADY INIT, 3=LL DRIVER NOT EXIST, 4=NOT IMPLEMENTED, 5=INVALID ADDR, 6=DEVICE BUSY, 7=WRITE ERR, 8=INTERFACE BUSY, 9=TIMEOUT, 10=INVALID LEN, 11=ERASE ERR
    'O2SNFC' / construct.BitsInteger(4),
    'O2RA1O' / enum_81,  # 0=NO ERROR, 1=NOT INIT, 2=ALREADY INIT, 3=LL DRIVER NOT EXIST, 4=INVLD ADDR
    'O2RA1C' / construct.BitsInteger(4),
    'O2RA2O' / enum_81,  # 0=NO ERROR, 1=NOT INIT, 2=ALREADY INIT, 3=LL DRIVER NOT EXIST, 4=INVLD ADDR
    'O2RA2C' / construct.BitsInteger(4),
    'O3PN1O' / enum_80,  # 0=NO ERROR, 1=NOT INIT, 2=ALREADY INIT, 3=LL DRIVER NOT EXIST, 4=NOT IMPLEMENTED, 5=INVALID ADDR, 6=DEVICE BUSY, 7=WRITE ERR, 8=INTERFACE BUSY, 9=TIMEOUT, 10=INVALID LEN, 11=ERASE ERR
    'O3PN1C' / construct.BitsInteger(4),
    'O3PN2O' / enum_80,  # 0=NO ERROR, 1=NOT INIT, 2=ALREADY INIT, 3=LL DRIVER NOT EXIST, 4=NOT IMPLEMENTED, 5=INVALID ADDR, 6=DEVICE BUSY, 7=WRITE ERR, 8=INTERFACE BUSY, 9=TIMEOUT, 10=INVALID LEN, 11=ERASE ERR
    'O3PN2C' / construct.BitsInteger(4),
    'O3SNFO' / enum_80,  # 0=NO ERROR, 1=NOT INIT, 2=ALREADY INIT, 3=LL DRIVER NOT EXIST, 4=NOT IMPLEMENTED, 5=INVALID ADDR, 6=DEVICE BUSY, 7=WRITE ERR, 8=INTERFACE BUSY, 9=TIMEOUT, 10=INVALID LEN, 11=ERASE ERR
    'O3SNFC' / construct.BitsInteger(4),
    'O3RA1O' / enum_81,  # 0=NO ERROR, 1=NOT INIT, 2=ALREADY INIT, 3=LL DRIVER NOT EXIST, 4=INVLD ADDR
    'O3RA1C' / construct.BitsInteger(4),
    'O3RA2O' / enum_81,  # 0=NO ERROR, 1=NOT INIT, 2=ALREADY INIT, 3=LL DRIVER NOT EXIST, 4=INVLD ADDR
    'O3RA2C' / construct.BitsInteger(4),
    'O4PN1O' / enum_80,  # 0=NO ERROR, 1=NOT INIT, 2=ALREADY INIT, 3=LL DRIVER NOT EXIST, 4=NOT IMPLEMENTED, 5=INVALID ADDR, 6=DEVICE BUSY, 7=WRITE ERR, 8=INTERFACE BUSY, 9=TIMEOUT, 10=INVALID LEN, 11=ERASE ERR
    'O4PN1C' / construct.BitsInteger(4),
    'O4PN2O' / enum_80,  # 0=NO ERROR, 1=NOT INIT, 2=ALREADY INIT, 3=LL DRIVER NOT EXIST, 4=NOT IMPLEMENTED, 5=INVALID ADDR, 6=DEVICE BUSY, 7=WRITE ERR, 8=INTERFACE BUSY, 9=TIMEOUT, 10=INVALID LEN, 11=ERASE ERR
    'O4PN2C' / construct.BitsInteger(4),
    'O4SNFO' / enum_80,  # 0=NO ERROR, 1=NOT INIT, 2=ALREADY INIT, 3=LL DRIVER NOT EXIST, 4=NOT IMPLEMENTED, 5=INVALID ADDR, 6=DEVICE BUSY, 7=WRITE ERR, 8=INTERFACE BUSY, 9=TIMEOUT, 10=INVALID LEN, 11=ERASE ERR
    'O4SNFC' / construct.BitsInteger(4),
    'O4RA1O' / enum_81,  # 0=NO ERROR, 1=NOT INIT, 2=ALREADY INIT, 3=LL DRIVER NOT EXIST, 4=INVLD ADDR
    'O4RA1C' / construct.BitsInteger(4),
    'O4RA2O' / enum_81,  # 0=NO ERROR, 1=NOT INIT, 2=ALREADY INIT, 3=LL DRIVER NOT EXIST, 4=INVLD ADDR
    'O4RA2C' / construct.BitsInteger(4),
    'O1P2RG' / enum_82,  # 1=NO RESET, 0=RESET
    'O1P5RG' / enum_82,  # 1=NO RESET, 0=RESET
    'O1VHRG' / enum_82,  # 1=NO RESET, 0=RESET
    'O1UHRG' / enum_82,  # 1=NO RESET, 0=RESET
    'O1FREQ' / enum_83,  # 0=6, 5=96, 6=120, 7=144, 8=168, 9=8, 10=16, 11=32, 12=64, 1=12, 2=24, 3=48, 4=72
    'O1CBVL' / common.EvalAdapter('0.07936508*x', construct.BitsInteger(6)),  # 0.07936508*x
    'O1HOFM' / enum_84,  # 0=UHF_VHF_ONLY, 1=SBAND_ONLY, 2=UHF_VHF_AND_SBAND
    'O1GNRG' / enum_82,  # 0=RESET, 1=NO RESET
    'O2P2RG' / enum_82,  # 1=NO RESET, 0=RESET
    'O2P5RG' / enum_82,  # 1=NO RESET, 0=RESET
    'O2VHRG' / enum_82,  # 1=NO RESET, 0=RESET
    'O2UHRG' / enum_82,  # 1=NO RESET, 0=RESET
    'O2FREQ' / enum_83,  # 0=6, 5=96, 6=120, 7=144, 8=168, 9=8, 10=16, 11=32, 12=64, 1=12, 2=24, 3=48, 4=72
    'O2CBVL' / common.EvalAdapter('0.07936508*x', construct.BitsInteger(6)),  # 0.07936508*x
    'O2HOFM' / enum_84,  # 0=UHF_VHF_ONLY, 1=SBAND_ONLY, 2=UHF_VHF_AND_SBAND
    'O2GNRG' / enum_82,  # 0=RESET, 1=NO RESET
    'O3P2RG' / enum_82,  # 1=NO RESET, 0=RESET
    'O3P5RG' / enum_82,  # 1=NO RESET, 0=RESET
    'O3VHRG' / enum_82,  # 1=NO RESET, 0=RESET
    'O3UHRG' / enum_82,  # 1=NO RESET, 0=RESET
    'O3FREQ' / enum_83,  # 0=6, 5=96, 6=120, 7=144, 8=168, 9=8, 10=16, 11=32, 12=64, 1=12, 2=24, 3=48, 4=72
    'O3CBVL' / common.EvalAdapter('0.07936508*x', construct.BitsInteger(6)),  # 0.07936508*x
    'O3HOFM' / enum_84,  # 0=UHF_VHF_ONLY, 1=SBAND_ONLY, 2=UHF_VHF_AND_SBAND
    'O3GNRG' / enum_82,  # 0=RESET, 1=NO RESET
    'O4P2RG' / enum_82,  # 1=NO RESET, 0=RESET
    'O4P5RG' / enum_82,  # 1=NO RESET, 0=RESET
    'O4VHRG' / enum_82,  # 1=NO RESET, 0=RESET
    'O4UHRG' / enum_82,  # 1=NO RESET, 0=RESET
    'O4FREQ' / enum_85,  # 0=6, 1=12, 2=24, 3=48, 4=72, 5=96, 6=120, 7=144, 8=168, 9=8, 10=16, 11=32, 12=64
    'O4CBVL' / common.EvalAdapter('0.07936508*x', construct.BitsInteger(6)),  # 0.07936508*x
    'O4HOFM' / enum_84,  # 0=UHF_VHF_ONLY, 1=SBAND_ONLY, 2=UHF_VHF_AND_SBAND
    'O4GNRG' / enum_82,  # 0=RESET, 1=NO RESET
    '_pad0' / construct.BitsInteger(4),
)

obdh_sto_rep_chk_hk = construct.BitStruct(
    '_name' / construct.Computed('obdh_sto_rep_chk_hk'),
    'name' / construct.Computed('OBDH STO REP CHK HK'),
    'O1RCAV' / enum_25,  # 0=NOT AVAILABLE, 1=AVAILABLE
    'O1RCST' / enum_86,  # 0=IDLE, 1=ERASE PAGES, 2=W4 SRC ADDR, 3=REPAIR IMG, 4=LOCKING CRC, 6=COMPUTE INT CRC, 5=COMPUTE EXT CRC, 7=W4_CRC_COMP_DONE, 8=PREP MEM TEST, 9=WR TEST PATTERN, 10=RD TEST PATTERN
    'O1RCPG' / common.EvalAdapter('0.392156863*x', construct.BitsInteger(8)),  # 0.392156863*x
    'O1RCEO' / enum_87,  # 0=NO ERROR, 1=INVALID STATE, 2=INVALID ADDR, 3=ERASE ERROR, 4=WRITE ERROR, 5=READ ERROR, 6=CRC INVALID, 7=INVALID PARAM, 8=PATTERN TEST ERR, 9=SUCCESSFUL, 10=FORBID ADDR
    'O1RCEC' / construct.BitsInteger(4),
    'O1RCRC' / construct.BitsInteger(32),
    'O2RCAV' / enum_25,  # 0=NOT AVAILABLE, 1=AVAILABLE
    'O2RCST' / enum_86,  # 0=IDLE, 1=ERASE PAGES, 2=W4 SRC ADDR, 3=REPAIR IMG, 4=LOCKING CRC, 6=COMPUTE INT CRC, 5=COMPUTE EXT CRC, 7=W4_CRC_COMP_DONE, 8=PREP MEM TEST, 9=WR TEST PATTERN, 10=RD TEST PATTERN
    'O2RCPG' / common.EvalAdapter('0.392156863*x', construct.BitsInteger(8)),  # 0.392156863*x
    'O2RCEO' / enum_87,  # 0=NO ERROR, 1=INVALID STATE, 2=INVALID ADDR, 3=ERASE ERROR, 4=WRITE ERROR, 5=READ ERROR, 6=CRC INVALID, 7=INVALID PARAM, 8=PATTERN TEST ERR, 9=SUCCESSFUL, 10=FORBID ADDR
    'O2RCEC' / construct.BitsInteger(4),
    'O2RCRC' / construct.BitsInteger(32),
    'O3RCAV' / enum_25,  # 0=NOT AVAILABLE, 1=AVAILABLE
    'O3RCST' / enum_86,  # 0=IDLE, 1=ERASE PAGES, 2=W4 SRC ADDR, 3=REPAIR IMG, 4=LOCKING CRC, 6=COMPUTE INT CRC, 5=COMPUTE EXT CRC, 7=W4_CRC_COMP_DONE, 8=PREP MEM TEST, 9=WR TEST PATTERN, 10=RD TEST PATTERN
    'O3RCPG' / common.EvalAdapter('0.392156863*x', construct.BitsInteger(8)),  # 0.392156863*x
    'O3RCEO' / enum_87,  # 0=NO ERROR, 1=INVALID STATE, 2=INVALID ADDR, 3=ERASE ERROR, 4=WRITE ERROR, 5=READ ERROR, 6=CRC INVALID, 7=INVALID PARAM, 8=PATTERN TEST ERR, 9=SUCCESSFUL, 10=FORBID ADDR
    'O3RCEC' / construct.BitsInteger(4),
    'O3RCRC' / construct.BitsInteger(32),
    'O4RCAV' / enum_25,  # 0=NOT AVAILABLE, 1=AVAILABLE
    'O4RCST' / enum_86,  # 0=IDLE, 1=ERASE PAGES, 2=W4 SRC ADDR, 3=REPAIR IMG, 4=LOCKING CRC, 6=COMPUTE INT CRC, 5=COMPUTE EXT CRC, 7=W4_CRC_COMP_DONE, 8=PREP MEM TEST, 9=WR TEST PATTERN, 10=RD TEST PATTERN
    'O4RCPG' / common.EvalAdapter('0.392156863*x', construct.BitsInteger(8)),  # 0.392156863*x
    'O4RCEO' / enum_87,  # 0=NO ERROR, 1=INVALID STATE, 2=INVALID ADDR, 3=ERASE ERROR, 4=WRITE ERROR, 5=READ ERROR, 6=CRC INVALID, 7=INVALID PARAM, 8=PATTERN TEST ERR, 9=SUCCESSFUL, 10=FORBID ADDR
    'O4RCEC' / construct.BitsInteger(4),
    'O4RCRC' / construct.BitsInteger(32),
    '_pad0' / construct.BitsInteger(4),
)

obdh_sw_upld = construct.BitStruct(
    '_name' / construct.Computed('obdh_sw_upld'),
    'name' / construct.Computed('OBDH SW UPLD'),
    'OSWURS' / construct.BitsInteger(1),
    'OSWUAV' / enum_25,  # 0=NOT AVAILABLE, 1=AVAILABLE
    'OSWUHW' / enum_36,  # 0=OBDH 1, 1=OBDH 2, 2=OBDH 3, 3=OBDH 4
    'OSWUIT' / enum_23,  # 0=FALSE, 1=TRUE
    'OSWUST' / enum_88,  # 0=IDLE, 1=ERASE PAGES, 2=AWAITING DATA, 3=AWAITING FINALIZE, 4=COMPUTE CRC
    'OSWUPG' / common.EvalAdapter('0.3921568*x', construct.BitsInteger(8)),  # 0.3921568*x
    'OSWUEO' / enum_89,  # 0=NO ERROR, 1=INVALID STATE, 2=WRITE ERROR, 3=READ ERROR, 4=INVALID ADDR, 5=INVALID CRC, 6=ERASE ERROR, 7=INVALID PARAM, 8=INVLD SEGMENT ORDER, 10=SUCCESSFUL, 9=INVLD SEGMENT NR, 11=FORBID ADDR
    'OSWUEC' / construct.BitsInteger(4),
    'OSWUSL' / construct.BitsInteger(8),
    'OSWULS' / construct.BitsInteger(32),
    'OSWULC' / construct.BitsInteger(32),
    'OSWUFL' / construct.BitsInteger(32),
)

obdh_ext_hk_buf_cnt = construct.BitStruct(
    '_name' / construct.Computed('obdh_ext_hk_buf_cnt'),
    'name' / construct.Computed('OBDH EXT HK BUF CNT'),
    'OAHKHW' / enum_36,  # 0=OBDH 1, 1=OBDH 2, 2=OBDH 3, 3=OBDH 4
    '_pad0' / construct.BitsInteger(6),
    'OASTDL' / construct.BitsInteger(16),
    'OAOPEL' / construct.BitsInteger(16),
    'OAADSL' / construct.BitsInteger(16),
    'OAAA1L' / construct.BitsInteger(16),
    'OAAA2L' / construct.BitsInteger(16),
    'OASS1L' / construct.BitsInteger(16),
    'OASS2L' / construct.BitsInteger(16),
    'OATH1L' / construct.BitsInteger(16),
    'OSWINL' / construct.BitsInteger(16),
    'OAPS1L' / construct.BitsInteger(16),
    'OAADEL' / construct.BitsInteger(16),
    'OAPLDL' / construct.BitsInteger(16),
    'OAEXPL' / construct.BitsInteger(16),
    'OASBDL' / construct.BitsInteger(16),
    'OAMOPL' / construct.BitsInteger(16),
    'OAISTL' / construct.BitsInteger(16),
    'OAI01L' / construct.BitsInteger(16),
    'OAI02L' / construct.BitsInteger(16),
    'OAI03L' / construct.BitsInteger(16),
    'OAI04L' / construct.BitsInteger(16),
    'OAI05L' / construct.BitsInteger(16),
    'OAI06L' / construct.BitsInteger(16),
    'OAI07L' / construct.BitsInteger(16),
    'OAI08L' / construct.BitsInteger(16),
    'OAI09L' / construct.BitsInteger(16),
    'OAI10L' / construct.BitsInteger(16),
    'OAMVSL' / construct.BitsInteger(16),
    'OATHRL' / construct.BitsInteger(16),
    'OALEOL' / construct.BitsInteger(16),
    'OAOECL' / construct.BitsInteger(16),
    'OAOMSL' / construct.BitsInteger(16),
    'OAOSWL' / construct.BitsInteger(16),
    'OAOSRL' / construct.BitsInteger(16),
    'OAGPSL' / construct.BitsInteger(16),
    'ORSTCL' / construct.BitsInteger(16),
    'OAMVEL' / construct.BitsInteger(16),
    'ORES2L' / construct.BitsInteger(16),
    'ORES1L' / construct.BitsInteger(16),
    'OERMBL' / construct.BitsInteger(16),
)

obdh_ext_tc_lst_len = construct.BitStruct(
    '_name' / construct.Computed('obdh_ext_tc_lst_len'),
    'name' / construct.Computed('OBDH EXT TC LST LEN'),
    'OAAS1L' / construct.BitsInteger(8),
    'OAAS2L' / construct.BitsInteger(8),
    'OAAS3L' / construct.BitsInteger(8),
    'OAPASL' / construct.BitsInteger(8),
    'OALP1L' / construct.BitsInteger(8),
    'OALP2L' / construct.BitsInteger(8),
    'OALP3L' / construct.BitsInteger(8),
    'OAR01L' / construct.BitsInteger(8),
    'OAR02L' / construct.BitsInteger(8),
    'OAR03L' / construct.BitsInteger(8),
    'OAR04L' / construct.BitsInteger(8),
    'OAR05L' / construct.BitsInteger(8),
    'OAR06L' / construct.BitsInteger(8),
    'OAR07L' / construct.BitsInteger(8),
    'OAR08L' / construct.BitsInteger(8),
    'OAR09L' / construct.BitsInteger(8),
    'OAR10L' / construct.BitsInteger(8),
    'OAR11L' / construct.BitsInteger(8),
    'OAR12L' / construct.BitsInteger(8),
    'OAR13L' / construct.BitsInteger(8),
    'OAR14L' / construct.BitsInteger(8),
    'OAR15L' / construct.BitsInteger(8),
    'OAR16L' / construct.BitsInteger(8),
    'OAATTL' / construct.BitsInteger(12),
    'OAPTTL' / construct.BitsInteger(12),
    'OATCHW' / enum_36,  # 0=OBDH 1, 1=OBDH 2, 2=OBDH 3, 3=OBDH 4
    '_pad0' / construct.BitsInteger(6),
)

obdh_rst_cntr_hk = construct.BitStruct(
    '_name' / construct.Computed('obdh_rst_cntr_hk'),
    'name' / construct.Computed('OBDH RST CNTR HK'),
    'OVHF1X' / enum_37,  # 1=YES, 0=NO
    'OVHF1S' / enum_90,  # 1=VALID, 0=INVALID
    'OVHF1B' / enum_90,  # 0=INVALID, 1=VALID
    'OVHF1C' / construct.BitsInteger(5),
    'OUHF1X' / enum_37,  # 1=YES, 0=NO
    'OUHF1S' / enum_90,  # 1=VALID, 0=INVALID
    'OUHF1B' / enum_90,  # 0=INVALID, 1=VALID
    'OUHF1C' / construct.BitsInteger(5),
    'ORWX1X' / enum_37,  # 1=YES, 0=NO
    'ORWX1S' / enum_90,  # 1=VALID, 0=INVALID
    'ORWX1B' / enum_90,  # 0=INVALID, 1=VALID
    'ORWX1C' / construct.BitsInteger(5),
    'ORWY1X' / enum_37,  # 1=YES, 0=NO
    'ORWY1S' / enum_90,  # 1=VALID, 0=INVALID
    'ORWY1B' / enum_90,  # 0=INVALID, 1=VALID
    'ORWY1C' / construct.BitsInteger(5),
    'ORWZ1X' / enum_37,  # 1=YES, 0=NO
    'ORWZ1S' / enum_90,  # 1=VALID, 0=INVALID
    'ORWZ1B' / enum_90,  # 0=INVALID, 1=VALID
    'ORWZ1C' / construct.BitsInteger(5),
    'OSXP1X' / enum_37,  # 1=YES, 0=NO
    'OSXP1S' / enum_90,  # 1=VALID, 0=INVALID
    'OSXP1B' / enum_90,  # 0=INVALID, 1=VALID
    'OSXP1C' / construct.BitsInteger(5),
    'OSXN1X' / enum_37,  # 1=YES, 0=NO
    'OSXN1S' / enum_90,  # 1=VALID, 0=INVALID
    'OSXN1B' / enum_90,  # 0=INVALID, 1=VALID
    'OSXN1C' / construct.BitsInteger(5),
    'OSYP1X' / enum_37,  # 1=YES, 0=NO
    'OSYP1S' / enum_90,  # 1=VALID, 0=INVALID
    'OSYP1B' / enum_90,  # 0=INVALID, 1=VALID
    'OSYP1C' / construct.BitsInteger(5),
    'OSYN1X' / enum_37,  # 1=YES, 0=NO
    'OSYN1S' / enum_90,  # 1=VALID, 0=INVALID
    'OSYN1B' / enum_90,  # 0=INVALID, 1=VALID
    'OSYN1C' / construct.BitsInteger(5),
    'OSZP1X' / enum_37,  # 1=YES, 0=NO
    'OSZP1S' / enum_90,  # 1=VALID, 0=INVALID
    'OSZP1B' / enum_90,  # 0=INVALID, 1=VALID
    'OSZP1C' / construct.BitsInteger(5),
    'OSZN1X' / enum_37,  # 1=YES, 0=NO
    'OSZN1S' / enum_90,  # 1=VALID, 0=INVALID
    'OSZN1B' / enum_90,  # 0=INVALID, 1=VALID
    'OSZN1C' / construct.BitsInteger(5),
    'OADC1X' / enum_37,  # 1=YES, 0=NO
    'OADC1S' / enum_90,  # 1=VALID, 0=INVALID
    'OADC1B' / enum_90,  # 0=INVALID, 1=VALID
    'OADC1C' / construct.BitsInteger(5),
    'OIFP1X' / enum_37,  # 1=YES, 0=NO
    'OIFP1S' / enum_90,  # 1=VALID, 0=INVALID
    'OIFP1B' / enum_90,  # 0=INVALID, 1=VALID
    'OIFP1C' / construct.BitsInteger(5),
    'OP5V1X' / enum_37,  # 1=YES, 0=NO
    'OP5V1S' / enum_90,  # 1=VALID, 0=INVALID
    'OP5V1B' / enum_90,  # 0=INVALID, 1=VALID
    'OP5V1C' / construct.BitsInteger(5),
    'O12V1X' / enum_37,  # 1=YES, 0=NO
    'O12V1S' / enum_90,  # 1=VALID, 0=INVALID
    'O12V1B' / enum_90,  # 0=INVALID, 1=VALID
    'O12V1C' / construct.BitsInteger(5),
    'OMVW1X' / enum_37,  # 1=YES, 0=NO
    'OMVW1S' / enum_90,  # 1=VALID, 0=INVALID
    'OMVW1B' / enum_90,  # 0=INVALID, 1=VALID
    'OMVW1C' / construct.BitsInteger(5),
    'OVHF2X' / enum_37,  # 1=YES, 0=NO
    'OVHF2S' / enum_90,  # 1=VALID, 0=INVALID
    'OVHF2B' / enum_90,  # 0=INVALID, 1=VALID
    'OVHF2C' / construct.BitsInteger(5),
    'OUHF2X' / enum_37,  # 1=YES, 0=NO
    'OUHF2S' / enum_90,  # 1=VALID, 0=INVALID
    'OUHF2B' / enum_90,  # 0=INVALID, 1=VALID
    'OUHF2C' / construct.BitsInteger(5),
    'ORWX2X' / enum_37,  # 1=YES, 0=NO
    'ORWX2S' / enum_90,  # 1=VALID, 0=INVALID
    'ORWX2B' / enum_90,  # 0=INVALID, 1=VALID
    'ORWX2C' / construct.BitsInteger(5),
    'ORWY2X' / enum_37,  # 1=YES, 0=NO
    'ORWY2S' / enum_90,  # 1=VALID, 0=INVALID
    'ORWY2B' / enum_90,  # 0=INVALID, 1=VALID
    'ORWY2C' / construct.BitsInteger(5),
    'ORWZ2X' / enum_37,  # 1=YES, 0=NO
    'ORWZ2S' / enum_90,  # 1=VALID, 0=INVALID
    'ORWZ2B' / enum_90,  # 0=INVALID, 1=VALID
    'ORWZ2C' / construct.BitsInteger(5),
    'OSXP2X' / enum_37,  # 1=YES, 0=NO
    'OSXP2S' / enum_90,  # 1=VALID, 0=INVALID
    'OSXP2B' / enum_90,  # 0=INVALID, 1=VALID
    'OSXP2C' / construct.BitsInteger(5),
    'OSXN2X' / enum_37,  # 1=YES, 0=NO
    'OSXN2S' / enum_90,  # 1=VALID, 0=INVALID
    'OSXN2B' / enum_90,  # 0=INVALID, 1=VALID
    'OSXN2C' / construct.BitsInteger(5),
    'OSYP2X' / enum_37,  # 1=YES, 0=NO
    'OSYP2S' / enum_90,  # 1=VALID, 0=INVALID
    'OSYP2B' / enum_90,  # 0=INVALID, 1=VALID
    'OSYP2C' / construct.BitsInteger(5),
    'OSYN2X' / enum_37,  # 1=YES, 0=NO
    'OSYN2S' / enum_90,  # 1=VALID, 0=INVALID
    'OSYN2B' / enum_90,  # 0=INVALID, 1=VALID
    'OSYN2C' / construct.BitsInteger(5),
    'OSZP2X' / enum_37,  # 1=YES, 0=NO
    'OSZP2S' / enum_90,  # 1=VALID, 0=INVALID
    'OSZP2B' / enum_90,  # 0=INVALID, 1=VALID
    'OSZP2C' / construct.BitsInteger(5),
    'OSZN2X' / enum_37,  # 1=YES, 0=NO
    'OSZN2S' / enum_90,  # 1=VALID, 0=INVALID
    'OSZN2B' / enum_90,  # 0=INVALID, 1=VALID
    'OSZN2C' / construct.BitsInteger(5),
    'OADC2X' / enum_37,  # 1=YES, 0=NO
    'OADC2S' / enum_90,  # 1=VALID, 0=INVALID
    'OADC2B' / enum_90,  # 0=INVALID, 1=VALID
    'OADC2C' / construct.BitsInteger(5),
    'OIFP2X' / enum_37,  # 1=YES, 0=NO
    'OIFP2S' / enum_90,  # 1=VALID, 0=INVALID
    'OIFP2B' / enum_90,  # 0=INVALID, 1=VALID
    'OIFP2C' / construct.BitsInteger(5),
    'OP5V2X' / enum_37,  # 1=YES, 0=NO
    'OP5V2S' / enum_90,  # 1=VALID, 0=INVALID
    'OP5V2B' / enum_90,  # 0=INVALID, 1=VALID
    'OP5V2C' / construct.BitsInteger(5),
    'O12V2X' / enum_37,  # 1=YES, 0=NO
    'O12V2S' / enum_90,  # 1=VALID, 0=INVALID
    'O12V2B' / enum_90,  # 0=INVALID, 1=VALID
    'O12V2C' / construct.BitsInteger(5),
    'OMVW2X' / enum_37,  # 1=YES, 0=NO
    'OMVW2S' / enum_90,  # 1=VALID, 0=INVALID
    'OMVW2B' / enum_90,  # 0=INVALID, 1=VALID
    'OMVW2C' / construct.BitsInteger(5),
    'OVHF1M' / enum_91,  # 0=UNKNOWN, 1=LPM RST, 2=WWDG RST, 3=IWDG RST, 4=SW RST, 5=BROWN-OUT RST, 6=PIN RST, 7=OPTN BYTE LD RST, 8=FIREWALL RST
    'OVHF2M' / enum_91,  # 0=UNKNOWN, 1=LPM RST, 2=WWDG RST, 3=IWDG RST, 4=SW RST, 5=BROWN-OUT RST, 6=PIN RST, 7=OPTN BYTE LD RST, 8=FIREWALL RST
    'OUHF1M' / enum_91,  # 0=UNKNOWN, 1=LPM RST, 2=WWDG RST, 3=IWDG RST, 4=SW RST, 5=BROWN-OUT RST, 6=PIN RST, 7=OPTN BYTE LD RST, 8=FIREWALL RST
    'OUHF2M' / enum_91,  # 0=UNKNOWN, 1=LPM RST, 2=WWDG RST, 3=IWDG RST, 4=SW RST, 5=BROWN-OUT RST, 6=PIN RST, 7=OPTN BYTE LD RST, 8=FIREWALL RST
    'ORWX1M' / enum_91,  # 0=UNKNOWN, 1=LPM RST, 2=WWDG RST, 3=IWDG RST, 4=SW RST, 5=BROWN-OUT RST, 6=PIN RST, 7=OPTN BYTE LD RST, 8=FIREWALL RST
    'ORWX2M' / enum_91,  # 0=UNKNOWN, 1=LPM RST, 2=WWDG RST, 3=IWDG RST, 4=SW RST, 5=BROWN-OUT RST, 6=PIN RST, 7=OPTN BYTE LD RST, 8=FIREWALL RST
    'ORWY1M' / enum_91,  # 0=UNKNOWN, 1=LPM RST, 2=WWDG RST, 3=IWDG RST, 4=SW RST, 5=BROWN-OUT RST, 6=PIN RST, 7=OPTN BYTE LD RST, 8=FIREWALL RST
    'ORWY2M' / enum_91,  # 0=UNKNOWN, 1=LPM RST, 2=WWDG RST, 3=IWDG RST, 4=SW RST, 5=BROWN-OUT RST, 6=PIN RST, 7=OPTN BYTE LD RST, 8=FIREWALL RST
    'ORWZ1M' / enum_91,  # 0=UNKNOWN, 1=LPM RST, 2=WWDG RST, 3=IWDG RST, 4=SW RST, 5=BROWN-OUT RST, 6=PIN RST, 7=OPTN BYTE LD RST, 8=FIREWALL RST
    'ORWZ2M' / enum_91,  # 0=UNKNOWN, 1=LPM RST, 2=WWDG RST, 3=IWDG RST, 4=SW RST, 5=BROWN-OUT RST, 6=PIN RST, 7=OPTN BYTE LD RST, 8=FIREWALL RST
    'OSXP1M' / enum_91,  # 0=UNKNOWN, 1=LPM RST, 2=WWDG RST, 3=IWDG RST, 4=SW RST, 5=BROWN-OUT RST, 6=PIN RST, 7=OPTN BYTE LD RST, 8=FIREWALL RST
    'OSXP2M' / enum_91,  # 0=UNKNOWN, 1=LPM RST, 2=WWDG RST, 3=IWDG RST, 4=SW RST, 5=BROWN-OUT RST, 6=PIN RST, 7=OPTN BYTE LD RST, 8=FIREWALL RST
    'OSXN1M' / enum_91,  # 0=UNKNOWN, 1=LPM RST, 2=WWDG RST, 3=IWDG RST, 4=SW RST, 5=BROWN-OUT RST, 6=PIN RST, 7=OPTN BYTE LD RST, 8=FIREWALL RST
    'OSXN2M' / enum_91,  # 0=UNKNOWN, 1=LPM RST, 2=WWDG RST, 3=IWDG RST, 4=SW RST, 5=BROWN-OUT RST, 6=PIN RST, 7=OPTN BYTE LD RST, 8=FIREWALL RST
    'OSYP1M' / enum_91,  # 0=UNKNOWN, 1=LPM RST, 2=WWDG RST, 3=IWDG RST, 4=SW RST, 5=BROWN-OUT RST, 6=PIN RST, 7=OPTN BYTE LD RST, 8=FIREWALL RST
    'OSYP2M' / enum_91,  # 0=UNKNOWN, 1=LPM RST, 2=WWDG RST, 3=IWDG RST, 4=SW RST, 5=BROWN-OUT RST, 6=PIN RST, 7=OPTN BYTE LD RST, 8=FIREWALL RST
    'OSYN1M' / enum_91,  # 0=UNKNOWN, 1=LPM RST, 2=WWDG RST, 3=IWDG RST, 4=SW RST, 5=BROWN-OUT RST, 6=PIN RST, 7=OPTN BYTE LD RST, 8=FIREWALL RST
    'OSYN2M' / enum_91,  # 0=UNKNOWN, 1=LPM RST, 2=WWDG RST, 3=IWDG RST, 4=SW RST, 5=BROWN-OUT RST, 6=PIN RST, 7=OPTN BYTE LD RST, 8=FIREWALL RST
    'OSZP1M' / enum_91,  # 0=UNKNOWN, 1=LPM RST, 2=WWDG RST, 3=IWDG RST, 4=SW RST, 5=BROWN-OUT RST, 6=PIN RST, 7=OPTN BYTE LD RST, 8=FIREWALL RST
    'OSZP2M' / enum_91,  # 0=UNKNOWN, 1=LPM RST, 2=WWDG RST, 3=IWDG RST, 4=SW RST, 5=BROWN-OUT RST, 6=PIN RST, 7=OPTN BYTE LD RST, 8=FIREWALL RST
    'OSZN1M' / enum_91,  # 0=UNKNOWN, 1=LPM RST, 2=WWDG RST, 3=IWDG RST, 4=SW RST, 5=BROWN-OUT RST, 6=PIN RST, 7=OPTN BYTE LD RST, 8=FIREWALL RST
    'OSZN2M' / enum_91,  # 0=UNKNOWN, 1=LPM RST, 2=WWDG RST, 3=IWDG RST, 4=SW RST, 5=BROWN-OUT RST, 6=PIN RST, 7=OPTN BYTE LD RST, 8=FIREWALL RST
    'OADC1M' / enum_91,  # 0=UNKNOWN, 1=LPM RST, 2=WWDG RST, 3=IWDG RST, 4=SW RST, 5=BROWN-OUT RST, 6=PIN RST, 7=OPTN BYTE LD RST, 8=FIREWALL RST
    'OADC2M' / enum_91,  # 0=UNKNOWN, 1=LPM RST, 2=WWDG RST, 3=IWDG RST, 4=SW RST, 5=BROWN-OUT RST, 6=PIN RST, 7=OPTN BYTE LD RST, 8=FIREWALL RST
    'OIFP1M' / enum_92,  # 0=UNKNOWN, 1=JTAG RST, 2=WATCHDOG RST, 3=BROWN OUT RST, 4=EXTERNAL RST, 5=POWER ON RST
    'OIFP2M' / enum_92,  # 0=UNKNOWN, 1=JTAG RST, 2=WATCHDOG RST, 3=BROWN OUT RST, 4=EXTERNAL RST, 5=POWER ON RST
    'OP5V1M' / enum_92,  # 0=UNKNOWN, 1=JTAG RST, 2=WATCHDOG RST, 3=BROWN OUT RST, 4=EXTERNAL RST, 5=POWER ON RST
    'OP5V2M' / enum_92,  # 0=UNKNOWN, 1=JTAG RST, 2=WATCHDOG RST, 3=BROWN OUT RST, 4=EXTERNAL RST, 5=POWER ON RST
    'O12V1M' / enum_92,  # 0=UNKNOWN, 1=JTAG RST, 2=WATCHDOG RST, 3=BROWN OUT RST, 4=EXTERNAL RST, 5=POWER ON RST
    'O12V2M' / enum_92,  # 0=UNKNOWN, 1=JTAG RST, 2=WATCHDOG RST, 3=BROWN OUT RST, 4=EXTERNAL RST, 5=POWER ON RST
    'OMVW1M' / enum_91,  # 0=UNKNOWN, 1=LPM RST, 2=WWDG RST, 3=IWDG RST, 4=SW RST, 5=BROWN-OUT RST, 6=PIN RST, 7=OPTN BYTE LD RST, 8=FIREWALL RST
    'OMVW2M' / enum_91,  # 0=UNKNOWN, 1=LPM RST, 2=WWDG RST, 3=IWDG RST, 4=SW RST, 5=BROWN-OUT RST, 6=PIN RST, 7=OPTN BYTE LD RST, 8=FIREWALL RST
    'OAIM1X' / enum_37,  # 1=YES, 0=NO
    'OAIM1S' / enum_90,  # 1=VALID, 0=INVALID
    'OAIM1B' / enum_90,  # 0=INVALID, 1=VALID
    'OAIM1C' / construct.BitsInteger(5),
    'OTHR1X' / enum_37,  # 1=YES, 0=NO
    'OTHR1S' / enum_90,  # 1=VALID, 0=INVALID
    'OTHR1B' / enum_90,  # 0=INVALID, 1=VALID
    'OTHR1C' / construct.BitsInteger(5),
    'OAIM2X' / enum_37,  # 1=YES, 0=NO
    'OAIM2S' / enum_90,  # 1=VALID, 0=INVALID
    'OAIM2B' / enum_90,  # 0=INVALID, 1=VALID
    'OAIM2C' / construct.BitsInteger(5),
    'OTHR2X' / enum_37,  # 1=YES, 0=NO
    'OTHR2S' / enum_90,  # 1=VALID, 0=INVALID
    'OTHR2B' / enum_90,  # 0=INVALID, 1=VALID
    'OTHR2C' / construct.BitsInteger(5),
    'OOBC1X' / enum_37,  # 1=YES, 0=NO
    'OOBC1S' / enum_90,  # 1=VALID, 0=INVALID
    'OOBC1B' / enum_90,  # 0=INVALID, 1=VALID
    'OOBC1C' / construct.BitsInteger(5),
    'OOBC2X' / enum_37,  # 1=YES, 0=NO
    'OOBC2S' / enum_90,  # 1=VALID, 0=INVALID
    'OOBC2B' / enum_90,  # 0=INVALID, 1=VALID
    'OOBC2C' / construct.BitsInteger(5),
    'OOBC3X' / enum_37,  # 1=YES, 0=NO
    'OOBC3S' / enum_90,  # 1=VALID, 0=INVALID
    'OOBC3B' / enum_90,  # 0=INVALID, 1=VALID
    'OOBC3C' / construct.BitsInteger(5),
    'OOBC4X' / enum_37,  # 1=YES, 0=NO
    'OOBC4S' / enum_90,  # 1=VALID, 0=INVALID
    'OOBC4B' / enum_90,  # 0=INVALID, 1=VALID
    'OOBC4C' / construct.BitsInteger(5),
    'OAIM1M' / enum_91,  # 0=UNKNOWN, 1=LPM RST, 2=WWDG RST, 3=IWDG RST, 4=SW RST, 5=BROWN-OUT RST, 6=PIN RST, 7=OPTN BYTE LD RST, 8=FIREWALL RST
    'OAIM2M' / enum_91,  # 0=UNKNOWN, 1=LPM RST, 2=WWDG RST, 3=IWDG RST, 4=SW RST, 5=BROWN-OUT RST, 6=PIN RST, 7=OPTN BYTE LD RST, 8=FIREWALL RST
    'OTHR1M' / enum_92,  # 0=UNKNOWN, 1=JTAG RST, 2=WATCHDOG RST, 3=BROWN OUT RST, 4=EXTERNAL RST, 5=POWER ON RST
    'OTHR2M' / enum_92,  # 0=UNKNOWN, 1=JTAG RST, 2=WATCHDOG RST, 3=BROWN OUT RST, 4=EXTERNAL RST, 5=POWER ON RST
    'OOBC2M' / enum_93,  # 0=UNKNOWN, 1=LPM RST, 2=WWDG RST, 3=IWDG RST, 4=SW RST, 5=POR PDR RST, 6=PIN RST, 7=BOR RST
    'OOBC1M' / enum_93,  # 0=UNKNOWN, 1=LPM RST, 2=WWDG RST, 3=IWDG RST, 4=SW RST, 5=POR PDR RST, 6=PIN RST, 7=BOR RST
    'OOBC4M' / enum_93,  # 0=UNKNOWN, 1=LPM RST, 2=WWDG RST, 3=IWDG RST, 4=SW RST, 5=POR PDR RST, 6=PIN RST, 7=BOR RST
    'OOBC3M' / enum_93,  # 0=UNKNOWN, 1=LPM RST, 2=WWDG RST, 3=IWDG RST, 4=SW RST, 5=POR PDR RST, 6=PIN RST, 7=BOR RST
    'OGNS1X' / enum_37,  # 1=YES, 0=NO
    'OGNS1S' / enum_90,  # 0=INVALID, 1=VALID
    'OGNS1B' / enum_90,  # 0=INVALID, 1=VALID
    'OGNS1C' / construct.BitsInteger(5),
    'OGNS2X' / enum_37,  # 1=YES, 0=NO
    'OGNS2S' / enum_90,  # 0=INVALID, 1=VALID
    'OGNS2B' / enum_90,  # 0=INVALID, 1=VALID
    'OGNS2C' / construct.BitsInteger(5),
    'OGNS2M' / enum_91,  # 0=UNKNOWN, 1=LPM RST, 2=WWDG RST, 3=IWDG RST, 4=SW RST, 5=BROWN-OUT RST, 6=PIN RST, 7=OPTN BYTE LD RST, 8=FIREWALL RST
    'OGNS1M' / enum_91,  # 0=UNKNOWN, 1=LPM RST, 2=WWDG RST, 3=IWDG RST, 4=SW RST, 5=BROWN-OUT RST, 6=PIN RST, 7=OPTN BYTE LD RST, 8=FIREWALL RST
    'ORSTEO' / enum_94,  # 0=NO ERROR, 1=INVLD MIC, 2=INVLD SAT BUS, 3=INVLD BOOT MSG LEN, 4=INVLD SW IMG, 5=INVLD BTLDR IMG
    'ORSTEC' / construct.BitsInteger(4),
    'ORSTHW' / enum_36,  # 0=OBDH 1, 1=OBDH 2, 2=OBDH 3, 3=OBDH 4
    'ORSTAV' / construct.BitsInteger(1),
    'ORSTRS' / construct.BitsInteger(5),
)

obdh_sw_inst = construct.BitStruct(
    '_name' / construct.Computed('obdh_sw_inst'),
    'name' / construct.Computed('OBDH SW INST'),
    'OSWIST' / enum_95,  # 0=IDLE, 1=COMPUTE CRC, 2=CNCT TO BTLDR, 3=ERASE IMAGE, 4=WRITE IMAGE, 5=READ IMAGE, 6=START APP, 7=END, 8=DISCNCT FROM BTLDR
    'OSWIAR' / enum_96,  # 0=STM32 CAN, 1=ATMEGA CAN, 2=CUSTOM STM32, 3=INVALID
    'OSWIHW' / enum_36,  # 0=OBDH 1, 1=OBDH 2, 2=OBDH 3, 3=OBDH 4
    'OSWIEO' / enum_97,  # 0=NO ERROR, 1=TIMEOUT, 2=NACK, 3=READ ERROR, 4=INVALID CRC, 5=INVALID STATE, 6=INVALID RESPONSE, 7=INVALID VALUE, 8=ERROR RETURNED, 9=INVALID MIC, 10=INVLD ACK COUNT, 11=INT FLAH WR ERR, 12=INT FLASH ER ERR, 13=INVLD META DATA, 14=SUCCESSFUL, 15=SELFUPDATE PREP FAIL
    'OSWIEC' / construct.BitsInteger(4),
    'OSWIPG' / common.EvalAdapter('0.39215686*x', construct.BitsInteger(8)),  # 0.39215686*x
    'OSWIUC' / enum_98,  # 1=ADCS BTLDR, 2=VHF BTLDR, 3=UHF BTLDR, 4=SS BTLDR, 5=RW BTLDR, 6=AI MIC BTLDR, 7=MVIEW BTLDR, 10=PCU 5V APP, 11=PCU 12V APP, 12=IFP APP, 13=THRUSTER APP, 8=OBDH BTLDR, 15=OBDH 1 APP, 16=OBDH 2 APP, 17=OBDH 3 APP, 18=OBDH 4 APP, 19=VHF APP, 20=UHF APP, 21=RW X APP, 22=RW Y APP, 23=RW Z APP, 24=SS XP APP, 25=SS XN APP, 26=SS YP APP, 27=SS YN APP, 28=SS ZP APP, 29=SS ZN APP, 31=ADCS APP, 32=MVIEW APP, 33=AI MIC APP, 9=GNSS BTLDR, 30=GNSS APP
    'OSWIBS' / enum_99,  # 0=BUS 1, 1=BUS 2
    'OSWICR' / construct.BitsInteger(32),
    'OSWIAV' / enum_25,  # 0=NOT AVAILABLE, 1=AVAILABLE
    'OSWITK' / enum_100,  # 1=WRITE TASK, 2=READ TASK, 3=RUN APP TASK, 0=NONE, 4=ERASE TASK
    'O1P2BG' / enum_101,  # 1=BOOTLOADER, 0=RUN
    'O1P5BG' / enum_101,  # 1=BOOTLOADER, 0=RUN
    'O1VHBG' / enum_101,  # 1=BOOTLOADER, 0=RUN
    'O1UHBG' / enum_101,  # 1=BOOTLOADER, 0=RUN
    'O1ADBG' / enum_101,  # 1=BOOTLOADER, 0=RUN
    'O1AIBG' / enum_101,  # 1=BOOTLOADER, 0=RUN
    'O1IFBG' / enum_101,  # 1=BOOTLOADER, 0=RUN
    'O1OBBG' / enum_101,  # 1=BOOTLOADER, 0=RUN
    'O1BPAV' / enum_25,  # 0=NOT AVAILABLE, 1=AVAILABLE
    'O2P2BG' / enum_101,  # 1=BOOTLOADER, 0=RUN
    'O2P5BG' / enum_101,  # 1=BOOTLOADER, 0=RUN
    'O2VHBG' / enum_101,  # 1=BOOTLOADER, 0=RUN
    'O2UHBG' / enum_101,  # 1=BOOTLOADER, 0=RUN
    'O2ADBG' / enum_101,  # 1=BOOTLOADER, 0=RUN
    'O2AIBG' / enum_101,  # 1=BOOTLOADER, 0=RUN
    'O2IFBG' / enum_101,  # 1=BOOTLOADER, 0=RUN
    'O2OBBG' / enum_101,  # 1=BOOTLOADER, 0=RUN
    'O2BPAV' / enum_25,  # 0=NOT AVAILABLE, 1=AVAILABLE
    'O3P2BG' / enum_101,  # 1=BOOTLOADER, 0=RUN
    'O3P5BG' / enum_101,  # 1=BOOTLOADER, 0=RUN
    'O3VHBG' / enum_101,  # 1=BOOTLOADER, 0=RUN
    'O3UHBG' / enum_101,  # 1=BOOTLOADER, 0=RUN
    'O3ADBG' / enum_101,  # 1=BOOTLOADER, 0=RUN
    'O3AIBG' / enum_101,  # 1=BOOTLOADER, 0=RUN
    'O3IFBG' / enum_101,  # 1=BOOTLOADER, 0=RUN
    'O3OBBG' / enum_101,  # 1=BOOTLOADER, 0=RUN
    'O3BPAV' / enum_25,  # 0=NOT AVAILABLE, 1=AVAILABLE
    'O4P2BG' / enum_101,  # 1=BOOTLOADER, 0=RUN
    'O4P5BG' / enum_101,  # 1=BOOTLOADER, 0=RUN
    'O4VHBG' / enum_101,  # 1=BOOTLOADER, 0=RUN
    'O4UHBG' / enum_101,  # 1=BOOTLOADER, 0=RUN
    'O4ADBG' / enum_101,  # 1=BOOTLOADER, 0=RUN
    'O4AIBG' / enum_101,  # 1=BOOTLOADER, 0=RUN
    'O4IFBG' / enum_101,  # 1=BOOTLOADER, 0=RUN
    'O4OBBG' / enum_101,  # 1=BOOTLOADER, 0=RUN
    'O4BPAV' / enum_25,  # 0=NOT AVAILABLE, 1=AVAILABLE
    'SSXP1B' / enum_102,  # 0=RUN, 1=BOOTLOADER
    'SSXN1B' / enum_102,  # 0=RUN, 1=BOOTLOADER
    'SSYP1B' / enum_102,  # 0=RUN, 1=BOOTLOADER
    'SSYN1B' / enum_102,  # 0=RUN, 1=BOOTLOADER
    'SSZP1B' / enum_102,  # 0=RUN, 1=BOOTLOADER
    'SSZN1B' / enum_102,  # 0=RUN, 1=BOOTLOADER
    'THR1BP' / enum_102,  # 0=RUN, 1=BOOTLOADER
    'MV1BOP' / enum_102,  # 0=RUN, 1=BOOTLOADER
    'P5V1B1' / enum_25,  # 0=NOT AVAILABLE, 1=AVAILABLE
    'P5V1B2' / enum_25,  # 0=NOT AVAILABLE, 1=AVAILABLE
    'P5V1B3' / enum_25,  # 0=NOT AVAILABLE, 1=AVAILABLE
    'P5V1B4' / enum_25,  # 0=NOT AVAILABLE, 1=AVAILABLE
    'SSXP2B' / enum_102,  # 0=RUN, 1=BOOTLOADER
    'SSXN2B' / enum_102,  # 0=RUN, 1=BOOTLOADER
    'SSYP2B' / enum_102,  # 0=RUN, 1=BOOTLOADER
    'SSYN2B' / enum_102,  # 0=RUN, 1=BOOTLOADER
    'SSZP2B' / enum_102,  # 0=RUN, 1=BOOTLOADER
    'SSZN2B' / enum_102,  # 0=RUN, 1=BOOTLOADER
    'THR2BP' / enum_102,  # 0=RUN, 1=BOOTLOADER
    'MV2BOP' / enum_102,  # 0=RUN, 1=BOOTLOADER
    'P5V2B1' / enum_25,  # 0=NOT AVAILABLE, 1=AVAILABLE
    'P5V2B2' / enum_25,  # 0=NOT AVAILABLE, 1=AVAILABLE
    'P5V2B3' / enum_25,  # 0=NOT AVAILABLE, 1=AVAILABLE
    'P5V2B4' / enum_25,  # 0=NOT AVAILABLE, 1=AVAILABLE
    'RWX1BO' / enum_103,  # 0=RUN, 1=PROGRAM
    'RWY1BO' / enum_103,  # 0=RUN, 1=PROGRAM
    'RWZ1BO' / enum_103,  # 0=RUN, 1=PROGRAM
    'IFP1AV' / enum_25,  # 0=NOT AVAILABLE, 1=AVAILABLE
    'RWX2BO' / enum_103,  # 0=RUN, 1=PROGRAM
    'RWY2BO' / enum_103,  # 0=RUN, 1=PROGRAM
    'RWZ2BO' / enum_103,  # 0=RUN, 1=PROGRAM
    'IFP2AV' / enum_25,  # 0=NOT AVAILABLE, 1=AVAILABLE
)

obdh_thread_run_time_hk = construct.BitStruct(
    '_name' / construct.Computed('obdh_thread_run_time_hk'),
    'name' / construct.Computed('OBDH THREAD RUN TIME HK'),
    'OWDTRT' / common.EvalAdapter('1*x', construct.BitsInteger(16)),  # 1*x
    'ORMTRT' / common.EvalAdapter('1*x', construct.BitsInteger(16)),  # 1*x
    'OHKTRT' / common.EvalAdapter('1*x', construct.BitsInteger(16)),  # 1*x
    'OSMTRT' / common.EvalAdapter('1*x', construct.BitsInteger(16)),  # 1*x
    'OTCTRT' / common.EvalAdapter('1*x', construct.BitsInteger(16)),  # 1*x
    'OTDTRT' / common.EvalAdapter('1*x', construct.BitsInteger(16)),  # 1*x
    'OCATRT' / common.EvalAdapter('1*x', construct.BitsInteger(16)),  # 1*x
    'OMMTRT' / common.EvalAdapter('1*x', construct.BitsInteger(16)),  # 1*x
    'OPDTRT' / common.EvalAdapter('1*x', construct.BitsInteger(16)),  # 1*x
    'OSITRT' / common.EvalAdapter('1*x', construct.BitsInteger(16)),  # 1*x
    'OSBTRT' / common.EvalAdapter('1*x', construct.BitsInteger(16)),  # 1*x
    'OTRTHW' / enum_36,  # 0=OBDH 1, 1=OBDH 2, 2=OBDH 3, 3=OBDH 4
    'OTRTAV' / enum_25,  # 1=AVAILABLE, 0=NOT AVAILABLE
    '_pad0' / construct.BitsInteger(5),
)

obdh_timestamps = construct.BitStruct(
    '_name' / construct.Computed('obdh_timestamps'),
    'name' / construct.Computed('OBDH TIMESTAMPS'),
    'OAUTCS' / enum_104,  # 0=RODOS, 1=RTC
    'OAUTCT' / common.UNIXTimestampAdapter(construct.BitsInteger(47)),
    'OARUPT' / construct.BitsInteger(48),
    'OATMHW' / enum_36,  # 0=OBDH 1, 1=OBDH 2, 2=OBDH 3, 3=OBDH 4
    'OATEMP' / common.EvalAdapter('-40*x**0 +  1.904761904761905*x**1', construct.BitsInteger(6)),  # -40*x^0 +  1.904761904761905*x^1
)

obdh_can_listener_sts = construct.BitStruct(
    '_name' / construct.Computed('obdh_can_listener_sts'),
    'name' / construct.Computed('OBDH CAN LISTENER STS'),
    'OCLF11' / construct.BitsInteger(11),
    'OCLF12' / construct.BitsInteger(11),
    'OCLF13' / construct.BitsInteger(11),
    'OCLF14' / construct.BitsInteger(11),
    'OCLAVA' / enum_25,  # 1=AVAILABLE, 0=NOT AVAILABLE
    'OCLFB1' / enum_105,  # 0=ID MASK, 1=ID LIST
    'OCLFB2' / enum_105,  # 0=ID MASK, 1=ID LIST
    'OCLBFI' / enum_69,  # 1=INITIALIZED, 0=NOT INIT
    'OCLBFL' / construct.BitsInteger(16),
    'OCLF21' / construct.BitsInteger(11),
    'OCLF22' / construct.BitsInteger(11),
    'OCLF23' / construct.BitsInteger(11),
    'OCLF24' / construct.BitsInteger(11),
    'OCLB1A' / enum_43,  # 1=ARMED, 0=DISARMED
    'OCLB2A' / enum_43,  # 1=ARMED, 0=DISARMED
    'OCLHWI' / enum_36,  # 0=OBDH 1, 1=OBDH 2, 2=OBDH 3, 3=OBDH 4
    'OCLBFF' / enum_106,  # 0=NOT FINAL, 1=FINALIZED
    'OCLECO' / enum_107,  # 1=BUF PUSH FAIL, 2=BUF INIT FAIL, 3=BUF FULL, 4=BUF ERASE FAIL, 0=NO ERROR, 5=BUF FINALIZE FAIL
    'OCLECN' / construct.BitsInteger(4),
)

obdh_cfg_rest = construct.BitStruct(
    '_name' / construct.Computed('obdh_cfg_rest'),
    'name' / construct.Computed('OBDH CFG REST'),
    'OOOPEN' / enum_46,  # 0=DISABLED, 1=ENABLED
    'OOOSEN' / enum_46,  # 0=DISABLED, 1=ENABLED
    'OCPUSE' / enum_0,  # 1=ON, 0=OFF
    'OOTRAV' / construct.BitsInteger(1),
    'ORTCCP' / enum_108,  # 0=CALIB 32s, 1=CALIB 16s, 2=CALIB 8s
    'ORTCCV' / common.EvalAdapter('-512*x**0 +  1*x**1', construct.BitsInteger(10)),  # -512*x^0 +  1*x^1
    'OTTORP' / common.EvalAdapter('-2147483648*x**0 +  1*x**1', construct.BitsInteger(32)),  # -2147483648*x^0 +  1*x^1
    'ORMPRI' / construct.BitsInteger(8),
    'ORMMTO' / construct.BitsInteger(8),
    'ORMRTP' / construct.BitsInteger(8),
    'ORMRTS' / construct.BitsInteger(8),
    'ORMRTT' / construct.BitsInteger(8),
    'ORMCSP' / enum_109,  # 0=UART, 1=CAN1, 2=CAN2
    'ORMCSS' / enum_109,  # 0=UART, 1=CAN1, 2=CAN2
    'ORMCST' / enum_109,  # 0=UART, 1=CAN1, 2=CAN2
    'OOTRHW' / enum_36,  # 0=OBDH 1, 1=OBDH 2, 2=OBDH 3, 3=OBDH 4
    'ORSTTO' / construct.BitsInteger(8),
    'OTMDTO' / construct.BitsInteger(8),
    'OBEMOI' / construct.BitsInteger(8),
    'OGLOCI' / construct.BitsInteger(8),
    'OTDTGL' / construct.BitsInteger(16),
    'OCFGCI' / construct.BitsInteger(8),
    'OTCLCI' / construct.BitsInteger(8),
    'OTIMED' / common.EvalAdapter('-100*x**0 +  0.0030518*x**1', construct.BitsInteger(16)),  # -100*x^0 +  0.0030518*x^1
    'OTGPSU' / enum_46,  # 0=DISABLED, 1=ENABLED
    'OTRTCE' / enum_46,  # 1=ENABLED, 0=DISABLED
    'OORES1' / construct.BitsInteger(4),
    'OTSCID' / construct.BitsInteger(10),
    'OTIMEA' / construct.BitsInteger(32),
    'OCAN1E' / enum_46,  # 1=ENABLED, 0=DISABLED
    'OCAN2E' / enum_46,  # 1=ENABLED, 0=DISABLED
    'OSYN1E' / enum_46,  # 1=ENABLED, 0=DISABLED
    'OSYN2E' / enum_46,  # 1=ENABLED, 0=DISABLED
    'OSYN3E' / enum_46,  # 1=ENABLED, 0=DISABLED
    'OSYN4E' / enum_46,  # 1=ENABLED, 0=DISABLED
    'ORAM1E' / enum_46,  # 1=ENABLED, 0=DISABLED
    'ORAM2E' / enum_46,  # 1=ENABLED, 0=DISABLED
    'OPNF1E' / enum_46,  # 1=ENABLED, 0=DISABLED
    'OPNF2E' / enum_46,  # 1=ENABLED, 0=DISABLED
    'OSNFEN' / enum_46,  # 1=ENABLED, 0=DISABLED
    'OSYNTE' / enum_46,  # 1=ENABLED, 0=DISABLED
    'OTIMEE' / enum_46,  # 0=DISABLED, 1=ENABLED
    'OTDPRR' / enum_110,  # 0=VHF 1, 1=VHF 2, 2=UHF 1, 3=UHF 2
    'OSWDGW' / construct.BitsInteger(8),
    'OSWDGD' / construct.BitsInteger(8),
    'OVHF1E' / construct.BitsInteger(8),
    'OVHF2E' / construct.BitsInteger(8),
    'OUHF1E' / construct.BitsInteger(8),
    'OUHF2E' / construct.BitsInteger(8),
    'OVHF1R' / construct.BitsInteger(8),
    'OVHF2R' / construct.BitsInteger(8),
    'OUHF1R' / construct.BitsInteger(8),
    'OUHF2R' / construct.BitsInteger(8),
    'OVHF1L' / construct.BitsInteger(8),
    'OVHF2L' / construct.BitsInteger(8),
    'OUHF1L' / construct.BitsInteger(8),
    'OUHF2L' / construct.BitsInteger(8),
    'OCANLA' / construct.BitsInteger(32),
    'OCANLC' / construct.BitsInteger(8),
    'OSWDGR' / construct.BitsInteger(8),
    'OVHFVT' / construct.BitsInteger(16),
    'OUHFVT' / construct.BitsInteger(16),
    'OTCRFD' / construct.BitsInteger(8),
    'OUMACF' / enum_85,  # 0=6, 1=12, 2=24, 3=48, 4=72, 5=96, 6=120, 7=144, 8=168, 9=8, 10=16, 11=32, 12=64
    'OUMPCF' / enum_85,  # 0=6, 1=12, 2=24, 3=48, 4=72, 5=96, 6=120, 7=144, 8=168, 9=8, 10=16, 11=32, 12=64
    '_pad0' / construct.BitsInteger(8),
    'OEMBUA' / construct.BitsInteger(32),
    'OEMBUS' / construct.BitsInteger(8),
    'OEMBUE' / enum_46,  # 0=DISABLED, 1=ENABLED
    'OTCFIT' / construct.BitsInteger(16),
    'OSBORP' / common.EvalAdapter('-2147483648*x**0 +  1*x**1', construct.BitsInteger(32)),  # -2147483648*x^0 +  1*x^1
    'OGPORP' / common.EvalAdapter('-2147483648*x**0 +  1*x**1', construct.BitsInteger(32)),  # -2147483648*x^0 +  1*x^1
    'OTUTCP' / construct.BitsInteger(8),
    'ORTCRI' / construct.BitsInteger(8),
    'OTCFMT' / construct.BitsInteger(16),
    'OTDTGT' / construct.BitsInteger(16),
    'OINICI' / construct.BitsInteger(8),
)

obdh_cfg_hk_buf = construct.BitStruct(
    '_name' / construct.Computed('obdh_cfg_hk_buf'),
    'name' / construct.Computed('OBDH CFG HK BUF'),
    'OSTDHF' / enum_46,  # 0=DISABLED, 1=ENABLED
    'OSTDHC' / construct.BitsInteger(7),
    'OEPERF' / enum_46,  # 0=DISABLED, 1=ENABLED
    'OEPERC' / construct.BitsInteger(7),
    'OADCSF' / enum_46,  # 0=DISABLED, 1=ENABLED
    'OADCSC' / construct.BitsInteger(7),
    'OACT1F' / enum_46,  # 0=DISABLED, 1=ENABLED
    'OACT1C' / construct.BitsInteger(7),
    'OACT2F' / enum_46,  # 0=DISABLED, 1=ENABLED
    'OACT2C' / construct.BitsInteger(7),
    'OSUN1F' / enum_46,  # 0=DISABLED, 1=ENABLED
    'OSUN1C' / construct.BitsInteger(7),
    'OSUN2F' / enum_46,  # 0=DISABLED, 1=ENABLED
    'OSUN2C' / construct.BitsInteger(7),
    'OTHERF' / enum_46,  # 0=DISABLED, 1=ENABLED
    'OTHERC' / construct.BitsInteger(7),
    'OSWINF' / enum_46,  # 0=DISABLED, 1=ENABLED
    'OSWINC' / construct.BitsInteger(7),
    'OPWRSF' / enum_46,  # 0=DISABLED, 1=ENABLED
    'OPWRSC' / construct.BitsInteger(7),
    'OADCEF' / enum_46,  # 0=DISABLED, 1=ENABLED
    'OADCEC' / construct.BitsInteger(7),
    'OPLDTF' / enum_46,  # 0=DISABLED, 1=ENABLED
    'OPLDTC' / construct.BitsInteger(7),
    'OEXPDF' / enum_46,  # 0=DISABLED, 1=ENABLED
    'OEXPDC' / construct.BitsInteger(7),
    'OSBNDF' / enum_46,  # 0=DISABLED, 1=ENABLED
    'OSBNDC' / construct.BitsInteger(7),
    'OMOPSF' / enum_46,  # 0=DISABLED, 1=ENABLED
    'OMOPSC' / construct.BitsInteger(7),
    'OAISTF' / enum_46,  # 0=DISABLED, 1=ENABLED
    'OAISTC' / construct.BitsInteger(7),
    'OAI01F' / enum_46,  # 0=DISABLED, 1=ENABLED
    'OAI01C' / construct.BitsInteger(7),
    'OAI02F' / enum_46,  # 0=DISABLED, 1=ENABLED
    'OAI02C' / construct.BitsInteger(7),
    'OAI03F' / enum_46,  # 0=DISABLED, 1=ENABLED
    'OAI03C' / construct.BitsInteger(7),
    'OAI04F' / enum_46,  # 0=DISABLED, 1=ENABLED
    'OAI04C' / construct.BitsInteger(7),
    'OAI05F' / enum_46,  # 0=DISABLED, 1=ENABLED
    'OAI05C' / construct.BitsInteger(7),
    'OAI06F' / enum_46,  # 0=DISABLED, 1=ENABLED
    'OAI06C' / construct.BitsInteger(7),
    'OAI07F' / enum_46,  # 0=DISABLED, 1=ENABLED
    'OAI07C' / construct.BitsInteger(7),
    'OAI08F' / enum_46,  # 0=DISABLED, 1=ENABLED
    'OAI08C' / construct.BitsInteger(7),
    'OAI09F' / enum_46,  # 0=DISABLED, 1=ENABLED
    'OAI09C' / construct.BitsInteger(7),
    'OAI10F' / enum_46,  # 0=DISABLED, 1=ENABLED
    'OAI10C' / construct.BitsInteger(7),
    'OMVWSF' / enum_46,  # 0=DISABLED, 1=ENABLED
    'OMVWSC' / construct.BitsInteger(7),
    'OTHRUF' / enum_46,  # 0=DISABLED, 1=ENABLED
    'OTHRUC' / construct.BitsInteger(7),
    'OLEOPF' / enum_46,  # 0=DISABLED, 1=ENABLED
    'OLEOPC' / construct.BitsInteger(7),
    'OECDEF' / enum_46,  # 0=DISABLED, 1=ENABLED
    'OECDEC' / construct.BitsInteger(7),
    'OMEMSF' / enum_46,  # 0=DISABLED, 1=ENABLED
    'OMEMSC' / construct.BitsInteger(7),
    'OSWUPF' / enum_46,  # 0=DISABLED, 1=ENABLED
    'OSWUPC' / construct.BitsInteger(7),
    'OSTRCF' / enum_46,  # 0=DISABLED, 1=ENABLED
    'OSTRCC' / construct.BitsInteger(7),
    'OGPSSF' / enum_46,  # 0=DISABLED, 1=ENABLED
    'OGPSSC' / construct.BitsInteger(7),
    'ORSTCF' / enum_46,  # 0=DISABLED, 1=ENABLED
    'ORSTCC' / construct.BitsInteger(7),
    'OMVWEF' / enum_46,  # 0=DISABLED, 1=ENABLED
    'OMVWEC' / construct.BitsInteger(7),
    'ORES2F' / enum_46,  # 1=ENABLED, 0=DISABLED
    'ORES2C' / construct.BitsInteger(7),
    'ORES1F' / enum_46,  # 1=ENABLED, 0=DISABLED
    'ORES1C' / construct.BitsInteger(7),
    'OSTDHP' / enum_46,  # 0=DISABLED, 1=ENABLED
    'OSTDHI' / construct.BitsInteger(7),
    'OEPERP' / enum_46,  # 0=DISABLED, 1=ENABLED
    'OEPERI' / construct.BitsInteger(7),
    'OADCSP' / enum_46,  # 0=DISABLED, 1=ENABLED
    'OADCSI' / construct.BitsInteger(7),
    'OACT1P' / enum_46,  # 0=DISABLED, 1=ENABLED
    'OACT1I' / construct.BitsInteger(7),
    'OACT2P' / enum_46,  # 0=DISABLED, 1=ENABLED
    'OACT2I' / construct.BitsInteger(7),
    'OSUN1P' / enum_46,  # 0=DISABLED, 1=ENABLED
    'OSUN1I' / construct.BitsInteger(7),
    'OSUN2P' / enum_46,  # 0=DISABLED, 1=ENABLED
    'OSUN2I' / construct.BitsInteger(7),
    'OTHERP' / enum_46,  # 0=DISABLED, 1=ENABLED
    'OTHERI' / construct.BitsInteger(7),
    'OSWINP' / enum_46,  # 0=DISABLED, 1=ENABLED
    'OSWINI' / construct.BitsInteger(7),
    'OPWRSP' / enum_46,  # 0=DISABLED, 1=ENABLED
    'OPWRSI' / construct.BitsInteger(7),
    'OADCEP' / enum_46,  # 0=DISABLED, 1=ENABLED
    'OADCEI' / construct.BitsInteger(7),
    'OPLDTP' / enum_46,  # 0=DISABLED, 1=ENABLED
    'OPLDTI' / construct.BitsInteger(7),
    'OEXPDP' / enum_46,  # 0=DISABLED, 1=ENABLED
    'OEXPDI' / construct.BitsInteger(7),
    'OSBNDP' / enum_46,  # 0=DISABLED, 1=ENABLED
    'OSBNDI' / construct.BitsInteger(7),
    'OMOPSP' / enum_46,  # 0=DISABLED, 1=ENABLED
    'OMOPSI' / construct.BitsInteger(7),
    'OAISTP' / enum_46,  # 0=DISABLED, 1=ENABLED
    'OAISTI' / construct.BitsInteger(7),
    'OAI01P' / enum_46,  # 0=DISABLED, 1=ENABLED
    'OAI01I' / construct.BitsInteger(7),
    'OAI02P' / enum_46,  # 0=DISABLED, 1=ENABLED
    'OAI02I' / construct.BitsInteger(7),
    'OAI03P' / enum_46,  # 0=DISABLED, 1=ENABLED
    'OAI03I' / construct.BitsInteger(7),
    'OAI04P' / enum_46,  # 0=DISABLED, 1=ENABLED
    'OAI04I' / construct.BitsInteger(7),
    'OAI05P' / enum_46,  # 0=DISABLED, 1=ENABLED
    'OAI05I' / construct.BitsInteger(7),
    'OAI06P' / enum_46,  # 0=DISABLED, 1=ENABLED
    'OAI06I' / construct.BitsInteger(7),
    'OAI07P' / enum_46,  # 0=DISABLED, 1=ENABLED
    'OAI07I' / construct.BitsInteger(7),
    'OAI08P' / enum_46,  # 0=DISABLED, 1=ENABLED
    'OAI08I' / construct.BitsInteger(7),
    'OAI09P' / enum_46,  # 0=DISABLED, 1=ENABLED
    'OAI09I' / construct.BitsInteger(7),
    'OAI10P' / enum_46,  # 0=DISABLED, 1=ENABLED
    'OAI10I' / construct.BitsInteger(7),
    'OMVWSP' / enum_46,  # 0=DISABLED, 1=ENABLED
    'OMVWSI' / construct.BitsInteger(7),
    'OTHRUP' / enum_46,  # 0=DISABLED, 1=ENABLED
    'OTHRUI' / construct.BitsInteger(7),
    'OLEOPP' / enum_46,  # 0=DISABLED, 1=ENABLED
    'OLEOPI' / construct.BitsInteger(7),
    'OECDEP' / enum_46,  # 0=DISABLED, 1=ENABLED
    'OECDEI' / construct.BitsInteger(7),
    'OMEMSP' / enum_46,  # 0=DISABLED, 1=ENABLED
    'OMEMSI' / construct.BitsInteger(7),
    'OSWUPP' / enum_46,  # 0=DISABLED, 1=ENABLED
    'OSWUPI' / construct.BitsInteger(7),
    'OSTRCP' / enum_46,  # 0=DISABLED, 1=ENABLED
    'OSTRCI' / construct.BitsInteger(7),
    'OGPSSP' / enum_46,  # 0=DISABLED, 1=ENABLED
    'OGPSSI' / construct.BitsInteger(7),
    'ORSTCP' / enum_46,  # 0=DISABLED, 1=ENABLED
    'ORSTCI' / construct.BitsInteger(7),
    'OMVWEP' / enum_46,  # 0=DISABLED, 1=ENABLED
    'OMVWEI' / construct.BitsInteger(7),
    'ORES2P' / enum_46,  # 1=ENABLED, 0=DISABLED
    'ORES2I' / construct.BitsInteger(7),
    'ORES1P' / enum_46,  # 1=ENABLED, 0=DISABLED
    'ORES1I' / construct.BitsInteger(7),
    'OSTDHA' / construct.BitsInteger(32),
    'OEPERA' / construct.BitsInteger(32),
    'OADCSA' / construct.BitsInteger(32),
    'OACT1A' / construct.BitsInteger(32),
    'OACT2A' / construct.BitsInteger(32),
    'OSUN1A' / construct.BitsInteger(32),
    'OSUN2A' / construct.BitsInteger(32),
    'OTHERA' / construct.BitsInteger(32),
    'OSWINA' / construct.BitsInteger(32),
    'OPWRSA' / construct.BitsInteger(32),
    'OADCEA' / construct.BitsInteger(32),
    'OPLDTA' / construct.BitsInteger(32),
    'OEXPDA' / construct.BitsInteger(32),
    'OSBNDA' / construct.BitsInteger(32),
    'OMOPSA' / construct.BitsInteger(32),
    'OAISTA' / construct.BitsInteger(32),
    'OAI01A' / construct.BitsInteger(32),
    'OAI02A' / construct.BitsInteger(32),
    'OAI03A' / construct.BitsInteger(32),
    'OAI04A' / construct.BitsInteger(32),
    'OAI05A' / construct.BitsInteger(32),
    'OAI06A' / construct.BitsInteger(32),
    'OAI07A' / construct.BitsInteger(32),
    'OAI08A' / construct.BitsInteger(32),
    'OAI09A' / construct.BitsInteger(32),
    'OAI10A' / construct.BitsInteger(32),
    'OMVWSA' / construct.BitsInteger(32),
    'OTHRUA' / construct.BitsInteger(32),
    'OLEOPA' / construct.BitsInteger(32),
    'OECDEA' / construct.BitsInteger(32),
    'OMEMSA' / construct.BitsInteger(32),
    'OSWUPA' / construct.BitsInteger(32),
    'OSTRCA' / construct.BitsInteger(32),
    'OGPSSA' / construct.BitsInteger(32),
    'ORSTCA' / construct.BitsInteger(32),
    'OMVWEA' / construct.BitsInteger(32),
    'ORES2A' / construct.BitsInteger(32),
    'ORES1A' / construct.BitsInteger(32),
    'OSTDHR' / enum_46,  # 1=ENABLED, 0=DISABLED
    'OEPERR' / enum_46,  # 1=ENABLED, 0=DISABLED
    'OADCSR' / enum_46,  # 1=ENABLED, 0=DISABLED
    'OACT1R' / enum_46,  # 1=ENABLED, 0=DISABLED
    'OACT2R' / enum_46,  # 1=ENABLED, 0=DISABLED
    'OSUN1R' / enum_46,  # 1=ENABLED, 0=DISABLED
    'OSUN2R' / enum_46,  # 1=ENABLED, 0=DISABLED
    'OTHERR' / enum_46,  # 1=ENABLED, 0=DISABLED
    'OSWINR' / enum_46,  # 1=ENABLED, 0=DISABLED
    'OPWRSR' / enum_46,  # 1=ENABLED, 0=DISABLED
    'OADCER' / enum_46,  # 1=ENABLED, 0=DISABLED
    'OPLDTR' / enum_46,  # 1=ENABLED, 0=DISABLED
    'OEXPDR' / enum_46,  # 1=ENABLED, 0=DISABLED
    'OSBNDR' / enum_46,  # 1=ENABLED, 0=DISABLED
    'OMOPSR' / enum_46,  # 1=ENABLED, 0=DISABLED
    'OAISTR' / enum_46,  # 1=ENABLED, 0=DISABLED
    'OAI01R' / enum_46,  # 1=ENABLED, 0=DISABLED
    'OAI02R' / enum_46,  # 1=ENABLED, 0=DISABLED
    'OAI03R' / enum_46,  # 1=ENABLED, 0=DISABLED
    'OAI04R' / enum_46,  # 1=ENABLED, 0=DISABLED
    'OAI05R' / enum_46,  # 1=ENABLED, 0=DISABLED
    'OAI06R' / enum_46,  # 1=ENABLED, 0=DISABLED
    'OAI07R' / enum_46,  # 1=ENABLED, 0=DISABLED
    'OAI08R' / enum_46,  # 1=ENABLED, 0=DISABLED
    'OAI09R' / enum_46,  # 1=ENABLED, 0=DISABLED
    'OAI10R' / enum_46,  # 1=ENABLED, 0=DISABLED
    'OMVWSR' / enum_46,  # 1=ENABLED, 0=DISABLED
    'OTHRUR' / enum_46,  # 1=ENABLED, 0=DISABLED
    'OLEOPR' / enum_46,  # 1=ENABLED, 0=DISABLED
    'OECDER' / enum_46,  # 1=ENABLED, 0=DISABLED
    'OMEMSR' / enum_46,  # 1=ENABLED, 0=DISABLED
    'OSWUPR' / enum_46,  # 1=ENABLED, 0=DISABLED
    'OSTRCR' / enum_46,  # 1=ENABLED, 0=DISABLED
    'OGPSSR' / enum_46,  # 0=DISABLED, 1=ENABLED
    'ORSTCR' / enum_46,  # 0=DISABLED, 1=ENABLED
    'OMVWER' / enum_46,  # 0=DISABLED, 1=ENABLED
    'ORES2R' / enum_46,  # 1=ENABLED, 0=DISABLED
    'ORES1R' / enum_46,  # 1=ENABLED, 0=DISABLED
    'OCHKHW' / enum_36,  # 0=OBDH 1, 1=OBDH 2, 2=OBDH 3, 3=OBDH 4
    'OCHKAV' / enum_25,  # 0=NOT AVAILABLE, 1=AVAILABLE
    '_pad0' / construct.BitsInteger(7),
)

obdh_cfg_tc_lst = construct.BitStruct(
    '_name' / construct.Computed('obdh_cfg_tc_lst'),
    'name' / construct.Computed('OBDH CFG TC LST'),
    'OLPL1A' / construct.BitsInteger(32),
    'OLPL2A' / construct.BitsInteger(32),
    'OLPL3A' / construct.BitsInteger(32),
    'OASL1A' / construct.BitsInteger(32),
    'OASL2A' / construct.BitsInteger(32),
    'OASL3A' / construct.BitsInteger(32),
    'OPASLA' / construct.BitsInteger(32),
    'OPATTA' / construct.BitsInteger(32),
    'OACTTA' / construct.BitsInteger(32),
    'OPATTC' / construct.BitsInteger(8),
    '_pad0' / construct.BitsInteger(8),
    'OACTTC' / construct.BitsInteger(8),
    'OTCLHW' / enum_36,  # 0=OBDH 1, 1=OBDH 2, 2=OBDH 3, 3=OBDH 4
    'OTCLAV' / enum_25,  # 0=NOT AVAILABLE, 1=AVAILABLE
    'OTCRES' / construct.BitsInteger(5),
    'ORP01A' / construct.BitsInteger(32),
    'ORP02A' / construct.BitsInteger(32),
    'ORP03A' / construct.BitsInteger(32),
    'ORP04A' / construct.BitsInteger(32),
    'ORP05A' / construct.BitsInteger(32),
    'ORP06A' / construct.BitsInteger(32),
    'ORP07A' / construct.BitsInteger(32),
    'ORP08A' / construct.BitsInteger(32),
    'ORP09A' / construct.BitsInteger(32),
    'ORP10A' / construct.BitsInteger(32),
    'ORP11A' / construct.BitsInteger(32),
    'ORP12A' / construct.BitsInteger(32),
    'ORP13A' / construct.BitsInteger(32),
    'ORP14A' / construct.BitsInteger(32),
    'ORP15A' / construct.BitsInteger(32),
    'ORP16A' / construct.BitsInteger(32),
    'OSWUPS' / construct.BitsInteger(32),
)

obdh_cfg_addr = construct.BitStruct(
    '_name' / construct.Computed('obdh_cfg_addr'),
    'name' / construct.Computed('OBDH CFG ADDR'),
    'O1CFA1' / construct.BitsInteger(32),
    'O1CFA2' / construct.BitsInteger(32),
    'O1CFA3' / construct.BitsInteger(32),
    'O2CFA1' / construct.BitsInteger(32),
    'O2CFA2' / construct.BitsInteger(32),
    'O2CFA3' / construct.BitsInteger(32),
    'O3CFA1' / construct.BitsInteger(32),
    'O3CFA2' / construct.BitsInteger(32),
    'O3CFA3' / construct.BitsInteger(32),
    'O4CFA1' / construct.BitsInteger(32),
    'O4CFA2' / construct.BitsInteger(32),
    'O4CFA3' / construct.BitsInteger(32),
)

obdh_cfg_sm_lim = construct.BitStruct(
    '_name' / construct.Computed('obdh_cfg_sm_lim'),
    'name' / construct.Computed('OBDH CFG SM LIM'),
    'LB05H1' / construct.BitsInteger(8),
    'LI05H1' / construct.BitsInteger(8),
    'LU05H1' / construct.BitsInteger(8),
    'LV05H1' / construct.BitsInteger(8),
    'LB05H2' / construct.BitsInteger(8),
    'LI05H2' / construct.BitsInteger(8),
    'LU05H2' / construct.BitsInteger(8),
    'LV05H2' / construct.BitsInteger(8),
    'LB12H1' / construct.BitsInteger(8),
    'LI12H1' / construct.BitsInteger(8),
    'LV12H2' / construct.BitsInteger(8),
    'LI12H2' / construct.BitsInteger(8),
    'NB05H1' / construct.BitsInteger(8),
    'NI05H1' / construct.BitsInteger(8),
    'NU05H1' / construct.BitsInteger(8),
    'NV05H1' / construct.BitsInteger(8),
    'NB05H2' / construct.BitsInteger(8),
    'NI05H2' / construct.BitsInteger(8),
    'NU05H2' / construct.BitsInteger(8),
    'NV05H2' / construct.BitsInteger(8),
    'NB12H1' / construct.BitsInteger(8),
    'NI12H1' / construct.BitsInteger(8),
    'NV12H2' / construct.BitsInteger(8),
    'NI12H2' / construct.BitsInteger(8),
    'PB05H1' / construct.BitsInteger(8),
    'PI05H1' / construct.BitsInteger(8),
    'PU05H1' / construct.BitsInteger(8),
    'PV05H1' / construct.BitsInteger(8),
    'PB05H2' / construct.BitsInteger(8),
    'PI05H2' / construct.BitsInteger(8),
    'PU05H2' / construct.BitsInteger(8),
    'PV05H2' / construct.BitsInteger(8),
    'PB12H1' / construct.BitsInteger(8),
    'PI12H1' / construct.BitsInteger(8),
    'PV12H2' / construct.BitsInteger(8),
    'PI12H2' / construct.BitsInteger(8),
    'BB05H1' / construct.BitsInteger(8),
    'BI05H1' / construct.BitsInteger(8),
    'BU05H1' / construct.BitsInteger(8),
    'BV05H1' / construct.BitsInteger(8),
    'BB05H2' / construct.BitsInteger(8),
    'BI05H2' / construct.BitsInteger(8),
    'BU05H2' / construct.BitsInteger(8),
    'BV05H2' / construct.BitsInteger(8),
    'BB12H1' / construct.BitsInteger(8),
    'BI12H1' / construct.BitsInteger(8),
    'BV12H2' / construct.BitsInteger(8),
    'BI12H2' / construct.BitsInteger(8),
    'UB05H1' / construct.BitsInteger(8),
    'UI05H1' / construct.BitsInteger(8),
    'UU05H1' / construct.BitsInteger(8),
    'UV05H1' / construct.BitsInteger(8),
    'UB05H2' / construct.BitsInteger(8),
    'UI05H2' / construct.BitsInteger(8),
    'UU05H2' / construct.BitsInteger(8),
    'UV05H2' / construct.BitsInteger(8),
    'UB12H1' / construct.BitsInteger(8),
    'UI12H1' / construct.BitsInteger(8),
    'UV12H2' / construct.BitsInteger(8),
    'UI12H2' / construct.BitsInteger(8),
    'OB05E1' / construct.BitsInteger(8),
    'OI05E1' / construct.BitsInteger(8),
    'OU05E1' / construct.BitsInteger(8),
    'OV05E1' / construct.BitsInteger(8),
    'OB05E2' / construct.BitsInteger(8),
    'OI05E2' / construct.BitsInteger(8),
    'OU05E2' / construct.BitsInteger(8),
    'OV05E2' / construct.BitsInteger(8),
    'OV12E1' / construct.BitsInteger(8),
    'OI12E1' / construct.BitsInteger(8),
    'OV12E2' / construct.BitsInteger(8),
    'OI12E2' / construct.BitsInteger(8),
    'OSMLHW' / enum_36,  # 0=OBDH 1, 1=OBDH 2, 2=OBDH 3, 3=OBDH 4
    'OSMLAV' / enum_25,  # 0=NOT AVAILABLE, 1=AVAILABLE
    'OSMRS1' / construct.BitsInteger(1),
    'OP12F2' / enum_37,  # 1=YES, 0=NO
    'OP12F1' / enum_37,  # 1=YES, 0=NO
    'OP05F2' / enum_37,  # 1=YES, 0=NO
    'OP05F1' / enum_37,  # 1=YES, 0=NO
    'OPUNRL' / construct.BitsInteger(8),
    'OSMRS2' / construct.BitsInteger(4),
    'OI12A2' / enum_37,  # 1=YES, 0=NO
    'OV12A2' / enum_37,  # 1=YES, 0=NO
    'OI12A1' / enum_37,  # 1=YES, 0=NO
    'OV12A1' / enum_37,  # 1=YES, 0=NO
    'OV05A2' / enum_37,  # 1=YES, 0=NO
    'OU05A2' / enum_37,  # 1=YES, 0=NO
    'OI05A2' / enum_37,  # 1=YES, 0=NO
    'OB05A2' / enum_37,  # 1=YES, 0=NO
    'OV05A1' / enum_37,  # 1=YES, 0=NO
    'OU05A1' / enum_37,  # 1=YES, 0=NO
    'OI05A1' / enum_37,  # 1=YES, 0=NO
    'OB05A1' / enum_37,  # 1=YES, 0=NO
    'OSMCIV' / construct.BitsInteger(8),
    'OSMLAF' / common.EvalAdapter('0.003921568627451*x', construct.BitsInteger(8)),  # 0.003921568627451*x
    'LB05L1' / construct.BitsInteger(8),
    'LI05L1' / construct.BitsInteger(8),
    'LU05L1' / construct.BitsInteger(8),
    'LV05L1' / construct.BitsInteger(8),
    'LB05L2' / construct.BitsInteger(8),
    'LI05L2' / construct.BitsInteger(8),
    'LU05L2' / construct.BitsInteger(8),
    'LV05L2' / construct.BitsInteger(8),
    'LB12L1' / construct.BitsInteger(8),
    'LI12L1' / construct.BitsInteger(8),
    'LV12L2' / construct.BitsInteger(8),
    'LI12L2' / construct.BitsInteger(8),
    'NB05L1' / construct.BitsInteger(8),
    'NI05L1' / construct.BitsInteger(8),
    'NU05L1' / construct.BitsInteger(8),
    'NV05L1' / construct.BitsInteger(8),
    'NB05L2' / construct.BitsInteger(8),
    'NI05L2' / construct.BitsInteger(8),
    'NU05L2' / construct.BitsInteger(8),
    'NV05L2' / construct.BitsInteger(8),
    'NB12L1' / construct.BitsInteger(8),
    'NI12L1' / construct.BitsInteger(8),
    'NV12L2' / construct.BitsInteger(8),
    'NI12L2' / construct.BitsInteger(8),
    'PB05L1' / construct.BitsInteger(8),
    'PI05L1' / construct.BitsInteger(8),
    'PU05L1' / construct.BitsInteger(8),
    'PV05L1' / construct.BitsInteger(8),
    'PB05L2' / construct.BitsInteger(8),
    'PI05L2' / construct.BitsInteger(8),
    'PU05L2' / construct.BitsInteger(8),
    'PV05L2' / construct.BitsInteger(8),
    'PB12L1' / construct.BitsInteger(8),
    'PI12L1' / construct.BitsInteger(8),
    'PV12L2' / construct.BitsInteger(8),
    'PI12L2' / construct.BitsInteger(8),
    'BB05L1' / construct.BitsInteger(8),
    'BI05L1' / construct.BitsInteger(8),
    'BU05L1' / construct.BitsInteger(8),
    'BV05L1' / construct.BitsInteger(8),
    'BB05L2' / construct.BitsInteger(8),
    'BI05L2' / construct.BitsInteger(8),
    'BU05L2' / construct.BitsInteger(8),
    'BV05L2' / construct.BitsInteger(8),
    'BB12L1' / construct.BitsInteger(8),
    'BI12L1' / construct.BitsInteger(8),
    'BV12L2' / construct.BitsInteger(8),
    'BI12L2' / construct.BitsInteger(8),
    'UB05L1' / construct.BitsInteger(8),
    'UI05L1' / construct.BitsInteger(8),
    'UU05L1' / construct.BitsInteger(8),
    'UV05L1' / construct.BitsInteger(8),
    'UB05L2' / construct.BitsInteger(8),
    'UI05L2' / construct.BitsInteger(8),
    'UU05L2' / construct.BitsInteger(8),
    'UV05L2' / construct.BitsInteger(8),
    'UB12L1' / construct.BitsInteger(8),
    'UI12L1' / construct.BitsInteger(8),
    'UV12L2' / construct.BitsInteger(8),
    'UI12L2' / construct.BitsInteger(8),
)

obdh_cfg_pdh = construct.BitStruct(
    '_name' / construct.Computed('obdh_cfg_pdh'),
    'name' / construct.Computed('OBDH CFG PDH'),
    'OCANMR' / construct.BitsInteger(8),
    'OSPIMR' / construct.BitsInteger(8),
    'OSPIPS' / construct.BitsInteger(16),
    'OSPISA' / construct.BitsInteger(32),
    'OSPIFQ' / common.EvalAdapter('100*x', construct.BitsInteger(8)),  # 100*x
    'OPDCAV' / enum_25,  # 0=NOT AVAILABLE, 1=AVAILABLE
    'OPRES1' / construct.BitsInteger(5),
    'OPDHHW' / enum_36,  # 0=OBDH 1, 1=OBDH 2, 2=OBDH 3, 3=OBDH 4
    'OSSTVA' / construct.BitsInteger(32),
    'OEXB0C' / construct.BitsInteger(8),
    'OEXB1C' / construct.BitsInteger(8),
    'OEXB2C' / construct.BitsInteger(8),
    'OEXB3C' / construct.BitsInteger(8),
    'OEXB4C' / construct.BitsInteger(8),
    'OEXB5C' / construct.BitsInteger(8),
    'OEXB6C' / construct.BitsInteger(8),
    'OEXB7C' / construct.BitsInteger(8),
    'OEXB0A' / construct.BitsInteger(32),
    'OEXB1A' / construct.BitsInteger(32),
    'OEXB2A' / construct.BitsInteger(32),
    'OEXB3A' / construct.BitsInteger(32),
    'OEXB4A' / construct.BitsInteger(32),
    'OEXB5A' / construct.BitsInteger(32),
    'OEXB6A' / construct.BitsInteger(32),
    'OEXB7A' / construct.BitsInteger(32),
)

adcs_std = construct.BitStruct(
    '_name' / construct.Computed('adcs_std'),
    'name' / construct.Computed('ADCS STD'),
    'ADCACT' / enum_111,  # 0=ADCS 1, 1=ADCS 2
    'ADCMOD' / enum_112,  # 1=IDLE, 2=DETERMINATION, 3=DETUMBLING, 4=SUN POINTING, 5=EARTH POINTING, 6=TARGET POINTING, 0=OFF
    'ADCOCO' / construct.BitsInteger(4),
    'ADCECO' / enum_113,  # 0=NONE, 1=UNKNOWN, 2=NO UTC UPDATE, 3=TIME SYNC FAILED, 22=CAN TX FIFO FULL, 24=DATA FRAME TOO LARGE, 25=FLASH ERASE FAILED, 26=FLASH WRITING FAILED, 27=EXP CHANGE WHILE RUN, 28=PAGE 2 FULL, 32=ADXRS X INIT FAIL, 33=ADXRS Y INIT FAIL, 34=ADXRS Z INIT FAIL, 35=CRM X INIT FAIL, 36=CRM Y INIT FAIL, 37=CRM Z INIT FAIL, 38=RM INIT FAIL, 39=HMC INIT FAIL, 56=ADXRS X FAIL, 57=ADXRS Y FAIL, 58=ADXRS Z FAIL, 59=CRM X FAIL, 60=CRM Y FAIL, 61=CRM Z FAIL, 62=RM FAIL, 63=HMC FAIL, 77=INVALID SS CMD, 81=NO SS DATA, 83=SUN SENSOR TIMEOUT, 84=ADXRS COMPLETE FAIL, 85=CRM COMPLETE FAIL, 86=GYRO INCONSISTENT, 87=GYRO NO DATA, 88=MAG INCONSISTENT, 89=MAG NO DATA, 90=NOT ENOUGH DATA, 111=RW X1 FAULT, 112=RW Y1 FAULT, 113=RW Z1 FAULT, 114=RW X2 FAULT, 115=RW Y2 FAULT, 116=RW Z2 FAULT, 120=SGP4 FAULT, 121=SGP4 EPOCH IN FUTURE, 129=CRC MISMATCH, 130=NO VALID SETTINGS, 131=ERASE FAILED, 132=SAVING FAILED, 133=INVALID SLOT NUMBER, 144=CRM FAIL, 145=CRM PREV CMD FAIL, 146=CRM CBIT ENABLED, 147=CRM FACTORY FAIL, 148=CRM CRC FAIL, 149=S
    'ADCECN' / construct.BitsInteger(6),
    'ADFALG' / enum_114,  # 0=NONE, 1=GYRO INTEGRATION, 2=TRIAD, 3=QUEST
    'ADFIMV' / enum_115,  # 3=RM & HMC, 2=RM, 1=HMC, 0=NONE
    'ADCREF' / enum_116,  # 0=ECI, 1=LVLH
    'ADCSR2' / construct.BitsInteger(1),
    'ADFIST' / enum_117,  # 0=NONE, 1=YES
    'ADFISS' / enum_118,  # 0=NONE, 1=X+, 2=X-, 3=Y+, 4=Y-, 5=Z+, 6=Z-
    'ADFROL' / common.EvalAdapter('-180*x**0 +  0.005493247882811*x**1', construct.BitsInteger(16)),  # -180*x^0 +  0.005493247882811*x^1
    'ADFPIT' / common.EvalAdapter('-180*x**0 +  0.005493247882811*x**1', construct.BitsInteger(16)),  # -180*x^0 +  0.005493247882811*x^1
    'ADFYAW' / common.EvalAdapter('-180*x**0 +  0.005493247882811*x**1', construct.BitsInteger(16)),  # -180*x^0 +  0.005493247882811*x^1
    'MVIROL' / common.EvalAdapter('-180*x**0 +  0.005493247882811*x**1', construct.BitsInteger(16)),  # -180*x^0 +  0.005493247882811*x^1
    'MVIPIT' / common.EvalAdapter('-180*x**0 +  0.005493247882811*x**1', construct.BitsInteger(16)),  # -180*x^0 +  0.005493247882811*x^1
    'MVIYAW' / common.EvalAdapter('-180*x**0 +  0.005493247882811*x**1', construct.BitsInteger(16)),  # -180*x^0 +  0.005493247882811*x^1
    'MMX1BF' / common.EvalAdapter('-800*x**0 +  0.024414435034714*x**1', construct.BitsInteger(16)),  # -800*x^0 +  0.024414435034714*x^1
    'MMY1BF' / common.EvalAdapter('-800*x**0 +  0.024414435034714*x**1', construct.BitsInteger(16)),  # -800*x^0 +  0.024414435034714*x^1
    'MMZ1BF' / common.EvalAdapter('-800*x**0 +  0.024414435034714*x**1', construct.BitsInteger(16)),  # -800*x^0 +  0.024414435034714*x^1
    'GYRROX' / common.EvalAdapter('-300*x**0 +  0.009155413138017853*x**1', construct.BitsInteger(16)),  # -300*x^0 +  0.009155413138017853*x^1
    'GYRROY' / common.EvalAdapter('-300*x**0 +  0.009155413138017853*x**1', construct.BitsInteger(16)),  # -300*x^0 +  0.009155413138017853*x^1
    'GYRROZ' / common.EvalAdapter('-300*x**0 +  0.009155413138017853*x**1', construct.BitsInteger(16)),  # -300*x^0 +  0.009155413138017853*x^1
    'SSXMEA' / common.EvalAdapter('-1*x**0 +  0.000030518043793392844*x**1', construct.BitsInteger(16)),  # -1*x^0 +  0.000030518043793392844*x^1
    'SSYMEA' / common.EvalAdapter('-1*x**0 +  0.000030518043793392844*x**1', construct.BitsInteger(16)),  # -1*x^0 +  0.000030518043793392844*x^1
    'SSZMEA' / common.EvalAdapter('-1*x**0 +  0.000030518043793392844*x**1', construct.BitsInteger(16)),  # -1*x^0 +  0.000030518043793392844*x^1
    'PREALT' / common.EvalAdapter('-6378*x**0 +  1*x**1', construct.BitsInteger(16)),  # -6378*x^0 +  1*x^1
    'PRELAT' / common.EvalAdapter('-180*x**0 +  0.005493247882811*x**1', construct.BitsInteger(16)),  # -180*x^0 +  0.005493247882811*x^1
    'PRELON' / common.EvalAdapter('-180*x**0 +  0.005493247882811*x**1', construct.BitsInteger(16)),  # -180*x^0 +  0.005493247882811*x^1
    'TTORQX' / common.EvalAdapter('-10*x**0 +  0.00030518043793392844*x**1', construct.BitsInteger(16)),  # -10*x^0 +  0.00030518043793392844*x^1
    'TTORQY' / common.EvalAdapter('-10*x**0 +  0.00030518043793392844*x**1', construct.BitsInteger(16)),  # -10*x^0 +  0.00030518043793392844*x^1
    'TTORQZ' / common.EvalAdapter('-10*x**0 +  0.00030518043793392844*x**1', construct.BitsInteger(16)),  # -10*x^0 +  0.00030518043793392844*x^1
    'SUNVIS' / enum_119,  # 1=DAY, 0=NIGHT
    'ADCATV' / enum_90,  # 1=VALID, 0=INVALID
    'ADCGUX' / enum_120,  # 3=ADXRS & CRM, 1=CRM, 2=ADXRS, 0=NONE
    'ADCGUY' / enum_120,  # 3=ADXRS & CRM, 1=CRM, 2=ADXRS, 0=NONE
    'ADCGUZ' / enum_120,  # 3=ADXRS & CRM, 1=CRM, 2=ADXRS, 0=NONE
)

adcs_ext = construct.BitStruct(
    '_name' / construct.Computed('adcs_ext'),
    'name' / construct.Computed('ADCS EXT'),
    'ADCUTC' / common.UNIXTimestampAdapter(construct.BitsInteger(48)),
    'ADLOOP' / common.EvalAdapter('0.0001525902189669642*x', construct.BitsInteger(16)),  # 0.0001525902189669642*x
    'ERRBU0' / enum_113,  # 0=NONE, 1=UNKNOWN, 2=NO UTC UPDATE, 3=TIME SYNC FAILED, 22=CAN TX FIFO FULL, 24=DATA FRAME TOO LARGE, 25=FLASH ERASE FAILED, 26=FLASH WRITING FAILED, 27=EXP CHANGE WHILE RUN, 28=PAGE 2 FULL, 32=ADXRS X INIT FAIL, 33=ADXRS Y INIT FAIL, 34=ADXRS Z INIT FAIL, 35=CRM X INIT FAIL, 36=CRM Y INIT FAIL, 37=CRM Z INIT FAIL, 38=RM INIT FAIL, 39=HMC INIT FAIL, 56=ADXRS X FAIL, 57=ADXRS Y FAIL, 58=ADXRS Z FAIL, 59=CRM X FAIL, 60=CRM Y FAIL, 61=CRM Z FAIL, 62=RM FAIL, 63=HMC FAIL, 77=INVALID SS CMD, 81=NO SS DATA, 83=SUN SENSOR TIMEOUT, 84=ADXRS COMPLETE FAIL, 85=CRM COMPLETE FAIL, 86=GYRO INCONSISTENT, 87=GYRO NO DATA, 88=MAG INCONSISTENT, 89=MAG NO DATA, 90=NOT ENOUGH DATA, 111=RW X1 FAULT, 112=RW Y1 FAULT, 113=RW Z1 FAULT, 114=RW X2 FAULT, 115=RW Y2 FAULT, 116=RW Z2 FAULT, 120=SGP4 FAULT, 121=SGP4 EPOCH IN FUTURE, 129=CRC MISMATCH, 130=NO VALID SETTINGS, 131=ERASE FAILED, 132=SAVING FAILED, 133=INVALID SLOT NUMBER, 144=CRM FAIL, 145=CRM PREV CMD FAIL, 146=CRM CBIT ENABLED, 147=CRM FACTORY FAIL, 148=CRM CRC FAIL, 149=S
    'ERRBU1' / enum_113,  # 0=NONE, 1=UNKNOWN, 2=NO UTC UPDATE, 3=TIME SYNC FAILED, 22=CAN TX FIFO FULL, 24=DATA FRAME TOO LARGE, 25=FLASH ERASE FAILED, 26=FLASH WRITING FAILED, 27=EXP CHANGE WHILE RUN, 28=PAGE 2 FULL, 32=ADXRS X INIT FAIL, 33=ADXRS Y INIT FAIL, 34=ADXRS Z INIT FAIL, 35=CRM X INIT FAIL, 36=CRM Y INIT FAIL, 37=CRM Z INIT FAIL, 38=RM INIT FAIL, 39=HMC INIT FAIL, 56=ADXRS X FAIL, 57=ADXRS Y FAIL, 58=ADXRS Z FAIL, 59=CRM X FAIL, 60=CRM Y FAIL, 61=CRM Z FAIL, 62=RM FAIL, 63=HMC FAIL, 77=INVALID SS CMD, 81=NO SS DATA, 83=SUN SENSOR TIMEOUT, 84=ADXRS COMPLETE FAIL, 85=CRM COMPLETE FAIL, 86=GYRO INCONSISTENT, 87=GYRO NO DATA, 88=MAG INCONSISTENT, 89=MAG NO DATA, 90=NOT ENOUGH DATA, 111=RW X1 FAULT, 112=RW Y1 FAULT, 113=RW Z1 FAULT, 114=RW X2 FAULT, 115=RW Y2 FAULT, 116=RW Z2 FAULT, 120=SGP4 FAULT, 121=SGP4 EPOCH IN FUTURE, 129=CRC MISMATCH, 130=NO VALID SETTINGS, 131=ERASE FAILED, 132=SAVING FAILED, 133=INVALID SLOT NUMBER, 144=CRM FAIL, 145=CRM PREV CMD FAIL, 146=CRM CBIT ENABLED, 147=CRM FACTORY FAIL, 148=CRM CRC FAIL, 149=S
    'ERRBU2' / enum_113,  # 0=NONE, 1=UNKNOWN, 2=NO UTC UPDATE, 3=TIME SYNC FAILED, 22=CAN TX FIFO FULL, 24=DATA FRAME TOO LARGE, 25=FLASH ERASE FAILED, 26=FLASH WRITING FAILED, 27=EXP CHANGE WHILE RUN, 28=PAGE 2 FULL, 32=ADXRS X INIT FAIL, 33=ADXRS Y INIT FAIL, 34=ADXRS Z INIT FAIL, 35=CRM X INIT FAIL, 36=CRM Y INIT FAIL, 37=CRM Z INIT FAIL, 38=RM INIT FAIL, 39=HMC INIT FAIL, 56=ADXRS X FAIL, 57=ADXRS Y FAIL, 58=ADXRS Z FAIL, 59=CRM X FAIL, 60=CRM Y FAIL, 61=CRM Z FAIL, 62=RM FAIL, 63=HMC FAIL, 77=INVALID SS CMD, 81=NO SS DATA, 83=SUN SENSOR TIMEOUT, 84=ADXRS COMPLETE FAIL, 85=CRM COMPLETE FAIL, 86=GYRO INCONSISTENT, 87=GYRO NO DATA, 88=MAG INCONSISTENT, 89=MAG NO DATA, 90=NOT ENOUGH DATA, 111=RW X1 FAULT, 112=RW Y1 FAULT, 113=RW Z1 FAULT, 114=RW X2 FAULT, 115=RW Y2 FAULT, 116=RW Z2 FAULT, 120=SGP4 FAULT, 121=SGP4 EPOCH IN FUTURE, 129=CRC MISMATCH, 130=NO VALID SETTINGS, 131=ERASE FAILED, 132=SAVING FAILED, 133=INVALID SLOT NUMBER, 144=CRM FAIL, 145=CRM PREV CMD FAIL, 146=CRM CBIT ENABLED, 147=CRM FACTORY FAIL, 148=CRM CRC FAIL, 149=S
    'ERRBU3' / enum_113,  # 0=NONE, 1=UNKNOWN, 2=NO UTC UPDATE, 3=TIME SYNC FAILED, 22=CAN TX FIFO FULL, 24=DATA FRAME TOO LARGE, 25=FLASH ERASE FAILED, 26=FLASH WRITING FAILED, 27=EXP CHANGE WHILE RUN, 28=PAGE 2 FULL, 32=ADXRS X INIT FAIL, 33=ADXRS Y INIT FAIL, 34=ADXRS Z INIT FAIL, 35=CRM X INIT FAIL, 36=CRM Y INIT FAIL, 37=CRM Z INIT FAIL, 38=RM INIT FAIL, 39=HMC INIT FAIL, 56=ADXRS X FAIL, 57=ADXRS Y FAIL, 58=ADXRS Z FAIL, 59=CRM X FAIL, 60=CRM Y FAIL, 61=CRM Z FAIL, 62=RM FAIL, 63=HMC FAIL, 77=INVALID SS CMD, 81=NO SS DATA, 83=SUN SENSOR TIMEOUT, 84=ADXRS COMPLETE FAIL, 85=CRM COMPLETE FAIL, 86=GYRO INCONSISTENT, 87=GYRO NO DATA, 88=MAG INCONSISTENT, 89=MAG NO DATA, 90=NOT ENOUGH DATA, 111=RW X1 FAULT, 112=RW Y1 FAULT, 113=RW Z1 FAULT, 114=RW X2 FAULT, 115=RW Y2 FAULT, 116=RW Z2 FAULT, 120=SGP4 FAULT, 121=SGP4 EPOCH IN FUTURE, 129=CRC MISMATCH, 130=NO VALID SETTINGS, 131=ERASE FAILED, 132=SAVING FAILED, 133=INVALID SLOT NUMBER, 144=CRM FAIL, 145=CRM PREV CMD FAIL, 146=CRM CBIT ENABLED, 147=CRM FACTORY FAIL, 148=CRM CRC FAIL, 149=S
    'ERRBU4' / enum_113,  # 0=NONE, 1=UNKNOWN, 2=NO UTC UPDATE, 3=TIME SYNC FAILED, 22=CAN TX FIFO FULL, 24=DATA FRAME TOO LARGE, 25=FLASH ERASE FAILED, 26=FLASH WRITING FAILED, 27=EXP CHANGE WHILE RUN, 28=PAGE 2 FULL, 32=ADXRS X INIT FAIL, 33=ADXRS Y INIT FAIL, 34=ADXRS Z INIT FAIL, 35=CRM X INIT FAIL, 36=CRM Y INIT FAIL, 37=CRM Z INIT FAIL, 38=RM INIT FAIL, 39=HMC INIT FAIL, 56=ADXRS X FAIL, 57=ADXRS Y FAIL, 58=ADXRS Z FAIL, 59=CRM X FAIL, 60=CRM Y FAIL, 61=CRM Z FAIL, 62=RM FAIL, 63=HMC FAIL, 77=INVALID SS CMD, 81=NO SS DATA, 83=SUN SENSOR TIMEOUT, 84=ADXRS COMPLETE FAIL, 85=CRM COMPLETE FAIL, 86=GYRO INCONSISTENT, 87=GYRO NO DATA, 88=MAG INCONSISTENT, 89=MAG NO DATA, 90=NOT ENOUGH DATA, 111=RW X1 FAULT, 112=RW Y1 FAULT, 113=RW Z1 FAULT, 114=RW X2 FAULT, 115=RW Y2 FAULT, 116=RW Z2 FAULT, 120=SGP4 FAULT, 121=SGP4 EPOCH IN FUTURE, 129=CRC MISMATCH, 130=NO VALID SETTINGS, 131=ERASE FAILED, 132=SAVING FAILED, 133=INVALID SLOT NUMBER, 144=CRM FAIL, 145=CRM PREV CMD FAIL, 146=CRM CBIT ENABLED, 147=CRM FACTORY FAIL, 148=CRM CRC FAIL, 149=S
    'ERRBU5' / enum_113,  # 0=NONE, 1=UNKNOWN, 2=NO UTC UPDATE, 3=TIME SYNC FAILED, 22=CAN TX FIFO FULL, 24=DATA FRAME TOO LARGE, 25=FLASH ERASE FAILED, 26=FLASH WRITING FAILED, 27=EXP CHANGE WHILE RUN, 28=PAGE 2 FULL, 32=ADXRS X INIT FAIL, 33=ADXRS Y INIT FAIL, 34=ADXRS Z INIT FAIL, 35=CRM X INIT FAIL, 36=CRM Y INIT FAIL, 37=CRM Z INIT FAIL, 38=RM INIT FAIL, 39=HMC INIT FAIL, 56=ADXRS X FAIL, 57=ADXRS Y FAIL, 58=ADXRS Z FAIL, 59=CRM X FAIL, 60=CRM Y FAIL, 61=CRM Z FAIL, 62=RM FAIL, 63=HMC FAIL, 77=INVALID SS CMD, 81=NO SS DATA, 83=SUN SENSOR TIMEOUT, 84=ADXRS COMPLETE FAIL, 85=CRM COMPLETE FAIL, 86=GYRO INCONSISTENT, 87=GYRO NO DATA, 88=MAG INCONSISTENT, 89=MAG NO DATA, 90=NOT ENOUGH DATA, 111=RW X1 FAULT, 112=RW Y1 FAULT, 113=RW Z1 FAULT, 114=RW X2 FAULT, 115=RW Y2 FAULT, 116=RW Z2 FAULT, 120=SGP4 FAULT, 121=SGP4 EPOCH IN FUTURE, 129=CRC MISMATCH, 130=NO VALID SETTINGS, 131=ERASE FAILED, 132=SAVING FAILED, 133=INVALID SLOT NUMBER, 144=CRM FAIL, 145=CRM PREV CMD FAIL, 146=CRM CBIT ENABLED, 147=CRM FACTORY FAIL, 148=CRM CRC FAIL, 149=S
    'ERRBU6' / enum_113,  # 0=NONE, 1=UNKNOWN, 2=NO UTC UPDATE, 3=TIME SYNC FAILED, 22=CAN TX FIFO FULL, 24=DATA FRAME TOO LARGE, 25=FLASH ERASE FAILED, 26=FLASH WRITING FAILED, 27=EXP CHANGE WHILE RUN, 28=PAGE 2 FULL, 32=ADXRS X INIT FAIL, 33=ADXRS Y INIT FAIL, 34=ADXRS Z INIT FAIL, 35=CRM X INIT FAIL, 36=CRM Y INIT FAIL, 37=CRM Z INIT FAIL, 38=RM INIT FAIL, 39=HMC INIT FAIL, 56=ADXRS X FAIL, 57=ADXRS Y FAIL, 58=ADXRS Z FAIL, 59=CRM X FAIL, 60=CRM Y FAIL, 61=CRM Z FAIL, 62=RM FAIL, 63=HMC FAIL, 77=INVALID SS CMD, 81=NO SS DATA, 83=SUN SENSOR TIMEOUT, 84=ADXRS COMPLETE FAIL, 85=CRM COMPLETE FAIL, 86=GYRO INCONSISTENT, 87=GYRO NO DATA, 88=MAG INCONSISTENT, 89=MAG NO DATA, 90=NOT ENOUGH DATA, 111=RW X1 FAULT, 112=RW Y1 FAULT, 113=RW Z1 FAULT, 114=RW X2 FAULT, 115=RW Y2 FAULT, 116=RW Z2 FAULT, 120=SGP4 FAULT, 121=SGP4 EPOCH IN FUTURE, 129=CRC MISMATCH, 130=NO VALID SETTINGS, 131=ERASE FAILED, 132=SAVING FAILED, 133=INVALID SLOT NUMBER, 144=CRM FAIL, 145=CRM PREV CMD FAIL, 146=CRM CBIT ENABLED, 147=CRM FACTORY FAIL, 148=CRM CRC FAIL, 149=S
    'ERRBU7' / enum_113,  # 0=NONE, 1=UNKNOWN, 2=NO UTC UPDATE, 3=TIME SYNC FAILED, 22=CAN TX FIFO FULL, 24=DATA FRAME TOO LARGE, 25=FLASH ERASE FAILED, 26=FLASH WRITING FAILED, 27=EXP CHANGE WHILE RUN, 28=PAGE 2 FULL, 32=ADXRS X INIT FAIL, 33=ADXRS Y INIT FAIL, 34=ADXRS Z INIT FAIL, 35=CRM X INIT FAIL, 36=CRM Y INIT FAIL, 37=CRM Z INIT FAIL, 38=RM INIT FAIL, 39=HMC INIT FAIL, 56=ADXRS X FAIL, 57=ADXRS Y FAIL, 58=ADXRS Z FAIL, 59=CRM X FAIL, 60=CRM Y FAIL, 61=CRM Z FAIL, 62=RM FAIL, 63=HMC FAIL, 77=INVALID SS CMD, 81=NO SS DATA, 83=SUN SENSOR TIMEOUT, 84=ADXRS COMPLETE FAIL, 85=CRM COMPLETE FAIL, 86=GYRO INCONSISTENT, 87=GYRO NO DATA, 88=MAG INCONSISTENT, 89=MAG NO DATA, 90=NOT ENOUGH DATA, 111=RW X1 FAULT, 112=RW Y1 FAULT, 113=RW Z1 FAULT, 114=RW X2 FAULT, 115=RW Y2 FAULT, 116=RW Z2 FAULT, 120=SGP4 FAULT, 121=SGP4 EPOCH IN FUTURE, 129=CRC MISMATCH, 130=NO VALID SETTINGS, 131=ERASE FAILED, 132=SAVING FAILED, 133=INVALID SLOT NUMBER, 144=CRM FAIL, 145=CRM PREV CMD FAIL, 146=CRM CBIT ENABLED, 147=CRM FACTORY FAIL, 148=CRM CRC FAIL, 149=S
    'ADCUPT' / common.TimeDeltaAdapter(construct.BitsInteger(16)),
    'ADSECO' / construct.BitsInteger(8),
    'ADCPDR' / common.EvalAdapter('256*x', construct.BitsInteger(8)),  # 256*x
    'ADGMST' / common.EvalAdapter('0.0054931640625*x', construct.BitsInteger(16)),  # 0.0054931640625*x
    'ADCPDS' / common.EvalAdapter('8*x', construct.BitsInteger(16)),  # 8*x
    'PREDMX' / common.EvalAdapter('-800*x**0 +  0.024414435034714*x**1', construct.BitsInteger(16)),  # -800*x^0 +  0.024414435034714*x^1
    'PREDMY' / common.EvalAdapter('-800*x**0 +  0.024414435034714*x**1', construct.BitsInteger(16)),  # -800*x^0 +  0.024414435034714*x^1
    'PREDMZ' / common.EvalAdapter('-800*x**0 +  0.024414435034714*x**1', construct.BitsInteger(16)),  # -800*x^0 +  0.024414435034714*x^1
    'PREDSX' / common.EvalAdapter('0.000030518043793392844*x**1 +  -1*x**0', construct.BitsInteger(16)),  # 0.000030518043793392844*x^1 +  -1*x^0
    'PREDSY' / common.EvalAdapter('-1*x**0 +  0.000030518043793392844*x**1', construct.BitsInteger(16)),  # -1*x^0 +  0.000030518043793392844*x^1
    'PREDSZ' / common.EvalAdapter('-1*x**0 +  0.000030518043793392844*x**1', construct.BitsInteger(16)),  # -1*x^0 +  0.000030518043793392844*x^1
    'SS1XPV' / enum_23,  # 0=FALSE, 1=TRUE
    'SS1XNV' / enum_23,  # 0=FALSE, 1=TRUE
    'SS1YPV' / enum_23,  # 0=FALSE, 1=TRUE
    'SS1YNV' / enum_23,  # 0=FALSE, 1=TRUE
    'SS1ZPV' / enum_23,  # 0=FALSE, 1=TRUE
    'SS1ZNV' / enum_23,  # 0=FALSE, 1=TRUE
    'SS2XPV' / enum_23,  # 0=FALSE, 1=TRUE
    'SS2XNV' / enum_23,  # 0=FALSE, 1=TRUE
    'SS2YPV' / enum_23,  # 0=FALSE, 1=TRUE
    'SS2YNV' / enum_23,  # 0=FALSE, 1=TRUE
    'SS2ZPV' / enum_23,  # 0=FALSE, 1=TRUE
    'SS2ZNV' / enum_23,  # 0=FALSE, 1=TRUE
    'TOACX1' / enum_23,  # 0=FALSE, 1=TRUE
    'TOACY1' / enum_23,  # 0=FALSE, 1=TRUE
    'TOACZ1' / enum_23,  # 0=FALSE, 1=TRUE
    'TOACX2' / enum_23,  # 0=FALSE, 1=TRUE
    'TOACY2' / enum_23,  # 0=FALSE, 1=TRUE
    'TOACZ2' / enum_23,  # 0=FALSE, 1=TRUE
    'RWACX1' / enum_23,  # 0=FALSE, 1=TRUE
    'RWACY1' / enum_23,  # 0=FALSE, 1=TRUE
    'RWACZ1' / enum_23,  # 0=FALSE, 1=TRUE
    'RWACX2' / enum_23,  # 0=FALSE, 1=TRUE
    'RWACY2' / enum_23,  # 0=FALSE, 1=TRUE
    'RWACZ2' / enum_23,  # 0=FALSE, 1=TRUE
    'ADCREC' / enum_23,  # 0=FALSE, 1=TRUE
    'ADCDLI' / enum_23,  # 0=FALSE, 1=TRUE
    'ADCTRA' / enum_23,  # 0=FALSE, 1=TRUE
    'EXPE00' / enum_23,  # 0=FALSE, 1=TRUE
    'EXPE01' / enum_23,  # 0=FALSE, 1=TRUE
    'EXPE02' / enum_23,  # 0=FALSE, 1=TRUE
    'EXPE03' / enum_23,  # 0=FALSE, 1=TRUE
    'EXPE04' / enum_23,  # 0=FALSE, 1=TRUE
    'EXPE05' / enum_23,  # 0=FALSE, 1=TRUE
    'EXPE06' / enum_23,  # 0=FALSE, 1=TRUE
    'EXPE07' / enum_23,  # 0=FALSE, 1=TRUE
    'EXPE08' / enum_23,  # 0=FALSE, 1=TRUE
    'EXPE09' / enum_23,  # 0=FALSE, 1=TRUE
    'EXPE10' / enum_23,  # 0=FALSE, 1=TRUE
    'EXPE11' / enum_23,  # 0=FALSE, 1=TRUE
    'EXPE12' / enum_23,  # 0=FALSE, 1=TRUE
    'EXPE13' / enum_23,  # 0=FALSE, 1=TRUE
    'EXPE14' / enum_23,  # 0=FALSE, 1=TRUE
    'EXPE15' / enum_23,  # 0=FALSE, 1=TRUE
    'EXPE16' / enum_23,  # 0=FALSE, 1=TRUE
    'EXPE17' / enum_23,  # 0=FALSE, 1=TRUE
    'EXPE18' / enum_23,  # 0=FALSE, 1=TRUE
    'EXPE19' / enum_23,  # 0=FALSE, 1=TRUE
    'EXPE20' / enum_23,  # 0=FALSE, 1=TRUE
    'ADCADT' / enum_121,  # 0=NONE, 1=SECONDS, 2=MILLISECONDS
    'ADCADC' / enum_122,  # 0=NONE, 1=ENABLED
    'APCANF' / enum_0,  # 0=OFF, 1=ON
    'EPMRO' / common.EvalAdapter('-180*x**0 +  5.625*x**1', construct.BitsInteger(6)),  # -180*x^0 +  5.625*x^1
    'EPMPI' / common.EvalAdapter('-180*x**0 +  5.625*x**1', construct.BitsInteger(6)),  # -180*x^0 +  5.625*x^1
    'EPMYA' / common.EvalAdapter('-180*x**0 +  5.625*x**1', construct.BitsInteger(6)),  # -180*x^0 +  5.625*x^1
    'TPMLAT' / common.EvalAdapter('-180*x**0 +  5.625*x**1', construct.BitsInteger(6)),  # -180*x^0 +  5.625*x^1
    'TPMLON' / common.EvalAdapter('-180*x**0 +  5.625*x**1', construct.BitsInteger(6)),  # -180*x^0 +  5.625*x^1
    'TPMRAD' / common.EvalAdapter('156.25*x', construct.BitsInteger(6)),  # 156.25*x
)

adcs_cfg = construct.BitStruct(
    '_name' / construct.Computed('adcs_cfg'),
    'name' / construct.Computed('ADCS CFG'),
    'TLEEPO' / construct.BitsInteger(32),
    'TLEBST' / common.EvalAdapter('0.00001525902189669642*x', construct.BitsInteger(16)),  # 0.00001525902189669642*x
    'TLEECC' / common.EvalAdapter('0.00001525902189669642*x', construct.BitsInteger(16)),  # 0.00001525902189669642*x
    'TLEARG' / common.EvalAdapter('0.005493247882811*x', construct.BitsInteger(16)),  # 0.005493247882811*x
    'TLEINC' / common.EvalAdapter('0.005493247882811*x', construct.BitsInteger(16)),  # 0.005493247882811*x
    'TLEMEA' / common.EvalAdapter('0.005493247882811*x', construct.BitsInteger(16)),  # 0.005493247882811*x
    'TLENOD' / common.EvalAdapter('0.005493247882811*x', construct.BitsInteger(16)),  # 0.005493247882811*x
    'TLEMOT' / common.EvalAdapter('0.00048828125*x', construct.BitsInteger(16)),  # 0.00048828125*x
    'SETREV' / construct.BitsInteger(6),
    'SVREV0' / construct.BitsInteger(6),
    'SVREV1' / construct.BitsInteger(6),
    'SVREV2' / construct.BitsInteger(6),
    'SENRTO' / common.EvalAdapter('15.625*x', construct.BitsInteger(6)),  # 15.625*x
    'IMURDU' / common.EvalAdapter('15.625*x', construct.BitsInteger(6)),  # 15.625*x
    'TSTOFS' / common.EvalAdapter('15.625*x', construct.BitsInteger(6)),  # 15.625*x
    'CRCSL0' / enum_123,  # 0=FAULT, 1=OK
    'CRCSL1' / enum_123,  # 0=FAULT, 1=OK
    'CRCSL2' / enum_123,  # 0=FAULT, 1=OK
    'ADCCAN' / enum_124,  # 0=CAN1, 1=CAN2
    'ADCAVA' / construct.BitsInteger(1),
    'ADCCRS' / construct.BitsInteger(1),
    'HMCOFX' / common.EvalAdapter('-20*x**0 +  0.6349206349206349*x**1', construct.BitsInteger(6)),  # -20*x^0 +  0.6349206349206349*x^1
    'HMCOFY' / common.EvalAdapter('-20*x**0 +  0.6349206349206349*x**1', construct.BitsInteger(6)),  # -20*x^0 +  0.6349206349206349*x^1
    'HMCOFZ' / common.EvalAdapter('-20*x**0 +  0.6349206349206349*x**1', construct.BitsInteger(6)),  # -20*x^0 +  0.6349206349206349*x^1
    'HMCM00' / common.EvalAdapter('-1.25*x**0 +  0.0396825396825397*x**1', construct.BitsInteger(6)),  # -1.25*x^0 +  0.0396825396825397*x^1
    'HMCM01' / common.EvalAdapter('-1.25*x**0 +  0.0396825396825397*x**1', construct.BitsInteger(6)),  # -1.25*x^0 +  0.0396825396825397*x^1
    'HMCM02' / common.EvalAdapter('-1.25*x**0 +  0.0396825396825397*x**1', construct.BitsInteger(6)),  # -1.25*x^0 +  0.0396825396825397*x^1
    'HMCM10' / common.EvalAdapter('-1.25*x**0 +  0.0396825396825397*x**1', construct.BitsInteger(6)),  # -1.25*x^0 +  0.0396825396825397*x^1
    'HMCM11' / common.EvalAdapter('-1.25*x**0 +  0.0396825396825397*x**1', construct.BitsInteger(6)),  # -1.25*x^0 +  0.0396825396825397*x^1
    'HMCM12' / common.EvalAdapter('-1.25*x**0 +  0.0396825396825397*x**1', construct.BitsInteger(6)),  # -1.25*x^0 +  0.0396825396825397*x^1
    'HMCM20' / common.EvalAdapter('-1.25*x**0 +  0.0396825396825397*x**1', construct.BitsInteger(6)),  # -1.25*x^0 +  0.0396825396825397*x^1
    'ADCCR1' / construct.BitsInteger(4),
    'HMCM21' / common.EvalAdapter('-1.25*x**0 +  0.0396825396825397*x**1', construct.BitsInteger(6)),  # -1.25*x^0 +  0.0396825396825397*x^1
    'HMCM22' / common.EvalAdapter('-1.25*x**0 +  0.0396825396825397*x**1', construct.BitsInteger(6)),  # -1.25*x^0 +  0.0396825396825397*x^1
    'RM3OFX' / common.EvalAdapter('-20*x**0 +  0.6349206349206349*x**1', construct.BitsInteger(6)),  # -20*x^0 +  0.6349206349206349*x^1
    'RM3OFY' / common.EvalAdapter('-20*x**0 +  0.6349206349206349*x**1', construct.BitsInteger(6)),  # -20*x^0 +  0.6349206349206349*x^1
    'RM3OFZ' / common.EvalAdapter('-20*x**0 +  0.6349206349206349*x**1', construct.BitsInteger(6)),  # -20*x^0 +  0.6349206349206349*x^1
    'RM3M00' / common.EvalAdapter('-1.25*x**0 +  0.0396825396825397*x**1', construct.BitsInteger(6)),  # -1.25*x^0 +  0.0396825396825397*x^1
    'RM3M01' / common.EvalAdapter('-1.25*x**0 +  0.0396825396825397*x**1', construct.BitsInteger(6)),  # -1.25*x^0 +  0.0396825396825397*x^1
    'RM3M02' / common.EvalAdapter('-1.25*x**0 +  0.0396825396825397*x**1', construct.BitsInteger(6)),  # -1.25*x^0 +  0.0396825396825397*x^1
    'RM3M10' / common.EvalAdapter('-1.25*x**0 +  0.0396825396825397*x**1', construct.BitsInteger(6)),  # -1.25*x^0 +  0.0396825396825397*x^1
    'RM3M11' / common.EvalAdapter('-1.25*x**0 +  0.0396825396825397*x**1', construct.BitsInteger(6)),  # -1.25*x^0 +  0.0396825396825397*x^1
    'RM3M12' / common.EvalAdapter('-1.25*x**0 +  0.0396825396825397*x**1', construct.BitsInteger(6)),  # -1.25*x^0 +  0.0396825396825397*x^1
    'RM3M20' / common.EvalAdapter('-1.25*x**0 +  0.0396825396825397*x**1', construct.BitsInteger(6)),  # -1.25*x^0 +  0.0396825396825397*x^1
    'RM3M21' / common.EvalAdapter('-1.25*x**0 +  0.0396825396825397*x**1', construct.BitsInteger(6)),  # -1.25*x^0 +  0.0396825396825397*x^1
    'RM3M22' / common.EvalAdapter('-1.25*x**0 +  0.0396825396825397*x**1', construct.BitsInteger(6)),  # -1.25*x^0 +  0.0396825396825397*x^1
    'ADXOFX' / common.EvalAdapter('-1.25*x**0 +  0.0396825396825397*x**1', construct.BitsInteger(6)),  # -1.25*x^0 +  0.0396825396825397*x^1
    'ADXOFY' / common.EvalAdapter('-1.25*x**0 +  0.0396825396825397*x**1', construct.BitsInteger(6)),  # -1.25*x^0 +  0.0396825396825397*x^1
    'ADXOFZ' / common.EvalAdapter('-1.25*x**0 +  0.0396825396825397*x**1', construct.BitsInteger(6)),  # -1.25*x^0 +  0.0396825396825397*x^1
    'ADXM00' / common.EvalAdapter('-1.25*x**0 +  0.0396825396825397*x**1', construct.BitsInteger(6)),  # -1.25*x^0 +  0.0396825396825397*x^1
    'ADXM01' / common.EvalAdapter('-1.25*x**0 +  0.0396825396825397*x**1', construct.BitsInteger(6)),  # -1.25*x^0 +  0.0396825396825397*x^1
    'ADXM02' / common.EvalAdapter('-1.25*x**0 +  0.0396825396825397*x**1', construct.BitsInteger(6)),  # -1.25*x^0 +  0.0396825396825397*x^1
    'ADXM10' / common.EvalAdapter('-1.25*x**0 +  0.0396825396825397*x**1', construct.BitsInteger(6)),  # -1.25*x^0 +  0.0396825396825397*x^1
    'ADXM11' / common.EvalAdapter('-1.25*x**0 +  0.0396825396825397*x**1', construct.BitsInteger(6)),  # -1.25*x^0 +  0.0396825396825397*x^1
    'ADXM12' / common.EvalAdapter('-1.25*x**0 +  0.0396825396825397*x**1', construct.BitsInteger(6)),  # -1.25*x^0 +  0.0396825396825397*x^1
    'ADXM20' / common.EvalAdapter('-1.25*x**0 +  0.0396825396825397*x**1', construct.BitsInteger(6)),  # -1.25*x^0 +  0.0396825396825397*x^1
    'ADXM21' / common.EvalAdapter('-1.25*x**0 +  0.0396825396825397*x**1', construct.BitsInteger(6)),  # -1.25*x^0 +  0.0396825396825397*x^1
    'ADXM22' / common.EvalAdapter('-1.25*x**0 +  0.0396825396825397*x**1', construct.BitsInteger(6)),  # -1.25*x^0 +  0.0396825396825397*x^1
    'CRMOFX' / common.EvalAdapter('-1.25*x**0 +  0.0396825396825397*x**1', construct.BitsInteger(6)),  # -1.25*x^0 +  0.0396825396825397*x^1
    'CRMOFY' / common.EvalAdapter('-1.25*x**0 +  0.0396825396825397*x**1', construct.BitsInteger(6)),  # -1.25*x^0 +  0.0396825396825397*x^1
    'CRMOFZ' / common.EvalAdapter('-1.25*x**0 +  0.0396825396825397*x**1', construct.BitsInteger(6)),  # -1.25*x^0 +  0.0396825396825397*x^1
    'CRMM00' / common.EvalAdapter('-1.25*x**0 +  0.0396825396825397*x**1', construct.BitsInteger(6)),  # -1.25*x^0 +  0.0396825396825397*x^1
    'CRMM01' / common.EvalAdapter('-1.25*x**0 +  0.0396825396825397*x**1', construct.BitsInteger(6)),  # -1.25*x^0 +  0.0396825396825397*x^1
    'CRMM02' / common.EvalAdapter('-1.25*x**0 +  0.0396825396825397*x**1', construct.BitsInteger(6)),  # -1.25*x^0 +  0.0396825396825397*x^1
    'CRMM10' / common.EvalAdapter('-1.25*x**0 +  0.0396825396825397*x**1', construct.BitsInteger(6)),  # -1.25*x^0 +  0.0396825396825397*x^1
    'CRMM11' / common.EvalAdapter('-1.25*x**0 +  0.0396825396825397*x**1', construct.BitsInteger(6)),  # -1.25*x^0 +  0.0396825396825397*x^1
    'CRMM12' / common.EvalAdapter('-1.25*x**0 +  0.0396825396825397*x**1', construct.BitsInteger(6)),  # -1.25*x^0 +  0.0396825396825397*x^1
    'CRMM20' / common.EvalAdapter('-1.25*x**0 +  0.0396825396825397*x**1', construct.BitsInteger(6)),  # -1.25*x^0 +  0.0396825396825397*x^1
    'CRMM21' / common.EvalAdapter('-1.25*x**0 +  0.0396825396825397*x**1', construct.BitsInteger(6)),  # -1.25*x^0 +  0.0396825396825397*x^1
    'CRMM22' / common.EvalAdapter('-1.25*x**0 +  0.0396825396825397*x**1', construct.BitsInteger(6)),  # -1.25*x^0 +  0.0396825396825397*x^1
    'SXP1Q0' / common.EvalAdapter('-1*x**0 +  0.0317460317460317*x**1', construct.BitsInteger(6)),  # -1*x^0 +  0.0317460317460317*x^1
    'SXP1Q1' / common.EvalAdapter('-1*x**0 +  0.0317460317460317*x**1', construct.BitsInteger(6)),  # -1*x^0 +  0.0317460317460317*x^1
    'SXP1Q2' / common.EvalAdapter('-1*x**0 +  0.0317460317460317*x**1', construct.BitsInteger(6)),  # -1*x^0 +  0.0317460317460317*x^1
    'SXP1Q3' / common.EvalAdapter('-1*x**0 +  0.0317460317460317*x**1', construct.BitsInteger(6)),  # -1*x^0 +  0.0317460317460317*x^1
    'SXN1Q0' / common.EvalAdapter('-1*x**0 +  0.0317460317460317*x**1', construct.BitsInteger(6)),  # -1*x^0 +  0.0317460317460317*x^1
    'SXN1Q1' / common.EvalAdapter('-1*x**0 +  0.0317460317460317*x**1', construct.BitsInteger(6)),  # -1*x^0 +  0.0317460317460317*x^1
    'SXN1Q2' / common.EvalAdapter('-1*x**0 +  0.0317460317460317*x**1', construct.BitsInteger(6)),  # -1*x^0 +  0.0317460317460317*x^1
    'SXN1Q3' / common.EvalAdapter('-1*x**0 +  0.0317460317460317*x**1', construct.BitsInteger(6)),  # -1*x^0 +  0.0317460317460317*x^1
    'SYP1Q0' / common.EvalAdapter('-1*x**0 +  0.0317460317460317*x**1', construct.BitsInteger(6)),  # -1*x^0 +  0.0317460317460317*x^1
    'SYP1Q1' / common.EvalAdapter('-1*x**0 +  0.0317460317460317*x**1', construct.BitsInteger(6)),  # -1*x^0 +  0.0317460317460317*x^1
    'SYP1Q2' / common.EvalAdapter('-1*x**0 +  0.0317460317460317*x**1', construct.BitsInteger(6)),  # -1*x^0 +  0.0317460317460317*x^1
    'SYP1Q3' / common.EvalAdapter('-1*x**0 +  0.0317460317460317*x**1', construct.BitsInteger(6)),  # -1*x^0 +  0.0317460317460317*x^1
    'SYN1Q0' / common.EvalAdapter('-1*x**0 +  0.0317460317460317*x**1', construct.BitsInteger(6)),  # -1*x^0 +  0.0317460317460317*x^1
    'SYN1Q1' / common.EvalAdapter('-1*x**0 +  0.0317460317460317*x**1', construct.BitsInteger(6)),  # -1*x^0 +  0.0317460317460317*x^1
    'SYN1Q2' / common.EvalAdapter('-1*x**0 +  0.0317460317460317*x**1', construct.BitsInteger(6)),  # -1*x^0 +  0.0317460317460317*x^1
    'SYN1Q3' / common.EvalAdapter('-1*x**0 +  0.0317460317460317*x**1', construct.BitsInteger(6)),  # -1*x^0 +  0.0317460317460317*x^1
    'SZP1Q0' / common.EvalAdapter('-1*x**0 +  0.0317460317460317*x**1', construct.BitsInteger(6)),  # -1*x^0 +  0.0317460317460317*x^1
    'SZP1Q1' / common.EvalAdapter('-1*x**0 +  0.0317460317460317*x**1', construct.BitsInteger(6)),  # -1*x^0 +  0.0317460317460317*x^1
    'SZP1Q2' / common.EvalAdapter('-1*x**0 +  0.0317460317460317*x**1', construct.BitsInteger(6)),  # -1*x^0 +  0.0317460317460317*x^1
    'SZP1Q3' / common.EvalAdapter('-1*x**0 +  0.0317460317460317*x**1', construct.BitsInteger(6)),  # -1*x^0 +  0.0317460317460317*x^1
    'SZN1Q0' / common.EvalAdapter('-1*x**0 +  0.0317460317460317*x**1', construct.BitsInteger(6)),  # -1*x^0 +  0.0317460317460317*x^1
    'SZN1Q1' / common.EvalAdapter('-1*x**0 +  0.0317460317460317*x**1', construct.BitsInteger(6)),  # -1*x^0 +  0.0317460317460317*x^1
    'SZN1Q2' / common.EvalAdapter('-1*x**0 +  0.0317460317460317*x**1', construct.BitsInteger(6)),  # -1*x^0 +  0.0317460317460317*x^1
    'SZN1Q3' / common.EvalAdapter('-1*x**0 +  0.0317460317460317*x**1', construct.BitsInteger(6)),  # -1*x^0 +  0.0317460317460317*x^1
    'SXP2Q0' / common.EvalAdapter('-1*x**0 +  0.0317460317460317*x**1', construct.BitsInteger(6)),  # -1*x^0 +  0.0317460317460317*x^1
    'SXP2Q1' / common.EvalAdapter('-1*x**0 +  0.0317460317460317*x**1', construct.BitsInteger(6)),  # -1*x^0 +  0.0317460317460317*x^1
    'SXP2Q2' / common.EvalAdapter('-1*x**0 +  0.0317460317460317*x**1', construct.BitsInteger(6)),  # -1*x^0 +  0.0317460317460317*x^1
    'SXP2Q3' / common.EvalAdapter('-1*x**0 +  0.0317460317460317*x**1', construct.BitsInteger(6)),  # -1*x^0 +  0.0317460317460317*x^1
    'SXN2Q0' / common.EvalAdapter('-1*x**0 +  0.0317460317460317*x**1', construct.BitsInteger(6)),  # -1*x^0 +  0.0317460317460317*x^1
    'SXN2Q1' / common.EvalAdapter('-1*x**0 +  0.0317460317460317*x**1', construct.BitsInteger(6)),  # -1*x^0 +  0.0317460317460317*x^1
    'SXN2Q2' / common.EvalAdapter('-1*x**0 +  0.0317460317460317*x**1', construct.BitsInteger(6)),  # -1*x^0 +  0.0317460317460317*x^1
    'SXN2Q3' / common.EvalAdapter('-1*x**0 +  0.0317460317460317*x**1', construct.BitsInteger(6)),  # -1*x^0 +  0.0317460317460317*x^1
    'SYP2Q0' / common.EvalAdapter('-1*x**0 +  0.0317460317460317*x**1', construct.BitsInteger(6)),  # -1*x^0 +  0.0317460317460317*x^1
    'SYP2Q1' / common.EvalAdapter('-1*x**0 +  0.0317460317460317*x**1', construct.BitsInteger(6)),  # -1*x^0 +  0.0317460317460317*x^1
    'SYP2Q2' / common.EvalAdapter('-1*x**0 +  0.0317460317460317*x**1', construct.BitsInteger(6)),  # -1*x^0 +  0.0317460317460317*x^1
    'SYP2Q3' / common.EvalAdapter('-1*x**0 +  0.0317460317460317*x**1', construct.BitsInteger(6)),  # -1*x^0 +  0.0317460317460317*x^1
    'SYN2Q0' / common.EvalAdapter('-1*x**0 +  0.0317460317460317*x**1', construct.BitsInteger(6)),  # -1*x^0 +  0.0317460317460317*x^1
    'SYN2Q1' / common.EvalAdapter('-1*x**0 +  0.0317460317460317*x**1', construct.BitsInteger(6)),  # -1*x^0 +  0.0317460317460317*x^1
    'SYN2Q2' / common.EvalAdapter('-1*x**0 +  0.0317460317460317*x**1', construct.BitsInteger(6)),  # -1*x^0 +  0.0317460317460317*x^1
    'SYN2Q3' / common.EvalAdapter('-1*x**0 +  0.0317460317460317*x**1', construct.BitsInteger(6)),  # -1*x^0 +  0.0317460317460317*x^1
    'SZP2Q0' / common.EvalAdapter('-1*x**0 +  0.0317460317460317*x**1', construct.BitsInteger(6)),  # -1*x^0 +  0.0317460317460317*x^1
    'SZP2Q1' / common.EvalAdapter('-1*x**0 +  0.0317460317460317*x**1', construct.BitsInteger(6)),  # -1*x^0 +  0.0317460317460317*x^1
    'SZP2Q2' / common.EvalAdapter('-1*x**0 +  0.0317460317460317*x**1', construct.BitsInteger(6)),  # -1*x^0 +  0.0317460317460317*x^1
    'SZP2Q3' / common.EvalAdapter('-1*x**0 +  0.0317460317460317*x**1', construct.BitsInteger(6)),  # -1*x^0 +  0.0317460317460317*x^1
    'SZN2Q0' / common.EvalAdapter('-1*x**0 +  0.0317460317460317*x**1', construct.BitsInteger(6)),  # -1*x^0 +  0.0317460317460317*x^1
    'SZN2Q1' / common.EvalAdapter('-1*x**0 +  0.0317460317460317*x**1', construct.BitsInteger(6)),  # -1*x^0 +  0.0317460317460317*x^1
    'SZN2Q2' / common.EvalAdapter('-1*x**0 +  0.0317460317460317*x**1', construct.BitsInteger(6)),  # -1*x^0 +  0.0317460317460317*x^1
    'SZN2Q3' / common.EvalAdapter('-1*x**0 +  0.0317460317460317*x**1', construct.BitsInteger(6)),  # -1*x^0 +  0.0317460317460317*x^1
    'MROTQ0' / common.EvalAdapter('-1*x**0 +  0.0317460317460317*x**1', construct.BitsInteger(6)),  # -1*x^0 +  0.0317460317460317*x^1
    'MROTQ1' / common.EvalAdapter('-1*x**0 +  0.0317460317460317*x**1', construct.BitsInteger(6)),  # -1*x^0 +  0.0317460317460317*x^1
    'MROTQ2' / common.EvalAdapter('-1*x**0 +  0.0317460317460317*x**1', construct.BitsInteger(6)),  # -1*x^0 +  0.0317460317460317*x^1
    'MROTQ3' / common.EvalAdapter('-1*x**0 +  0.0317460317460317*x**1', construct.BitsInteger(6)),  # -1*x^0 +  0.0317460317460317*x^1
    'DTBMOD' / enum_125,  # 0=BDOTBANGBANG, 1=RATE DETUMBLING
    'DETPRI' / enum_126,  # 0=TRIAD, 1=QUEST
    'HMCCOR' / enum_0,  # 0=OFF, 1=ON
    'DESATA' / enum_0,  # 0=OFF, 1=ON
    'TMXMX1' / common.EvalAdapter('0.0317460317460317*x', construct.BitsInteger(6)),  # 0.0317460317460317*x
    'TMXMY1' / common.EvalAdapter('0.0317460317460317*x', construct.BitsInteger(6)),  # 0.0317460317460317*x
    'TMXMZ1' / common.EvalAdapter('0.0317460317460317*x', construct.BitsInteger(6)),  # 0.0317460317460317*x
    'TMXMX2' / common.EvalAdapter('0.0317460317460317*x', construct.BitsInteger(6)),  # 0.0317460317460317*x
    'TMXMY2' / common.EvalAdapter('0.0317460317460317*x', construct.BitsInteger(6)),  # 0.0317460317460317*x
    'TMXMZ2' / common.EvalAdapter('0.0317460317460317*x', construct.BitsInteger(6)),  # 0.0317460317460317*x
    'TSETLT' / common.EvalAdapter('1.587301587301587*x', construct.BitsInteger(6)),  # 1.587301587301587*x
    'MAGTLR' / common.EvalAdapter('0.3174603174603175*x', construct.BitsInteger(6)),  # 0.3174603174603175*x
    'GYRTLR' / common.EvalAdapter('0.0317460317460317*x', construct.BitsInteger(6)),  # 0.0317460317460317*x
    'MAGGAI' / common.EvalAdapter('0.0158730158730159*x', construct.BitsInteger(6)),  # 0.0158730158730159*x
    'TDIRX1' / enum_127,  # 0=POS, 1=NEG
    'TDIRY1' / enum_127,  # 0=POS, 1=NEG
    'TDIRZ1' / enum_127,  # 0=POS, 1=NEG
    'PRIMAG' / enum_128,  # 0=HMC5883L, 1=RM3100
    'GYRGAI' / common.EvalAdapter('0.0158730158730159*x', construct.BitsInteger(6)),  # 0.0158730158730159*x
    'TRIALP' / common.EvalAdapter('0.0158730158730159*x', construct.BitsInteger(6)),  # 0.0158730158730159*x
    'QUWMAG' / common.EvalAdapter('0.0158730158730159*x', construct.BitsInteger(6)),  # 0.0158730158730159*x
    'QUWSUN' / common.EvalAdapter('0.0158730158730159*x', construct.BitsInteger(6)),  # 0.0158730158730159*x
    'QUWSTA' / common.EvalAdapter('0.0158730158730159*x', construct.BitsInteger(6)),  # 0.0158730158730159*x
    'MAXRPM' / common.EvalAdapter('158.7301587301587*x', construct.BitsInteger(6)),  # 158.7301587301587*x
    'RWMAXT' / common.EvalAdapter('0.1587301587301587*x', construct.BitsInteger(6)),  # 0.1587301587301587*x
    'SUNPKP' / common.EvalAdapter('0.0317460317460317*x', construct.BitsInteger(6)),  # 0.0317460317460317*x
    'SUNPKI' / common.EvalAdapter('0.0317460317460317*x', construct.BitsInteger(6)),  # 0.0317460317460317*x
    'SUNPKD' / common.EvalAdapter('0.0317460317460317*x', construct.BitsInteger(6)),  # 0.0317460317460317*x
    'TDIRX2' / enum_127,  # 0=POS, 1=NEG
    'TDIRY2' / enum_127,  # 0=POS, 1=NEG
    'TDIRZ2' / enum_127,  # 0=POS, 1=NEG
    'PRIGYR' / enum_129,  # 0=ADXRS453, 1=CRM100/200
    'SVPOSX' / common.EvalAdapter('-1*x**0 +  0.0317460317460317*x**1', construct.BitsInteger(6)),  # -1*x^0 +  0.0317460317460317*x^1
    'SVPOSY' / common.EvalAdapter('-1*x**0 +  0.0317460317460317*x**1', construct.BitsInteger(6)),  # -1*x^0 +  0.0317460317460317*x^1
    'SVPOSZ' / common.EvalAdapter('-1*x**0 +  0.0317460317460317*x**1', construct.BitsInteger(6)),  # -1*x^0 +  0.0317460317460317*x^1
    'SVNEGX' / common.EvalAdapter('-1*x**0 +  0.0317460317460317*x**1', construct.BitsInteger(6)),  # -1*x^0 +  0.0317460317460317*x^1
    'SVNEGY' / common.EvalAdapter('-1*x**0 +  0.0317460317460317*x**1', construct.BitsInteger(6)),  # -1*x^0 +  0.0317460317460317*x^1
    'SVNEGZ' / common.EvalAdapter('-1*x**0 +  0.0317460317460317*x**1', construct.BitsInteger(6)),  # -1*x^0 +  0.0317460317460317*x^1
    'DETUKP' / common.EvalAdapter('31.7460317460317*x', construct.BitsInteger(6)),  # 31.7460317460317*x
    'BDOTTH' / common.EvalAdapter('0.3174603174603175*x', construct.BitsInteger(6)),  # 0.3174603174603175*x
    'MINANG' / common.EvalAdapter('0.46875*x', construct.BitsInteger(6)),  # 0.46875*x
    'INTTMO' / common.EvalAdapter('0.476183*x', construct.BitsInteger(6)),  # 0.476183*x
    'SRODUR' / common.EvalAdapter('0.015625*x', construct.BitsInteger(6)),  # 0.015625*x
    'SROMSA' / construct.BitsInteger(6),
    'SRTSOF' / common.EvalAdapter('0.015625*x', construct.BitsInteger(6)),  # 0.015625*x
    'ACEPMP' / common.EvalAdapter('-1*x**0 +  0.0317460317460317*x**1', construct.BitsInteger(6)),  # -1*x^0 +  0.0317460317460317*x^1
    'ACEPMI' / common.EvalAdapter('-1*x**0 +  0.0317460317460317*x**1', construct.BitsInteger(6)),  # -1*x^0 +  0.0317460317460317*x^1
    'ACEPMD' / common.EvalAdapter('-1*x**0 +  0.0317460317460317*x**1', construct.BitsInteger(6)),  # -1*x^0 +  0.0317460317460317*x^1
    'ACTPMP' / common.EvalAdapter('-1*x**0 +  0.0317460317460317*x**1', construct.BitsInteger(6)),  # -1*x^0 +  0.0317460317460317*x^1
    'ACTPMI' / common.EvalAdapter('-1*x**0 +  0.0317460317460317*x**1', construct.BitsInteger(6)),  # -1*x^0 +  0.0317460317460317*x^1
    'ACTPMD' / common.EvalAdapter('-1*x**0 +  0.0317460317460317*x**1', construct.BitsInteger(6)),  # -1*x^0 +  0.0317460317460317*x^1
    'ACDESP' / common.EvalAdapter('-1*x**0 +  3.17460317460317*x**1', construct.BitsInteger(6)),  # -1*x^0 +  3.17460317460317*x^1
    'ADCTRM' / enum_130,  # 0=NONE, 1=SEPARATE, 2=PARALLEL, 3=MAXIMUM, 4=POLYFIT
    'ACDEST' / common.EvalAdapter('79.36507936507937*x', construct.BitsInteger(6)),  # 79.36507936507937*x
    'ADANLP' / common.EvalAdapter('0.0158730158730159*x', construct.BitsInteger(6)),  # 0.0158730158730159*x
    'ADOFRO' / common.EvalAdapter('1.428571428571429*x**1 +  -45*x**0', construct.BitsInteger(6)),  # 1.428571428571429*x^1 +  -45*x^0
    'ADOFPI' / common.EvalAdapter('1.428571428571429*x**1 +  -45*x**0', construct.BitsInteger(6)),  # 1.428571428571429*x^1 +  -45*x^0
    'ADOFYA' / common.EvalAdapter('1.428571428571429*x**1 +  -45*x**0', construct.BitsInteger(6)),  # 1.428571428571429*x^1 +  -45*x^0
    'HMCREX' / common.EvalAdapter('-125*x**0 +  3.968253968253968*x**1', construct.BitsInteger(6)),  # -125*x^0 +  3.968253968253968*x^1
    'HMCREY' / common.EvalAdapter('-125*x**0 +  3.968253968253968*x**1', construct.BitsInteger(6)),  # -125*x^0 +  3.968253968253968*x^1
    'HMCREZ' / common.EvalAdapter('-125*x**0 +  3.968253968253968*x**1', construct.BitsInteger(6)),  # -125*x^0 +  3.968253968253968*x^1
    'GYRRAN' / common.EvalAdapter('0*x**0 +  4.7619047619*x**1', construct.BitsInteger(6)),  # 0*x^0 +  4.7619047619*x^1
    'MAGRAN' / common.EvalAdapter('0*x**0 +  12.69841256984*x**1', construct.BitsInteger(6)),  # 0*x^0 +  12.69841256984*x^1
    'TORTIM' / common.EvalAdapter('125*x', construct.BitsInteger(6)),  # 125*x
    'ADCCR2' / construct.BitsInteger(2),
)

adcs_akt_bus1_hk = construct.BitStruct(
    '_name' / construct.Computed('adcs_akt_bus1_hk'),
    'name' / construct.Computed('ADCS AKT BUS1 HK'),
    'MTX1CU' / common.EvalAdapter('0.6451612903*x', construct.BitsInteger(10)),  # 0.6451612903*x
    'MTY1CU' / common.EvalAdapter('0.6451612903*x', construct.BitsInteger(10)),  # 0.6451612903*x
    'MTZ1CU' / common.EvalAdapter('0.6451612903*x', construct.BitsInteger(10)),  # 0.6451612903*x
    'IFP1AA' / enum_25,  # 1=AVAILABLE, 0=NOT AVAILABLE
    'MTZRES' / construct.BitsInteger(1),
    'MTX1PW' / common.EvalAdapter('0.097751711*x', construct.BitsInteger(10)),  # 0.097751711*x
    'MTY1PW' / common.EvalAdapter('0.097751711*x', construct.BitsInteger(10)),  # 0.097751711*x
    'MTZ1PW' / common.EvalAdapter('0.097751711*x', construct.BitsInteger(10)),  # 0.097751711*x
    'MTX1FT' / enum_19,  # 0=FAULT, 1=NO FAULT
    'MTX1EN' / enum_46,  # 0=DISABLED, 1=ENABLED
    'MTX1DR' / enum_131,  # 0=NEGATIVE, 1=POSITIVE
    'MTX1SR' / enum_48,  # 0=STBY, 1=ON
    'MTY1FT' / enum_19,  # 0=FAULT, 1=NO FAULT
    'MTY1EN' / enum_46,  # 0=DISABLED, 1=ENABLED
    'MTY1DR' / enum_131,  # 0=NEGATIVE, 1=POSITIVE
    'MTY1SR' / enum_48,  # 0=STBY, 1=ON
    'MTZ1FT' / enum_19,  # 0=FAULT, 1=NO FAULT
    'MTZ1EN' / enum_46,  # 0=DISABLED, 1=ENABLED
    'MTZ1DR' / enum_131,  # 0=NEGATIVE, 1=POSITIVE
    'MTZ1SR' / enum_48,  # 0=STBY, 1=ON
    'RWX1EN' / enum_0,  # 0=OFF, 1=ON
    'RWY1EN' / enum_0,  # 0=OFF, 1=ON
    'RWZ1EN' / enum_0,  # 0=OFF, 1=ON
    'RX1RAT' / common.EvalAdapter('-5080*x**0 +  40*x**1', construct.BitsInteger(8)),  # -5080*x^0 +  40*x^1
    'RX1CUR' / common.EvalAdapter('10*x', construct.BitsInteger(8)),  # 10*x
    'RX1CMC' / construct.BitsInteger(4),
    'RX1ERC' / construct.BitsInteger(4),
    'RX1OPM' / enum_132,  # 0=TORQUE, 1=RATE, 2=IDLE
    'RX1ECN' / enum_133,  # 0=NO_ERROR, 1=ERR_HAL, 5=ERR_CAN_SEND, 6=ERR_CAN_RECV, 2=ERR_TEST_ERROR, 7=ERR_WRONG_PARAMETER, 8=ERR_NO_RW_ID, 9=ERR_NO_SUCH_CMD, 10=ERR_HAL_UART_INIT, 11=ERR_CAN_INIT, 12=ERR_CFG_ERASE, 13=ERR_CFG_WRITE, 14=ERR_TC_BUF_FULL, 15=ERR_TC_ARG, 16=ERR_I2C_READ, 17=ERR_I2C_WRITE, 18=ERR_CFG_CRC, 19=ERR_CFG_SIZE, 20=ERR_NO_CFG_FOUND
    'RX1ACC' / construct.BitsInteger(4),
    'RX1RES' / construct.BitsInteger(2),
    'RX1CTR' / enum_134,  # 0=BLOCK COMMUTATION, 1=SINE COMMUTATION, 2=FIELD ORIENTED, 3=NONE
    'RX1TMP' / common.EvalAdapter('-40*x**0 +  0.74598962*x**1', construct.BitsInteger(8)),  # -40*x^0 +  0.74598962*x^1
    'RX1AVA' / enum_25,  # 1=AVAILABLE, 0=NOT AVAILABLE
    'RY1RAT' / common.EvalAdapter('-5080*x**0 +  40*x**1', construct.BitsInteger(8)),  # -5080*x^0 +  40*x^1
    'RY1CUR' / common.EvalAdapter('10*x', construct.BitsInteger(8)),  # 10*x
    'RY1CMC' / construct.BitsInteger(4),
    'RY1ERC' / construct.BitsInteger(4),
    'RY1OPM' / enum_132,  # 0=TORQUE, 1=RATE, 2=IDLE
    'RY1ECN' / enum_133,  # 0=NO_ERROR, 1=ERR_HAL, 5=ERR_CAN_SEND, 6=ERR_CAN_RECV, 2=ERR_TEST_ERROR, 7=ERR_WRONG_PARAMETER, 8=ERR_NO_RW_ID, 9=ERR_NO_SUCH_CMD, 10=ERR_HAL_UART_INIT, 11=ERR_CAN_INIT, 12=ERR_CFG_ERASE, 13=ERR_CFG_WRITE, 14=ERR_TC_BUF_FULL, 15=ERR_TC_ARG, 16=ERR_I2C_READ, 17=ERR_I2C_WRITE, 18=ERR_CFG_CRC, 19=ERR_CFG_SIZE, 20=ERR_NO_CFG_FOUND
    'RY1ACC' / construct.BitsInteger(4),
    'RY1RES' / construct.BitsInteger(2),
    'RY1CTR' / enum_134,  # 0=BLOCK COMMUTATION, 1=SINE COMMUTATION, 2=FIELD ORIENTED, 3=NONE
    'RY1TMP' / common.EvalAdapter('-40*x**0 +  0.74598962*x**1', construct.BitsInteger(8)),  # -40*x^0 +  0.74598962*x^1
    'RY1AVA' / enum_25,  # 1=AVAILABLE, 0=NOT AVAILABLE
    'RZ1RAT' / common.EvalAdapter('-5080*x**0 +  40*x**1', construct.BitsInteger(8)),  # -5080*x^0 +  40*x^1
    'RZ1CUR' / common.EvalAdapter('10*x', construct.BitsInteger(8)),  # 10*x
    'RZ1CMC' / construct.BitsInteger(4),
    'RZ1ERC' / construct.BitsInteger(4),
    'RZ1OPM' / enum_132,  # 0=TORQUE, 1=RATE, 2=IDLE
    'RZ1ECN' / enum_133,  # 0=NO_ERROR, 1=ERR_HAL, 5=ERR_CAN_SEND, 6=ERR_CAN_RECV, 2=ERR_TEST_ERROR, 7=ERR_WRONG_PARAMETER, 8=ERR_NO_RW_ID, 9=ERR_NO_SUCH_CMD, 10=ERR_HAL_UART_INIT, 11=ERR_CAN_INIT, 12=ERR_CFG_ERASE, 13=ERR_CFG_WRITE, 14=ERR_TC_BUF_FULL, 15=ERR_TC_ARG, 16=ERR_I2C_READ, 17=ERR_I2C_WRITE, 18=ERR_CFG_CRC, 19=ERR_CFG_SIZE, 20=ERR_NO_CFG_FOUND
    'RZ1ACC' / construct.BitsInteger(4),
    'RZ1RES' / construct.BitsInteger(2),
    'RZ1CTR' / enum_134,  # 0=BLOCK COMMUTATION, 1=SINE COMMUTATION, 2=FIELD ORIENTED, 3=NONE
    'RZ1TMP' / common.EvalAdapter('-40*x**0 +  0.74598962*x**1', construct.BitsInteger(8)),  # -40*x^0 +  0.74598962*x^1
    'RZ1AVA' / enum_25,  # 1=AVAILABLE, 0=NOT AVAILABLE
)

adcs_akt_bus2_hk = construct.BitStruct(
    '_name' / construct.Computed('adcs_akt_bus2_hk'),
    'name' / construct.Computed('ADCS AKT BUS2 HK'),
    'MTX2CU' / common.EvalAdapter('0.6451612903*x', construct.BitsInteger(10)),  # 0.6451612903*x
    'MTY2CU' / common.EvalAdapter('0.6451612903*x', construct.BitsInteger(10)),  # 0.6451612903*x
    'MTZ2CU' / common.EvalAdapter('0.6451612903*x', construct.BitsInteger(10)),  # 0.6451612903*x
    'IFP2AA' / enum_25,  # 1=AVAILABLE, 0=NOT AVAILABLE
    'MTZ2RS' / construct.BitsInteger(1),
    'MTX2PW' / common.EvalAdapter('0.097751711*x', construct.BitsInteger(10)),  # 0.097751711*x
    'MTY2PW' / common.EvalAdapter('0.097751711*x', construct.BitsInteger(10)),  # 0.097751711*x
    'MTZ2PW' / common.EvalAdapter('0.097751711*x', construct.BitsInteger(10)),  # 0.097751711*x
    'MTX2FT' / enum_19,  # 0=FAULT, 1=NO FAULT
    'MTX2EN' / enum_46,  # 0=DISABLED, 1=ENABLED
    'MTX2DR' / enum_131,  # 0=NEGATIVE, 1=POSITIVE
    'MTX2SR' / enum_48,  # 0=STBY, 1=ON
    'MTY2FT' / enum_19,  # 1=NO FAULT, 0=FAULT
    'MTY2EN' / enum_46,  # 0=DISABLED, 1=ENABLED
    'MTY2DR' / enum_131,  # 0=NEGATIVE, 1=POSITIVE
    'MTY2SR' / enum_48,  # 0=STBY, 1=ON
    'MTZ2FT' / enum_19,  # 0=FAULT, 1=NO FAULT
    'MTZ2EN' / enum_46,  # 1=ENABLED, 0=DISABLED
    'MTZ2DR' / enum_131,  # 0=NEGATIVE, 1=POSITIVE
    'MTZ2SR' / enum_48,  # 0=STBY, 1=ON
    'RWX2EN' / enum_0,  # 0=OFF, 1=ON
    'RWY2EN' / enum_0,  # 0=OFF, 1=ON
    'RWZ2EN' / enum_0,  # 0=OFF, 1=ON
    'RX2RAT' / common.EvalAdapter('40*x**1 +  -5080*x**0', construct.BitsInteger(8)),  # 40*x^1 +  -5080*x^0
    'RX2CUR' / common.EvalAdapter('10*x', construct.BitsInteger(8)),  # 10*x
    'RX2CMC' / construct.BitsInteger(4),
    'RX2ERC' / construct.BitsInteger(4),
    'RX2OPM' / enum_132,  # 0=TORQUE, 2=IDLE, 1=RATE
    'RX2ECN' / enum_133,  # 0=NO_ERROR, 1=ERR_HAL, 5=ERR_CAN_SEND, 6=ERR_CAN_RECV, 2=ERR_TEST_ERROR, 7=ERR_WRONG_PARAMETER, 8=ERR_NO_RW_ID, 9=ERR_NO_SUCH_CMD, 10=ERR_HAL_UART_INIT, 11=ERR_CAN_INIT, 12=ERR_CFG_ERASE, 13=ERR_CFG_WRITE, 14=ERR_TC_BUF_FULL, 15=ERR_TC_ARG, 16=ERR_I2C_READ, 17=ERR_I2C_WRITE, 18=ERR_CFG_CRC, 19=ERR_CFG_SIZE, 20=ERR_NO_CFG_FOUND
    'RX2ACC' / construct.BitsInteger(4),
    'RX2RES' / construct.BitsInteger(2),
    'RX2CTR' / enum_134,  # 0=BLOCK COMMUTATION, 1=SINE COMMUTATION, 2=FIELD ORIENTED, 3=NONE
    'RX2TMP' / common.EvalAdapter('-40*x**0 +  0.74598962*x**1', construct.BitsInteger(8)),  # -40*x^0 +  0.74598962*x^1
    'RX2AVA' / enum_25,  # 1=AVAILABLE, 0=NOT AVAILABLE
    'RY2RAT' / common.EvalAdapter('40*x**1 +  -5080*x**0', construct.BitsInteger(8)),  # 40*x^1 +  -5080*x^0
    'RY2CUR' / common.EvalAdapter('10*x', construct.BitsInteger(8)),  # 10*x
    'RY2CMC' / construct.BitsInteger(4),
    'RY2ERC' / construct.BitsInteger(4),
    'RY2OPM' / enum_132,  # 0=TORQUE, 2=IDLE, 1=RATE
    'RY2ECN' / enum_133,  # 0=NO_ERROR, 1=ERR_HAL, 5=ERR_CAN_SEND, 6=ERR_CAN_RECV, 2=ERR_TEST_ERROR, 7=ERR_WRONG_PARAMETER, 8=ERR_NO_RW_ID, 9=ERR_NO_SUCH_CMD, 10=ERR_HAL_UART_INIT, 11=ERR_CAN_INIT, 12=ERR_CFG_ERASE, 13=ERR_CFG_WRITE, 14=ERR_TC_BUF_FULL, 15=ERR_TC_ARG, 16=ERR_I2C_READ, 17=ERR_I2C_WRITE, 18=ERR_CFG_CRC, 19=ERR_CFG_SIZE, 20=ERR_NO_CFG_FOUND
    'RY2ACC' / construct.BitsInteger(4),
    'RY2RES' / construct.BitsInteger(2),
    'RY2CTR' / enum_134,  # 0=BLOCK COMMUTATION, 1=SINE COMMUTATION, 2=FIELD ORIENTED, 3=NONE
    'RY2TMP' / common.EvalAdapter('-40*x**0 +  0.74598962*x**1', construct.BitsInteger(8)),  # -40*x^0 +  0.74598962*x^1
    'RY2AVA' / enum_25,  # 1=AVAILABLE, 0=NOT AVAILABLE
    'RZ2RAT' / common.EvalAdapter('40*x**1 +  -5080*x**0', construct.BitsInteger(8)),  # 40*x^1 +  -5080*x^0
    'RZ2CUR' / common.EvalAdapter('10*x', construct.BitsInteger(8)),  # 10*x
    'RZ2CMC' / construct.BitsInteger(4),
    'RZ2ERC' / construct.BitsInteger(4),
    'RZ2OPM' / enum_132,  # 0=TORQUE, 2=IDLE, 1=RATE
    'RZ2ECN' / enum_133,  # 0=NO_ERROR, 1=ERR_HAL, 5=ERR_CAN_SEND, 6=ERR_CAN_RECV, 2=ERR_TEST_ERROR, 7=ERR_WRONG_PARAMETER, 8=ERR_NO_RW_ID, 9=ERR_NO_SUCH_CMD, 10=ERR_HAL_UART_INIT, 11=ERR_CAN_INIT, 12=ERR_CFG_ERASE, 13=ERR_CFG_WRITE, 14=ERR_TC_BUF_FULL, 15=ERR_TC_ARG, 16=ERR_I2C_READ, 17=ERR_I2C_WRITE, 18=ERR_CFG_CRC, 19=ERR_CFG_SIZE, 20=ERR_NO_CFG_FOUND
    'RZ2ACC' / construct.BitsInteger(4),
    'RZ2RES' / construct.BitsInteger(2),
    'RZ2CTR' / enum_134,  # 0=BLOCK COMMUTATION, 1=SINE COMMUTATION, 2=FIELD ORIENTED, 3=NONE
    'RZ2TMP' / common.EvalAdapter('-40*x**0 +  0.74598962*x**1', construct.BitsInteger(8)),  # -40*x^0 +  0.74598962*x^1
    'RZ2AVA' / enum_25,  # 1=AVAILABLE, 0=NOT AVAILABLE
)

adcs_rw_cfg = construct.BitStruct(
    '_name' / construct.Computed('adcs_rw_cfg'),
    'name' / construct.Computed('ADCS RW CFG'),
    'RWCBLP' / common.EvalAdapter('0.1*x', construct.BitsInteger(16)),  # 0.1*x
    'RWCBLI' / common.EvalAdapter('0.01*x', construct.BitsInteger(16)),  # 0.01*x
    'RWCBLW' / common.EvalAdapter('0.01*x', construct.BitsInteger(16)),  # 0.01*x
    'RWCBLM' / common.EvalAdapter('0.01*x', construct.BitsInteger(16)),  # 0.01*x
    'RWCFRP' / common.EvalAdapter('0.1*x', construct.BitsInteger(16)),  # 0.1*x
    'RWCFRI' / common.EvalAdapter('0.01*x', construct.BitsInteger(16)),  # 0.01*x
    'RWCFRW' / common.EvalAdapter('0.01*x', construct.BitsInteger(16)),  # 0.01*x
    'RWCFRM' / common.EvalAdapter('0.01*x', construct.BitsInteger(16)),  # 0.01*x
    'RWCFDP' / common.EvalAdapter('0.0001*x', construct.BitsInteger(16)),  # 0.0001*x
    'RWCFDI' / common.EvalAdapter('0.01*x', construct.BitsInteger(16)),  # 0.01*x
    'RWCFDW' / common.EvalAdapter('0.01*x', construct.BitsInteger(16)),  # 0.01*x
    'RWCFDM' / common.EvalAdapter('0.01*x', construct.BitsInteger(16)),  # 0.01*x
    'RWCFQP' / common.EvalAdapter('0.0001*x', construct.BitsInteger(16)),  # 0.0001*x
    'RWCFQI' / common.EvalAdapter('0.01*x', construct.BitsInteger(16)),  # 0.01*x
    'RWCFQW' / common.EvalAdapter('0.01*x', construct.BitsInteger(16)),  # 0.01*x
    'RWCFQM' / common.EvalAdapter('0.01*x', construct.BitsInteger(16)),  # 0.01*x
    'RWCINM' / common.EvalAdapter('0.01*x', construct.BitsInteger(16)),  # 0.01*x
    'RWCMRT' / common.EvalAdapter('9.54929658551372*x', construct.BitsInteger(16)),  # 9.54929658551372*x
    'RWCMTR' / common.EvalAdapter('0.1*x', construct.BitsInteger(16)),  # 0.1*x
    'RWCAVA' / enum_25,  # 1=AVAILABLE, 0=NOT AVAILABLE
    'RWCBUS' / enum_135,  # 0=BUS1, 1=BUS2
    'RWCENC' / enum_136,  # 0=ENCODER A, 1=ENCODER B
    'RWCAXS' / enum_137,  # 1=RW X, 2=RW Y, 3=RW Z
    'RWCRES' / construct.BitsInteger(3),
)

adcs_sun_sen_bus1_hk = construct.BitStruct(
    '_name' / construct.Computed('adcs_sun_sen_bus1_hk'),
    'name' / construct.Computed('ADCS SUN SEN BUS1 HK'),
    'SXP1CC' / construct.BitsInteger(3),
    'SXP1EO' / enum_138,  # 0=NO ERROR, 1=CAN TX TO, 2=CAN BUF OVFL, 3=SPI TX FAIL, 4=SPI RX FAIL, 5=TC INVLD LEN, 6=TC INVLD CMD CODE, 7=TC INVLD CMD PARAM, 8=FLASH WRITE ERR, 9=FLASH ERASE ERR, 10=CFG CRC ERR, 11=NO CFG FOUND, 12=CFG SIZE INVLD, 13=ADC START ERR, 14=SPI RX DMA ERR, 17=PEAK WIDTH VIOL, 18=PEAK UNDEREXPOSED, 19=PEAK OVEREXPOSED, 15=PROF BUF SIZE INVLD, 16=INVLD OPERATION MODE, 24=SUN SENSOR BUSY, 26=STDBY MODE FAIL, 27=SPI WRITE FAIL, 20=SUCCESSFUL, 21=LOCAL CFG BROKEN, 22=MEAS TIMEOUT
    'SXP1MD' / enum_139,  # 1=CMD MODE, 2=ADCS TRIGGER MODE, 3=CONTINUOUS MODE, 0=OFF
    'SXP1EC' / construct.BitsInteger(4),
    'SXP1PF' / enum_140,  # 0=ERASED, 1=FINALIZED, 2=WRITE PENDING, 3=ERASE PENDING
    'SXP1MC' / construct.BitsInteger(4),
    'SXP1XV' / common.EvalAdapter('-1*x**0 +  0.0004884*x**1', construct.BitsInteger(12)),  # -1*x^0 +  0.0004884*x^1
    'SXP1YV' / common.EvalAdapter('-1*x**0 +  0.0004884*x**1', construct.BitsInteger(12)),  # -1*x^0 +  0.0004884*x^1
    'SXP1ZV' / common.EvalAdapter('-1*x**0 +  0.0004884*x**1', construct.BitsInteger(12)),  # -1*x^0 +  0.0004884*x^1
    'SXP1VS' / enum_90,  # 1=VALID, 0=INVALID
    'SXP1TM' / common.EvalAdapter('-60*x**0 +  1.496062992125984*x**1', construct.BitsInteger(7)),  # -60*x^0 +  1.496062992125984*x^1
    'SXN1CC' / construct.BitsInteger(3),
    'SXN1EO' / enum_138,  # 0=NO ERROR, 1=CAN TX TO, 2=CAN BUF OVFL, 3=SPI TX FAIL, 4=SPI RX FAIL, 5=TC INVLD LEN, 6=TC INVLD CMD CODE, 7=TC INVLD CMD PARAM, 8=FLASH WRITE ERR, 9=FLASH ERASE ERR, 10=CFG CRC ERR, 11=NO CFG FOUND, 12=CFG SIZE INVLD, 13=ADC START ERR, 14=SPI RX DMA ERR, 15=PROF BUF SIZE INVLD, 16=INVLD OPERATION MODE, 17=PEAK WIDTH VIOL, 18=PEAK UNDEREXPOSED, 19=PEAK OVEREXPOSED, 24=SUN SENSOR BUSY, 26=STDBY MODE FAIL, 27=SPI WRITE FAIL, 20=SUCCESSFUL, 21=LOCAL CFG BROKEN, 22=MEAS TIMEOUT
    'SXN1MD' / enum_139,  # 1=CMD MODE, 2=ADCS TRIGGER MODE, 3=CONTINUOUS MODE, 0=OFF
    'SXN1EC' / construct.BitsInteger(4),
    'SXN1PF' / enum_140,  # 0=ERASED, 1=FINALIZED, 2=WRITE PENDING, 3=ERASE PENDING
    'SXN1MC' / construct.BitsInteger(4),
    'SXN1XV' / common.EvalAdapter('-1*x**0 +  0.0004884*x**1', construct.BitsInteger(12)),  # -1*x^0 +  0.0004884*x^1
    'SXN1YV' / common.EvalAdapter('-1*x**0 +  0.0004884*x**1', construct.BitsInteger(12)),  # -1*x^0 +  0.0004884*x^1
    'SXN1ZV' / common.EvalAdapter('-1*x**0 +  0.0004884*x**1', construct.BitsInteger(12)),  # -1*x^0 +  0.0004884*x^1
    'SXN1VS' / enum_90,  # 1=VALID, 0=INVALID
    'SXN1TM' / common.EvalAdapter('-60*x**0 +  1.496062992125984*x**1', construct.BitsInteger(7)),  # -60*x^0 +  1.496062992125984*x^1
    'SYP1CC' / construct.BitsInteger(3),
    'SYP1EO' / enum_138,  # 0=NO ERROR, 1=CAN TX TO, 2=CAN BUF OVFL, 3=SPI TX FAIL, 4=SPI RX FAIL, 5=TC INVLD LEN, 6=TC INVLD CMD CODE, 7=TC INVLD CMD PARAM, 8=FLASH WRITE ERR, 9=FLASH ERASE ERR, 10=CFG CRC ERR, 11=NO CFG FOUND, 12=CFG SIZE INVLD, 13=ADC START ERR, 14=SPI RX DMA ERR, 15=PROF BUF SIZE INVLD, 16=INVLD OPERATION MODE, 17=PEAK WIDTH VIOL, 18=PEAK UNDEREXPOSED, 19=PEAK OVEREXPOSED, 24=SUN SENSOR BUSY, 26=STDBY MODE FAIL, 27=SPI WRITE FAIL, 20=SUCCESSFUL, 21=LOCAL CFG BROKEN, 22=MEAS TIMEOUT
    'SYP1MD' / enum_139,  # 1=CMD MODE, 2=ADCS TRIGGER MODE, 3=CONTINUOUS MODE, 0=OFF
    'SYP1EC' / construct.BitsInteger(4),
    'SYP1PF' / enum_140,  # 0=ERASED, 1=FINALIZED, 2=WRITE PENDING, 3=ERASE PENDING
    'SYP1MC' / construct.BitsInteger(4),
    'SYP1XV' / common.EvalAdapter('-1*x**0 +  0.0004884*x**1', construct.BitsInteger(12)),  # -1*x^0 +  0.0004884*x^1
    'SYP1YV' / common.EvalAdapter('-1*x**0 +  0.0004884*x**1', construct.BitsInteger(12)),  # -1*x^0 +  0.0004884*x^1
    'SYP1ZV' / common.EvalAdapter('-1*x**0 +  0.0004884*x**1', construct.BitsInteger(12)),  # -1*x^0 +  0.0004884*x^1
    'SYP1VS' / enum_90,  # 1=VALID, 0=INVALID
    'SYP1TM' / common.EvalAdapter('-60*x**0 +  1.496062992125984*x**1', construct.BitsInteger(7)),  # -60*x^0 +  1.496062992125984*x^1
    'SYN1CC' / construct.BitsInteger(3),
    'SYN1EO' / enum_138,  # 0=NO ERROR, 1=CAN TX TO, 2=CAN BUF OVFL, 3=SPI TX FAIL, 4=SPI RX FAIL, 5=TC INVLD LEN, 6=TC INVLD CMD CODE, 7=TC INVLD CMD PARAM, 8=FLASH WRITE ERR, 9=FLASH ERASE ERR, 10=CFG CRC ERR, 11=NO CFG FOUND, 12=CFG SIZE INVLD, 13=ADC START ERR, 14=SPI RX DMA ERR, 15=PROF BUF SIZE INVLD, 16=INVLD OPERATION MODE, 17=PEAK WIDTH VIOL, 18=PEAK UNDEREXPOSED, 19=PEAK OVEREXPOSED, 24=SUN SENSOR BUSY, 26=STDBY MODE FAIL, 27=SPI WRITE FAIL, 20=SUCCESSFUL, 21=LOCAL CFG BROKEN, 22=MEAS TIMEOUT
    'SYN1MD' / enum_139,  # 1=CMD MODE, 2=ADCS TRIGGER MODE, 3=CONTINUOUS MODE, 0=OFF
    'SYN1EC' / construct.BitsInteger(4),
    'SYN1PF' / enum_140,  # 0=ERASED, 1=FINALIZED, 2=WRITE PENDING, 3=ERASE PENDING
    'SYN1MC' / construct.BitsInteger(4),
    'SYN1XV' / common.EvalAdapter('-1*x**0 +  0.0004884*x**1', construct.BitsInteger(12)),  # -1*x^0 +  0.0004884*x^1
    'SYN1YV' / common.EvalAdapter('-1*x**0 +  0.0004884*x**1', construct.BitsInteger(12)),  # -1*x^0 +  0.0004884*x^1
    'SYN1ZV' / common.EvalAdapter('-1*x**0 +  0.0004884*x**1', construct.BitsInteger(12)),  # -1*x^0 +  0.0004884*x^1
    'SYN1VS' / enum_90,  # 1=VALID, 0=INVALID
    'SYN1TM' / common.EvalAdapter('-60*x**0 +  1.496062992125984*x**1', construct.BitsInteger(7)),  # -60*x^0 +  1.496062992125984*x^1
    'SZP1CC' / construct.BitsInteger(3),
    'SZP1EO' / enum_138,  # 0=NO ERROR, 1=CAN TX TO, 2=CAN BUF OVFL, 3=SPI TX FAIL, 4=SPI RX FAIL, 5=TC INVLD LEN, 6=TC INVLD CMD CODE, 7=TC INVLD CMD PARAM, 8=FLASH WRITE ERR, 9=FLASH ERASE ERR, 10=CFG CRC ERR, 11=NO CFG FOUND, 12=CFG SIZE INVLD, 13=ADC START ERR, 14=SPI RX DMA ERR, 15=PROF BUF SIZE INVLD, 16=INVLD OPERATION MODE, 17=PEAK WIDTH VIOL, 18=PEAK UNDEREXPOSED, 19=PEAK OVEREXPOSED, 24=SUN SENSOR BUSY, 26=STDBY MODE FAIL, 27=SPI WRITE FAIL, 20=SUCCESSFUL, 21=LOCAL CFG BROKEN, 22=MEAS TIMEOUT
    'SZP1MD' / enum_139,  # 1=CMD MODE, 2=ADCS TRIGGER MODE, 3=CONTINUOUS MODE, 0=OFF
    'SZP1EC' / construct.BitsInteger(4),
    'SZP1PF' / enum_140,  # 0=ERASED, 1=FINALIZED, 2=WRITE PENDING, 3=ERASE PENDING
    'SZP1MC' / construct.BitsInteger(4),
    'SZP1XV' / common.EvalAdapter('-1*x**0 +  0.0004884*x**1', construct.BitsInteger(12)),  # -1*x^0 +  0.0004884*x^1
    'SZP1YV' / common.EvalAdapter('-1*x**0 +  0.0004884*x**1', construct.BitsInteger(12)),  # -1*x^0 +  0.0004884*x^1
    'SZP1ZV' / common.EvalAdapter('-1*x**0 +  0.0004884*x**1', construct.BitsInteger(12)),  # -1*x^0 +  0.0004884*x^1
    'SZP1VS' / enum_90,  # 1=VALID, 0=INVALID
    'SZP1TM' / common.EvalAdapter('-60*x**0 +  1.496062992125984*x**1', construct.BitsInteger(7)),  # -60*x^0 +  1.496062992125984*x^1
    'SZN1CC' / construct.BitsInteger(3),
    'SZN1EO' / enum_138,  # 0=NO ERROR, 1=CAN TX TO, 2=CAN BUF OVFL, 3=SPI TX FAIL, 4=SPI RX FAIL, 5=TC INVLD LEN, 6=TC INVLD CMD CODE, 7=TC INVLD CMD PARAM, 8=FLASH WRITE ERR, 9=FLASH ERASE ERR, 10=CFG CRC ERR, 11=NO CFG FOUND, 12=CFG SIZE INVLD, 13=ADC START ERR, 14=SPI RX DMA ERR, 15=PROF BUF SIZE INVLD, 16=INVLD OPERATION MODE, 17=PEAK WIDTH VIOL, 18=PEAK UNDEREXPOSED, 19=PEAK OVEREXPOSED, 24=SUN SENSOR BUSY, 26=STDBY MODE FAIL, 27=SPI WRITE FAIL, 20=SUCCESSFUL, 21=LOCAL CFG BROKEN, 22=MEAS TIMEOUT
    'SZN1MD' / enum_139,  # 1=CMD MODE, 2=ADCS TRIGGER MODE, 3=CONTINUOUS MODE, 0=OFF
    'SZN1EC' / construct.BitsInteger(4),
    'SZN1PF' / enum_140,  # 0=ERASED, 1=FINALIZED, 2=WRITE PENDING, 3=ERASE PENDING
    'SZN1MC' / construct.BitsInteger(4),
    'SZN1XV' / common.EvalAdapter('-1*x**0 +  0.0004884*x**1', construct.BitsInteger(12)),  # -1*x^0 +  0.0004884*x^1
    'SZN1YV' / common.EvalAdapter('-1*x**0 +  0.0004884*x**1', construct.BitsInteger(12)),  # -1*x^0 +  0.0004884*x^1
    'SZN1ZV' / common.EvalAdapter('-1*x**0 +  0.0004884*x**1', construct.BitsInteger(12)),  # -1*x^0 +  0.0004884*x^1
    'SZN1VS' / enum_90,  # 1=VALID, 0=INVALID
    'SZN1TM' / common.EvalAdapter('-60*x**0 +  1.496062992125984*x**1', construct.BitsInteger(7)),  # -60*x^0 +  1.496062992125984*x^1
)

adcs_sun_sen_bus2_hk = construct.BitStruct(
    '_name' / construct.Computed('adcs_sun_sen_bus2_hk'),
    'name' / construct.Computed('ADCS SUN SEN BUS2 HK'),
    'SXP2CC' / construct.BitsInteger(3),
    'SXP2EO' / enum_138,  # 0=NO ERROR, 1=CAN TX TO, 2=CAN BUF OVFL, 3=SPI TX FAIL, 4=SPI RX FAIL, 5=TC INVLD LEN, 6=TC INVLD CMD CODE, 7=TC INVLD CMD PARAM, 8=FLASH WRITE ERR, 9=FLASH ERASE ERR, 10=CFG CRC ERR, 11=NO CFG FOUND, 12=CFG SIZE INVLD, 13=ADC START ERR, 14=SPI RX DMA ERR, 15=PROF BUF SIZE INVLD, 16=INVLD OPERATION MODE, 17=PEAK WIDTH VIOL, 18=PEAK UNDEREXPOSED, 19=PEAK OVEREXPOSED, 24=SUN SENSOR BUSY, 26=STDBY MODE FAIL, 27=SPI WRITE FAIL, 20=SUCCESSFUL, 21=LOCAL CFG BROKEN, 22=MEAS TIMEOUT
    'SXP2MD' / enum_139,  # 1=CMD MODE, 2=ADCS TRIGGER MODE, 3=CONTINUOUS MODE, 0=OFF
    'SXP2EC' / construct.BitsInteger(4),
    'SXP2PF' / enum_140,  # 0=ERASED, 1=FINALIZED, 2=WRITE PENDING, 3=ERASE PENDING
    'SXP2MC' / construct.BitsInteger(4),
    'SXP2XV' / common.EvalAdapter('-1*x**0 +  0.0004884*x**1', construct.BitsInteger(12)),  # -1*x^0 +  0.0004884*x^1
    'SXP2YV' / common.EvalAdapter('-1*x**0 +  0.0004884*x**1', construct.BitsInteger(12)),  # -1*x^0 +  0.0004884*x^1
    'SXP2ZV' / common.EvalAdapter('-1*x**0 +  0.0004884*x**1', construct.BitsInteger(12)),  # -1*x^0 +  0.0004884*x^1
    'SXP2VS' / enum_90,  # 1=VALID, 0=INVALID
    'SXP2TM' / common.EvalAdapter('-60*x**0 +  1.496062992125984*x**1', construct.BitsInteger(7)),  # -60*x^0 +  1.496062992125984*x^1
    'SXN2CC' / construct.BitsInteger(3),
    'SXN2EO' / enum_138,  # 0=NO ERROR, 1=CAN TX TO, 2=CAN BUF OVFL, 3=SPI TX FAIL, 4=SPI RX FAIL, 5=TC INVLD LEN, 6=TC INVLD CMD CODE, 7=TC INVLD CMD PARAM, 8=FLASH WRITE ERR, 9=FLASH ERASE ERR, 10=CFG CRC ERR, 11=NO CFG FOUND, 12=CFG SIZE INVLD, 13=ADC START ERR, 14=SPI RX DMA ERR, 15=PROF BUF SIZE INVLD, 16=INVLD OPERATION MODE, 17=PEAK WIDTH VIOL, 18=PEAK UNDEREXPOSED, 19=PEAK OVEREXPOSED, 24=SUN SENSOR BUSY, 26=STDBY MODE FAIL, 27=SPI WRITE FAIL, 20=SUCCESSFUL, 21=LOCAL CFG BROKEN, 22=MEAS TIMEOUT
    'SXN2MD' / enum_139,  # 1=CMD MODE, 2=ADCS TRIGGER MODE, 3=CONTINUOUS MODE, 0=OFF
    'SXN2EC' / construct.BitsInteger(4),
    'SXN2PF' / enum_140,  # 0=ERASED, 1=FINALIZED, 2=WRITE PENDING, 3=ERASE PENDING
    'SXN2MC' / construct.BitsInteger(4),
    'SXN2XV' / common.EvalAdapter('-1*x**0 +  0.0004884*x**1', construct.BitsInteger(12)),  # -1*x^0 +  0.0004884*x^1
    'SXN2YV' / common.EvalAdapter('-1*x**0 +  0.0004884*x**1', construct.BitsInteger(12)),  # -1*x^0 +  0.0004884*x^1
    'SXN2ZV' / common.EvalAdapter('-1*x**0 +  0.0004884*x**1', construct.BitsInteger(12)),  # -1*x^0 +  0.0004884*x^1
    'SXN2VS' / enum_90,  # 1=VALID, 0=INVALID
    'SXN2TM' / common.EvalAdapter('-60*x**0 +  1.496062992125984*x**1', construct.BitsInteger(7)),  # -60*x^0 +  1.496062992125984*x^1
    'SYP2CC' / construct.BitsInteger(3),
    'SYP2EO' / enum_138,  # 0=NO ERROR, 1=CAN TX TO, 2=CAN BUF OVFL, 3=SPI TX FAIL, 4=SPI RX FAIL, 5=TC INVLD LEN, 6=TC INVLD CMD CODE, 7=TC INVLD CMD PARAM, 8=FLASH WRITE ERR, 9=FLASH ERASE ERR, 10=CFG CRC ERR, 11=NO CFG FOUND, 12=CFG SIZE INVLD, 13=ADC START ERR, 14=SPI RX DMA ERR, 15=PROF BUF SIZE INVLD, 16=INVLD OPERATION MODE, 17=PEAK WIDTH VIOL, 18=PEAK UNDEREXPOSED, 19=PEAK OVEREXPOSED, 24=SUN SENSOR BUSY, 26=STDBY MODE FAIL, 27=SPI WRITE FAIL, 20=SUCCESSFUL, 21=LOCAL CFG BROKEN, 22=MEAS TIMEOUT
    'SYP2MD' / enum_139,  # 1=CMD MODE, 2=ADCS TRIGGER MODE, 3=CONTINUOUS MODE, 0=OFF
    'SYP2EC' / construct.BitsInteger(4),
    'SYP2PF' / enum_140,  # 0=ERASED, 1=FINALIZED, 2=WRITE PENDING, 3=ERASE PENDING
    'SYP2MC' / construct.BitsInteger(4),
    'SYP2XV' / common.EvalAdapter('-1*x**0 +  0.0004884*x**1', construct.BitsInteger(12)),  # -1*x^0 +  0.0004884*x^1
    'SYP2YV' / common.EvalAdapter('-1*x**0 +  0.0004884*x**1', construct.BitsInteger(12)),  # -1*x^0 +  0.0004884*x^1
    'SYP2ZV' / common.EvalAdapter('-1*x**0 +  0.0004884*x**1', construct.BitsInteger(12)),  # -1*x^0 +  0.0004884*x^1
    'SYP2VS' / enum_90,  # 1=VALID, 0=INVALID
    'SYP2TM' / common.EvalAdapter('-60*x**0 +  1.496062992125984*x**1', construct.BitsInteger(7)),  # -60*x^0 +  1.496062992125984*x^1
    'SYN2CC' / construct.BitsInteger(3),
    'SYN2EO' / enum_138,  # 0=NO ERROR, 1=CAN TX TO, 2=CAN BUF OVFL, 3=SPI TX FAIL, 4=SPI RX FAIL, 5=TC INVLD LEN, 6=TC INVLD CMD CODE, 7=TC INVLD CMD PARAM, 8=FLASH WRITE ERR, 9=FLASH ERASE ERR, 10=CFG CRC ERR, 11=NO CFG FOUND, 12=CFG SIZE INVLD, 13=ADC START ERR, 14=SPI RX DMA ERR, 15=PROF BUF SIZE INVLD, 16=INVLD OPERATION MODE, 17=PEAK WIDTH VIOL, 18=PEAK UNDEREXPOSED, 19=PEAK OVEREXPOSED, 24=SUN SENSOR BUSY, 26=STDBY MODE FAIL, 27=SPI WRITE FAIL, 20=SUCCESSFUL, 21=LOCAL CFG BROKEN, 22=MEAS TIMEOUT
    'SYN2MD' / enum_139,  # 1=CMD MODE, 2=ADCS TRIGGER MODE, 3=CONTINUOUS MODE, 0=OFF
    'SYN2EC' / construct.BitsInteger(4),
    'SYN2PF' / enum_140,  # 0=ERASED, 1=FINALIZED, 2=WRITE PENDING, 3=ERASE PENDING
    'SYN2MC' / construct.BitsInteger(4),
    'SYN2XV' / common.EvalAdapter('-1*x**0 +  0.0004884*x**1', construct.BitsInteger(12)),  # -1*x^0 +  0.0004884*x^1
    'SYN2YV' / common.EvalAdapter('-1*x**0 +  0.0004884*x**1', construct.BitsInteger(12)),  # -1*x^0 +  0.0004884*x^1
    'SYN2ZV' / common.EvalAdapter('-1*x**0 +  0.0004884*x**1', construct.BitsInteger(12)),  # -1*x^0 +  0.0004884*x^1
    'SYN2VS' / enum_90,  # 1=VALID, 0=INVALID
    'SYN2TM' / common.EvalAdapter('-60*x**0 +  1.496062992125984*x**1', construct.BitsInteger(7)),  # -60*x^0 +  1.496062992125984*x^1
    'SZP2CC' / construct.BitsInteger(3),
    'SZP2EO' / enum_138,  # 0=NO ERROR, 1=CAN TX TO, 2=CAN BUF OVFL, 3=SPI TX FAIL, 4=SPI RX FAIL, 5=TC INVLD LEN, 6=TC INVLD CMD CODE, 7=TC INVLD CMD PARAM, 8=FLASH WRITE ERR, 9=FLASH ERASE ERR, 10=CFG CRC ERR, 11=NO CFG FOUND, 12=CFG SIZE INVLD, 13=ADC START ERR, 14=SPI RX DMA ERR, 15=PROF BUF SIZE INVLD, 16=INVLD OPERATION MODE, 17=PEAK WIDTH VIOL, 18=PEAK UNDEREXPOSED, 19=PEAK OVEREXPOSED, 24=SUN SENSOR BUSY, 26=STDBY MODE FAIL, 27=SPI WRITE FAIL, 20=SUCCESSFUL, 21=LOCAL CFG BROKEN, 22=MEAS TIMEOUT
    'SZP2MD' / enum_139,  # 1=CMD MODE, 2=ADCS TRIGGER MODE, 3=CONTINUOUS MODE, 0=OFF
    'SZP2EC' / construct.BitsInteger(4),
    'SZP2PF' / enum_140,  # 0=ERASED, 1=FINALIZED, 2=WRITE PENDING, 3=ERASE PENDING
    'SZP2MC' / construct.BitsInteger(4),
    'SZP2XV' / common.EvalAdapter('-1*x**0 +  0.0004884*x**1', construct.BitsInteger(12)),  # -1*x^0 +  0.0004884*x^1
    'SZP2YV' / common.EvalAdapter('-1*x**0 +  0.0004884*x**1', construct.BitsInteger(12)),  # -1*x^0 +  0.0004884*x^1
    'SZP2ZV' / common.EvalAdapter('-1*x**0 +  0.0004884*x**1', construct.BitsInteger(12)),  # -1*x^0 +  0.0004884*x^1
    'SZP2VS' / enum_90,  # 1=VALID, 0=INVALID
    'SZP2TM' / common.EvalAdapter('-60*x**0 +  1.496062992125984*x**1', construct.BitsInteger(7)),  # -60*x^0 +  1.496062992125984*x^1
    'SZN2CC' / construct.BitsInteger(3),
    'SZN2EO' / enum_138,  # 0=NO ERROR, 1=CAN TX TO, 2=CAN BUF OVFL, 3=SPI TX FAIL, 4=SPI RX FAIL, 5=TC INVLD LEN, 6=TC INVLD CMD CODE, 7=TC INVLD CMD PARAM, 8=FLASH WRITE ERR, 9=FLASH ERASE ERR, 10=CFG CRC ERR, 11=NO CFG FOUND, 12=CFG SIZE INVLD, 13=ADC START ERR, 14=SPI RX DMA ERR, 15=PROF BUF SIZE INVLD, 16=INVLD OPERATION MODE, 17=PEAK WIDTH VIOL, 18=PEAK UNDEREXPOSED, 19=PEAK OVEREXPOSED, 24=SUN SENSOR BUSY, 26=STDBY MODE FAIL, 27=SPI WRITE FAIL, 20=SUCCESSFUL, 21=LOCAL CFG BROKEN, 22=MEAS TIMEOUT
    'SZN2MD' / enum_139,  # 1=CMD MODE, 2=ADCS TRIGGER MODE, 3=CONTINUOUS MODE, 0=OFF
    'SZN2EC' / construct.BitsInteger(4),
    'SZN2PF' / enum_140,  # 0=ERASED, 1=FINALIZED, 2=WRITE PENDING, 3=ERASE PENDING
    'SZN2MC' / construct.BitsInteger(4),
    'SZN2XV' / common.EvalAdapter('-1*x**0 +  0.0004884*x**1', construct.BitsInteger(12)),  # -1*x^0 +  0.0004884*x^1
    'SZN2YV' / common.EvalAdapter('-1*x**0 +  0.0004884*x**1', construct.BitsInteger(12)),  # -1*x^0 +  0.0004884*x^1
    'SZN2ZV' / common.EvalAdapter('-1*x**0 +  0.0004884*x**1', construct.BitsInteger(12)),  # -1*x^0 +  0.0004884*x^1
    'SZN2VS' / enum_90,  # 1=VALID, 0=INVALID
    'SZN2TM' / common.EvalAdapter('-60*x**0 +  1.496062992125984*x**1', construct.BitsInteger(7)),  # -60*x^0 +  1.496062992125984*x^1
)

adcs_sun_sen_cfg = construct.BitStruct(
    '_name' / construct.Computed('adcs_sun_sen_cfg'),
    'name' / construct.Computed('ADCS SUN SEN CFG'),
    'SSCSID' / enum_141,  # 0=SUN SENSOR XP, 1=SUN SENSOR XN, 2=SUN SENSOR YP, 3=SUN SENSOR YN, 4=SUN SENSOR ZP, 5=SUN SENSOR ZN
    'SSCBUS' / enum_99,  # 0=BUS 1, 1=BUS 2
    'SSCTSS' / enum_142,  # 0=EXTERNAL, 1=INTERNAL
    'SSCDBS' / enum_46,  # 0=DISABLED, 1=ENABLED
    'SSCAVI' / enum_25,  # 0=NOT AVAILABLE, 1=AVAILABLE
    'SSCBLT' / construct.BitsInteger(8),
    'SSCUVL' / enum_143,  # 0=1.85 V, 1=1.90 V, 2=1.95 V, 3=2.00 V, 4=2.05 V, 5=2.10 V, 6=2.15 V, 7=2.20 V, 8=2.25 V, 9=2.30 V, 10=2.35 V, 11=2.40 V, 12=2.45 V, 13=2.50 V, 14=2.55 V, 15=2.60 V
    'SSCLVL' / enum_144,  # 0=0.80 V, 1=0.85 V, 2=0.90 V, 3=0.95 V, 4=1.00 V, 5=1.05 V, 6=1.10 V, 7=1.15 V, 8=1.20 V, 9=1.25 V, 10=1.30 V, 11=1.35 V, 12=1.40 V, 13=1.45 V, 14=1.50 V, 15=1.55 V
    'SSCCFC' / enum_145,  # 0=CAP 0.2 pF, 1=CAP 0.4 pF, 2=CAP 0.6 pF, 3=CAP 0.8 pF
    'SSCAAG' / enum_146,  # 0=GAIN 1.000, 1=GAIN 0.500, 2=GAIN 0.333, 3=GAIN 0.250, 4=GAIN 0.200, 5=GAIN 0.167, 6=GAIN 0.143, 7=GAIN 0.125, 8=GAIN 0.111, 9=GAIN 0.100, 10=GAIN 0.091, 11=GAIN 0.083, 12=GAIN 0.077, 13=GAIN 0.071, 14=GAIN 0.067, 15=GAIN 0.063
    'SSCCGA' / enum_147,  # 0=5 PIXELS, 1=9 PIXELS, 2=19 PIXELS, 3=29 PIXELS
    'SSCCGT' / construct.BitsInteger(8),
    'SSCINT' / construct.BitsInteger(16),
    'SSCEHS' / enum_46,  # 0=DISABLED, 1=ENABLED
    'SSCDOP' / enum_148,  # 0=CMD MODE, 2=CONTINOUS MODE, 1=ADCS TRIGGER MODE
    'SSCRES' / construct.BitsInteger(4),
    'SSCAEA' / enum_42,  # 1=ACTIVATED, 0=DEACTIVATED
    'SSCPWX' / construct.BitsInteger(12),
    'SSCPWY' / construct.BitsInteger(12),
    'SSCASS' / construct.BitsInteger(8),
    'SSCAET' / construct.BitsInteger(16),
    'SSCEHL' / construct.BitsInteger(16),
    'SSCCTX' / common.EvalAdapter('0.00003051758*x', construct.BitsInteger(24)),  # 0.00003051758*x
    'SSCCTY' / common.EvalAdapter('0.00003051758*x', construct.BitsInteger(24)),  # 0.00003051758*x
    'SSCELL' / construct.BitsInteger(16),
    'SSCCMP' / construct.BitsInteger(16),
    'SSCHTX' / construct.BitsInteger(8),
    'SSCHTY' / construct.BitsInteger(8),
    'SSCLTX' / construct.BitsInteger(8),
    'SSCLTY' / construct.BitsInteger(8),
    'SSCRAZ' / common.EvalAdapter('-180*x**0 +  0.005493248*x**1', construct.BitsInteger(16)),  # -180*x^0 +  0.005493248*x^1
    'SSCCA0' / common.EvalAdapter('-1*x**0 +  0.000030518043793392844*x**1', construct.BitsInteger(16)),  # -1*x^0 +  0.000030518043793392844*x^1
    'SSCCA1' / common.EvalAdapter('-10*x**0 +  0.00030518043793392844*x**1', construct.BitsInteger(16)),  # -10*x^0 +  0.00030518043793392844*x^1
    'SSCCA2' / common.EvalAdapter('-100*x**0 +  0.0030518043793392844*x**1', construct.BitsInteger(16)),  # -100*x^0 +  0.0030518043793392844*x^1
    'SSCCA3' / common.EvalAdapter('-100*x**0 +  0.0030518043793392844*x**1', construct.BitsInteger(16)),  # -100*x^0 +  0.0030518043793392844*x^1
    'SSCCA4' / common.EvalAdapter('-10*x**0 +  0.00030518043793392844*x**1', construct.BitsInteger(16)),  # -10*x^0 +  0.00030518043793392844*x^1
    'SSCCA5' / common.EvalAdapter('-100*x**0 +  0.0030518043793392844*x**1', construct.BitsInteger(16)),  # -100*x^0 +  0.0030518043793392844*x^1
)

power_sensor_hk = construct.BitStruct(
    '_name' / construct.Computed('power_sensor_hk'),
    'name' / construct.Computed('POWER SENSOR HK'),
    'O1VLTG' / common.EvalAdapter('0.016*x', construct.BitsInteger(8)),  # 0.016*x
    'O2VLTG' / common.EvalAdapter('0.016*x', construct.BitsInteger(8)),  # 0.016*x
    'UHF1VS' / common.EvalAdapter('0.032*x', construct.BitsInteger(8)),  # 0.032*x
    'IFP1VS' / common.EvalAdapter('0.032*x', construct.BitsInteger(8)),  # 0.032*x
    'ADCS1V' / common.EvalAdapter('0.016*x', construct.BitsInteger(8)),  # 0.016*x
    'AI1VLT' / common.EvalAdapter('0.064*x', construct.BitsInteger(8)),  # 0.064*x
    'VHF1VS' / common.EvalAdapter('0.032*x', construct.BitsInteger(8)),  # 0.032*x
    'SPZN1V' / common.EvalAdapter('0.032*x', construct.BitsInteger(8)),  # 0.032*x
    'O3VLTG' / common.EvalAdapter('0.016*x', construct.BitsInteger(8)),  # 0.016*x
    'O4VLTG' / common.EvalAdapter('0.016*x', construct.BitsInteger(8)),  # 0.016*x
    'UHF2VS' / common.EvalAdapter('0.032*x', construct.BitsInteger(8)),  # 0.032*x
    'IFP2VS' / common.EvalAdapter('0.032*x', construct.BitsInteger(8)),  # 0.032*x
    'ADCS2V' / common.EvalAdapter('0.016*x', construct.BitsInteger(8)),  # 0.016*x
    'AI2VLT' / common.EvalAdapter('0.064*x', construct.BitsInteger(8)),  # 0.064*x
    'VHF2VS' / common.EvalAdapter('0.032*x', construct.BitsInteger(8)),  # 0.032*x
    'SPZN2V' / common.EvalAdapter('0.032*x', construct.BitsInteger(8)),  # 0.032*x
    'SPXP1V' / common.EvalAdapter('0.032*x', construct.BitsInteger(8)),  # 0.032*x
    'SPYP1V' / common.EvalAdapter('0.032*x', construct.BitsInteger(8)),  # 0.032*x
    'SPZP1V' / common.EvalAdapter('0.032*x', construct.BitsInteger(8)),  # 0.032*x
    'SPMB1V' / common.EvalAdapter('0.064*x', construct.BitsInteger(8)),  # 0.064*x
    'SBND1V' / common.EvalAdapter('0.064*x', construct.BitsInteger(8)),  # 0.064*x
    'TH1VLT' / common.EvalAdapter('0.064*x', construct.BitsInteger(8)),  # 0.064*x
    'MV1VLT' / common.EvalAdapter('0.032*x', construct.BitsInteger(8)),  # 0.032*x
    'SPXP2V' / common.EvalAdapter('0.032*x', construct.BitsInteger(8)),  # 0.032*x
    'SPYN2V' / common.EvalAdapter('0.032*x', construct.BitsInteger(8)),  # 0.032*x
    'SPZP2V' / common.EvalAdapter('0.032*x', construct.BitsInteger(8)),  # 0.032*x
    'SPMB2V' / common.EvalAdapter('0.064*x', construct.BitsInteger(8)),  # 0.064*x
    'SBND2V' / common.EvalAdapter('0.064*x', construct.BitsInteger(8)),  # 0.064*x
    'TH2VLT' / common.EvalAdapter('0.064*x', construct.BitsInteger(8)),  # 0.064*x
    'MV2VLT' / common.EvalAdapter('0.032*x', construct.BitsInteger(8)),  # 0.032*x
    'O1CURR' / common.EvalAdapter('1.2121212121212122*x', construct.BitsInteger(8)),  # 1.2121212121212122*x
    'O2CURR' / common.EvalAdapter('1.212121212*x', construct.BitsInteger(8)),  # 1.212121212*x
    'UHF1CT' / common.EvalAdapter('16*x', construct.BitsInteger(8)),  # 16*x
    'IFP1CR' / common.EvalAdapter('8.88888888888889*x', construct.BitsInteger(8)),  # 8.88888888888889*x
    'ADCS1C' / common.EvalAdapter('1.212121212*x', construct.BitsInteger(8)),  # 1.212121212*x
    'AI1CUR' / common.EvalAdapter('8.88888888888889*x', construct.BitsInteger(8)),  # 8.88888888888889*x
    'VHF1CR' / common.EvalAdapter('16*x', construct.BitsInteger(8)),  # 16*x
    'SPZN1C' / common.EvalAdapter('16*x', construct.BitsInteger(8)),  # 16*x
    'O3CURR' / common.EvalAdapter('1.212121212*x', construct.BitsInteger(8)),  # 1.212121212*x
    'O4CURR' / common.EvalAdapter('1.212121212*x', construct.BitsInteger(8)),  # 1.212121212*x
    'UHF2CT' / common.EvalAdapter('16*x', construct.BitsInteger(8)),  # 16*x
    'IFP2CR' / common.EvalAdapter('8.88888888888889*x', construct.BitsInteger(8)),  # 8.88888888888889*x
    'ADCS2C' / common.EvalAdapter('1.212121212*x', construct.BitsInteger(8)),  # 1.212121212*x
    'AI2CUR' / common.EvalAdapter('8.88888888888889*x', construct.BitsInteger(8)),  # 8.88888888888889*x
    'VHF2CR' / common.EvalAdapter('16*x', construct.BitsInteger(8)),  # 16*x
    'SPZN2C' / common.EvalAdapter('16*x', construct.BitsInteger(8)),  # 16*x
    'SPXP1C' / common.EvalAdapter('16*x', construct.BitsInteger(8)),  # 16*x
    'SPYP1C' / common.EvalAdapter('16*x', construct.BitsInteger(8)),  # 16*x
    'SPZP1C' / common.EvalAdapter('16*x', construct.BitsInteger(8)),  # 16*x
    'SPMB1C' / common.EvalAdapter('8.88888888888889*x', construct.BitsInteger(8)),  # 8.88888888888889*x
    'SBND1C' / common.EvalAdapter('8.88888888888889*x', construct.BitsInteger(8)),  # 8.88888888888889*x
    'TH1CUR' / common.EvalAdapter('17.77777777777778*x', construct.BitsInteger(8)),  # 17.77777777777778*x
    'MV1CUR' / common.EvalAdapter('2.2222222222222223*x', construct.BitsInteger(8)),  # 2.2222222222222223*x
    'PWS1AV' / enum_25,  # 1=AVAILABLE, 0=NOT AVAILABLE
    'SPXP2C' / common.EvalAdapter('16*x', construct.BitsInteger(8)),  # 16*x
    'SPYN2C' / common.EvalAdapter('16*x', construct.BitsInteger(8)),  # 16*x
    'SPZP2C' / common.EvalAdapter('16*x', construct.BitsInteger(8)),  # 16*x
    'SPMB2C' / common.EvalAdapter('8.88888888888889*x', construct.BitsInteger(8)),  # 8.88888888888889*x
    'SBND2C' / common.EvalAdapter('8.88888888888889*x', construct.BitsInteger(8)),  # 8.88888888888889*x
    'TH2CUR' / common.EvalAdapter('17.77777777777778*x', construct.BitsInteger(8)),  # 17.77777777777778*x
    'MV2CUR' / common.EvalAdapter('2.2222222222222223*x', construct.BitsInteger(8)),  # 2.2222222222222223*x
    'PWS2AV' / enum_25,  # 1=AVAILABLE, 0=NOT AVAILABLE
    '_pad0' / construct.BitsInteger(6),
)

pwr_cfg_hk = construct.BitStruct(
    '_name' / construct.Computed('pwr_cfg_hk'),
    'name' / construct.Computed('PWR CFG HK'),
    'P5VIO1' / enum_37,  # 1=YES, 0=NO
    'P5VIO2' / enum_37,  # 0=NO, 1=YES
    'P5VIUH' / enum_37,  # 0=NO, 1=YES
    'P5VIIF' / enum_37,  # 0=NO, 1=YES
    'P5VIAD' / enum_37,  # 0=NO, 1=YES
    'P5VIAI' / enum_37,  # 0=NO, 1=YES
    'P5VIVH' / enum_37,  # 0=NO, 1=YES
    'P5VIZN' / enum_37,  # 0=NO, 1=YES
    'P5VIXP' / enum_37,  # 0=NO, 1=YES
    'P5VISY' / enum_37,  # 0=NO, 1=YES
    'P5VIZP' / enum_37,  # 0=NO, 1=YES
    'P5VIMN' / enum_37,  # 0=NO, 1=YES
    'P5VISB' / enum_37,  # 0=NO, 1=YES
    'P5VITH' / enum_37,  # 0=NO, 1=YES
    'P5VIMV' / enum_37,  # 0=NO, 1=YES
    'P5VCAV' / construct.BitsInteger(1),
    'P5VTAI' / enum_37,  # 0=NO, 1=YES
    'P5VTIF' / enum_37,  # 0=NO, 1=YES
    'P5VTAD' / enum_37,  # 0=NO, 1=YES
    'P5VTTM' / enum_37,  # 0=NO, 1=YES
    'P5VT05' / enum_37,  # 0=NO, 1=YES
    'P5VT12' / enum_37,  # 0=NO, 1=YES
    'P5VTFR' / enum_37,  # 0=NO, 1=YES
    'P5VTZP' / enum_37,  # 0=NO, 1=YES
    'P5VTZN' / enum_37,  # 0=NO, 1=YES
    'P5VTXP' / enum_37,  # 0=NO, 1=YES
    'P5VTSY' / enum_37,  # 0=NO, 1=YES
    'P5VTO1' / enum_37,  # 0=NO, 1=YES
    'P5VTO2' / enum_37,  # 0=NO, 1=YES
    'P5VM05' / enum_37,  # 0=NO, 1=YES
    'P5VM12' / enum_37,  # 0=NO, 1=YES
    'P5VMAI' / enum_37,  # 0=NO, 1=YES
    'P5VLZP' / enum_37,  # 0=NO, 1=YES
    'P5VLZN' / enum_37,  # 0=NO, 1=YES
    'P5VLXP' / enum_37,  # 0=NO, 1=YES
    'P5VLSY' / enum_37,  # 0=NO, 1=YES
    'P5VLSM' / enum_37,  # 0=NO, 1=YES
    'P5VMF1' / enum_37,  # 0=NO, 1=YES
    'P5VMTM' / enum_37,  # 0=NO, 1=YES
    'P5VMF2' / enum_37,  # 0=NO, 1=YES
    'P5VMF3' / enum_37,  # 0=NO, 1=YES
    'P5VMF4' / enum_37,  # 0=NO, 1=YES
    'P5VBMD' / enum_26,  # 0=PFM, 1=PWM
    'P5VCFS' / enum_135,  # 0=BUS1, 1=BUS2
    'P5VGPI' / enum_149,  # 0=ENABLED, 1=DISABLED
    'P12CAV' / construct.BitsInteger(1),
    'P12BMD' / enum_26,  # 0=PFM, 1=PWM
    'P12CFS' / enum_135,  # 0=BUS1, 1=BUS2
)

ifp_cfg_hk = construct.BitStruct(
    '_name' / construct.Computed('ifp_cfg_hk'),
    'name' / construct.Computed('IFP CFG HK'),
    'IFP1DL' / common.EvalAdapter('0.1612903226*x', construct.BitsInteger(16)),  # 0.1612903226*x
    'IFP1DT' / common.EvalAdapter('0.03278688524590164*x', construct.BitsInteger(16)),  # 0.03278688524590164*x
    'IFP1XL' / common.EvalAdapter('0.6451612903*x', construct.BitsInteger(16)),  # 0.6451612903*x
    'IFP1YL' / common.EvalAdapter('0.6451612903*x', construct.BitsInteger(16)),  # 0.6451612903*x
    'IFP1ZL' / common.EvalAdapter('0.6451612903*x', construct.BitsInteger(16)),  # 0.6451612903*x
    'IFP1CT' / common.EvalAdapter('0.03278688524590164*x', construct.BitsInteger(16)),  # 0.03278688524590164*x
    'IFP2DL' / common.EvalAdapter('0.1612903226*x', construct.BitsInteger(16)),  # 0.1612903226*x
    'IFP2DT' / common.EvalAdapter('0.03278688524590164*x', construct.BitsInteger(16)),  # 0.03278688524590164*x
    'IFP2XL' / common.EvalAdapter('0.6451612903*x', construct.BitsInteger(16)),  # 0.6451612903*x
    'IFP2YL' / common.EvalAdapter('0.6451612903*x', construct.BitsInteger(16)),  # 0.6451612903*x
    'IFP2ZL' / common.EvalAdapter('0.6451612903*x', construct.BitsInteger(16)),  # 0.6451612903*x
    'IFP2CT' / common.EvalAdapter('0.03278688524590164*x', construct.BitsInteger(16)),  # 0.03278688524590164*x
    'IFP2CA' / construct.BitsInteger(1),
    'IFP1CA' / construct.BitsInteger(1),
    '_pad0' / construct.BitsInteger(6),
)

thermal_hk = construct.BitStruct(
    '_name' / construct.Computed('thermal_hk'),
    'name' / construct.Computed('THERMAL HK'),
    'AI1PTM' / common.EvalAdapter('-128*x**0 +  1*x**1', construct.BitsInteger(8)),  # -128*x^0 +  1*x^1
    'IFP1TM' / common.EvalAdapter('-128*x**0 +  1*x**1', construct.BitsInteger(8)),  # -128*x^0 +  1*x^1
    'ADCS1T' / common.EvalAdapter('-128*x**0 +  1*x**1', construct.BitsInteger(8)),  # -128*x^0 +  1*x^1
    'TERM1T' / common.EvalAdapter('-128*x**0 +  1*x**1', construct.BitsInteger(8)),  # -128*x^0 +  1*x^1
    'P5V1TM' / common.EvalAdapter('-128*x**0 +  1*x**1', construct.BitsInteger(8)),  # -128*x^0 +  1*x^1
    '12V1TM' / common.EvalAdapter('-128*x**0 +  1*x**1', construct.BitsInteger(8)),  # -128*x^0 +  1*x^1
    'FRNT1T' / common.EvalAdapter('-128*x**0 +  1*x**1', construct.BitsInteger(8)),  # -128*x^0 +  1*x^1
    'SZP1IT' / common.EvalAdapter('-128*x**0 +  1*x**1', construct.BitsInteger(8)),  # -128*x^0 +  1*x^1
    'AI2PTM' / common.EvalAdapter('-128*x**0 +  1*x**1', construct.BitsInteger(8)),  # -128*x^0 +  1*x^1
    'IFP2TM' / common.EvalAdapter('-128*x**0 +  1*x**1', construct.BitsInteger(8)),  # -128*x^0 +  1*x^1
    'ADCS2T' / common.EvalAdapter('-128*x**0 +  1*x**1', construct.BitsInteger(8)),  # -128*x^0 +  1*x^1
    'TERM2T' / common.EvalAdapter('-128*x**0 +  1*x**1', construct.BitsInteger(8)),  # -128*x^0 +  1*x^1
    'P5V2TM' / common.EvalAdapter('-128*x**0 +  1*x**1', construct.BitsInteger(8)),  # -128*x^0 +  1*x^1
    '12V2TM' / common.EvalAdapter('-128*x**0 +  1*x**1', construct.BitsInteger(8)),  # -128*x^0 +  1*x^1
    'FRNT2T' / common.EvalAdapter('-128*x**0 +  1*x**1', construct.BitsInteger(8)),  # -128*x^0 +  1*x^1
    'SZP2IT' / common.EvalAdapter('-128*x**0 +  1*x**1', construct.BitsInteger(8)),  # -128*x^0 +  1*x^1
    'SZN1IT' / common.EvalAdapter('-128*x**0 +  1*x**1', construct.BitsInteger(8)),  # -128*x^0 +  1*x^1
    'SXP1IT' / common.EvalAdapter('-128*x**0 +  1*x**1', construct.BitsInteger(8)),  # -128*x^0 +  1*x^1
    'SYP1IT' / common.EvalAdapter('-128*x**0 +  1*x**1', construct.BitsInteger(8)),  # -128*x^0 +  1*x^1
    'O1TEMP' / common.EvalAdapter('-128*x**0 +  1*x**1', construct.BitsInteger(8)),  # -128*x^0 +  1*x^1
    'O2TEMP' / common.EvalAdapter('-128*x**0 +  1*x**1', construct.BitsInteger(8)),  # -128*x^0 +  1*x^1
    'AI1JTM' / common.EvalAdapter('-42.65387155*x**0 +  0.619346427*x**1 +  0.000022607*x**2', construct.BitsInteger(8)),  # -42.65387155*x^0 +  0.619346427*x^1 +  0.000022607*x^2
    'SZP1OT' / common.EvalAdapter('-93.27894086*x**0 +  0.945045347*x**1 +  0.000028062*x**2', construct.BitsInteger(8)),  # -93.27894086*x^0 +  0.945045347*x^1 +  0.000028062*x^2
    'SZN1OT' / common.EvalAdapter('-93.27894086*x**0 +  0.945045347*x**1 +  0.000028062*x**2', construct.BitsInteger(8)),  # -93.27894086*x^0 +  0.945045347*x^1 +  0.000028062*x^2
    'SZN2IT' / common.EvalAdapter('-128*x**0 +  1*x**1', construct.BitsInteger(8)),  # -128*x^0 +  1*x^1
    'SXP2IT' / common.EvalAdapter('-128*x**0 +  1*x**1', construct.BitsInteger(8)),  # -128*x^0 +  1*x^1
    'SYN2IT' / common.EvalAdapter('-128*x**0 +  1*x**1', construct.BitsInteger(8)),  # -128*x^0 +  1*x^1
    'O3TEMP' / common.EvalAdapter('-128*x**0 +  1*x**1', construct.BitsInteger(8)),  # -128*x^0 +  1*x^1
    'O4TEMP' / common.EvalAdapter('-128*x**0 +  1*x**1', construct.BitsInteger(8)),  # -128*x^0 +  1*x^1
    'AI2JTM' / common.EvalAdapter('-43.78139196*x**0 +  0.616088207*x**1 +  0.0000223757*x**2', construct.BitsInteger(8)),  # -43.78139196*x^0 +  0.616088207*x^1 +  0.0000223757*x^2
    'SZP2OT' / common.EvalAdapter('-93.41041843*x**0 +  0.944294731*x**1 +  0.0000280179*x**2', construct.BitsInteger(8)),  # -93.41041843*x^0 +  0.944294731*x^1 +  0.0000280179*x^2
    'SZN2OT' / common.EvalAdapter('-93.41041843*x**0 +  0.944294731*x**1 +  0.0000280179*x**2', construct.BitsInteger(8)),  # -93.41041843*x^0 +  0.944294731*x^1 +  0.0000280179*x^2
    'SXP1OT' / common.EvalAdapter('-93.27894086*x**0 +  0.945045347*x**1 +  0.000028062*x**2', construct.BitsInteger(8)),  # -93.27894086*x^0 +  0.945045347*x^1 +  0.000028062*x^2
    'SYP1OT' / common.EvalAdapter('-93.27894086*x**0 +  0.945045347*x**1 +  0.000028062*x**2', construct.BitsInteger(8)),  # -93.27894086*x^0 +  0.945045347*x^1 +  0.000028062*x^2
    'SPMB1T' / common.EvalAdapter('-93.27894086*x**0 +  0.945045347*x**1 +  0.000028062*x**2', construct.BitsInteger(8)),  # -93.27894086*x^0 +  0.945045347*x^1 +  0.000028062*x^2
    'THK1AV' / enum_25,  # 1=AVAILABLE, 0=NOT AVAILABLE
    'SXP2OT' / common.EvalAdapter('-93.41041843*x**0 +  0.944294731*x**1 +  0.0000280179*x**2', construct.BitsInteger(8)),  # -93.41041843*x^0 +  0.944294731*x^1 +  0.0000280179*x^2
    'SYN2OT' / common.EvalAdapter('-93.41041843*x**0 +  0.944294731*x**1 +  0.0000280179*x**2', construct.BitsInteger(8)),  # -93.41041843*x^0 +  0.944294731*x^1 +  0.0000280179*x^2
    'SPMB2T' / common.EvalAdapter('-93.41041843*x**0 +  0.944294731*x**1 +  0.0000280179*x**2', construct.BitsInteger(8)),  # -93.41041843*x^0 +  0.944294731*x^1 +  0.0000280179*x^2
    'THK2AV' / enum_25,  # 1=AVAILABLE, 0=NOT AVAILABLE
    '_pad0' / construct.BitsInteger(6),
)

vhf_ext_hk = construct.BitStruct(
    '_name' / construct.Computed('vhf_ext_hk'),
    'name' / construct.Computed('VHF EXT HK'),
    'VHF1TF' / common.EvalAdapter('0.001*x', construct.BitsInteger(24)),  # 0.001*x
    'VHF1RF' / common.EvalAdapter('0.001*x', construct.BitsInteger(24)),  # 0.001*x
    'VHF1TX' / enum_150,  # 0=AFSK 1K2, 1=GMSK 9K6
    'VHF1RX' / enum_150,  # 0=AFSK 1K2, 1=GMSK 9K6
    'VHF2TF' / common.EvalAdapter('0.001*x', construct.BitsInteger(24)),  # 0.001*x
    'VHF2RF' / common.EvalAdapter('0.001*x', construct.BitsInteger(24)),  # 0.001*x
    'VHF2TX' / enum_150,  # 0=AFSK 1K2, 1=GMSK 9K6
    'VHF2RX' / enum_150,  # 0=AFSK 1K2, 1=GMSK 9K6
    'VHF1SC' / construct.BitsInteger(48),  # bytewise ASCII
    'VHF1SS' / construct.BitsInteger(8),
    'VHF1PR' / construct.BitsInteger(8),
    'VHF2SC' / construct.BitsInteger(48),  # bytewise ASCII
    'VHF2SS' / construct.BitsInteger(8),
    'VHF2PR' / construct.BitsInteger(8),
    'VHF1GC' / construct.BitsInteger(48),  # bytewise ASCII
    'VHF1GS' / construct.BitsInteger(8),
    'VHF1PO' / construct.BitsInteger(8),
    'VHF2GC' / construct.BitsInteger(48),  # bytewise ASCII
    'VHF2GS' / construct.BitsInteger(8),
    'VHF2PO' / construct.BitsInteger(8),
    'VHF1AV' / common.EvalAdapter('0.0000152590219*x', construct.BitsInteger(16)),  # 0.0000152590219*x
    'VHF1RI' / common.EvalAdapter('0.1*x', construct.BitsInteger(16)),  # 0.1*x
    'VHF1EA' / construct.BitsInteger(1),
    'VHF1DF' / enum_0,  # 0=OFF, 1=ON
    'VHF1SF' / enum_0,  # 0=OFF, 1=ON
    'VHF1MF' / enum_0,  # 0=OFF, 1=ON
    'VHF1TP' / construct.BitsInteger(16),
    'VHF2AV' / common.EvalAdapter('0.0000152590219*x', construct.BitsInteger(16)),  # 0.0000152590219*x
    'VHF2RI' / common.EvalAdapter('0.1*x', construct.BitsInteger(16)),  # 0.1*x
    'VHF2EA' / construct.BitsInteger(1),
    'VHF2DF' / enum_0,  # 0=OFF, 1=ON
    'VHF2SF' / enum_0,  # 0=OFF, 1=ON
    'VHF2MF' / enum_0,  # 0=OFF, 1=ON
    'VHF2TP' / construct.BitsInteger(16),
    'VHF1FC' / construct.BitsInteger(48),  # bytewise ASCII
    'VHF1WA' / enum_151,  # 1=ALL, 0=ADDRESSED ONLY
    'VHF1AC' / enum_152,  # 0=ALL FRAMES, 1=SELF FILTER PASSED, 2=SOURCE FILTER PASSED, 3=ALL FILTERS PASSED
    'VHF1DT' / construct.BitsInteger(8),
    'VHF2FC' / construct.BitsInteger(48),  # bytewise ASCII
    'VHF2WA' / enum_151,  # 1=ALL, 0=ADDRESSED ONLY
    'VHF2AC' / enum_152,  # 0=ALL FRAMES, 1=SELF FILTER PASSED, 2=SOURCE FILTER PASSED, 3=ALL FILTERS PASSED
    'VHF2DT' / construct.BitsInteger(8),
    'VHF1AT' / common.EvalAdapter('0.001*x', construct.BitsInteger(24)),  # 0.001*x
    'VHF1AR' / common.EvalAdapter('0.001*x', construct.BitsInteger(24)),  # 0.001*x
    'VHF2AT' / common.EvalAdapter('0.001*x', construct.BitsInteger(24)),  # 0.001*x
    'VHF2AR' / common.EvalAdapter('0.001*x', construct.BitsInteger(24)),  # 0.001*x
    'VHF1ST' / common.EvalAdapter('0.001*x', construct.BitsInteger(24)),  # 0.001*x
    'VHF1CT' / common.EvalAdapter('0.001*x', construct.BitsInteger(24)),  # 0.001*x
    'VHF1GI' / common.EvalAdapter('10*x', construct.BitsInteger(8)),  # 10*x
    'VHF1SL' / common.EvalAdapter('10*x', construct.BitsInteger(8)),  # 10*x
    'VHF2ST' / common.EvalAdapter('0.001*x', construct.BitsInteger(24)),  # 0.001*x
    'VHF2CT' / common.EvalAdapter('0.001*x', construct.BitsInteger(24)),  # 0.001*x
    'VHF2GI' / common.EvalAdapter('10*x', construct.BitsInteger(8)),  # 10*x
    'VHF2SL' / common.EvalAdapter('10*x', construct.BitsInteger(8)),  # 10*x
    '_pad0' / construct.BitsInteger(6),
)

uhf_ext_hk = construct.BitStruct(
    '_name' / construct.Computed('uhf_ext_hk'),
    'name' / construct.Computed('UHF EXT HK'),
    'UHF1TF' / common.EvalAdapter('0.001*x', construct.BitsInteger(24)),  # 0.001*x
    'UHF1RF' / common.EvalAdapter('0.001*x', construct.BitsInteger(24)),  # 0.001*x
    'UHF1TX' / enum_150,  # 0=AFSK 1K2, 1=GMSK 9K6
    'UHF1RX' / enum_150,  # 0=AFSK 1K2, 1=GMSK 9K6
    'UHF2TF' / common.EvalAdapter('0.001*x', construct.BitsInteger(24)),  # 0.001*x
    'UHF2RF' / common.EvalAdapter('0.001*x', construct.BitsInteger(24)),  # 0.001*x
    'UHF2TX' / enum_150,  # 0=AFSK 1K2, 1=GMSK 9K6
    'UHF2RX' / enum_150,  # 0=AFSK 1K2, 1=GMSK 9K6
    'UHF1SC' / construct.BitsInteger(48),  # bytewise ASCII
    'UHF1SS' / construct.BitsInteger(8),
    'UHF1PR' / construct.BitsInteger(8),
    'UHF2SC' / construct.BitsInteger(48),  # bytewise ASCII
    'UHF2SS' / construct.BitsInteger(8),
    'UHF2PR' / construct.BitsInteger(8),
    'UHF1GC' / construct.BitsInteger(48),  # bytewise ASCII
    'UHF1GS' / construct.BitsInteger(8),
    'UHF1PO' / construct.BitsInteger(8),
    'UHF2GC' / construct.BitsInteger(48),  # bytewise ASCII
    'UHF2GS' / construct.BitsInteger(8),
    'UHF2PO' / construct.BitsInteger(8),
    'UHF1AV' / common.EvalAdapter('0.0000152590219*x', construct.BitsInteger(16)),  # 0.0000152590219*x
    'UHF1RI' / common.EvalAdapter('0.1*x', construct.BitsInteger(16)),  # 0.1*x
    'UHF1EA' / construct.BitsInteger(1),
    'UHF1DF' / enum_0,  # 0=OFF, 1=ON
    'UHF1SF' / enum_0,  # 0=OFF, 1=ON
    'UHF1MF' / enum_0,  # 0=OFF, 1=ON
    'UHF1TP' / construct.BitsInteger(16),
    'UHF2AV' / common.EvalAdapter('0.0000152590219*x', construct.BitsInteger(16)),  # 0.0000152590219*x
    'UHF2RI' / common.EvalAdapter('0.1*x', construct.BitsInteger(16)),  # 0.1*x
    'UHF2EA' / construct.BitsInteger(1),
    'UHF2DF' / enum_0,  # 0=OFF, 1=ON
    'UHF2SF' / enum_0,  # 0=OFF, 1=ON
    'UHF2MF' / enum_0,  # 0=OFF, 1=ON
    'UHF2TP' / construct.BitsInteger(16),
    'UHF1FC' / construct.BitsInteger(48),  # bytewise ASCII
    'UHF1WA' / enum_151,  # 1=ALL, 0=ADDRESSED ONLY
    'UHF1AC' / enum_152,  # 0=ALL FRAMES, 1=SELF FILTER PASSED, 2=SOURCE FILTER PASSED, 3=ALL FILTERS PASSED
    'UHF1DT' / construct.BitsInteger(8),
    'UHF2FC' / construct.BitsInteger(48),  # bytewise ASCII
    'UHF2WA' / enum_151,  # 1=ALL, 0=ADDRESSED ONLY
    'UHF2AC' / enum_152,  # 0=ALL FRAMES, 1=SELF FILTER PASSED, 2=SOURCE FILTER PASSED, 3=ALL FILTERS PASSED
    'UHF2DT' / construct.BitsInteger(8),
    'UHF1AT' / common.EvalAdapter('0.001*x', construct.BitsInteger(24)),  # 0.001*x
    'UHF1AR' / common.EvalAdapter('0.001*x', construct.BitsInteger(24)),  # 0.001*x
    'UHF2AT' / common.EvalAdapter('0.001*x', construct.BitsInteger(24)),  # 0.001*x
    'UHF2AR' / common.EvalAdapter('0.001*x', construct.BitsInteger(24)),  # 0.001*x
    'UHF1ST' / common.EvalAdapter('0.001*x', construct.BitsInteger(24)),  # 0.001*x
    'UHF1CX' / common.EvalAdapter('0.001*x', construct.BitsInteger(24)),  # 0.001*x
    'UHF1GI' / common.EvalAdapter('10*x', construct.BitsInteger(8)),  # 10*x
    'UHF1SL' / common.EvalAdapter('10*x', construct.BitsInteger(8)),  # 10*x
    'UHF2ST' / common.EvalAdapter('0.001*x', construct.BitsInteger(24)),  # 0.001*x
    'UHF2CX' / common.EvalAdapter('0.001*x', construct.BitsInteger(24)),  # 0.001*x
    'UHF2GI' / common.EvalAdapter('10*x', construct.BitsInteger(8)),  # 10*x
    'UHF2SL' / common.EvalAdapter('10*x', construct.BitsInteger(8)),  # 10*x
    '_pad0' / construct.BitsInteger(6),
)

s_band_std_hk = construct.BitStruct(
    '_name' / construct.Computed('s_band_std_hk'),
    'name' / construct.Computed('S BAND STD HK'),
    'SBTMAD' / common.EvalAdapter('-128*x**0 +  1*x**1', construct.BitsInteger(8)),  # -128*x^0 +  1*x^1
    'SBTMET' / common.EvalAdapter('-128*x**0 +  1*x**1', construct.BitsInteger(8)),  # -128*x^0 +  1*x^1
    'SBTMZY' / common.EvalAdapter('-128*x**0 +  1*x**1', construct.BitsInteger(8)),  # -128*x^0 +  1*x^1
    'SBRXGN' / construct.BitsInteger(7),
    'SBRXDF' / common.EvalAdapter('-256*x**0 +  1*x**1', construct.BitsInteger(9)),  # -256*x^0 +  1*x^1
    'SBRX0A' / enum_0,  # 0=OFF, 1=ON
    'SBRX1A' / enum_0,  # 0=OFF, 1=ON
    'SBRXSL' / construct.BitsInteger(6),
    'SBRXSY' / enum_153,  # 0=NOT SYNC, 1=SYNC
    'SBRXCU' / enum_154,  # 0=CH0, 1=CH1
    'SBRXSH' / construct.BitsInteger(6),
    'SBOBHW' / enum_36,  # 0=OBDH 1, 1=OBDH 2, 2=OBDH 3, 3=OBDH 4
    'SBRXPL' / construct.BitsInteger(6),
    'SBHKAV' / enum_25,  # 0=NOT AVAILABLE, 1=AVAILABLE
    'SBCFGR' / enum_23,  # 1=TRUE, 0=FALSE
    'SBRSPH' / construct.BitsInteger(6),
    'SBRXST' / construct.BitsInteger(8),
    'SBRXBC' / construct.BitsInteger(32),
    'SBRXEB' / construct.BitsInteger(16),
    'SBTXMD' / enum_155,  # 0=NO MOD, 1=BPSK, 2=QPSK, 3=8PSK, 4=16PSK, 5=32PSK, 6=64PSK, 15=S-BAND EGSE
    'SBTXFC' / enum_156,  # 0=FEC_1_1, 1=FEC_1_2, 2=FEC_2_3, 3=FEC_3_4, 4=FEC_5_6, 5=FEC_7_8
    'SBTX0A' / enum_0,  # 0=OFF, 1=ON
    'SBTX1A' / enum_0,  # 0=OFF, 1=ON
    'SBTXCU' / enum_154,  # 0=CH0, 1=CH1
    '_pad0' / construct.BitsInteger(3),
    'SBTXAT' / common.EvalAdapter('0.1*x', construct.BitsInteger(10)),  # 0.1*x
    'SBVCIN' / common.EvalAdapter('0.011764706*x', construct.BitsInteger(8)),  # 0.011764706*x
    'SBVCAU' / common.EvalAdapter('0.011764706*x', construct.BitsInteger(8)),  # 0.011764706*x
    'SBVCRM' / common.EvalAdapter('0.011764706*x', construct.BitsInteger(8)),  # 0.011764706*x
    'SBVCPT' / common.EvalAdapter('0.011764706*x', construct.BitsInteger(8)),  # 0.011764706*x
    'SBVCPA' / common.EvalAdapter('0.011764706*x', construct.BitsInteger(8)),  # 0.011764706*x
    'SBVCPO' / common.EvalAdapter('0.011764706*x', construct.BitsInteger(8)),  # 0.011764706*x
    'SBECDE' / enum_157,  # 0=NO ERROR, 1=NO START FOUND, 2=NO END FOUND, 3=INVLD IDENT RX, 4=INVLD MSG LEN, 5=NAK RECEIVED, 6=SPI TIMEOUT, 7=TF INVLD CRC, 8=TF FRAME TO SHORT, 9=TF INVLD TC LEN, 10=TF BUFFER FULL, 11=TF FRAME TO LONG, 12=NO HK RECEIVED, 13=TF INVLD VC, 14=TF INVLD SC ID, 15=SPI WR BUF REJ
    'SBECNT' / construct.BitsInteger(4),
    'SBFWSU' / enum_46,  # 1=ENABLED, 0=DISABLED
    'SBSWVR' / enum_23,  # 1=TRUE, 0=FALSE
    'SBDVFR' / enum_23,  # 1=TRUE, 0=FALSE
    'SBUPTM' / common.TimeDeltaAdapter(construct.BitsInteger(13)),
)

s_band_cfg = construct.BitStruct(
    '_name' / construct.Computed('s_band_cfg'),
    'name' / construct.Computed('S BAND CFG'),
    'SBCHWI' / enum_36,  # 0=OBDH 1, 1=OBDH 2, 2=OBDH 3, 3=OBDH 4
    'SBCAVA' / enum_158,  # 0=UNAVAILABLE, 1=AVAILABLE
    'SBCRXC' / enum_159,  # 0=CH 0, 1=CH 1
    'SBCTXC' / enum_159,  # 0=CH 0, 1=CH 1
    'SBCTPR' / enum_42,  # 1=ACTIVATED, 0=DEACTIVATED
    'SBCRPR' / enum_42,  # 1=ACTIVATED, 0=DEACTIVATED
    'SPCRBD' / enum_42,  # 1=ACTIVATED, 0=DEACTIVATED
    'SPCSPF' / common.EvalAdapter('100*x', construct.BitsInteger(8)),  # 100*x
    'SPCHRR' / construct.BitsInteger(8),
    'SPCTMD' / enum_160,  # 0=NO MOD, 1=BPSK, 2=QPSK
    'SPCTFC' / enum_161,  # 0=FEC 1/1, 1=FEC 1/2, 2=FEC 2/3, 3=FEC 3/4, 4=FEC 5/6, 5=FEC 7/8
    'SBCTAG' / common.EvalAdapter('0.1*x', construct.BitsInteger(11)),  # 0.1*x
    'SBCTFQ' / construct.BitsInteger(24),
    'SBCRBE' / enum_162,  # 1=ACCEPT, 0=REJECT
    'SBCRBM' / enum_163,  # 0=ALWAYS, 1=IN SYNC
    'SBCRFQ' / construct.BitsInteger(24),
    'SBCPK1' / construct.BitsInteger(32),
    'SBCPK2' / construct.BitsInteger(32),
    'SBCPK3' / construct.BitsInteger(32),
    'SBCPK4' / construct.BitsInteger(32),
)

ai_std_hk = construct.BitStruct(
    '_name' / construct.Computed('ai_std_hk'),
    'name' / construct.Computed('AI STD HK'),
    'AIJCPU' / common.EvalAdapter('1.587301*x', construct.BitsInteger(6)),  # 1.587301*x
    'AIJGPU' / common.EvalAdapter('6.66666*x', construct.BitsInteger(4)),  # 6.66666*x
    'AIJRAM' / common.EvalAdapter('1.5873*x', construct.BitsInteger(6)),  # 1.5873*x
    'AIJCMD' / construct.BitsInteger(4),
    'AIJECN' / construct.BitsInteger(4),
    'AIJTMP' / common.EvalAdapter('-128*x**0 +  1*x**1', construct.BitsInteger(8)),  # -128*x^0 +  1*x^1
    'AIJPRG' / common.EvalAdapter('0.3922*x', construct.BitsInteger(8)),  # 0.3922*x
    'AIJPWR' / common.EvalAdapter('78.43137254901961*x', construct.BitsInteger(8)),  # 78.43137254901961*x
    'AIJUPT' / common.TimeDeltaAdapter(construct.BitsInteger(12)),
    'AIJRSC' / construct.BitsInteger(4),
    'AIJECO' / enum_164,  # 0=NO ERROR, 1=UNKNOWN TC, 2=INVALID_TC, 3=PROCESS ALREADY RUN, 4=PROCESS NOT RUNNING, 13=DB INIT ERROR, 14=DB FAILED QUERY, 15=DB NO ENTRY, 16=DB RESULT EXISTS, 17=DB WRITE ERRIR, 18=DB READ ERROR, 19=DB NO CONFIG, 20=DB MISSING TABLE, 21=DL DIR ERROR, 22=DL FILE ERROR, 23=TAR ERROR, 24=PACKET OOB, 25=CAN UD INV STATE, 26=CAN UD INIT ERR, 27=CAN UD FORMAT, 28=CAN WRITE ERROR, 29=WRONG CRC, 30=UL_FILE_ERROR, 31=SPI_CMD_ERROR, 32=SPI_INIT_ERRROR, 5=NO_PROCESS_RUNNING, 6=PROCESS_FAILED_START, 7=PROCESS_CRASHED, 8=PROCESS_TIMEDOUT, 9=PROCESS_WRITE_ERROR, 10=PROCESS_READ_ERROR, 11=PROCESS_UKN_ERROR, 12=PROCESS_STDERR_OUTPU, 33=DB_SUCCESS, 34=DIR_NOT_EXIST, 35=SUCCESS
    'AIJPCT' / construct.BitsInteger(2),
    'AIJPER' / enum_165,  # 5=NO PROCESS RUNNING, 7=PROCESS CRASHED, 8=PROCESS TIMEOUT, 9=PROCESS WRITE ERR, 10=PROCESS READ ERR, 11=PROCESS UKN ERR, 12=STDERR OUTPUT, 6=PROCESS FAILED START, 0=NO ERROR
    'AIJPID' / enum_166,  # 0=NO_PROCESS, 1=CAM_APP, 2=WIDE_SEG, 3=NEAR_SEG, 4=OBJECT_DET, 5=ANO_DET, 6=LIGHTNING, 9=BASH
    'AIKSPC' / common.EvalAdapter('250.0343327992676*x', construct.BitsInteger(16)),  # 250.0343327992676*x
    'AIJRID' / construct.BitsInteger(16),
    'AIJGFR' / common.EvalAdapter('25.879032258064*x', construct.BitsInteger(5)),  # 25.879032258064*x
    'AIJSWP' / common.EvalAdapter('14.2857142857*x', construct.BitsInteger(3)),  # 14.2857142857*x
    'AIJRTP' / enum_167,  # 0=LOG ONLY, 1=IMAGES, 2=VIDEOS, 3=IMAGE SEG PAIRS
    'AIJRFL' / construct.BitsInteger(10),
    'AIJBUS' / enum_99,  # 0=BUS 1, 1=BUS 2
    'AIJAVA' / enum_25,  # 1=AVAILABLE, 0=NOT AVAILABLE
    'AIJFSZ' / construct.BitsInteger(32),
    'AIJFTA' / enum_168,  # 1=ARMED, 0=IDLE
    'AIMUPT' / common.TimeDeltaAdapter(construct.BitsInteger(16)),
    'AIMERR' / enum_169,  # 0=NO ERROR, 10=UART INIT, 1=HAL ERROR, 2=TEST ERROR, 3=FLASH INIT, 4=FLASH CORRUPT, 5=CAN SEND, 6=CAN RECV, 7=SPI SEND, 8=SPI RECV, 9=NO SUCH CMD, 11=CAN INIT, 12=APP CRASHED, 13=OS CRASHED, 14=TC BUF FULL, 15=TOO MANY REBOOTS, 16=FORCE POWEROFF, 17=FORCE POWERCYCLE, 18=UNEXPECTED STATE, 19=CMD PARAMETER, 20=NO MMC IF JETSON ON, 21=MMC TRANSFER TIMEOUT, 22=MMC CRC TIMEOUT, 23=MMC CRC FAIL, 24=CFG ERASE, 25=CFG WRITE, 26=CFG CRC, 27=CFG SIZE, 28=NO CFG FOUND, 29=MMC READ, 30=MMC WRITE, 31=CRC SUCCESS, 32=CMD TOO LONG, 33=CMD CRC FAIL, 35=CMD SUCCESS, 34=CMD TIMEOUT, 36=CRC INIT FAIL, 37=COPY SUCCESS
    'AIMCMD' / construct.BitsInteger(4),
    'AIMECN' / construct.BitsInteger(4),
    'AIMSTE' / enum_170,  # 0=APP RUN, 1=APP CHECK, 2=APP CRASH, 3=OS CHECK, 4=OS CRASH, 5=OS REBOOT, 6=PWR ON, 7=BOOT, 8=OS SHUTDOWN, 9=FORCE PWR OFF, 10=POWER CYCLE, 11=JETSON STARTUP, 12=CMD EXEC
    'AIMM1S' / enum_171,  # 0=ERROR, 1=GOOD
    'AIMM2S' / enum_171,  # 0=ERROR, 1=GOOD
    'AIMMUX' / enum_172,  # 0=JETSON, 1=STM
    'AIMAVA' / enum_25,  # 1=AVAILABLE, 0=NOT AVAILABLE
    'AIMCPS' / enum_173,  # 0=IDLE, 1=COPY, 2=CRC CHECK, 3=CMD EXEC
    'AIMCPP' / common.EvalAdapter('1.587301*x', construct.BitsInteger(6)),  # 1.587301*x
    'AIMBUS' / enum_99,  # 0=BUS 1, 1=BUS 2
    'AIMBKR' / enum_174,  # 0=PRIMARY, 1=BACKUP
    'AIMBIM' / enum_175,  # 0=INTERNAL, 1=MMC 1, 2=MMC 1 Read Only
    'AIMABT' / enum_46,  # 1=ENABLED, 0=DISABLED
    'AIMAAC' / enum_46,  # 1=ENABLED, 0=DISABLED
    'AIMRES' / construct.BitsInteger(1),
)

ai_cam_app_std_hk = construct.BitStruct(
    '_name' / construct.Computed('ai_cam_app_std_hk'),
    'name' / construct.Computed('AI CAM APP STD HK'),
    'CAMUPT' / common.TimeDeltaAdapter(construct.BitsInteger(16)),
    'CAMCOC' / construct.BitsInteger(4),
    'CAMERC' / construct.BitsInteger(4),
    'CAMECO' / enum_176,  # 0=NO ERROR, 1=CAN INIT FAIL, 2=CAN IS NULLPTR, 3=CAN UNKNOWN RX, 4=TC INVLD CMD LEN, 5=TC INVLD CMD CODE, 6=TC INVLD CMD PARAM, 7=CFG NOT EXISTING, 8=SOCKET DISCONNECTED, 9=SOCKET ERROR, 10=SOCKET IS NULLPTR, 11=SOCKET NOT CONNECTED, 12=TCP WRITE FAIL, 13=RESULT DIR EXISTS, 14=DIR CREATION FAIL, 15=LOG CREATION FAIL, 16=CAM CFG LOAD FAIL, 17=CAM INIT FAIL, 18=CAM CMD FAIL, 19=CAM IMG SAVE FAIL, 20=CAM IMG GRAB FAIL, 21=CAM START FAIL, 22=CAM STOP FAIL, 23=TASK ALREADY RUNNING, 24=EXP NOT STARTED, 25=EXP ALREADY STARTED, 26=TASK_STILL_RUNNING, 27=CAM_IFACE_NO_ERROR, 28=CAM_IFACE_INVALID, 29=CAM_IF_ALRDY_RUNS, 30=CAM_IF_START_FAIL, 31=CAM_IF_PROP_SET_FAIL, 32=CAM_IF_NOT_STARTED, 33=CAM_IF_STOP_FAILED, 34=CAM_IF_WRONG_MODE, 35=CAM_IF_INV_IN_DATA, 36=CAM_IF_CAPT_TIMEOUT, 37=CAM_IF_NOT_LOADED, 38=CAM_IF_NO_CFG_FILE, 39=CAM_IF_FAIL_OPEN_CFG, 40=CAM_IF_CFG_WRTE_FAIL, 41=CAM_IF_INVAL_CAN_ID, 42=CAM_IF_INVAL_LENGTH, 43=CAM_IF_INVAL_CODE, 44=CAM_IF_INVALID_PARA, 45=CAM_IF_SCKT_OP_FAIL, 46=CAM_IF_BND_SCKT_FAIL, 47=CAM_
    'CAMTCS' / enum_177,  # 1=CONNECTED, 0=DISCONNECTED
    'CAMAVA' / enum_25,  # 1=AVAILABLE, 0=NOT AVAILABLE
    'CAMWMM' / enum_178,  # 0=IDLE, 1=CONTINUOUS, 2=TRIGGER, 3=VIDEO
    'CAMNMM' / enum_178,  # 0=IDLE, 1=CONTINUOUS, 2=TRIGGER, 3=VIDEO
    'CAMWCM' / enum_178,  # 0=IDLE, 1=CONTINUOUS, 2=TRIGGER, 3=VIDEO
    'CAMNCM' / enum_178,  # 0=IDLE, 1=CONTINUOUS, 2=TRIGGER, 3=VIDEO
    'CAMIFS' / enum_75,  # 0=NOT INITIALIZED, 1=INITIALIZED
    'CAMTSS' / enum_179,  # 1=RUNNING, 0=FINISHED
    'CAMEXS' / enum_180,  # 1=STARTED, 0=STOPPED
    'CAMIMM' / enum_181,  # 0=ONE_SHOT, 1=PRE_CALC
    'CAMTTY' / enum_182,  # 0=NONE, 1=IMAGE CAPTURE, 2=SINGLE TIMED CAPTURE, 3=DUAL TIMED CAPTURE, 4=QUAD TIMED CAPTURE, 5=MATCHED IMAGE CPTRE, 6=MATCHED TIMED CPTRE
    'CAMTPS' / common.EvalAdapter('0.39215686274509803*x', construct.BitsInteger(8)),  # 0.39215686274509803*x
    'CAMRTP' / enum_183,  # 0=LOG_ONLY, 1=SINGLE_IMAGES, 2=VIDEOS, 3=IMAGE_SEG_PAIRS, 4=IMAGE_PAIRS
    'CAMWMA' / enum_184,  # 0=AUTO_EXP_OFF, 1=AUTO_EXP_ON
    'CAMNMA' / enum_184,  # 0=AUTO_EXP_OFF, 1=AUTO_EXP_ON
    'CAMWCA' / enum_184,  # 0=AUTO_EXP_OFF, 1=AUTO_EXP_ON
    'CAMNCA' / enum_184,  # 0=AUTO_EXP_OFF, 1=AUTO_EXP_ON
    'CAMRCN' / construct.BitsInteger(16),
    'CAMRID' / construct.BitsInteger(16),
    'CAMWMG' / common.EvalAdapter('1*x', construct.BitsInteger(8)),  # 1*x
    'CAMNMG' / common.EvalAdapter('1*x', construct.BitsInteger(8)),  # 1*x
    'CAMWCG' / common.EvalAdapter('1*x', construct.BitsInteger(8)),  # 1*x
    'CAMNCG' / common.EvalAdapter('1*x', construct.BitsInteger(8)),  # 1*x
    '_pad0' / construct.BitsInteger(8),
    'CAMWME' / common.EvalAdapter('1*x', construct.BitsInteger(16)),  # 1*x
    'CAMNME' / common.EvalAdapter('1*x', construct.BitsInteger(16)),  # 1*x
    'CAMWCE' / common.EvalAdapter('1*x', construct.BitsInteger(16)),  # 1*x
    'CAMNCE' / common.EvalAdapter('1*x', construct.BitsInteger(16)),  # 1*x
)

ai_ws_app_std_hk = construct.BitStruct(
    '_name' / construct.Computed('ai_ws_app_std_hk'),
    'name' / construct.Computed('AI WS APP STD HK'),
    'AIWSUP' / common.TimeDeltaAdapter(construct.BitsInteger(16)),
    'AIWSTC' / construct.BitsInteger(4),
    'AIWSER' / construct.BitsInteger(4),
    'AIWSEC' / enum_185,  # 0=NO_ERROR, 4=OVERFLOW, 6=ALREADY EXISTS, 8=DOES_NOT_EXIST, 9=MODEL_NOT_INIT, 11=MODEL_NOT EXIST
    'AIWSCA' / construct.BitsInteger(16),
    'AIWSCS' / construct.BitsInteger(4),
    'AIWSAS' / enum_186,  # 0=NOT_LOADED, 1=LOADING, 2=READY, 3=BUSY
    'AIWSEP' / common.EvalAdapter('1*x', construct.BitsInteger(8)),  # 1*x
    'AIWSIC' / construct.BitsInteger(8),
    'AIWSRI' / construct.BitsInteger(8),
    'AIWSRT' / enum_167,  # 0=LOG ONLY, 1=IMAGES, 2=VIDEOS, 3=IMAGE SEG PAIRS
    'AIWSNF' / construct.BitsInteger(12),
    'AIWSSP' / common.EvalAdapter('1*x', construct.BitsInteger(8)),  # 1*x
    'AIWSCP' / common.EvalAdapter('1*x', construct.BitsInteger(8)),  # 1*x
    'AIWSLP' / common.EvalAdapter('1*x', construct.BitsInteger(8)),  # 1*x
    'AIWSWP' / common.EvalAdapter('1*x', construct.BitsInteger(8)),  # 1*x
    'AIWSNP' / common.EvalAdapter('1*x', construct.BitsInteger(8)),  # 1*x
    'AIWSFP' / common.EvalAdapter('1*x', construct.BitsInteger(8)),  # 1*x
    'AIWS1A' / enum_46,  # 0=DISABLED, 1=ENABLED
    'AIWS2A' / enum_46,  # 0=DISABLED, 1=ENABLED
    'AIWSBA' / enum_46,  # 0=DISABLED, 1=ENABLED
    'AIWSFA' / enum_46,  # 0=DISABLED, 1=ENABLED
    'AIWSGA' / enum_46,  # 0=DISABLED, 1=ENABLED
    'AIWSHA' / enum_46,  # 0=DISABLED, 1=ENABLED
    'AIWSSA' / enum_46,  # 0=DISABLED, 1=ENABLED
    'AIWSKI' / enum_75,  # 0=NOT INITIALIZED, 1=INITIALIZED
    'AIWSLM' / enum_187,  # 0=0 - TEST, 1=1 - OLED, 2=2 - TEST CNTD, 3=3 - OLED CNTD, 4=4 - EVRTH
)

ai_ns_app_std_hk = construct.BitStruct(
    '_name' / construct.Computed('ai_ns_app_std_hk'),
    'name' / construct.Computed('AI NS APP STD HK'),
    'AINSUP' / common.TimeDeltaAdapter(construct.BitsInteger(16)),
    'AINSTC' / construct.BitsInteger(4),
    'AINSER' / construct.BitsInteger(4),
    'AINSEC' / enum_185,  # 0=NO_ERROR, 4=OVERFLOW, 6=ALREADY EXISTS, 8=DOES_NOT_EXIST, 9=MODEL_NOT_INIT, 11=MODEL_NOT EXIST
    'AINSCA' / construct.BitsInteger(16),
    'AINSCS' / construct.BitsInteger(4),
    'AINSAS' / enum_186,  # 0=NOT_LOADED, 1=LOADING, 2=READY, 3=BUSY
    'AINSEP' / common.EvalAdapter('1*x', construct.BitsInteger(8)),  # 1*x
    'AINSIC' / construct.BitsInteger(8),
    'AINSRI' / construct.BitsInteger(8),
    'AINSRT' / enum_167,  # 0=LOG ONLY, 1=IMAGES, 2=VIDEOS, 3=IMAGE SEG PAIRS
    'AINSNF' / construct.BitsInteger(12),
    'AINSCL' / common.EvalAdapter('1*x', construct.BitsInteger(8)),  # 1*x
    'AINSFP' / common.EvalAdapter('1*x', construct.BitsInteger(8)),  # 1*x
    'AINSGL' / common.EvalAdapter('1*x', construct.BitsInteger(8)),  # 1*x
    'AINSSP' / common.EvalAdapter('1*x', construct.BitsInteger(8)),  # 1*x
    'AINSWP' / common.EvalAdapter('1*x', construct.BitsInteger(8)),  # 1*x
    'AINSWL' / common.EvalAdapter('1*x', construct.BitsInteger(8)),  # 1*x
    'AINSTP' / common.EvalAdapter('1*x', construct.BitsInteger(8)),  # 1*x
    'AINSAP' / common.EvalAdapter('1*x', construct.BitsInteger(8)),  # 1*x
    'AINSBP' / common.EvalAdapter('1*x', construct.BitsInteger(8)),  # 1*x
    'AINSIP' / common.EvalAdapter('1*x', construct.BitsInteger(8)),  # 1*x
    'AINSCP' / common.EvalAdapter('1*x', construct.BitsInteger(8)),  # 1*x
    'AINS1A' / enum_46,  # 0=DISABLED, 1=ENABLED
    'AINS2A' / enum_46,  # 0=DISABLED, 1=ENABLED
    'AINSBA' / enum_46,  # 0=DISABLED, 1=ENABLED
    'AINSFA' / enum_46,  # 0=DISABLED, 1=ENABLED
    'AINSGA' / enum_46,  # 0=DISABLED, 1=ENABLED
    'AINSHA' / enum_46,  # 0=DISABLED, 1=ENABLED
    'AINSSA' / enum_46,  # 0=DISABLED, 1=ENABLED
    'AINSKI' / enum_75,  # 0=NOT INITIALIZED, 1=INITIALIZED
    'AINSLM' / enum_188,  # 0=0 - SENTINEL, 1=1 - LANDSAT, 2=2 - SENTINEL CNTD, 3=3 - LANDSAT CNTD
)

ai_od_app_std_hk = construct.BitStruct(
    '_name' / construct.Computed('ai_od_app_std_hk'),
    'name' / construct.Computed('AI OD APP STD HK'),
    'AIODUP' / common.TimeDeltaAdapter(construct.BitsInteger(16)),
    'AIODTC' / construct.BitsInteger(4),
    'AIODER' / construct.BitsInteger(4),
    'AIODEC' / enum_185,  # 0=NO_ERROR, 4=OVERFLOW, 6=ALREADY EXISTS, 8=DOES_NOT_EXIST, 9=MODEL_NOT_INIT, 11=MODEL_NOT EXIST
    'AIODCA' / construct.BitsInteger(16),
    'AIODCS' / construct.BitsInteger(4),
    'AIODAS' / enum_186,  # 0=NOT_LOADED, 1=LOADING, 2=READY, 3=BUSY
    'AIODEP' / construct.BitsInteger(8),
    'AIODIC' / construct.BitsInteger(8),
    'AIODRI' / construct.BitsInteger(8),
    'AIODRT' / enum_167,  # 0=LOG ONLY, 1=IMAGES, 2=VIDEOS, 3=IMAGE SEG PAIRS
    'AIODNF' / construct.BitsInteger(12),
    'AIODWA' / construct.BitsInteger(8),
    'AIODCP' / construct.BitsInteger(8),
    'AIODGP' / construct.BitsInteger(8),
    'AIODIP' / construct.BitsInteger(8),
    'AIODFP' / construct.BitsInteger(8),
    'AIODWL' / construct.BitsInteger(8),
    'AIODR1' / construct.BitsInteger(8),
    'AIODR2' / construct.BitsInteger(8),
    'AIODR3' / construct.BitsInteger(8),
    'AIODR4' / construct.BitsInteger(8),
    'AIODR5' / construct.BitsInteger(8),
    'AIODR6' / construct.BitsInteger(8),
    'AIODR7' / construct.BitsInteger(8),
    'AIODR8' / construct.BitsInteger(8),
    'AIOD1A' / enum_46,  # 0=DISABLED, 1=ENABLED
    'AIOD2A' / enum_46,  # 0=DISABLED, 1=ENABLED
    'AIODBA' / enum_46,  # 0=DISABLED, 1=ENABLED
    'AIODFA' / enum_46,  # 0=DISABLED, 1=ENABLED
    'AIODGA' / enum_46,  # 0=DISABLED, 1=ENABLED
    'AIODHA' / enum_46,  # 0=DISABLED, 1=ENABLED
    'AIODSA' / enum_46,  # 0=DISABLED, 1=ENABLED
    'AIODKI' / enum_75,  # 0=NOT INITIALIZED, 1=INITIALIZED
    'AIODLM' / enum_189,  # 0=COARSE DETECT, 1=FINE DETECT
    'AIODR9' / construct.BitsInteger(8),
)

ai_ad_app_std_hk = construct.BitStruct(
    '_name' / construct.Computed('ai_ad_app_std_hk'),
    'name' / construct.Computed('AI AD APP STD HK'),
    'AIADUP' / common.TimeDeltaAdapter(construct.BitsInteger(16)),
    'AIADTC' / construct.BitsInteger(4),
    'AIADER' / construct.BitsInteger(4),
    'AIADEC' / enum_190,  # 0=NO_ERROR, 4=OVERFLOW, 6=ALREADY EXISTS, 7=SUCCESS, 8=DOES_NOT_EXIST, 9=MODEL_NOT_INIT, 10=TIME_LIMIT, 11=MODEL_NOT EXIST, 12=CLASS_NOT_EXIST, 13=COPY_FAILED
    'AIADCA' / construct.BitsInteger(8),
    'AIADR2' / construct.BitsInteger(1),
    'AIAD1A' / enum_46,  # 0=DISABLED, 1=ENABLED
    'AIAD2A' / enum_46,  # 0=DISABLED, 1=ENABLED
    'AIADBA' / enum_46,  # 0=DISABLED, 1=ENABLED
    'AIADFA' / enum_46,  # 0=DISABLED, 1=ENABLED
    'AIADGA' / enum_46,  # 0=DISABLED, 1=ENABLED
    'AIADHA' / enum_46,  # 0=DISABLED, 1=ENABLED
    'AIADSA' / enum_46,  # 0=DISABLED, 1=ENABLED
    'AIADCS' / construct.BitsInteger(4),
    'AIADAS' / enum_191,  # 0=NOT_LOADED, 1=LOADING, 2=READY, 3=BUSY, 4=TRAINING, 5=LOADING DATASET, 6=TAKING IMAGES
    'AIADPR' / common.EvalAdapter('0.39215686274509803*x', construct.BitsInteger(8)),  # 0.39215686274509803*x
    'AIADIC' / construct.BitsInteger(8),
    'AIADRI' / construct.BitsInteger(16),
    'AIADRT' / enum_167,  # 0=LOG ONLY, 1=IMAGES, 2=VIDEOS, 3=IMAGE SEG PAIRS
    'AIADNF' / construct.BitsInteger(12),
    'AIADLO' / common.EvalAdapter('0.00015259*x', construct.BitsInteger(16)),  # 0.00015259*x
    'AIADAC' / common.EvalAdapter('0.00015259*x', construct.BitsInteger(16)),  # 0.00015259*x
    'AIADSC' / common.EvalAdapter('0.0117647*x', construct.BitsInteger(8)),  # 0.0117647*x
    'AIADIP' / common.EvalAdapter('0.0117647*x', construct.BitsInteger(8)),  # 0.0117647*x
    'AIADEO' / construct.BitsInteger(8),
    'AIADAD' / construct.BitsInteger(4),
    'AIADAM' / construct.BitsInteger(4),
    'AIADIF' / construct.BitsInteger(1),
    'AIADAV' / construct.BitsInteger(1),
    'AIADRS' / construct.BitsInteger(6),
    'AIADDN' / construct.BitsInteger(16),
    'AIADDA' / construct.BitsInteger(16),
)

ai_ld_app_std_hk = construct.BitStruct(
    '_name' / construct.Computed('ai_ld_app_std_hk'),
    'name' / construct.Computed('AI LD APP STD HK'),
    'LDCMDC' / construct.BitsInteger(4),
    'LDERCO' / construct.BitsInteger(4),
    'LDERCD' / enum_192,  # 0=NO ERROR, 1=CAN INIT FAIL, 2=CAN IS NULL, 3=CAN UNKNOWN MSG, 4=TC INVLD CMD LEN, 5=TC INVLD CMD CODE, 6=TC INVLD CMD PARAM, 7=CFG NOT EXISTING, 8=TCP SOCKET DC, 9=TCP SOCKET ERR, 10=TCP SOCKET IS NULL, 11=TCP SOCKET NC, 12=RESULT DIR EXISTS, 13=RESULT DIR FAIL, 14=LOG FILE FAIL, 17=CAM INIT FAIL, 18=CAM IS NULL, 19=IP INIT FAIL, 20=CAM CFG FAIL, 21=CAM START FAIL, 22=CAM STOP FAIL, 23=CAM CMD FAIL, 24=EVENT TOO LONG, 25=EVENT TOO SHORT, 26=CUDA ALLOC FAILED, 27=NO CUDA DEVICE FOUND, 15=INVLD BACK SUB ALGO, 16=LABELING OVERFLOW, 28=DEFECT PIXEL FULL, 29=CFG WRITE FAIL, 30=CFG INVLD SIZE, 31=CFG INVLD CRC, 32=LD ALREADY RUNNING, 33=RESULT DIR DEL FAIL, 34=SUCCESSFUL
    'LDFPSR' / common.EvalAdapter('0.11730205278592376*x', construct.BitsInteger(10)),  # 0.11730205278592376*x
    'LDFWEV' / construct.BitsInteger(16),
    'LDRES2' / enum_25,  # 1=AVAILABLE, 0=NOT AVAILABLE
    'LDTCPS' / enum_177,  # 1=CONNECTED, 0=DISCONNECTED
    'LDIPST' / enum_193,  # 1=RUNNING, 0=STOPPED
    'LDRGBU' / enum_46,  # 1=ENABLED, 0=DISABLED
    'LDRES3' / construct.BitsInteger(1),
    'LDFRMC' / construct.BitsInteger(19),
    'LDEVCT' / construct.BitsInteger(12),
    'LDLEFC' / construct.BitsInteger(12),
    'LDLEBG' / construct.BitsInteger(8),
    'LDUPTM' / common.TimeDeltaAdapter(construct.BitsInteger(16)),
    'LDLRES' / construct.BitsInteger(16),
    'LDTLEC' / construct.BitsInteger(8),
    'LDCPRT' / common.EvalAdapter('0.19607843137254902*x', construct.BitsInteger(8)),  # 0.19607843137254902*x
    'LDRDTM' / common.EvalAdapter('0.19607843137254902*x', construct.BitsInteger(8)),  # 0.19607843137254902*x
    'LDGPRT' / common.EvalAdapter('0.19607843137254902*x', construct.BitsInteger(8)),  # 0.19607843137254902*x
    'LDBSAL' / enum_194,  # 0=SIGMA DELTA, 1=GAUSSIAN
    'LDLETP' / enum_195,  # 0=UNKNOWN, 1=LIGHTNING, 2=METEOR
    'LDRGBM' / enum_196,  # 0=IDLE, 1=CONTINUOUS, 2=TRIGGER
    'LDNIRM' / enum_196,  # 0=IDLE, 1=CONTINUOUS, 2=TRIGGER
    'LDTSEC' / construct.BitsInteger(8),
    'LDNIRG' / construct.BitsInteger(4),
    'LDNIRE' / common.EvalAdapter('10*x', construct.BitsInteger(12)),  # 10*x
)

ai_app_07_std_hk = construct.BitStruct(
    '_name' / construct.Computed('ai_app_07_std_hk'),
    'name' / construct.Computed('AI APP 07 STD HK'),
    'AI07D1' / construct.BitsInteger(32),
    'AI07D2' / construct.BitsInteger(32),
    'AI07D3' / construct.BitsInteger(32),
    'AI07D4' / construct.BitsInteger(32),
    'AI07D5' / construct.BitsInteger(32),
    'AI07D6' / construct.BitsInteger(32),
    'AI07D7' / construct.BitsInteger(32),
)

ai_app_08_std_hk = construct.BitStruct(
    '_name' / construct.Computed('ai_app_08_std_hk'),
    'name' / construct.Computed('AI APP 08 STD HK'),
    'AI08D1' / construct.BitsInteger(32),
    'AI08D2' / construct.BitsInteger(32),
    'AI08D3' / construct.BitsInteger(32),
    'AI08D4' / construct.BitsInteger(32),
    'AI08D5' / construct.BitsInteger(32),
    'AI08D6' / construct.BitsInteger(32),
    'AI08D7' / construct.BitsInteger(32),
)

ai_app_09_std_hk = construct.BitStruct(
    '_name' / construct.Computed('ai_app_09_std_hk'),
    'name' / construct.Computed('AI APP 09 STD HK'),
    'AI09D1' / construct.BitsInteger(32),
    'AI09D2' / construct.BitsInteger(32),
    'AI09D3' / construct.BitsInteger(32),
    'AI09D4' / construct.BitsInteger(32),
    'AI09D5' / construct.BitsInteger(32),
    'AI09D6' / construct.BitsInteger(32),
    'AI09D7' / construct.BitsInteger(32),
)

ai_app_10_std_hk = construct.BitStruct(
    '_name' / construct.Computed('ai_app_10_std_hk'),
    'name' / construct.Computed('AI APP 10 STD HK'),
    'AI10D1' / construct.BitsInteger(32),
    'AI10D2' / construct.BitsInteger(32),
    'AI10D3' / construct.BitsInteger(32),
    'AI10D4' / construct.BitsInteger(32),
    'AI10D5' / construct.BitsInteger(32),
    'AI10D6' / construct.BitsInteger(32),
    'AI10D7' / construct.BitsInteger(32),
)

ai_cam_cfg_hk = construct.BitStruct(
    '_name' / construct.Computed('ai_cam_cfg_hk'),
    'name' / construct.Computed('AI CAM CFG HK'),
    'AICCET' / construct.BitsInteger(20),
    'AICCIC' / enum_23,  # 0=FALSE, 1=TRUE
    'AICCAG' / enum_46,  # 0=DISABLED, 1=ENABLED
    'AICCAE' / enum_46,  # 0=DISABLED, 1=ENABLED
    'AICCAO' / enum_46,  # 0=DISABLED, 1=ENABLED
    'AICCBL' / construct.BitsInteger(9),
    'AICCGN' / common.EvalAdapter('0.1*x', construct.BitsInteger(9)),  # 0.1*x
    'AICCOX' / construct.BitsInteger(11),
    'AICCOY' / construct.BitsInteger(11),
    'AICCCN' / common.EvalAdapter('-64*x**0 +  1*x**1', construct.BitsInteger(9)),  # -64*x^0 +  1*x^1
    'AICCGM' / common.EvalAdapter('-8*x**0 +  0.01*x**1', construct.BitsInteger(11)),  # -8*x^0 +  0.01*x^1
    'AICCST' / common.EvalAdapter('0.01*x', construct.BitsInteger(9)),  # 0.01*x
    'AICCWE' / enum_46,  # 1=ENABLED, 0=DISABLED
    'AICCWA' / enum_46,  # 1=ENABLED, 0=DISABLED
    'AICCHU' / common.EvalAdapter('-180*x**0 +  1*x**1', construct.BitsInteger(9)),  # -180*x^0 +  1*x^1
    'AICCWR' / construct.BitsInteger(8),
    'AICCWG' / construct.BitsInteger(8),
    'AICCWB' / construct.BitsInteger(8),
    'AICCGU' / common.EvalAdapter('0.1*x', construct.BitsInteger(9)),  # 0.1*x
    'AICCTB' / common.EvalAdapter('0.01*x', construct.BitsInteger(7)),  # 0.01*x
    'AICCGL' / common.EvalAdapter('0.1*x', construct.BitsInteger(9)),  # 0.1*x
    'AICCFR' / construct.BitsInteger(7),
    'AICCEA' / construct.BitsInteger(8),
    'AICCTI' / common.EvalAdapter('-8*x**0 +  0.01*x**1', construct.BitsInteger(11)),  # -8*x^0 +  0.01*x^1
    'AICCLA' / enum_46,  # 1=ENABLED, 0=DISABLED
    'AICCTM' / enum_46,  # 1=ENABLED, 0=DISABLED
    'AICCHT' / construct.BitsInteger(11),
    'AICCEL' / construct.BitsInteger(20),
    'AICCEU' / construct.BitsInteger(20),
    'AICCDN' / construct.BitsInteger(4),
    'AICCSH' / construct.BitsInteger(4),
    'AICCCT' / enum_197,  # 0=WIDE MONO, 1=NARROW MONO, 2=WIDE RGB, 3=NARROW RGB
    'AICCAV' / enum_25,  # 1=AVAILABLE, 0=NOT AVAILABLE
    'AICCHR' / enum_46,  # 1=ENABLED, 0=DISABLED
    'AICCR1' / construct.BitsInteger(1),
    'AICCWT' / construct.BitsInteger(11),
    'AICCAF' / enum_198,  # 0=DEFAULT_0, 1=DEFAULT_1, 2=DEFAULT_2, 3=CAMERA_APP_1, 4=CAMERA_APP_2, 5=CAMERA_APP_3, 6=WIDE_SEGMENTATION_1, 7=WIDE_SEGMENTATION_2, 8=WIDE_SEGMENTATION_3, 9=NEAR_SEGMENTATION_1, 10=NEAR_SEGMENTATION_2, 11=NEAR_SEGMENTATION_3, 12=OBJECT_DETECTION_1, 13=OBJECT_DETECTION_2, 14=OBJECT_DETECTION_3, 15=ANOMALIEDETECTION_1, 16=ANOMALIEDETECTION_2, 17=ANOMALIEDETECTION_3, 18=LIGHT_DETECTION_1, 19=LIGHT_DETECTION_2, 20=LIGHT_DETECTION_3, 21=APP_7_1, 22=APP_7_2, 23=APP_7_3, 24=APP_8_1, 25=APP_8_2, 26=APP_8_3, 27=GENERIC_SHELL_1, 28=GENERIC_SHELL_2, 29=GENERIC_SHELL_3, 30=FREE_1, 31=FREE_2
    'AICCSN' / construct.BitsInteger(27),
)

ai_app_ld_cfg_hk = construct.BitStruct(
    '_name' / construct.Computed('ai_app_ld_cfg_hk'),
    'name' / construct.Computed('AI APP LD CFG HK'),
    'LDCOFX' / common.EvalAdapter('-2048*x**0 +  1*x**1', construct.BitsInteger(12)),  # -2048*x^0 +  1*x^1
    'LDCOFY' / common.EvalAdapter('-2048*x**0 +  1*x**1', construct.BitsInteger(12)),  # -2048*x^0 +  1*x^1
    'LDCRBC' / construct.BitsInteger(16),
    'LDCFBE' / construct.BitsInteger(8),
    'LDCFAE' / construct.BitsInteger(8),
    'LDCDIR' / construct.BitsInteger(4),
    'LDCERR' / construct.BitsInteger(4),
    'LDCBSM' / construct.BitsInteger(8),
    'LDCLDS' / construct.BitsInteger(12),
    'LDCUDS' / construct.BitsInteger(12),
    'LDCLED' / construct.BitsInteger(12),
    'LDCUED' / construct.BitsInteger(12),
    'LDCAVA' / enum_25,  # 1=AVAILABLE, 0=NOT AVAILABLE
    'LDCURC' / enum_46,  # 1=ENABLED, 0=DISABLED
    'LDCMTI' / enum_46,  # 0=DISABLED, 1=ENABLED
    'LDCRES' / construct.BitsInteger(3),
    'LDCBSA' / enum_194,  # 0=SIGMA DELTA, 1=GAUSSIAN
    'LDCMAF' / construct.BitsInteger(16),
    'LDCBOV' / construct.BitsInteger(8),
    'LDCEMR' / construct.BitsInteger(8),
    'LDCSDL' / construct.BitsInteger(8),
    'LDCSDU' / construct.BitsInteger(8),
    'LDCSDT' / construct.BitsInteger(8),
    'LDCSDN' / construct.BitsInteger(8),
    'LDCGAA' / common.EvalAdapter('0.00392156862745098*x', construct.BitsInteger(8)),  # 0.00392156862745098*x
    'LDCGAK' / common.EvalAdapter('0.0015259021896696422*x', construct.BitsInteger(16)),  # 0.0015259021896696422*x
    'LDCDAC' / construct.BitsInteger(16),
    'LDCRS2' / construct.BitsInteger(16),
)

ai_cam_img_match_cfg = construct.BitStruct(
    '_name' / construct.Computed('ai_cam_img_match_cfg'),
    'name' / construct.Computed('AI CAM IMG MATCH CFG'),
    'AIIMCR' / enum_46,  # 1=ENABLED, 0=DISABLED
    'AIIMMM' / construct.BitsInteger(4),
    'AIIMDT' / construct.BitsInteger(8),
    'AIIMDR' / common.EvalAdapter('0*x**0 +  0.1*x**1', construct.BitsInteger(8)),  # 0*x^0 +  0.1*x^1
    'AIIM11' / common.EvalAdapter('-1*x**0 +  0.01*x**1', construct.BitsInteger(16)),  # -1*x^0 +  0.01*x^1
    'AIIM33' / common.EvalAdapter('0*x**0 +  1*x**1', construct.BitsInteger(3)),  # 0*x^0 +  1*x^1
    'AIIM31' / common.EvalAdapter('0*x**0 +  1*x**1', construct.BitsInteger(3)),  # 0*x^0 +  1*x^1
    'AIIM32' / common.EvalAdapter('0*x**0 +  1*x**1', construct.BitsInteger(3)),  # 0*x^0 +  1*x^1
    'AIIM12' / common.EvalAdapter('-1*x**0 +  0.01*x**1', construct.BitsInteger(16)),  # -1*x^0 +  0.01*x^1
    'AIIMOP' / enum_199,  # 1=PRE CALC, 0=ONE SHOT
    'AIIMAV' / construct.BitsInteger(1),
    'AIIM13' / common.EvalAdapter('0.01*x**1 +  -100*x**0', construct.BitsInteger(16)),  # 0.01*x^1 +  -100*x^0
    'AIIM21' / common.EvalAdapter('0.001*x**1 +  -1*x**0', construct.BitsInteger(16)),  # 0.001*x^1 +  -1*x^0
    'AIIM22' / common.EvalAdapter('0.001*x**1 +  -1*x**0', construct.BitsInteger(16)),  # 0.001*x^1 +  -1*x^0
    'AIIM23' / common.EvalAdapter('0.01*x**1 +  -100*x**0', construct.BitsInteger(16)),  # 0.01*x^1 +  -100*x^0
)

mview_std_hk = construct.BitStruct(
    '_name' / construct.Computed('mview_std_hk'),
    'name' / construct.Computed('MVIEW STD HK'),
    'MVE1DG' / enum_200,  # 16=SM TC LEN IVLD, 17=SM STATE FOR TC IVLD, 18=SM CMD CODE UNKOWN, 19=SM TC PARAM IVLD, 20=SM TC CAN RX BUF FUL, 21=SM CAN MSG TOO SHORT, 22=SM CAN BUS ERR, 23=SM TC NOT IMPL, 24=SM CAN BUS TIMEOUT, 25=SM CALIB MODE IVLD, 32=SM FLSH OP ERR, 33=SM FLSH CFG ERR, 34=SM FLSH CRC IVLD, 40=SM PARAM ID UNKOWN, 41=SM PARAM VALUE IVLD, 42=SM CAT RING LIMIT, 128=ZE TC IVLD, 129=ZE TC LEN IVLD, 130=ZE STATE FOR TC IVLD, 131=ZE CMD CODE UNKOWN, 132=ZE TC PARAM IVLD, 133=ZE TC CAN RX BUF FUL, 134=ZE CAN BUS ERR, 0=MV NO ERR, 135=ZE TC NOT IMPL, 136=ZE INVLD DEBUG MODE, 144=ZE FLSH OP ERR, 145=ZE FLSH OP LEN IVLD, 146=ZE FLSH CFG ERR, 147=ZE FLSH CRC IVLD, 160=ZE NO SM ACTIVE, 161=ZE SM ID NOT RESP, 162=ZE SM ID NO ACT MASK, 163=ZE SM ID MARK DEFECT, 164=ZE SM ID IVLD, 168=ZE NO MCU COORDIN, 169=ZE BOTH MCU COORDIN, 176=ZE OTHR MCU NOT RESP, 177=ZE UART COMM ERR, 178=ZE UART PKG LEN IVLD, 179=ZE UART CRC IVLD, 180=ZE UART TC UNKOWN, 181=ZE UART PARAM IVLD, 182=ZE UART RX BUF FUL, 192=ZE HAL ERR HANDLER, 137=ZE TC CAN ID U
    'MVE1DI' / construct.BitsInteger(16),
    'MVE1CT' / construct.BitsInteger(4),
    'MVZ1RC' / construct.BitsInteger(4),
    'MVZ1RO' / enum_201,  # 0=COORDINATOR, 1=FORWARDER
    'MVZ1ST' / enum_202,  # 0=ZE_IDLE, 1=ZE_ATTI_DET, 2=ZE_SM_CHANGE, 3=ZE_IMG_CAPT_GRAB, 4=ZE_CTLG_OP, 5=ZE_SM_SW_APPLY, 6=ZE_DATA_UPL_DWNL, 7=ZE_RELAY
    'MVZ1CC' / construct.BitsInteger(4),
    'MVZ1HI' / construct.BitsInteger(1),
    'MVZ1PE' / enum_0,  # 0=OFF, 1=ON
    'MVZ1UI' / enum_203,  # 0=UART IF 1, 1=UART IF 2
    'MVZ1OR' / enum_204,  # 1=RESPONDING, 0=NOT RESPONDING
    'MVE2DG' / enum_205,  # 16=SM TC LEN IVLD, 17=SM STATE FOR TC IVLD, 18=SM CMD CODE UNKOWN, 19=SM TC PARAM IVLD, 20=SM TC CAN RX BUF FUL, 21=SM CAN MSG TOO SHORT, 22=SM CAN BUS ERR, 23=SM TC NOT IMPL, 24=SM CAN BUS TIMEOUT, 25=SM CALIB MODE IVLD, 32=SM FLSH OP ERR, 33=SM FLSH CFG ERR, 34=SM FLSH CRC IVLD, 40=SM PARAM ID UNKOWN, 41=SM PARAM VALUE IVLD, 42=SM CAT RING LIMIT, 128=ZE TC IVLD, 129=ZE TC LEN IVLD, 130=ZE STATE FOR TC IVLD, 131=ZE CMD CODE UNKOWN, 132=ZE TC PARAM IVLD, 133=ZE TC CAN RX BUF FUL, 134=ZE CAN BUS ERR, 0=MV NO ERR, 135=ZE TC NOT IMPL, 136=ZE INVLD DEBUG MODE, 144=ZE FLSH OP ERR, 145=ZE FLSH OP LEN IVLD, 146=ZE FLSH CFG ERR, 147=ZE FLSH CRC IVLD, 160=ZE NO SM ACTIVE, 161=ZE SM ID NOT RESP, 162=ZE SM ID NO ACT MASK, 163=ZE SM ID MARK DEFECT, 164=ZE SM ID IVLD, 168=ZE NO MCU COORDIN, 169=ZE BOTH MCU COORDIN, 176=ZE OTHR MCU NOT RESP, 177=ZE UART COMM ERR, 178=ZE UART PGK LEN IVLD, 179=ZE UART CRC IVLD, 180=ZE UART TC UNKOWN, 181=ZE UART PARAM IVLD, 182=ZE UART RX BUF FUL, 192=ZE HAL ERR HANDLER, 137=ZE TC CAN ID U
    'MVE2DI' / construct.BitsInteger(16),
    'MVE2CT' / construct.BitsInteger(4),
    'MVZ2RC' / construct.BitsInteger(4),
    'MVZ2RO' / enum_201,  # 0=COORDINATOR, 1=FORWARDER
    'MVZ2ST' / enum_202,  # 0=ZE_IDLE, 1=ZE_ATTI_DET, 2=ZE_SM_CHANGE, 3=ZE_IMG_CAPT_GRAB, 4=ZE_CTLG_OP, 5=ZE_SM_SW_APPLY, 6=ZE_DATA_UPL_DWNL, 7=ZE_RELAY
    'MVZ2CC' / construct.BitsInteger(4),
    'MVZ2HI' / construct.BitsInteger(1),
    'MVZ2PE' / enum_0,  # 0=OFF, 1=ON
    'MVZ2UI' / enum_203,  # 0=UART IF 1, 1=UART IF 2
    'MVZ2OR' / enum_204,  # 1=RESPONDING, 0=NOT RESPONDING
    'MVSMST' / enum_206,  # 0=SM_SLEEP, 16=SM_AD, 48=SM_DEL_FLASH, 49=SM_FLASH_COPY, 50=SM_CALC_CRC32, 53=SM_REPAIR_HIP, 54=SM_CALC_VEC_DB, 51=SM_RECV_WRITE_CAT, 40=SM_IMG_CAPTURE, 57=SM_CHECK_VEC_DB
    'MVSMAC' / enum_207,  # 0=OFF, 1=ON, 2=AUTO, 3=ILLIGAL_AC_MODE
    'MVSTEM' / common.EvalAdapter('-50*x**0 +  0.7843137255*x**1', construct.BitsInteger(8)),  # -50*x^0 +  0.7843137255*x^1
    'MVS1MK' / construct.BitsInteger(1),
    'MVS2MK' / construct.BitsInteger(1),
    'MVS3MK' / construct.BitsInteger(1),
    'MVS4MK' / construct.BitsInteger(1),
    'MVS1DF' / construct.BitsInteger(1),
    'MVS2DF' / construct.BitsInteger(1),
    'MVS3DF' / construct.BitsInteger(1),
    'MVS4DF' / construct.BitsInteger(1),
    'MVS1PE' / construct.BitsInteger(1),
    'MVS2PE' / construct.BitsInteger(1),
    'MVS3PE' / construct.BitsInteger(1),
    'MVS4PE' / construct.BitsInteger(1),
    'MVADMD' / enum_208,  # 0=AD_SYNC_PIN, 1=AD_AUTO_TRIG
    '_pad0' / construct.BitsInteger(3),
    'MVASID' / construct.BitsInteger(3),
    'MVADVA' / construct.BitsInteger(1),
    'MVASRY' / enum_209,  # 0=RDY, 1=NONE RDY
    'MVADEC' / enum_210,  # 0=AD NO ERR, 1=AD NO 3 STARS, 2=AD NO CENTER STAR, 3=AD NO NEIGH STAR1, 4=AD NO NEIGH STAR2, 5=AD TOO BIG OBJECT, 6=AD TOO BRIGHT
    '_pad1' / construct.BitsInteger(8),
    'MVAQ1N' / common.EvalAdapter('-1*x**0 +  0.00003051804*x**1', construct.BitsInteger(16)),  # -1*x^0 +  0.00003051804*x^1
    'MVAQ2N' / common.EvalAdapter('-1*x**0 +  0.00003051804*x**1', construct.BitsInteger(16)),  # -1*x^0 +  0.00003051804*x^1
    'MVAQ3N' / common.EvalAdapter('-1*x**0 +  0.00003051804*x**1', construct.BitsInteger(16)),  # -1*x^0 +  0.00003051804*x^1
)

mview_cfg_hk = construct.BitStruct(
    '_name' / construct.Computed('mview_cfg_hk'),
    'name' / construct.Computed('MVIEW CFG HK'),
    'MVCZUE' / construct.BitsInteger(8),
    'MVCZMR' / construct.BitsInteger(8),
    'MVCZCC' / construct.BitsInteger(24),
    'MVCZCI' / construct.BitsInteger(24),
    'MVCZCS' / construct.BitsInteger(24),
    'MVCZHW' / construct.BitsInteger(1),
    'MVCSAV' / enum_211,  # 0=SM PARAMS NOT AVAIL, 1=SM PARAMS AVAIL
    '_pad0' / construct.BitsInteger(3),
    'MVCSID' / construct.BitsInteger(3),
    '_pad1' / construct.BitsInteger(8),
    'MVCS14' / construct.BitsInteger(8),
    'MVCS15' / construct.BitsInteger(16),
    'MVCS00' / construct.BitsInteger(32),
    'MVCS01' / construct.BitsInteger(32),
    'MVCS02' / construct.BitsInteger(32),
    'MVCS03' / construct.BitsInteger(32),
    'MVCS04' / construct.BitsInteger(32),
    'MVCS05' / construct.BitsInteger(32),
    'MVCS06' / construct.BitsInteger(32),
    'MVCS07' / construct.BitsInteger(32),
    'MVCS08' / construct.BitsInteger(16),
    'MVCS09' / construct.BitsInteger(16),
    'MVCS0A' / construct.BitsInteger(16),
    'MVCS0B' / construct.BitsInteger(8),
    '_pad2' / construct.BitsInteger(8),
    'MVCS0C' / construct.BitsInteger(16),
    'MVCS0D' / construct.BitsInteger(8),
    'MVCS0E' / common.EvalAdapter('1*x', construct.BitsInteger(16)),  # 1*x
    'MVCS0F' / construct.BitsInteger(8),
    'MVCS10' / construct.BitsInteger(16),
    'MVCS11' / construct.BitsInteger(32),
    'MVCS12' / construct.BitsInteger(16),
    'MVCS13' / construct.BitsInteger(16),
    'MVCS16' / construct.BitsInteger(16),
    'MVCS17' / construct.BitsInteger(16),
    'MVCS18' / common.EvalAdapter('0.01*x', construct.BitsInteger(8)),  # 0.01*x
    'MVCS19' / common.EvalAdapter('0.01*x', construct.BitsInteger(8)),  # 0.01*x
    'MVCS1A' / construct.BitsInteger(8),
    'MVCS1B' / construct.BitsInteger(8),
    'MVCS1C' / construct.BitsInteger(32),
    'MVCS1D' / construct.BitsInteger(32),
    'MVCS1E' / construct.BitsInteger(32),
    'MVCS1F' / construct.BitsInteger(32),
    'MVCS20' / construct.BitsInteger(32),
    'MVCS21' / construct.BitsInteger(32),
)

mview_ext_hk = construct.BitStruct(
    '_name' / construct.Computed('mview_ext_hk'),
    'name' / construct.Computed('MVIEW EXT HK'),
    'MVPTPR' / construct.BitsInteger(7),
    'MVPRHI' / construct.BitsInteger(1),
    'MVPOTY' / enum_212,  # 0=SM CATAL UPDATE, 1=SM SW UPDATE, 2=SM CAPTURE IMG, 3=SM CHANGE, 4=EXT DATA UPLOAD, 5=EXT DATA DOWNLOAD, 6=ZE FLASH OP TC
    'MVPRCD' / enum_213,  # 0=NOT RUNNING, 1=RUNNING, 2=SUCCESSFUL, 3=ABORTED, 4=ERROR
    'MVPOST' / construct.BitsInteger(4),
    'MVRES1' / construct.BitsInteger(4),
)

thruster_std_hk = construct.BitStruct(
    '_name' / construct.Computed('thruster_std_hk'),
    'name' / construct.Computed('THRUSTER STD HK'),
    'TH1TM1' / common.EvalAdapter('-75*x**0 +  1*x**1', construct.BitsInteger(8)),  # -75*x^0 +  1*x^1
    'TH1TM2' / common.EvalAdapter('-75*x**0 +  1*x**1', construct.BitsInteger(8)),  # -75*x^0 +  1*x^1
    'TH1TM3' / common.EvalAdapter('-75*x**0 +  1*x**1', construct.BitsInteger(8)),  # -75*x^0 +  1*x^1
    'TH1TMI' / common.EvalAdapter('-128*x**0 +  1*x**1', construct.BitsInteger(8)),  # -128*x^0 +  1*x^1
    'TH1ECN' / construct.BitsInteger(4),
    'TH1ECO' / enum_214,  # 0=NO ERROR, 1=ILL CMD, 2=ILL PARAM, 3=CFG REPAIRED, 4=CHARGE NOT EN, 5=CHARGE T/O, 6=CHARGE TOO SHORT, 7=CHARGE HW FAULT, 8=CHARGE RET WARN, 9=IGNITOR NOT EN, 10=TEMP1 LIMIT, 11=TEMP2 LIMIT, 12=TEMP3 LIMIT, 13=TEMPI2C LIMIT, 14=I2C ERR, 15=CFG REPAIR FAILED
    'TH1CCN' / construct.BitsInteger(4),
    'TH1CHE' / enum_0,  # 0=OFF, 1=ON
    'TH1IGE' / enum_0,  # 0=OFF, 1=ON
    'TH1AVA' / construct.BitsInteger(1),
    'TH1STA' / construct.BitsInteger(1),
    'TH1IGC' / construct.BitsInteger(8),
    'TH2TM1' / common.EvalAdapter('-75*x**0 +  1*x**1', construct.BitsInteger(8)),  # -75*x^0 +  1*x^1
    'TH2TM2' / common.EvalAdapter('-75*x**0 +  1*x**1', construct.BitsInteger(8)),  # -75*x^0 +  1*x^1
    'TH2TM3' / common.EvalAdapter('-75*x**0 +  1*x**1', construct.BitsInteger(8)),  # -75*x^0 +  1*x^1
    'TH2TMI' / common.EvalAdapter('-128*x**0 +  1*x**1', construct.BitsInteger(8)),  # -128*x^0 +  1*x^1
    'TH2ECN' / construct.BitsInteger(4),
    'TH2ECO' / enum_214,  # 0=NO ERROR, 1=ILL CMD, 2=ILL PARAM, 3=CFG REPAIRED, 4=CHARGE NOT EN, 5=CHARGE T/O, 6=CHARGE TOO SHORT, 7=CHARGE HW FAULT, 8=CHARGE RET WARN, 9=IGNITOR NOT EN, 10=TEMP1 LIMIT, 11=TEMP2 LIMIT, 12=TEMP3 LIMIT, 13=TEMPI2C LIMIT, 14=I2C ERR, 15=CFG REPAIR FAILED
    'TH2CCN' / construct.BitsInteger(4),
    'TH2CHE' / enum_0,  # 0=OFF, 1=ON
    'TH2IGE' / enum_0,  # 0=OFF, 1=ON
    'TH2AVA' / construct.BitsInteger(1),
    'TH2STA' / construct.BitsInteger(1),
    'TH2IGC' / construct.BitsInteger(8),
    'TH1RIG' / construct.BitsInteger(16),
    'TH1CAV' / construct.BitsInteger(16),
    'TH2RIG' / construct.BitsInteger(16),
    'TH2CAV' / construct.BitsInteger(16),
    'TH1CEC' / construct.BitsInteger(16),
    'TH1CMI' / construct.BitsInteger(16),
    'TH1CMA' / construct.BitsInteger(16),
    'TH1CLD' / construct.BitsInteger(16),
    'TH2CEC' / construct.BitsInteger(16),
    'TH2CMI' / construct.BitsInteger(16),
    'TH2CMA' / construct.BitsInteger(16),
    'TH2CLD' / construct.BitsInteger(16),
)

thruster_cfg_hk = construct.BitStruct(
    '_name' / construct.Computed('thruster_cfg_hk'),
    'name' / construct.Computed('THRUSTER CFG HK'),
    'THMICT' / construct.BitsInteger(16),
    'THMACT' / construct.BitsInteger(16),
    'THPUDI' / construct.BitsInteger(16),
    'THIGDI' / construct.BitsInteger(16),
    'THPUPI' / construct.BitsInteger(8),
    'THEMT1' / enum_0,  # 0=OFF, 1=ON
    'THEMT2' / enum_0,  # 0=OFF, 1=ON
    'THEMT3' / enum_0,  # 0=OFF, 1=ON
    'THEMTI' / enum_0,  # 0=OFF, 1=ON
    'THEMNE' / enum_0,  # 0=OFF, 1=ON
    'THEMTO' / enum_0,  # 0=OFF, 1=ON
    'THEMTS' / enum_0,  # 0=OFF, 1=ON
    'THEMFT' / enum_0,  # 0=OFF, 1=ON
    'THRESV' / construct.BitsInteger(7),
    'THEXTS' / enum_99,  # 0=BUS 1, 1=BUS 2
    'THT1LL' / construct.BitsInteger(16),
    'THT1UL' / construct.BitsInteger(16),
    'THT2LL' / construct.BitsInteger(16),
    'THT2UL' / construct.BitsInteger(16),
    'THT3LL' / construct.BitsInteger(16),
    'THT3UL' / construct.BitsInteger(16),
    'THTILL' / construct.BitsInteger(16),
    'THTIUL' / construct.BitsInteger(16),
    'THRUPT' / construct.BitsInteger(16),
)

gps_std_hk = construct.BitStruct(
    '_name' / construct.Computed('gps_std_hk'),
    'name' / construct.Computed('GPS STD HK'),
    'GPS1PS' / enum_0,  # 1=ON, 0=OFF
    'GPS1BS' / enum_0,  # 1=ON, 0=OFF
    'GPS1AV' / construct.BitsInteger(1),
    'GPS1PT' / enum_37,  # 1=YES, 0=NO
    'GPS1RN' / enum_0,  # 0=OFF, 1=ON
    'GPS1MF' / enum_37,  # 0=NO, 1=YES
    'GPS1RS' / construct.BitsInteger(2),
    'GPS1UT' / common.UNIXTimestampAdapter(construct.BitsInteger(48)),
    'GPS1QL' / enum_215,  # 0=NO FIX, 1=VALID SPS MODE, 2=VALID DIFF MODE, 3=VALID PPS MODE, 4=FIXED RTK, 5=FLOAT RTK, 6=ESTIMATED, 7=MANUAL, 8=SIMULATION
    'GPS1SU' / construct.BitsInteger(4),
    'GPS2PS' / enum_0,  # 1=ON, 0=OFF
    'GPS2BS' / enum_0,  # 1=ON, 0=OFF
    'GPS2AV' / construct.BitsInteger(1),
    'GPS2PT' / enum_37,  # 1=YES, 0=NO
    'GPS2RN' / enum_0,  # 0=OFF, 1=ON
    'GPS2MF' / enum_37,  # 0=NO, 1=YES
    'GPS2RS' / construct.BitsInteger(2),
    'GPS2UT' / common.UNIXTimestampAdapter(construct.BitsInteger(48)),
    'GPS2QL' / enum_215,  # 0=NO FIX, 1=VALID SPS MODE, 2=VALID DIFF MODE, 3=VALID PPS MODE, 4=FIXED RTK, 5=FLOAT RTK, 6=ESTIMATED, 7=MANUAL, 8=SIMULATION
    'GPS2SU' / construct.BitsInteger(4),
    'GPS1LT' / common.EvalAdapter('0.0000001*x**1 +  -214.7483647*x**0', construct.BitsInteger(32)),  # 0.0000001*x^1 +  -214.7483647*x^0
    'GPS1LN' / common.EvalAdapter('0.0000001*x**1 +  -214.7483647*x**0', construct.BitsInteger(32)),  # 0.0000001*x^1 +  -214.7483647*x^0
    'GPS2LT' / common.EvalAdapter('0.0000001*x**1 +  -214.7483647*x**0', construct.BitsInteger(32)),  # 0.0000001*x^1 +  -214.7483647*x^0
    'GPS2LN' / common.EvalAdapter('0.0000001*x**1 +  -214.7483647*x**0', construct.BitsInteger(32)),  # 0.0000001*x^1 +  -214.7483647*x^0
    'GPS1AL' / common.EvalAdapter('0.000001*x**1 +  -2147.483647*x**0', construct.BitsInteger(32)),  # 0.000001*x^1 +  -2147.483647*x^0
    'GPS1SP' / common.EvalAdapter('0.001*x', construct.BitsInteger(32)),  # 0.001*x
    'GPS2AL' / common.EvalAdapter('0.000001*x**1 +  -2147.483647*x**0', construct.BitsInteger(32)),  # 0.000001*x^1 +  -2147.483647*x^0
    'GPS2SP' / common.EvalAdapter('0.001*x', construct.BitsInteger(32)),  # 0.001*x
    'GPS1FC' / construct.BitsInteger(8),
    'GPS1SV' / construct.BitsInteger(8),
    'GPS1ER' / enum_216,  # 0=NO ERROR, 1=ILL CMD, 2=CFG REPAIR 1-2 GOOD, 3=CFG TRIPLE RED SUCC, 4=CFG TRIPLE RED FAIL, 5=CAN BUSY TIMEOUT, 6=CAN RX BUF OVERRUN, 7=GNSS RX BUF OVERRUN, 8=GNSS BUF OVERRUN, 9=INVALID NMEA, 10=NMEA NOT PARSED, 11=RMC PARSE FAILED, 12=GGA PARSE FAILED, 13=GSV PARSE FAILED, 14=ZDA PARSE FAILED, 15=GSV PARSE ILLEG SYS, 16=PREP COMPLETE, 17=GNSS MEM NOT ERASE, 18=GNSS REC START, 19=GNSS REC STOP, 20=PREP FAILED
    'GPS1CC' / construct.BitsInteger(4),
    'GPS1EC' / construct.BitsInteger(4),
    'GPS2FC' / construct.BitsInteger(8),
    'GPS2SV' / construct.BitsInteger(8),
    'GPS2ER' / enum_216,  # 0=NO ERROR, 1=ILL CMD, 2=CFG REPAIR 1-2 GOOD, 3=CFG TRIPLE RED SUCC, 4=CFG TRIPLE RED FAIL, 5=CAN BUSY TIMEOUT, 6=CAN RX BUF OVERRUN, 7=GNSS RX BUF OVERRUN, 8=GNSS BUF OVERRUN, 9=INVALID NMEA, 10=NMEA NOT PARSED, 11=RMC PARSE FAILED, 12=GGA PARSE FAILED, 13=GSV PARSE FAILED, 14=ZDA PARSE FAILED, 15=GSV PARSE ILLEG SYS, 16=PREP COMPLETE, 17=GNSS MEM NOT ERASE, 18=GNSS REC START, 19=GNSS REC STOP, 20=PREP FAILED
    'GPS2CC' / construct.BitsInteger(4),
    'GPS2EC' / construct.BitsInteger(4),
    '_pad0' / construct.BitsInteger(6),
)

reserved_apid_1 = construct.BitStruct(
    '_name' / construct.Computed('reserved_apid_1'),
    'name' / construct.Computed('RESERVED APID 1'),
    'RES011' / construct.BitsInteger(32),
    'RES012' / construct.BitsInteger(32),
    'RES013' / construct.BitsInteger(32),
    'RES014' / construct.BitsInteger(32),
    'RES015' / construct.BitsInteger(32),
    'RES016' / construct.BitsInteger(32),
)

obdh_cfg_raw = construct.BitStruct(
    '_name' / construct.Computed('obdh_cfg_raw'),
    'name' / construct.Computed('OBDH CFG RAW'),
    'data' / construct.GreedyBytes,
)

obdh_swupld_rcvd_sgmnts = construct.BitStruct(
    '_name' / construct.Computed('obdh_swupld_rcvd_sgmnts'),
    'name' / construct.Computed('OBDH SWUPLD RCVD SGMNTS'),
    'data' / construct.GreedyBytes,
)

obdh_mem_exp_data = construct.BitStruct(
    '_name' / construct.Computed('obdh_mem_exp_data'),
    'name' / construct.Computed('OBDH MEM EXP DATA'),
    'data' / construct.GreedyBytes,
)

obdh_time_ext_live = construct.BitStruct(
    '_name' / construct.Computed('obdh_time_ext_live'),
    'name' / construct.Computed('OBDH TIME EXT LIVE'),
    'data' / construct.GreedyBytes,
)

leop_list_1 = construct.BitStruct(
    '_name' / construct.Computed('leop_list_1'),
    'name' / construct.Computed('LEOP LIST 1'),
    'data' / construct.GreedyBytes,
)

leop_list_2 = construct.BitStruct(
    '_name' / construct.Computed('leop_list_2'),
    'name' / construct.Computed('LEOP LIST 2'),
    'data' / construct.GreedyBytes,
)

leop_list_3 = construct.BitStruct(
    '_name' / construct.Computed('leop_list_3'),
    'name' / construct.Computed('LEOP LIST 3'),
    'data' / construct.GreedyBytes,
)

active_safe_mode_list_1 = construct.BitStruct(
    '_name' / construct.Computed('active_safe_mode_list_1'),
    'name' / construct.Computed('ACTIVE SAFE MODE LIST 1'),
    'data' / construct.GreedyBytes,
)

active_safe_mode_list_2 = construct.BitStruct(
    '_name' / construct.Computed('active_safe_mode_list_2'),
    'name' / construct.Computed('ACTIVE SAFE MODE LIST 2'),
    'data' / construct.GreedyBytes,
)

active_safe_mode_list_3 = construct.BitStruct(
    '_name' / construct.Computed('active_safe_mode_list_3'),
    'name' / construct.Computed('ACTIVE SAFE MODE LIST 3'),
    'data' / construct.GreedyBytes,
)

passive_safe_mode_list = construct.BitStruct(
    '_name' / construct.Computed('passive_safe_mode_list'),
    'name' / construct.Computed('PASSIVE SAFE MODE LIST'),
    'data' / construct.GreedyBytes,
)

routine_procedure_1 = construct.BitStruct(
    '_name' / construct.Computed('routine_procedure_1'),
    'name' / construct.Computed('ROUTINE PROCEDURE 1'),
    'data' / construct.GreedyBytes,
)

routine_procedure_2 = construct.BitStruct(
    '_name' / construct.Computed('routine_procedure_2'),
    'name' / construct.Computed('ROUTINE PROCEDURE 2'),
    'data' / construct.GreedyBytes,
)

routine_procedure_3 = construct.BitStruct(
    '_name' / construct.Computed('routine_procedure_3'),
    'name' / construct.Computed('ROUTINE PROCEDURE 3'),
    'data' / construct.GreedyBytes,
)

routine_procedure_4 = construct.BitStruct(
    '_name' / construct.Computed('routine_procedure_4'),
    'name' / construct.Computed('ROUTINE PROCEDURE 4'),
    'data' / construct.GreedyBytes,
)

routine_procedure_5 = construct.BitStruct(
    '_name' / construct.Computed('routine_procedure_5'),
    'name' / construct.Computed('ROUTINE PROCEDURE 5'),
    'data' / construct.GreedyBytes,
)

routine_procedure_6 = construct.BitStruct(
    '_name' / construct.Computed('routine_procedure_6'),
    'name' / construct.Computed('ROUTINE PROCEDURE 6'),
    'data' / construct.GreedyBytes,
)

routine_procedure_7 = construct.BitStruct(
    '_name' / construct.Computed('routine_procedure_7'),
    'name' / construct.Computed('ROUTINE PROCEDURE 7'),
    'data' / construct.GreedyBytes,
)

routine_procedure_8 = construct.BitStruct(
    '_name' / construct.Computed('routine_procedure_8'),
    'name' / construct.Computed('ROUTINE PROCEDURE 8'),
    'data' / construct.GreedyBytes,
)

routine_procedure_9 = construct.BitStruct(
    '_name' / construct.Computed('routine_procedure_9'),
    'name' / construct.Computed('ROUTINE PROCEDURE 9'),
    'data' / construct.GreedyBytes,
)

routine_procedure_10 = construct.BitStruct(
    '_name' / construct.Computed('routine_procedure_10'),
    'name' / construct.Computed('ROUTINE PROCEDURE 10'),
    'data' / construct.GreedyBytes,
)

routine_procedure_11 = construct.BitStruct(
    '_name' / construct.Computed('routine_procedure_11'),
    'name' / construct.Computed('ROUTINE PROCEDURE 11'),
    'data' / construct.GreedyBytes,
)

routine_procedure_12 = construct.BitStruct(
    '_name' / construct.Computed('routine_procedure_12'),
    'name' / construct.Computed('ROUTINE PROCEDURE 12'),
    'data' / construct.GreedyBytes,
)

routine_procedure_13 = construct.BitStruct(
    '_name' / construct.Computed('routine_procedure_13'),
    'name' / construct.Computed('ROUTINE PROCEDURE 13'),
    'data' / construct.GreedyBytes,
)

routine_procedure_14 = construct.BitStruct(
    '_name' / construct.Computed('routine_procedure_14'),
    'name' / construct.Computed('ROUTINE PROCEDURE 14'),
    'data' / construct.GreedyBytes,
)

routine_procedure_15 = construct.BitStruct(
    '_name' / construct.Computed('routine_procedure_15'),
    'name' / construct.Computed('ROUTINE PROCEDURE 15'),
    'data' / construct.GreedyBytes,
)

routine_procedure_16 = construct.BitStruct(
    '_name' / construct.Computed('routine_procedure_16'),
    'name' / construct.Computed('ROUTINE PROCEDURE 16'),
    'data' / construct.GreedyBytes,
)

active_tt_list = construct.BitStruct(
    '_name' / construct.Computed('active_tt_list'),
    'name' / construct.Computed('ACTIVE TT LIST'),
    'data' / construct.GreedyBytes,
)

passive_tt_list = construct.BitStruct(
    '_name' / construct.Computed('passive_tt_list'),
    'name' / construct.Computed('PASSIVE TT LIST'),
    'data' / construct.GreedyBytes,
)

obdh_hist_err_cde = construct.BitStruct(
    '_name' / construct.Computed('obdh_hist_err_cde'),
    'name' / construct.Computed('OBDH HIST ERR CDE'),
    'data' / construct.GreedyBytes,
)

obdh_nor_flash_data = construct.BitStruct(
    '_name' / construct.Computed('obdh_nor_flash_data'),
    'name' / construct.Computed('OBDH NOR FLASH DATA'),
    'data' / construct.GreedyBytes,
)

can_listener_data = construct.BitStruct(
    '_name' / construct.Computed('can_listener_data'),
    'name' / construct.Computed('CAN LISTENER DATA'),
    'data' / construct.GreedyBytes,
)

obdh_ram_data = construct.BitStruct(
    '_name' / construct.Computed('obdh_ram_data'),
    'name' / construct.Computed('OBDH RAM DATA'),
    'data' / construct.GreedyBytes,
)

adcs_ext_live = construct.BitStruct(
    '_name' / construct.Computed('adcs_ext_live'),
    'name' / construct.Computed('ADCS EXT LIVE'),
    'data' / construct.GreedyBytes,
)

adcs_sun_sen_profile = construct.BitStruct(
    '_name' / construct.Computed('adcs_sun_sen_profile'),
    'name' / construct.Computed('ADCS SUN SEN PROFILE'),
    'data' / construct.GreedyBytes,
)

adcs_sun_sen_ext = construct.BitStruct(
    '_name' / construct.Computed('adcs_sun_sen_ext'),
    'name' / construct.Computed('ADCS SUN SEN EXT'),
    'data' / construct.GreedyBytes,
)

s_band_raw = construct.BitStruct(
    '_name' / construct.Computed('s_band_raw'),
    'name' / construct.Computed('S BAND RAW'),
    'data' / construct.GreedyBytes,
)

ai_exp_data = construct.BitStruct(
    '_name' / construct.Computed('ai_exp_data'),
    'name' / construct.Computed('AI EXP DATA'),
    'data' / construct.GreedyBytes,
)

mview_img_data = construct.BitStruct(
    '_name' / construct.Computed('mview_img_data'),
    'name' / construct.Computed('MVIEW IMG DATA'),
    'data' / construct.GreedyBytes,
)

mview_ext_live = construct.BitStruct(
    '_name' / construct.Computed('mview_ext_live'),
    'name' / construct.Computed('MVIEW EXT LIVE'),
    'data' / construct.GreedyBytes,
)

gps_raw_data = construct.BitStruct(
    '_name' / construct.Computed('gps_raw_data'),
    'name' / construct.Computed('GPS RAW DATA'),
    'data' / construct.GreedyBytes,
)

exp_apid_backup_01 = construct.BitStruct(
    '_name' / construct.Computed('exp_apid_backup_01'),
    'name' / construct.Computed('EXP APID BACKUP 01'),
    'data' / construct.GreedyBytes,
)

exp_apid_backup_02 = construct.BitStruct(
    '_name' / construct.Computed('exp_apid_backup_02'),
    'name' / construct.Computed('EXP APID BACKUP 02'),
    'data' / construct.GreedyBytes,
)

exp_apid_backup_03 = construct.BitStruct(
    '_name' / construct.Computed('exp_apid_backup_03'),
    'name' / construct.Computed('EXP APID BACKUP 03'),
    'data' / construct.GreedyBytes,
)

exp_apid_backup_04 = construct.BitStruct(
    '_name' / construct.Computed('exp_apid_backup_04'),
    'name' / construct.Computed('EXP APID BACKUP 04'),
    'data' / construct.GreedyBytes,
)

exp_apid_backup_05 = construct.BitStruct(
    '_name' / construct.Computed('exp_apid_backup_05'),
    'name' / construct.Computed('EXP APID BACKUP 05'),
    'data' / construct.GreedyBytes,
)

exp_apid_backup_06 = construct.BitStruct(
    '_name' / construct.Computed('exp_apid_backup_06'),
    'name' / construct.Computed('EXP APID BACKUP 06'),
    'data' / construct.GreedyBytes,
)

exp_apid_backup_07 = construct.BitStruct(
    '_name' / construct.Computed('exp_apid_backup_07'),
    'name' / construct.Computed('EXP APID BACKUP 07'),
    'data' / construct.GreedyBytes,
)

exp_apid_backup_08 = construct.BitStruct(
    '_name' / construct.Computed('exp_apid_backup_08'),
    'name' / construct.Computed('EXP APID BACKUP 08'),
    'data' / construct.GreedyBytes,
)

exp_apid_backup_09 = construct.BitStruct(
    '_name' / construct.Computed('exp_apid_backup_09'),
    'name' / construct.Computed('EXP APID BACKUP 09'),
    'data' / construct.GreedyBytes,
)

exp_apid_backup_10 = construct.BitStruct(
    '_name' / construct.Computed('exp_apid_backup_10'),
    'name' / construct.Computed('EXP APID BACKUP 10'),
    'data' / construct.GreedyBytes,
)
sonate2_map = {
    0x064: std_hk,
    0x069: obdh_ext_mem_ops_hk,
    0x06A: pdh_pldt_hk,
    0x06B: pdh_expdh_hk,
    0x06E: leop_hk,
    0x078: obdh_ext_err_cde,
    0x079: obdh_ext_mem_sts,
    0x07A: obdh_ext_periph_sts,
    0x07B: obdh_sto_rep_chk_hk,
    0x07C: obdh_sw_upld,
    0x07D: obdh_ext_hk_buf_cnt,
    0x07E: obdh_ext_tc_lst_len,
    0x07F: obdh_rst_cntr_hk,
    0x080: obdh_sw_inst,
    0x081: obdh_thread_run_time_hk,
    0x082: obdh_timestamps,
    0x083: obdh_can_listener_sts,
    0x08C: obdh_cfg_rest,
    0x08D: obdh_cfg_hk_buf,
    0x08E: obdh_cfg_tc_lst,
    0x08F: obdh_cfg_addr,
    0x090: obdh_cfg_sm_lim,
    0x091: obdh_cfg_pdh,
    0x092: obdh_cfg_raw,
    0x0A0: obdh_swupld_rcvd_sgmnts,
    0x0A5: obdh_mem_exp_data,
    0x0A6: obdh_time_ext_live,
    0x0AA: leop_list_1,
    0x0AB: leop_list_2,
    0x0AC: leop_list_3,
    0x0AD: active_safe_mode_list_1,
    0x0AE: active_safe_mode_list_2,
    0x0AF: active_safe_mode_list_3,
    0x0B0: passive_safe_mode_list,
    0x0B1: routine_procedure_1,
    0x0B2: routine_procedure_2,
    0x0B3: routine_procedure_3,
    0x0B4: routine_procedure_4,
    0x0B5: routine_procedure_5,
    0x0B6: routine_procedure_6,
    0x0B7: routine_procedure_7,
    0x0B8: routine_procedure_8,
    0x0B9: routine_procedure_9,
    0x0BA: routine_procedure_10,
    0x0BB: routine_procedure_11,
    0x0BC: routine_procedure_12,
    0x0BD: routine_procedure_13,
    0x0BE: routine_procedure_14,
    0x0BF: routine_procedure_15,
    0x0C0: routine_procedure_16,
    0x0C1: active_tt_list,
    0x0C2: passive_tt_list,
    0x0C3: obdh_hist_err_cde,
    0x0C4: obdh_nor_flash_data,
    0x0C5: can_listener_data,
    0x0C7: obdh_ram_data,
    0x0C8: adcs_std,
    0x0C9: adcs_ext,
    0x0CA: adcs_cfg,
    0x0CB: adcs_ext_live,
    0x0D2: adcs_akt_bus1_hk,
    0x0D3: adcs_akt_bus2_hk,
    0x0D4: adcs_rw_cfg,
    0x0E6: adcs_sun_sen_bus1_hk,
    0x0E7: adcs_sun_sen_bus2_hk,
    0x0E8: adcs_sun_sen_cfg,
    0x0E9: adcs_sun_sen_profile,
    0x0EA: adcs_sun_sen_ext,
    0x12C: power_sensor_hk,
    0x136: pwr_cfg_hk,
    0x140: ifp_cfg_hk,
    0x190: thermal_hk,
    0x1F4: vhf_ext_hk,
    0x1F5: uhf_ext_hk,
    0x1FE: s_band_std_hk,
    0x208: s_band_cfg,
    0x209: s_band_raw,
    0x2BC: ai_std_hk,
    0x2C1: ai_exp_data,
    0x2C6: ai_cam_app_std_hk,
    0x2C7: ai_ws_app_std_hk,
    0x2C8: ai_ns_app_std_hk,
    0x2C9: ai_od_app_std_hk,
    0x2CA: ai_ad_app_std_hk,
    0x2CB: ai_ld_app_std_hk,
    0x2CC: ai_app_07_std_hk,
    0x2CD: ai_app_08_std_hk,
    0x2CE: ai_app_09_std_hk,
    0x2CF: ai_app_10_std_hk,
    0x2D0: ai_cam_cfg_hk,
    0x2D5: ai_app_ld_cfg_hk,
    0x2DA: ai_cam_img_match_cfg,
    0x320: mview_std_hk,
    0x321: mview_cfg_hk,
    0x322: mview_ext_hk,
    0x32A: mview_img_data,
    0x334: mview_ext_live,
    0x384: thruster_std_hk,
    0x385: thruster_cfg_hk,
    0x3B6: gps_std_hk,
    0x3B7: gps_raw_data,
    0x3D4: reserved_apid_1,
    0x3E8: exp_apid_backup_01,
    0x3E9: exp_apid_backup_02,
    0x3EA: exp_apid_backup_03,
    0x3EB: exp_apid_backup_04,
    0x3EC: exp_apid_backup_05,
    0x3ED: exp_apid_backup_06,
    0x3EE: exp_apid_backup_07,
    0x3EF: exp_apid_backup_08,
    0x3F0: exp_apid_backup_09,
    0x3F1: exp_apid_backup_10,
}


class SonateProtocol(common.Protocol):
    columns = 'APID',
    c_width = 60,
    has_ax25 = 1

    tlm_table = {
        'std_hk': {
            'table': (
                ('name', 'Name', 0),
                ('O1UPTM', 'OBDH1 UPTIME, sec', 0),
                ('O1RSTC', 'OBDH1 RESET COUNTER', 0),
                ('O1CMDC', 'OBDH1 CMD COUNTER', 0),
                ('O1PWRS', 'OBDH1 POWER STATUS', 0),
                ('O1ROLE', 'OBDH1 ROLE', 0),
                ('O1ECNT', 'OBDH1 ERROR COUNTER', 0),
                ('O1ECDE', 'OBDH1 ERROR CODE', 0),
                ('O2UPTM', 'OBDH2 UPTIME, sec', 0),
                ('O2RSTC', 'OBDH2 RESET COUNTER', 0),
                ('O2CMDC', 'OBDH2 CMD COUNTER', 0),
                ('O2PWRS', 'OBDH2 POWER STATUS', 0),
                ('O2ROLE', 'OBDH2 ROLE', 0),
                ('O2ECNT', 'OBDH2 ERROR COUNTER', 0),
                ('O2ECDE', 'OBDH2 ERROR CODE', 0),
                ('O3UPTM', 'OBDH3 UPTIME, sec', 0),
                ('O3RSTC', 'OBDH3 RESET COUNTER', 0),
                ('O3CMDC', 'OBDH3 CMD COUNTER', 0),
                ('O3PWRS', 'OBDH3 POWER STATUS', 0),
                ('O3ROLE', 'OBDH3 ROLE', 0),
                ('O3ECNT', 'OBDH3 ERROR COUNTER', 0),
                ('O3ECDE', 'OBDH3 ERROR CODE', 0),
                ('O4UPTM', 'OBDH4 UPTIME, sec', 0),
                ('O4RSTC', 'OBDH4 RESET COUNTER', 0),
                ('O4CMDC', 'OBDH4 CMD COUNTER', 0),
                ('O4PWRS', 'OBDH4 POWER STATUS', 0),
                ('O4ROLE', 'OBDH4 ROLE', 0),
                ('O4ECNT', 'OBDH4 ERROR COUNTER', 0),
                ('O4ECDE', 'OBDH4 ERROR CODE', 0),
                ('PDHHWI', 'PDH HW ID', 0),
                ('CMDACN', 'ACTIVE TT LIST COUNTER', 0),
                ('CMDPCN', 'PASSIVE TT LIST COUNTER', 0),
                ('CMDEEC', 'CMD EXECUTION ERROR COUNT', 0),
                ('CMDEED', 'CMD EXECUTION ERROR CODE', 0),
                ('CMDSRC', 'LAST TC SOURCE', 0),
                ('CMDECE', 'CMD COUNTER ERROR COUNTER', 0),
                ('CAN1RS', 'CAN-BUS 1 RX STATE', 0),
                ('CAN1TS', 'CAN-BUS 1 TX STATE', 0),
                ('CAN2RS', 'CAN-BUS 2 RX STATE', 0),
                ('CAN2TS', 'CAN-BUS 2 TX STATE', 0),
                ('OBMODE', 'OBDH MODE', 0),
                ('TMSINK', 'CURRENT TM SINK', 0),
                ('GPCTHW', 'GPIO CONTROLLER HW ID', 0),
                ('SWUPHW', 'SW UPLOAD RCVR HW ID', 0),
                ('SWINHW', 'SW INSTALLER HW ID', 0),
                ('SBCTHW', 'S-BAND CONTROLLER HW ID', 0),
                ('CMDCNT', 'SAT CMD COUNTER', 0),
                ('VHF1MO', 'VHF1 MODE', 0),
                ('VHF1TC', 'VHF1 APRS TX COUNTER', 0),
                ('VHF1TM', 'VHF1 TEMPERATURE, °C', 0),
                ('VHF1RS', 'VHF1 RSSI RX, dBm', 0),
                ('VHF1RA', 'VHF1 RSSI AVG, dBm', 0),
                ('VHF1TO', 'VHF1 TX PWR, dBm', 0),
                ('VHF1EC', 'VHF1 ERROR CODE', 0),
                ('VHF1CC', 'VHF1 CMD COUNTER', 0),
                ('VHF1EN', 'VHF1 ERROR COUNTER', 0),
                ('VHF1RC', 'VHF1 AX25 RX COUNTER', 0),
                ('VHF2MO', 'VHF2 MODE', 0),
                ('VHF2TC', 'VHF2 APRS TX COUNTER', 0),
                ('VHF2TM', 'VHF2 TEMPERATURE, °C', 0),
                ('VHF2RS', 'VHF2 RSSI RX, dBm', 0),
                ('VHF2RA', 'VHF2 RSSI AVG, dBm', 0),
                ('VHF2TO', 'VHF2 TX PWR, dBm', 0),
                ('VHF2EC', 'VHF2 ERROR CODE', 0),
                ('VHF2CC', 'VHF2 CMD COUNTER', 0),
                ('VHF2EN', 'VHF2 ERROR COUNTER', 0),
                ('VHF2RC', 'VHF2 AX25 RX COUNTER', 0),
                ('UHF1MO', 'UHF1 MODE', 0),
                ('UHF1TM', 'UHF1 TEMPERATURE, °C', 0),
                ('UHF1RS', 'UHF1 RSSI RX, dBm', 0),
                ('UHF1RA', 'UHF1 RSSI AVG, dBm', 0),
                ('UHF1TO', 'UHF1 TX PWR, dBm', 0),
                ('UHF1EC', 'UHF1 ERROR CODE', 0),
                ('UHF1CC', 'UHF1 CMD COUNTER', 0),
                ('UHF1EN', 'UHF1 ERROR COUNTER', 0),
                ('UHF1RC', 'UHF1 AX25 RX COUNTER', 0),
                ('UHF2MO', 'UHF2 MODE', 0),
                ('UHF2TM', 'UHF2 TEMPERATURE, °C', 0),
                ('UHF2RS', 'UHF2 RSSI RX, dBm', 0),
                ('UHF2RA', 'UHF2 RSSI AVG, dBm', 0),
                ('UHF2TO', 'UHF2 TX PWR, dBm', 0),
                ('UHF2EC', 'UHF2 ERROR CODE', 0),
                ('UHF2CC', 'UHF2 CMD COUNTER', 0),
                ('UHF2EN', 'UHF2 ERROR COUNTER', 0),
                ('UHF2RC', 'UHF2 AX25 RX COUNTER', 0),
                ('P5V1CC', 'PCU05V1 CMD COUNTER', 0),
                ('P5V1PG', 'PCU05V1 CURR LIM PWR GOOD', 0),
                ('P5V1PF', 'PCU05V1 CURR LIM PWR FLT', 0),
                ('P5V1UE', 'PCU05V1 UPCNVRTR EN', 0),
                ('P5V1PE', 'PCU05V1 POWER ENABLE', 0),
                ('P5V1EO', 'PCU05V1 ERROR CODE', 0),
                ('P5V1EC', 'PCU05V1 ERROR COUNTER', 0),
                ('P5V1AV', 'PCU05V1 BATTERY VOLTAGE, V', 0),
                ('P5V1AC', 'PCU05V1 BATTERY CURRENT, A', 0),
                ('P5V1UV', 'PCU05V1 UPCNVRTR IN VLTG, V', 0),
                ('P5V1UC', 'PCU05V1 UPCNVRTR IN CURR, A', 0),
                ('P5V1BV', 'PCU05V1 BUS1 5V VOLTAGE, V', 0),
                ('P5V1BC', 'PCU05V1 BUS1 5V CURRENT, A', 0),
                ('P5V2CC', 'PCU05V2 CMD COUNTER', 0),
                ('P5V2PG', 'PCU05V2 CURR LIM PWR GOOD', 0),
                ('P5V2PF', 'PCU05V2 CURR LIM PWR FLT', 0),
                ('P5V2UE', 'PCU05V2 UPCNVRTR EN', 0),
                ('P5V2PE', 'PCU05V2 POWER ENABLE', 0),
                ('P5V2EO', 'PCU05V2 ERROR CODE', 0),
                ('P5V2EC', 'PCU05V2 ERROR COUNTER', 0),
                ('P5V2AV', 'PCU05V2 BATTERY VOLTAGE, V', 0),
                ('P5V2AC', 'PCU05V2 BATTERY CURRENT, A', 0),
                ('P5V2UV', 'PCU05V2 UPCNVRTR IN VLTG, V', 0),
                ('P5V2UC', 'PCU05V2 UPCNVRTR IN CURR, A', 0),
                ('P5V2BV', 'PCU05V2 BUS2 5V VOLTAGE, V', 0),
                ('P5V2BC', 'PCU05V2 BUS2 5V CURRENT, A', 0),
                ('P5V1BT', 'PCU05V1 BATTERY TEMP, °C', 0),
                ('12V1BT', 'PCU12V1 BATTERY TEMP, °C', 0),
                ('SXP1PS', 'SS XP1 POWER STATUS', 0),
                ('SXN1PS', 'SS XN1 POWER STATUS', 0),
                ('SYP1PS', 'SS YP1 POWER STATUS', 0),
                ('SYN1PS', 'SS YN1 POWER STATUS', 0),
                ('SZP1PS', 'SS ZP1 POWER STATUS', 0),
                ('SZN1PS', 'SS ZN1 POWER STATUS', 0),
                ('ADS1PS', 'ADCS1 POWER STATUS', 0),
                ('MVW1PS', 'MULTIVIEW1 POWER STATUS', 0),
                ('THR1PS', 'THRUSTER1 POWER STATUS', 0),
                ('IFP1PS', 'IFP1 POWER STATUS', 0),
                ('P5V1PS', 'PCU05V1 POWER SYNC', 0),
                ('P5V1HA', 'PCU05V1 HK AVAILABLE', 0),
                ('THR1PG', 'THRUSTER1 POWER GOOD', 0),
                ('P5V1RS', 'PCU05V1 RELAIS STATUS', 0),
                ('P5V1CS', 'PCU05V1 CURRENT LIMIT STS', 0),
                ('P5V111', 'PCU05V1 MAX FRONT11 AV', 0),
                ('P5V121', 'PCU05V1 MAX FRONT21 AV', 0),
                ('P5V122', 'PCU05V1 MAX FRONT22 AV', 0),
                ('P5V1TR', 'PCU05V1 MAX TERM AV', 0),
                ('P5V1RM', 'PCU05V1 UPCNVRTR MODE', 0),
                ('P5V2BT', 'PCU05V2 BATTERY TEMP, °C', 0),
                ('12V2BT', 'PCU12V2 BATTERY TEMP, °C', 0),
                ('SXP2PS', 'SS XP2 POWER STATUS', 0),
                ('SXN2PS', 'SS XN2 POWER STATUS', 0),
                ('SYP2PS', 'SS YP2 POWER STATUS', 0),
                ('SYN2PS', 'SS YN2 POWER STATUS', 0),
                ('SZP2PS', 'SS ZP2 POWER STATUS', 0),
                ('SZN2PS', 'SS ZN2 POWER STATUS', 0),
                ('ADS2PS', 'ADCS2 POWER STATUS', 0),
                ('MVW2PS', 'MULTIVIEW2 POWER STATUS', 0),
                ('THR2PS', 'THRUSTER2 POWER STATUS', 0),
                ('IFP2PS', 'IFP2 POWER STATUS', 0),
                ('P5V2PS', 'PCU05V2 POWER SYNC', 0),
                ('P5V2HA', 'PCU05V2 HK AVAILABLE', 0),
                ('THR2PG', 'THRUSTER2 POWER GOOD', 0),
                ('P5V2RS', 'PCU05V2 RELAIS STATUS', 0),
                ('P5V2CS', 'PCU05V2 CURRENT LIMIT STS', 0),
                ('P5V211', 'PCU05V2 MAX FRONT11 AV', 0),
                ('P5V221', 'PCU05V2 MAX FRONT21 AV', 0),
                ('P5V222', 'PCU05V2 MAX FRONT22 AV', 0),
                ('P5V2TR', 'PCU05V2 MAX TERM AV', 0),
                ('P5V2RM', 'PCU05V2 UPCNVRTR MODE', 0),
                ('12V1CC', 'PCU12V1 CMD COUNTER', 0),
                ('12V1PG', 'PCU12V1 CURR LIM PWR GOOD', 0),
                ('12V1PF', 'PCU12V1 CURR LIM PWR FLT', 0),
                ('12V1UE', 'PCU12V1 UPCNVRTR EN', 0),
                ('12V1PE', 'PCU12V1 POWER ENABLE', 0),
                ('12V1EO', 'PCU12V1 ERROR CODE', 0),
                ('12V1EC', 'PCU12V1 ERROR COUNTER', 0),
                ('12V1AV', 'PCU12V1 BATTERY VOLTAGE, V', 0),
                ('12V1AC', 'PCU12V1 BATTERY CURRENT, A', 0),
                ('12V1UV', 'PCU12V1 UPCNVRTR IN VLTG, V', 0),
                ('12V1UC', 'PCU12V1 UPCNVRTR IN CURR, A', 0),
                ('12V1BV', 'PCU12V1 BUS1 12V VOLTAGE, V', 0),
                ('12V1BC', 'PCU12V1 BUS1 12V CURRENT, A', 0),
                ('12V2CC', 'PCU12V2 CMD COUNTER', 0),
                ('12V2PG', 'PCU12V2 CURR LIM PWR GOOD', 0),
                ('12V2PF', 'PCU12V2 CURR LIM PWR FLT', 0),
                ('12V2UE', 'PCU12V2 UPCNVRTR EN', 0),
                ('12V2PE', 'PCU12V2 POWER ENABLE', 0),
                ('12V2EO', 'PCU12V2 ERROR CODE', 0),
                ('12V2EC', 'PCU12V2 ERROR COUNTER', 0),
                ('12V2AV', 'PCU12V2 BATTERY VOLTAGE, V', 0),
                ('12V2AC', 'PCU12V2 BATTERY CURRENT, A', 0),
                ('12V2UV', 'PCU12V2 UPCNVRTR IN VLTG, V', 0),
                ('12V2UC', 'PCU12V2 UPCNVRTR IN CURR, A', 0),
                ('12V2BV', 'PCU12V2 BUS2 12V VOLTAGE, V', 0),
                ('12V2BC', 'PCU12V2 BUS2 12V CURRENT, A', 0),
                ('12V1SS', 'PCU12V1 SOLAR REG STATE', 0),
                ('AI1PWS', 'AI1 POWER STATUS', 0),
                ('12V1HA', 'PCU12V1 HK AVAILABLE', 0),
                ('12V1CS', 'PCU12V1 CHARGE STATUS', 0),
                ('12V1RM', 'PCU12V1 UPCNVRTR MODE', 0),
                ('12V2SS', 'PCU12V2 SOLAR REG STATE', 0),
                ('AI2PWS', 'AI2 POWER STATUS', 0),
                ('12V2HA', 'PCU12V2 HK AVAILABLE', 0),
                ('12V2CS', 'PCU12V2 CHARGE STATUS', 0),
                ('12V2RM', 'PCU12V2 UPCNVRTR MODE', 0),
                ('IFP1ST', 'IFP1 STATE', 0),
                ('SB1RXS', 'S-BAND1 RS422 RX STATE', 0),
                ('SB1ENA', 'S-BAND1 POWER', 0),
                ('RWX1PS', 'RW X1 POWER STATUS', 0),
                ('RWY1PS', 'RW Y1 POWER STATUS', 0),
                ('RWZ1PS', 'RW Z1 POWER STATUS', 0),
                ('SB1TXS', 'S-BAND1 RS422 TX STATE', 0),
                ('IFP1EN', 'IFP1 ERROR COUNTER', 0),
                ('IFP1EC', 'IFP1 ERROR CODE', 0),
                ('IFP1CC', 'IFP1 CMD COUNTER', 0),
                ('IFP1AC', 'IFP1 ADCS CMD COUNTER', 0),
                ('IFP2ST', 'IFP2 STATE', 0),
                ('SB2RXS', 'S-BAND2 RS422 RX STATE', 0),
                ('SB2ENA', 'S-BAND2 POWER', 0),
                ('RWX2PS', 'RW X2 POWER STATUS', 0),
                ('RWY2PS', 'RW Y2 POWER STATUS', 0),
                ('RWZ2PS', 'RW Z2 POWER STATUS', 0),
                ('SB2TXS', 'S-BAND2 RS422 TX STATE', 0),
                ('IFP2EN', 'IFP2 ERROR COUNTER', 0),
                ('IFP2EC', 'IFP2 ERROR CODE', 0),
                ('IFP2CC', 'IFP2 CMD COUNTER', 0),
                ('IFP2AC', 'IFP2 ADCS CMD COUNTER', 0),
            ),
        },
        'obdh_ext_mem_ops_hk': {
            'table': (
                ('name', 'Name', 0),
                ('O1MOAV', 'OBDH1 MEM OPS AVAILABLE', 0),
                ('O1MOST', 'OBDH1 MEM OPS STATE', 0),
                ('O1MOPR', 'OBDH1 MEM OPS PROGRESS, %', 0),
                ('O1MOEO', 'OBDH1 MEM OPS ERR CDE', 0),
                ('O1MOEC', 'OBDH1 MEM OPS ERR CNT', 0),
                ('O2MOAV', 'OBDH2 MEM OPS AVAILABLE', 0),
                ('O2MOST', 'OBDH2 MEM OPS STATE', 0),
                ('O2MOPR', 'OBDH2 MEM OPS PROGRESS, %', 0),
                ('O2MOEO', 'OBDH2 MEM OPS ERR CDE', 0),
                ('O2MOEC', 'OBDH2 MEM OPS ERR CNT', 0),
                ('O3MOAV', 'OBDH3 MEM OPS AVAILABLE', 0),
                ('O3MOST', 'OBDH3 MEM OPS STATE', 0),
                ('O3MOPR', 'OBDH3 MEM OPS PROGRESS, %', 0),
                ('O3MOEO', 'OBDH3 MEM OPS ERR CDE', 0),
                ('O3MOEC', 'OBDH3 MEM OPS ERR CNT', 0),
                ('O4MOAV', 'OBDH4 MEM OPS AVAILABLE', 0),
                ('O4MOST', 'OBDH4 MEM OPS STATE', 0),
                ('O4MOPR', 'OBDH4 MEM OPS PROGRESS, %', 0),
                ('O4MOEO', 'OBDH4 MEM OPS ERR CDE', 0),
                ('O4MOEC', 'OBDH4 MEM OPS ERR CNT', 0),
            ),
        },
        'pdh_pldt_hk': {
            'table': (
                ('name', 'Name', 0),
                ('OPECNT', 'PLDT ERROR COUNTER', 0),
                ('OPECDE', 'PLDT ERROR CODE', 0),
                ('OPCDWS', 'PLDT CAN DWNLD STATE', 0),
                ('OPCUPS', 'PLDT CAN UPLD STATE', 0),
                ('OPHWID', 'PDH HW ID', 0),
                ('OPIFAC', 'PDH I/F ACTIVATED', 0),
                ('OPSUPS', 'PLDT SPI UPLD STATE', 0),
                ('OPDHOP', 'PLDT OPERATION', 0),
                ('OPSDWS', 'PLDT SPI DWNLD STATE', 0),
                ('OPPROG', 'PLDT PROGRESS, %', 0),
                ('OPECRC', 'PLDT EXPECTED CRC', 0),
                ('OPDTSZ', 'PLDT DATA SIZE', 0),
            ),
        },
        'pdh_expdh_hk': {
            'table': (
                ('name', 'Name', 0),
                ('OPEXEC', 'PDH EXPDH ERR CNT', 0),
                ('OPEXEO', 'PDH EXPDH ERR CDE', 0),
                ('OPDHEI', 'PDH EXPDH HW ID', 0),
                ('OPEXST', 'PDH EXPDH STATE', 0),
                ('OPBERO', 'PDH EXPDH BUF ERASE STS', 0),
                ('OPERES', 'PDH EXPDH RESERVED(3 bit)', 0),
                ('OPEIAC', 'PDH EXPDH I/F ACTIVATED', 0),
                ('OPEX0I', 'PDH EXPDH BUF0 ID', 0),
                ('OPEX0S', 'PDH EXPDH BUF0 STATE', 0),
                ('OPEX0C', 'PDH EXPDH BUF0 BYTE CNT', 0),
                ('OPEX1I', 'PDH EXPDH BUF1 ID', 0),
                ('OPEX1S', 'PDH EXPDH BUF1 STATE', 0),
                ('OPEX1C', 'PDH EXPDH BUF1 BYTE CNT', 0),
                ('OPEX2I', 'PDH EXPDH BUF2 ID', 0),
                ('OPEX2S', 'PDH EXPDH BUF2 STATE', 0),
                ('OPEX2C', 'PDH EXPDH BUF2 BYTE CNT', 0),
                ('OPEX3I', 'PDH EXPDH BUF3 ID', 0),
                ('OPEX3S', 'PDH EXPDH BUF3 STATE', 0),
                ('OPEX3C', 'PDH EXPDH BUF3 BYTE CNT', 0),
                ('OPEX4I', 'PDH EXPDH BUF4 ID', 0),
                ('OPEX4S', 'PDH EXPDH BUF4 STATE', 0),
                ('OPEX4C', 'PDH EXPDH BUF4 BYTE CNT', 0),
                ('OPEX5I', 'PDH EXPDH BUF5 ID', 0),
                ('OPEX5S', 'PDH EXPDH BUF5 STATE', 0),
                ('OPEX5C', 'PDH EXPDH BUF5 BYTE CNT', 0),
                ('OPEX6I', 'PDH EXPDH BUF6 ID', 0),
                ('OPEX6S', 'PDH EXPDH BUF6 STATE', 0),
                ('OPEX6C', 'PDH EXPDH BUF6 BYTE CNT', 0),
                ('OPEX7I', 'PDH EXPDH BUF7 ID', 0),
                ('OPEX7S', 'PDH EXPDH BUF7 STATE', 0),
                ('OPEX7C', 'PDH EXPDH BUF7 BYTE CNT', 0),
            ),
        },
        'leop_hk': {
            'table': (
                ('name', 'Name', 0),
                ('O1LEFA', 'OBDH1 LEOP FLAG AVAILABLE', 0),
                ('O1LEFS', 'OBDH1 LEOP FLAG STATUS', 0),
                ('O2LEFA', 'OBDH2 LEOP FLAG AVAILABLE', 0),
                ('O2LEFS', 'OBDH2 LEOP FLAG STATUS', 0),
                ('O3LEFA', 'OBDH3 LEOP FLAG AVAILABLE', 0),
                ('O3LEFS', 'OBDH3 LEOP FLAG STATUS', 0),
                ('O4LEFA', 'OBDH4 LEOP FLAG AVAILABLE', 0),
                ('O4LEFS', 'OBDH4 LEOP FLAG STATUS', 0),
                ('VA1DFB', 'VHF ANT 1 DEPLOYMENT', 0),
                ('VA1DEN', 'VHF ANT 1 DEPLOY EN', 0),
                ('VA1DDR', 'VHF ANT 1 DEPLOY DIR', 0),
                ('VA1HAV', 'VHF1 LEOP HK AVAIL', 0),
                ('VA1DPW', 'VHF ANT 1 DEPLOY PWM, %', 0),
                ('VA2DFB', 'VHF ANT 2 DEPLOYMENT', 0),
                ('VA2DEN', 'VHF ANT 2 DEPLOY EN', 0),
                ('VA2DDR', 'VHF ANT 2 DEPLOY DIR', 0),
                ('VA2HAV', 'VHF2 LEOP HK AVAIL', 0),
                ('VA2DPW', 'VHF ANT 2 DEPLOY PWM, %', 0),
                ('UA1DFB', 'UHF ANT 1 DEPLOYMENT', 0),
                ('UA1DEN', 'UHF ANT 1 DEPLOY EN', 0),
                ('UA1DDR', 'UHF ANT 1 DEPLOY DIR', 0),
                ('UA1HAV', 'UHF1 LEOP HK AVAIL', 0),
                ('UA1DPW', 'UHF ANT 1 DEPLOY PWM, %', 0),
                ('UA2DFB', 'UHF ANT 2 DEPLOYMENT', 0),
                ('UA2DEN', 'UHF ANT 2 DEPLOY EN', 0),
                ('UA2DDR', 'UHF ANT 2 DEPLOY DIR', 0),
                ('UA2HAV', 'UHF2 LEOP HK AVAIL', 0),
                ('UA2DPW', 'UHF ANT 2 DEPLOY PWM, %', 0),
                ('IF1DFT', 'SOL PANEL 1 DEPLOY FAULT', 0),
                ('IF1DFB', 'SOL PANEL 1 DEPLOYMENT', 0),
                ('IF1DEN', 'SOL PANEL 1 DEPLOY EN', 0),
                ('IF1DDR', 'SOL PANEL 1 DEPLOY DIR', 0),
                ('IF1DSR', 'SOL PANEL 1 DEPLOY STBY', 0),
                ('IF1DCU', 'SOL PANEL 1 DEPLOY CURR, mA', 0),
                ('IF1DPW', 'SOL PANEL 1 DEPLOY PWM, %', 0),
                ('IF1LAV', 'IFP 1 LEOP HK AVAIL', 0),
                ('IF2DFT', 'SOL PANEL 2 DEPLOY FAULT', 0),
                ('IF2DFB', 'SOL PANEL 2 DEPLOYMENT', 0),
                ('IF2DEN', 'SOL PANEL 2 DEPLOY EN', 0),
                ('IF2DDR', 'SOL PANEL 2 DEPLOY DIR', 0),
                ('IF2DSR', 'SOL PANEL 2 DEPLOY STBY', 0),
                ('IF2DCU', 'SOL PANEL 2 DEPLOY CURR, mA', 0),
                ('IF2DPW', 'SOL PANEL 2 DEPLOY PWM, %', 0),
                ('IF2LAV', 'IFP 2 LEOP HK AVAIL', 0),
            ),
        },
        'obdh_ext_err_cde': {
            'table': (
                ('name', 'Name', 0),
                ('O1EOCF', 'OBDH1 ERR CDE CONFIG', 0),
                ('O1ECCF', 'OBDH1 ERR CNT CONFIG', 0),
                ('O1EORM', 'OBDH1 ERR CDE ROLE MGR', 0),
                ('O1ECRM', 'OBDH1 ERR CNT ROLE MGR', 0),
                ('O1EONM', 'OBDH1 ERR CDE NOR CTRL', 0),
                ('O1ECNM', 'OBDH1 ERR CNT NOR CTRL', 0),
                ('O1EOTE', 'OBDH1 ERR CDE TC EXEC', 0),
                ('O1ECTE', 'OBDH1 ERR CNT TC EXEC', 0),
                ('O1EOTR', 'OBDH1 ERR CDE TC RCVR', 0),
                ('O1ECTR', 'OBDH1 ERR CNT TC RCVR', 0),
                ('O1EOTS', 'OBDH1 ERR CDE TC SAVER', 0),
                ('O1ECTS', 'OBDH1 ERR CNT TC SAVER', 0),
                ('O1EOWD', 'OBDH1 ERR CDE SWDG', 0),
                ('O1ECWD', 'OBDH1 ERR CNT SWDG', 0),
                ('O1ECAV', 'OBDH1 ERR FRAME AVAILABLE', 0),
                ('O1EOOT', 'OBDH1 ERR CDE OBC TC RX', 0),
                ('O1ECOT', 'OBDH1 ERR CNT OBC TC RX', 0),
                ('O2EOCF', 'OBDH2 ERR CDE CONFIG', 0),
                ('O2ECCF', 'OBDH2 ERR CNT CONFIG', 0),
                ('O2EORM', 'OBDH2 ERR CDE ROLE MGR', 0),
                ('O2ECRM', 'OBDH2 ERR CNT ROLE MGR', 0),
                ('O2EONM', 'OBDH2 ERR CDE NOR CTRL', 0),
                ('O2ECNM', 'OBDH2 ERR CNT NOR CTRL', 0),
                ('O2EOTE', 'OBDH2 ERR CDE TC EXEC', 0),
                ('O2ECTE', 'OBDH2 ERR CNT TC EXEC', 0),
                ('O2EOTR', 'OBDH2 ERR CDE TC RCVR', 0),
                ('O2ECTR', 'OBDH2 ERR CNT TC RCVR', 0),
                ('O2EOTS', 'OBDH2 ERR CDE TC SAVER', 0),
                ('O2ECTS', 'OBDH2 ERR CNT TC SAVER', 0),
                ('O2EOWD', 'OBDH2 ERR CDE SWDG', 0),
                ('O2ECWD', 'OBDH2 ERR CNT SWDG', 0),
                ('O2ECAV', 'OBDH2 ERR FRAME AVAILABLE', 0),
                ('O2EOOT', 'OBDH2 ERR CDE OBC TC RX', 0),
                ('O2ECOT', 'OBDH2 ERR CNT OBC TC RX', 0),
                ('O3EOCF', 'OBDH3 ERR CDE CONFIG', 0),
                ('O3ECCF', 'OBDH3 ERR CNT CONFIG', 0),
                ('O3EORM', 'OBDH3 ERR CDE ROLE MGR', 0),
                ('O3ECRM', 'OBDH3 ERR CNT ROLE MGR', 0),
                ('O3EONM', 'OBDH3 ERR CDE NOR CTRL', 0),
                ('O3ECNM', 'OBDH3 ERR CNT NOR CTRL', 0),
                ('O3EOTE', 'OBDH3 ERR CDE TC EXEC', 0),
                ('O3ECTE', 'OBDH3 ERR CNT TC EXEC', 0),
                ('O3EOTR', 'OBDH3 ERR CDE TC RCVR', 0),
                ('O3ECTR', 'OBDH3 ERR CNT TC RCVR', 0),
                ('O3EOTS', 'OBDH3 ERR CDE TC SAVER', 0),
                ('O3ECTS', 'OBDH3 ERR CNT TC SAVER', 0),
                ('O3EOWD', 'OBDH3 ERR CDE SWDG', 0),
                ('O3ECWD', 'OBDH3 ERR CNT SWDG', 0),
                ('O3ECAV', 'OBDH3 ERR FRAME AVAILABLE', 0),
                ('O3EOOT', 'OBDH3 ERR CDE OBC TC RX', 0),
                ('O3ECOT', 'OBDH3 ERR CNT OBC TC RX', 0),
                ('O4EOCF', 'OBDH4 ERR CDE CONFIG', 0),
                ('O4ECCF', 'OBDH4 ERR CNT CONFIG', 0),
                ('O4EORM', 'OBDH4 ERR CDE ROLE MGR', 0),
                ('O4ECRM', 'OBDH4 ERR CNT ROLE MGR', 0),
                ('O4EONM', 'OBDH4 ERR CDE NOR CTRL', 0),
                ('O4ECNM', 'OBDH4 ERR CNT NOR CTRL', 0),
                ('O4EOTE', 'OBDH4 ERR CDE TC EXEC', 0),
                ('O4ECTE', 'OBDH4 ERR CNT TC EXEC', 0),
                ('O4EOTR', 'OBDH4 ERR CDE TC RCVR', 0),
                ('O4ECTR', 'OBDH4 ERR CNT TC RCVR', 0),
                ('O4EOTS', 'OBDH4 ERR CDE TC SAVER', 0),
                ('O4ECTS', 'OBDH4 ERR CNT TC SAVER', 0),
                ('O4EOWD', 'OBDH4 ERR CDE SWDG', 0),
                ('O4ECWD', 'OBDH4 ERR CNT SWDG', 0),
                ('O4ECAV', 'OBDH4 ERR FRAME AVAILABLE', 0),
                ('O4EOOT', 'OBDH4 ERR CDE OBC TC RX', 0),
                ('O4ECOT', 'OBDH4 ERR CNT OBC TC RX', 0),
                ('O1EOSM', 'OBDH1 ERR CDE SYS MGR', 0),
                ('O1ECSM', 'OBDH1 ERR CNT SYS MGR', 0),
                ('O1EOHK', 'OBDH1 ERR CDE HOUSEKEEPER', 0),
                ('O1ECHK', 'OBDH1 ERR CNT HOUSEKEEPER', 0),
                ('O1EOTD', 'OBDH1 ERR CDE TM DOWNLINK', 0),
                ('O1ECTD', 'OBDH1 ERR CNT TM DOWNLINK', 0),
                ('O1EOMM', 'OBDH1 ERR CDE MEM MON', 0),
                ('O1ECMM', 'OBDH1 ERR CNT MEM MON', 0),
                ('O1EOSC', 'OBDH1 ERR CDE SRAM CTRL', 0),
                ('O1ECSC', 'OBDH1 ERR CNT SRAM CTRL', 0),
                ('O1EOV1', 'OBDH1 ERR CDE VHF1 I/F', 0),
                ('O1ECV1', 'OBDH1 ERR CNT VHF1 I/F', 0),
                ('O1EOV2', 'OBDH1 ERR CDE VHF2 I/F', 0),
                ('O1ECV2', 'OBDH1 ERR CNT VHF2 I/F', 0),
                ('O1EOU1', 'OBDH1 ERR CDE UHF1 I/F', 0),
                ('O1ECU1', 'OBDH1 ERR CNT UHF1 I/F', 0),
                ('O2EOSM', 'OBDH2 ERR CDE SYS MGR', 0),
                ('O2ECSM', 'OBDH2 ERR CNT SYS MGR', 0),
                ('O2EOHK', 'OBDH2 ERR CDE HOUSEKEEPER', 0),
                ('O2ECHK', 'OBDH2 ERR CNT HOUSEKEEPER', 0),
                ('O2EOTD', 'OBDH2 ERR CDE TM DOWNLINK', 0),
                ('O2ECTD', 'OBDH2 ERR CNT TM DOWNLINK', 0),
                ('O2EOMM', 'OBDH2 ERR CDE MEM MON', 0),
                ('O2ECMM', 'OBDH2 ERR CNT MEM MON', 0),
                ('O2EOSC', 'OBDH2 ERR CDE SRAM CTRL', 0),
                ('O2ECSC', 'OBDH2 ERR CNT SRAM CTRL', 0),
                ('O2EOV1', 'OBDH2 ERR CDE VHF1 I/F', 0),
                ('O2ECV1', 'OBDH2 ERR CNT VHF1 I/F', 0),
                ('O2EOV2', 'OBDH2 ERR CDE VHF2 I/F', 0),
                ('O2ECV2', 'OBDH2 ERR CNT VHF2 I/F', 0),
                ('O2EOU1', 'OBDH2 ERR CDE UHF1 I/F', 0),
                ('O2ECU1', 'OBDH2 ERR CNT UHF1 I/F', 0),
                ('O3EOSM', 'OBDH3 ERR CDE SYS MGR', 0),
                ('O3ECSM', 'OBDH3 ERR CNT SYS MGR', 0),
                ('O3EOHK', 'OBDH3 ERR CDE HOUSEKEEPER', 0),
                ('O3ECHK', 'OBDH3 ERR CNT HOUSEKEEPER', 0),
                ('O3EOTD', 'OBDH3 ERR CDE TM DOWNLINK', 0),
                ('O3ECTD', 'OBDH3 ERR CNT TM DOWNLINK', 0),
                ('O3EOMM', 'OBDH3 ERR CDE MEM MON', 0),
                ('O3ECMM', 'OBDH3 ERR CNT MEM MON', 0),
                ('O3EOSC', 'OBDH3 ERR CDE SRAM CTRL', 0),
                ('O3ECSC', 'OBDH3 ERR CNT SRAM CTRL', 0),
                ('O3EOV1', 'OBDH3 ERR CDE VHF1 I/F', 0),
                ('O3ECV1', 'OBDH3 ERR CNT VHF1 I/F', 0),
                ('O3EOV2', 'OBDH3 ERR CDE VHF2 I/F', 0),
                ('O3ECV2', 'OBDH3 ERR CNT VHF2 I/F', 0),
                ('O3EOU1', 'OBDH3 ERR CDE UHF1 I/F', 0),
                ('O3ECU1', 'OBDH3 ERR CNT UHF1 I/F', 0),
                ('O4EOSM', 'OBDH4 ERR CDE SYS MGR', 0),
                ('O4ECSM', 'OBDH4 ERR CNT SYS MGR', 0),
                ('O4EOHK', 'OBDH4 ERR CDE HOUSEKEEPER', 0),
                ('O4ECHK', 'OBDH4 ERR CNT HOUSEKEEPER', 0),
                ('O4EOTD', 'OBDH4 ERR CDE TM DOWNLINK', 0),
                ('O4ECTD', 'OBDH4 ERR CNT TM DOWNLINK', 0),
                ('O4EOMM', 'OBDH4 ERR CDE MEM MON', 0),
                ('O4ECMM', 'OBDH4 ERR CNT MEM MON', 0),
                ('O4EOSC', 'OBDH4 ERR CDE SRAM CTRL', 0),
                ('O4ECSC', 'OBDH4 ERR CNT SRAM CTRL', 0),
                ('O4EOV1', 'OBDH4 ERR CDE VHF1 I/F', 0),
                ('O4ECV1', 'OBDH4 ERR CNT VHF1 I/F', 0),
                ('O4EOV2', 'OBDH4 ERR CDE VHF2 I/F', 0),
                ('O4ECV2', 'OBDH4 ERR CNT VHF2 I/F', 0),
                ('O4EOU1', 'OBDH4 ERR CDE UHF1 I/F', 0),
                ('O4ECU1', 'OBDH4 ERR CNT UHF1 I/F', 0),
                ('O1EOU2', 'OBDH1 ERR CDE UHF2 I/F', 0),
                ('O1ECU2', 'OBDH1 ERR CNT UHF2 I/F', 0),
                ('O1EOSL', 'OBDH1 ERR CDE SM LIM', 0),
                ('O1ECSL', 'OBDH1 ERR CNT SM LIM', 0),
                ('O2EOU2', 'OBDH2 ERR CDE UHF2 I/F', 0),
                ('O2ECU2', 'OBDH2 ERR CNT UHF2 I/F', 0),
                ('O2EOSL', 'OBDH2 ERR CDE SM LIM', 0),
                ('O2ECSL', 'OBDH2 ERR CNT SM LIM', 0),
                ('O3EOU2', 'OBDH3 ERR CDE UHF2 I/F', 0),
                ('O3ECU2', 'OBDH3 ERR CNT UHF2 I/F', 0),
                ('O3EOSL', 'OBDH3 ERR CDE SM LIM', 0),
                ('O3ECSL', 'OBDH3 ERR CNT SM LIM', 0),
                ('O4EOU2', 'OBDH4 ERR CDE UHF2 I/F', 0),
                ('O4ECU2', 'OBDH4 ERR CNT UHF2 I/F', 0),
                ('O4EOSL', 'OBDH4 ERR CDE SM LIM', 0),
                ('O4ECSL', 'OBDH4 ERR CNT SM LIM', 0),
            ),
        },
        'obdh_ext_mem_sts': {
            'table': (
                ('name', 'Name', 0),
                ('O1LP1S', 'OBDH1 LEOP LIST 1 STS', 0),
                ('O1LP2S', 'OBDH1 LEOP LIST 2 STS', 0),
                ('O1LP3S', 'OBDH1 LEOP LIST 3 STS', 0),
                ('O1AS1S', 'OBDH1 ACT SM LIST 1 STS', 0),
                ('O1AS2S', 'OBDH1 ACT SM LIST 2 STS', 0),
                ('O1AS3S', 'OBDH1 ACT SM LIST 3 STS', 0),
                ('O1PASS', 'OBDH1 PAS SM LIST STS', 0),
                ('O1R01S', 'OBDH1 RP LIST 01 STS', 0),
                ('O1R02S', 'OBDH1 RP LIST 02 STS', 0),
                ('O1R03S', 'OBDH1 RP LIST 03 STS', 0),
                ('O1R04S', 'OBDH1 RP LIST 04 STS', 0),
                ('O1R05S', 'OBDH1 RP LIST 05 STS', 0),
                ('O1R06S', 'OBDH1 RP LIST 06 STS', 0),
                ('O1R07S', 'OBDH1 RP LIST 07 STS', 0),
                ('O1R08S', 'OBDH1 RP LIST 08 STS', 0),
                ('O1R09S', 'OBDH1 RP LIST 09 STS', 0),
                ('O1R10S', 'OBDH1 RP LIST 10 STS', 0),
                ('O1R11S', 'OBDH1 RP LIST 11 STS', 0),
                ('O1R12S', 'OBDH1 RP LIST 12 STS', 0),
                ('O1R13S', 'OBDH1 RP LIST 13 STS', 0),
                ('O1R14S', 'OBDH1 RP LIST 14 STS', 0),
                ('O1R15S', 'OBDH1 RP LIST 15 STS', 0),
                ('O1R16S', 'OBDH1 RP LIST 16 STS', 0),
                ('O1CF1S', 'OBDH1 CONFIG 1 STS', 0),
                ('O1CF2S', 'OBDH1 CONFIG 2 STS', 0),
                ('O1CF3S', 'OBDH1 CONFIG 3 STS', 0),
                ('O1PTTS', 'OBDH1 PAS TT LIST STS', 0),
                ('O1ATTS', 'OBDH1 ACT TT LIST STS', 0),
                ('O1TMBS', 'OBDH1 TIME BUF STS', 0),
                ('O1MRS1', 'Reserved (1 bit)', 0),
                ('O1ACFG', 'OBDH1 ACTIVE CONFIG', 0),
                ('O1MSAV', 'OBDH1 MEM STS AVAILABLE', 0),
                ('O1EMBS', 'OBDH1 ERR MGR BUF STS', 0),
                ('O2LP1S', 'OBDH2 LEOP LIST 1 STS', 0),
                ('O2LP2S', 'OBDH2 LEOP LIST 2 STS', 0),
                ('O2LP3S', 'OBDH2 LEOP LIST 3 STS', 0),
                ('O2AS1S', 'OBDH2 ACT SM LIST 1 STS', 0),
                ('O2AS2S', 'OBDH2 ACT SM LIST 2 STS', 0),
                ('O2AS3S', 'OBDH2 ACT SM LIST 3 STS', 0),
                ('O2PASS', 'OBDH2 PAS SM LIST STS', 0),
                ('O2R01S', 'OBDH2 RP LIST 01 STS', 0),
                ('O2R02S', 'OBDH2 RP LIST 02 STS', 0),
                ('O2R03S', 'OBDH2 RP LIST 03 STS', 0),
                ('O2R04S', 'OBDH2 RP LIST 04 STS', 0),
                ('O2R05S', 'OBDH2 RP LIST 05 STS', 0),
                ('O2R06S', 'OBDH2 RP LIST 06 STS', 0),
                ('O2R07S', 'OBDH2 RP LIST 07 STS', 0),
                ('O2R08S', 'OBDH2 RP LIST 08 STS', 0),
                ('O2R09S', 'OBDH2 RP LIST 09 STS', 0),
                ('O2R10S', 'OBDH2 RP LIST 10 STS', 0),
                ('O2R11S', 'OBDH2 RP LIST 11 STS', 0),
                ('O2R12S', 'OBDH2 RP LIST 12 STS', 0),
                ('O2R13S', 'OBDH2 RP LIST 13 STS', 0),
                ('O2R14S', 'OBDH2 RP LIST 14 STS', 0),
                ('O2R15S', 'OBDH2 RP LIST 15 STS', 0),
                ('O2R16S', 'OBDH2 RP LIST 16 STS', 0),
                ('O2CF1S', 'OBDH2 CONFIG 1 STS', 0),
                ('O2CF2S', 'OBDH2 CONFIG 2 STS', 0),
                ('O2CF3S', 'OBDH2 CONFIG 3 STS', 0),
                ('O2PTTS', 'OBDH2 PAS TT LIST STS', 0),
                ('O2ATTS', 'OBDH2 ACT TT LIST STS', 0),
                ('O2TMBS', 'OBDH2 TIME BUF STS', 0),
                ('O2MRS1', 'Reserved (1 bit)', 0),
                ('O2ACFG', 'OBDH2 ACTIVE CONFIG', 0),
                ('O2MSAV', 'OBDH2 MEM STS AVAILABLE', 0),
                ('O2EMBS', 'OBDH2 ERR MGR BUF STS', 0),
                ('O3LP1S', 'OBDH3 LEOP LIST 1 STS', 0),
                ('O3LP2S', 'OBDH3 LEOP LIST 2 STS', 0),
                ('O3LP3S', 'OBDH3 LEOP LIST 3 STS', 0),
                ('O3AS1S', 'OBDH3 ACT SM LIST 1 STS', 0),
                ('O3AS2S', 'OBDH3 ACT SM LIST 2 STS', 0),
                ('O3AS3S', 'OBDH3 ACT SM LIST 3 STS', 0),
                ('O3PASS', 'OBDH3 PAS SM LIST STS', 0),
                ('O3R01S', 'OBDH3 RP LIST 01 STS', 0),
                ('O3R02S', 'OBDH3 RP LIST 02 STS', 0),
                ('O3R03S', 'OBDH3 RP LIST 03 STS', 0),
                ('O3R04S', 'OBDH3 RP LIST 04 STS', 0),
                ('O3R05S', 'OBDH3 RP LIST 05 STS', 0),
                ('O3R06S', 'OBDH3 RP LIST 06 STS', 0),
                ('O3R07S', 'OBDH3 RP LIST 07 STS', 0),
                ('O3R08S', 'OBDH3 RP LIST 08 STS', 0),
                ('O3R09S', 'OBDH3 RP LIST 09 STS', 0),
                ('O3R10S', 'OBDH3 RP LIST 10 STS', 0),
                ('O3R11S', 'OBDH3 RP LIST 11 STS', 0),
                ('O3R12S', 'OBDH3 RP LIST 12 STS', 0),
                ('O3R13S', 'OBDH3 RP LIST 13 STS', 0),
                ('O3R14S', 'OBDH3 RP LIST 14 STS', 0),
                ('O3R15S', 'OBDH3 RP LIST 15 STS', 0),
                ('O3R16S', 'OBDH3 RP LIST 16 STS', 0),
                ('O3CF1S', 'OBDH3 CONFIG 1 STS', 0),
                ('O3CF2S', 'OBDH3 CONFIG 2 STS', 0),
                ('O3CF3S', 'OBDH3 CONFIG 3 STS', 0),
                ('O3PTTS', 'OBDH3 PAS TT LIST STS', 0),
                ('O3ATTS', 'OBDH3 ACT TT LIST STS', 0),
                ('O3TMBS', 'OBDH3 TIME BUF STS', 0),
                ('O3MRS1', 'Reserved (1 bit)', 0),
                ('O3ACFG', 'OBDH3 ACTIVE CONFIG', 0),
                ('O3MSAV', 'OBDH3 MEM STS AVAILABLE', 0),
                ('O3EMBS', 'OBDH3 ERR MGR BUF STS', 0),
                ('O4LP1S', 'OBDH4 LEOP LIST 1 STS', 0),
                ('O4LP2S', 'OBDH4 LEOP LIST 2 STS', 0),
                ('O4LP3S', 'OBDH4 LEOP LIST 3 STS', 0),
                ('O4AS1S', 'OBDH4 ACT SM LIST 1 STS', 0),
                ('O4AS2S', 'OBDH4 ACT SM LIST 2 STS', 0),
                ('O4AS3S', 'OBDH4 ACT SM LIST 3 STS', 0),
                ('O4PASS', 'OBDH4 PAS SM LIST STS', 0),
                ('O4R01S', 'OBDH4 RP LIST 01 STS', 0),
                ('O4R02S', 'OBDH4 RP LIST 02 STS', 0),
                ('O4R03S', 'OBDH4 RP LIST 03 STS', 0),
                ('O4R04S', 'OBDH4 RP LIST 04 STS', 0),
                ('O4R05S', 'OBDH4 RP LIST 05 STS', 0),
                ('O4R06S', 'OBDH4 RP LIST 06 STS', 0),
                ('O4R07S', 'OBDH4 RP LIST 07 STS', 0),
                ('O4R08S', 'OBDH4 RP LIST 08 STS', 0),
                ('O4R09S', 'OBDH4 RP LIST 09 STS', 0),
                ('O4R10S', 'OBDH4 RP LIST 10 STS', 0),
                ('O4R11S', 'OBDH4 RP LIST 11 STS', 0),
                ('O4R12S', 'OBDH4 RP LIST 12 STS', 0),
                ('O4R13S', 'OBDH4 RP LIST 13 STS', 0),
                ('O4R14S', 'OBDH4 RP LIST 14 STS', 0),
                ('O4R15S', 'OBDH4 RP LIST 15 STS', 0),
                ('O4R16S', 'OBDH4 RP LIST 16 STS', 0),
                ('O4CF1S', 'OBDH4 CONFIG 1 STS', 0),
                ('O4CF2S', 'OBDH4 CONFIG 2 STS', 0),
                ('O4CF3S', 'OBDH4 CONFIG 3 STS', 0),
                ('O4PTTS', 'OBDH4 PAS TT LIST STS', 0),
                ('O4ATTS', 'OBDH4 ACT TT LIST STS', 0),
                ('O4TMBS', 'OBDH4 TIME BUF STS', 0),
                ('O4MRS1', 'Reserved (1 bit)', 0),
                ('O4ACFG', 'OBDH4 ACTIVE CONFIG', 0),
                ('O4MSAV', 'OBDH4 MEM STS AVAILABLE', 0),
                ('O4EMBS', 'OBDH4 ERR MGR BUF STS', 0),
                ('O1STDS', 'OBDH1 STD HK STS', 0),
                ('O1OPES', 'OBDH1 PERIPHERAL HK STS', 0),
                ('O1ADSS', 'OBDH1 ADCS STD HK STS', 0),
                ('O1AA1S', 'OBDH1 ACTUATOR1 HK STS', 0),
                ('O1AA2S', 'OBDH1 ACTUATOR2 HK STS', 0),
                ('O1SS1S', 'OBDH1 SUN SENSOR1 HK STS', 0),
                ('O1SS2S', 'OBDH1 SUN SENSOR2 HK STS', 0),
                ('O1THMS', 'OBDH1 THERMAL HK STS', 0),
                ('O1SWIS', 'OBDH1 SW INST HK STS', 0),
                ('O1PWSS', 'OBDH1 PWR SENSOR HK STS', 0),
                ('O1ADES', 'OBDH1 ADCS EXT HK STS', 0),
                ('O1PLDS', 'OBDH1 PDH PLDT HK STS', 0),
                ('O1EXPS', 'OBDH1 PDH EXPDH HK STS', 0),
                ('O1SBDS', 'OBDH1 S-BAND HK STS', 0),
                ('O1MOPS', 'OBDH1 MEMORY OPS STS', 0),
                ('O1AISS', 'OBDH1 AI HK STS', 0),
                ('O1A01S', 'OBDH1 AI CAM APP HK STS', 0),
                ('O1A02S', 'OBDH1 AI WS APP HK STS', 0),
                ('O1A03S', 'OBDH1 AI NS APP HK STS', 0),
                ('O1A04S', 'OBDH1 AI OD APP HK STS', 0),
                ('O1A05S', 'OBDH1 AI AD APP HK STS', 0),
                ('O1A06S', 'OBDH1 AI LD APP HK STS', 0),
                ('O1A07S', 'OBDH1 AI APP07 HK STS', 0),
                ('O1A08S', 'OBDH1 AI APP08 HK STS', 0),
                ('O1A09S', 'OBDH1 AI APP09 HK STS', 0),
                ('O1A10S', 'OBDH1 AI APP10 HK STS', 0),
                ('O1MVSS', 'OBDH1 MVIEW STD HK STS', 0),
                ('O1THRS', 'OBDH1 THRUSTER HK STS', 0),
                ('O1LEOS', 'OBDH1 LEOP HK STS', 0),
                ('O1OECS', 'OBDH1 ERROR CODE HK STS', 0),
                ('O1OMSS', 'OBDH1 MEMORY STS HK STS', 0),
                ('O1OSWS', 'OBDH1 SW UPLD HK STS', 0),
                ('O1OSRS', 'OBDH1 STORAGE REP CHK STS', 0),
                ('O1GPSS', 'OBDH1 GPS HK STS', 0),
                ('O1RSTS', 'OBDH1 RST CNTR HK STS', 0),
                ('O1MVES', 'OBDH1 MVIEW EXT HK STS', 0),
                ('O1RS2S', 'OBDH1 AI CAM CFG HK STS', 0),
                ('O1RS1S', 'OBDH1 RESERVED1 HK STS', 0),
                ('O2STDS', 'OBDH2 STD HK STS', 0),
                ('O2OPES', 'OBDH2 PERIPHERAL HK STS', 0),
                ('O2ADSS', 'OBDH2 ADCS STD HK STS', 0),
                ('O2AA1S', 'OBDH2 ACTUATOR1 HK STS', 0),
                ('O2AA2S', 'OBDH2 ACTUATOR2 HK STS', 0),
                ('O2SS1S', 'OBDH2 SUN SENSOR1 HK STS', 0),
                ('O2SS2S', 'OBDH2 SUN SENSOR2 HK STS', 0),
                ('O2THMS', 'OBDH2 THERMAL HK STS', 0),
                ('O2SWIS', 'OBDH2 SW INST HK STS', 0),
                ('O2PWSS', 'OBDH2 PWR SENSOR HK STS', 0),
                ('O2ADES', 'OBDH2 ADCS EXT HK STS', 0),
                ('O2PLDS', 'OBDH2 PDH PLDT HK STS', 0),
                ('O2EXPS', 'OBDH2 PDH EXPDH HK STS', 0),
                ('O2SBDS', 'OBDH2 S-BAND HK STS', 0),
                ('O2MOPS', 'OBDH2 MEMORY OPS STS', 0),
                ('O2AISS', 'OBDH2 AI HK STS', 0),
                ('O2A01S', 'OBDH2 AI CAM APP HK STS', 0),
                ('O2A02S', 'OBDH2 AI WS APP HK STS', 0),
                ('O2A03S', 'OBDH2 AI NS APP HK STS', 0),
                ('O2A04S', 'OBDH2 AI OD APP HK STS', 0),
                ('O2A05S', 'OBDH2 AI AD APP HK STS', 0),
                ('O2A06S', 'OBDH2 AI LD APP HK STS', 0),
                ('O2A07S', 'OBDH2 AI APP07 HK STS', 0),
                ('O2A08S', 'OBDH2 AI APP08 HK STS', 0),
                ('O2A09S', 'OBDH2 AI APP09 HK STS', 0),
                ('O2A10S', 'OBDH2 AI APP10 HK STS', 0),
                ('O2MVSS', 'OBDH2 MVIEW STD HK STS', 0),
                ('O2THRS', 'OBDH2 THRUSTER HK STS', 0),
                ('O2LEOS', 'OBDH2 LEOP HK STS', 0),
                ('O2OECS', 'OBDH2 ERROR CODE HK STS', 0),
                ('O2OMSS', 'OBDH2 MEMORY STS HK STS', 0),
                ('O2OSWS', 'OBDH2 SW UPLD HK STS', 0),
                ('O2OSRS', 'OBDH2 STORAGE REP CHK STS', 0),
                ('O2GPSS', 'OBDH2 GPS HK STS', 0),
                ('O2RSTS', 'OBDH2 RST CNTR HK STS', 0),
                ('O2MVES', 'OBDH2 MVIEW EXT HK STS', 0),
                ('O2RS2S', 'OBDH2 AI CAM CFG HK STS', 0),
                ('O2RS1S', 'OBDH2 RESERVED1 HK STS', 0),
                ('O3STDS', 'OBDH3 STD HK STS', 0),
                ('O3OPES', 'OBDH3 PERIPHERAL HK STS', 0),
                ('O3ADSS', 'OBDH3 ADCS STD HK STS', 0),
                ('O3AA1S', 'OBDH3 ACTUATOR1 HK STS', 0),
                ('O3AA2S', 'OBDH3 ACTUATOR2 HK STS', 0),
                ('O3SS1S', 'OBDH3 SUN SENSOR1 HK STS', 0),
                ('O3SS2S', 'OBDH3 SUN SENSOR2 HK STS', 0),
                ('O3THMS', 'OBDH3 THERMAL HK STS', 0),
                ('O3SWIS', 'OBDH3 SW INST HK STS', 0),
                ('O3PWSS', 'OBDH3 PWR SENSOR HK STS', 0),
                ('O3ADES', 'OBDH3 ADCS EXT HK STS', 0),
                ('O3PLDS', 'OBDH3 PDH PLDT HK STS', 0),
                ('O3EXPS', 'OBDH3 PDH EXPDH HK STS', 0),
                ('O3SBDS', 'OBDH3 S-BAND HK STS', 0),
                ('O3MOPS', 'OBDH3 MEMORY OPS STS', 0),
                ('O3AISS', 'OBDH3 AI HK STS', 0),
                ('O3A01S', 'OBDH3 AI CAM APP HK STS', 0),
                ('O3A02S', 'OBDH3 AI WS APP HK STS', 0),
                ('O3A03S', 'OBDH3 AI NS APP HK STS', 0),
                ('O3A04S', 'OBDH3 AI OD APP HK STS', 0),
                ('O3A05S', 'OBDH3 AI AD APP HK STS', 0),
                ('O3A06S', 'OBDH3 AI LD APP HK STS', 0),
                ('O3A07S', 'OBDH3 AI APP07 HK STS', 0),
                ('O3A08S', 'OBDH3 AI APP08 HK STS', 0),
                ('O3A09S', 'OBDH3 AI APP09 HK STS', 0),
                ('O3A10S', 'OBDH3 AI APP10 HK STS', 0),
                ('O3MVSS', 'OBDH3 MVIEW STD HK STS', 0),
                ('O3THRS', 'OBDH3 THRUSTER HK STS', 0),
                ('O3LEOS', 'OBDH3 LEOP HK STS', 0),
                ('O3OECS', 'OBDH3 ERROR CODE HK STS', 0),
                ('O3OMSS', 'OBDH3 MEMORY STS HK STS', 0),
                ('O3OSWS', 'OBDH3 SW UPLD HK STS', 0),
                ('O3OSRS', 'OBDH3 STORAGE REP CHK STS', 0),
                ('O3GPSS', 'OBDH3 GPS HK STS', 0),
                ('O3RSTS', 'OBDH3 RST CNTR HK STS', 0),
                ('O3MVES', 'OBDH3 MIVEW EXT HK STS', 0),
                ('O3RS2S', 'OBDH3 AI CAM CFG HK STS', 0),
                ('O3RS1S', 'OBDH3 RESERVED1 HK STS', 0),
                ('O4STDS', 'OBDH4 STD HK STS', 0),
                ('O4OPES', 'OBDH4 PERIPHERAL HK STS', 0),
                ('O4ADSS', 'OBDH4 ADCS STD HK STS', 0),
                ('O4AA1S', 'OBDH4 ACTUATOR1 HK STS', 0),
                ('O4AA2S', 'OBDH4 ACTUATOR2 HK STS', 0),
                ('O4SS1S', 'OBDH4 SUN SENSOR1 HK STS', 0),
                ('O4SS2S', 'OBDH4 SUN SENSOR2 HK STS', 0),
                ('O4THMS', 'OBDH4 THERMAL HK STS', 0),
                ('O4SWIS', 'OBDH4 SW INST HK STS', 0),
                ('O4PWSS', 'OBDH4 PWR SENSOR HK STS', 0),
                ('O4ADES', 'OBDH4 ADCS EXT HK STS', 0),
                ('O4PLDS', 'OBDH4 PDH PLDT HK STS', 0),
                ('O4EXPS', 'OBDH4 PDH EXPDH HK STS', 0),
                ('O4SBDS', 'OBDH4 S-BAND HK STS', 0),
                ('O4MOPS', 'OBDH4 MEMORY OPS STS', 0),
                ('O4AISS', 'OBDH4 AI HK STS', 0),
                ('O4A01S', 'OBDH4 AI CAM APP HK STS', 0),
                ('O4A02S', 'OBDH4 AI WS APP HK STS', 0),
                ('O4A03S', 'OBDH4 AI NS APP HK STS', 0),
                ('O4A04S', 'OBDH4 AI OD APP HK STS', 0),
                ('O4A05S', 'OBDH4 AI AD APP HK STS', 0),
                ('O4A06S', 'OBDH4 AI LD APP HK STS', 0),
                ('O4A07S', 'OBDH4 AI APP07 HK STS', 0),
                ('O4A08S', 'OBDH4 AI APP08 HK STS', 0),
                ('O4A09S', 'OBDH4 AI APP09 HK STS', 0),
                ('O4A10S', 'OBDH4 AI APP10 HK STS', 0),
                ('O4MVSS', 'OBDH4 MVIEW STD HK STS', 0),
                ('O4THRS', 'OBDH4 THRUSTER HK STS', 0),
                ('O4LEOS', 'OBDH4 LEOP HK STS', 0),
                ('O4OECS', 'OBDH4 ERROR CODE HK STS', 0),
                ('O4OMSS', 'OBDH4 MEMORY STS HK STS', 0),
                ('O4OSWS', 'OBDH4 SW UPLD HK STS', 0),
                ('O4OSRS', 'OBDH4 STORAGE REP CHK STS', 0),
                ('O4GPSS', 'OBDH4 GPS HK STS', 0),
                ('O4RSTS', 'OBDH4 RST CNTR HK STS', 0),
                ('O4MVES', 'OBDH4 MVIEW EXT HK STS', 0),
                ('O4RS2S', 'OBDH4 AI CAM CFG HK STS', 0),
                ('O4RS1S', 'OBDH4 RESERVED1 HK STS', 0),
            ),
        },
        'obdh_ext_periph_sts': {
            'table': (
                ('name', 'Name', 0),
                ('O1CN1S', 'OBDH1 CAN BUS1 STATUS', 0),
                ('O1CN2S', 'OBDH1 CAN BUS2 STATUS', 0),
                ('O1SY1S', 'OBDH1 SYNCH1 STATUS', 0),
                ('O1SY2S', 'OBDH1 SYNCH2 STATUS', 0),
                ('O1SY3S', 'OBDH1 SYNCH3 STATUS', 0),
                ('O1SY4S', 'OBDH1 SYNCH4 STATUS', 0),
                ('O1LC1S', 'OBDH1 LINK CAN1 STATUS', 0),
                ('O1LC2S', 'OBDH1 LINK CAN2 STATUS', 0),
                ('O1RA1S', 'OBDH1 SRAM1 STATUS', 0),
                ('O1RA2S', 'OBDH1 SRAM2 STATUS', 0),
                ('O1PN1S', 'OBDH1 PAR NOR1 STATUS', 0),
                ('O1PN2S', 'OBDH1 PAR NOR2 STATUS', 0),
                ('O1SNFS', 'OBDH1 SPI NOR STATUS', 0),
                ('O1PSAV', 'OBDH1 PRPH STS AVAILABLE', 0),
                ('O1CN1R', 'OBDH1 CAN BUS1 RX ERR CNT', 0),
                ('O1CN1T', 'OBDH1 CAN BUS1 TX ERR CNT', 0),
                ('O1CN2R', 'OBDH1 CAN BUS2 RX ERR CNT', 0),
                ('O1C2TE', 'OBDH1 CAN BUS2 TX ERR CNT', 0),
                ('O1LC1B', 'OBDH1 LINK CAN1 BUFF HLT', 0),
                ('O1LC2B', 'OBDH1 LINK CAN2 BUFF HLT', 0),
                ('O2CN1S', 'OBDH2 CAN BUS1 STATUS', 0),
                ('O2CN2S', 'OBDH2 CAN BUS2 STATUS', 0),
                ('O2SY1S', 'OBDH2 SYNCH1 STATUS', 0),
                ('O2SY2S', 'OBDH2 SYNCH2 STATUS', 0),
                ('O2SY3S', 'OBDH2 SYNCH3 STATUS', 0),
                ('O2SY4S', 'OBDH2 SYNCH4 STATUS', 0),
                ('O2LC1S', 'OBDH2 LINK CAN1 STATUS', 0),
                ('O2LC2S', 'OBDH2 LINK CAN2 STATUS', 0),
                ('O2RA1S', 'OBDH2 SRAM1 STATUS', 0),
                ('O2RA2S', 'OBDH2 SRAM2 STATUS', 0),
                ('O2PN1S', 'OBDH2 PAR NOR1 STATUS', 0),
                ('O2PN2S', 'OBDH2 PAR NOR2 STATUS', 0),
                ('O2SNFS', 'OBDH2 SPI NOR STATUS', 0),
                ('O2PSAV', 'OBDH2 PRPH STS AVAILABLE', 0),
                ('O2CN1R', 'OBDH2 CAN BUS1 RX ERR CNT', 0),
                ('O2CN1T', 'OBDH2 CAN BUS1 TX ERR CNT', 0),
                ('O2CN2R', 'OBDH2 CAN BUS2 RX ERR CNT', 0),
                ('O2C2TE', 'OBDH2 CAN BUS2 TX ERR CNT', 0),
                ('O2LC1B', 'OBDH2 LINK CAN1 BUFF HLT', 0),
                ('O2LC2B', 'OBDH2 LINK CAN2 BUFF HLT', 0),
                ('O3CN1S', 'OBDH3 CAN BUS1 STATUS', 0),
                ('O3CN2S', 'OBDH3 CAN BUS2 STATUS', 0),
                ('O3SY1S', 'OBDH3 SYNCH1 STATUS', 0),
                ('O3SY2S', 'OBDH3 SYNCH2 STATUS', 0),
                ('O3SY3S', 'OBDH3 SYNCH3 STATUS', 0),
                ('O3SY4S', 'OBDH3 SYNCH4 STATUS', 0),
                ('O3LC1S', 'OBDH3 LINK CAN1 STATUS', 0),
                ('O3LC2S', 'OBDH3 LINK CAN2 STATUS', 0),
                ('O3RA1S', 'OBDH3 SRAM1 STATUS', 0),
                ('O3RA2S', 'OBDH3 SRAM2 STATUS', 0),
                ('O3PN1S', 'OBDH3 PAR NOR1 STATUS', 0),
                ('O3PN2S', 'OBDH3 PAR NOR2 STATUS', 0),
                ('O3SNFS', 'OBDH3 SPI NOR STATUS', 0),
                ('O3PSAV', 'OBDH3 PRPH STS AVAILABLE', 0),
                ('O3CN1R', 'OBDH3 CAN BUS1 RX ERR CNT', 0),
                ('O3CN1T', 'OBDH3 CAN BUS1 TX ERR CNT', 0),
                ('O3CN2R', 'OBDH3 CAN BUS2 RX ERR CNT', 0),
                ('O3C2TE', 'OBDH3 CAN BUS2 TX ERR CNT', 0),
                ('O3LC1B', 'OBDH3 LINK CAN1 BUFF HLT', 0),
                ('O3LC2B', 'OBDH3 LINK CAN2 BUFF HLT', 0),
                ('O4CN1S', 'OBDH4 CAN BUS1 STATUS', 0),
                ('O4CN2S', 'OBDH4 CAN BUS2 STATUS', 0),
                ('O4SY1S', 'OBDH4 SYNCH1 STATUS', 0),
                ('O4SY2S', 'OBDH4 SYNCH2 STATUS', 0),
                ('O4SY3S', 'OBDH4 SYNCH3 STATUS', 0),
                ('O4SY4S', 'OBDH4 SYNCH4 STATUS', 0),
                ('O4LC1S', 'OBDH4 LINK CAN1 STATUS', 0),
                ('O4LC2S', 'OBDH4 LINK CAN2 STATUS', 0),
                ('O4RA1S', 'OBDH4 SRAM1 STATUS', 0),
                ('O4RA2S', 'OBDH4 SRAM2 STATUS', 0),
                ('O4PN1S', 'OBDH4 PAR NOR1 STATUS', 0),
                ('O4PN2S', 'OBDH4 PAR NOR2 STATUS', 0),
                ('O4SNFS', 'OBDH4 SPI NOR STATUS', 0),
                ('O4PSAV', 'OBDH4 PRPH STS AVAILABLE', 0),
                ('O4CN1R', 'OBDH4 CAN BUS1 RX ERR CNT', 0),
                ('O4CN1T', 'OBDH4 CAN BUS1 TX ERR CNT', 0),
                ('O4CN2R', 'OBDH4 CAN BUS2 RX ERR CNT', 0),
                ('O4C2TE', 'OBDH4 CAN BUS2 TX ERR CNT', 0),
                ('O4LC1B', 'OBDH4 LINK CAN1 BUFF HLT', 0),
                ('O4LC2B', 'OBDH4 LINK CAN2 BUFF HLT', 0),
                ('O1CN1O', 'OBDH1 CAN BUS1 ERR CDE', 0),
                ('O1CN1C', 'OBDH1 CAN BUS1 ERR CNT', 0),
                ('O1CN2O', 'OBDH1 CAN BUS2 ERR CDE', 0),
                ('O1CN2C', 'OBDH1 CAN BUS2 ERR CNT', 0),
                ('O1SY1O', 'OBDH1 SYNCH1 ERR CDE', 0),
                ('O1SY1C', 'OBDH1 SYNCH1 ERR CNT', 0),
                ('O1SY2O', 'OBDH1 SYNCH2 ERR CDE', 0),
                ('O1SY2C', 'OBDH1 SYNCH2 ERR CNT', 0),
                ('O1SY3O', 'OBDH1 SYNCH3 ERR CDE', 0),
                ('O1SY3C', 'OBDH1 SYNCH3 ERR CNT', 0),
                ('O1SY4O', 'OBDH1 SYNCH4 ERR CDE', 0),
                ('O1SY4C', 'OBDH1 SYNCH4 ERR CNT', 0),
                ('O1LC1O', 'OBDH1 LINK CAN1 ERR CDE', 0),
                ('O1LC1C', 'OBDH1 LINK CAN1 ERR CNT', 0),
                ('O1LC2O', 'OBDH1 LINK CAN2 ERR CDE', 0),
                ('O1LC2C', 'OBDH1 LINK CAN2 ERR CNT', 0),
                ('O2CN1O', 'OBDH2 CAN BUS1 ERR CDE', 0),
                ('O2CN1C', 'OBDH2 CAN BUS1 ERR CNT', 0),
                ('O2CN2O', 'OBDH2 CAN BUS2 ERR CDE', 0),
                ('O2CN2C', 'OBDH2 CAN BUS2 ERR CNT', 0),
                ('O2SY1O', 'OBDH2 SYNCH1 ERR CDE', 0),
                ('O2SY1C', 'OBDH2 SYNCH1 ERR CNT', 0),
                ('O2SY2O', 'OBDH2 SYNCH2 ERR CDE', 0),
                ('O2SY2C', 'OBDH2 SYNCH2 ERR CNT', 0),
                ('O2SY3O', 'OBDH2 SYNCH3 ERR CDE', 0),
                ('O2SY3C', 'OBDH2 SYNCH3 ERR CNT', 0),
                ('O2SY4O', 'OBDH2 SYNCH4 ERR CDE', 0),
                ('O2SY4C', 'OBDH2 SYNCH4 ERR CNT', 0),
                ('O2LC1O', 'OBDH2 LINK CAN1 ERR CDE', 0),
                ('O2LC1C', 'OBDH2 LINK CAN1 ERR CNT', 0),
                ('O2LC2O', 'OBDH2 LINK CAN2 ERR CDE', 0),
                ('O2LC2C', 'OBDH2 LINK CAN2 ERR CNT', 0),
                ('O3CN1O', 'OBDH3 CAN BUS1 ERR CDE', 0),
                ('O3CN1C', 'OBDH3 CAN BUS1 ERR CNT', 0),
                ('O3CN2O', 'OBDH3 CAN BUS2 ERR CDE', 0),
                ('O3CN2C', 'OBDH3 CAN BUS2 ERR CNT', 0),
                ('O3SY1O', 'OBDH3 SYNCH1 ERR CDE', 0),
                ('O3SY1C', 'OBDH3 SYNCH1 ERR CNT', 0),
                ('O3SY2O', 'OBDH3 SYNCH2 ERR CDE', 0),
                ('O3SY2C', 'OBDH3 SYNCH2 ERR CNT', 0),
                ('O3SY3O', 'OBDH3 SYNCH3 ERR CDE', 0),
                ('O3SY3C', 'OBDH3 SYNCH3 ERR CNT', 0),
                ('O3SY4O', 'OBDH3 SYNCH4 ERR CDE', 0),
                ('O3SY4C', 'OBDH3 SYNCH4 ERR CNT', 0),
                ('O3LC1O', 'OBDH3 LINK CAN1 ERR CDE', 0),
                ('O3LC1C', 'OBDH3 LINK CAN1 ERR CNT', 0),
                ('O3LC2O', 'OBDH3 LINK CAN2 ERR CDE', 0),
                ('O3LC2C', 'OBDH3 LINK CAN2 ERR CNT', 0),
                ('O4CN1O', 'OBDH4 CAN BUS1 ERR CDE', 0),
                ('O4CN1C', 'OBDH4 CAN BUS1 ERR CNT', 0),
                ('O4CN2O', 'OBDH4 CAN BUS2 ERR CDE', 0),
                ('O4CN2C', 'OBDH4 CAN BUS2 ERR CNT', 0),
                ('O4SY1O', 'OBDH4 SYNCH1 ERR CDE', 0),
                ('O4SY1C', 'OBDH4 SYNCH1 ERR CNT', 0),
                ('O4SY2O', 'OBDH4 SYNCH2 ERR CDE', 0),
                ('O4SY2C', 'OBDH4 SYNCH2 ERR CNT', 0),
                ('O4SY3O', 'OBDH4 SYNCH3 ERR CDE', 0),
                ('O4SY3C', 'OBDH4 SYNCH3 ERR CNT', 0),
                ('O4SY4O', 'OBDH4 SYNCH4 ERR CDE', 0),
                ('O4SY4C', 'OBDH4 SYNCH4 ERR CNT', 0),
                ('O4LC1O', 'OBDH4 LINK CAN1 ERR CDE', 0),
                ('O4LC1C', 'OBDH4 LINK CAN1 ERR CNT', 0),
                ('O4LC2O', 'OBDH4 LINK CAN2 ERR CDE', 0),
                ('O4LC2C', 'OBDH4 LINK CAN2 ERR CNT', 0),
                ('O1RSTP', 'OBDH1 RST PROTECT STATUS', 0),
                ('O1B1RS', 'OBDH1 BUS1 RST STATUS', 0),
                ('O1B2RS', 'OBDH1 BUS2 RST STATUS', 0),
                ('O1ONFP', 'OBDH1 ON OFF PROTECT', 0),
                ('O1ONFS', 'OBDH1 ON OFF SLAVE', 0),
                ('O1RTCI', 'OBDH1 RTC STATUS', 0),
                ('O1RTCS', 'OBDH1 RTC CLK SRC', 0),
                ('O1SCLS', 'OBDH1 SYS CLK SRC', 0),
                ('O1FTEX', 'OBDH1 FWRD TIME EXP FRAME', 0),
                ('O2RSTP', 'OBDH2 RST PROTECT STATUS', 0),
                ('O2B1RS', 'OBDH2 BUS1 RST STATUS', 0),
                ('O2B2RS', 'OBDH2 BUS2 RST STATUS', 0),
                ('O2ONFP', 'OBDH2 ON OFF PROTECT', 0),
                ('O2ONFS', 'OBDH2 ON OFF SLAVE', 0),
                ('O2RTCI', 'OBDH2 RTC STATUS', 0),
                ('O2RTCS', 'OBDH2 RTC CLK SRC', 0),
                ('O2SCLS', 'OBDH2 SYS CLK SRC', 0),
                ('O2FTEX', 'OBDH2 FWRD TIME EXP FRAME', 0),
                ('O3RSTP', 'OBDH3 RST PROTECT STATUS', 0),
                ('O3B1RS', 'OBDH3 BUS1 RST STATUS', 0),
                ('O3B2RS', 'OBDH3 BUS2 RST STATUS', 0),
                ('O3ONFP', 'OBDH3 ON OFF PROTECT', 0),
                ('O3ONFS', 'OBDH3 ON OFF SLAVE', 0),
                ('O3RTCI', 'OBDH3 RTC STATUS', 0),
                ('O3RTCS', 'OBDH3 RTC CLK SRC', 0),
                ('O3SCLS', 'OBDH3 SYS CLK SRC', 0),
                ('O3FTEX', 'OBDH3 FWRD TIME EXP FRAME', 0),
                ('O4RSTP', 'OBDH4 RST PROTECT STATUS', 0),
                ('O4B1RS', 'OBDH4 BUS1 RST STATUS', 0),
                ('O4B2RS', 'OBDH4 BUS2 RST STATUS', 0),
                ('O4ONFP', 'OBDH4 ON OFF PROTECT', 0),
                ('O4ONFS', 'OBDH4 ON OFF SLAVE', 0),
                ('O4RTCI', 'OBDH4 RTC STATUS', 0),
                ('O4RTCS', 'OBDH4 RTC CLK SRC', 0),
                ('O4SCLS', 'OBDH4 SYS CLK SRC', 0),
                ('O4FTEX', 'OBDH4 FWRD TIME EXP FRAME', 0),
                ('O1RMC2', 'OBDH1 RM COM SRC W OBDH2', 0),
                ('O1RMC3', 'OBDH1 RM COM SRC W OBDH3', 0),
                ('O1RMC4', 'OBDH1 RM COM SRC W OBDH4', 0),
                ('O1RMHW', 'OBDH1 RM MON HW ID', 0),
                ('O1RPDS', 'OBDH1 RM PDH I/F FLAG STS', 0),
                ('O1RSIS', 'OBDH1 RM SW INSTLR IF STS', 0),
                ('O1RSCS', 'OBDH1 RM SBAND CNTRLR STS', 0),
                ('O1RSUS', 'OBDH1 RM SW UPLD RCVR STS', 0),
                ('O2RMC1', 'OBDH2 RM COM SRC W OBDH1', 0),
                ('O2RMC3', 'OBDH2 RM COM SRC W OBDH3', 0),
                ('O2RMC4', 'OBDH2 RM COM SRC W OBDH4', 0),
                ('O2RMHW', 'OBDH2 RM MON HW ID', 0),
                ('O2RPDS', 'OBDH2 RM PDH I/F FLAG STS', 0),
                ('O2RSIS', 'OBDH2 RM SW INSTLR IF STS', 0),
                ('O2RSCS', 'OBDH2 RM SBAND CNTRLR STS', 0),
                ('O2RSUS', 'OBDH2 RM SW UPLD RCVR STS', 0),
                ('O3RMC1', 'OBDH3 RM COM SRC W OBDH1', 0),
                ('O3RMC2', 'OBDH3 RM COM SRC W OBDH2', 0),
                ('O3RMC4', 'OBDH3 RM COM SRC W OBDH4', 0),
                ('O3RMHW', 'OBDH3 RM MON HW ID', 0),
                ('O3RPDS', 'OBDH3 RM PDH I/F FLAG STS', 0),
                ('O3RSIS', 'OBDH3 RM SW INSTLR IF STS', 0),
                ('O3RSCS', 'OBDH3 RM SBAND CNTRLR STS', 0),
                ('O3RSUS', 'OBDH3 RM SW UPLD RCVR STS', 0),
                ('O4RMC1', 'OBDH4 RM COM SRC W OBDH1', 0),
                ('O4RMC2', 'OBDH4 RM COM SRC W OBDH2', 0),
                ('O4RMC3', 'OBDH4 RM COM SRC W OBDH3', 0),
                ('O4RMHW', 'OBDH4 RM MON HW ID', 0),
                ('O4RPDS', 'OBDH4 RM PDH I/F FLAG STS', 0),
                ('O4RSIS', 'OBDH4 RM SW INSTLR IF STS', 0),
                ('O4RSCS', 'OBDH4 RM SBAND CNTRLR STS', 0),
                ('O4RSUS', 'OBDH4 RM SW UPLD RCVR STS', 0),
                ('O1PN1O', 'OBDH1 PAR NOR1 ERR CDE', 0),
                ('O1PN1C', 'OBDH1 PAR NOR1 ERR CNT', 0),
                ('O1PN2O', 'OBDH1 PAR NOR2 ERR CDE', 0),
                ('O1PN2C', 'OBDH1 PAR NOR2 ERR CNT', 0),
                ('O1SNFO', 'OBDH1 SPI NOR ERR CDE', 0),
                ('O1SNFC', 'OBDH1 SPI NOR ERR CNT', 0),
                ('O1RA1O', 'OBDH1 SRAM1 ERR CDE', 0),
                ('O1RA1C', 'OBDH1 SRAM1 ERR CNT', 0),
                ('O1RA2O', 'OBDH1 SRAM2 ERR CDE', 0),
                ('O1RA2C', 'OBDH1 SRAM2 ERR CNT', 0),
                ('O2PN1O', 'OBDH2 PAR NOR1 ERR CDE', 0),
                ('O2PN1C', 'OBDH2 PAR NOR1 ERR CNT', 0),
                ('O2PN2O', 'OBDH2 PAR NOR2 ERR CDE', 0),
                ('O2PN2C', 'OBDH2 PAR NOR2 ERR CNT', 0),
                ('O2SNFO', 'OBDH2 SPI NOR ERR CDE', 0),
                ('O2SNFC', 'OBDH2 SPI NOR ERR CNT', 0),
                ('O2RA1O', 'OBDH2 SRAM1 ERR CDE', 0),
                ('O2RA1C', 'OBDH2 SRAM1 ERR CNT', 0),
                ('O2RA2O', 'OBDH2 SRAM2 ERR CDE', 0),
                ('O2RA2C', 'OBDH2 SRAM2 ERR CNT', 0),
                ('O3PN1O', 'OBDH3 PAR NOR1 ERR CDE', 0),
                ('O3PN1C', 'OBDH3 PAR NOR1 ERR CNT', 0),
                ('O3PN2O', 'OBDH3 PAR NOR2 ERR CDE', 0),
                ('O3PN2C', 'OBDH3 PAR NOR2 ERR CNT', 0),
                ('O3SNFO', 'OBDH3 SPI NOR ERR CDE', 0),
                ('O3SNFC', 'OBDH3 SPI NOR ERR CNT', 0),
                ('O3RA1O', 'OBDH3 SRAM1 ERR CDE', 0),
                ('O3RA1C', 'OBDH3 SRAM1 ERR CNT', 0),
                ('O3RA2O', 'OBDH3 SRAM2 ERR CDE', 0),
                ('O3RA2C', 'OBDH3 SRAM2 ERR CNT', 0),
                ('O4PN1O', 'OBDH4 PAR NOR1 ERR CDE', 0),
                ('O4PN1C', 'OBDH4 PAR NOR1 ERR CNT', 0),
                ('O4PN2O', 'OBDH4 PAR NOR2 ERR CDE', 0),
                ('O4PN2C', 'OBDH4 PAR NOR2 ERR CNT', 0),
                ('O4SNFO', 'OBDH4 SPI NOR ERR CDE', 0),
                ('O4SNFC', 'OBDH4 SPI NOR ERR CNT', 0),
                ('O4RA1O', 'OBDH4 SRAM1 ERR CDE', 0),
                ('O4RA1C', 'OBDH4 SRAM1 ERR CNT', 0),
                ('O4RA2O', 'OBDH4 SRAM2 ERR CDE', 0),
                ('O4RA2C', 'OBDH4 SRAM2 ERR CNT', 0),
                ('O1P2RG', 'OBDH1 PCU12V RST GPIO', 0),
                ('O1P5RG', 'OBDH1 PCU5V RST GPIO', 0),
                ('O1VHRG', 'OBDH1 VHF RST GPIO', 0),
                ('O1UHRG', 'OBDH1 UHF RST GPIO', 0),
                ('O1FREQ', 'OBDH1 CPU FREQUENCY, MHz', 0),
                ('O1CBVL', 'OBDH1 CARRIER BOARD VLTG, V', 0),
                ('O1HOFM', 'OBDH1 ONLINE HK FWD MODE', 0),
                ('O1GNRG', 'OBDH1 GNSS RST GPIO', 0),
                ('O2P2RG', 'OBDH2 PCU12V RST GPIO', 0),
                ('O2P5RG', 'OBDH2 PCU5V RST GPIO', 0),
                ('O2VHRG', 'OBDH2 VHF RST GPIO', 0),
                ('O2UHRG', 'OBDH2 UHF RST GPIO', 0),
                ('O2FREQ', 'OBDH2 CPU FREQUENCY, MHz', 0),
                ('O2CBVL', 'OBDH2 CARRIER BOARD VLTG, V', 0),
                ('O2HOFM', 'OBDH2 ONLINE HK FWD MODE', 0),
                ('O2GNRG', 'OBDH2 GNSS RST GPIO', 0),
                ('O3P2RG', 'OBDH3 PCU12V RST GPIO', 0),
                ('O3P5RG', 'OBDH3 PCU5V RST GPIO', 0),
                ('O3VHRG', 'OBDH3 VHF RST GPIO', 0),
                ('O3UHRG', 'OBDH3 UHF RST GPIO', 0),
                ('O3FREQ', 'OBDH3 CPU FREQUENCY, MHz', 0),
                ('O3CBVL', 'OBDH3 CARRIER BOARD VLTG, V', 0),
                ('O3HOFM', 'OBDH3 ONLINE HK FWD MODE', 0),
                ('O3GNRG', 'OBDH3 GNSS RST GPIO', 0),
                ('O4P2RG', 'OBDH4 PCU12V RST GPIO', 0),
                ('O4P5RG', 'OBDH4 PCU5V RST GPIO', 0),
                ('O4VHRG', 'OBDH4 VHF RST GPIO', 0),
                ('O4UHRG', 'OBDH4 UHF RST GPIO', 0),
                ('O4FREQ', 'OBDH4 CPU FREQUENCY, MHz', 0),
                ('O4CBVL', 'OBDH4 CARRIER BOARD VLTG, V', 0),
                ('O4HOFM', 'OBDH4 ONLINE HK FWD MODE', 0),
                ('O4GNRG', 'OBDH4 GNSS RST GPIO', 0),
            ),
        },
        'obdh_sto_rep_chk_hk': {
            'table': (
                ('name', 'Name', 0),
                ('O1RCAV', 'OBDH1 STO REP CHK AVAIL', 0),
                ('O1RCST', 'OBDH1 STO REP CHK STATE', 0),
                ('O1RCPG', 'OBDH1 STO REP CHK PRGRS, %', 0),
                ('O1RCEO', 'OBDH1 STO REP CHK ERR CDE', 0),
                ('O1RCEC', 'OBDH1 STO REP CHK ERR CNT', 0),
                ('O1RCRC', 'OBDH1 STO REP CHK CRC', 0),
                ('O2RCAV', 'OBDH2 STO REP CHK AVAIL', 0),
                ('O2RCST', 'OBDH2 STO REP CHK STATE', 0),
                ('O2RCPG', 'OBDH2 STO REP CHK PRGRS, %', 0),
                ('O2RCEO', 'OBDH2 STO REP CHK ERR CDE', 0),
                ('O2RCEC', 'OBDH2 STO REP CHK ERR CNT', 0),
                ('O2RCRC', 'OBDH2 STO REP CHK CRC', 0),
                ('O3RCAV', 'OBDH3 STO REP CHK AVAIL', 0),
                ('O3RCST', 'OBDH3 STO REP CHK STATE', 0),
                ('O3RCPG', 'OBDH3 STO REP CHK PRGRS, %', 0),
                ('O3RCEO', 'OBDH3 STO REP CHK ERR CDE', 0),
                ('O3RCEC', 'OBDH3 STO REP CHK ERR CNT', 0),
                ('O3RCRC', 'OBDH3 STO REP CHK CRC', 0),
                ('O4RCAV', 'OBDH4 STO REP CHK AVAIL', 0),
                ('O4RCST', 'OBDH4 STO REP CHK STATE', 0),
                ('O4RCPG', 'OBDH4 STO REP CHK PRGRS, %', 0),
                ('O4RCEO', 'OBDH4 STO REP CHK ERR CDE', 0),
                ('O4RCEC', 'OBDH4 STO REP CHK ERR CNT', 0),
                ('O4RCRC', 'OBDH4 STO REP CHK CRC', 0),
            ),
        },
        'obdh_sw_upld': {
            'table': (
                ('name', 'Name', 0),
                ('OSWURS', 'SW UPLD RESERVED (1 bit)', 0),
                ('OSWUAV', 'SW UPLD AVAILABLE FLAG', 0),
                ('OSWUHW', 'SW UPLD HARDWARE ID', 0),
                ('OSWUIT', 'SW UPLD IGNORE TC CNTR', 0),
                ('OSWUST', 'SW UPLD STATE', 0),
                ('OSWUPG', 'SW UPLD PROGRESS, %', 0),
                ('OSWUEO', 'SW UPLD ERROR CODE', 0),
                ('OSWUEC', 'SW UPLD ERROR CNTR', 0),
                ('OSWUSL', 'SW UPLD SEGMENT LEN', 0),
                ('OSWULS', 'SW UPLD LAST RCVD SGMNT', 0),
                ('OSWULC', 'SW UPLD MISNG SGMNT CNT', 0),
                ('OSWUFL', 'SW UPLD FIRST LOST SGMNT', 0),
            ),
        },
        'obdh_ext_hk_buf_cnt': {
            'table': (
                ('name', 'Name', 0),
                ('OAHKHW', 'OBDH HK BUFFER HW ID', 0),
                ('OASTDL', 'OBDH STD HK LEN', 0),
                ('OAOPEL', 'OBDH PERIPHERAL HK LEN', 0),
                ('OAADSL', 'OBDH ADCS STD HK LEN', 0),
                ('OAAA1L', 'OBDH ACTUATOR1 HK LEN', 0),
                ('OAAA2L', 'OBDH ACTUATOR2 HK LEN', 0),
                ('OASS1L', 'OBDH SUN SENSOR1 HK LEN', 0),
                ('OASS2L', 'OBDH SUN SENSOR2 HK LEN', 0),
                ('OATH1L', 'OBDH THERMAL HK LEN', 0),
                ('OSWINL', 'OBDH SW INST HK LEN', 0),
                ('OAPS1L', 'OBDH PWR SENSOR HK LEN', 0),
                ('OAADEL', 'OBDH ADCS EXT HK LEN', 0),
                ('OAPLDL', 'OBDH PDH PLDT HK LEN', 0),
                ('OAEXPL', 'OBDH PDH EXPDH HK LEN', 0),
                ('OASBDL', 'OBDH S-BAND HK LEN', 0),
                ('OAMOPL', 'OBDH MEMORY OPS HK LEN', 0),
                ('OAISTL', 'OBDH AI STD HK LEN', 0),
                ('OAI01L', 'OBDH AI CAM APP HK LEN', 0),
                ('OAI02L', 'OBDH AI WS APP HK LEN', 0),
                ('OAI03L', 'OBDH AI NS APP HK LEN', 0),
                ('OAI04L', 'OBDH AI OD APP HK LEN', 0),
                ('OAI05L', 'OBDH AI AD APP HK LEN', 0),
                ('OAI06L', 'OBDH AI LD APP HK LEN', 0),
                ('OAI07L', 'OBDH AI APP07 HK LEN', 0),
                ('OAI08L', 'OBDH AI APP08 HK LEN', 0),
                ('OAI09L', 'OBDH AI APP09 HK LEN', 0),
                ('OAI10L', 'OBDH AI APP10 HK LEN', 0),
                ('OAMVSL', 'OBDH MVIEW STD HK LEN', 0),
                ('OATHRL', 'OBDH THRUSTER HK LEN', 0),
                ('OALEOL', 'OBDH LEOP HK LEN', 0),
                ('OAOECL', 'OBDH ERROR CODE HK LEN', 0),
                ('OAOMSL', 'OBDH MEMORY STS HK LEN', 0),
                ('OAOSWL', 'OBDH SW UPLD HK LEN', 0),
                ('OAOSRL', 'OBDH STORAGE REP CHK LEN', 0),
                ('OAGPSL', 'OBDH GPS STD HK LEN', 0),
                ('ORSTCL', 'OBDH RST CNTR HK LEN', 0),
                ('OAMVEL', 'OBDH MIVEW EXT HK LEN', 0),
                ('ORES2L', 'OBDH AI CAM CFG HK LEN', 0),
                ('ORES1L', 'OBDH RESERVED1 HK LEN', 0),
                ('OERMBL', 'OBDH ERR MGR BUF LEN', 0),
            ),
        },
        'obdh_ext_tc_lst_len': {
            'table': (
                ('name', 'Name', 0),
                ('OAAS1L', 'OBDH ACT SM LIST 1 LEN', 0),
                ('OAAS2L', 'OBDH ACT SM LIST 2 LEN', 0),
                ('OAAS3L', 'OBDH ACT SM LIST 3 LEN', 0),
                ('OAPASL', 'OBDH PAS SM LIST LEN', 0),
                ('OALP1L', 'OBDH LEOP LIST 1 LEN', 0),
                ('OALP2L', 'OBDH LEOP LIST 2 LEN', 0),
                ('OALP3L', 'OBDH LEOP LIST 3 LEN', 0),
                ('OAR01L', 'OBDH RP LIST 01 LEN', 0),
                ('OAR02L', 'OBDH RP LIST 02 LEN', 0),
                ('OAR03L', 'OBDH RP LIST 03 LEN', 0),
                ('OAR04L', 'OBDH RP LIST 04 LEN', 0),
                ('OAR05L', 'OBDH RP LIST 05 LEN', 0),
                ('OAR06L', 'OBDH RP LIST 06 LEN', 0),
                ('OAR07L', 'OBDH RP LIST 07 LEN', 0),
                ('OAR08L', 'OBDH RP LIST 08 LEN', 0),
                ('OAR09L', 'OBDH RP LIST 09 LEN', 0),
                ('OAR10L', 'OBDH RP LIST 10 LEN', 0),
                ('OAR11L', 'OBDH RP LIST 11 LEN', 0),
                ('OAR12L', 'OBDH RP LIST 12 LEN', 0),
                ('OAR13L', 'OBDH RP LIST 13 LEN', 0),
                ('OAR14L', 'OBDH RP LIST 14 LEN', 0),
                ('OAR15L', 'OBDH RP LIST 15 LEN', 0),
                ('OAR16L', 'OBDH RP LIST 16 LEN', 0),
                ('OAATTL', 'OBDH ACT TT LIST LEN', 0),
                ('OAPTTL', 'OBDH PAS TT LIST LEN', 0),
                ('OATCHW', 'OBDH TC LIST LEN HW ID', 0),
            ),
        },
        'obdh_rst_cntr_hk': {
            'table': (
                ('name', 'Name', 0),
                ('OVHF1X', 'VHF1 BOOT MSG RECEIVED', 0),
                ('OVHF1S', 'VHF1 SW IMAGE STATUS', 0),
                ('OVHF1B', 'VHF1 BOOTLOADER STATUS', 0),
                ('OVHF1C', 'VHF1 RESET COUNTER', 0),
                ('OUHF1X', 'UHF1 BOOT MSG RECEIVED', 0),
                ('OUHF1S', 'UHF1 SW IMAGE STATUS', 0),
                ('OUHF1B', 'UHF1 BOOTLOADER STATUS', 0),
                ('OUHF1C', 'UHF1 RESET COUNTER', 0),
                ('ORWX1X', 'RW X1 BOOT MSG RECEIVED', 0),
                ('ORWX1S', 'RW X1 SW IMAGE STATUS', 0),
                ('ORWX1B', 'RW X1 BOOTLOADER STATUS', 0),
                ('ORWX1C', 'RW X1 RESET COUNTER', 0),
                ('ORWY1X', 'RW Y1 BOOT MSG RECEIVED', 0),
                ('ORWY1S', 'RW Y1 SW IMAGE STATUS', 0),
                ('ORWY1B', 'RW Y1 BOOTLOADER STATUS', 0),
                ('ORWY1C', 'RW Y1 RESET COUNTER', 0),
                ('ORWZ1X', 'RW Z1 BOOT MSG RECEIVED', 0),
                ('ORWZ1S', 'RW Z1 SW IMAGE STATUS', 0),
                ('ORWZ1B', 'RW Z1 BOOTLOADER STATUS', 0),
                ('ORWZ1C', 'RW Z1 RESET COUNTER', 0),
                ('OSXP1X', 'SS XP1 BOOT MSG RECEIVED', 0),
                ('OSXP1S', 'SS XP1 SW IMAGE STATUS', 0),
                ('OSXP1B', 'SS XP1 BOOTLOADER STATUS', 0),
                ('OSXP1C', 'SS XP1 RESET COUNTER', 0),
                ('OSXN1X', 'SS XN1 BOOT MSG RECEIVED', 0),
                ('OSXN1S', 'SS XN1 SW IMAGE STATUS', 0),
                ('OSXN1B', 'SS XN1 BOOTLOADER STATUS', 0),
                ('OSXN1C', 'SS XN1 RESET COUNTER', 0),
                ('OSYP1X', 'SS YP1 BOOT MSG RECEIVED', 0),
                ('OSYP1S', 'SS YP1 SW IMAGE STATUS', 0),
                ('OSYP1B', 'SS YP1 BOOTLOADER STATUS', 0),
                ('OSYP1C', 'SS YP1 RESET COUNTER', 0),
                ('OSYN1X', 'SS YN1 BOOT MSG RECEIVED', 0),
                ('OSYN1S', 'SS YN1 SW IMAGE STATUS', 0),
                ('OSYN1B', 'SS YN1 BOOTLOADER STATUS', 0),
                ('OSYN1C', 'SS YN1 RESET COUNTER', 0),
                ('OSZP1X', 'SS ZP1 BOOT MSG RECEIVED', 0),
                ('OSZP1S', 'SS ZP1 SW IMAGE STATUS', 0),
                ('OSZP1B', 'SS ZP1 BOOTLOADER STATUS', 0),
                ('OSZP1C', 'SS ZP1 RESET COUNTER', 0),
                ('OSZN1X', 'SS ZN1 BOOT MSG RECEIVED', 0),
                ('OSZN1S', 'SS ZN1 SW IMAGE STATUS', 0),
                ('OSZN1B', 'SS ZN1 BOOTLOADER STATUS', 0),
                ('OSZN1C', 'SS ZN1 RESET COUNTER', 0),
                ('OADC1X', 'ADCS1 BOOT MSG RECEIVED', 0),
                ('OADC1S', 'ADCS1 SW IMAGE STATUS', 0),
                ('OADC1B', 'ADCS1 BOOTLOADER STATUS', 0),
                ('OADC1C', 'ADCS1 RESET COUNTER', 0),
                ('OIFP1X', 'IFP1 BOOT MSG RECEIVED', 0),
                ('OIFP1S', 'IFP1 SW IMAGE STATUS', 0),
                ('OIFP1B', 'IFP1 BOOTLOADER STATUS', 0),
                ('OIFP1C', 'IFP1 RESET COUNTER', 0),
                ('OP5V1X', 'PCU05V1 BOOT MSG RECEIVED', 0),
                ('OP5V1S', 'PCU05V1 SW IMAGE STATUS', 0),
                ('OP5V1B', 'PCU05V1 BOOTLOADER STATUS', 0),
                ('OP5V1C', 'PCU05V1 RESET COUNTER', 0),
                ('O12V1X', 'PCU12V1 BOOT MSG RECEIVED', 0),
                ('O12V1S', 'PCU12V1 SW IMAGE STATUS', 0),
                ('O12V1B', 'PCU12V1 BOOTLOADER STATUS', 0),
                ('O12V1C', 'PCU12V1 RESET COUNTER', 0),
                ('OMVW1X', 'MVIEW1 BOOT MSG RECEIVED', 0),
                ('OMVW1S', 'MVIEW1 SW IMAGE STATUS', 0),
                ('OMVW1B', 'MVIEW1 BOOTLOADER STATUS', 0),
                ('OMVW1C', 'MVIEW1 RESET COUNTER', 0),
                ('OVHF2X', 'VHF2 BOOT MSG RECEIVED', 0),
                ('OVHF2S', 'VHF2 SW IMAGE STATUS', 0),
                ('OVHF2B', 'VHF2 BOOTLOADER STATUS', 0),
                ('OVHF2C', 'VHF2 RESET COUNTER', 0),
                ('OUHF2X', 'UHF2 BOOT MSG RECEIVED', 0),
                ('OUHF2S', 'UHF2 SW IMAGE STATUS', 0),
                ('OUHF2B', 'UHF2 BOOTLOADER STATUS', 0),
                ('OUHF2C', 'UHF2 RESET COUNTER', 0),
                ('ORWX2X', 'RW X2 BOOT MSG RECEIVED', 0),
                ('ORWX2S', 'RW X2 SW IMAGE STATUS', 0),
                ('ORWX2B', 'RW X2 BOOTLOADER STATUS', 0),
                ('ORWX2C', 'RW X2 RESET COUNTER', 0),
                ('ORWY2X', 'RW Y2 BOOT MSG RECEIVED', 0),
                ('ORWY2S', 'RW Y2 SW IMAGE STATUS', 0),
                ('ORWY2B', 'RW YZ BOOTLOADER STATUS', 0),
                ('ORWY2C', 'RW Y2 RESET COUNTER', 0),
                ('ORWZ2X', 'RW Z2 BOOT MSG RECEIVED', 0),
                ('ORWZ2S', 'RW Z2 SW IMAGE STATUS', 0),
                ('ORWZ2B', 'RW Z2 BOOTLOADER STATUS', 0),
                ('ORWZ2C', 'RW Z2 RESET COUNTER', 0),
                ('OSXP2X', 'SS XP2 BOOT MSG RECEIVED', 0),
                ('OSXP2S', 'SS XP2 SW IMAGE STATUS', 0),
                ('OSXP2B', 'SS XP2 BOOTLOADER STATUS', 0),
                ('OSXP2C', 'SS XP2 RESET COUNTER', 0),
                ('OSXN2X', 'SS XN2 BOOT MSG RECEIVED', 0),
                ('OSXN2S', 'SS XN2 SW IMAGE STATUS', 0),
                ('OSXN2B', 'SS XN2 BOOTLOADER STATUS', 0),
                ('OSXN2C', 'SS XN2 RESET COUNTER', 0),
                ('OSYP2X', 'SS YP2 BOOT MSG RECEIVED', 0),
                ('OSYP2S', 'SS YP2 SW IMAGE STATUS', 0),
                ('OSYP2B', 'SS YP2 BOOTLOADER STATUS', 0),
                ('OSYP2C', 'SS YP2 RESET COUNTER', 0),
                ('OSYN2X', 'SS YN2 BOOT MSG RECEIVED', 0),
                ('OSYN2S', 'SS YN2 SW IMAGE STATUS', 0),
                ('OSYN2B', 'SS YN2 BOOTLOADER STATUS', 0),
                ('OSYN2C', 'SS YN2 RESET COUNTER', 0),
                ('OSZP2X', 'SS ZP2 BOOT MSG RECEIVED', 0),
                ('OSZP2S', 'SS ZP2 SW IMAGE STATUS', 0),
                ('OSZP2B', 'SS ZP2 BOOTLOADER STATUS', 0),
                ('OSZP2C', 'SS ZP2 RESET COUNTER', 0),
                ('OSZN2X', 'SS ZN2 BOOT MSG RECEIVED', 0),
                ('OSZN2S', 'SS ZN2 SW IMAGE STATUS', 0),
                ('OSZN2B', 'SS ZN2 BOOTLOADER STATUS', 0),
                ('OSZN2C', 'SS ZN2 RESET COUNTER', 0),
                ('OADC2X', 'ADCS2 BOOT MSG RECEIVED', 0),
                ('OADC2S', 'ADCS2 SW IMAGE STATUS', 0),
                ('OADC2B', 'ADCS2 BOOTLOADER STATUS', 0),
                ('OADC2C', 'ADCS2 RESET COUNTER', 0),
                ('OIFP2X', 'IFP2 BOOT MSG RECEIVED', 0),
                ('OIFP2S', 'IFP2 SW IMAGE STATUS', 0),
                ('OIFP2B', 'IFP2 BOOTLOADER STATUS', 0),
                ('OIFP2C', 'IFP2 RESET COUNTER', 0),
                ('OP5V2X', 'PCU05V2 BOOT MSG RECEIVED', 0),
                ('OP5V2S', 'PCU05V2 SW IMAGE STATUS', 0),
                ('OP5V2B', 'PCU05V2 BOOTLOADER STATUS', 0),
                ('OP5V2C', 'PCU05V2 RESET COUNTER', 0),
                ('O12V2X', 'PCU12V2 BOOT MSG RECEIVED', 0),
                ('O12V2S', 'PCU12V2 SW IMAGE STATUS', 0),
                ('O12V2B', 'PCU12V2 BOOTLOADER STATUS', 0),
                ('O12V2C', 'PCU12V2 RESET COUNTER', 0),
                ('OMVW2X', 'MVIEW2 BOOT MSG RECEIVED', 0),
                ('OMVW2S', 'MVIEW2 SW IMAGE STATUS', 0),
                ('OMVW2B', 'MVIEW2 BOOTLOADER STATUS', 0),
                ('OMVW2C', 'MVIEW2 RESET COUNTER', 0),
                ('OVHF1M', 'VHF1 LAST RESET REASON', 0),
                ('OVHF2M', 'VHF2 LAST RESET REASON', 0),
                ('OUHF1M', 'UHF1 LAST RESET REASON', 0),
                ('OUHF2M', 'UHF2 LAST RESET REASON', 0),
                ('ORWX1M', 'RW X1 LAST RESET REASON', 0),
                ('ORWX2M', 'RW X2 LAST RESET REASON', 0),
                ('ORWY1M', 'RW Y1 LAST RESET REASON', 0),
                ('ORWY2M', 'RW Y2 LAST RESET REASON', 0),
                ('ORWZ1M', 'RW Z1 LAST RESET REASON', 0),
                ('ORWZ2M', 'RW Z2 LAST RESET REASON', 0),
                ('OSXP1M', 'SS XP1 LAST RESET REASON', 0),
                ('OSXP2M', 'SS XP2 LAST RESET REASON', 0),
                ('OSXN1M', 'SS XN1 LAST RESET REASON', 0),
                ('OSXN2M', 'SS XN2 LAST RESET REASON', 0),
                ('OSYP1M', 'SS YP1 LAST RESET REASON', 0),
                ('OSYP2M', 'SS YP2 LAST RESET REASON', 0),
                ('OSYN1M', 'SS YN1 LAST RESET REASON', 0),
                ('OSYN2M', 'SS YN2 LAST RESET REASON', 0),
                ('OSZP1M', 'SS ZP1 LAST RESET REASON', 0),
                ('OSZP2M', 'SS ZP2 LAST RESET REASON', 0),
                ('OSZN1M', 'SS ZN1 LAST RESET REASON', 0),
                ('OSZN2M', 'SS ZN2 LAST RESET REASON', 0),
                ('OADC1M', 'ADCS1 LAST RESET REASON', 0),
                ('OADC2M', 'ADCS2 LAST RESET REASON', 0),
                ('OIFP1M', 'IFP1 LAST RESET REASON', 0),
                ('OIFP2M', 'IFP2 LAST RESET REASON', 0),
                ('OP5V1M', 'PCU05V1 LAST RESET REASON', 0),
                ('OP5V2M', 'PCU05V2 LAST RESET REASON', 0),
                ('O12V1M', 'PCU12V1 LAST RESET REASON', 0),
                ('O12V2M', 'PCU12V2 LAST RESET REASON', 0),
                ('OMVW1M', 'MVIEW1 LAST RESET REASON', 0),
                ('OMVW2M', 'MVIEW2 LAST RESET REASON', 0),
                ('OAIM1X', 'AI MC1 BOOT MSG RECEIVED', 0),
                ('OAIM1S', 'AI MC1 SW IMAGE STATUS', 0),
                ('OAIM1B', 'AI MC1 BOOTLOADER STATUS', 0),
                ('OAIM1C', 'AI MC1 RESET COUNTER', 0),
                ('OTHR1X', 'THRUSTER1 BOOT MSG RCVD', 0),
                ('OTHR1S', 'THRUSTER1 SW IMAGE STATUS', 0),
                ('OTHR1B', 'THRUSTER1 BTLDR STATUS', 0),
                ('OTHR1C', 'THRUSTER1 RESET COUNTER', 0),
                ('OAIM2X', 'AI MC2 BOOT MSG RECEIVED', 0),
                ('OAIM2S', 'AI MC2 SW IMAGE STATUS', 0),
                ('OAIM2B', 'AI MC2 BOOTLOADER STATUS', 0),
                ('OAIM2C', 'AI MC2 RESET COUNTER', 0),
                ('OTHR2X', 'THRUSTER2 BOOT MSG RCVD', 0),
                ('OTHR2S', 'THRUSTER2 SW IMAGE STATUS', 0),
                ('OTHR2B', 'THRUSTER2 BTLDR STATUS', 0),
                ('OTHR2C', 'THRUSTER2 RESET COUNTER', 0),
                ('OOBC1X', 'OBDH1 BOOT MSG RECEIVED', 0),
                ('OOBC1S', 'OBDH1 SW IMAGE STATUS', 0),
                ('OOBC1B', 'OBDH1 BOOTLOADER STATUS', 0),
                ('OOBC1C', 'OBDH1 RESET COUNTER', 0),
                ('OOBC2X', 'OBDH2 BOOT MSG RECEIVED', 0),
                ('OOBC2S', 'OBDH2 SW IMAGE STATUS', 0),
                ('OOBC2B', 'OBDH2 BOOTLOADER STATUS', 0),
                ('OOBC2C', 'OBDH2 RESET COUNTER', 0),
                ('OOBC3X', 'OBDH3 BOOT MSG RECEIVED', 0),
                ('OOBC3S', 'OBDH3 SW IMAGE STATUS', 0),
                ('OOBC3B', 'OBDH3 BOOTLOADER STATUS', 0),
                ('OOBC3C', 'OBDH3 RESET COUNTER', 0),
                ('OOBC4X', 'OBDH4 BOOT MSG RECEIVED', 0),
                ('OOBC4S', 'OBDH4 SW IMAGE STATUS', 0),
                ('OOBC4B', 'OBDH4 BOOTLOADER STATUS', 0),
                ('OOBC4C', 'OBDH4 RESET COUNTER', 0),
                ('OAIM1M', 'AI MC1 LAST RESET REASON', 0),
                ('OAIM2M', 'AI MC2 LAST RESET REASON', 0),
                ('OTHR1M', 'THRUSTER1 LAST RST REASON', 0),
                ('OTHR2M', 'THRUSTER2 LAST RST REASON', 0),
                ('OOBC2M', 'OBDH2 LAST RESET REASON', 0),
                ('OOBC1M', 'OBDH1 LAST RESET REASON', 0),
                ('OOBC4M', 'OBDH4 LAST RESET REASON', 0),
                ('OOBC3M', 'OBDH3 LAST RESET REASON', 0),
                ('OGNS1X', 'GNSS1 BOOT MSG RECEIVED', 0),
                ('OGNS1S', 'GNSS1 SW IMAGE STATUS', 0),
                ('OGNS1B', 'GNSS1 BOOTLOADER STATUS', 0),
                ('OGNS1C', 'GNSS1 RESET COUNTER', 0),
                ('OGNS2X', 'GNSS2 BOOT MSG RECEIVED', 0),
                ('OGNS2S', 'GNSS2 SW IMAGE STATUS', 0),
                ('OGNS2B', 'GNSS2 BOOTLOADER STATUS', 0),
                ('OGNS2C', 'GNSS2 RESET COUNTER', 0),
                ('OGNS2M', 'GNSS2 LAST RESET REASON', 0),
                ('OGNS1M', 'GNSS1 LAST RESET REASON', 0),
                ('ORSTEO', 'OBDH RST CNTR ERR CODE', 0),
                ('ORSTEC', 'OBDH RST CNTR ERR CNT', 0),
                ('ORSTHW', 'OBDH RESET CNTR HW ID', 0),
                ('ORSTAV', 'OBDH RESET CNTR AVAILABLE', 0),
                ('ORSTRS', 'OBDH REST CNTR RESERVED', 0),
            ),
        },
        'obdh_sw_inst': {
            'table': (
                ('name', 'Name', 0),
                ('OSWIST', 'SW INSTALL STATE', 0),
                ('OSWIAR', 'SW INSTALL ARCHITECTURE', 0),
                ('OSWIHW', 'SW INSTALL HARDWARE ID', 0),
                ('OSWIEO', 'SW INSTALL ERROR CODE', 0),
                ('OSWIEC', 'SW INSTALL ERROR CNTR', 0),
                ('OSWIPG', 'SW INSTALL PROGRESS, %', 0),
                ('OSWIUC', 'SW INSTALL MICROCNTRLR', 0),
                ('OSWIBS', 'SW INSTALL SAT BUS', 0),
                ('OSWICR', 'SW INSTALL COMP CRC', 0),
                ('OSWIAV', 'SW INSTALL AVAILABLE FLAG', 0),
                ('OSWITK', 'SW INSTALL TASK', 0),
                ('O1P2BG', 'OBDH1 PCU12V BOOT GPIO', 0),
                ('O1P5BG', 'OBDH1 PCU5V BOOT GPIO', 0),
                ('O1VHBG', 'OBDH1 VHF BOOT GPIO', 0),
                ('O1UHBG', 'OBDH1 UHF BOOT GPIO', 0),
                ('O1ADBG', 'OBDH1 ADCS BOOT GPIO', 0),
                ('O1AIBG', 'OBDH1 AI BOOT GPIO', 0),
                ('O1IFBG', 'OBDH1 IFP BOOT GPIO', 0),
                ('O1OBBG', 'OBDH1 OBDH BOOT GPIO', 0),
                ('O1BPAV', 'OBDH1 BOOT PINS AVAILABLE', 0),
                ('O2P2BG', 'OBDH2 PCU12V BOOT GPIO', 0),
                ('O2P5BG', 'OBDH2 PCU5V BOOT GPIO', 0),
                ('O2VHBG', 'OBDH2 VHF BOOT GPIO', 0),
                ('O2UHBG', 'OBDH2 UHF BOOT GPIO', 0),
                ('O2ADBG', 'OBDH2 ADCS BOOT GPIO', 0),
                ('O2AIBG', 'OBDH2 AI BOOT GPIO', 0),
                ('O2IFBG', 'OBDH2 IFP BOOT GPIO', 0),
                ('O2OBBG', 'OBDH2 OBDH BOOT GPIO', 0),
                ('O2BPAV', 'OBDH2 BOOT PINS AVAILABLE', 0),
                ('O3P2BG', 'OBDH3 PCU12V BOOT GPIO', 0),
                ('O3P5BG', 'OBDH3 PCU5V BOOT GPIO', 0),
                ('O3VHBG', 'OBDH3 VHF BOOT GPIO', 0),
                ('O3UHBG', 'OBDH3 UHF BOOT GPIO', 0),
                ('O3ADBG', 'OBDH3 ADCS BOOT GPIO', 0),
                ('O3AIBG', 'OBDH3 AI BOOT GPIO', 0),
                ('O3IFBG', 'OBDH3 IFP BOOT GPIO', 0),
                ('O3OBBG', 'OBDH3 OBDH BOOT GPIO', 0),
                ('O3BPAV', 'OBDH3 BOOT PINS AVAILABLE', 0),
                ('O4P2BG', 'OBDH4 PCU12V BOOT GPIO', 0),
                ('O4P5BG', 'OBDH4 PCU5V BOOT GPIO', 0),
                ('O4VHBG', 'OBDH4 VHF BOOT GPIO', 0),
                ('O4UHBG', 'OBDH4 UHF BOOT GPIO', 0),
                ('O4ADBG', 'OBDH4 ADCS BOOT GPIO', 0),
                ('O4AIBG', 'OBDH4 AI BOOT GPIO', 0),
                ('O4IFBG', 'OBDH4 IFP BOOT GPIO', 0),
                ('O4OBBG', 'OBDH4 OBDH BOOT GPIO', 0),
                ('O4BPAV', 'OBDH4 BOOT PINS AVAILABLE', 0),
                ('SSXP1B', 'SS XP1 BOOT PIN', 0),
                ('SSXN1B', 'SS XN1 BOOT PIN', 0),
                ('SSYP1B', 'SS YP1 BOOT PIN', 0),
                ('SSYN1B', 'SS YN1 BOOT PIN', 0),
                ('SSZP1B', 'SS ZP1 BOOT PIN', 0),
                ('SSZN1B', 'SS ZN1 BOOT PIN', 0),
                ('THR1BP', 'THRUSTER1 BOOT PIN', 0),
                ('MV1BOP', 'MULTIVIEW1 BOOT PIN', 0),
                ('P5V1B1', 'PCU05V1 MAX FRONT11 AV', 0),
                ('P5V1B2', 'PCU05V1 MAX FRONT21 AV', 0),
                ('P5V1B3', 'PCU05V1 MAX FRONT22 AV', 0),
                ('P5V1B4', 'PCU05V1 MAX TERM AV', 0),
                ('SSXP2B', 'SS XP2 BOOT PIN', 0),
                ('SSXN2B', 'SS XN2 BOOT PIN', 0),
                ('SSYP2B', 'SS YP2 BOOT PIN', 0),
                ('SSYN2B', 'SS YN2 BOOT PIN', 0),
                ('SSZP2B', 'SS ZP2 BOOT PIN', 0),
                ('SSZN2B', 'SS ZN2 BOOT PIN', 0),
                ('THR2BP', 'THRUSTER2 BOOT PIN', 0),
                ('MV2BOP', 'MULTIVIEW2 BOOT PIN', 0),
                ('P5V2B1', 'PCU05V2 MAX FRONT11 AV', 0),
                ('P5V2B2', 'PCU05V2 MAX FRONT21 AV', 0),
                ('P5V2B3', 'PCU05V2 MAX FRONT22 AV', 0),
                ('P5V2B4', 'PCU05V2 MAX TERM AV', 0),
                ('RWX1BO', 'RW X1 BOOT PIN', 0),
                ('RWY1BO', 'RW Y1 BOOT PIN', 0),
                ('RWZ1BO', 'RW Z1 BOOT PIN', 0),
                ('IFP1AV', 'IFP1 BOOT PIN AVAIL', 0),
                ('RWX2BO', 'RW X2 BOOT PIN', 0),
                ('RWY2BO', 'RW Y2 BOOT PIN', 0),
                ('RWZ2BO', 'RW Z2 BOOT PIN', 0),
                ('IFP2AV', 'IFP2 BOOT PIN AVAIL', 0),
            ),
        },
        'obdh_thread_run_time_hk': {
            'table': (
                ('name', 'Name', 0),
                ('OWDTRT', 'OBDH WATCHDOG THREAD RT, µs', 0),
                ('ORMTRT', 'OBDH ROLE MGR THREAD RT, µs', 0),
                ('OHKTRT', 'OBDH HK THREAD RT, µs', 0),
                ('OSMTRT', 'OBDH SYS MGR THREAD RT, µs', 0),
                ('OTCTRT', 'OBDH TC THREAD RT, µs', 0),
                ('OTDTRT', 'OBDH TM DWNL THREAD RT, µs', 0),
                ('OCATRT', 'OBDH CAN RX THREAD RT, µs', 0),
                ('OMMTRT', 'OBDH STO MGR THREAD RT, µs', 0),
                ('OPDTRT', 'OBDH PDH THREAD RT, µs', 0),
                ('OSITRT', 'OBDH SW INST THREAD RT, µs', 0),
                ('OSBTRT', 'OBDH S-BAND THREAD RT, µs', 0),
                ('OTRTHW', 'OBDH THREAD RUN TIME HW', 0),
                ('OTRTAV', 'OBDH THREAD RUN TIME AV', 0),
            ),
        },
        'obdh_timestamps': {
            'table': (
                ('name', 'Name', 0),
                ('OAUTCS', 'OBDH UTC SOURCE', 0),
                ('OAUTCT', 'OBDH UTC TIME, sec', 0),
                ('OARUPT', 'OBDH RODOS UPTIME, ms', 0),
                ('OATMHW', 'OBDH TIME HW ID', 0),
                ('OATEMP', 'OBDH INTERNAL TEMP, °C', 0),
            ),
        },
        'obdh_can_listener_sts': {
            'table': (
                ('name', 'Name', 0),
                ('OCLF11', 'OBDH CAN LSTNR B1 FLTR 1', 0),
                ('OCLF12', 'OBDH CAN LSTNR B1 FLTR 2', 0),
                ('OCLF13', 'OBDH CAN LSTNR B1 FLTR 3', 0),
                ('OCLF14', 'OBDH CAN LSTNR B1 FLTR 4', 0),
                ('OCLAVA', 'OBDH CAN LSTNR AVAILABLE', 0),
                ('OCLFB1', 'OBDH CAN LSTNR B1 FLTR MD', 0),
                ('OCLFB2', 'OBDH CAN LSTNR B2 FLTR MD', 0),
                ('OCLBFI', 'OBDH CAN LSTNR BUF INIT', 0),
                ('OCLBFL', 'OBDH CAN LSTNR BUF LEN', 0),
                ('OCLF21', 'OBDH CAN LSTNR B2 FLTR 1', 0),
                ('OCLF22', 'OBDH CAN LSTNR B2 FLTR 2', 0),
                ('OCLF23', 'OBDH CAN LSTNR B2 FLTR 3', 0),
                ('OCLF24', 'OBDH CAN LSTNR B2 FLTR 4', 0),
                ('OCLB1A', 'OBDH CAN LSTNR B1 FLTR ST', 0),
                ('OCLB2A', 'OBDH CAN LSTNR B2 FLTR ST', 0),
                ('OCLHWI', 'OBDH CAN LSTNR HW ID', 0),
                ('OCLBFF', 'OBDH CAN LISTNR BUF FINAL', 0),
                ('OCLECO', 'OBDH CAN LISTNR ERR CDE', 0),
                ('OCLECN', 'OBDH CAN LISTNR ERR CNT', 0),
            ),
        },
        'obdh_cfg_rest': {
            'table': (
                ('name', 'Name', 0),
                ('OOOPEN', 'OBDH WDG ON OFF PROT EN', 0),
                ('OOOSEN', 'OBDH WDG ON OFF SLV EN', 0),
                ('OCPUSE', 'OBDH CPU SLEEP MODE', 0),
                ('OOTRAV', 'OBDH CFG OTHERS AVAILABLE', 0),
                ('ORTCCP', 'OBDH RTC CALIB PERIOD', 0),
                ('ORTCCV', 'OBDH RTC CALIB VALUE', 0),
                ('OTTORP', 'OBDH TM TC TM EPOCH OFST, s', 0),
                ('ORMPRI', 'OBDH RM PRIORITY', 0),
                ('ORMMTO', 'OBDH RM MAX TRIES B4 OFF', 0),
                ('ORMRTP', 'OBDH RM ROLE TRIES PRI', 0),
                ('ORMRTS', 'OBDH RM ROLE TRIES SEC', 0),
                ('ORMRTT', 'OBDH RM ROLE TRIES TER', 0),
                ('ORMCSP', 'OBDH RM COM SRC PRI', 0),
                ('ORMCSS', 'OBDH RM COM SRC SEC', 0),
                ('ORMCST', 'OBDH RM COM SRC TER', 0),
                ('OOTRHW', 'OBDH CFG OTHERS HW ID', 0),
                ('ORSTTO', 'OBDH WDG RST TO NO TC, h', 0),
                ('OTMDTO', 'OBDH TM DOWN TIMEOUT, min', 0),
                ('OBEMOI', 'OBDH BEACON MODE INTVL, s', 0),
                ('OGLOCI', 'OBDH GLOBALS CHK INTVL, min', 0),
                ('OTDTGL', 'OBDH TM DOWN RDO TGL INTV, s', 0),
                ('OCFGCI', 'OBDH CONFIG CHK INTVL, min', 0),
                ('OTCLCI', 'OBDH TC LIST CHK INTVL, min', 0),
                ('OTIMED', 'OBDH TIME MODEL DRIFT, E-5', 0),
                ('OTGPSU', 'OBDH TIME GPS USAGE', 0),
                ('OTRTCE', 'OBDH RTC USAGE', 0),
                ('OORES1', 'OBDH RESERVED (4 bit)', 0),
                ('OTSCID', 'OBDH TF SPACECRAFT ID', 0),
                ('OTIMEA', 'OBDH TIME BUF ADR', 0),
                ('OCAN1E', 'OBDH CAN1 ENABLED', 0),
                ('OCAN2E', 'OBDH CAN2 ENABLED', 0),
                ('OSYN1E', 'OBDH SYNCH1 RX ENABLED', 0),
                ('OSYN2E', 'OBDH SYNCH2 RX ENABLED', 0),
                ('OSYN3E', 'OBDH SYNCH3 RX ENABLED', 0),
                ('OSYN4E', 'OBDH SYNCH4 RX ENABLED', 0),
                ('ORAM1E', 'OBDH SRAM1 ENABLED', 0),
                ('ORAM2E', 'OBDH SRAM2 ENABLED', 0),
                ('OPNF1E', 'OBDH PAR NOR1 ENABLED', 0),
                ('OPNF2E', 'OBDH PAR NOR2 ENABLED', 0),
                ('OSNFEN', 'OBDH SPI NOR ENABLED', 0),
                ('OSYNTE', 'OBDH SYNCH1 TX ENABLED', 0),
                ('OTIMEE', 'OBDH TIME BUF ENABLED', 0),
                ('OTDPRR', 'OBDH TM DOWN DFLT RADIO', 0),
                ('OSWDGW', 'OBDH SWDG TO WARN LIMIT, s', 0),
                ('OSWDGD', 'OBDH SWDG TO DEAD LIMIT, s', 0),
                ('OVHF1E', 'OBDH RDO ERR THRESH VHF1', 0),
                ('OVHF2E', 'OBDH RDO ERR THRESH VHF2', 0),
                ('OUHF1E', 'OBDH RDO ERR THRESH UHF1', 0),
                ('OUHF2E', 'OBDH RDO ERR THRESH UHF2', 0),
                ('OVHF1R', 'OBDH RDO ALIVE RATE VHF1, s', 0),
                ('OVHF2R', 'OBDH RDO ALIVE RATE VHF2, s', 0),
                ('OUHF1R', 'OBDH RDO ALIVE RATE UHF1, s', 0),
                ('OUHF2R', 'OBDH RDO ALIVE RATE UHF2, s', 0),
                ('OVHF1L', 'OBDH RDO RST LIMIT VHF1', 0),
                ('OVHF2L', 'OBDH RDO RST LIMIT VHF2', 0),
                ('OUHF1L', 'OBDH RDO RST LIMIT UHF1', 0),
                ('OUHF2L', 'OBDH RDO RST LIMIT UHF2', 0),
                ('OCANLA', 'OBDH CAN LISTEN BUF ADR', 0),
                ('OCANLC', 'OBDH CAN LISTEN BUF SECT', 0),
                ('OSWDGR', 'OBDH SWDG RUN INTVL, s', 0),
                ('OVHFVT', 'OBDH RDO VC0 TIMEOUT VHF, ms', 0),
                ('OUHFVT', 'OBDH RDO VC0 TIMEOUT UHF, ms', 0),
                ('OTCRFD', 'OBDH TC RCVR FWRD DELAY, ms', 0),
                ('OUMACF', 'OBDH USER MD ACT CPU FREQ, MHz', 0),
                ('OUMPCF', 'OBDH USER MD PAS CPU FREQ, MHz', 0),
                ('OEMBUA', 'OBDH ERR MGR BUF ADDR', 0),
                ('OEMBUS', 'OBDH ERR MGR BUF SCTR CNT', 0),
                ('OEMBUE', 'OBDH ERR MGR BUF ENABLED', 0),
                ('OTCFIT', 'OBDH CTRL FLOW INC TIME, ms', 0),
                ('OSBORP', 'OBDH TM BUS EPOCH OFFSET, s', 0),
                ('OGPORP', 'OBDH TM GPS EPOCH OFFSET, s', 0),
                ('OTUTCP', 'OBDH UTC BROADCAST PERIOD, s', 0),
                ('ORTCRI', 'OBDH RTC REREAD INTVL, s', 0),
                ('OTCFMT', 'OBDH CTRL FLOW MAX TIME, ms', 0),
                ('OTDTGT', 'OBDH RDO TGL INTVL DUE TC, s', 0),
                ('OINICI', 'OBDH INTRNL IMG CHK INTVL, min', 0),
            ),
        },
        'obdh_cfg_hk_buf': {
            'table': (
                ('name', 'Name', 0),
                ('OSTDHF', 'STD HK FORWARD', 0),
                ('OSTDHC', 'STD HK SCT CNT', 0),
                ('OEPERF', 'OBDH PERIPH HK FORWARD', 0),
                ('OEPERC', 'OBDH PERIPH HK SCT CNT', 0),
                ('OADCSF', 'ADCS STD HK FORWARD', 0),
                ('OADCSC', 'ADCS STD HK SCT CNT', 0),
                ('OACT1F', 'ACTUATOR1 HK FORWARD', 0),
                ('OACT1C', 'ACTUATOR1 HK SCT CNT', 0),
                ('OACT2F', 'ACTUATOR2 HK FORWARD', 0),
                ('OACT2C', 'ACTUATOR2 HK SCT CNT', 0),
                ('OSUN1F', 'SUN SENSOR1 HK FORWARD', 0),
                ('OSUN1C', 'SUN SENSOR1 HK SCT CNT', 0),
                ('OSUN2F', 'SUN SENSOR2 HK FORWARD', 0),
                ('OSUN2C', 'SUN SENSOR2 HK SCT CNT', 0),
                ('OTHERF', 'THERMAL HK FORWARD', 0),
                ('OTHERC', 'THERMAL HK SCT CNT', 0),
                ('OSWINF', 'SW INST HK FORWARD', 0),
                ('OSWINC', 'SW INST HK SCT CNT', 0),
                ('OPWRSF', 'PWR SENSOR HK FORWARD', 0),
                ('OPWRSC', 'PWR SENSOR HK SCT CNT', 0),
                ('OADCEF', 'ADCS EXT HK FORWARD', 0),
                ('OADCEC', 'ADCS EXT HK SCT CNT', 0),
                ('OPLDTF', 'PDH PLDT HK FORWARD', 0),
                ('OPLDTC', 'PDH PLDT HK SCT CNT', 0),
                ('OEXPDF', 'PDH EXPDH HK FORWARD', 0),
                ('OEXPDC', 'PDH EXPDH HK SCT CNT', 0),
                ('OSBNDF', 'S-BAND HK FORWARD', 0),
                ('OSBNDC', 'S-BAND HK SCT CNT', 0),
                ('OMOPSF', 'OBDH MEM OPS HK FORWARD', 0),
                ('OMOPSC', 'OBDH MEM OPS HK SCT CNT', 0),
                ('OAISTF', 'AI STD HK FORWARD', 0),
                ('OAISTC', 'AI STD HK SCT CNT', 0),
                ('OAI01F', 'AI CAM APP HK FORWARD', 0),
                ('OAI01C', 'AI CAM APP HK SCT CNT', 0),
                ('OAI02F', 'AI WS APP HK FORWARD', 0),
                ('OAI02C', 'AI WS APP HK SCT CNT', 0),
                ('OAI03F', 'AI NS APP HK FORWARD', 0),
                ('OAI03C', 'AI NS APP HK SCT CNT', 0),
                ('OAI04F', 'AI OD APP HK FORWARD', 0),
                ('OAI04C', 'AI OD APP HK SCT CNT', 0),
                ('OAI05F', 'AI AD APP HK FORWARD', 0),
                ('OAI05C', 'AI AD APP HK SCT CNT', 0),
                ('OAI06F', 'AI LD APP HK FORWARD', 0),
                ('OAI06C', 'AI LD APP HK SCT CNT', 0),
                ('OAI07F', 'AI APP07 HK FORWARD', 0),
                ('OAI07C', 'AI APP07 HK SCT CNT', 0),
                ('OAI08F', 'AI APP08 HK FORWARD', 0),
                ('OAI08C', 'AI APP08 HK SCT CNT', 0),
                ('OAI09F', 'AI APP09 HK FORWARD', 0),
                ('OAI09C', 'AI APP09 HK SCT CNT', 0),
                ('OAI10F', 'AI APP10 HK FORWARD', 0),
                ('OAI10C', 'AI APP10 HK SCT CNT', 0),
                ('OMVWSF', 'MULTIVIEW STD HK FORWARD', 0),
                ('OMVWSC', 'MULTIVIEW STD HK SCT CNT', 0),
                ('OTHRUF', 'THRUSTER HK FORWARD', 0),
                ('OTHRUC', 'THRUSTER HK SKT CNT', 0),
                ('OLEOPF', 'LEOP HK FORWARD', 0),
                ('OLEOPC', 'LEOP HK SCT CNT', 0),
                ('OECDEF', 'OBDH ERR CDE HK FORWARD', 0),
                ('OECDEC', 'OBDH ERR CDE HK SCT CNT', 0),
                ('OMEMSF', 'OBDH MEM STS HK FORWARD', 0),
                ('OMEMSC', 'OBDH MEM STS HK SCT CNT', 0),
                ('OSWUPF', 'OBDH SW UPLD HK FORWARD', 0),
                ('OSWUPC', 'OBDH SW UPLD HK SCT CNT', 0),
                ('OSTRCF', 'OBDH STO REPCHK FORWARD', 0),
                ('OSTRCC', 'OBDH STO REPCHK SCT CNT', 0),
                ('OGPSSF', 'GPS STD HK FORWARD', 0),
                ('OGPSSC', 'GPS STD HK SCT CNT', 0),
                ('ORSTCF', 'OBDH RST CNTR HK FORWARD', 0),
                ('ORSTCC', 'OBDH RST CNTR HK SCT CNT', 0),
                ('OMVWEF', 'MULTIVIEW EXT HK FORWARD', 0),
                ('OMVWEC', 'MULTIVIEW EXT HK SCT CNT', 0),
                ('ORES2F', 'AI CAM CFG HK FORWARD', 0),
                ('ORES2C', 'AI CAM CFG HK SCT CNT', 0),
                ('ORES1F', 'RESERVED1 HK FORWARD', 0),
                ('ORES1C', 'RESERVED1 HK SCT CNT', 0),
                ('OSTDHP', 'STD HK POLL', 0),
                ('OSTDHI', 'STD HK RATE, s', 0),
                ('OEPERP', 'OBDH PERIPH HK POLL', 0),
                ('OEPERI', 'OBDH PERIPH HK RATE, s', 0),
                ('OADCSP', 'ADCS STD HK POLL', 0),
                ('OADCSI', 'ADCS STD HK RATE, s', 0),
                ('OACT1P', 'ACTUATOR1 HK POLL', 0),
                ('OACT1I', 'ACTUATOR1 HK RATE, s', 0),
                ('OACT2P', 'ACTUATOR2 HK POLL', 0),
                ('OACT2I', 'ACTUATOR2 HK RATE, s', 0),
                ('OSUN1P', 'SUN SENSOR1 HK POLL', 0),
                ('OSUN1I', 'SUN SENSOR1 HK RATE, s', 0),
                ('OSUN2P', 'SUN SENSOR2 HK POLL', 0),
                ('OSUN2I', 'SUN SENSOR2 HK RATE, s', 0),
                ('OTHERP', 'THERMAL HK POLL', 0),
                ('OTHERI', 'THERMAL HK RATE, s', 0),
                ('OSWINP', 'SW INST HK POLL', 0),
                ('OSWINI', 'SW INST HK RATE, s', 0),
                ('OPWRSP', 'PWR SENSOR HK POLL', 0),
                ('OPWRSI', 'PWR SENSOR HK RATE, s', 0),
                ('OADCEP', 'ADCS EXT HK POLL', 0),
                ('OADCEI', 'ADCS EXT HK RATE, s', 0),
                ('OPLDTP', 'PDH PLDT HK POLL', 0),
                ('OPLDTI', 'PDH PLDT HK RATE, s', 0),
                ('OEXPDP', 'PDH EXPDH HK POLL', 0),
                ('OEXPDI', 'PDH EXPDH HK RATE, s', 0),
                ('OSBNDP', 'S-BAND HK POLL', 0),
                ('OSBNDI', 'S-BAND HK RATE, s', 0),
                ('OMOPSP', 'OBDH MEM OPS HK POLL', 0),
                ('OMOPSI', 'OBDH MEM OPS HK RATE, s', 0),
                ('OAISTP', 'AI STD HK POLL', 0),
                ('OAISTI', 'AI STD HK RATE, s', 0),
                ('OAI01P', 'AI CAM APP HK POLL', 0),
                ('OAI01I', 'AI CAM APP HK RATE, s', 0),
                ('OAI02P', 'AI WS APP HK POLL', 0),
                ('OAI02I', 'AI WS APP HK RATE, s', 0),
                ('OAI03P', 'AI NS APP HK POLL', 0),
                ('OAI03I', 'AI NS APP HK RATE, s', 0),
                ('OAI04P', 'AI OD APP HK POLL', 0),
                ('OAI04I', 'AI OD APP HK RATE, s', 0),
                ('OAI05P', 'AI AD APP HK POLL', 0),
                ('OAI05I', 'AI AD APP HK RATE, s', 0),
                ('OAI06P', 'AI LD APP HK POLL', 0),
                ('OAI06I', 'AI LD APP HK RATE, s', 0),
                ('OAI07P', 'AI APP07 HK POLL', 0),
                ('OAI07I', 'AI APP07 HK RATE, s', 0),
                ('OAI08P', 'AI APP08 HK POLL', 0),
                ('OAI08I', 'AI APP08 HK RATE, s', 0),
                ('OAI09P', 'AI APP09 HK POLL', 0),
                ('OAI09I', 'AI APP09 HK RATE, s', 0),
                ('OAI10P', 'AI APP10 HK POLL', 0),
                ('OAI10I', 'AI APP10 HK RATE, s', 0),
                ('OMVWSP', 'MULTIVIEW STD HK POLL', 0),
                ('OMVWSI', 'MULTIVIEW STD HK RATE, s', 0),
                ('OTHRUP', 'THRUSTER HK POLL', 0),
                ('OTHRUI', 'THRUSTER HK RATE, s', 0),
                ('OLEOPP', 'LEOP HK POLL', 0),
                ('OLEOPI', 'LEOP HK RATE, s', 0),
                ('OECDEP', 'OBDH ERR CDE HK POLL', 0),
                ('OECDEI', 'OBDH ERR CDE HK RATE, s', 0),
                ('OMEMSP', 'OBDH MEM STS HK POLL', 0),
                ('OMEMSI', 'OBDH MEM STS HK RATE, s', 0),
                ('OSWUPP', 'OBDH SW UPLD HK POLL', 0),
                ('OSWUPI', 'OBDH SW UPLD HK RATE, s', 0),
                ('OSTRCP', 'OBDH STO REPCHK POLL', 0),
                ('OSTRCI', 'OBDH STO REPCHK RATE, s', 0),
                ('OGPSSP', 'GPS STD HK POLL', 0),
                ('OGPSSI', 'GPS STD HK RATE, s', 0),
                ('ORSTCP', 'OBDH RST CNTR HK POLL', 0),
                ('ORSTCI', 'OBDH RST CNTR HK RATE, s', 0),
                ('OMVWEP', 'MULTIVIEW EXT HK POLL', 0),
                ('OMVWEI', 'MULTIVIEW EXT HK RATE, s', 0),
                ('ORES2P', 'AI CAM CFG HK POLL', 0),
                ('ORES2I', 'AI CAM CFG HK RATE, s', 0),
                ('ORES1P', 'RESERVED1 HK POLL', 0),
                ('ORES1I', 'RESERVED1 HK RATE, s', 0),
                ('OSTDHA', 'STD HK ADR', 0),
                ('OEPERA', 'OBDH PERIPH HK ADR', 0),
                ('OADCSA', 'ADCS STD HK ADR', 0),
                ('OACT1A', 'ACTUATOR1 HK ADR', 0),
                ('OACT2A', 'ACTUATOR2 HK ADR', 0),
                ('OSUN1A', 'SUN SENSOR1 HK ADR', 0),
                ('OSUN2A', 'SUN SENSOR2 HK ADR', 0),
                ('OTHERA', 'THERMAL HK ADR', 0),
                ('OSWINA', 'SW INST HK ADR', 0),
                ('OPWRSA', 'PWR SENSOR HK ADR', 0),
                ('OADCEA', 'ADCS EXT HK ADR', 0),
                ('OPLDTA', 'PDH PLDT HK ADR', 0),
                ('OEXPDA', 'PDH EXPDH HK ADR', 0),
                ('OSBNDA', 'S-BAND HK ADR', 0),
                ('OMOPSA', 'OBDH MEM OPS HK ADR', 0),
                ('OAISTA', 'AI STD HK ADR', 0),
                ('OAI01A', 'AI CAM APP HK ADR', 0),
                ('OAI02A', 'AI WS APP HK ADR', 0),
                ('OAI03A', 'AI NS APP HK ADR', 0),
                ('OAI04A', 'AI OD APP HK ADR', 0),
                ('OAI05A', 'AI AD APP HK ADR', 0),
                ('OAI06A', 'AI LD APP HK ADR', 0),
                ('OAI07A', 'AI APP07 HK ADR', 0),
                ('OAI08A', 'AI APP08 HK ADR', 0),
                ('OAI09A', 'AI APP09 HK ADR', 0),
                ('OAI10A', 'AI APP10 HK ADR', 0),
                ('OMVWSA', 'MULTIVIEW STD HK ADR', 0),
                ('OTHRUA', 'THRUSTER HK ADR', 0),
                ('OLEOPA', 'LEOP HK ADR', 0),
                ('OECDEA', 'OBDH ERR CDE HK ADR', 0),
                ('OMEMSA', 'OBDH MEM STS HK ADR', 0),
                ('OSWUPA', 'OBDH SW UPLD HK ADR', 0),
                ('OSTRCA', 'OBDH STO REPCHK ADR', 0),
                ('OGPSSA', 'GPS STD HK ADR', 0),
                ('ORSTCA', 'OBDH RST CNTR HK ADR', 0),
                ('OMVWEA', 'MULTIVIEW EXT HK ADR', 0),
                ('ORES2A', 'AI CAM CFG HK ADR', 0),
                ('ORES1A', 'RESERVED1 HK ADR', 0),
                ('OSTDHR', 'STD HK RECORD', 0),
                ('OEPERR', 'OBDH PERIPH HK RECORD', 0),
                ('OADCSR', 'ADCS STD HK RECORD', 0),
                ('OACT1R', 'ACTUATOR1 HK RECORD', 0),
                ('OACT2R', 'ACTUATOR2 HK RECORD', 0),
                ('OSUN1R', 'SUN SENSOR1 HK RECORD', 0),
                ('OSUN2R', 'SUN SENSOR2 HK RECORD', 0),
                ('OTHERR', 'THERMAL HK RECORD', 0),
                ('OSWINR', 'SW INST HK RECORD', 0),
                ('OPWRSR', 'PWR SENSOR HK RECORD', 0),
                ('OADCER', 'ADCS EXT HK RECORD', 0),
                ('OPLDTR', 'PDH PLDT HK RECORD', 0),
                ('OEXPDR', 'PDH EXPDH HK RECORD', 0),
                ('OSBNDR', 'S-BAND HK RECORD', 0),
                ('OMOPSR', 'OBDH MEM OPS HK RECORD', 0),
                ('OAISTR', 'AI STD HK RECORD', 0),
                ('OAI01R', 'AI CAM APP HK RECORD', 0),
                ('OAI02R', 'AI WS APP HK RECORD', 0),
                ('OAI03R', 'AI NS APP HK RECORD', 0),
                ('OAI04R', 'AI OD APP HK RECORD', 0),
                ('OAI05R', 'AI AD APP HK RECORD', 0),
                ('OAI06R', 'AI LD APP HK RECORD', 0),
                ('OAI07R', 'AI APP07 HK RECORD', 0),
                ('OAI08R', 'AI APP08 HK RECORD', 0),
                ('OAI09R', 'AI APP09 HK RECORD', 0),
                ('OAI10R', 'AI APP10 HK RECORD', 0),
                ('OMVWSR', 'MULTIVIEW STD HK RECORD', 0),
                ('OTHRUR', 'THRUSTER HK RECORD', 0),
                ('OLEOPR', 'LEOP HK RECORD', 0),
                ('OECDER', 'OBDH ERR CDE HK RECORD', 0),
                ('OMEMSR', 'OBDH MEM STS HK RECORD', 0),
                ('OSWUPR', 'OBDH SW UPLD HK RECORD', 0),
                ('OSTRCR', 'OBDH STO REPCHK RECORD', 0),
                ('OGPSSR', 'GPS STD HK RECORD', 0),
                ('ORSTCR', 'OBDH RST CNTR HK RECORD', 0),
                ('OMVWER', 'MULTIVIEW EXT HK RECORD', 0),
                ('ORES2R', 'AI CAM CFG HK RECORD', 0),
                ('ORES1R', 'RESERVED1 HK RECORD', 0),
                ('OCHKHW', 'OBDH CFG HK BUF HW ID', 0),
                ('OCHKAV', 'OBDH CFG HK BUF AVAILABLE', 0),
            ),
        },
        'obdh_cfg_tc_lst': {
            'table': (
                ('name', 'Name', 0),
                ('OLPL1A', 'OBDH LEOP LIST 1 ADR', 0),
                ('OLPL2A', 'OBDH LEOP LIST 2 ADR', 0),
                ('OLPL3A', 'OBDH LEOP LIST 3 ADR', 0),
                ('OASL1A', 'OBDH ACT SM LIST 1 ADR', 0),
                ('OASL2A', 'OBDH ACT SM LIST 2 ADR', 0),
                ('OASL3A', 'OBDH ACT SM LIST 3 ADR', 0),
                ('OPASLA', 'OBDH PAS SM LIST ADR', 0),
                ('OPATTA', 'OBDH PAS TT LIST ADR', 0),
                ('OACTTA', 'OBDH ACT TT LIST ADR', 0),
                ('OPATTC', 'OBDH PAS TT LIST SCT', 0),
                ('OACTTC', 'OBDH ACT TT LIST SCT', 0),
                ('OTCLHW', 'OBDH TC LIST CFG HW ID', 0),
                ('OTCLAV', 'OBDH TC LIST CFG AVAIL', 0),
                ('OTCRES', 'Reserved (5 bit)', 0),
                ('ORP01A', 'OBDH RP LIST 01 ADR', 0),
                ('ORP02A', 'OBDH RP LIST 02 ADR', 0),
                ('ORP03A', 'OBDH RP LIST 03 ADR', 0),
                ('ORP04A', 'OBDH RP LIST 04 ADR', 0),
                ('ORP05A', 'OBDH RP LIST 05 ADR', 0),
                ('ORP06A', 'OBDH RP LIST 06 ADR', 0),
                ('ORP07A', 'OBDH RP LIST 07 ADR', 0),
                ('ORP08A', 'OBDH RP LIST 08 ADR', 0),
                ('ORP09A', 'OBDH RP LIST 09 ADR', 0),
                ('ORP10A', 'OBDH RP LIST 10 ADR', 0),
                ('ORP11A', 'OBDH RP LIST 11 ADR', 0),
                ('ORP12A', 'OBDH RP LIST 12 ADR', 0),
                ('ORP13A', 'OBDH RP LIST 13 ADR', 0),
                ('ORP14A', 'OBDH RP LIST 14 ADR', 0),
                ('ORP15A', 'OBDH RP LIST 15 ADR', 0),
                ('ORP16A', 'OBDH RP LIST 16 ADR', 0),
                ('OSWUPS', 'OBDH SW UPLD PRG ADDR', 0),
            ),
        },
        'obdh_cfg_addr': {
            'table': (
                ('name', 'Name', 0),
                ('O1CFA1', 'OBDH1 CONFIG ADDRESS 1', 0),
                ('O1CFA2', 'OBDH1 CONFIG ADDRESS 2', 0),
                ('O1CFA3', 'OBDH1 CONFIG ADDRESS 3', 0),
                ('O2CFA1', 'OBDH2 CONFIG ADDRESS 1', 0),
                ('O2CFA2', 'OBDH2 CONFIG ADDRESS 2', 0),
                ('O2CFA3', 'OBDH2 CONFIG ADDRESS 3', 0),
                ('O3CFA1', 'OBDH3 CONFIG ADDRESS 1', 0),
                ('O3CFA2', 'OBDH3 CONFIG ADDRESS 2', 0),
                ('O3CFA3', 'OBDH3 CONFIG ADDRESS 3', 0),
                ('O4CFA1', 'OBDH4 CONFIG ADDRESS 1', 0),
                ('O4CFA2', 'OBDH4 CONFIG ADDRESS 2', 0),
                ('O4CFA3', 'OBDH4 CONFIG ADDRESS 3', 0),
            ),
        },
        'obdh_cfg_sm_lim': {
            'table': (
                ('name', 'Name', 0),
                ('LB05H1', 'LEOP VBAT 5V1 HIGH LIM', 0),
                ('LI05H1', 'LEOP IBUS 5V1 HIGH LIM', 0),
                ('LU05H1', 'LEOP IUHF 5V1 HIGH LIM', 0),
                ('LV05H1', 'LEOP IVHF 5V1 HIGH LIM', 0),
                ('LB05H2', 'LEOP VBAT 5V2 HIGH LIM', 0),
                ('LI05H2', 'LEOP IBUS 5V2 HIGH LIM', 0),
                ('LU05H2', 'LEOP IUHF 5V2 HIGH LIM', 0),
                ('LV05H2', 'LEOP IVHF 5V2 HIGH LIM', 0),
                ('LB12H1', 'LEOP VBAT 12V1 HIGH LIM', 0),
                ('LI12H1', 'LEOP IBUS 12V1 HIGH LIM', 0),
                ('LV12H2', 'LEOP VBAT 12V2 HIGH LIM', 0),
                ('LI12H2', 'LEOP IBUS 12V2 HIGH LIM', 0),
                ('NB05H1', 'NORMAL VBAT 5V1 HIGH LIM', 0),
                ('NI05H1', 'NORMAL IBUS 5V1 HIGH LIM', 0),
                ('NU05H1', 'NORMAL IUHF 5V1 HIGH LIM', 0),
                ('NV05H1', 'NORMAL IVHF 5V1 HIGH LIM', 0),
                ('NB05H2', 'NORMAL VBAT 5V2 HIGH LIM', 0),
                ('NI05H2', 'NORMAL IBUS 5V2 HIGH LIM', 0),
                ('NU05H2', 'NORMAL IUHF 5V2 HIGH LIM', 0),
                ('NV05H2', 'NORMAL IVHF 5V2 HIGH LIM', 0),
                ('NB12H1', 'NORMAL VBAT 12V1 HIGH LIM', 0),
                ('NI12H1', 'NORMAL IBUS 12V1 HIGH LIM', 0),
                ('NV12H2', 'NORMAL VBAT 12V2 HIGH LIM', 0),
                ('NI12H2', 'NORMAL IBUS 12V2 HIGH LIM', 0),
                ('PB05H1', 'PROC VBAT 5V1 HIGH LIM', 0),
                ('PI05H1', 'PROC IBUS 5V1 HIGH LIM', 0),
                ('PU05H1', 'PROC IUHF 5V1 HIGH LIM', 0),
                ('PV05H1', 'PROC IVHF 5V1 HIGH LIM', 0),
                ('PB05H2', 'PROC VBAT 5V2 HIGH LIM', 0),
                ('PI05H2', 'PROC IBUS 5V2 HIGH LIM', 0),
                ('PU05H2', 'PROC IUHF 5V2 HIGH LIM', 0),
                ('PV05H2', 'PROC IVHF 5V2 HIGH LIM', 0),
                ('PB12H1', 'PROC VBAT 12V1 HIGH LIM', 0),
                ('PI12H1', 'PROC IBUS 12V1 HIGH LIM', 0),
                ('PV12H2', 'PROC VBAT 12V2 HIGH LIM', 0),
                ('PI12H2', 'PROC IBUS 12V2 HIGH LIM', 0),
                ('BB05H1', 'BEACON VBAT 5V1 HIGH LIM', 0),
                ('BI05H1', 'BEACON IBUS 5V1 HIGH LIM', 0),
                ('BU05H1', 'BEACON IUHF 5V1 HIGH LIM', 0),
                ('BV05H1', 'BEACON IVHF 5V1 HIGH LIM', 0),
                ('BB05H2', 'BEACON VBAT 5V2 HIGH LIM', 0),
                ('BI05H2', 'BEACON IBUS 5V2 HIGH LIM', 0),
                ('BU05H2', 'BEACON IUHF 5V2 HIGH LIM', 0),
                ('BV05H2', 'BEACON IVHF 5V2 HIGH LIM', 0),
                ('BB12H1', 'BEACON VBAT 12V1 HIGH LIM', 0),
                ('BI12H1', 'BEACON IBUS 12V1 HIGH LIM', 0),
                ('BV12H2', 'BEACON VBAT 12V2 HIGH LIM', 0),
                ('BI12H2', 'BEACON IBUS 12V2 HIGH LIM', 0),
                ('UB05H1', 'USER VBAT 5V1 HIGH LIM', 0),
                ('UI05H1', 'USER IBUS 5V1 HIGH LIM', 0),
                ('UU05H1', 'USER IUHF 5V1 HIGH LIM', 0),
                ('UV05H1', 'USER IVHF 5V1 HIGH LIM', 0),
                ('UB05H2', 'USER VBAT 5V2 HIGH LIM', 0),
                ('UI05H2', 'USER IBUS 5V2 HIGH LIM', 0),
                ('UU05H2', 'USER IUHF 5V2 HIGH LIM', 0),
                ('UV05H2', 'USER IVHF 5V2 HIGH LIM', 0),
                ('UB12H1', 'USER VBAT 12V1 HIGH LIM', 0),
                ('UI12H1', 'USER IBUS 12V1 HIGH LIM', 0),
                ('UV12H2', 'USER VBAT 12V2 HIGH LIM', 0),
                ('UI12H2', 'USER IBUS 12V2 HIGH LIM', 0),
                ('OB05E1', 'OBDH VBAT 5V1 EXCEED LIM', 0),
                ('OI05E1', 'OBDH IBUS 5V1 EXCEED LIM', 0),
                ('OU05E1', 'OBDH IUHF 5V1 EXCEED LIM', 0),
                ('OV05E1', 'OBDH IVHF 5V2 EXCEED LIM', 0),
                ('OB05E2', 'OBDH VBAT 5V2 EXCEED LIM', 0),
                ('OI05E2', 'OBDH IBUS 5V2 EXCEED LIM', 0),
                ('OU05E2', 'OBDH IUHF 5V2 EXCEED LIM', 0),
                ('OV05E2', 'OBDH IVHF 5V2 EXCEED LIM', 0),
                ('OV12E1', 'OBDH VBAT 12V1 EXCEED LIM', 0),
                ('OI12E1', 'OBDH IBUS 12V1 EXCEED LIM', 0),
                ('OV12E2', 'OBDH VBAT 12V2 EXCEED LIM', 0),
                ('OI12E2', 'OBDH IBUS 12V2 EXCEED LIM', 0),
                ('OSMLHW', 'OBDH CFG SM LIMITS HW ID', 0),
                ('OSMLAV', 'OBDH CFG SM LIMITS AVAIL', 0),
                ('OSMRS1', 'OBDH SM RESERVED1', 0),
                ('OP12F2', 'OBDH PCU12V2 USED', 0),
                ('OP12F1', 'OBDH PCU12V1 USED', 0),
                ('OP05F2', 'OBDH PCU05V2 USED', 0),
                ('OP05F1', 'OBDH PCU05V1 USED', 0),
                ('OPUNRL', 'PCU NO RESPONSE LIMIT', 0),
                ('OSMRS2', 'OBDH SM RESERVED2', 0),
                ('OI12A2', 'OBDH IBUS 12V2 USED', 0),
                ('OV12A2', 'OBDH VBAT 12V2 USED', 0),
                ('OI12A1', 'OBDH IBUS 12V1 USED', 0),
                ('OV12A1', 'OBDH VBAT 12V1 USED', 0),
                ('OV05A2', 'OBDH IVHF 5V2 USED', 0),
                ('OU05A2', 'OBDH IUHF 5V2 USED', 0),
                ('OI05A2', 'OBDH IBUS 5V2 USED', 0),
                ('OB05A2', 'OBDH VBAT 5V2 USED', 0),
                ('OV05A1', 'OBDH IVHF 5V1 USED', 0),
                ('OU05A1', 'OBDH IUHF 5V1 USED', 0),
                ('OI05A1', 'OBDH IBUS 5V1 USED', 0),
                ('OB05A1', 'OBDH VBAT 5V1 USED', 0),
                ('OSMCIV', 'OBDH LIMITS CHECK INTVL, s', 0),
                ('OSMLAF', 'OBDH LIMITS AVG FACTOR', 0),
                ('LB05L1', 'LEOP VBAT 5V1 LOW LIM', 0),
                ('LI05L1', 'LEOP IBUS 5V1 LOW LIM', 0),
                ('LU05L1', 'LEOP IUHF 5V1 LOW LIM', 0),
                ('LV05L1', 'LEOP IVHF 5V1 LOW LIM', 0),
                ('LB05L2', 'LEOP VBAT 5V2 LOW LIM', 0),
                ('LI05L2', 'LEOP IBUS 5V2 LOW LIM', 0),
                ('LU05L2', 'LEOP IUHF 5V2 LOW LIM', 0),
                ('LV05L2', 'LEOP IVHF 5V2 LOW LIM', 0),
                ('LB12L1', 'LEOP VBAT 12V1 LOW LIM', 0),
                ('LI12L1', 'LEOP IBUS 12V1 LOW LIM', 0),
                ('LV12L2', 'LEOP VBAT 12V2 LOW LIM', 0),
                ('LI12L2', 'LEOP IBUS 12V2 LOW LIM', 0),
                ('NB05L1', 'NORMAL VBAT 5V1 LOW LIM', 0),
                ('NI05L1', 'NORMAL IBUS 5V1 LOW LIM', 0),
                ('NU05L1', 'NORMAL IUHF 5V1 LOW LIM', 0),
                ('NV05L1', 'NORMAL IVHF 5V1 LOW LIM', 0),
                ('NB05L2', 'NORMAL VBAT 5V2 LOW LIM', 0),
                ('NI05L2', 'NORMAL IBUS 5V2 LOW LIM', 0),
                ('NU05L2', 'NORMAL IUHF 5V2 LOW LIM', 0),
                ('NV05L2', 'NORMAL IVHF 5V2 LOW LIM', 0),
                ('NB12L1', 'NORMAL VBAT 12V1 LOW LIM', 0),
                ('NI12L1', 'NORMAL IBUS 12V1 LOW LIM', 0),
                ('NV12L2', 'NORMAL VBAT 12V2 LOW LIM', 0),
                ('NI12L2', 'NORMAL IBUS 12V2 LOW LIM', 0),
                ('PB05L1', 'PROC VBAT 5V1 LOW LIM', 0),
                ('PI05L1', 'PROC IBUS 5V1 LOW LIM', 0),
                ('PU05L1', 'PROC IUHF 5V1 LOW LIM', 0),
                ('PV05L1', 'PROC IVHF 5V1 LOW LIM', 0),
                ('PB05L2', 'PROC VBAT 5V2 LOW LIM', 0),
                ('PI05L2', 'PROC IBUS 5V2 LOW LIM', 0),
                ('PU05L2', 'PROC IUHF 5V2 LOW LIM', 0),
                ('PV05L2', 'PROC IVHF 5V2 LOW LIM', 0),
                ('PB12L1', 'PROC VBAT 12V1 LOW LIM', 0),
                ('PI12L1', 'PROC IBUS 12V1 LOW LIM', 0),
                ('PV12L2', 'PROC VBAT 12V2 LOW LIM', 0),
                ('PI12L2', 'PROC IBUS 12V2 LOW LIM', 0),
                ('BB05L1', 'BEACON VBAT 5V1 LOW LIM', 0),
                ('BI05L1', 'BEACON IBUS 5V1 LOW LIM', 0),
                ('BU05L1', 'BEACON IUHF 5V1 LOW LIM', 0),
                ('BV05L1', 'BEACON IVHF 5V1 LOW LIM', 0),
                ('BB05L2', 'BEACON VBAT 5V2 LOW LIM', 0),
                ('BI05L2', 'BEACON IBUS 5V2 LOW LIM', 0),
                ('BU05L2', 'BEACON IUHF 5V2 LOW LIM', 0),
                ('BV05L2', 'BEACON IVHF 5V2 LOW LIM', 0),
                ('BB12L1', 'BEACON VBAT 12V1 LOW LIM', 0),
                ('BI12L1', 'BEACON IBUS 12V1 LOW LIM', 0),
                ('BV12L2', 'BEACON VBAT 12V2 LOW LIM', 0),
                ('BI12L2', 'BEACON IBUS 12V2 LOW LIM', 0),
                ('UB05L1', 'USER VBAT 5V1 LOW LIM', 0),
                ('UI05L1', 'USER IBUS 5V1 LOW LIM', 0),
                ('UU05L1', 'USER IUHF 5V1 LOW LIM', 0),
                ('UV05L1', 'USER IVHF 5V1 LOW LIM', 0),
                ('UB05L2', 'USER VBAT 5V2 LOW LIM', 0),
                ('UI05L2', 'USER IBUS 5V2 LOW LIM', 0),
                ('UU05L2', 'USER IUHF 5V2 LOW LIM', 0),
                ('UV05L2', 'USER IVHF 5V2 LOW LIM', 0),
                ('UB12L1', 'USER VBAT 12V1 LOW LIM', 0),
                ('UI12L1', 'USER IBUS 12V1 LOW LIM', 0),
                ('UV12L2', 'USER VBAT 12V2 LOW LIM', 0),
                ('UI12L2', 'USER IBUS 12V2 LOW LIM', 0),
            ),
        },
        'obdh_cfg_pdh': {
            'table': (
                ('name', 'Name', 0),
                ('OCANMR', 'PDH CAN MAX RETRY', 0),
                ('OSPIMR', 'PDH SPI MAX RETRY', 0),
                ('OSPIPS', 'PDH SPI PKT SIZE', 0),
                ('OSPISA', 'PDH SPI SRAM ADDR', 0),
                ('OSPIFQ', 'PDH SPI FREQUENCY, kHz', 0),
                ('OPDCAV', 'PDH CFG AVAILABLE', 0),
                ('OPRES1', 'OBDH PDH RESERVED', 0),
                ('OPDHHW', 'OBDH PDH CFG HW ID', 0),
                ('OSSTVA', 'PDH SSTV SRAM ADDRESS', 0),
                ('OEXB0C', 'PDH EXP BUF0 SECTOR CNT', 0),
                ('OEXB1C', 'PDH EXP BUF1 SECTOR CNT', 0),
                ('OEXB2C', 'PDH EXP BUF2 SECTOR CNT', 0),
                ('OEXB3C', 'PDH EXP BUF3 SECTOR CNT', 0),
                ('OEXB4C', 'PDH EXP BUF4 SECTOR CNT', 0),
                ('OEXB5C', 'PDH EXP BUF5 SECTOR CNT', 0),
                ('OEXB6C', 'PDH EXP BUF6 SECTOR CNT', 0),
                ('OEXB7C', 'PDH EXP BUF7 SECTOR CNT', 0),
                ('OEXB0A', 'PDH EXP BUF0 ADDRESS', 0),
                ('OEXB1A', 'PDH EXP BUF1 ADDRESS', 0),
                ('OEXB2A', 'PDH EXP BUF2 ADDRESS', 0),
                ('OEXB3A', 'PDH EXP BUF3 ADDRESS', 0),
                ('OEXB4A', 'PDH EXP BUF4 ADDRESS', 0),
                ('OEXB5A', 'PDH EXP BUF5 ADDRESS', 0),
                ('OEXB6A', 'PDH EXP BUF6 ADDRESS', 0),
                ('OEXB7A', 'PDH EXP BUF7 ADDRESS', 0),
            ),
        },
        'adcs_std': {
            'table': (
                ('name', 'Name', 0),
                ('ADCACT', 'ACTIVE ADCS UNIT', 0),
                ('ADCMOD', 'ADCS MODE', 0),
                ('ADCOCO', 'ADCS CMD COUNTER', 0),
                ('ADCECO', 'ADCS ERROR CODE', 0),
                ('ADCECN', 'ADCS ERROR COUNTER', 0),
                ('ADFALG', 'ADCS SENSOR FUSION ALGO', 0),
                ('ADFIMV', 'ADCS MAGMETER USED', 0),
                ('ADCREF', 'ADCS REFERENCE FRAME', 0),
                ('ADCSR2', 'Reserved (1 bit)', 0),
                ('ADFIST', 'ADCS MULTIVIEW USED', 0),
                ('ADFISS', 'ADCS SUN SENSOR USED', 0),
                ('ADFROL', 'ADCS SENSOR FUSION ROLL, deg', 0),
                ('ADFPIT', 'ADCS SENSOR FUSION PITCH, deg', 0),
                ('ADFYAW', 'ADCS SENSOR FUSION YAW, deg', 0),
                ('MVIROL', 'ADCS MULTIVIEW ROLL, deg', 0),
                ('MVIPIT', 'ADCS MULTIVIEW PITCH, deg', 0),
                ('MVIYAW', 'ADCS MULTIVIEW YAW, deg', 0),
                ('MMX1BF', 'ADCS MAGNETIC FIELD X, µT', 0),
                ('MMY1BF', 'ADCS MAGNETIC FIELD Y, µT', 0),
                ('MMZ1BF', 'ADCS MAGNETIC FIELD Z, µT', 0),
                ('GYRROX', 'ADCS ANGULAR RATE X, deg/s', 0),
                ('GYRROY', 'ADCS ANGULAR RATE Y, deg/s', 0),
                ('GYRROZ', 'ADCS ANGULAR RATE Z, deg/s', 0),
                ('SSXMEA', 'ADCS SUN VECTOR X', 0),
                ('SSYMEA', 'ADCS SUN VECTOR Y', 0),
                ('SSZMEA', 'ADCS SUN VECTOR Z', 0),
                ('PREALT', 'ADCS GEO POS ALTITUDE, km', 0),
                ('PRELAT', 'ADCS GEO POS LATITUDE, ° N', 0),
                ('PRELON', 'ADCS GEO POS LONGITUDE, ° E', 0),
                ('TTORQX', 'ADCS TARGET TORQUE X, mNm', 0),
                ('TTORQY', 'ADCS TARGET TORQUE Y, mNm', 0),
                ('TTORQZ', 'ADCS TARGET TORQUE Z, mNm', 0),
                ('SUNVIS', 'ADCS SUN VISIBILITY', 0),
                ('ADCATV', 'ADCS ATTITUDE VALID', 0),
                ('ADCGUX', 'ADCS GYRO X USED', 0),
                ('ADCGUY', 'ADCS GYRO Y USED', 0),
                ('ADCGUZ', 'ADCS GYRO Z USED', 0),
            ),
        },
        'adcs_ext': {
            'table': (
                ('name', 'Name', 0),
                ('ADCUTC', 'ADCS UTC TIME, sec', 0),
                ('ADLOOP', 'ADCS LOOP TIME, ms', 0),
                ('ERRBU0', 'ADCS BUFFERED ERROR 0', 0),
                ('ERRBU1', 'ADCS BUFFERED ERROR 1', 0),
                ('ERRBU2', 'ADCS BUFFERED ERROR 2', 0),
                ('ERRBU3', 'ADCS BUFFERED ERROR 3', 0),
                ('ERRBU4', 'ADCS BUFFERED ERROR 4', 0),
                ('ERRBU5', 'ADCS BUFFERED ERROR 5', 0),
                ('ERRBU6', 'ADCS BUFFERED ERROR 6', 0),
                ('ERRBU7', 'ADCS BUFFERED ERROR 7', 0),
                ('ADCUPT', 'ADCS UPTIME, s', 0),
                ('ADSECO', 'ADCS MEASUREMENT CNT', 0),
                ('ADCPDR', 'ADCS PAYLOAD DATA RATE, ms', 0),
                ('ADGMST', 'ADCS PREDICTED GMST, °', 0),
                ('ADCPDS', 'ADCS PLD DATA SAVED BYTES', 0),
                ('PREDMX', 'ADCS MAG VECTOR ECI X, uT', 0),
                ('PREDMY', 'ADCS MAG VECTOR ECI Y, uT', 0),
                ('PREDMZ', 'ADCS MAG VECTOR ECI Z, uT', 0),
                ('PREDSX', 'ADCS SUN VECTOR ECI X', 0),
                ('PREDSY', 'ADCS SUN VECTOR ECI Y', 0),
                ('PREDSZ', 'ADCS SUN VECTOR ECI Z', 0),
                ('SS1XPV', 'ADCS SS XP1 DATA VAILD', 0),
                ('SS1XNV', 'ADCS SS XN1 DATA VAILD', 0),
                ('SS1YPV', 'ADCS SS YP1 DATA VAILD', 0),
                ('SS1YNV', 'ADCS SS YN1 DATA VAILD', 0),
                ('SS1ZPV', 'ADCS SS ZP1 DATA VAILD', 0),
                ('SS1ZNV', 'ADCS SS ZN1 DATA VAILD', 0),
                ('SS2XPV', 'ADCS SS XP2 DATA VAILD', 0),
                ('SS2XNV', 'ADCS SS XN2 DATA VAILD', 0),
                ('SS2YPV', 'ADCS SS YP2 DATA VAILD', 0),
                ('SS2YNV', 'ADCS SS YN2 DATA VAILD', 0),
                ('SS2ZPV', 'ADCS SS ZP2 DATA VAILD', 0),
                ('SS2ZNV', 'ADCS SS ZN2 DATA VAILD', 0),
                ('TOACX1', 'ADCS TORQUER X1 USED', 0),
                ('TOACY1', 'ADCS TORQUER Y1 USED', 0),
                ('TOACZ1', 'ADCS TORQUER Z1 USED', 0),
                ('TOACX2', 'ADCS TORQUER X2 USED', 0),
                ('TOACY2', 'ADCS TORQUER Y2 USED', 0),
                ('TOACZ2', 'ADCS TORQUER Z2 USED', 0),
                ('RWACX1', 'ADCS RW X1 USED', 0),
                ('RWACY1', 'ADCS RW Y1 USED', 0),
                ('RWACZ1', 'ADCS RW Z1 USED', 0),
                ('RWACX2', 'ADCS RW X2 USED', 0),
                ('RWACY2', 'ADCS RW Y2 USED', 0),
                ('RWACZ2', 'ADCS RW Z2 USED', 0),
                ('ADCREC', 'ADCS PLD DATA RECORDING', 0),
                ('ADCDLI', 'ADCS PLD DATA LIVE STATUS', 0),
                ('ADCTRA', 'ADCS PLD DATA TRANSFER', 0),
                ('EXPE00', 'ADCS RECORD TIMESTAMP', 0),
                ('EXPE01', 'ADCS RECORD CRC', 0),
                ('EXPE02', 'ADCS RECORD ADXRS', 0),
                ('EXPE03', 'ADCS RECORD CRM', 0),
                ('EXPE04', 'ADCS RECORD ANG RATE', 0),
                ('EXPE05', 'ADCS RECORD HMC', 0),
                ('EXPE06', 'ADCS RECORD RM', 0),
                ('EXPE07', 'ADCS RECORD MAG VECT', 0),
                ('EXPE08', 'ADCS RECORD PRED MAG', 0),
                ('EXPE09', 'ADCS RECORD SUN VECTOR', 0),
                ('EXPE10', 'ADCS RECORD MV QUAT', 0),
                ('EXPE11', 'ADCS RECORD ATTITUDE', 0),
                ('EXPE12', 'ADCS RECORD TORQUE CMD', 0),
                ('EXPE13', 'ADCS RECORD RW CMD', 0),
                ('EXPE14', 'ADCS RECORD RW RPM', 0),
                ('EXPE15', 'Recording Placeholder', 0),
                ('EXPE16', 'Recording Placeholder', 0),
                ('EXPE17', 'Recording Placeholder', 0),
                ('EXPE18', 'Recording Placeholder', 0),
                ('EXPE19', 'Recording Placeholder', 0),
                ('EXPE20', 'Recording Placeholder', 0),
                ('ADCADT', 'ADCS PLD ADD TIMESTAMP', 0),
                ('ADCADC', 'ADCS PLD ADD CRC', 0),
                ('APCANF', 'ADCS DATA CAN FILTER', 0),
                ('EPMRO', 'EPM TARGET ROLL, °', 0),
                ('EPMPI', 'EPM TARGET PITCH, °', 0),
                ('EPMYA', 'EPM TARGET YAW, °', 0),
                ('TPMLAT', 'TPM TARGET LATITUDE, °', 0),
                ('TPMLON', 'TPM TARGET LONGITUDE, °', 0),
                ('TPMRAD', 'TPM TARGET RADIUS', 0),
            ),
        },
        'adcs_cfg': {
            'table': (
                ('name', 'Name', 0),
                ('TLEEPO', 'TLE EPOCH, sec', 0),
                ('TLEBST', 'TLE B-STAR, /m', 0),
                ('TLEECC', 'TLE ECCENTRICITY', 0),
                ('TLEARG', 'TLE ARGUMENT OF PERIGEE, deg', 0),
                ('TLEINC', 'TLE INCLINATION, deg', 0),
                ('TLEMEA', 'TLE MEAN ANOMALY, deg', 0),
                ('TLENOD', 'TLE RAAN, deg', 0),
                ('TLEMOT', 'TLE MEAN MOTION, rev/day', 0),
                ('SETREV', 'SETTINGS REVISION', 0),
                ('SVREV0', 'SAVED SETTINGS REV 0', 0),
                ('SVREV1', 'SAVED SETTINGS REV 1', 0),
                ('SVREV2', 'SAVED SETTINGS REV 2', 0),
                ('SENRTO', 'SENSOR DATA TIMEOUT, ms', 0),
                ('IMURDU', 'IMU READOUT DURATION, ms', 0),
                ('TSTOFS', 'DATA TIMESTAMP OFFSET, ms', 0),
                ('CRCSL0', 'CRC SLOT 0', 0),
                ('CRCSL1', 'CRC SLOT 1', 0),
                ('CRCSL2', 'CRC SLOT 2', 0),
                ('ADCCAN', 'ADCS PRIMARY CAN BUS', 0),
                ('ADCAVA', 'ADCS CFG AVAILABILITY', 0),
                ('ADCCRS', 'ADCS Reserved (1 bit)', 0),
                ('HMCOFX', 'HMC OFFSET X, uT', 0),
                ('HMCOFY', 'HMC OFFSET Y, uT', 0),
                ('HMCOFZ', 'HMC OFFSET Z, uT', 0),
                ('HMCM00', 'HMC SCALAR [0,0]', 0),
                ('HMCM01', 'HMC SCALAR [0,1]', 0),
                ('HMCM02', 'HMC SCALAR [0,2]', 0),
                ('HMCM10', 'HMC SCALAR [1,0]', 0),
                ('HMCM11', 'HMC SCALAR [1,1]', 0),
                ('HMCM12', 'HMC SCALAR [1,2]', 0),
                ('HMCM20', 'HMC SCALAR [2,0]', 0),
                ('ADCCR1', 'ADCS Reserved (4 bit)', 0),
                ('HMCM21', 'HMC SCALAR [2,1]', 0),
                ('HMCM22', 'HMC SCALAR [2,2]', 0),
                ('RM3OFX', 'RM OFFSET X, uT', 0),
                ('RM3OFY', 'RM OFFSET Y, uT', 0),
                ('RM3OFZ', 'RM OFFSET Z, uT', 0),
                ('RM3M00', 'RM SCALAR [0,0]', 0),
                ('RM3M01', 'RM SCALAR [0,1]', 0),
                ('RM3M02', 'RM SCALAR [0,2]', 0),
                ('RM3M10', 'RM SCALAR [1,0]', 0),
                ('RM3M11', 'RM SCALAR [1,1]', 0),
                ('RM3M12', 'RM SCALAR [1,2]', 0),
                ('RM3M20', 'RM SCALAR [2,0]', 0),
                ('RM3M21', 'RM SCALAR [2,1]', 0),
                ('RM3M22', 'RM SCALAR [2,2]', 0),
                ('ADXOFX', 'ADXRS OFFSET X, °/s', 0),
                ('ADXOFY', 'ADXRS OFFSET Y, °/s', 0),
                ('ADXOFZ', 'ADXRS OFFSET Z, °/s', 0),
                ('ADXM00', 'ADXRS SCALAR [0,0]', 0),
                ('ADXM01', 'ADXRS SCALAR [0,1]', 0),
                ('ADXM02', 'ADXRS SCALAR [0,2]', 0),
                ('ADXM10', 'ADXRS SCALAR [1,0]', 0),
                ('ADXM11', 'ADXRS SCALAR [1,1]', 0),
                ('ADXM12', 'ADXRS SCALAR [1,2]', 0),
                ('ADXM20', 'ADXRS SCALAR [2,0]', 0),
                ('ADXM21', 'ADXRS SCALAR [2,1]', 0),
                ('ADXM22', 'ADXRS SCALAR [2,2]', 0),
                ('CRMOFX', 'CRM OFFSET X, °/s', 0),
                ('CRMOFY', 'CRM OFFSET Y, °/s', 0),
                ('CRMOFZ', 'CRM OFFSET Z, °/s', 0),
                ('CRMM00', 'CRM SCALAR [0,0]', 0),
                ('CRMM01', 'CRM SCALAR [0,1]', 0),
                ('CRMM02', 'CRM SCALAR [0,2]', 0),
                ('CRMM10', 'CRM SCALAR [1,0]', 0),
                ('CRMM11', 'CRM SCALAR [1,1]', 0),
                ('CRMM12', 'CRM SCALAR [1,2]', 0),
                ('CRMM20', 'CRM SCALAR [2,0]', 0),
                ('CRMM21', 'CRM SCALAR [2,1]', 0),
                ('CRMM22', 'CRM SCALAR [2,2]', 0),
                ('SXP1Q0', 'SUN SENSOR XP1 Q0', 0),
                ('SXP1Q1', 'SUN SENSOR XP1 Q1', 0),
                ('SXP1Q2', 'SUN SENSOR XP1 Q2', 0),
                ('SXP1Q3', 'SUN SENSOR XP1 Q3', 0),
                ('SXN1Q0', 'SUN SENSOR XN1 Q0', 0),
                ('SXN1Q1', 'SUN SENSOR XN1 Q1', 0),
                ('SXN1Q2', 'SUN SENSOR XN1 Q2', 0),
                ('SXN1Q3', 'SUN SENSOR XN1 Q3', 0),
                ('SYP1Q0', 'SUN SENSOR YP1 Q0', 0),
                ('SYP1Q1', 'SUN SENSOR YP1 Q1', 0),
                ('SYP1Q2', 'SUN SENSOR YP1 Q2', 0),
                ('SYP1Q3', 'SUN SENSOR YP1 Q3', 0),
                ('SYN1Q0', 'SUN SENSOR YN1 Q0', 0),
                ('SYN1Q1', 'SUN SENSOR YN1 Q1', 0),
                ('SYN1Q2', 'SUN SENSOR YN1 Q2', 0),
                ('SYN1Q3', 'SUN SENSOR YN1 Q3', 0),
                ('SZP1Q0', 'SUN SENSOR ZP1 Q0', 0),
                ('SZP1Q1', 'SUN SENSOR ZP1 Q1', 0),
                ('SZP1Q2', 'SUN SENSOR ZP1 Q2', 0),
                ('SZP1Q3', 'SUN SENSOR ZP1 Q3', 0),
                ('SZN1Q0', 'SUN SENSOR ZN1 Q0', 0),
                ('SZN1Q1', 'SUN SENSOR ZN1 Q1', 0),
                ('SZN1Q2', 'SUN SENSOR ZN1 Q2', 0),
                ('SZN1Q3', 'SUN SENSOR ZN1 Q3', 0),
                ('SXP2Q0', 'SUN SENSOR XP2 Q0', 0),
                ('SXP2Q1', 'SUN SENSOR XP2 Q1', 0),
                ('SXP2Q2', 'SUN SENSOR XP2 Q2', 0),
                ('SXP2Q3', 'SUN SENSOR XP2 Q3', 0),
                ('SXN2Q0', 'SUN SENSOR XN2 Q0', 0),
                ('SXN2Q1', 'SUN SENSOR XN2 Q1', 0),
                ('SXN2Q2', 'SUN SENSOR XN2 Q2', 0),
                ('SXN2Q3', 'SUN SENSOR XN2 Q3', 0),
                ('SYP2Q0', 'SUN SENSOR YP2 Q0', 0),
                ('SYP2Q1', 'SUN SENSOR YP2 Q1', 0),
                ('SYP2Q2', 'SUN SENSOR YP2 Q2', 0),
                ('SYP2Q3', 'SUN SENSOR YP2 Q3', 0),
                ('SYN2Q0', 'SUN SENSOR YN2 Q0', 0),
                ('SYN2Q1', 'SUN SENSOR YN2 Q1', 0),
                ('SYN2Q2', 'SUN SENSOR YN2 Q2', 0),
                ('SYN2Q3', 'SUN SENSOR YN2 Q3', 0),
                ('SZP2Q0', 'SUN SENSOR ZP2 Q0', 0),
                ('SZP2Q1', 'SUN SENSOR ZP2 Q1', 0),
                ('SZP2Q2', 'SUN SENSOR ZP2 Q2', 0),
                ('SZP2Q3', 'SUN SENSOR ZP2 Q3', 0),
                ('SZN2Q0', 'SUN SENSOR ZN2 Q0', 0),
                ('SZN2Q1', 'SUN SENSOR ZN2 Q1', 0),
                ('SZN2Q2', 'SUN SENSOR ZN2 Q2', 0),
                ('SZN2Q3', 'SUN SENSOR ZN2 Q3', 0),
                ('MROTQ0', 'MULTIVIEW Q0', 0),
                ('MROTQ1', 'MULTIVIEW Q1', 0),
                ('MROTQ2', 'MULTIVIEW Q2', 0),
                ('MROTQ3', 'MULTIVIEW Q3', 0),
                ('DTBMOD', 'DETUMBLING MODE', 0),
                ('DETPRI', 'DETERMINATION PRIO', 0),
                ('HMCCOR', 'HMC TEMP CORRECTION', 0),
                ('DESATA', 'DESATURATION', 0),
                ('TMXMX1', 'TORQUER MAX MOMENT X1, Am^2', 0),
                ('TMXMY1', 'TORQUER MAX MOMENT Y1, Am^2', 0),
                ('TMXMZ1', 'TORQUER MAX MOMENT Z1, Am^2', 0),
                ('TMXMX2', 'TORQUER MAX MOMENT X2, Am^2', 0),
                ('TMXMY2', 'TORQUER MAX MOMENT Y2, Am^2', 0),
                ('TMXMZ2', 'TORQUER MAX MOMENT Z2, Am^2', 0),
                ('TSETLT', 'TORQUER SETTLE TIME, ms', 0),
                ('MAGTLR', 'MAG TOLERANCE, uT', 0),
                ('GYRTLR', 'GYRO TOLERANCE, °/s', 0),
                ('MAGGAI', 'MAG FUSION GAIN', 0),
                ('TDIRX1', 'TORQUER DIRECTION X1', 0),
                ('TDIRY1', 'TORQUER DIRECTION Y1', 0),
                ('TDIRZ1', 'TORQUER DIRECTION Z1', 0),
                ('PRIMAG', 'PRIMARY MAG', 0),
                ('GYRGAI', 'GYRO FUSION GAIN', 0),
                ('TRIALP', 'TRIAD ALPHA', 0),
                ('QUWMAG', 'QUEST WEIGHT MAG', 0),
                ('QUWSUN', 'QUEST WEIGHT SUN', 0),
                ('QUWSTA', 'QUEST WEIGHT STAR', 0),
                ('MAXRPM', 'MAX RW RPM, RPM', 0),
                ('RWMAXT', 'MAX RW TORQUE, mNm', 0),
                ('SUNPKP', 'SUN POINTING KP', 0),
                ('SUNPKI', 'SUN POINTING KI', 0),
                ('SUNPKD', 'SUN POINTING KD', 0),
                ('TDIRX2', 'TORQUER DIRECTION X2', 0),
                ('TDIRY2', 'TORQUER DIRECTION Y2', 0),
                ('TDIRZ2', 'TORQUER DIRECTION Z2', 0),
                ('PRIGYR', 'PRIMARY GYRO', 0),
                ('SVPOSX', 'SOLAR SURFACE POS X', 0),
                ('SVPOSY', 'SOLAR SURFACE POS Y', 0),
                ('SVPOSZ', 'SOLAR SURFACE POS Z', 0),
                ('SVNEGX', 'SOLAR SURFACE NEG X', 0),
                ('SVNEGY', 'SOLAR SURFACE NEG Y', 0),
                ('SVNEGZ', 'SOLAR SURFACE NEG Z', 0),
                ('DETUKP', 'RATE DETUMBLING KP', 0),
                ('BDOTTH', 'BDOT THRESHOLD, uT', 0),
                ('MINANG', 'MIN VECTOR ANGLE, °', 0),
                ('INTTMO', 'INTEGRATION TMEOUT, min', 0),
                ('SRODUR', 'SNSR RDT DURATION, ms', 0),
                ('SROMSA', 'SNSR RDT MAX SAMPLES', 0),
                ('SRTSOF', 'SNSR RDT TIMESTAMP OFFSET, ms', 0),
                ('ACEPMP', 'EPM P GAIN', 0),
                ('ACEPMI', 'EPM I GAIN', 0),
                ('ACEPMD', 'EPM D GAIN', 0),
                ('ACTPMP', 'TPM P GAIN', 0),
                ('ACTPMI', 'TPM I GAIN', 0),
                ('ACTPMD', 'TPM D GAIN', 0),
                ('ACDESP', 'DESATURATION P GAIN', 0),
                ('ADCTRM', 'TORQUER MODE', 0),
                ('ACDEST', 'DESATURATION THRESHOLD, RPM', 0),
                ('ADANLP', 'ANGULAR RATE LOWPASS BETA', 0),
                ('ADOFRO', 'ATTITUDE DET OFFSET ROLL, °', 0),
                ('ADOFPI', 'ATTITUDE DET OFFSET PITCH, °', 0),
                ('ADOFYA', 'ATTITUDE DET OFFSET YAW, °', 0),
                ('HMCREX', 'HMC TEMP REF X, µT', 0),
                ('HMCREY', 'HMC TEMP REF Y, µT', 0),
                ('HMCREZ', 'HMC TEMP REF Z, µT', 0),
                ('GYRRAN', 'GYRO MEASUREMENT RANGE, °/s', 0),
                ('MAGRAN', 'MAG MEASUREMENT RANGE, µT', 0),
                ('TORTIM', 'TORQUER ACTIVATION TIME', 0),
                ('ADCCR2', 'ADCS Reserved (2 bit)', 0),
            ),
        },
        'adcs_akt_bus1_hk': {
            'table': (
                ('name', 'Name', 0),
                ('MTX1CU', 'MAG TORQ X1 CURRENT, mA', 0),
                ('MTY1CU', 'MAG TORQ Y1 CURRENT, mA', 0),
                ('MTZ1CU', 'MAG TORQ Z1 CURRENT, mA', 0),
                ('IFP1AA', 'IFP ACT 1 AVAILABLE', 0),
                ('MTZRES', 'Reserved (1 bit)', 0),
                ('MTX1PW', 'MAG TORQ X1 PWM, %', 0),
                ('MTY1PW', 'MAG TORQ Y1 PWM, %', 0),
                ('MTZ1PW', 'MAG TORQ Z1 PWM, %', 0),
                ('MTX1FT', 'MAG TORQ X1 FAULT', 0),
                ('MTX1EN', 'MAG TORQ X1 ENABLED', 0),
                ('MTX1DR', 'MAG TORQ X1 DIR', 0),
                ('MTX1SR', 'MAG TORQ X1 STBY/RST', 0),
                ('MTY1FT', 'MAG TORQ Y1 FAULT', 0),
                ('MTY1EN', 'MAG TORQ Y1 ENABLED', 0),
                ('MTY1DR', 'MAG TORQ Y1 DIR', 0),
                ('MTY1SR', 'MAG TORQ Y1 STBY/RST', 0),
                ('MTZ1FT', 'MAG TORQ Z1 FAULT', 0),
                ('MTZ1EN', 'MAG TORQ Z1 ENABLED', 0),
                ('MTZ1DR', 'MAG TORQ Z1 DIR', 0),
                ('MTZ1SR', 'MAG TORQ Z1 STBY/RST', 0),
                ('RWX1EN', 'RW X1 POWER STATE', 0),
                ('RWY1EN', 'RW Y1 POWER STATE', 0),
                ('RWZ1EN', 'RW Z1 POWER STATE', 0),
                ('RX1RAT', 'RW X1 RATE, RPM', 0),
                ('RX1CUR', 'RW X1 CURRENT, mA', 0),
                ('RX1CMC', 'RW X1 CMD COUNTER', 0),
                ('RX1ERC', 'RW X1 ERROR COUNTER', 0),
                ('RX1OPM', 'RW X1 OP MODE', 0),
                ('RX1ECN', 'RW X1 ERROR CODE', 0),
                ('RX1ACC', 'RW X1 ADCS CMD COUNT', 0),
                ('RX1RES', 'RW X1 Reserved (2 bit)', 0),
                ('RX1CTR', 'RW X1 CONTROLLER', 0),
                ('RX1TMP', 'RW X1 TEMPERATURE, °C', 0),
                ('RX1AVA', 'RW X1 AVAILABILITY', 0),
                ('RY1RAT', 'RW Y1 RATE, RPM', 0),
                ('RY1CUR', 'RW Y1 CURRENT, mA', 0),
                ('RY1CMC', 'RW Y1 CMD COUNTER', 0),
                ('RY1ERC', 'RW Y1 ERROR COUNTER', 0),
                ('RY1OPM', 'RW Y1 OP MODE', 0),
                ('RY1ECN', 'RW Y1 ERROR CODE', 0),
                ('RY1ACC', 'RW Y1 ADCS CMD COUNT', 0),
                ('RY1RES', 'RW Y1 Reserved (2 bit)', 0),
                ('RY1CTR', 'RW Y1 CONTROLLER', 0),
                ('RY1TMP', 'RW Y1 TEMPERATURE, °C', 0),
                ('RY1AVA', 'RW Y1 AVAILABILITY', 0),
                ('RZ1RAT', 'RW Z1 RATE, RPM', 0),
                ('RZ1CUR', 'RW Z1 CURRENT, mA', 0),
                ('RZ1CMC', 'RW Z1 CMD COUNTER', 0),
                ('RZ1ERC', 'RW Z1 ERROR COUNTER', 0),
                ('RZ1OPM', 'RW Z1 OP MODE', 0),
                ('RZ1ECN', 'RW Z1 ERROR CODE', 0),
                ('RZ1ACC', 'RW Z1 ADCS CMD COUNT', 0),
                ('RZ1RES', 'RW Z1 Reserved (2 bit)', 0),
                ('RZ1CTR', 'RW Z1 CONTROLLER', 0),
                ('RZ1TMP', 'RW Z1 TEMPERATURE, °C', 0),
                ('RZ1AVA', 'RW Z1 AVAILABILITY', 0),
            ),
        },
        'adcs_akt_bus2_hk': {
            'table': (
                ('name', 'Name', 0),
                ('MTX2CU', 'MAG TORQ X2 CURRENT, mA', 0),
                ('MTY2CU', 'MAG TORQ Y2 CURRENT, mA', 0),
                ('MTZ2CU', 'MAG TORQ Z2 CURRENT, mA', 0),
                ('IFP2AA', 'IFP ACT 2 AVAILABLE', 0),
                ('MTZ2RS', 'Reserved (1 bit)', 0),
                ('MTX2PW', 'MAG TORQ X2 PWM, %', 0),
                ('MTY2PW', 'MAG TORQ Y2 PWM, %', 0),
                ('MTZ2PW', 'MAG TORQ Z2 PWM, %', 0),
                ('MTX2FT', 'MAG TORQ X2 FAULT', 0),
                ('MTX2EN', 'MAG TORQ X2 ENABLED', 0),
                ('MTX2DR', 'MAG TORQ X2 DIR', 0),
                ('MTX2SR', 'MAG TORQ X2 STBY/RST', 0),
                ('MTY2FT', 'MAG TORQ Y2 FAULT', 0),
                ('MTY2EN', 'MAG TORQ Y2 ENABLED', 0),
                ('MTY2DR', 'MAG TORQ Y2 DIR', 0),
                ('MTY2SR', 'MAG TORQ Y2 STBY/RST', 0),
                ('MTZ2FT', 'MAG TORQ Z2 FAULT', 0),
                ('MTZ2EN', 'MAG TORQ Z2 ENABLED', 0),
                ('MTZ2DR', 'MAG TORQ Z2 DIR', 0),
                ('MTZ2SR', 'MAG TORQ Z2 STBY/RST', 0),
                ('RWX2EN', 'RW X2 POWER STATE', 0),
                ('RWY2EN', 'RW Y2 POWER STATE', 0),
                ('RWZ2EN', 'RW Z2 POWER STATE', 0),
                ('RX2RAT', 'RW X2 RATE, RPM', 0),
                ('RX2CUR', 'RW X2 CURRENT, mA', 0),
                ('RX2CMC', 'RW X2 CMD COUNTER', 0),
                ('RX2ERC', 'RW X2 ERROR COUNTER', 0),
                ('RX2OPM', 'RW X2 OP MODE', 0),
                ('RX2ECN', 'RW X2 ERROR CODE', 0),
                ('RX2ACC', 'RW X2 ADCS CMD COUNT', 0),
                ('RX2RES', 'RW X2 Reserved (2 bit)', 0),
                ('RX2CTR', 'RW X2 CONTROLLER', 0),
                ('RX2TMP', 'RW X2 TEMPERATURE, °C', 0),
                ('RX2AVA', 'RW X2 AVAILABILITY', 0),
                ('RY2RAT', 'RW Y2 RATE, RPM', 0),
                ('RY2CUR', 'RW Y2 CURRENT, mA', 0),
                ('RY2CMC', 'RW Y2 CMD COUNTER', 0),
                ('RY2ERC', 'RW Y2 ERROR COUNTER', 0),
                ('RY2OPM', 'RW Y2 OP MODE', 0),
                ('RY2ECN', 'RW Y2 ERROR CODE', 0),
                ('RY2ACC', 'RW Y2 ADCS CMD COUNT', 0),
                ('RY2RES', 'RW Y2 Reserved (2 bit)', 0),
                ('RY2CTR', 'RW Y2 CONTROLLER', 0),
                ('RY2TMP', 'RW Y2 TEMPERATURE, °C', 0),
                ('RY2AVA', 'RW Y2 AVAILABILITY', 0),
                ('RZ2RAT', 'RW Z2 RATE, RPM', 0),
                ('RZ2CUR', 'RW Z2 CURRENT, mA', 0),
                ('RZ2CMC', 'RW Z2 CMD COUNTER', 0),
                ('RZ2ERC', 'RW Z2 ERROR COUNTER', 0),
                ('RZ2OPM', 'RW Z2 OP MODE', 0),
                ('RZ2ECN', 'RW Z2 ERROR CODE', 0),
                ('RZ2ACC', 'RW Z2 ADCS CMD COUNT', 0),
                ('RZ2RES', 'RW Z2 Reserved (2 bit)', 0),
                ('RZ2CTR', 'RW Z2 CONTROLLER', 0),
                ('RZ2TMP', 'RW Z2 TEMPERATURE, °C', 0),
                ('RZ2AVA', 'RW Z2 AVAILABILITY', 0),
            ),
        },
        'adcs_rw_cfg': {
            'table': (
                ('name', 'Name', 0),
                ('RWCBLP', 'RW CFG BLOCK KP, E-3', 0),
                ('RWCBLI', 'RW CFG BLOCK KI', 0),
                ('RWCBLW', 'RW CFG BLOCK WINDUP', 0),
                ('RWCBLM', 'RW CFG BLOCK OUT MAX', 0),
                ('RWCFRP', 'RW CFG FOC RATE KP, E-3', 0),
                ('RWCFRI', 'RW CFG FOC RATE KI', 0),
                ('RWCFRW', 'RW CFG FOC RATE WINDUP', 0),
                ('RWCFRM', 'RW CFG FOC RATE OUT MAX', 0),
                ('RWCFDP', 'RW CFG FOC D KP', 0),
                ('RWCFDI', 'RW CFG FOC D KI', 0),
                ('RWCFDW', 'RW CFG FOC D WINDUP', 0),
                ('RWCFDM', 'RW CFG FOC D OUT MAX', 0),
                ('RWCFQP', 'RW CFG FOC Q KP', 0),
                ('RWCFQI', 'RW CFG FOC Q KI', 0),
                ('RWCFQW', 'RW CFG FOC Q WINDUP', 0),
                ('RWCFQM', 'RW CFG FOC Q OUT MAX', 0),
                ('RWCINM', 'RW CFG INERTIA MOMENT, gcm³', 0),
                ('RWCMRT', 'RW CFG MAX RATE, RPM', 0),
                ('RWCMTR', 'RW CFG MAX TORQUE, mNm', 0),
                ('RWCAVA', 'RW CFG AVAILABLE', 0),
                ('RWCBUS', 'RW CFG BUS', 0),
                ('RWCENC', 'RW CFG ENCODER', 0),
                ('RWCAXS', 'RW CFG AXIS', 0),
                ('RWCRES', 'RW CFG RESERVED (3 bit)', 0),
            ),
        },
        'adcs_sun_sen_bus1_hk': {
            'table': (
                ('name', 'Name', 0),
                ('SXP1CC', 'SS XP1 CMD COUNTER', 0),
                ('SXP1EO', 'SS XP1 ERROR CODE', 0),
                ('SXP1MD', 'SS XP1 OPERATION MODE', 0),
                ('SXP1EC', 'SS XP1 ERROR COUNTER', 0),
                ('SXP1PF', 'SS XP1 PROFILE SAFE STATE', 0),
                ('SXP1MC', 'SS XP1 MEASUREMENT CNTR', 0),
                ('SXP1XV', 'SS XP1 SUN VECTOR X', 0),
                ('SXP1YV', 'SS XP1 SUN VECTOR Y', 0),
                ('SXP1ZV', 'SS XP1 SUN VECTOR Z', 0),
                ('SXP1VS', 'SS XP1 SUN VECTOR STATUS', 0),
                ('SXP1TM', 'SS XP1 TEMPERATURE, °C', 0),
                ('SXN1CC', 'SS XN1 CMD COUNTER', 0),
                ('SXN1EO', 'SS XN1 ERROR CODE', 0),
                ('SXN1MD', 'SS XN1 OPERATION MODE', 0),
                ('SXN1EC', 'SS XN1 ERROR COUNTER', 0),
                ('SXN1PF', 'SS XN1 PROFILE SAFE STATE', 0),
                ('SXN1MC', 'SS XN1 MEASUREMENT CNTR', 0),
                ('SXN1XV', 'SS XN1 SUN VECTOR X', 0),
                ('SXN1YV', 'SS XN1 SUN VECTOR Y', 0),
                ('SXN1ZV', 'SS XN1 SUN VECTOR Z', 0),
                ('SXN1VS', 'SS XN1 SUN VECTOR STATUS', 0),
                ('SXN1TM', 'SS XN1 TEMPERATURE, °C', 0),
                ('SYP1CC', 'SS YP1 CMD COUNTER', 0),
                ('SYP1EO', 'SS YP1 ERROR CODE', 0),
                ('SYP1MD', 'SS YP1 OPERATION MODE', 0),
                ('SYP1EC', 'SS YP1 ERROR COUNTER', 0),
                ('SYP1PF', 'SS YP1 PROFILE SAFE STATE', 0),
                ('SYP1MC', 'SS YP1 MEASUREMENT CNTR', 0),
                ('SYP1XV', 'SS YP1 SUN VECTOR X', 0),
                ('SYP1YV', 'SS YP1 SUN VECTOR Y', 0),
                ('SYP1ZV', 'SS YP1 SUN VECTOR Z', 0),
                ('SYP1VS', 'SS YP1 SUN VECTOR STATUS', 0),
                ('SYP1TM', 'SS YP1 TEMPERATURE, °C', 0),
                ('SYN1CC', 'SS YN1 CMD COUNTER', 0),
                ('SYN1EO', 'SS YN1 ERROR CODE', 0),
                ('SYN1MD', 'SS YN1 OPERATION MODE', 0),
                ('SYN1EC', 'SS YN1 ERROR COUNTER', 0),
                ('SYN1PF', 'SS YN1 PROFILE SAFE STATE', 0),
                ('SYN1MC', 'SS YN1 MEASUREMENT CNTR', 0),
                ('SYN1XV', 'SS YN1 SUN VECTOR X', 0),
                ('SYN1YV', 'SS YN1 SUN VECTOR Y', 0),
                ('SYN1ZV', 'SS YN1 SUN VECTOR Z', 0),
                ('SYN1VS', 'SS YN1 SUN VECTOR STATUS', 0),
                ('SYN1TM', 'SS YN1 TEMPERATURE, °C', 0),
                ('SZP1CC', 'SS ZP1 CMD COUNTER', 0),
                ('SZP1EO', 'SS ZP1 ERROR CODE', 0),
                ('SZP1MD', 'SS ZP1 OPERATION MODE', 0),
                ('SZP1EC', 'SS ZP1 ERROR COUNTER', 0),
                ('SZP1PF', 'SS ZP1 PROFILE SAFE STATE', 0),
                ('SZP1MC', 'SS ZP1 MEASUREMENT CNTR', 0),
                ('SZP1XV', 'SS ZP1 SUN VECTOR X', 0),
                ('SZP1YV', 'SS ZP1 SUN VECTOR Y', 0),
                ('SZP1ZV', 'SS ZP1 SUN VECTOR Z', 0),
                ('SZP1VS', 'SS ZP1 SUN VECTOR STATUS', 0),
                ('SZP1TM', 'SS ZP1 TEMPERATURE, °C', 0),
                ('SZN1CC', 'SS ZN1 CMD COUNTER', 0),
                ('SZN1EO', 'SS ZN1 ERROR CODE', 0),
                ('SZN1MD', 'SS ZN1 OPERATION MODE', 0),
                ('SZN1EC', 'SS ZN1 ERROR COUNTER', 0),
                ('SZN1PF', 'SS ZN1 PROFILE SAFE STATE', 0),
                ('SZN1MC', 'SS ZN1 MEASUREMENT CNTR', 0),
                ('SZN1XV', 'SS ZN1 SUN VECTOR X', 0),
                ('SZN1YV', 'SS ZN1 SUN VECTOR Y', 0),
                ('SZN1ZV', 'SS ZN1 SUN VECTOR Z', 0),
                ('SZN1VS', 'SS ZN1 SUN VECTOR STATUS', 0),
                ('SZN1TM', 'SS ZN1 TEMPERATURE, °C', 0),
            ),
        },
        'adcs_sun_sen_bus2_hk': {
            'table': (
                ('name', 'Name', 0),
                ('SXP2CC', 'SS XP2 CMD COUNTER', 0),
                ('SXP2EO', 'SS XP2 ERROR CODE', 0),
                ('SXP2MD', 'SS XP2 OPERATION MODE', 0),
                ('SXP2EC', 'SS XP2 ERROR COUNTER', 0),
                ('SXP2PF', 'SS XP2 PROFILE SAFE STATE', 0),
                ('SXP2MC', 'SS XP2 MEASUREMENT CNTR', 0),
                ('SXP2XV', 'SS XP2 SUN VECTOR X', 0),
                ('SXP2YV', 'SS XP2 SUN VECTOR Y', 0),
                ('SXP2ZV', 'SS XP2 SUN VECTOR Z', 0),
                ('SXP2VS', 'SS XP2 SUN VECTOR STATUS', 0),
                ('SXP2TM', 'SS XP2 TEMPERATURE, °C', 0),
                ('SXN2CC', 'SS XN2 CMD COUNTER', 0),
                ('SXN2EO', 'SS XN2 ERROR CODE', 0),
                ('SXN2MD', 'SS XN2 OPERATION MODE', 0),
                ('SXN2EC', 'SS XN2 ERROR COUNTER', 0),
                ('SXN2PF', 'SS XN2 PROFILE SAFE STATE', 0),
                ('SXN2MC', 'SS XN2 MEASUREMENT CNTR', 0),
                ('SXN2XV', 'SS XN2 SUN VECTOR X', 0),
                ('SXN2YV', 'SS XN2 SUN VECTOR Y', 0),
                ('SXN2ZV', 'SS XN2 SUN VECTOR Z', 0),
                ('SXN2VS', 'SS XN2 SUN VECTOR STATUS', 0),
                ('SXN2TM', 'SS XN2 TEMPERATURE, °C', 0),
                ('SYP2CC', 'SS YP2 CMD COUNTER', 0),
                ('SYP2EO', 'SS YP2 ERROR CODE', 0),
                ('SYP2MD', 'SS YP2 OPERATION MODE', 0),
                ('SYP2EC', 'SS YP2 ERROR COUNTER', 0),
                ('SYP2PF', 'SS YP2 PROFILE SAFE STATE', 0),
                ('SYP2MC', 'SS YP2 MEASUREMENT CNTR', 0),
                ('SYP2XV', 'SS YP2 SUN VECTOR X', 0),
                ('SYP2YV', 'SS YP2 SUN VECTOR Y', 0),
                ('SYP2ZV', 'SS YP2 SUN VECTOR Z', 0),
                ('SYP2VS', 'SS YP2 SUN VECTOR STATUS', 0),
                ('SYP2TM', 'SS YP2 TEMPERATURE, °C', 0),
                ('SYN2CC', 'SS YN2 CMD COUNTER', 0),
                ('SYN2EO', 'SS YN2 ERROR CODE', 0),
                ('SYN2MD', 'SS YN2 OPERATION MODE', 0),
                ('SYN2EC', 'SS YN2 ERROR COUNTER', 0),
                ('SYN2PF', 'SS YN2 PROFILE SAFE STATE', 0),
                ('SYN2MC', 'SS YN2 MEASUREMENT CNTR', 0),
                ('SYN2XV', 'SS YN2 SUN VECTOR X', 0),
                ('SYN2YV', 'SS YN2 SUN VECTOR Y', 0),
                ('SYN2ZV', 'SS YN2 SUN VECTOR Z', 0),
                ('SYN2VS', 'SS YN2 SUN VECTOR STATUS', 0),
                ('SYN2TM', 'SS YN2 TEMPERATURE, °C', 0),
                ('SZP2CC', 'SS ZP2 CMD COUNTER', 0),
                ('SZP2EO', 'SS ZP2 ERROR CODE', 0),
                ('SZP2MD', 'SS ZP2 OPERATION MODE', 0),
                ('SZP2EC', 'SS ZP2 ERROR COUNTER', 0),
                ('SZP2PF', 'SS ZP2 PROFILE SAFE STATE', 0),
                ('SZP2MC', 'SS ZP2 MEASUREMENT CNTR', 0),
                ('SZP2XV', 'SS ZP2 SUN VECTOR X', 0),
                ('SZP2YV', 'SS ZP2 SUN VECTOR Y', 0),
                ('SZP2ZV', 'SS ZP2 SUN VECTOR Z', 0),
                ('SZP2VS', 'SS ZP2 SUN VECTOR STATUS', 0),
                ('SZP2TM', 'SS ZP2 TEMPERATURE, °C', 0),
                ('SZN2CC', 'SS ZN2 CMD COUNTER', 0),
                ('SZN2EO', 'SS ZN2 ERROR CODE', 0),
                ('SZN2MD', 'SS ZN2 OPERATION MODE', 0),
                ('SZN2EC', 'SS ZN2 ERROR COUNTER', 0),
                ('SZN2PF', 'SS ZN2 PROFILE SAFE STATE', 0),
                ('SZN2MC', 'SS ZN2 MEASUREMENT CNTR', 0),
                ('SZN2XV', 'SS ZN2 SUN VECTOR X', 0),
                ('SZN2YV', 'SS ZN2 SUN VECTOR Y', 0),
                ('SZN2ZV', 'SS ZN2 SUN VECTOR Z', 0),
                ('SZN2VS', 'SS ZN2 SUN VECTOR STATUS', 0),
                ('SZN2TM', 'SS ZN2 TEMPERATURE, °C', 0),
            ),
        },
        'adcs_sun_sen_cfg': {
            'table': (
                ('name', 'Name', 0),
                ('SSCSID', 'SUN SENSOR ID', 0),
                ('SSCBUS', 'SAT BUS', 0),
                ('SSCTSS', 'TEMP SENSOR SOURCE', 0),
                ('SSCDBS', 'DEBUG OUTPUT STATUS', 0),
                ('SSCAVI', 'SUN SENSOR CFG AVAILABLE', 0),
                ('SSCBLT', 'PS BLANKING TIME', 0),
                ('SSCUVL', 'PS UPPER VOLTAGE LIMIT', 0),
                ('SSCLVL', 'PS LOWER VOLTAGE LIMIT', 0),
                ('SSCCFC', 'PS CHRG AMP FDBK CAP', 0),
                ('SSCAAG', 'PS ANALOG AMP GAIN', 0),
                ('SSCCGA', 'PS COG AREA', 0),
                ('SSCCGT', 'PS COG THRESHOLD', 0),
                ('SSCINT', 'PS INTEGRATION TIME', 0),
                ('SSCEHS', 'EXTENDED HK STATUS', 0),
                ('SSCDOP', 'DEFAULT OPERATION MODE', 0),
                ('SSCRES', 'RESERVED (4 bit)', 0),
                ('SSCAEA', 'AUTO EXP ACTIVE', 0),
                ('SSCPWX', 'PEAK WIDTH THRESHOLD X', 0),
                ('SSCPWY', 'PEAK WIDTH THRESHOLD Y', 0),
                ('SSCASS', 'AUTO EXP STEP SIZE', 0),
                ('SSCAET', 'AUTO EXP TIME', 0),
                ('SSCEHL', 'AUTO EXP HIGH LIMIT', 0),
                ('SSCCTX', 'CENTER X', 0),
                ('SSCCTY', 'CENTER Y', 0),
                ('SSCELL', 'AUTO EXP LOW LIMIT', 0),
                ('SSCCMP', 'CONTINUOUS MODE PERIOD, ms', 0),
                ('SSCHTX', 'AUTO EXP HIGH THRESH X', 0),
                ('SSCHTY', 'AUTO EXP HIGH THRESH Y', 0),
                ('SSCLTX', 'AUTO EXP LOW THRESH X', 0),
                ('SSCLTY', 'AUTO EXP LOW THRESH Y', 0),
                ('SSCRAZ', 'ROTATION ANGLE Z, deg', 0),
                ('SSCCA0', 'CALIB COEFFICIENT A0, E-3', 0),
                ('SSCCA1', 'CALIB COEFFICIENT A1, E-3', 0),
                ('SSCCA2', 'CALIB COEFFICIENT A2, E-7', 0),
                ('SSCCA3', 'CALIB COEFFICIENT A3, E-8', 0),
                ('SSCCA4', 'CALIB COEFFICIENT A4, E-10', 0),
                ('SSCCA5', 'CALIB COEFFICIENT A5, E-13', 0),
            ),
        },
        'power_sensor_hk': {
            'table': (
                ('name', 'Name', 0),
                ('O1VLTG', 'OBDH1 VOLTAGE, V', 0),
                ('O2VLTG', 'OBDH2 VOLTAGE, V', 0),
                ('UHF1VS', 'UHF1 VOLTAGE, V', 0),
                ('IFP1VS', 'IFP1 VOLTAGE, V', 0),
                ('ADCS1V', 'ADCS1 VOLTAGE, V', 0),
                ('AI1VLT', 'AI1 VOLTAGE, V', 0),
                ('VHF1VS', 'VHF1 VOLTAGE, V', 0),
                ('SPZN1V', 'SOLAR ZN1 VOLTAGE, V', 0),
                ('O3VLTG', 'OBDH3 VOLTAGE, V', 0),
                ('O4VLTG', 'OBDH4 VOLTAGE, V', 0),
                ('UHF2VS', 'UHF2 VOLTAGE, V', 0),
                ('IFP2VS', 'IFP2 VOLTAGE, V', 0),
                ('ADCS2V', 'ADCS2 VOLTAGE, V', 0),
                ('AI2VLT', 'AI2 VOLTAGE, V', 0),
                ('VHF2VS', 'VHF2 VOLTAGE, V', 0),
                ('SPZN2V', 'SOLAR ZN2 VOLTAGE, V', 0),
                ('SPXP1V', 'SOLAR XP1 VOLTAGE, V', 0),
                ('SPYP1V', 'SOLAR YP1 VOLTAGE, V', 0),
                ('SPZP1V', 'SOLAR ZP1 VOLTAGE, V', 0),
                ('SPMB1V', 'SOLAR MOBIL1 VOLTAGE, V', 0),
                ('SBND1V', 'S-BAND1 VOLTAGE, V', 0),
                ('TH1VLT', 'THRUSTER1 VOLTAGE, V', 0),
                ('MV1VLT', 'MVIEW1 VOLTAGE, V', 0),
                ('SPXP2V', 'SOLAR XP2 VOLTAGE, V', 0),
                ('SPYN2V', 'SOLAR YN2 VOLTAGE, V', 0),
                ('SPZP2V', 'SOLAR ZP2 VOLTAGE, V', 0),
                ('SPMB2V', 'SOLAR MOBIL2 VOLTAGE, V', 0),
                ('SBND2V', 'S-BAND2 VOLTAGE, V', 0),
                ('TH2VLT', 'THRUSTER2 VOLTAGE, V', 0),
                ('MV2VLT', 'MVIEW2 VOLTAGE, V', 0),
                ('O1CURR', 'OBDH1 CURRENT, mA', 0),
                ('O2CURR', 'OBDH2 CURRENT, mA', 0),
                ('UHF1CT', 'UHF1 CURRENT, mA', 0),
                ('IFP1CR', 'IFP1 CURRENT, mA', 0),
                ('ADCS1C', 'ADCS1 CURRENT, mA', 0),
                ('AI1CUR', 'AI1 CURRENT, mA', 0),
                ('VHF1CR', 'VHF1 CURRENT, mA', 0),
                ('SPZN1C', 'SOLAR ZN1 CURRENT, mA', 0),
                ('O3CURR', 'OBDH3 CURRENT, mA', 0),
                ('O4CURR', 'OBDH4 CURRENT, mA', 0),
                ('UHF2CT', 'UHF2 CURRENT, mA', 0),
                ('IFP2CR', 'IFP2 CURRENT, mA', 0),
                ('ADCS2C', 'ADCS2 CURRENT, mA', 0),
                ('AI2CUR', 'AI2 CURRENT, mA', 0),
                ('VHF2CR', 'VHF2 CURRENT, mA', 0),
                ('SPZN2C', 'SOLAR ZN2 CURRENT, mA', 0),
                ('SPXP1C', 'SOLAR XP1 CURRENT, mA', 0),
                ('SPYP1C', 'SOLAR YP1 CURRENT, mA', 0),
                ('SPZP1C', 'SOLAR ZP1 CURRENT, mA', 0),
                ('SPMB1C', 'SOLAR MOBIL1 CURRENT, mA', 0),
                ('SBND1C', 'S-BAND1 CURRENT, mA', 0),
                ('TH1CUR', 'THRUSTER1 CURRENT, mA', 0),
                ('MV1CUR', 'MVIEW1 CURRENT, mA', 0),
                ('PWS1AV', 'POWER SENSOR 1 AVAILABLE', 0),
                ('SPXP2C', 'SOLAR XP2 CURRENT, mA', 0),
                ('SPYN2C', 'SOLAR YN2 CURRENT, mA', 0),
                ('SPZP2C', 'SOLAR ZP2 CURRENT, mA', 0),
                ('SPMB2C', 'SOLAR MOBIL2 CURRENT, mA', 0),
                ('SBND2C', 'S-BAND2 CURRENT, mA', 0),
                ('TH2CUR', 'THRUSTER2 CURRENT, mA', 0),
                ('MV2CUR', 'MVIEW2 CURRENT, mA', 0),
                ('PWS2AV', 'POWER SENSOR 2 AVAILABLE', 0),
            ),
        },
        'pwr_cfg_hk': {
            'table': (
                ('name', 'Name', 0),
                ('P5VIO1', 'READ INA219 OBDH1/3', 0),
                ('P5VIO2', 'READ INA219 OBDH2/4', 0),
                ('P5VIUH', 'READ INA219 UHF', 0),
                ('P5VIIF', 'READ INA219 IFP', 0),
                ('P5VIAD', 'READ INA219 ADCS', 0),
                ('P5VIAI', 'READ INA219 AI', 0),
                ('P5VIVH', 'READ INA219 VHF', 0),
                ('P5VIZN', 'READ INA219 SOLAR ZN', 0),
                ('P5VIXP', 'READ INA219 SOLAR XP', 0),
                ('P5VISY', 'READ INA219 SOLAR Y', 0),
                ('P5VIZP', 'READ INA219 SOLAR ZP', 0),
                ('P5VIMN', 'READ INA219 SOLAR MOBIL N', 0),
                ('P5VISB', 'READ INA219 S-BAND', 0),
                ('P5VITH', 'READ INA219 THRUSTER', 0),
                ('P5VIMV', 'READ INA219 MULTIVIEW', 0),
                ('P5VCAV', 'PCU05V CFG AVAILABLE', 0),
                ('P5VTAI', 'READ TMP175 AI', 0),
                ('P5VTIF', 'READ TMP175 IFP', 0),
                ('P5VTAD', 'READ TMP175 ADCS', 0),
                ('P5VTTM', 'READ TMP175 TERM', 0),
                ('P5VT05', 'READ TMP175 PCU05V', 0),
                ('P5VT12', 'READ TMP175 PCU12V', 0),
                ('P5VTFR', 'READ TMP175 FRONT', 0),
                ('P5VTZP', 'READ TMP175 SOLAR ZP', 0),
                ('P5VTZN', 'READ TMP175 SOLAR ZN', 0),
                ('P5VTXP', 'READ TMP175 SOLAR XP', 0),
                ('P5VTSY', 'READ TMP175 SOLAR Y', 0),
                ('P5VTO1', 'READ TMP1075 OBDH1/3', 0),
                ('P5VTO2', 'READ TMP1075 OBDH2/4', 0),
                ('P5VM05', 'READ MCP3421 PCU05V', 0),
                ('P5VM12', 'READ MCP3421 PCU12V', 0),
                ('P5VMAI', 'READ MCP3421 AI', 0),
                ('P5VLZP', 'READ LTC2481 SOLAR ZP', 0),
                ('P5VLZN', 'READ LTC2481 SOLAR ZN', 0),
                ('P5VLXP', 'READ LTC2481 SOLAR XP', 0),
                ('P5VLSY', 'READ LTC2481 SOLAR Y', 0),
                ('P5VLSM', 'READ LTC2481 SOLAR MOBIL', 0),
                ('P5VMF1', 'READ MAX7310 FRONT 1/1', 0),
                ('P5VMTM', 'READ MAX7310 TERM', 0),
                ('P5VMF2', 'READ MAX7310 FRONT 2/1', 0),
                ('P5VMF3', 'READ MAX7310 FRONT 1/2', 0),
                ('P5VMF4', 'READ MAX7310 FRONT 2/2', 0),
                ('P5VBMD', 'PCU05V BOOST MODE', 0),
                ('P5VCFS', 'PCU05V EXT HK SOURCE', 0),
                ('P5VGPI', 'PCU05V PG INT 5V->12V EN', 0),
                ('P12CAV', 'PCU12V CFG AVAILABLE', 0),
                ('P12BMD', 'PCU12V BOOST MODE', 0),
                ('P12CFS', 'PCU12V EXT HK SOURCE', 0),
            ),
        },
        'ifp_cfg_hk': {
            'table': (
                ('name', 'Name', 0),
                ('IFP1DL', 'IFP1 DEPLOY LIMIT, mA', 0),
                ('IFP1DT', 'IFP1 DEPLOY TIMEOUT, sec', 0),
                ('IFP1XL', 'IFP1 MAG TORQ X LIMIT, mA', 0),
                ('IFP1YL', 'IFP1 MAG TORQ Y LIMIT, mA', 0),
                ('IFP1ZL', 'IFP1 MAG TORQ Z LIMIT, mA', 0),
                ('IFP1CT', 'IFP1 MAG TORQ TIMEOUT, sec', 0),
                ('IFP2DL', 'IFP2 DEPLOY LIMIT, mA', 0),
                ('IFP2DT', 'IFP2 DEPLOY TIMEOUT, sec', 0),
                ('IFP2XL', 'IFP2 MAG TORQ X LIMIT, mA', 0),
                ('IFP2YL', 'IFP2 MAG TORQ Y LIMIT, mA', 0),
                ('IFP2ZL', 'IFP2 MAG TORQ Z LIMIT, mA', 0),
                ('IFP2CT', 'IFP2 MAG TORQ TIMEOUT, sec', 0),
                ('IFP2CA', 'IFP2 CFG AVAIL', 0),
                ('IFP1CA', 'IFP1 CFG AVAIL', 0),
            ),
        },
        'thermal_hk': {
            'table': (
                ('name', 'Name', 0),
                ('AI1PTM', 'AI1 PCB TEMPERATURE, °C', 0),
                ('IFP1TM', 'IFP1 TEMPERATURE, °C', 0),
                ('ADCS1T', 'ADCS1 TEMPERATURE, °C', 0),
                ('TERM1T', 'TERM1 TEMPERATURE, °C', 0),
                ('P5V1TM', 'PCU5V1 PCB TEMPERATURE, °C', 0),
                ('12V1TM', 'PCU12V1 PCB TEMPERATURE, °C', 0),
                ('FRNT1T', 'FRONT1 TEMPERATURE, °C', 0),
                ('SZP1IT', 'SOLAR ZP1 INSIDE TEMP, °C', 0),
                ('AI2PTM', 'AI2 PCB TEMPERATURE, °C', 0),
                ('IFP2TM', 'IFP2 TEMPERATURE, °C', 0),
                ('ADCS2T', 'ADCS2 TEMPERATURE, °C', 0),
                ('TERM2T', 'TERM2 TEMPERATURE, °C', 0),
                ('P5V2TM', 'PCU5V2 PCB TEMPERATURE, °C', 0),
                ('12V2TM', 'PCU12V2 PCB TEMPERATURE, °C', 0),
                ('FRNT2T', 'FRONT2 TEMPERATURE, °C', 0),
                ('SZP2IT', 'SOLAR ZP2 INSIDE TEMP, °C', 0),
                ('SZN1IT', 'SOLAR ZN1 INSIDE TEMP, °C', 0),
                ('SXP1IT', 'SOLAR XP1 INSIDE TEMP, °C', 0),
                ('SYP1IT', 'SOLAR YP1 INSIDE TEMP, °C', 0),
                ('O1TEMP', 'OBDH1 TEMPERATURE, °C', 0),
                ('O2TEMP', 'OBDH2 TEMPERATURE, °C', 0),
                ('AI1JTM', 'AI1 JETSON TEMPERATURE, °C', 0),
                ('SZP1OT', 'SOLAR ZP1 OUTSIDE TEMP, °C', 0),
                ('SZN1OT', 'SOLAR ZN1 OUTSIDE TEMP, °C', 0),
                ('SZN2IT', 'SOLAR ZN2 INSIDE TEMP, °C', 0),
                ('SXP2IT', 'SOLAR XP2 INSIDE TEMP, °C', 0),
                ('SYN2IT', 'SOLAR YN2 INSIDE TEMP, °C', 0),
                ('O3TEMP', 'OBDH3 TEMPERATURE, °C', 0),
                ('O4TEMP', 'OBDH4 TEMPERATURE, °C', 0),
                ('AI2JTM', 'AI2 JETSON TEMPERATURE, °C', 0),
                ('SZP2OT', 'SOLAR ZP2 OUTSIDE TEMP, °C', 0),
                ('SZN2OT', 'SOLAR ZN2 OUTSIDE TEMP, °C', 0),
                ('SXP1OT', 'SOLAR XP1 OUTSIDE TEMP, °C', 0),
                ('SYP1OT', 'SOLAR YP1 OUTSIDE TEMP, °C', 0),
                ('SPMB1T', 'SOLAR MOBIL1 TEMP, °C', 0),
                ('THK1AV', 'THERMAL HK 1 AVAILABILITY', 0),
                ('SXP2OT', 'SOLAR XP2 OUTSIDE TEMP, °C', 0),
                ('SYN2OT', 'SOLAR YN2 OUTSIDE TEMP, °C', 0),
                ('SPMB2T', 'SOLAR MOBIL2 TEMP, °C', 0),
                ('THK2AV', 'THERMAL HK 2 AVAILABILITY', 0),
            ),
        },
        'vhf_ext_hk': {
            'table': (
                ('name', 'Name', 0),
                ('VHF1TF', 'VHF1 TM TX FREQUENCY, MHz', 0),
                ('VHF1RF', 'VHF1 TC RX FREQUENCY, MHz', 0),
                ('VHF1TX', 'VHF1 TX DATA MODULATION', 0),
                ('VHF1RX', 'VHF1 RX DATA MODULATION', 0),
                ('VHF2TF', 'VHF2 TM TX FREQUENCY, MHz', 0),
                ('VHF2RF', 'VHF2 TC RX FREQUENCY, MHz', 0),
                ('VHF2TX', 'VHF2 TX DATA MODULATION', 0),
                ('VHF2RX', 'VHF2 RX DATA MODULATION', 0),
                ('VHF1SC', 'VHF1 S/C CALLSIGN', 0),
                ('VHF1SS', 'VHF1 S/C SSID', 0),
                ('VHF1PR', 'VHF1 PREAMBLE LENGTH, Bytes', 0),
                ('VHF2SC', 'VHF2 S/C CALLSIGN', 0),
                ('VHF2SS', 'VHF2 S/C SSID', 0),
                ('VHF2PR', 'VHF2 PREAMBLE LENGTH, Bytes', 0),
                ('VHF1GC', 'VHF1 G/S CALLSIGN', 0),
                ('VHF1GS', 'VHF1 G/S SSID', 0),
                ('VHF1PO', 'VHF1 POSTAMBLE LENGTH, Bytes', 0),
                ('VHF2GC', 'VHF2 G/S CALLSIGN', 0),
                ('VHF2GS', 'VHF2 G/S SSID', 0),
                ('VHF2PO', 'VHF2 POSTAMBLE LENGTH, Bytes', 0),
                ('VHF1AV', 'VHF1 RSSI AVG RATIO', 0),
                ('VHF1RI', 'VHF1 RSSI POLL INTERVAL, ms', 0),
                ('VHF1EA', 'VHF1 EXT AVAILABLE', 0),
                ('VHF1DF', 'VHF1 DESTINATION FILTER', 0),
                ('VHF1SF', 'VHF1 SOURCE FILTER', 0),
                ('VHF1MF', 'VHF1 SELF FILTER', 0),
                ('VHF1TP', 'VHF1 TRX PWR AMP OVERRIDE', 0),
                ('VHF2AV', 'VHF2 RSSI AVG RATIO', 0),
                ('VHF2RI', 'VHF2 RSSI POLL INTERVAL, ms', 0),
                ('VHF2EA', 'VHF2 EXT AVAILABLE', 0),
                ('VHF2DF', 'VHF2 DESTINATION FILTER', 0),
                ('VHF2SF', 'VHF2 SOURCE FILTER', 0),
                ('VHF2MF', 'VHF2 SELF FILTER', 0),
                ('VHF2TP', 'VHF2 TRX PWR AMP OVERRIDE', 0),
                ('VHF1FC', 'VHF1 SRC FILTER CALLSIGN', 0),
                ('VHF1WA', 'VHF1 APRS RPTR WO SC ADR', 0),
                ('VHF1AC', 'VHF1 AX.25 RX CNT COND', 0),
                ('VHF1DT', 'VHF1 DEPLOY TIMEOUT, sec', 0),
                ('VHF2FC', 'VHF2 SRC FILTER CALLSIGN', 0),
                ('VHF2WA', 'VHF2 APRS RPTR WO SC ADR', 0),
                ('VHF2AC', 'VHF2 AX.25 RX CNT COND', 0),
                ('VHF2DT', 'VHF2 DEPLOY TIMEOUT, sec', 0),
                ('VHF1AT', 'VHF1 APRS TX FREQUENCY, MHz', 0),
                ('VHF1AR', 'VHF1 APRS RX FREQUENCY, MHz', 0),
                ('VHF2AT', 'VHF2 APRS TX FREQUENCY, MHz', 0),
                ('VHF2AR', 'VHF2 APRS RX FREQUENCY, MHz', 0),
                ('VHF1ST', 'VHF1 SSTV TX FREQUENCY, MHz', 0),
                ('VHF1CT', 'VHF1 CW TX FREQUENCY, MHz', 0),
                ('VHF1GI', 'VHF1 APRS GREET INTERVAL, sec', 0),
                ('VHF1SL', 'VHF1 APRS SLOT TIME, ms', 0),
                ('VHF2ST', 'VHF2 SSTV TX FREQUENCY, MHz', 0),
                ('VHF2CT', 'VHF2 CW TX FREQUENCY, MHz', 0),
                ('VHF2GI', 'VHF2 APRS GREET INTERVAL, sec', 0),
                ('VHF2SL', 'VHF2 APRS SLOT TIME, ms', 0),
            ),
        },
        'uhf_ext_hk': {
            'table': (
                ('name', 'Name', 0),
                ('UHF1TF', 'UHF1 TM TX FREQUENCY, MHz', 0),
                ('UHF1RF', 'UHF1 TC RX FREQUENCY, MHz', 0),
                ('UHF1TX', 'UHF1 TX DATA MODULATION', 0),
                ('UHF1RX', 'UHF1 RX DATA MODULATION', 0),
                ('UHF2TF', 'UHF2 TM TX FREQUENCY, MHz', 0),
                ('UHF2RF', 'UHF2 TC RX FREQUENCY, MHz', 0),
                ('UHF2TX', 'UHF2 TX DATA MODULATION', 0),
                ('UHF2RX', 'UHF2 RX DATA MODULATION', 0),
                ('UHF1SC', 'UHF1 S/C CALLSIGN', 0),
                ('UHF1SS', 'UHF1 S/C SSID', 0),
                ('UHF1PR', 'UHF1 PREAMBLE LENGTH, Bytes', 0),
                ('UHF2SC', 'UHF2 S/C CALLSIGN', 0),
                ('UHF2SS', 'UHF2 S/C SSID', 0),
                ('UHF2PR', 'UHF2 PREAMBLE LENGTH, Bytes', 0),
                ('UHF1GC', 'UHF1 G/S CALLSIGN', 0),
                ('UHF1GS', 'UHF1 G/S SSID', 0),
                ('UHF1PO', 'UHF1 POSTAMBLE LENGTH, Bytes', 0),
                ('UHF2GC', 'UHF2 G/S CALLSIGN', 0),
                ('UHF2GS', 'UHF2 G/S SSID', 0),
                ('UHF2PO', 'UHF2 POSTAMBLE LENGTH, Bytes', 0),
                ('UHF1AV', 'UHF1 RSSI AVG RATIO', 0),
                ('UHF1RI', 'UHF1 RSSI POLL INTERVAL, ms', 0),
                ('UHF1EA', 'UHF1 EXT AVAILABLE', 0),
                ('UHF1DF', 'UHF1 DESTINATION FILTER', 0),
                ('UHF1SF', 'UHF1 SOURCE FILTER', 0),
                ('UHF1MF', 'UHF1 SELF FILTER', 0),
                ('UHF1TP', 'UHF1 TRX PWR AMP OVERRIDE', 0),
                ('UHF2AV', 'UHF2 RSSI AVG RATIO', 0),
                ('UHF2RI', 'UHF2 RSSI POLL INTERVAL, ms', 0),
                ('UHF2EA', 'UHF2 EXT AVAILABLE', 0),
                ('UHF2DF', 'UHF2 DESTINATION FILTER', 0),
                ('UHF2SF', 'UHF2 SOURCE FILTER', 0),
                ('UHF2MF', 'UHF2 SELF FILTER', 0),
                ('UHF2TP', 'UHF2 TRX PWR AMP OVERRIDE', 0),
                ('UHF1FC', 'UHF1 SRC FILTER CALLSIGN', 0),
                ('UHF1WA', 'UHF1 APRS RPTR WO SC ADR', 0),
                ('UHF1AC', 'UHF1 AX.25 RX CNT COND', 0),
                ('UHF1DT', 'UHF1 DEPLOY TIMEOUT, sec', 0),
                ('UHF2FC', 'UHF2 SRC FILTER CALLSIGN', 0),
                ('UHF2WA', 'UHF2 APRS RPTR WO SC ADR', 0),
                ('UHF2AC', 'UHF2 AX.25 RX CNT COND', 0),
                ('UHF2DT', 'UHF2 DEPLOY TIMEOUT, sec', 0),
                ('UHF1AT', 'UHF1 APRS TX FREQUENCY, MHz', 0),
                ('UHF1AR', 'UHF1 APRS RX FREQUENCY, MHz', 0),
                ('UHF2AT', 'UHF2 APRS TX FREQUENCY, MHz', 0),
                ('UHF2AR', 'UHF2 APRS RX FREQUENCY, MHz', 0),
                ('UHF1ST', 'UHF1 SSTV TX FREQUENCY, MHz', 0),
                ('UHF1CX', 'UHF1 CW TX FREQUENCY, MHz', 0),
                ('UHF1GI', 'UHF1 APRS GREET INTERVAL, sec', 0),
                ('UHF1SL', 'UHF1 APRS SLOT TIME, ms', 0),
                ('UHF2ST', 'UHF2 SSTV TX FREQUENCY, MHz', 0),
                ('UHF2CX', 'UHF2 CW TX FREQUENCY, MHz', 0),
                ('UHF2GI', 'UHF2 APRS GREET INTERVAL, sec', 0),
                ('UHF2SL', 'UHF2 APRS SLOT TIME, ms', 0),
            ),
        },
        's_band_std_hk': {
            'table': (
                ('name', 'Name', 0),
                ('SBTMAD', 'S-BAND AD9361 TEMP, °C', 0),
                ('SBTMET', 'S-BAND ETH PYH TEMP, °C', 0),
                ('SBTMZY', 'S-BAND ZYNQ TEMP, °C', 0),
                ('SBRXGN', 'S-BAND RX GAIN, dB', 0),
                ('SBRXDF', 'S-BAND RX DOPPLER FREQ, kHz', 0),
                ('SBRX0A', 'S-BAND RX CH 0 ACTIVE', 0),
                ('SBRX1A', 'S-BAND RX CH 1 ACTIVE', 0),
                ('SBRXSL', 'S-BAND RX SIR MIN, dB', 0),
                ('SBRXSY', 'S-BAND RX SYNC', 0),
                ('SBRXCU', 'S-BAND RX CH USED', 0),
                ('SBRXSH', 'S-BAND RX SIR MAX, dB', 0),
                ('SBOBHW', 'S-BAND OBDH HW ID', 0),
                ('SBRXPL', 'S-BAND RX PWR MIN, dB', 0),
                ('SBHKAV', 'S-BAND HK AVAILABLE', 0),
                ('SBCFGR', 'S-BAND CFG RECEIVED', 0),
                ('SBRSPH', 'S-BAND RX PWR MAX, dB', 0),
                ('SBRXST', 'S-BAND RX STATE', 0),
                ('SBRXBC', 'S-BAND RX BLOCK COUNT', 0),
                ('SBRXEB', 'S-BAND RX ERR BLOCK COUNT', 0),
                ('SBTXMD', 'S-BAND TX MODULATION', 0),
                ('SBTXFC', 'S-BAND TX FEC', 0),
                ('SBTX0A', 'S-BAND TX CH 0 ACTIVE', 0),
                ('SBTX1A', 'S-BAND TX CH 1 ACTIVE', 0),
                ('SBTXCU', 'S-BAND TX CH USED', 0),
                ('SBTXAT', 'S-BAND TX ATT, dB', 0),
                ('SBVCIN', 'S-BAND VCCINT, V', 0),
                ('SBVCAU', 'S-BAND VCCAUX, V', 0),
                ('SBVCRM', 'S-BAND VCCBRAM, V', 0),
                ('SBVCPT', 'S-BAND VCCPINT, V', 0),
                ('SBVCPA', 'S-BAND VCCPAXU, V', 0),
                ('SBVCPO', 'S-BAND VCCPDRO, V', 0),
                ('SBECDE', 'S-BAND ERROR CODE', 0),
                ('SBECNT', 'S-BAND ERROR COUNTER', 0),
                ('SBFWSU', 'S-BAND FWRD SW UPLD', 0),
                ('SBSWVR', 'S-BAND SW VERSION RCVD', 0),
                ('SBDVFR', 'S-BAND DEV FEATURE RCVD', 0),
                ('SBUPTM', 'S-BAND UPTIME, s', 0),
            ),
        },
        's_band_cfg': {
            'table': (
                ('name', 'Name', 0),
                ('SBCHWI', 'S-BAND CFG HW ID', 0),
                ('SBCAVA', 'S-BAND CFG AVAILABILITY', 0),
                ('SBCRXC', 'S-BAND RX CHANNEL', 0),
                ('SBCTXC', 'S-BAND TX CHANNEL', 0),
                ('SBCTPR', 'S-BAND TX PSEUDO RAND', 0),
                ('SBCRPR', 'S-BAND RX PSEUDO RAND', 0),
                ('SPCRBD', 'S-BAND RX BCH DECODER', 0),
                ('SPCSPF', 'S-BAND SPI FREQUENCY, kHz', 0),
                ('SPCHRR', 'S-BAND HK REQUEST RATE, s', 0),
                ('SPCTMD', 'S-BAND TX MODULATION', 0),
                ('SPCTFC', 'S-BAND TX FEC', 0),
                ('SBCTAG', 'S-BAND TX ATT GAIN, dB', 0),
                ('SBCTFQ', 'S-BAND TX FREQUENCY, kHz', 0),
                ('SBCRBE', 'S-BAND RX ACC BCH ERR', 0),
                ('SBCRBM', 'S-BAND RX BCH CNT MODE', 0),
                ('SBCRFQ', 'S-BAND RX FREQUENCY', 0),
                ('SBCPK1', 'S-BAND PRODUCT KEY 1', 0),
                ('SBCPK2', 'S-BAND PRODUCT KEY 2', 0),
                ('SBCPK3', 'S-BAND PRODUCT KEY 3', 0),
                ('SBCPK4', 'S-BAND PRODUCT KEY 4', 0),
            ),
        },
        'ai_std_hk': {
            'table': (
                ('name', 'Name', 0),
                ('AIJCPU', 'AI JTSN CPU USAGE, %', 0),
                ('AIJGPU', 'AI JTSN GPU USAGE, %', 0),
                ('AIJRAM', 'AI JTSN RAM USAGE, %', 0),
                ('AIJCMD', 'AI JTSN CMD CNT', 0),
                ('AIJECN', 'AI JTSN ERR CNT', 0),
                ('AIJTMP', 'AI JTSN TEMPERATURE, °C', 0),
                ('AIJPRG', 'AI JTSN UL DL PROGRESS, %', 0),
                ('AIJPWR', 'AI JTSN POWER, mW', 0),
                ('AIJUPT', 'AI JTSN UPTIME, s', 0),
                ('AIJRSC', 'AI JTSN RESET CNT', 0),
                ('AIJECO', 'AI JTSN ERROR CODE', 0),
                ('AIJPCT', 'AI JTSN PROCESS COUNTER', 0),
                ('AIJPER', 'AI JTSN PROCESS ERROR', 0),
                ('AIJPID', 'AI JTSN PROCESS ID', 0),
                ('AIKSPC', 'AI JTSN FREE SPACE, KB', 0),
                ('AIJRID', 'AI JTSN RESULT ID', 0),
                ('AIJGFR', 'AI JTSN GPU FREQ, MHz', 0),
                ('AIJSWP', 'AI JTSN SWAP USG, %', 0),
                ('AIJRTP', 'AI JTSN RESULT TYPE', 0),
                ('AIJRFL', 'AI JTSN RESULT FILES', 0),
                ('AIJBUS', 'AI JTSN BUS', 0),
                ('AIJAVA', 'AI JTSN AVAILABILITY', 0),
                ('AIJFSZ', 'AI JTSN FILE SIZE, Bytes', 0),
                ('AIJFTA', 'AI JTSN TRANSFER ARMED', 0),
                ('AIMUPT', 'AI STM UPTIME, s', 0),
                ('AIMERR', 'AI STM ERROR CODE', 0),
                ('AIMCMD', 'AI STM CMD COUNTER', 0),
                ('AIMECN', 'AI STM ERR COUNTER', 0),
                ('AIMSTE', 'AI STM JETSON STATE', 0),
                ('AIMM1S', 'AI STM EMMC1 STATE', 0),
                ('AIMM2S', 'AI STM EMMC2 STATE', 0),
                ('AIMMUX', 'AI STM MUX STATE', 0),
                ('AIMAVA', 'AI STM AVAILABILITY', 0),
                ('AIMCPS', 'AI STM COPY STATUS', 0),
                ('AIMCPP', 'AI STM COPY PROGRESS, %', 0),
                ('AIMBUS', 'AI STM BUS', 0),
                ('AIMBKR', 'AI STM BOOT KERNEL', 0),
                ('AIMBIM', 'AI STM BOOT IMAGE', 0),
                ('AIMABT', 'AI STM AUTO BOOT', 0),
                ('AIMAAC', 'AI STM AUTO APP CHECK', 0),
                ('AIMRES', 'AI STM RESERVED (1 bit)', 0),
            ),
        },
        'ai_cam_app_std_hk': {
            'table': (
                ('name', 'Name', 0),
                ('CAMUPT', 'CAM APP UPTIME, s', 0),
                ('CAMCOC', 'CAM APP CMD COUNTER', 0),
                ('CAMERC', 'CAM APP ERROR COUNTER', 0),
                ('CAMECO', 'CAM APP ERROR CODE', 0),
                ('CAMTCS', 'CAM APP TCP SOCKET STATUS', 0),
                ('CAMAVA', 'CAM APP AVAILABILITY', 0),
                ('CAMWMM', 'CAM APP WIDE NIR MODE', 0),
                ('CAMNMM', 'CAM APP NARROW NIR MODE', 0),
                ('CAMWCM', 'CAM APP WIDE RGB MODE', 0),
                ('CAMNCM', 'CAM APP NARROW RGB MODE', 0),
                ('CAMIFS', 'CAM APP INTERFACE STATUS', 0),
                ('CAMTSS', 'CAM APP TASK STATUS', 0),
                ('CAMEXS', 'CAM APP EXPERIMENT STATUS', 0),
                ('CAMIMM', 'CAM APP IMG MATCH MODE', 0),
                ('CAMTTY', 'CAM APP TASK TYPE', 0),
                ('CAMTPS', 'CAM APP TASK PROGRESS, %', 0),
                ('CAMRTP', 'CAM APP RESULT TYPE', 0),
                ('CAMWMA', 'CAM APP WIDE NIR AUTO EXP', 0),
                ('CAMNMA', 'CAM APP NRRW NIR AUTO EXP', 0),
                ('CAMWCA', 'CAM APP WIDE RGB AUTO EXP', 0),
                ('CAMNCA', 'CAM APP NRRW RGB AUTO EXP', 0),
                ('CAMRCN', 'CAM APP RESULT COUNT', 0),
                ('CAMRID', 'CAM APP RESULT ID', 0),
                ('CAMWMG', 'CAM APP WIDE NIR GAIN, dB', 0),
                ('CAMNMG', 'CAM APP NARROW NIR GAIN, dB', 0),
                ('CAMWCG', 'CAM APP WIDE RGB GAIN, dB', 0),
                ('CAMNCG', 'CAM APP NARROW RGB GAIN, dB', 0),
                ('CAMWME', 'CAM APP WIDE NIR EXP TIME, µs', 0),
                ('CAMNME', 'CAM APP NRRW NIR EXP TIME, µs', 0),
                ('CAMWCE', 'CAM APP WIDE RGB EXP TIME, µs', 0),
                ('CAMNCE', 'CAM APP NRRW RGB EXP TIME, µs', 0),
            ),
        },
        'ai_ws_app_std_hk': {
            'table': (
                ('name', 'Name', 0),
                ('AIWSUP', 'AI WS UPTIME, s', 0),
                ('AIWSTC', 'AI WS CMD COUNTER', 0),
                ('AIWSER', 'AI WS ERROR COUNTER', 0),
                ('AIWSEC', 'AI WS ERROR CODE', 0),
                ('AIWSCA', 'AI WS Reserved (16 bit)', 0),
                ('AIWSCS', 'AI WS Reserved (4 bit)', 0),
                ('AIWSAS', 'AI WS AI STATUS', 0),
                ('AIWSEP', 'AI WS EXECUTION PROGRESS, %', 0),
                ('AIWSIC', 'AI WS IMAGE COUNTER', 0),
                ('AIWSRI', 'AI WS RESULT ID', 0),
                ('AIWSRT', 'AI WS RESULT TYPE', 0),
                ('AIWSNF', 'AI WS RESULT NUM FILES', 0),
                ('AIWSSP', 'AI WS SPACE PERCENT, %', 0),
                ('AIWSCP', 'AI WS CLOUD PERCENT, %', 0),
                ('AIWSLP', 'AI WS LAND PERCENT, %', 0),
                ('AIWSWP', 'AI WS WATER PERCENT, %', 0),
                ('AIWSNP', 'AI WS SUN PERCENT, %', 0),
                ('AIWSFP', 'AI WS LENSFLARE PERCENT, %', 0),
                ('AIWS1A', 'AI WS CONV1 ACTIVE', 0),
                ('AIWS2A', 'AI WS CONV2 ACTIVE', 0),
                ('AIWSBA', 'AI WS BRIGHTNESS ACTIVE', 0),
                ('AIWSFA', 'AI WS CONTRAST ACTIVE', 0),
                ('AIWSGA', 'AI WS GAMMA ACTIVE', 0),
                ('AIWSHA', 'AI WS HUE_ROTATION ACTIVE', 0),
                ('AIWSSA', 'AI WS SATURATION ACTIVE', 0),
                ('AIWSKI', 'AI WS AI INIT', 0),
                ('AIWSLM', 'AI WS LOADED MODEL', 0),
            ),
        },
        'ai_ns_app_std_hk': {
            'table': (
                ('name', 'Name', 0),
                ('AINSUP', 'AI NS UPTIME, s', 0),
                ('AINSTC', 'AI NS CMD COUNTER', 0),
                ('AINSER', 'AI NS ERROR COUNTER', 0),
                ('AINSEC', 'AI NS ERROR CODE', 0),
                ('AINSCA', 'AI NS Reserved (16 bit)', 0),
                ('AINSCS', 'AI NS Reserved (4 bit)', 0),
                ('AINSAS', 'AI NS AI STATUS', 0),
                ('AINSEP', 'AI NS EXECUTION PROGRESS, %', 0),
                ('AINSIC', 'AI NS IMAGE COUNTER', 0),
                ('AINSRI', 'AI NS RESULT ID', 0),
                ('AINSRT', 'AI NS RESULT TYPE', 0),
                ('AINSNF', 'AI NS RESULT NUM FILES', 0),
                ('AINSCL', 'AI NS CLTIVTD LAND PRCNT, %', 0),
                ('AINSFP', 'AI NS FOREST PERCENT, %', 0),
                ('AINSGL', 'AI NS GRASSLAND PERCENT, %', 0),
                ('AINSSP', 'AI NS SHRUBLAND PERCENT, %', 0),
                ('AINSWP', 'AI NS WATER PERCENT, %', 0),
                ('AINSWL', 'AI NS WETLANDS PERCENT, %', 0),
                ('AINSTP', 'AI NS TUNDRA PERCENT, %', 0),
                ('AINSAP', 'AI NS ARTIFICIAL PERCENT, %', 0),
                ('AINSBP', 'AI NS BARELAND PERCENT, %', 0),
                ('AINSIP', 'AI NS ICE PERCENT, %', 0),
                ('AINSCP', 'AI NS CLOUD PERCENT, %', 0),
                ('AINS1A', 'AI NS CONV1 ACTIVE', 0),
                ('AINS2A', 'AI NS CONV2 ACTIVE', 0),
                ('AINSBA', 'AI NS BRIGHTNESS ACTIVE', 0),
                ('AINSFA', 'AI NS CONTRAST ACTIVE', 0),
                ('AINSGA', 'AI NS GAMMA ACTIVE', 0),
                ('AINSHA', 'AI NS HUE_ROTATION ACTIVE', 0),
                ('AINSSA', 'AI NS SATURATION ACTIVE', 0),
                ('AINSKI', 'AI NS AI INIT', 0),
                ('AINSLM', 'AI NS LOADED MODEL', 0),
            ),
        },
        'ai_od_app_std_hk': {
            'table': (
                ('name', 'Name', 0),
                ('AIODUP', 'AI OD UPTIME, s', 0),
                ('AIODTC', 'AI OD CMD COUNTER', 0),
                ('AIODER', 'AI OD ERROR COUNTER', 0),
                ('AIODEC', 'AI OD ERROR CODE', 0),
                ('AIODCA', 'AI OD Reserved (16 bit)', 0),
                ('AIODCS', 'AI OD Reserved (4 bit)', 0),
                ('AIODAS', 'AI OD AI STATUS', 0),
                ('AIODEP', 'AI OD EXECUTION PROGRESS, %', 0),
                ('AIODIC', 'AI OD IMAGE COUNTER', 0),
                ('AIODRI', 'AI OD RESULT ID', 0),
                ('AIODRT', 'AI OD RESULT TYPE', 0),
                ('AIODNF', 'AI OD RESULT NUM FILES', 0),
                ('AIODWA', 'AI OD MAX CONFIDENCE, %', 0),
                ('AIODCP', 'AI OD MIN CONFIDENCE, %', 0),
                ('AIODGP', 'AI OD SUM DETECTIONS', 0),
                ('AIODIP', 'AI OD TRIANGLES', 0),
                ('AIODFP', 'AI OD CIRCLES', 0),
                ('AIODWL', 'AI OD RECTANGLES', 0),
                ('AIODR1', 'AI OD Reserved 1 (8-bit)', 0),
                ('AIODR2', 'AI OD Reserved 2 (8-bit)', 0),
                ('AIODR3', 'AI OD Reserved 3 (8-bit)', 0),
                ('AIODR4', 'AI OD Reserved 4 (8-bit)', 0),
                ('AIODR5', 'AI OD Reserved 5 (8-bit)', 0),
                ('AIODR6', 'AI OD Reserved 6 (8-bit)', 0),
                ('AIODR7', 'AI OD Reserved 7 (8-bit)', 0),
                ('AIODR8', 'AI OD Reserved 8 (8-bit)', 0),
                ('AIOD1A', 'AI OD CONV1 ACTIVE', 0),
                ('AIOD2A', 'AI OD CONV2 ACTIVE', 0),
                ('AIODBA', 'AI OD BRIGHTNESS ACTIVE', 0),
                ('AIODFA', 'AI OD CONTRAST ACTIVE', 0),
                ('AIODGA', 'AI OD GAMMA ACTIVE', 0),
                ('AIODHA', 'AI OD HUE_ROTATION ACTIVE', 0),
                ('AIODSA', 'AI OD SATURATION ACTIVE', 0),
                ('AIODKI', 'AI OD AI INIT', 0),
                ('AIODLM', 'AI OD LOADED MODEL', 0),
                ('AIODR9', 'AI OD Reserved 9 (8-bit)', 0),
            ),
        },
        'ai_ad_app_std_hk': {
            'table': (
                ('name', 'Name', 0),
                ('AIADUP', 'AI AD UPTIME, s', 0),
                ('AIADTC', 'AI AD CMD COUNTER', 0),
                ('AIADER', 'AI AD ERROR COUNTER', 0),
                ('AIADEC', 'AI AD ERROR CODE', 0),
                ('AIADCA', 'AI AD ACTIVE CLASSIFIER', 0),
                ('AIADR2', 'AI AD RESERVED (1 bit)', 0),
                ('AIAD1A', 'AI AD CONV1 ACTIVE', 0),
                ('AIAD2A', 'AI AD CONV2 ACTIVE', 0),
                ('AIADBA', 'AI AD BRIGHTNESS ACTIVE', 0),
                ('AIADFA', 'AI AD CONTRAST ACTIVE', 0),
                ('AIADGA', 'AI AD GAMMA ACTIVE', 0),
                ('AIADHA', 'AI AD HUE_ROTATION ACTIVE', 0),
                ('AIADSA', 'AI AD SATURATION ACTIVE', 0),
                ('AIADCS', 'AI AD Reserved (4 bit)', 0),
                ('AIADAS', 'AI AD AI STATUS', 0),
                ('AIADPR', 'AI AD EXECUTION PROGRESS, %', 0),
                ('AIADIC', 'AI AD IMAGE COUNTER', 0),
                ('AIADRI', 'AI AD RESULT ID', 0),
                ('AIADRT', 'AI AD RESULT TYPE', 0),
                ('AIADNF', 'AI AD RESULT NUM FILES', 0),
                ('AIADLO', 'AI AD LAST LOSS', 0),
                ('AIADAC', 'AI AD LAST VAL LOSS', 0),
                ('AIADSC', 'AI AD ANOMALIE SCORE', 0),
                ('AIADIP', 'AI AD CLASSIFIER SCORE', 0),
                ('AIADEO', 'AI AD EPOCHS', 0),
                ('AIADAD', 'AI AD ACTIVE DATASET', 0),
                ('AIADAM', 'AI AD ACTIVE MODEL', 0),
                ('AIADIF', 'AI AD INIT FLAG', 0),
                ('AIADAV', 'AI AD AVAILABLE', 0),
                ('AIADRS', 'AI AD RESERVED (6 bit)', 0),
                ('AIADDN', 'AI AD IMAGES N DATASET', 0),
                ('AIADDA', 'AI AD IMAGES A DATASET', 0),
            ),
        },
        'ai_ld_app_std_hk': {
            'table': (
                ('name', 'Name', 0),
                ('LDCMDC', 'LD CMD COUNTER', 0),
                ('LDERCO', 'LD ERROR COUNTER', 0),
                ('LDERCD', 'LD ERROR CODE', 0),
                ('LDFPSR', 'LD COMPUTATION FPS', 0),
                ('LDFWEV', 'LD FRAMES WITH EVENTS', 0),
                ('LDRES2', 'LD Reserved (1 bit)', 0),
                ('LDTCPS', 'LD TCP SOCKET STATUS', 0),
                ('LDIPST', 'LD IMAGE PROCESSING STS', 0),
                ('LDRGBU', 'LD RGB CAMERA USAGE', 0),
                ('LDRES3', 'LD Reserved (1 bit)', 0),
                ('LDFRMC', 'LD FRAME COUNT', 0),
                ('LDEVCT', 'LD TOTAL EVENT COUNT', 0),
                ('LDLEFC', 'LD LAST EVENT FRAME COUNT', 0),
                ('LDLEBG', 'LD LAST EVENT BRIGHTNESS', 0),
                ('LDUPTM', 'LD UPTIME, s', 0),
                ('LDLRES', 'LD LAST RESULT ID', 0),
                ('LDTLEC', 'LD TOO LONG EVENT COUNT', 0),
                ('LDCPRT', 'LD CPU PROCESSING TIME, ms', 0),
                ('LDRDTM', 'LD READOUT TIME, ms', 0),
                ('LDGPRT', 'LD GPU PROCESSING TIME, ms', 0),
                ('LDBSAL', 'LD BACKGROUND SUBS ALGO', 0),
                ('LDLETP', 'LD LAST EVENT TYP', 0),
                ('LDRGBM', 'LD RGB CAMERA MODE', 0),
                ('LDNIRM', 'LD NIR CAMERA MODE', 0),
                ('LDTSEC', 'LD TOO SHORT EVENT COUNT', 0),
                ('LDNIRG', 'LD NIR CAMERA GAIN', 0),
                ('LDNIRE', 'LD NIR CAMERA EXP TIME, µs', 0),
            ),
        },
        'ai_app_07_std_hk': {
            'table': (
                ('name', 'Name', 0),
                ('AI07D1', 'DUMMY', 0),
                ('AI07D2', 'DUMMY', 0),
                ('AI07D3', 'DUMMY', 0),
                ('AI07D4', 'DUMMY', 0),
                ('AI07D5', 'DUMMY', 0),
                ('AI07D6', 'DUMMY', 0),
                ('AI07D7', 'DUMMY', 0),
            ),
        },
        'ai_app_08_std_hk': {
            'table': (
                ('name', 'Name', 0),
                ('AI08D1', 'DUMMY', 0),
                ('AI08D2', 'DUMMY', 0),
                ('AI08D3', 'DUMMY', 0),
                ('AI08D4', 'DUMMY', 0),
                ('AI08D5', 'DUMMY', 0),
                ('AI08D6', 'DUMMY', 0),
                ('AI08D7', 'DUMMY', 0),
            ),
        },
        'ai_app_09_std_hk': {
            'table': (
                ('name', 'Name', 0),
                ('AI09D1', 'DUMMY', 0),
                ('AI09D2', 'DUMMY', 0),
                ('AI09D3', 'DUMMY', 0),
                ('AI09D4', 'DUMMY', 0),
                ('AI09D5', 'DUMMY', 0),
                ('AI09D6', 'DUMMY', 0),
                ('AI09D7', 'DUMMY', 0),
            ),
        },
        'ai_app_10_std_hk': {
            'table': (
                ('name', 'Name', 0),
                ('AI10D1', 'DUMMY', 0),
                ('AI10D2', 'DUMMY', 0),
                ('AI10D3', 'DUMMY', 0),
                ('AI10D4', 'DUMMY', 0),
                ('AI10D5', 'DUMMY', 0),
                ('AI10D6', 'DUMMY', 0),
                ('AI10D7', 'DUMMY', 0),
            ),
        },
        'ai_cam_cfg_hk': {
            'table': (
                ('name', 'Name', 0),
                ('AICCET', 'AI CAM EXP TIME, µs', 0),
                ('AICCIC', 'AI CAM RGB CAM', 0),
                ('AICCAG', 'AI CAM AUTO GAIN', 0),
                ('AICCAE', 'AI CAM AUTO EXPOSURE', 0),
                ('AICCAO', 'AI CAM AUTO OFFSET', 0),
                ('AICCBL', 'AI CAM BLACK LEVEL', 0),
                ('AICCGN', 'AI CAM GAIN', 0),
                ('AICCOX', 'AI CAM OFFSET X', 0),
                ('AICCOY', 'AI CAM OFFSET Y', 0),
                ('AICCCN', 'AI CAM CONTRAST', 0),
                ('AICCGM', 'AI CAM GAMMA', 0),
                ('AICCST', 'AI CAM SATURATION', 0),
                ('AICCWE', 'AI CAM WHITE BALANCE', 0),
                ('AICCWA', 'AI CAM AUTO WHITE BALANCE', 0),
                ('AICCHU', 'AI CAM HUE', 0),
                ('AICCWR', 'AI CAM WB RED', 0),
                ('AICCWG', 'AI CAM WB GREEN', 0),
                ('AICCWB', 'AI CAM WB BLUE', 0),
                ('AICCGU', 'AI CAM GAIN UPPER LIMIT', 0),
                ('AICCTB', 'AI CAM TNMPPG GLBL BRGHT', 0),
                ('AICCGL', 'AI CAM GAIN LOW LIMIT', 0),
                ('AICCFR', 'AI CAM FRAMERATE, FPS', 0),
                ('AICCEA', 'AI CAM EXP AUTO REFERENCE', 0),
                ('AICCTI', 'AI CAM TONEMAP INTENSITY', 0),
                ('AICCLA', 'AI CAM EXP UP LIMIT AUTO', 0),
                ('AICCTM', 'AI CAM TONEMAPPING', 0),
                ('AICCHT', 'AI CAM HEIGHT, px', 0),
                ('AICCEL', 'AI CAM AUTO EXP MIN, µs', 0),
                ('AICCEU', 'AI CAM AUTO EXP MAX, µs', 0),
                ('AICCDN', 'AI CAM DENOISE', 0),
                ('AICCSH', 'AI CAM SHARPNESS', 0),
                ('AICCCT', 'AI CAM TYPE', 0),
                ('AICCAV', 'AI CAM CFG AVAILABLE', 0),
                ('AICCHR', 'AI CAM HIGHLIGHT REDUCT', 0),
                ('AICCR1', 'AI CAM RESERVED (1 bit)', 0),
                ('AICCWT', 'AI CAM WIDTH, px', 0),
                ('AICCAF', 'AI CAM ACTIVE CONFIG', 0),
                ('AICCSN', 'AI CAM SERIAL NUMBER', 0),
            ),
        },
        'ai_app_ld_cfg_hk': {
            'table': (
                ('name', 'Name', 0),
                ('LDCOFX', 'LD RGB NIR OFFSET X', 0),
                ('LDCOFY', 'LD RGB NIR OFFSET Y', 0),
                ('LDCRBC', 'LD RING BUFFER COUNT', 0),
                ('LDCFBE', 'LD FRAMES BEFORE EVENT', 0),
                ('LDCFAE', 'LD FRAMES AFTER EVENT', 0),
                ('LDCDIR', 'LD DILATION RADIUS', 0),
                ('LDCERR', 'LD EROSION RADIUS', 0),
                ('LDCBSM', 'LD BOX SAVE MARGIN', 0),
                ('LDCLDS', 'LD MIN DET SIZE THRESH', 0),
                ('LDCUDS', 'LD MAX DET SIZE THRESH', 0),
                ('LDCLED', 'LD MIN EVENT DUR THRESH', 0),
                ('LDCUED', 'LD MAX EVENT DUR THRESH', 0),
                ('LDCAVA', 'LD AVAILABILITY', 0),
                ('LDCURC', 'LD RGB CAMERA USAGE', 0),
                ('LDCMTI', 'LD SAVE MARKED THMB IMG', 0),
                ('LDCRES', 'LD RESERVED (3 bit)', 0),
                ('LDCBSA', 'LD BACKGROUND SUB ALGO', 0),
                ('LDCMAF', 'LD MIN ADAPT FRAME CNT', 0),
                ('LDCBOV', 'LD BOX OVERLAP VALUE', 0),
                ('LDCEMR', 'LD EVENT MATCH RADIUS', 0),
                ('LDCSDL', 'LD SIGMA DELTA VMAX', 0),
                ('LDCSDU', 'LD SIGMA DELTA VMIN', 0),
                ('LDCSDT', 'LD SIGMA DELTA TV', 0),
                ('LDCSDN', 'LD SIGMA DELTA LOGN', 0),
                ('LDCGAA', 'LD GAUSSIAN ALPHA', 0),
                ('LDCGAK', 'LD GAUSSIAN K', 0),
                ('LDCDAC', 'LD DEFECT PIXEL AREA CNT', 0),
                ('LDCRS2', 'LD RESERVED (16 bit)', 0),
            ),
        },
        'ai_cam_img_match_cfg': {
            'table': (
                ('name', 'Name', 0),
                ('AIIMCR', 'AI CAM IM CROP MODE', 0),
                ('AIIMMM', 'AI CAM IM MIN MATCHES', 0),
                ('AIIMDT', 'AI CAM IM DIST THRESH', 0),
                ('AIIMDR', 'AI CAM IM DIST RATIO', 0),
                ('AIIM11', 'AI CAM MATCHING MATRIX 11', 0),
                ('AIIM33', 'AI CAM MATCHING MATRIX 33', 0),
                ('AIIM31', 'AI CAM MATCHING MATRIX 31', 0),
                ('AIIM32', 'AI CAM MATCHING MATRIX 32', 0),
                ('AIIM12', 'AI CAM MATCHING MATRIX 12', 0),
                ('AIIMOP', 'AI CAM MATCHING OP MODE', 0),
                ('AIIMAV', 'AI CAM MATCHING AVAIL', 0),
                ('AIIM13', 'AI CAM MATCHING MATRIX 13', 0),
                ('AIIM21', 'AI CAM MATCHING MATRIX 21', 0),
                ('AIIM22', 'AI CAM MATCHING MATRIX 22', 0),
                ('AIIM23', 'AI CAM MATCHING MATRIX 23', 0),
            ),
        },
        'mview_std_hk': {
            'table': (
                ('name', 'Name', 0),
                ('MVE1DG', 'MV Z1 ERR CODE GENERAL', 0),
                ('MVE1DI', 'MV Z1 ERR CODE INTERNAL, hex', 0),
                ('MVE1CT', 'MV Z1 ERR CNT', 0),
                ('MVZ1RC', 'MV Z1 RESET CNT', 0),
                ('MVZ1RO', 'MV Z1 ROLE', 0),
                ('MVZ1ST', 'MV Z1 STATE', 0),
                ('MVZ1CC', 'MV Z1 CMD CNT', 0),
                ('MVZ1HI', 'MV Z1 HW ID', 0),
                ('MVZ1PE', 'MV Z1 POWER EN', 0),
                ('MVZ1UI', 'MV Z1 UART MAIN IF ID', 0),
                ('MVZ1OR', 'MV Z1 OTHER MCU RESPOND', 0),
                ('MVE2DG', 'MV Z2 ERR CODE GENERAL', 0),
                ('MVE2DI', 'MV Z2 ERR CODE INTERNAL, hex', 0),
                ('MVE2CT', 'MV Z2 ERR CNT', 0),
                ('MVZ2RC', 'MV Z2 RESET CNT', 0),
                ('MVZ2RO', 'MV Z2 ROLE', 0),
                ('MVZ2ST', 'MV Z2 STATE', 0),
                ('MVZ2CC', 'MV Z2 CMD CNT', 0),
                ('MVZ2HI', 'MV Z2 HW ID', 0),
                ('MVZ2PE', 'MV Z2 POWER EN', 0),
                ('MVZ2UI', 'MV Z2 UART MAIN IF ID', 0),
                ('MVZ2OR', 'MV Z2 OTHER MCU RESPOND', 0),
                ('MVSMST', 'MV ACTIVE SM STATE', 0),
                ('MVSMAC', 'MV ACTIVE SM AUTO CAL', 0),
                ('MVSTEM', 'MV ACTIVE SM TEMPERATURE, °C', 0),
                ('MVS1MK', 'MV SM 1 ACT MASK', 0),
                ('MVS2MK', 'MV SM 2 ACT MASK', 0),
                ('MVS3MK', 'MV SM 3 ACT MASK', 0),
                ('MVS4MK', 'MV SM 4 ACT MASK', 0),
                ('MVS1DF', 'MV SM 1 DEFECT', 0),
                ('MVS2DF', 'MV SM 2 DEFECT', 0),
                ('MVS3DF', 'MV SM 3 DEFECT', 0),
                ('MVS4DF', 'MV SM 4 DEFECT', 0),
                ('MVS1PE', 'MV SM 1 PWR EN', 0),
                ('MVS2PE', 'MV SM 2 PWR EN', 0),
                ('MVS3PE', 'MV SM 3 PWR EN', 0),
                ('MVS4PE', 'MV SM 4 PWR EN', 0),
                ('MVADMD', 'MV AD MODE', 0),
                ('MVASID', 'MV AD SM ID', 0),
                ('MVADVA', 'MV AD DATA VALID', 0),
                ('MVASRY', 'MV NO SM READY', 0),
                ('MVADEC', 'MV AD ERR CODE', 0),
                ('MVAQ1N', 'MV Q1 NORM', 0),
                ('MVAQ2N', 'MV Q2 NORM', 0),
                ('MVAQ3N', 'MV Q3 NORM', 0),
            ),
        },
        'mview_cfg_hk': {
            'table': (
                ('name', 'Name', 0),
                ('MVCZUE', 'MV CFG ZE UART ERR MASK', 0),
                ('MVCZMR', 'MV CFG ZE SM MAX RETRY', 0),
                ('MVCZCC', 'MV CFG ZE CACHE ADDR CAT', 0),
                ('MVCZCI', 'MV CFG ZE CACHE ADDR IMG', 0),
                ('MVCZCS', 'MV CFG ZE CACHE ADDR SW', 0),
                ('MVCZHW', 'MV CFG ZE HW ID', 0),
                ('MVCSAV', 'MV CFG SM AVAIL', 0),
                ('MVCSID', 'MV CFG SM ID', 0),
                ('MVCS14', 'MV CFG SM CAM GAIN, x', 0),
                ('MVCS15', 'MV CFG SM CAM EXPOSURE, ms', 0),
                ('MVCS00', 'MV CFG SM CAT 1 ADDR', 0),
                ('MVCS01', 'MV CFG SM CAT 2 ADDR', 0),
                ('MVCS02', 'MV CFG SM CAT 3 ADDR', 0),
                ('MVCS03', 'MV CFG SM CAT CRC32', 0),
                ('MVCS04', 'MV CFG SM CAT LEN', 0),
                ('MVCS05', 'MV CFG SM VEC DB ADDR', 0),
                ('MVCS06', 'MV CFG SM VEC DB MAX LEN', 0),
                ('MVCS07', 'MV CFG SM VEC DB ENTRIES', 0),
                ('MVCS08', 'MV CFG SM NUM STARS, Stars', 0),
                ('MVCS09', 'MV CFG SM BIT VEC LEN', 0),
                ('MVCS0A', 'MV CFG SM SEN MAG', 0),
                ('MVCS0B', 'MV CFG SM ACURRACY', 0),
                ('MVCS0C', 'MV CFG SM DIAG IMG PX, px', 0),
                ('MVCS0D', 'MV CFG SM MIN DIST, px', 0),
                ('MVCS0E', 'MV CFG SM FOCAL LEN PX, px', 0),
                ('MVCS0F', 'MV CFG SM MIN STARSIZE PX, px', 0),
                ('MVCS10', 'MV CFG SM RECGN THRESH', 0),
                ('MVCS11', 'MV CFG SM RECGN MAX MASS', 0),
                ('MVCS12', 'MV CFG SM RECGN OFFSET X, px', 0),
                ('MVCS13', 'MV CFG SM RECGN OFFSET Y, px', 0),
                ('MVCS16', 'MV CFG SM IMG CROP OFFS X, px', 0),
                ('MVCS17', 'MV CFG SM IMG CROP OFFS Y, px', 0),
                ('MVCS18', 'MV CFG SM IDNT PAT LEN UP', 0),
                ('MVCS19', 'MV CFG SM IDNT PAT LEN LO', 0),
                ('MVCS1A', 'MV CFG SM VEC ACCURACY', 0),
                ('MVCS1B', 'MV CFG SM COSA, deg', 0),
                ('MVCS1C', 'MV CFG SM P1', 0),
                ('MVCS1D', 'MV CFG SM P2', 0),
                ('MVCS1E', 'MV CFG SM S1', 0),
                ('MVCS1F', 'MV CFG SM S2', 0),
                ('MVCS20', 'MV CFG SM K1', 0),
                ('MVCS21', 'MV CFG SM K2', 0),
            ),
        },
        'mview_ext_hk': {
            'table': (
                ('name', 'Name', 0),
                ('MVPTPR', 'MV TOTAL PROGRESS, %', 0),
                ('MVPRHI', 'MV PROGRESS HW ID', 0),
                ('MVPOTY', 'MV PROGRESS OP TYPE', 0),
                ('MVPRCD', 'MV PROGRESS RES CODE', 0),
                ('MVPOST', 'MV PROGRESS OP STEP', 0),
                ('MVRES1', 'MV Reserved (4 bit)', 0),
            ),
        },
        'thruster_std_hk': {
            'table': (
                ('name', 'Name', 0),
                ('TH1TM1', 'THRUSTER 1 TEMP 1, °C', 0),
                ('TH1TM2', 'THRUSTER 1 TEMP 2, °C', 0),
                ('TH1TM3', 'THRUSTER 1 TEMP 3, °C', 0),
                ('TH1TMI', 'THRUSTER 1 TEMP I2C, °C', 0),
                ('TH1ECN', 'THRUSTER 1 ERROR COUNTER', 0),
                ('TH1ECO', 'THRUSTER 1 ERROR CODE', 0),
                ('TH1CCN', 'THRUSTER 1 CMD COUNTER', 0),
                ('TH1CHE', 'THRUSTER 1 CHARGER ENABLE', 0),
                ('TH1IGE', 'THRUSTER 1 IGNITOR ENABLE', 0),
                ('TH1AVA', 'THRUSTER 1 HK AVAILABLE', 0),
                ('TH1STA', 'THRUSTER 1 STATISTICS AV', 0),
                ('TH1IGC', 'THRUSTER 1 IGNITION CNT', 0),
                ('TH2TM1', 'THRUSTER 2 TEMP 1, °C', 0),
                ('TH2TM2', 'THRUSTER 2 TEMP 2, °C', 0),
                ('TH2TM3', 'THRUSTER 2 TEMP 3, °C', 0),
                ('TH2TMI', 'THRUSTER 2 TEMP I2C, °C', 0),
                ('TH2ECN', 'THRUSTER 2 ERROR COUNTER', 0),
                ('TH2ECO', 'THRUSTER 2 ERROR CODE', 0),
                ('TH2CCN', 'THRUSTER 2 CMD COUNTER', 0),
                ('TH2CHE', 'THRUSTER 2 CHARGER ENABLE', 0),
                ('TH2IGE', 'THRUSTER 2 IGNITOR ENABLE', 0),
                ('TH2AVA', 'THRUSTER 2 HK AVAILABLE', 0),
                ('TH2STA', 'THRUSTER 2 STATISTICS AV', 0),
                ('TH2IGC', 'THRUSTER 2 IGNITION CNT', 0),
                ('TH1RIG', 'THRUSTER 1 REMAIN IGNS', 0),
                ('TH1CAV', 'THRUSTER 1 AVG CHARGE DUR, ms', 0),
                ('TH2RIG', 'THRUSTER 2 REMAIN IGNS', 0),
                ('TH2CAV', 'THRUSTER 2 AVG CHARGE DUR, ms', 0),
                ('TH1CEC', 'THRUSTER 1 CHARGE ERR CNT', 0),
                ('TH1CMI', 'THRUSTER 1 MIN CHARGE DUR, ms', 0),
                ('TH1CMA', 'THRUSTER 1 MAX CHARGE DUR, ms', 0),
                ('TH1CLD', 'THRUSTER 1 LST CHARGE DUR, ms', 0),
                ('TH2CEC', 'THRUSTER 2 CHARGE ERR CNT', 0),
                ('TH2CMI', 'THRUSTER 2 MIN CHARGE DUR, ms', 0),
                ('TH2CMA', 'THRUSTER 2 MAX CHARGE DUR, ms', 0),
                ('TH2CLD', 'THRUSTER 2 LST CHARGE DUR, ms', 0),
            ),
        },
        'thruster_cfg_hk': {
            'table': (
                ('name', 'Name', 0),
                ('THMICT', 'MIN CHARGE TIME, ms', 0),
                ('THMACT', 'MAX CHARGE TIME, ms', 0),
                ('THPUDI', 'PULSE DISTANCE, ms', 0),
                ('THIGDI', 'IGNITION DISTANCE, ms', 0),
                ('THPUPI', 'PULSES PER IGNITION', 0),
                ('THEMT1', 'ERR MASK TEMP1 DISABLING', 0),
                ('THEMT2', 'ERR MASK TEMP2 DISABLING', 0),
                ('THEMT3', 'ERR MASK TEMP3 DISABLING', 0),
                ('THEMTI', 'ERR MASK TEMI2C DISABLING', 0),
                ('THEMNE', 'ERR MASK CHRG N_EN DISABL', 0),
                ('THEMTO', 'ERR MASK CHRG T/O DISABL', 0),
                ('THEMTS', 'ERR MASK TOO SHORT DISABL', 0),
                ('THEMFT', 'ERR MASK HW FAULT DISABL', 0),
                ('THRESV', 'THRUSTER EXT RESERVED', 0),
                ('THEXTS', 'EXT HK SOURCE THRUSTER', 0),
                ('THT1LL', 'TEMP 1 LOWER LIMIT', 0),
                ('THT1UL', 'TEMP 1 UPPER LIMIT', 0),
                ('THT2LL', 'TEMP 2 LOWER LIMIT', 0),
                ('THT2UL', 'TEMP 2 UPPER LIMIT', 0),
                ('THT3LL', 'TEMP 3 LOWER LIMIT', 0),
                ('THT3UL', 'TEMP 3 UPPER LIMIT', 0),
                ('THTILL', 'TEMP I2C LOWER LIMIT', 0),
                ('THTIUL', 'TEMP I2C UPPER LIMIT', 0),
                ('THRUPT', 'RAMP UP TIME, ms', 0),
            ),
        },
        'gps_std_hk': {
            'table': (
                ('name', 'Name', 0),
                ('GPS1PS', 'GNSS1 POWER STATUS', 0),
                ('GPS1BS', 'GNSS1 BACKUP POWER STATUS', 0),
                ('GPS1AV', 'GNSS1 AVAILABILITY', 0),
                ('GPS1PT', 'GNSS1 PUBLISH UTC ENABLED', 0),
                ('GPS1RN', 'GNSS1 RECORDING NMEA', 0),
                ('GPS1MF', 'GNSS1 REC MEM FULL', 0),
                ('GPS1RS', 'GNSS1 RESERVED', 0),
                ('GPS1UT', 'GNSS1 UTC TIME, sec', 0),
                ('GPS1QL', 'GNSS1 QUALITY', 0),
                ('GPS1SU', 'GNSS1 SATS IN USE', 0),
                ('GPS2PS', 'GNSS2 POWER STATUS', 0),
                ('GPS2BS', 'GNSS2 BACKUP POWER STATUS', 0),
                ('GPS2AV', 'GNSS2 AVAILABILITY', 0),
                ('GPS2PT', 'GNSS2 PUBLISH UTC ENABLED', 0),
                ('GPS2RN', 'GNSS2 RECORDING NMEA', 0),
                ('GPS2MF', 'GNSS2 REC MEM FULL', 0),
                ('GPS2RS', 'GNSS2 RESERVED', 0),
                ('GPS2UT', 'GNSS2 UTC TIME, sec', 0),
                ('GPS2QL', 'GNSS2 QUALITY', 0),
                ('GPS2SU', 'GNSS2 SATS IN USE', 0),
                ('GPS1LT', 'GNSS1 LATITUDE, ° N', 0),
                ('GPS1LN', 'GNSS1 LONGITUDE, ° E', 0),
                ('GPS2LT', 'GNSS2 LATITUDE, ° N', 0),
                ('GPS2LN', 'GNSS2 LONGITUDE, ° E', 0),
                ('GPS1AL', 'GNSS1 ALTITUDE, km', 0),
                ('GPS1SP', 'GNSS1 SPEED, km/h', 0),
                ('GPS2AL', 'GNSS2 ALTITUDE, km', 0),
                ('GPS2SP', 'GNSS2 SPEED, km/h', 0),
                ('GPS1FC', 'GNSS1 NMEA FRAME CNT', 0),
                ('GPS1SV', 'GNSS1 SATS IN VIEW', 0),
                ('GPS1ER', 'GNSS1 ERROR CODE', 0),
                ('GPS1CC', 'GNSS1 COMMAND COUNTER', 0),
                ('GPS1EC', 'GNSS1 ERROR COUNTER', 0),
                ('GPS2FC', 'GNSS2 NMEA FRAME CNT', 0),
                ('GPS2SV', 'GNSS2 SATS IN VIEW', 0),
                ('GPS2ER', 'GNSS2 ERROR CODE', 0),
                ('GPS2CC', 'GNSS2 COMMAND COUNTER', 0),
                ('GPS2EC', 'GNSS2 ERROR COUNTER', 0),
            ),
        },
        'reserved_apid_1': {
            'table': (
                ('name', 'Name', 0),
                ('RES011', 'DUMMY', 0),
                ('RES012', 'DUMMY', 0),
                ('RES013', 'DUMMY', 0),
                ('RES014', 'DUMMY', 0),
                ('RES015', 'DUMMY', 0),
                ('RES016', 'DUMMY', 0),
            ),
        },
        'obdh_cfg_raw': {
            'table': (
                ('name', 'Name', 0),
                ('data', 'data', 0),
            ),
        },
        'obdh_swupld_rcvd_sgmnts': {
            'table': (
                ('name', 'Name', 0),
                ('data', 'data', 0),
            ),
        },
        'obdh_mem_exp_data': {
            'table': (
                ('name', 'Name', 0),
                ('data', 'data', 0),
            ),
        },
        'obdh_time_ext_live': {
            'table': (
                ('name', 'Name', 0),
                ('data', 'data', 0),
            ),
        },
        'leop_list_1': {
            'table': (
                ('name', 'Name', 0),
                ('data', 'data', 0),
            ),
        },
        'leop_list_2': {
            'table': (
                ('name', 'Name', 0),
                ('data', 'data', 0),
            ),
        },
        'leop_list_3': {
            'table': (
                ('name', 'Name', 0),
                ('data', 'data', 0),
            ),
        },
        'active_safe_mode_list_1': {
            'table': (
                ('name', 'Name', 0),
                ('data', 'data', 0),
            ),
        },
        'active_safe_mode_list_2': {
            'table': (
                ('name', 'Name', 0),
                ('data', 'data', 0),
            ),
        },
        'active_safe_mode_list_3': {
            'table': (
                ('name', 'Name', 0),
                ('data', 'data', 0),
            ),
        },
        'passive_safe_mode_list': {
            'table': (
                ('name', 'Name', 0),
                ('data', 'data', 0),
            ),
        },
        'routine_procedure_1': {
            'table': (
                ('name', 'Name', 0),
                ('data', 'data', 0),
            ),
        },
        'routine_procedure_2': {
            'table': (
                ('name', 'Name', 0),
                ('data', 'data', 0),
            ),
        },
        'routine_procedure_3': {
            'table': (
                ('name', 'Name', 0),
                ('data', 'data', 0),
            ),
        },
        'routine_procedure_4': {
            'table': (
                ('name', 'Name', 0),
                ('data', 'data', 0),
            ),
        },
        'routine_procedure_5': {
            'table': (
                ('name', 'Name', 0),
                ('data', 'data', 0),
            ),
        },
        'routine_procedure_6': {
            'table': (
                ('name', 'Name', 0),
                ('data', 'data', 0),
            ),
        },
        'routine_procedure_7': {
            'table': (
                ('name', 'Name', 0),
                ('data', 'data', 0),
            ),
        },
        'routine_procedure_8': {
            'table': (
                ('name', 'Name', 0),
                ('data', 'data', 0),
            ),
        },
        'routine_procedure_9': {
            'table': (
                ('name', 'Name', 0),
                ('data', 'data', 0),
            ),
        },
        'routine_procedure_10': {
            'table': (
                ('name', 'Name', 0),
                ('data', 'data', 0),
            ),
        },
        'routine_procedure_11': {
            'table': (
                ('name', 'Name', 0),
                ('data', 'data', 0),
            ),
        },
        'routine_procedure_12': {
            'table': (
                ('name', 'Name', 0),
                ('data', 'data', 0),
            ),
        },
        'routine_procedure_13': {
            'table': (
                ('name', 'Name', 0),
                ('data', 'data', 0),
            ),
        },
        'routine_procedure_14': {
            'table': (
                ('name', 'Name', 0),
                ('data', 'data', 0),
            ),
        },
        'routine_procedure_15': {
            'table': (
                ('name', 'Name', 0),
                ('data', 'data', 0),
            ),
        },
        'routine_procedure_16': {
            'table': (
                ('name', 'Name', 0),
                ('data', 'data', 0),
            ),
        },
        'active_tt_list': {
            'table': (
                ('name', 'Name', 0),
                ('data', 'data', 0),
            ),
        },
        'passive_tt_list': {
            'table': (
                ('name', 'Name', 0),
                ('data', 'data', 0),
            ),
        },
        'obdh_hist_err_cde': {
            'table': (
                ('name', 'Name', 0),
                ('data', 'data', 0),
            ),
        },
        'obdh_nor_flash_data': {
            'table': (
                ('name', 'Name', 0),
                ('data', 'data', 0),
            ),
        },
        'can_listener_data': {
            'table': (
                ('name', 'Name', 0),
                ('data', 'data', 0),
            ),
        },
        'obdh_ram_data': {
            'table': (
                ('name', 'Name', 0),
                ('data', 'data', 0),
            ),
        },
        'adcs_ext_live': {
            'table': (
                ('name', 'Name', 0),
                ('data', 'data', 0),
            ),
        },
        'adcs_sun_sen_profile': {
            'table': (
                ('name', 'Name', 0),
                ('data', 'data', 0),
            ),
        },
        'adcs_sun_sen_ext': {
            'table': (
                ('name', 'Name', 0),
                ('data', 'data', 0),
            ),
        },
        's_band_raw': {
            'table': (
                ('name', 'Name', 0),
                ('data', 'data', 0),
            ),
        },
        'ai_exp_data': {
            'table': (
                ('name', 'Name', 0),
                ('data', 'data', 0),
            ),
        },
        'mview_img_data': {
            'table': (
                ('name', 'Name', 0),
                ('data', 'data', 0),
            ),
        },
        'mview_ext_live': {
            'table': (
                ('name', 'Name', 0),
                ('data', 'data', 0),
            ),
        },
        'gps_raw_data': {
            'table': (
                ('name', 'Name', 0),
                ('data', 'data', 0),
            ),
        },
        'exp_apid_backup_01': {
            'table': (
                ('name', 'Name', 0),
                ('data', 'data', 0),
            ),
        },
        'exp_apid_backup_02': {
            'table': (
                ('name', 'Name', 0),
                ('data', 'data', 0),
            ),
        },
        'exp_apid_backup_03': {
            'table': (
                ('name', 'Name', 0),
                ('data', 'data', 0),
            ),
        },
        'exp_apid_backup_04': {
            'table': (
                ('name', 'Name', 0),
                ('data', 'data', 0),
            ),
        },
        'exp_apid_backup_05': {
            'table': (
                ('name', 'Name', 0),
                ('data', 'data', 0),
            ),
        },
        'exp_apid_backup_06': {
            'table': (
                ('name', 'Name', 0),
                ('data', 'data', 0),
            ),
        },
        'exp_apid_backup_07': {
            'table': (
                ('name', 'Name', 0),
                ('data', 'data', 0),
            ),
        },
        'exp_apid_backup_08': {
            'table': (
                ('name', 'Name', 0),
                ('data', 'data', 0),
            ),
        },
        'exp_apid_backup_09': {
            'table': (
                ('name', 'Name', 0),
                ('data', 'data', 0),
            ),
        },
        'exp_apid_backup_10': {
            'table': (
                ('name', 'Name', 0),
                ('data', 'data', 0),
            ),
        },
    }

    @staticmethod
    def get_sender_callsign(data):
        return ax25.get_sender_callsign(data.header)

    def recognize(self, bb, t=None):
        frame = ccsds.parse_space_packet(bb)
        if not frame:
            return
        cs = self.get_sender_callsign(frame)

        for sp in frame.info.payload.packets:
            s = sonate2_map.get(sp.SPHead.APID)
            if s:
                tlm = s.parse(sp.data)
                tlm.Time = ccsds.get_time_from_sp(sp)
                ty = 'tlm'
                p_data = cs, tlm
            else:
                ty = 'raw'
                p_data = sp.data

            yield ty, cs, '0x%04X' % sp.SPHead.APID, p_data
