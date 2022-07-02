from mido import get_input_names, get_output_names, open_input, open_output, Message
from sequencer import Sequencer
from clock import Clock
import logging
from track import Track
from mido.ports import BaseOutput
tracks = []
from typing import Optional
from time import sleep

GLOBAL_OUTPUT_PORT: Optional[BaseOutput] = None
# OFF BY ONE IN THE MIDI CHANNELS
def delete():
    if not tracks:
        return
    for track in tracks:
        track.delete()


def main():
    global tracks, GLOBAL_OUTPUT_PORT
    output_port_name = "mio"
    beats_per_minute = 120
    beat_length = 8
    num_tracks = 8
    clock = Clock(beats_per_minute)

    try:
        GLOBAL_OUTPUT_PORT = open_output(output_port_name)
    except:
        print(get_output_names())
        raise

    midi_channels = [i for i in range(0, num_tracks)]
    for channel in midi_channels:
        sequencer = Sequencer(beats_per_minute=beats_per_minute, beat_length=beat_length, clock=clock)
        tracks.append(Track(sequence=sequencer, midi_channel=channel, port=GLOBAL_OUTPUT_PORT))

    tracks[0].sequence.add_note(1, 60)

    for channel in midi_channels:
        message = Message("note_on", note=60, channel=channel)
        GLOBAL_OUTPUT_PORT.send(message)
    while True:
        pass


if __name__ == "__main__":

    logging.basicConfig(filename="example.log", encoding="utf-8", level=logging.DEBUG)
    try:
        main()
    finally:
        delete()
