from dataclasses import dataclass
import sys
import struct
import pycreate2.logger
import logging

logger = logging.getLogger("create2sensors")

@dataclass
class SensorPacket:
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
        assert len(
            data) == self.size, f"Data length {len(data)} does not match expected size {self.size}"
        fmt = self.pack_format()
        unpacked = struct.unpack(fmt, data)[0]

        if (not (self.value_range[0] <= unpacked <= self.value_range[1])):
            logger.warning(f"Unpacked value {unpacked} out of range {self.value_range}")

        return unpacked


class PacketNames:
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
    RADIUS = "Radius"
    VELOCITY_RIGHT = "Velocity Right"
    VELOCITY_LEFT = "Velocity Left"
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


PACKETS = {
    # Block 0, 1, 6, 100 begin
    PacketNames.BUMPS_WHEELDROPS: SensorPacket(7, 1, (0, 15), PacketNames.BUMPS_WHEELDROPS, [0, 1, 6, 100]),
    PacketNames.WALL: SensorPacket(8, 1, (0, 1), PacketNames.WALL, [0, 1, 6, 100]),
    PacketNames.CLIFF_LEFT: SensorPacket(9, 1, (0, 1), PacketNames.CLIFF_LEFT, [0, 1, 6, 100]),
    PacketNames.CLIFF_FRONT_LEFT: SensorPacket(10, 1, (0, 1), PacketNames.CLIFF_FRONT_LEFT, [0, 1, 6, 100]),
    PacketNames.CLIFF_FRONT_RIGHT: SensorPacket(11, 1, (0, 1), PacketNames.CLIFF_FRONT_RIGHT, [0, 1, 6, 100]),
    PacketNames.CLIFF_RIGHT: SensorPacket(12, 1, (0, 1), PacketNames.CLIFF_RIGHT, [0, 1, 6, 100]),
    PacketNames.VIRTUAL_WALL: SensorPacket(13, 1, (0, 1), PacketNames.VIRTUAL_WALL, [0, 1, 6, 100]),
    PacketNames.OVERCURRENTS: SensorPacket(14, 1, (0, 29), PacketNames.OVERCURRENTS, [0, 1, 6, 100]),
    PacketNames.DIRT_DETECT: SensorPacket(15, 1, (0, 255), PacketNames.DIRT_DETECT, [0, 1, 6, 100]),
    PacketNames.UNUSED_1: SensorPacket(16, 1, (0, 255), PacketNames.UNUSED_1, [0, 1, 6, 100]),
    # Block 1 end
    # Block 2 begin
    PacketNames.IR_OPCODE: SensorPacket(17, 1, (0, 255), PacketNames.IR_OPCODE, [0, 2, 6, 100]),
    PacketNames.BUTTONS: SensorPacket(18, 1, (0, 255), PacketNames.BUTTONS, [0, 2, 6, 100]),
    PacketNames.DISTANCE: SensorPacket(19, 2, (-32768, 32767), PacketNames.DISTANCE, [0, 2, 6, 100]),
    PacketNames.ANGLE: SensorPacket(20, 2, (-32768, 32767), PacketNames.ANGLE, [0, 2, 6, 100]),
    # Block 2 end
    # Block 3 begin
    PacketNames.CHARGING_STATE: SensorPacket(21, 1, (0, 6), PacketNames.CHARGING_STATE, [0, 3, 6, 100]),
    PacketNames.VOLTAGE: SensorPacket(22, 2, (0, 65535), PacketNames.VOLTAGE, [0, 3, 6, 100]),
    PacketNames.CURRENT: SensorPacket(23, 2, (-32768, 32767), PacketNames.CURRENT, [0, 3, 6, 100]),
    PacketNames.TEMPERATURE: SensorPacket(24, 1, (-128, 127), PacketNames.TEMPERATURE, [0, 3, 6, 100]),
    PacketNames.BATTERY_CHARGE: SensorPacket(25, 2, (0, 65535), PacketNames.BATTERY_CHARGE, [0, 3, 6, 100]),
    PacketNames.BATTERY_CAPACITY: SensorPacket(26, 2, (0, 65535), PacketNames.BATTERY_CAPACITY, [0, 3, 6, 100]),
    # Block 0, 3 end
    # Block 4 begin
    PacketNames.WALL_SIGNAL: SensorPacket(27, 2, (0, 1023), PacketNames.WALL_SIGNAL, [4, 6, 100]),
    PacketNames.CLIFF_LEFT_SIGNAL: SensorPacket(28, 2, (0, 4095), PacketNames.CLIFF_LEFT_SIGNAL, [4, 6, 100]),
    PacketNames.CLIFF_FRONT_LEFT_SIGNAL: SensorPacket(29, 2, (0, 4095), PacketNames.CLIFF_FRONT_LEFT_SIGNAL, [4, 6, 100]),
    PacketNames.CLIFF_FRONT_RIGHT_SIGNAL: SensorPacket(30, 2, (0, 4095), PacketNames.CLIFF_FRONT_RIGHT_SIGNAL, [4, 6, 100]),
    PacketNames.CLIFF_RIGHT_SIGNAL: SensorPacket(31, 2, (0, 4095), PacketNames.CLIFF_RIGHT_SIGNAL, [4, 6, 100]),
    PacketNames.UNUSED_2: SensorPacket(32, 1, (0, 255), PacketNames.UNUSED_2, [4, 6, 100]),
    PacketNames.UNUSED_3: SensorPacket(33, 2, (0, 65535), PacketNames.UNUSED_3, [4, 6, 100]),
    PacketNames.CHARGER_AVAILABLE: SensorPacket(34, 1, (0, 3), PacketNames.CHARGER_AVAILABLE, [4, 6, 100]),
    # Block 4 end
    # Block 5 begin
    PacketNames.OPEN_INTERFACE_MODE: SensorPacket(35, 1, (0, 3), PacketNames.OPEN_INTERFACE_MODE, [5, 6, 100]),
    PacketNames.SONG_NUMBER: SensorPacket(36, 1, (0, 4), PacketNames.SONG_NUMBER, [5, 6, 100]),
    PacketNames.SONG_PLAYING: SensorPacket(37, 1, (0, 1), PacketNames.SONG_PLAYING, [5, 6, 100]),
    PacketNames.OI_STREAM_NUM_PACKETS: SensorPacket(38, 1, (0, 108), PacketNames.OI_STREAM_NUM_PACKETS, [5, 6, 100]),
    PacketNames.VELOCITY: SensorPacket(39, 2, (-500, 500), PacketNames.VELOCITY, [5, 6, 100]),
    PacketNames.RADIUS: SensorPacket(40, 2, (-32768, 32767), PacketNames.RADIUS, [5, 6, 100]),
    PacketNames.VELOCITY_RIGHT: SensorPacket(41, 2, (-500, 500), PacketNames.VELOCITY_RIGHT, [5, 6, 100]),
    PacketNames.VELOCITY_LEFT: SensorPacket(42, 2, (-500, 500), PacketNames.VELOCITY_LEFT, [5, 6, 100]),
    # Block 5, 6 end
    # Block 101 begin
    PacketNames.ENCODER_COUNTS_LEFT: SensorPacket(43, 2, (-32768, 32767), PacketNames.ENCODER_COUNTS_LEFT, [100, 101]),
    PacketNames.ENCODER_COUNTS_RIGHT: SensorPacket(44, 2, (-32768, 32767), PacketNames.ENCODER_COUNTS_RIGHT, [100, 101]),
    PacketNames.LIGHT_BUMPER: SensorPacket(45, 1, (0, 127), PacketNames.LIGHT_BUMPER, [100, 101]),
    # Block 106 begin
    PacketNames.LIGHT_BUMP_LEFT: SensorPacket(46, 2, (0, 4095), PacketNames.LIGHT_BUMP_LEFT, [100, 101, 106]),
    PacketNames.LIGHT_BUMP_FRONT_LEFT: SensorPacket(47, 2, (0, 4095), PacketNames.LIGHT_BUMP_FRONT_LEFT, [100, 101, 106]),
    PacketNames.LIGHT_BUMP_CENTER_LEFT: SensorPacket(48, 2, (0, 4095), PacketNames.LIGHT_BUMP_CENTER_LEFT, [100, 101, 106]),
    PacketNames.LIGHT_BUMP_CENTER_RIGHT: SensorPacket(49, 2, (0, 4095), PacketNames.LIGHT_BUMP_CENTER_RIGHT, [100, 101, 106]),
    PacketNames.LIGHT_BUMP_FRONT_RIGHT: SensorPacket(50, 2, (0, 4095), PacketNames.LIGHT_BUMP_FRONT_RIGHT, [100, 101, 106]),
    PacketNames.LIGHT_BUMP_RIGHT: SensorPacket(51, 2, (0, 4095), PacketNames.LIGHT_BUMP_RIGHT, [100, 101, 106]),
    # Block 106 end
    PacketNames.IR_OPCODE_LEFT: SensorPacket(52, 1, (0, 255), PacketNames.IR_OPCODE_LEFT, [100, 101]),
    PacketNames.IR_OPCODE_RIGHT: SensorPacket(53, 1, (0, 255), PacketNames.IR_OPCODE_RIGHT, [100, 101]),
    # Block 107 begin
    PacketNames.LEFT_MOTOR_CURRENT: SensorPacket(54, 2, (-32768, 32767), PacketNames.LEFT_MOTOR_CURRENT, [100, 101, 107]),
    PacketNames.RIGHT_MOTOR_CURRENT: SensorPacket(55, 2, (-32768, 32767), PacketNames.RIGHT_MOTOR_CURRENT, [100, 101, 107]),
    PacketNames.MAIN_BRUSH_CURRENT: SensorPacket(56, 2, (-32768, 32767), PacketNames.MAIN_BRUSH_CURRENT, [100, 101, 107]),
    PacketNames.SIDE_BRUSH_CURRENT: SensorPacket(57, 2, (-32768, 32767), PacketNames.SIDE_BRUSH_CURRENT, [100, 101, 107]),
    PacketNames.STASIS: SensorPacket(58, 1, (0, 3), PacketNames.STASIS, [100, 101, 107]),
}


def get_packet_by_id(id: int) -> SensorPacket | None:
    """Return the SensorPacket with the given id, or None if not found."""
    for pkt in PACKETS.values():
        if pkt.id == id:
            return pkt
    return None


def get_packet_by_name(name: str) -> SensorPacket | None:
    """Return the SensorPacket with the given name, or None if not found."""
    return PACKETS.get(name, None)


if __name__ == "__main__":
    # simple test
    pkt = PACKETS["Encoder Counts Left"]
    assert pkt is not None

    print(pkt.unpack(b'\x01\x02'))  # should be 258
    print(pkt.pack(258))            # should be b'\x01\x02'
    print(pkt.pack(-40000))         # should be b'\x9c\x00' (clamped)
    pkt.unpack(b'\x80\x00\x00')     # should raise an assertion
