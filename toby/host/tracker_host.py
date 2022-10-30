from matplotlib.pyplot import cool
from serial import Serial
from toby.sequencer.sequencer import Sequencer, led_message_type
from toby.clock import Clock
from toby.midi_track import Track
from flask import Flask, request, send_from_directory

from mido import get_input_names, get_output_names, open_input, open_output, Message
import logging
from threading import Thread
from time import time
from flask import request


from toby.interface.flask_pages.tracker_config import TrackerConfigUI
from toby.interface.flask_pages.settings import SettingsUI
from toby.interface.flask_pages.flask_page import start_flask_thread

GLOBAL_OUTPUT_PORT = None
TRACK = None
THREAD = None
SEQUENCER = None
_MIDI_OUTPUT_PORT_NAME = "mio"
_DELETE = False


class HostException(Exception):
    """ExceptionClass"""


class InvalidCommand(HostException):
    """Invalid step"""


def delete():
    global TRACK, _DELETE, _SERIAL_PORT
    _DELETE = True
    if TRACK:
        TRACK.delete()


def main():
    global TRACK, GLOBAL_OUTPUT_PORT, THREAD, SEQUENCER, _DELETE, _SERIAL_PORT, _MACRO_PAD
    beats_per_minute = 120
    beat_length = 12

    clock = Clock(beats_per_minute)

    print("GLOBAL PORT DISABLED")
    # try:
    #     GLOBAL_OUTPUT_PORT = open_output(_MIDI_OUTPUT_PORT_NAME)
    # except:
    #     print(get_output_names())
    #     raise

    # uses the clock to handle the sequence and sends notes to the track
    SEQUENCER = Sequencer(
        beats_per_minute=beats_per_minute, beat_length=beat_length, clock=clock
    )
    SEQUENCER.add_note(0, 50)
    SEQUENCER.add_note(4, 55)

    # outputs notes to midi channel
    TRACK = Track(sequence=SEQUENCER, midi_channel=0, port=GLOBAL_OUTPUT_PORT)
    tracker = TrackerJsonUI(SEQUENCER)
    settings = SettingsUI(SEQUENCER)
    tracker.register_settings(settings)
    TRACK.register_settings(settings)
    start_flask_thread([tracker, settings])

    while not _DELETE:
        pass


if __name__ == "__main__":

    logging.basicConfig(filename="example.log", encoding="utf-8", level=logging.DEBUG)
    try:
        main()
    finally:
        delete()
