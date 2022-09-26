from collections import namedtuple
from toby.sequencer.sequencer import Sequencer
from toby.clock import Clock
from toby.value import WholeValue
from toby.midi_track import Track

from collections import namedtuple
from mido import get_input_names, get_output_names, open_input, open_output, Message
from random import choices
import logging

Coordinate = namedtuple("Coordinate", "x y")


def coordinate_eq(a, b):
    return a.x.value == b.x.value and a.y.value == b.y.value


class GridSequencer(Sequencer):
    def __init__(self, beats_per_minute, width, height, clock) -> None:
        super().__init__(
            beats_per_minute=beats_per_minute, beat_length=(width * height), clock=clock
        )
        self.width = width
        self.height = height
        self.coordinates = Coordinate(
            x=WholeValue(
                min_value=0, max_value=self.width - 1, initialized_value=(width / 2)
            ),
            y=WholeValue(
                min_value=0, max_value=self.height - 1, initialized_value=(height / 2)
            ),
        )

    def move_up(self):
        self.coordinates.y.value = self.coordinates.y.value - 1

    def move_left(self):
        self.coordinates.x.value = self.coordinates.x.value - 1

    def move_right(self):
        self.coordinates.x.value = self.coordinates.x.value + 1

    def move_down(self):
        self.coordinates.y.value = self.coordinates.y.value + 1

    def beat_callback(self):
        # print("beat!")
        next_action = choices(
            [self.move_up, self.move_left, self.move_right, self.move_down]
        )
        # perform the randomly selected move
        next_action[0]()
        coordinates_step_number = self.current_step_number()
        note = self.notes[coordinates_step_number]
        if note:
            for callback in self.notes_callback:
                callback(note)
            print("note: ", note)
        # self.print_grid()
    
    def current_step_number(self):
        return self.step_number(self.coordinates.x.value, self.coordinates.y.value)

    def step_number(self, row: int, column: int):
        return column + (self.width * row)

    def add_note_grid(self, row, column, note):
        self.add_note(self.step_number(row, column), note)

    def get_note_grid(self, row, column, note):
        return self.get_note(self.step_number(row, column), note)

    def clear_step_grid(self, row, column):
        self.clear_step(self.step_number(row, column))

    def print_grid(self):
        print(self.coordinates.x.value, self.coordinates.y.value)
        for row in range(0, self.width):
            row_str = ""
            for col in range(0, self.height):
                note = self.get_note(self.step_number(row=row, column=col))
                current_location = Coordinate(
                    x=WholeValue(
                        min_value=0,
                        max_value=self.width - 1,
                        initialized_value=row,
                    ),
                    y=WholeValue(
                        min_value=0,
                        max_value=self.height - 1,
                        initialized_value=col,
                    ),
                )
                is_current_location_beat = coordinate_eq(
                    current_location, self.coordinates
                )

                note_str = f"{note:03d}" if note else "   "
                if is_current_location_beat:
                    row_str += f" <{note_str}>"
                else:
                    row_str += f" [{note_str}]"
            print(row_str)
        print()


if __name__ == "__main__":
    logging.basicConfig(filename="example.log", encoding="utf-8", level=logging.DEBUG)
    _MIDI_OUTPUT_PORT_NAME = "mio"
    midi_channel = 0  # midi indexing is off by one
    beats_per_minute = 90
    clock = Clock(beats_per_minute)
    width = 11
    seq = GridSequencer(beats_per_minute, width, width, clock)
    output = open_output(_MIDI_OUTPUT_PORT_NAME)
    

    for i in range(0, width * width):
        seq.add_note(step=i, note=i + 1)

    seq.print_grid()
    
    track = Track(sequence=seq, midi_channel=midi_channel, port=output)
    try:
        while True:
            pass
    # x.clock._delete = True
    finally:
        x.delete()
