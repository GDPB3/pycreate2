#!/usr/bin/env python3
# -*-coding:utf-8-*-
##############################################
# The MIT License (MIT)
# Copyright (c) 2017 Kevin Walchko
# see LICENSE for full details
##############################################

from pycreate2 import Create2
import time


if __name__ == "__main__":
    bot = Create2()

    bot.start()

    bot.safe()

    print('Starting ...')

    cnt = 0
    while True:
        # Packet 100 contains all sensor data.
        sensor = bot.get_sensors()

        if cnt % 20 == 0:
            print("[L ] [LF] [LC] [CR] [RF] [ R]")

        print(f"{sensor.light_bumper_left:4} {sensor.light_bumper_front_left:4} {sensor.light_bumper_center_left:4} {sensor.light_bumper_center_right:4} {sensor.light_bumper_front_right:4} {sensor.light_bumper_right:4}")
        time.sleep(.01)

        cnt += 1
