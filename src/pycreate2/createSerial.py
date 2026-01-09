import serial
import pycreate2.logger  # just to set up logging
import logging
import struct
import time

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

    def open(self, port: str, baud: int = 115200, timeout: int = 1) -> bytes:
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

        if self.ser.is_open:
            self.ser.close()
        self.ser.open()
        if self.ser.is_open:
            logger.info("Create opened serial: {}".format(self.ser))
        else:
            raise Exception("Failed to open {} at {}".format(port, baud))

        # if we get data on open, it's a startup message.
        # read it and return it to be parsed/handled by caller
        startup_msg = self.ser.read(2048)

        return startup_msg

    def write(self, opcode: int, data: tuple | None = None, flush: bool = False):
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
        if flush:
            logger.debug("Flushing output buffer")
            self.ser.flush()
        logger.debug("Wrote: {}".format(msg))

    def waiting(self) -> int:
        """
        Returns the number of bytes waiting in the input buffer.
        """
        if not self.ser.is_open:
            raise Exception("You must open the serial port first")

        return self.ser.in_waiting

    def flush_input(self):
        """
        Flushes the input buffer.
        """
        if not self.ser.is_open:
            raise Exception("You must open the serial port first")

        logger.info("Flushing input buffer")
        self.ser.flush()
        self.ser.reset_output_buffer()
        self.ser.reset_input_buffer()

    def read(self, num_bytes: int) -> bytes:
        """
        Read a string of 'num_bytes' bytes from the robot.

        :param num_bytes: number of bytes to read from the robot
        :type num_bytes: int
        """
        if not self.ser.is_open:
            raise Exception("You must open the serial port first")

        # Read
        raw_data = self.ser.read(num_bytes)
        available_bytes = self.ser.in_waiting
        if available_bytes > 0:
            raw_data += self.ser.read(available_bytes)

        filtered_data = self.filter_begin(raw_data)
        if len(filtered_data) != num_bytes:
            logger.error(
                f"Expected {num_bytes} bytes but got {len(filtered_data)} bytes after filtering"
            )
            raise Exception("Did not receive expected number of bytes from Create2")

        logger.debug(f"Final read output: {filtered_data}")
        return bytes(filtered_data)

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
        full_flash_message = b"    Flash CRC successful: 0x0 (0x0)\n\r"
        if full_flash_message in msg:
            msg = msg.replace(full_flash_message, b"")
            logger.warning(
                "Filtered out exact startup message: {}".format(
                    full_flash_message.decode("utf-8")[:-2])
            )
            return SerialCommandInterface.filter_begin(msg)  # Recursion to filter multiple messages

        # No exact full message, look for partials
        flash_msg = msg.find(b"(0x0)\n\r")
        wakeup_msg = msg.find(b"conds\r\n")

        found = max(flash_msg, wakeup_msg)

        if found == -1:
            return msg

        filtered, msg = msg[: found + 7], msg[found + 7:]
        logger.warning(
            "Filtered out startup message: {}".format(
                filtered.decode("utf-8")[:-2])
        )
        return msg # recursion here is risky
