#!/usr/bin/env python3
# -*-coding:utf-8-*-
##############################################
# The MIT License (MIT)
# Copyright (c) 2017 Kevin Walchko
# see LICENSE for full details
##############################################
# moves the roomba through a simple sequence

import pycreate2
import time


if __name__ == "__main__":
    # Create a Create2 Bot
    bot = pycreate2.Create2()

    # define a movement path
    path = [
        [200, 200, 3, 'for'],
        [-200, -200, 3, 'back'],
        [0,   0, 1, 'stop'],
        [100,   0, 2, 'rite'],
        [0, 100, 4, 'left'],
        [100,   0, 2, 'rite'],
        [0,   0, 1, 'stop']
    ]

    bot.start()
    bot.safe()

    # path to move
    for lft, rht, dt, s in path:
        print(s)
        bot.digit_led_ascii(s)
        bot.drive_direct(lft, rht)
        time.sleep(dt)

    print('shutting down ... bye')
    bot.drive_stop()
    time.sleep(0.1)
