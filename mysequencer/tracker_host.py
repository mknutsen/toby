from matplotlib.pyplot import cool
from serial import Serial
from mysequencer.sequencer import Sequencer, led_message_type
from mysequencer.clock import Clock
from mysequencer.track import Track

from mido import get_input_names, get_output_names, open_input, open_output, Message
import logging
from threading import Thread
from time import time
from flask import request

from tracker_flask import main as RunDashboard

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

def sequence_update_macropad(mode, pin):
    global _MACRO_PAD

    if mode == led_message_type.ON:
        _MACRO_PAD.set_led(pin, 124,252,0)
    elif mode == led_message_type.OFF:
        _MACRO_PAD.set_led_off(pin)
    else:
        raise Exception(f"unknown mode {mode}")

def main():
    global TRACK, GLOBAL_OUTPUT_PORT, THREAD, SEQUENCER, _DELETE, _SERIAL_PORT, _MACRO_PAD
    beats_per_minute = 120
    beat_length = 12
    
    clock = Clock(beats_per_minute)

    # try:
    #     GLOBAL_OUTPUT_PORT = open_output(_MIDI_OUTPUT_PORT_NAME)
    # except:
    #     print(get_output_names())
    #     raise


    # uses the clock to handle the sequence and sends notes to the track
    SEQUENCER = Sequencer(beats_per_minute=beats_per_minute, beat_length=beat_length, clock=clock)
    SEQUENCER.add_note(0, 50)
    SEQUENCER.add_note(4, 55)
    
    # outputs notes to midi channel
    # TRACK = Track(sequence=SEQUENCER, midi_channel=midi_channel, port=GLOBAL_OUTPUT_PORT)
    def callback(*argv):
        print("callback", argv)
        if request:
            response = request.form.get("response")
            print(response)
        pass

    RunDashboard(SEQUENCER, callback)

    while not _DELETE:
        pass


if __name__ == "__main__":

    logging.basicConfig(filename="example.log", encoding="utf-8", level=logging.DEBUG)
    try:
        main()
    finally:
        delete()


            

