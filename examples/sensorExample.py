#!/usr/bin/env python3
# -*-coding:utf-8-*-
##############################################
# The MIT License (MIT)
# Copyright (c) 2017 Kevin Walchko
# see LICENSE for full details
##############################################

from pycreate2 import Create2
from pycreate2.sensors import PacketNames
import sys
import time


if __name__ == "__main__":
    if len(sys.argv) > 1:
        port = sys.argv[1]
        print(f"Using port: {port}")
        bot = Create2(port=port)
    else:
        bot = Create2()

    bot.start()

    bot.safe()

    print('Starting ...')

    cnt = 0
    names = [
        PacketNames.LIGHT_BUMP_LEFT,
        PacketNames.LIGHT_BUMP_FRONT_LEFT,
        PacketNames.LIGHT_BUMP_CENTER_LEFT,
        PacketNames.LIGHT_BUMP_CENTER_RIGHT,
        PacketNames.LIGHT_BUMP_FRONT_RIGHT,
        PacketNames.LIGHT_BUMP_RIGHT,
    ]
    while True:
        # Packet 100 contains all sensor data.
        sensors = bot.get_sensor_list(names)

        if cnt % 20 == 0:
            print("[L ] [LF] [LC] [CR] [RF] [ R]")

        print(
            f"{sensors[names[0]]:4} {sensors[names[1]]:4} {sensors[names[2]]:4} {sensors[names[3]]:4} {sensors[names[4]]:4} {sensors[names[5]]:4}")
        time.sleep(.01)

        cnt += 1
