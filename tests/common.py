import pytest
import logging
import sys
from pycreate2.createSerial import SerialCommandInterface
from dataclasses import dataclass
from threading import Thread, Lock
import time

@dataclass
class RespondWith:
    data: bytes
    wait: float = 0.0

class DummySerial:
    def __init__(self):
        self.buffer: bytearray = bytearray()
        self.port = "/dev/ttyUSB0"
        self.baudrate = 115200
        self.responses: list[RespondWith] = []
        self.buffer_lock = Lock()

    def close(self):
        ...

    @property
    def is_open(self):
        return True

    @property
    def in_waiting(self):
        return len(self.buffer)

    def add_response(self, data: bytes, wait: float = 0.0):
        self.responses.append(RespondWith(data, wait))

    def read(self, num_bytes: int) -> bytes:
        with self.buffer_lock:
            to_return, self.buffer = self.buffer[:num_bytes], self.buffer[num_bytes:]

        if len(to_return) < num_bytes:
            time.sleep(1) # simulate waiting for more data
        return to_return

    def reset_output_buffer(self):
        pass

    def reset_input_buffer(self):
        with self.buffer_lock:
            self.buffer.clear()

    def _respond(self, response: RespondWith):
        if response.wait > 0:
            time.sleep(response.wait)
        print("DummySerial responding with:", response.data)
        with self.buffer_lock:
            self.buffer += response.data

    def write(self, data: bytes):
        # If there are responses queued, respond with them
        if self.responses:
            response = self.responses.pop(0)
            thread = Thread(target=self._respond, args=(response,))
            thread.start()

    def waiting(self):
        return len(self.buffer)

    def flush(self):
        with self.buffer_lock:
            self.buffer.clear()

@pytest.fixture(scope="session", autouse=True)
def logging_setup():
    # To stderr
    logging.basicConfig(
        level=logging.WARNING,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[logging.StreamHandler(sys.stderr)],
    )
    yield

@pytest.fixture
def dummy_interface(logging_setup) -> SerialCommandInterface:
    interface = SerialCommandInterface()
    dummy_serial = DummySerial()
    interface.ser = dummy_serial  # type: ignore
    return interface
