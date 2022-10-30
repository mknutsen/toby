from toby.sequencer.sequencer import Sequencer

from mido import Message
from mido.ports import BaseOutput
from toby.interface.flask_pages.settings import SettingCache


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
        if not self.midi_output_port:
            print("no port")
            return

        self.midi_output_port.send(
            Message("note_on", note=note, channel=self.midi_channel)
        )

    def delete(self):
        self.sequence.delete()

    def register_settings(self, settings):
        def _set_midi_channel(midi_channel):
            print("setting midi_channel!", midi_channel)

        def _get_midi_channel():
            return self.midi_channel

        settings.register_settings(
            "midi_channel",
            SettingCache(callforward=_get_midi_channel, callback=_set_midi_channel),
        )
