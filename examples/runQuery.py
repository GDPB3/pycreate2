#!/usr/bin/env python3

import pycreate2
import time


def prettyPrint(sensors):
    print('-'*70)
    print('{:>40} | {:<5}'.format('Sensor', 'Value'))
    print('-'*70)
    for k, v in sensors.items():
        print(f"{k}: {v}")


if __name__ == "__main__":
    # setup create 2
    bot = pycreate2.Create2()
    bot.start()
    bot.safe()

    bot.digit_led_ascii('hi')  # set a nice message
    bot.led(1)  # turn on debris light

    sensors = {}

    try:
        while True:
            sensors = bot.get_sensor_group(100)
            if sensors:
                prettyPrint(sensors)
            else:
                print('robot asleep')

            time.sleep(1)

    except KeyboardInterrupt:
        print('shutting down ... bye')
