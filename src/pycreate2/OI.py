# Walchko: I took some of these ideas from: https://bitbucket.org/lemoneer/irobot

from enum import Enum


class BaudRate(Enum):
    BAUD_300 = 0
    BAUD_600 = 1
    BAUD_1200 = 2
    BAUD_2400 = 3
    BAUD_4800 = 4
    BAUD_9600 = 5
    BAUD_14400 = 6
    BAUD_19200 = 7
    BAUD_28800 = 8
    BAUD_38400 = 9
    BAUD_57600 = 10
    BAUD_115200 = 11
    DEFAULT = 11


class Days(Enum):
    SUNDAY = 0x01
    MONDAY = 0x02
    TUESDAY = 0x04
    WEDNESDAY = 0x08
    THURSDAY = 0x10
    FRIDAY = 0x20
    SATURDAY = 0x40


class DriveDirection(Enum):
    STRAIGHT = 0x8000
    STRAIGHT_ALT = 0x7FFF
    TURN_CW = -1
    TURN_CCW = 0x0001


class Motor(Enum):
    SIDE_BRUSH = 0x01
    VACUUM = 0x02
    MAIN_BRUSH = 0x04
    SIDE_BRUSH_DIRECTION = 0x08
    MAIN_BRUSH_DIRECTION = 0x10


class Leds(Enum):
    DEBRIS = 0x01
    SPOT = 0x02
    DOCK = 0x04
    CHECK_ROBOT = 0x08


# WEEKDAY_LEDS        = Namespace(SUNDAY=0x01, MONDAY=0x02, TUESDAY=0x04, WEDNESDAY=0x08, THURSDAY=0x10, FRIDAY=0x20, SATURDAY=0x40)
WeekdayLeds = Leds


class SchedulingLeds(Enum):
    COLON = 0x01
    PM = 0x02
    AM = 0x04
    CLOCK = 0x08
    SCHEDULE = 0x10


class RawLed(Enum):
    A = 0x01
    B = 0x02
    C = 0x04
    D = 0x08
    E = 0x10
    F = 0x20
    G = 0x40


class Buttons(Enum):
    CLEAN = 0x01
    SPOT = 0x02
    DOCK = 0x04
    MINUTE = 0x08
    HOUR = 0x10
    DAY = 0x20
    SCHEDULE = 0x40
    CLOCK = 0x80


class Robot(Enum):
    TICK_PER_REV = 508.8
    WHEEL_DIAMETER = 72  # mm
    WHEEL_BASE = 235     # mm
    TICK_TO_DISTANCE = 0.44456499814949904317867595046408  # mm per tick


class Modes(Enum):
    OFF = 0
    PASSIVE = 1
    SAFE = 2
    FULL = 3


class WheelOvercurrent(Enum):
    SIDE_BRUSH = 0x01
    MAIN_BRUSH = 0x02
    RIGHT_WHEEL = 0x04
    LEFT_WHEEL = 0x08


class BumpsWheelDrops(Enum):
    BUMP_RIGHT = 0x01
    BUMP_LEFT = 0x02
    WHEEL_DROP_RIGHT = 0x04
    WHEEL_DROP_LEFT = 0x08


class ChargeSource(Enum):
    INTERNAL = 0x01
    HOME_BASE = 0x02


class LightBumper(Enum):
    LEFT = 0x01
    FRONT_LEFT = 0x02
    CENTER_LEFT = 0x04
    CENTER_RIGHT = 0x08
    FRONT_RIGHT = 0x10
    RIGHT = 0x20


class Stasis(Enum):
    TOGGLING = 0x01
    DISABLED = 0x02


class Opcodes(Enum):
    RESET = 7
    OI_MODE = 35
    START = 128
    SAFE = 131
    FULL = 132
    POWER = 133
    DRIVE = 137
    MOTORS = 138
    LED = 139
    SONG = 140
    PLAY = 141
    SENSORS = 142
    SEEK_DOCK = 143
    MOTORS_PWM = 144
    DRIVE_DIRECT = 145
    DRIVE_PWM = 146
    QUERY_LIST = 149
    DIGIT_LED_ASCII = 164
    STOP = 173


RESPONSE_SIZES = {
    0: 26, 1: 10, 2: 6, 3: 10, 4: 14, 5: 12, 6: 52,
    # actual sensors
    7: 1, 8: 1, 9: 1, 10: 1, 11: 1, 12: 1, 13: 1, 14: 1, 15: 1, 16: 1, 17: 1, 18: 1, 19: 2, 20: 2, 21: 1,
    22: 2, 23: 2, 24: 1, 25: 2, 26: 2, 27: 2, 28: 2, 29: 2, 30: 2, 31: 2, 32: 3, 33: 3, 34: 1, 35: 1,
    36: 1, 37: 1, 38: 1, 39: 2, 40: 2, 41: 2, 42: 2, 43: 2, 44: 2, 45: 1, 46: 2, 47: 2, 48: 2, 49: 2,
    50: 2, 51: 2, 52: 1, 53: 1, 54: 2, 55: 2, 56: 2, 57: 2, 58: 1,
    # end actual sensors
    100: 80, 101: 28, 106: 12, 107: 9
}


def calc_query_data_len(pkts):
    packet_size = 0
    for p in pkts:
        packet_size += RESPONSE_SIZES[p]
    return packet_size


class ChargingState(Enum):
    NOT_CHARGING = 0
    RECONDITIONING_CHARGING = 1
    FULL_CHARGING = 2
    TRICKLE_CHARGING = 3
    WAITING = 4
    CHARGING_FAULT_CONDITION = 5


class MidiNote(Enum):
    REST = 0
    PAUSE = 0
    R = 0
    G1 = 31
    GS1 = 32
    A1 = 33
    AS1 = 34
    B1 = 35
    C2 = 36
    CS2 = 37
    D2 = 38
    DS2 = 39
    E2 = 40
    F2 = 41
    FS2 = 42
    G2 = 43
    GS2 = 44
    A2 = 45
    AS2 = 46
    B2 = 47
    C3 = 48
    CS3 = 49
    D3 = 50
    DS3 = 51
    E3 = 52
    F3 = 53
    FS3 = 54
    G3 = 55
    GS3 = 56
    A3 = 57
    AS3 = 58
    B3 = 59
    C4 = 60
    CS4 = 61
    D4 = 62
    DS4 = 63
    E4 = 64
    F4 = 65
    FS4 = 66
    G4 = 67
    GS4 = 68
    A4 = 69
    AS4 = 70
    B4 = 71
    C5 = 72
    CS5 = 73
    D5 = 74
    DS5 = 75
    E5 = 76
    F5 = 77
    FS5 = 78
    G5 = 79
    GS5 = 80
    A5 = 81
    AS5 = 82
    B5 = 83
    C6 = 84
    CS6 = 85
    D6 = 86
    DS6 = 87
    E6 = 88
    F6 = 89
    FS6 = 90
    G6 = 91
    GS6 = 92
    A6 = 93
    AS6 = 94
    B6 = 95
    C7 = 96
    CS7 = 97
    D7 = 98
    DS7 = 99
    E7 = 100
    F7 = 101
    FS7 = 102
    G7 = 103
    GS7 = 104
    A7 = 105
    AS7 = 106
    B7 = 107
    C8 = 108
    CS8 = 109
    D8 = 110
    DS8 = 111
    E8 = 112
    F8 = 113
    FS8 = 114
    G8 = 115
    GS8 = 116
    A8 = 117
    AS8 = 118
    B8 = 119
    C9 = 120
    CS9 = 121
    D9 = 122
    DS9 = 123
    E9 = 124
    F9 = 125
    FS9 = 126
    G9 = 127


class RemoteOpcode(Enum):
    NONE = 0
    LEFT = 129
    FORWARD = 130
    RIGHT = 131
    SPOT = 132
    MAX = 133
    SMALL = 134
    MEDIUM = 135
    CLEAN = 136
    PAUSE = 137
    POWER = 138
    ARC_LEFT = 139
    ARC_RIGHT = 140
    DRIVE_STOP = 141
    SEND_ALL = 142
    SEEK_DOCK = 143
    RESERVED_160 = 160
    FORCE_FIELD_161 = 161
    VIRTUAL_WALL = 162
    GREEN_BUOY = 164
    GREEN_BUOY_AND_FORCE_FIELD_165 = 165
    RED_BUOY = 168
    RED_BUOY_AND_FORCE_FIELD_169 = 169
    RED_BUOY_AND_GREEN_BUOY = 172
    RED_BUOY_AND_GREEN_BUOY_AND_FORCE_FIELD_173 = 173
    RESERVED_240 = 240
    FORCE_FIELD_242 = 242
    GREEN_BUOY_244 = 244
    GREEN_BUOY_AND_FORCE_FIELD_246 = 246
    RED_BUOY_248 = 248
    RED_BUOY_AND_FORCE_FIELD_250 = 250
    RED_BUOY_AND_GREEN_BUOY_252 = 252
    RED_BUOY_AND_GREEN_BUOY_AND_FORCE_FIELD_254 = 254
    NONE_255 = 255
