import logging
from clock import Clock


class MidiCvException(Exception):
    """ExceptionClass"""


class InvalidStepException(MidiCvException):
    """Invalid step"""


class Sequencer:
    # OFF BY ONE IN THE MIDI CHANNELS
    def __init__(self, beats_per_minute=120, beat_length=8) -> None:
        clock = Clock(beats_per_minute)
        self.__init__(beats_per_minute, beat_length, clock)

    def __init__(self, beats_per_minute, beat_length, clock) -> None:
        self.clock = clock
        self.beats_per_minute = beats_per_minute
        self.clock.add_tic_callback(self.tic_callback)
        self.clock.add_beat_callback(self.beat_callback)
        self.index = 0
        self.beat_length = beat_length
        self.notes = [None] * beat_length
        self.notes_callback = []

    def add_notes_callback(self, callback):
        self.notes_callback.append(callback)

    def delete(self):
        self.clock._delete = True

    def tic_callback(self):
        # print("tic!")
        pass

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

    def add_note(self, step: int, note: int):
        # make sure we're not being led out of bounds
        self.validate_step(step)
        self.notes[step] = note

    def get_note(self, step: int):
        # make sure we're not being led out of bounds
        self.validate_step(step)
        return self.notes[step]


if __name__ == "__main__":
    logging.basicConfig(filename="example.log", encoding="utf-8", level=logging.DEBUG)
    x = Sequencer()
    try:
        while True:
            pass
    # x.clock._delete = True
    finally:
        x.delete()
