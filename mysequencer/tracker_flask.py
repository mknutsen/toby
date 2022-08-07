from flask import Flask, request, send_from_directory
from pystache import Renderer
from os import makedirs
from shutil import rmtree
from pathlib import Path
from sequencer import Sequencer
from num2words import num2words
from yattag import Doc as HTML_Doc
from music21.note import Note

class FlaskException(Exception):
    """This is what happens when flask fails"""

def create_beat_name(beat):
    return f"beat_{num2words(beat)}"


NOTES_FLAT = ['C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B']
NOTES_SHARP = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

def NoteToMidi(KeyOctave):
    # KeyOctave is formatted like 'C#3'
    key = KeyOctave[:-1]  # eg C, Db
    octave = KeyOctave[-1]   # eg 3, 4
    answer = -1

    try:
        if 'b' in key:
            pos = NOTES_FLAT.index(key)
        else:
            pos = NOTES_SHARP.index(key)
    except:
        print('The key is not valid', key)
        return answer

    answer += pos + 12 * (int(octave) + 1) + 1
    return answer

def MidiToNote(note):
    return Note(note).nameWithOctave

class TrackerUI:
    def __init__(self, seq: Sequencer) -> None:
        """pass"""
        self.sequencer = seq

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
        retstr +=  """
}) ();
</script>"""
        return retstr

    def gen_body(self) -> str:
        doc, tag, text = HTML_Doc().tagtext()
        with tag("table"):
            with tag("form"):
                for beat_index in range(0, self.sequencer.get_beat_length()):
                    beat_value = self.sequencer.get_note(beat_index)
                    if not beat_value:
                        beat_value = ""
                    else:
                        beat_value = MidiToNote(beat_value)
                    print(beat_index, ":", beat_value)
                    with tag ("tr"):
                        with tag("td"):
                            with tag("select", id=f"beat_{num2words(beat_index)}"):
                                with tag("option", value="off"):
                                    text("")
                                for octave in range(2,6):
                                    for note in 'ABCDEFG':
                                        note_name = f"{note}{octave}"
                                        if note_name == beat_value:
                                            with tag("option", value=note_name, selected="true"):
                                                text(note_name)
                                        else:
                                            with tag("option", value=note_name):
                                                text(note_name)
        return doc.getvalue()


def main(sequencer, callback=None):
    file_path = Path(__file__) / ".."
    static_web_folder_name = "static_web"
    dashboard_file_name = "dashboard"
    tracker = TrackerUI(sequencer)


    _DEBUG = True
    static_web_folder_path = file_path / static_web_folder_name
    static_web_folder_path_str = static_web_folder_path.resolve()
    dashboard_file_path = static_web_folder_path / (dashboard_file_name + ".html")
    dashboard_file_path_str = dashboard_file_path.resolve()

    rmtree(static_web_folder_path_str, ignore_errors=True)
    makedirs(static_web_folder_path_str, exist_ok=True)

    input_template = f"""
    <!doctype html>
    <html lang="en">
    <head>
        <!-- Required meta tags -->
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

        <!-- Bootstrap CSS -->
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.3.1/dist/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">

        {tracker.gen_body()}
        {tracker.gen_script()}

        <!-- Optional JavaScript -->
        <!-- jQuery first, then Popper.js, then Bootstrap JS -->
        <script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>
        <script src="https://cdn.jsdelivr.net/npm/popper.js@1.14.7/dist/umd/popper.min.js" integrity="sha384-UO2eT0CpHqdSJQ6hJty5KVphtPhzWj9WO1clHTMGa3JDZwrnQq4sF86dIHNDz0W1" crossorigin="anonymous"></script>
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@4.3.1/dist/js/bootstrap.min.js" integrity="sha384-JjSmVgyd0p3pXB1rRibZUAYoIIy6OrQ6VrjIEaFf/nJGzIxFDsf4x0xIM+B07jRM" crossorigin="anonymous"></script>
    </body>
    </html>
    """
    with open(dashboard_file_path_str, "w") as file:
        file.write(input_template)
    app = Flask(__name__, static_url_path="", static_folder=static_web_folder_path_str)
    app.add_url_rule('/callback', 'response', callback, methods=['POST', 'GET'])
    app.run(host="localhost", port=5000)

if __name__ == "__main__":
    main()
