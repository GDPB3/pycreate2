import pycreate2.sensors as sensors
import random
from common import logging_setup


def test_unpack_on_range(logging_setup):
    pkt = sensors.SENSORS["Encoder Counts Left"]
    assert pkt is not None

    assert pkt.unpack(b'\x01\x02') == 258


def test_pack_unpack(logging_setup):
    pkt = sensors.SENSORS["Distance"]
    assert pkt is not None

    random.seed(42)
    value = random.randint(pkt.value_range[0], pkt.value_range[1])
    assert pkt.unpack(pkt.pack(value)) == value


def test_pack_out_unpack_in(logging_setup):
    pkt = sensors.SENSORS["Encoder Counts Left"]
    assert pkt is not None

    max_value = pkt.value_range[1]
    assert pkt.unpack(pkt.pack(max_value + 1)) == max_value
