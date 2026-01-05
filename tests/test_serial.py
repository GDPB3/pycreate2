import pytest
from pycreate2.createSerial import SerialCommandInterface
from common import logging_setup, DummySerial, dummy_interface
from threading import Thread
import time


FLASH_CRC_MSG = b"    Flash CRC successful: 0x0 (0x0)\n\r"

def test_read_later(dummy_interface: SerialCommandInterface):
    def target(delay):
        time.sleep(delay)
        dummy_interface.ser.buffer = bytearray(b"Hello")

    thread = Thread(target=target, args=(0.1,))
    thread.start()
    data = dummy_interface.read(5)
    assert data == b"Hello"

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
