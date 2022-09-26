from toby.interface.flask_pages.flask_page import FlaskPage, static_web_folder_path_str
from yattag import Doc as HTML_Doc
class SettingsUI(FlaskPage):
    def __init__(self, sequencer, callback):
        super().__init__("settings", sequencer, callback)

    def gen_body(self):
        doc, tag, text = HTML_Doc().tagtext()
        with tag("table"):
            for number in range(0, 128): # replace
                with tag("tr"):
                    with tag("td"):
                        text(f"{number}")
                    with tag("td"):
                        with tag("input", type="text", id=f"settings_{number}"):
                            text(f"{number}") # replace with current value
        with tag("button", id="button"):
            text("save!")
        return doc.getvalue()
    
    def gen_script(self):
        return ""