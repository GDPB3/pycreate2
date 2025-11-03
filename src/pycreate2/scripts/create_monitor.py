#!/usr/bin/env python3
import argparse
import pycreate2
import time
from pycreate2.sensors import SensorNames

DESCRIPTION = """
Prints the raw data from a Create 2. The default packet is 100 which get everything.
However, this can be changed and a different packet and refresh rates can be selected.
"""


def handleArgs():
    parser = argparse.ArgumentParser(
        description=DESCRIPTION, formatter_class=argparse.RawTextHelpFormatter)
    # parser.add_argument('-m', '--max', help='max id', type=int, default=253)
    parser.add_argument(
        '-s', '--sleep', help='time in seconds between samples, default 1.0', type=float, default=1.0)
    # parser.add_argument('-i', '--id', help='packet ID, default is 100', type=int, default=100)
    parser.add_argument(
        'port', help='serial port name, Ex: /dev/ttyUSB0 or COM1', type=str)

    args = vars(parser.parse_args())
    return args


class Monitor(object):
    def __init__(self):
        pass

    def display_formated(self, sensors: dict[str, int]):
        print('================================================')
        print('Sensors from left to right')
        print('------------------------------------------------')

        ir_left, ir_right = sensors[SensorNames.IR_OPCODE_LEFT], sensors[SensorNames.IR_OPCODE_RIGHT]
        print(f'  IR: {ir_left} {ir_right}')

        bl, bfl, bcl, bcr, bfr, br = (
            sensors[SensorNames.LIGHT_BUMP_LEFT],
            sensors[SensorNames.LIGHT_BUMP_FRONT_LEFT],
            sensors[SensorNames.LIGHT_BUMP_CENTER_LEFT],
            sensors[SensorNames.LIGHT_BUMP_CENTER_RIGHT],
            sensors[SensorNames.LIGHT_BUMP_FRONT_RIGHT],
            sensors[SensorNames.LIGHT_BUMP_RIGHT],
        )
        print(f'  Bump: {bl} {bfl} {bcl} {bcr} {bfr} {br}')

        cl, cfl, cfr, cr = (
            sensors[SensorNames.CLIFF_LEFT],
            sensors[SensorNames.CLIFF_FRONT_LEFT],
            sensors[SensorNames.CLIFF_FRONT_RIGHT],
            sensors[SensorNames.CLIFF_RIGHT],
        )
        print(f'  Cliff: {cl} {cfl} {cfr} {cr}')

        bumps_wheeldrops = sensors[SensorNames.BUMPS_WHEELDROPS]
        wheel_drop_left = (bumps_wheeldrops & 0b00001000) != 0
        wheel_drop_right = (bumps_wheeldrops & 0b00000100) != 0
        print(f'  Wheel drops: {wheel_drop_left} {wheel_drop_right}')

        el, er = sensors[SensorNames.ENCODER_COUNTS_LEFT], sensors[SensorNames.ENCODER_COUNTS_RIGHT]
        print(f'  Encoder: {el} {er}')

        temp_c = sensors[SensorNames.TEMPERATURE]
        temp_f = temp_c * 9.0 / 5.0 + 32
        print(f'  Temperature: {temp_c} C / {temp_f} F')

        overcurrent = sensors[SensorNames.OVERCURRENTS]
        over_left = (overcurrent & 0b00010000) != 0
        over_right = (overcurrent & 0b00001000) != 0
        print(f'  Wheel Overcurrents: {over_left} {over_right}')
        print('------------------------------------------------')
        print('Electrical:')
        print('------------------------------------------------')

        voltage = sensors[SensorNames.VOLTAGE] / 1000.0
        battery_charge = sensors[SensorNames.BATTERY_CHARGE]
        battery_capacity = sensors[SensorNames.BATTERY_CAPACITY]
        battery_percent = (battery_charge / battery_capacity) * 100.0
        print(f'  Battery: {battery_percent:.2f}% at {voltage} V')

        current = sensors[SensorNames.CURRENT] / 1000.0
        print(f'  Current: {current} A')

        current_left = sensors[SensorNames.LEFT_MOTOR_CURRENT] / 1000.0
        current_right = sensors[SensorNames.RIGHT_MOTOR_CURRENT] / 1000.0
        print(f'  Motor Current: {current_left} A {current_right} A')

        charging_state = sensors[SensorNames.CHARGING_STATE]
        print(f'  Charging: {charging_state}')
        print('------------------------------------------------')
        print('Commands:')
        print('------------------------------------------------')

        v_right = sensors[SensorNames.REQUESTED_VELOCITY_RIGHT]
        v_left = sensors[SensorNames.REQUESTED_VELOCITY_LEFT]
        print(f'  Motors: {v_right} {v_left} mm/sec')

        turn_radius = sensors[SensorNames.REQUESTED_RADIUS]
        print(f'  Turn Radius: {turn_radius} mm')


def main():
    # get command line args
    args = handleArgs()
    port = args['port']
    dt = args['sleep']

    # create print monitor
    mon = Monitor()

    # create robot
    bot = pycreate2.Create2(port)
    bot.start()
    bot.safe()

    # now run forever, until someone hits ctrl-C
    try:
        while True:
            try:
                sensor_state = bot.get_sensor_group(100)
                mon.display_formated(sensor_state)
                time.sleep(dt)
            except Exception as e:
                print(e)
                continue
            except:
                raise
    except KeyboardInterrupt:
        print('bye ... ')


if __name__ == '__main__':
    main()
