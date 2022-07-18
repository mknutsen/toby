from abc import ABC, ABCMeta, abstractclassmethod
from threading import Thread
from collections import namedtuple
from enum import Enum, auto


class MidiCvException(Exception):
    """ExceptionClass"""


Pixel = namedtuple("Pixel", "index r g b brightness")


class Macropad(ABC):
    def __init__(self, num_pixels):
        self.num_pixels = num_pixels

    @abstractclassmethod
    def set_led(self, pixel_index, r, g, b, brightness):
        raise Exception("Not Implemented")

    def set_leds(self, r, g, b, brightness):
        for num in range(0, self.num_pixels):
            self.set_led(num, r, g, b, brightness)

    def set_led_off(self, pixel_index):
        self.set_led(pixel_index, 0, 0, 0, 0)

    def all_off(self):
        self.set_leds(0, 0, 0, 0)


class arduino_message_type(Enum):
    ON = auto()
    OFF = auto()
    BEAT = auto()


arduino_message_types = dict()
arduino_message_types[arduino_message_type.ON] = "i"
arduino_message_types[arduino_message_type.OFF] = "d"
arduino_message_types[arduino_message_type.BEAT] = "b"


class ArduinoMacropad(Macropad):
    def __init__(self, num_pixels, serial_port):
        super.__init__(num_pixels)
        self._delete = False
        self._write_thread = Thread(target=self._write_func)
        self._read_thread = Thread(target=self._read_func)
        self._work_packets = []
        self.serial_connection = serial_port
        self._read_thread.start()
        self._write_thread.start()
        self._read_callbacks = []

    def add_read_callback(self, callback):
        self._read_callbacks.append(callback)

    def set_led(self, pixel_index, r, g, b, brightness):
        self._work_packets.append(
            Pixel(index=pixel_index, r=r, g=g, b=b, brightness=brightness)
        )

    def _read_func(self):
        incoming_string = ""
        while self._delete is False:
            incoming_string += self.serial_connection.read(
                self.serial_connection.in_waiting
            ).decode("utf-8")
            while new_line_index := incoming_string.find("\n") >= 0:
                bs = incoming_string[0:new_line_index]
                try:
                    incoming_string = incoming_string[new_line_index + 1 :]
                except:
                    incoming_string = ""
                try:
                    auth, command, value = bs.split("-")
                except:
                    print("BAD STRING: ", bs)

                if auth != "abc123":
                    raise MidiCvException()

                for callback in self._read_callbacks:
                    callback(command, value)

    def _write_func(self):
        while self._delete is False:
            try:
                packet = self._work_packets.pop(0)
            except IndexError:
                continue

            function_number = (
                "d" if packet.r == 0 and packet.g == 0 and packet.b == 0 else "i"
            )
            packet_str = f"abc123-{function_number}-{packet.pixel_number}\n"
            self.serial_connection.write(packet_str.encode())

    def __del__(self):
        self._delete = True
