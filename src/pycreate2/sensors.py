from dataclasses import dataclass
import sys
import struct
import pycreate2.logger
import logging

logger = logging.getLogger("create2sensors")


@dataclass
class Sensor:
    id: int
    size: int
    value_range: tuple[int, int]
    name: str
    membership: list[int]

    def clamp(self, value: int) -> int:
        """Clamp value to valid range for this sensor packet."""
        return max(self.value_range[0], min(self.value_range[1], value))

    def pack_format(self) -> str:
        # Check if its unsigned or signed
        signed = self.value_range[0] < 0

        # Check its size
        is_word = self.size == 2

        match (signed, is_word):
            case (False, False):
                return 'B'  # unsigned byte
            case (False, True):
                return '>H'  # unsigned word
            case (True, False):
                return 'b'  # signed byte
            case (True, True):
                return '>h'  # signed word

        # If we somehow didn't match any case, fall back to unsigned byte
        logger.warning(f"Could not determine pack format of packet {self.id}")
        return 'B'

    def pack(self, value: int) -> bytes:
        """Return packed bytes for this sensor packet with the given value."""
        fmt = self.pack_format()
        return struct.pack(fmt, self.clamp(value))

    def unpack(self, data: bytes) -> int:
        """Return unpacked value from bytes for this sensor packet."""
        if len(data) != self.size:
            logger.error(
                f"Data length {len(data)} does not match expected size {self.size} for sensor {self.name} (ID {self.id})"
            )
            raise ValueError("Invalid data length for unpacking sensor packet")
        fmt = self.pack_format()
        unpacked = struct.unpack(fmt, data)[0]

        if (not (self.value_range[0] <= unpacked <= self.value_range[1])):
            logger.warning(
                f"Unpacked value {unpacked} out of range {self.value_range}")

        return unpacked


class SensorNames:
    BUMPS_WHEELDROPS = "Bumps Wheeldrops"
    WALL = "Wall"
    CLIFF_LEFT = "Cliff Left"
    CLIFF_FRONT_LEFT = "Cliff Front Left"
    CLIFF_FRONT_RIGHT = "Cliff Front Right"
    CLIFF_RIGHT = "Cliff Right"
    VIRTUAL_WALL = "Virtual Wall"
    OVERCURRENTS = "Overcurrents"
    DIRT_DETECT = "Dirt Detect"
    UNUSED_1 = "Unused 1"
    IR_OPCODE = "IR Opcode"
    BUTTONS = "Buttons"
    DISTANCE = "Distance"
    ANGLE = "Angle"
    CHARGING_STATE = "Charging State"
    VOLTAGE = "Voltage"
    CURRENT = "Current"
    TEMPERATURE = "Temperature"
    BATTERY_CHARGE = "Battery Charge"
    BATTERY_CAPACITY = "Battery Capacity"
    WALL_SIGNAL = "Wall Signal"
    CLIFF_LEFT_SIGNAL = "Cliff Left Signal"
    CLIFF_FRONT_LEFT_SIGNAL = "Cliff Front Left Signal"
    CLIFF_FRONT_RIGHT_SIGNAL = "Cliff Front Right Signal"
    CLIFF_RIGHT_SIGNAL = "Cliff Right Signal"
    UNUSED_2 = "Unused 2"
    UNUSED_3 = "Unused 3"
    CHARGER_AVAILABLE = "Charger Available"
    OPEN_INTERFACE_MODE = "Open Interface Mode"
    SONG_NUMBER = "Song Number"
    SONG_PLAYING = "Song Playing?"
    OI_STREAM_NUM_PACKETS = "Oi Stream Num Packets"
    VELOCITY = "Velocity"
    REQUESTED_RADIUS = "Requested Radius"
    REQUESTED_VELOCITY_RIGHT = "Requested Velocity Right"
    REQUESTED_VELOCITY_LEFT = "Requested Velocity Left"
    ENCODER_COUNTS_LEFT = "Encoder Counts Left"
    ENCODER_COUNTS_RIGHT = "Encoder Counts Right"
    LIGHT_BUMPER = "Light Bumper"
    LIGHT_BUMP_LEFT = "Light Bump Left"
    LIGHT_BUMP_FRONT_LEFT = "Light Bump Front Left"
    LIGHT_BUMP_CENTER_LEFT = "Light Bump Center Left"
    LIGHT_BUMP_CENTER_RIGHT = "Light Bump Center Right"
    LIGHT_BUMP_FRONT_RIGHT = "Light Bump Front Right"
    LIGHT_BUMP_RIGHT = "Light Bump Right"
    IR_OPCODE_LEFT = "IR Opcode Left"
    IR_OPCODE_RIGHT = "IR Opcode Right"
    LEFT_MOTOR_CURRENT = "Left Motor Current"
    RIGHT_MOTOR_CURRENT = "Right Motor Current"
    MAIN_BRUSH_CURRENT = "Main Brush Current"
    SIDE_BRUSH_CURRENT = "Side Brush Current"
    STASIS = "Stasis"


SENSORS = {
    # Block 0, 1, 6, 100 begin
    SensorNames.BUMPS_WHEELDROPS: Sensor(7, 1, (0, 15), SensorNames.BUMPS_WHEELDROPS, [0, 1, 6, 100]),
    SensorNames.WALL: Sensor(8, 1, (0, 1), SensorNames.WALL, [0, 1, 6, 100]),
    SensorNames.CLIFF_LEFT: Sensor(9, 1, (0, 1), SensorNames.CLIFF_LEFT, [0, 1, 6, 100]),
    SensorNames.CLIFF_FRONT_LEFT: Sensor(10, 1, (0, 1), SensorNames.CLIFF_FRONT_LEFT, [0, 1, 6, 100]),
    SensorNames.CLIFF_FRONT_RIGHT: Sensor(11, 1, (0, 1), SensorNames.CLIFF_FRONT_RIGHT, [0, 1, 6, 100]),
    SensorNames.CLIFF_RIGHT: Sensor(12, 1, (0, 1), SensorNames.CLIFF_RIGHT, [0, 1, 6, 100]),
    SensorNames.VIRTUAL_WALL: Sensor(13, 1, (0, 1), SensorNames.VIRTUAL_WALL, [0, 1, 6, 100]),
    SensorNames.OVERCURRENTS: Sensor(14, 1, (0, 29), SensorNames.OVERCURRENTS, [0, 1, 6, 100]),
    SensorNames.DIRT_DETECT: Sensor(15, 1, (0, 255), SensorNames.DIRT_DETECT, [0, 1, 6, 100]),
    SensorNames.UNUSED_1: Sensor(16, 1, (0, 255), SensorNames.UNUSED_1, [0, 1, 6, 100]),
    # Block 1 end
    # Block 2 begin
    SensorNames.IR_OPCODE: Sensor(17, 1, (0, 255), SensorNames.IR_OPCODE, [0, 2, 6, 100]),
    SensorNames.BUTTONS: Sensor(18, 1, (0, 255), SensorNames.BUTTONS, [0, 2, 6, 100]),
    SensorNames.DISTANCE: Sensor(19, 2, (-32768, 32767), SensorNames.DISTANCE, [0, 2, 6, 100]),
    SensorNames.ANGLE: Sensor(20, 2, (-32768, 32767), SensorNames.ANGLE, [0, 2, 6, 100]),
    # Block 2 end
    # Block 3 begin
    SensorNames.CHARGING_STATE: Sensor(21, 1, (0, 6), SensorNames.CHARGING_STATE, [0, 3, 6, 100]),
    SensorNames.VOLTAGE: Sensor(22, 2, (0, 65535), SensorNames.VOLTAGE, [0, 3, 6, 100]),
    SensorNames.CURRENT: Sensor(23, 2, (-32768, 32767), SensorNames.CURRENT, [0, 3, 6, 100]),
    SensorNames.TEMPERATURE: Sensor(24, 1, (-128, 127), SensorNames.TEMPERATURE, [0, 3, 6, 100]),
    SensorNames.BATTERY_CHARGE: Sensor(25, 2, (0, 65535), SensorNames.BATTERY_CHARGE, [0, 3, 6, 100]),
    SensorNames.BATTERY_CAPACITY: Sensor(26, 2, (0, 65535), SensorNames.BATTERY_CAPACITY, [0, 3, 6, 100]),
    # Block 0, 3 end
    # Block 4 begin
    SensorNames.WALL_SIGNAL: Sensor(27, 2, (0, 1023), SensorNames.WALL_SIGNAL, [4, 6, 100]),
    SensorNames.CLIFF_LEFT_SIGNAL: Sensor(28, 2, (0, 4095), SensorNames.CLIFF_LEFT_SIGNAL, [4, 6, 100]),
    SensorNames.CLIFF_FRONT_LEFT_SIGNAL: Sensor(29, 2, (0, 4095), SensorNames.CLIFF_FRONT_LEFT_SIGNAL, [4, 6, 100]),
    SensorNames.CLIFF_FRONT_RIGHT_SIGNAL: Sensor(30, 2, (0, 4095), SensorNames.CLIFF_FRONT_RIGHT_SIGNAL, [4, 6, 100]),
    SensorNames.CLIFF_RIGHT_SIGNAL: Sensor(31, 2, (0, 4095), SensorNames.CLIFF_RIGHT_SIGNAL, [4, 6, 100]),
    SensorNames.UNUSED_2: Sensor(32, 1, (0, 255), SensorNames.UNUSED_2, [4, 6, 100]),
    SensorNames.UNUSED_3: Sensor(33, 2, (0, 65535), SensorNames.UNUSED_3, [4, 6, 100]),
    SensorNames.CHARGER_AVAILABLE: Sensor(34, 1, (0, 3), SensorNames.CHARGER_AVAILABLE, [4, 6, 100]),
    # Block 4 end
    # Block 5 begin
    SensorNames.OPEN_INTERFACE_MODE: Sensor(35, 1, (0, 3), SensorNames.OPEN_INTERFACE_MODE, [5, 6, 100]),
    SensorNames.SONG_NUMBER: Sensor(36, 1, (0, 4), SensorNames.SONG_NUMBER, [5, 6, 100]),
    SensorNames.SONG_PLAYING: Sensor(37, 1, (0, 1), SensorNames.SONG_PLAYING, [5, 6, 100]),
    SensorNames.OI_STREAM_NUM_PACKETS: Sensor(38, 1, (0, 108), SensorNames.OI_STREAM_NUM_PACKETS, [5, 6, 100]),
    SensorNames.VELOCITY: Sensor(39, 2, (-500, 500), SensorNames.VELOCITY, [5, 6, 100]),
    SensorNames.REQUESTED_RADIUS: Sensor(40, 2, (-32768, 32767), SensorNames.REQUESTED_RADIUS, [5, 6, 100]),
    SensorNames.REQUESTED_VELOCITY_RIGHT: Sensor(41, 2, (-500, 500), SensorNames.REQUESTED_VELOCITY_RIGHT, [5, 6, 100]),
    SensorNames.REQUESTED_VELOCITY_LEFT: Sensor(42, 2, (-500, 500), SensorNames.REQUESTED_VELOCITY_LEFT, [5, 6, 100]),
    # Block 5, 6 end
    # Block 101 begin
    SensorNames.ENCODER_COUNTS_LEFT: Sensor(43, 2, (-32768, 32767), SensorNames.ENCODER_COUNTS_LEFT, [100, 101]),
    SensorNames.ENCODER_COUNTS_RIGHT: Sensor(44, 2, (-32768, 32767), SensorNames.ENCODER_COUNTS_RIGHT, [100, 101]),
    SensorNames.LIGHT_BUMPER: Sensor(45, 1, (0, 127), SensorNames.LIGHT_BUMPER, [100, 101]),
    # Block 106 begin
    SensorNames.LIGHT_BUMP_LEFT: Sensor(46, 2, (0, 4095), SensorNames.LIGHT_BUMP_LEFT, [100, 101, 106]),
    SensorNames.LIGHT_BUMP_FRONT_LEFT: Sensor(47, 2, (0, 4095), SensorNames.LIGHT_BUMP_FRONT_LEFT, [100, 101, 106]),
    SensorNames.LIGHT_BUMP_CENTER_LEFT: Sensor(48, 2, (0, 4095), SensorNames.LIGHT_BUMP_CENTER_LEFT, [100, 101, 106]),
    SensorNames.LIGHT_BUMP_CENTER_RIGHT: Sensor(49, 2, (0, 4095), SensorNames.LIGHT_BUMP_CENTER_RIGHT, [100, 101, 106]),
    SensorNames.LIGHT_BUMP_FRONT_RIGHT: Sensor(50, 2, (0, 4095), SensorNames.LIGHT_BUMP_FRONT_RIGHT, [100, 101, 106]),
    SensorNames.LIGHT_BUMP_RIGHT: Sensor(51, 2, (0, 4095), SensorNames.LIGHT_BUMP_RIGHT, [100, 101, 106]),
    # Block 106 end
    SensorNames.IR_OPCODE_LEFT: Sensor(52, 1, (0, 255), SensorNames.IR_OPCODE_LEFT, [100, 101]),
    SensorNames.IR_OPCODE_RIGHT: Sensor(53, 1, (0, 255), SensorNames.IR_OPCODE_RIGHT, [100, 101]),
    # Block 107 begin
    SensorNames.LEFT_MOTOR_CURRENT: Sensor(54, 2, (-32768, 32767), SensorNames.LEFT_MOTOR_CURRENT, [100, 101, 107]),
    SensorNames.RIGHT_MOTOR_CURRENT: Sensor(55, 2, (-32768, 32767), SensorNames.RIGHT_MOTOR_CURRENT, [100, 101, 107]),
    SensorNames.MAIN_BRUSH_CURRENT: Sensor(56, 2, (-32768, 32767), SensorNames.MAIN_BRUSH_CURRENT, [100, 101, 107]),
    SensorNames.SIDE_BRUSH_CURRENT: Sensor(57, 2, (-32768, 32767), SensorNames.SIDE_BRUSH_CURRENT, [100, 101, 107]),
    SensorNames.STASIS: Sensor(58, 1, (0, 3), SensorNames.STASIS, [100, 101, 107]),
}


def get_sensor_by_id(id: int) -> Sensor | None:
    """Return the SensorPacket with the given id, or None if not found."""
    for pkt in SENSORS.values():
        if pkt.id == id:
            return pkt
    return None


def get_sensor_by_name(name: str) -> Sensor | None:
    """Return the SensorPacket with the given name, or None if not found."""
    return SENSORS.get(name, None)


def get_sensor_block(id: int) -> list[Sensor]:
    """Return a list of SensorPackets that belong to the given block id."""
    block_sensors = []
    for pkt in SENSORS.values():
        if id in pkt.membership:
            block_sensors.append(pkt)
    block_sensors.sort(key=lambda s: s.id)
    return block_sensors
