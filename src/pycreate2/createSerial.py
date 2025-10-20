##############################################
# The MIT License (MIT)
# Copyright (c) 2017 Kevin Walchko
# see LICENSE for full details
##############################################
# This is basically the interface between the Create2 and pyserial

import serial
import struct


class SerialCommandInterface(object):
    """
    This class handles sending commands to the Create2. Writes will take in tuples
    and format the data to transfer to the Create.
    """

    def __init__(self):
        """
        Constructor.

        Creates the serial port, but doesn't open it yet. Call open(port) to open
        it.
        """
        self.ser = serial.Serial(
            baudrate=115200,
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,

            # Flow control
            xonxoff=False,
            rtscts=False,
            dsrdtr=False
        )

    def __del__(self):
        """
        Destructor.

        Closes the serial port
        """
        self.close()

    def open(self, port: str, baud: int = 115200, timeout: int = 1):
        """
        Opens a serial port to the create.

        :param port: the serial port to open, ie, '/dev/ttyUSB0'
        :param baud: default is 115200, can be set to 19200 doing nefarious things
        :param timeout: serial timeout in seconds
        """
        self.ser.port = port

        assert baud in [115200, 19200], 'baudrate must be 115200 or 19200'
        self.ser.baudrate = baud
        self.ser.timeout = timeout

        if self.ser.is_open:
            self.ser.close()
        self.ser.open()
        if self.ser.is_open:
            # print("Create opened serial: {}".format(self.ser))
            print('-'*40)
            print(' Create opened serial connection')
            print('   port: {}'.format(self.ser.port))
            print('   datarate: {} bps'.format(self.ser.baudrate))
            print('-'*40)
        else:
            raise Exception('Failed to open {} at {}'.format(port, baud))

    def write(self, opcode: int, data: tuple | None = None):
        """
        Writes a command to the create. There needs to be an opcode and optionally
        data. Not all commands have data associated with it.

        :param opcode: The operation opcode to send to the Create (see api)
        :type opcode: int

        :param data: a tuple with data associated with a given opcode (see api)
        :type data: tuple | None
        """
        msg = (opcode,) + data if data else (opcode,)
        self.ser.write(struct.pack('B' * len(msg), *msg))

    def read(self, num_bytes: int) -> bytes:
        """
        Read a string of 'num_bytes' bytes from the robot.

        :param num_bytes: number of bytes to read from the robot
        :type num_bytes: int
        """
        if not self.ser.is_open:
            raise Exception('You must open the serial port first')

        data = self.ser.read(num_bytes)

        return data

    def close(self):
        """
        Closes the serial connection.
        """
        if self.ser.is_open:
            print('Closing port {} @ {}'.format(self.ser.port, self.ser.baudrate))
            self.ser.close()
