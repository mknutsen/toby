import logging
from toby.clock import Clock
from enum import Enum, auto

class MidiCvException(Exception):
    """ExceptionClass"""


class InvalidStepException(MidiCvException):
    """Invalid step"""


class led_message_type(Enum):
    ON = auto()
    OFF = auto()


class Sequencer:
    # OFF BY ONE IN THE MIDI CHANNELS
    def __init__(self, beats_per_minute = 120, beat_length = 8, clock = None) -> None:
        self.clock = clock if clock else Clock(beats_per_minute)
        self.beats_per_minute = self.clock.beats_per_minute
        self.clock.add_tic_callback(self.tic_callback)
        self.clock.add_beat_callback(self.beat_callback)
        self.index = 0
        self.beat_length = beat_length
        self.notes = [None] * beat_length
        self.notes_callback = []
        self.sequence_update_callback = []

    def add_sequence_update_callback(self, callback):
        self.sequence_update_callback.append(callback)

    def add_notes_callback(self, callback):
        self.notes_callback.append(callback)

    def delete(self):
        self.clock._delete = True

    def tic_callback(self):
        # print("tic!")
        pass
    
    def get_midi_note_labels(self):
        return [i for i in range(0, 128)]

    def sequence_update_callback_clear(self, step):
        for callback in self.sequence_update_callback:
            callback(led_message_type.OFF, step)

    def sequence_update_callback_add(self, step):
        for callback in self.sequence_update_callback:
            callback(led_message_type.ON, step)

    def beat_callback(self):
        # print("beat!")
        self.index += 1
        if self.index == self.beat_length:
            # print("bar!")
            self.index = 0

        note = self.notes[self.index]
        if note:
            for callback in self.notes_callback:
                callback(note)

    def validate_step(self, step):
        if step < 0 or step >= self.beat_length:
            raise InvalidStepException()

    def trigger_note(self, note: int) -> bool:
        """_summary_

        Args:
            note (int): _description_

        Returns:
            bool: True if note add False if note deleted TODO
        """
        step = self.index
        if self.notes[step]:
            self.clear_step(step)
            return (False, step)
        else:
            self.add_note(step=self.index, note=note)
            return (True, step)

    def get_beat_length(self):
        return self.beat_length

    def add_note(self, step: int, note: int):
        # make sure we're not being led out of bounds
        self.validate_step(step)
        self.notes[step] = note
        self.sequence_update_callback_add(step)

    def get_note(self, step: int):
        # make sure we're not being led out of bounds
        self.validate_step(step)
        return self.notes[step]

    def clear_step(self, step: int):
        self.validate_step(step)
        self.notes[step] = None
        self.sequence_update_callback_clear(step)


if __name__ == "__main__":
    logging.basicConfig(filename="example.log", encoding="utf-8", level=logging.DEBUG)
    x = Sequencer()
    try:
        while True:
            pass
    # x.clock._delete = True
    finally:
        x.delete()
