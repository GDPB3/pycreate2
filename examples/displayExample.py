#!/usr/bin/env python3
# display random characters to the roomba display. Note, there are some that
# roomba can't print, those are changed to ' '
import pycreate2
import time
import string
import random


if __name__ == "__main__":
    # setup create 2
    bot = pycreate2.Create2()
    bot.start()
    bot.safe()

    # get the set of all printable ascii characters
    char_set = string.printable

    print('WARNING: Not all of the allowed printable characters really look good on the LCD')

    while True:
        word = ''.join(random.sample(char_set, 4))
        print('phrase:', word)
        bot.digit_led_ascii(word)
        time.sleep(2)
