import pycreate2.sensors as sensors
import random
from common import logging_setup, DummySerial, dummy_interface
from pycreate2.create2api import Create2


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

def test_read_sensors(logging_setup, dummy_interface):
    create2 = Create2(sci=dummy_interface) # type: ignore
    ser: DummySerial = dummy_interface.ser  # type: ignore
    ser.add_response(b'\x01', wait=0.1)
    sensor_list = ["Charger Available"]
    result = create2.get_sensor_list(sensor_list)
    assert result == {'Charger Available': 1}

def test_read_sensors_no_data_first(logging_setup, dummy_interface):
    create2 = Create2(sci=dummy_interface) # type: ignore
    ser: DummySerial = dummy_interface.ser  # type: ignore
    ser.add_response(b'', wait=0.1)
    ser.add_response(b'\x01', wait=0.1)
    sensor_list = ["Charger Available"]
    result = create2.get_sensor_list(sensor_list)
    assert result == {'Charger Available': 1}

def test_read_sensors_out_range_first(logging_setup, dummy_interface):
    create2 = Create2(sci=dummy_interface) # type: ignore
    ser: DummySerial = dummy_interface.ser  # type: ignore
    ser.add_response(b'\xFF', wait=0.1)
    ser.add_response(b'\x01', wait=0.1)
    sensor_list = ["Charger Available"]
    result = create2.get_sensor_list(sensor_list)
    assert result == {'Charger Available': 1}

