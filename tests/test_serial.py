import pytest
from pycreate2.createSerial import SerialCommandInterface
from common import logging_setup


class DummySerial:
    def __init__(self):
        self.buffer: bytearray = bytearray()
        self.port = "/dev/ttyUSB0"
        self.baudrate = 115200

    def close(self):
        ...

    @property
    def is_open(self):
        return True

    @property
    def in_waiting(self):
        return len(self.buffer)

    def read(self, num_bytes: int) -> bytes:
        to_return, self.buffer = self.buffer[:num_bytes], self.buffer[num_bytes:]
        return to_return

    def write(self, data: bytes):
        ...


@pytest.fixture
def dummy_interface(logging_setup) -> SerialCommandInterface:
    interface = SerialCommandInterface()
    dummy_serial = DummySerial()
    interface.ser = dummy_serial  # type: ignore
    return interface

FLASH_CRC_MSG = b"    Flash CRC successful: 0x0 (0x0)\n\r"

def test_filter_long(dummy_interface: SerialCommandInterface):
    dummy_interface.ser.buffer = bytearray(
        FLASH_CRC_MSG + b"Hello")
    data = dummy_interface.read(5)
    assert data == b"Hello"

def test_filter_long_long(dummy_interface: SerialCommandInterface):
    dummy_interface.ser.buffer = bytearray(
        FLASH_CRC_MSG + FLASH_CRC_MSG + FLASH_CRC_MSG + b"Hello")
    data = dummy_interface.read(5)
    assert data == b"Hello"

def test_filter_in_middle(dummy_interface: SerialCommandInterface):
    dummy_interface.ser.buffer = bytearray(
        FLASH_CRC_MSG + b"Hello" + FLASH_CRC_MSG + FLASH_CRC_MSG)
    data = dummy_interface.read(5)
    assert data == b"Hello"

def test_read_exact(dummy_interface: SerialCommandInterface):
    dummy_interface.ser.buffer = bytearray(b"Hello, World!")
    data = dummy_interface.read(13)
    assert data == b"Hello, World!"


def test_read_less(dummy_interface: SerialCommandInterface):
    dummy_interface.ser.buffer = bytearray(b"Hello, World!")
    data = dummy_interface.read(5)
    assert data == b"Hello"
