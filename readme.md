![image](https://raw.githubusercontent.com/GDPB3/pycreate2/master/pics/create.png)

# pyCreate2

A python library for controlling the [iRobot
Create 2](http://www.irobot.com/About-iRobot/STEM/Create-2.aspx)

- [video](https://vimeo.com/266619301): robot could only follow the black tap road and couldn't run into anything. If anything got in the way, it had to naviage around it to its final destination
- [video](https://vimeo.com/266619767): robot pet, follow the pink ball
- [video](https://vimeo.com/266619636): robot pet, follow the pink ball

## Install

Due to this being a fork of the pycreate2 on pypi, the easiest way to install
is using pip specifying the package location like this:

```bash
pip install "pycreate2 @ git+https://github.com/GDPB3/pycreate2"
```

## Use

There are multiple ways to command the Create to move, here are some
examples:

```python
from pycreate2 import Create2
from pycreate2.sensors import SensorNames
import time

# Create a Create2.
port = "/dev/serial"  # where is your serial port?
bot = Create2(port)

# Start the Create 2
bot.start()

# Put the Create2 into 'safe' mode so we can drive it
# This will still provide some protection
bot.safe()

# You are responsible for handling issues, no protection/safety in
# this mode ... becareful
bot.full()

# directly set the motor speeds ... move forward
bot.drive_direct(100, 100)
time.sleep(2)

# turn in place
bot.drive_direct(200,-200)  # inputs for motors are +/- 500 max
time.sleep(2)

# Stop the bot
bot.drive_stop()

# query some sensors
sensors = bot.get_sensor_group(100)  # returns all data
print(sensors[SensorNames.BATTERY_CHARGE])
```

More examples are found in the [examples
folder](https://github.com/GDPB3/pycreate2/tree/master/examples).

## Documents

Additional notes and documents are in the [docs
folder](https://github.com/GDPB3/pycreate2/tree/master/docs/Markdown).

### Modes

![image](https://raw.githubusercontent.com/GDPB3/pycreate2/master/pics/create_modes.png)

The different modes (OFF, PASSIVE, SAFE, and FULL) can be switched
between by calling different commands.

- **OFF:** The robot is off and can charge, it will accept no commands
- **PASSIVE:** The robot is in standbye and can charge. It will send
  sensor packets, but will not move
- **SAFE:** The robot will not charge, but you full control over it
  with a few exceptions. If the cliff sensors or wheel drop sensors
  are triggered, the robot goes back to PASSIVE mode.
- **FULL:** The robot will not charge and you have full control. You
  are responsible to handle any response due to cliff, wheel drop or
  any other sensors.

## Change Log

| Date       | Version | Description                        |
| ---------- | ------- | ---------------------------------- |
| 2026-01-09 | 0.9.13  | Vacuum and brush motors
| 2026-01-05 | 0.9.12  | Retries in sensor reading          |
| 2026-01-04 | 0.9.11  | Pretty agresive serial flushing    |
| 2026-01-03 | 0.9.10  | Changed how reading is done        |
| 2025-12-22 | 0.9.9   | I hate tests (filtering)           |
| 2025-12-22 | 0.9.8   | Better filtering (yes, again)      |
| 2025-12-21 | 0.9.3-7 | Lots of logging                    |
| 2025-11-05 | 0.9.2   | Changed message filtering again    |
| 2025-11-04 | 0.9.1   | Move startup message filtering     |
| 2025-11-03 | 0.9     | Pytest and other minor changes     |
| 2025-11-03 | 0.8.9   | More filtering and startup message |
| 2025-10-29 | 0.8.8   | Confusing names                    |
| 2025-10-29 | 0.8.7   | Allow reading specific sensors     |
| 2025-10-29 | 0.8.6   | Logger                             |
| 2025-10-26 | 0.8.2-5 | Didn't take notes :p               |
| 2021-02-22 | 0.8.1   | Cleaned up code                    |
| 2020-02-16 | 0.8.0   | Simplified interface and bug fixes |
| 2020-02-16 | 0.7.7   | Fixed typo with poetry             |
| 2020-02-16 | 0.7.6   | Fixed typo erro in `bin`           |
| 2020-02-16 | 0.7.5   | Switched to toml and poetry        |
| 2019-06-30 | 0.7.4   | Midi sounds working                |
| 2017-08-26 | 0.7.3   | code clean up and doc updates      |
| 2017-08-26 | 0.7.2   | updates and fixes                  |
| 2017-05-26 | 0.5.0   | init and published to pypi         |

# The MIT License

**Copyright (c) 2007 Damon Kohler**

**Copyright (c) 2015 Jonathan Le Roux (Modifications for Create 2)**

**Copyright (c) 2015 Brandon Pomeroy**

**Copyright (c) 2017 Kevin Walchko**

**Copyright (c) 2025 luengor**

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be included
in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
