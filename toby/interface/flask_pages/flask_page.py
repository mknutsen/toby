from abc import ABCMeta, abstractmethod
from pathlib import Path
from flask import Flask, request, send_from_directory
from os import makedirs
from shutil import rmtree
from threading import Thread

from toby.sequencer.sequencer import Sequencer

file_path = Path(__file__) / ".."
static_web_folder_name = "static_web"

static_web_folder_path = file_path / static_web_folder_name
static_web_folder_path_str = static_web_folder_path.resolve()

class FlaskPage(metaclass=ABCMeta):
    def __init__(self, file_name, sequencer):
        self.file_name = file_name
        self.sequencer = sequencer

    @abstractmethod
    def callback(self):
        """must include tags
        """
        return

    @abstractmethod
    def gen_body(self):
        """must include tags
        """
        return

    @abstractmethod
    def gen_script(self):
        """must include tags
        """
        return

    def run(self):
        dashboard_file_path = static_web_folder_path / (self.file_name + ".html")
        dashboard_file_path_str = dashboard_file_path.resolve()

        input_template = f"""
<!doctype html>
<html lang="en">
<head>
    <!-- Required meta tags -->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

    <!-- Bootstrap CSS -->
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.3.1/dist/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">

    {self.gen_body()}
    {self.gen_script()}

    <!-- Optional JavaScript -->
    <!-- jQuery first, then Popper.js, then Bootstrap JS -->
    <script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>
    <script src="https://cdn.jsdelivr.net/npm/popper.js@1.14.7/dist/umd/popper.min.js" integrity="sha384-UO2eT0CpHqdSJQ6hJty5KVphtPhzWj9WO1clHTMGa3JDZwrnQq4sF86dIHNDz0W1" crossorigin="anonymous"></script>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@4.3.1/dist/js/bootstrap.min.js" integrity="sha384-JjSmVgyd0p3pXB1rRibZUAYoIIy6OrQ6VrjIEaFf/nJGzIxFDsf4x0xIM+B07jRM" crossorigin="anonymous"></script>
</html>"""

        print("starting ", dashboard_file_path_str)
        makedirs(static_web_folder_path_str, exist_ok=True)
        with open(dashboard_file_path_str, "w") as file:
            file.write(input_template)

def start_flask_thread(flask_pages):
    rmtree(static_web_folder_path_str, ignore_errors=True)
    makedirs(static_web_folder_path_str, exist_ok=True)

    for flask_page in flask_pages:
        flask_page.run()

    def _start():
        app = Flask(__name__, static_url_path="", static_folder=static_web_folder_path_str)
        for flask_page in flask_pages:
            callback_str = flask_page.file_name
            print("adding callback for", callback_str)
            app.add_url_rule(rule=f'/{callback_str}', endpoint=callback_str, methods=['POST', 'GET'])
            app.view_functions[callback_str] = flask_page.callback
        app.run(host="localhost", port=5000)
    
    thread = Thread(target=_start)
    thread.start()
    return thread

if __name__ == "__main__":
    from tracker_flask import TrackerUI
    from settings import SettingsUI
    
    start_flask_thread()
    seq = Sequencer()
    TrackerUI(seq).run()
    SettingsUI().run()

    while(True):
        pass
