from mysequencer.sequencer import Sequencer

from mido import Message
from mido.ports import BaseOutput


class Track:
    # OFF BY ONE IN THE MIDI CHANNELS
    def __init__(self, sequence, midi_channel: int, port: BaseOutput) -> None:
        self.sequence: Sequencer = sequence
        self.sequence.add_notes_callback(self._func)
        self.midi_channel = midi_channel
        # OFF BY ONE IN THE MIDI CHANNELS
        self.midi_output_port: BaseOutput = port

    def _func(self, note) -> None:
        print("note!", note, self.midi_channel)
        self.midi_output_port.send(
            Message("note_on", note=note, channel=self.midi_channel)
        )

    def delete(self):
        self.sequence.delete()
