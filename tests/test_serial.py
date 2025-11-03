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
        return self.buffer[:num_bytes]

    def write(self, data: bytes):
        ...


@pytest.fixture
def dummy_interface(logging_setup) -> SerialCommandInterface:
    interface = SerialCommandInterface()
    dummy_serial = DummySerial()
    interface.ser = dummy_serial  # type: ignore
    return interface


def test_filter_long(dummy_interface: SerialCommandInterface):
    dummy_interface.ser.buffer = bytearray(
        b"    Flash CRC successful 0x0 (0x0)\n\rHello")
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
