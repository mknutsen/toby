from toby.interface.flask_pages.flask_page import FlaskPage, static_web_folder_path_str
from yattag import Doc as HTML_Doc
from flask import Flask, request, send_from_directory
import base64


class SettingCache:
    def __init__(self, callforward, callback) -> None:
        self.callback = callback
        self.callforward = callforward


class SettingsUI(FlaskPage):
    def __init__(self, sequencer):
        super().__init__("settings", sequencer)
        self.settings = {}

    def callback(self):
        # print("settings callbacksdfads", request.form)
        for key, value in request.form.items():
            self.processSetting(key, value)

    def register_settings(self, key, setting_cache):
        self.settings[key] = setting_cache

    def processSetting(self, key, value):
        # print("process setting", key, value)
        self.settings[key].callback(value)

    def gen_body(self):
        doc, tag, text = HTML_Doc().tagtext()
        with tag("body"):
            with tag("table"):
                for name, settingsCache in self.settings.items():
                    with tag("tr"):
                        with tag("td"):
                            text(f"{name}")
                        with tag("td"):
                            with tag("input", type="text", id=f"{name}"):
                                pass

            with tag("button", id="button"):
                text("save!")
        return doc.getvalue()

    def gen_script(self):
        return_value = """
<script>
(function () {{
"""
        return_value += "".join(
            [
                f'document.getElementById("{settings_name}").value = "{settings_cache.callforward()}";'
                for settings_name, settings_cache in self.settings.items()
            ]
        )
        return_value += """
document.getElementById("button").addEventListener('click', () => {{
    var xhr = new XMLHttpRequest();
    xhr.open("POST", '/settings', true);
    xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
    console.log("button pressed");
    var resp_map = new Map();
    var resp_string = "";
"""

        for settings_name, settings_cache in self.settings.items():
            return_value += f'console.log("{settings_name}");'
            return_value += f'resp_map.set("{settings_name}", document.getElementById("{settings_name}").value);'
        #  i need to populate the string with this map i made of the key value pairs
        return_value += """
        var keys =  Array.from(resp_map.keys());
        console.log(resp_map);
        console.log("mid");
        console.log(keys);
        for (let i = 0; i < keys.length; i++) {
            const key = keys[i];
            const value = resp_map.get(key);
            console.log("abc123");
             console.log(key);
             console.log(value);
            resp_string += "&" + key + "=" + value;
        }
        console.log("end");
        console.log(resp_string.substring(1));
        xhr.send(resp_string.substring(1));
}});
}}) ();
</script>
"""
        #
        return return_value
