from flask import Flask, request, send_from_directory
from pystache import Renderer
from os import makedirs
from shutil import rmtree
from pathlib import Path
from num2words import num2words
from flask import Flask, request, send_from_directory
from yattag import Doc as HTML_Doc
from music21.note import Note
from toby.interface.flask_pages.flask_page import FlaskPage, static_web_folder_path_str
from toby.interface.flask_pages.settings import SettingCache


class FlaskException(Exception):
    """This is what happens when flask fails"""


def create_beat_name(beat):
    return f"beat_{num2words(beat)}"


NOTES_FLAT = ["C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"]
NOTES_SHARP = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]


def NoteToMidi(KeyOctave):
    # KeyOctave is formatted like 'C#3'
    key = KeyOctave[:-1]  # eg C, Db
    octave = KeyOctave[-1]  # eg 3, 4
    answer = -1

    try:
        if "b" in key:
            pos = NOTES_FLAT.index(key)
        else:
            pos = NOTES_SHARP.index(key)
    except:
        print("The key is not valid", key)
        return answer

    answer += pos + 12 * (int(octave) + 1) + 1
    return answer


def MidiToNote(note):
    return Note(note).nameWithOctave


def midi_note_value_from_index(number):
    """this should eventually do something"""
    return number


class TrackerConfigUI(FlaskPage):
    def __init__(self, sequencer, ):
        super().__init__("tracker", sequencer)

    def register_settings(self, settings):
        def _set_bpm(bpm):
            print("setting bpm!", bpm)

        def _get_bpm():
            return self.sequencer.beats_per_minute

        def _set_steps(steps):
            print("settingstep!", steps)

        def _get_steps():
            return self.sequencer.beat_length

        settings.register_settings(
            "steps", SettingCache(callforward=_get_steps, callback=_set_steps)
        )
        settings.register_settings(
            "bpm", SettingCache(callforward=_get_bpm, callback=_set_bpm)
        )

    def callback(self):
        print("tracker callback")
        print(request)

    def gen_script(self):
        retstr = "<script>(function () {var xhr = new XMLHttpRequest();"
        for beat_index in range(0, self.sequencer.get_beat_length()):
            retstr += f"""
document.getElementById("{create_beat_name(beat_index)}").addEventListener('click', () => {{
    console.log("button pressed: " + document.getElementById("{create_beat_name(beat_index)}").value);
    xhr.open("POST", '/callback', true);
    xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
    xhr.send("index={"{create_beat_name(beat_index)}"}&response=" + document.getElementById("{create_beat_name(beat_index)}").value);
}});"""
        retstr += """
}) ();
</script>"""
        return retstr

    def gen_body(self) -> str:
        doc, tag, text = HTML_Doc().tagtext()
        with tag("table"):
            for beat_index in range(0, self.sequencer.get_beat_length()):
                beat_value = self.sequencer.get_note(beat_index)
                if not beat_value:
                    beat_value = ""
                else:
                    beat_value = MidiToNote(beat_value)
                print(beat_index, ":", beat_value)
                with tag("tr"):
                    with tag("td"):
                        with tag("select", id=f"beat_{num2words(beat_index)}"):
                            with tag("option", value="off"):
                                text("")
                            for index, label in enumerate(
                                self.sequencer.get_midi_note_labels()
                            ):
                                midi_note_value = midi_note_value_from_index(index)
                                selected_str = (
                                    "true" if midi_note_value == beat_value else "false"
                                )
                                with tag("option", value=label, selected=selected_str):
                                    text(label)
        return doc.getvalue()


if __name__ == "__main__":
    rmtree(static_web_folder_path_str, ignore_errors=True)
    makedirs(static_web_folder_path_str, exist_ok=True)
    app = Flask(__name__, static_url_path="", static_folder=static_web_folder_path_str)
    app.run(host="localhost", port=5000)
    TrackerUI().run()

    while True:
        pass
