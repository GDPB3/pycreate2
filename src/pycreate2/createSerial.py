import serial
import pycreate2.logger  # just to set up logging
import logging
import struct

logger = logging.getLogger("create2serial")


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
            dsrdtr=False,
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

        assert baud in [115200, 19200], "baudrate must be 115200 or 19200"
        self.ser.baudrate = baud
        self.ser.timeout = timeout

        # if we get data on open, it's a startup message.
        # read it and return it to be parsed/handled by caller
        startup_msg = self.ser.read(2048)

        if self.ser.is_open:
            self.ser.close()
        self.ser.open()
        if self.ser.is_open:
            logger.info("Create opened serial: {}".format(self.ser))
        else:
            raise Exception("Failed to open {} at {}".format(port, baud))

        return startup_msg

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
        self.ser.write(struct.pack("B" * len(msg), *msg))
        logger.debug("Wrote: {}".format(msg))

    def read(self, num_bytes: int, throw_on_timeout: bool = True) -> bytes:
        """
        Read a string of 'num_bytes' bytes from the robot.

        :param num_bytes: number of bytes to read from the robot
        :type num_bytes: int
        """
        if not self.ser.is_open:
            raise Exception("You must open the serial port first")

        # Get the number of bytes currently available
        available_bytes = self.ser.in_waiting
        # War crime
        while available_bytes < num_bytes:
            available_bytes = self.ser.in_waiting

        # If the number of available bytes is the same as requested, read them all at once
        if available_bytes == num_bytes:
            data = self.ser.read(num_bytes)
            return data

        # If there are more bytes than requested the robot might be sending
        # trash data, so we read it all and filter it
        if available_bytes > num_bytes:
            raw_data = self.ser.read(available_bytes)
        else:
            # If not, try to read the requested number of bytes
            raw_data = self.ser.read(num_bytes)

        filtered_data = self.filter_begin(raw_data)

        if len(filtered_data) == num_bytes:
            return filtered_data
        else:
            logger.warning(f"Filtered data does not match requested size")
            return filtered_data[:num_bytes]

    def read_until(self, delim: bytes = b"\n\r") -> bytes:
        """
        Reads from the serial port until the delimiter is found.

        :param delim: the byte sequence to read until
        :type delim: bytes
        """
        if not self.ser.is_open:
            raise Exception("You must open the serial port first")

        data = self.ser.read_until(delim)
        return data

    def close(self):
        """
        Closes the serial connection.
        """
        if self.ser.is_open:
            logger.info(
                "Closing port {} @ {}".format(self.ser.port, self.ser.baudrate))
            self.ser.close()
        else:
            logger.warning("Trying to close a serial port that isn't open")

    @staticmethod
    def filter_begin(msg: bytes) -> bytes:
        flash_msg = msg.find(b"(0x0)\n\r")
        wakeup_msg = msg.find(b"conds\r\n")

        found = max(flash_msg, wakeup_msg)

        if found == -1:
            return msg

        filtered, msg = msg[: found + 7], msg[found + 7:]
        logger.info(
            "Filtered out startup message: {}".format(
                filtered.decode("utf-8")[:-2])
        )
        return msg
