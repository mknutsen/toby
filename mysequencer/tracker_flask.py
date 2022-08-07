from flask import Flask, request, send_from_directory
from pystache import Renderer
from os import makedirs
from shutil import rmtree
from pathlib import Path


class FlaskException(Exception):
    """This is what happens when flask fails"""





def main(beat_length, callback=None):
    file_path = Path(__file__) / ".."
    static_web_folder_name = "static_web"
    dashboard_file_name = "dashboard"


    _DEBUG = True
    static_web_folder_path = file_path / static_web_folder_name
    static_web_folder_path_str = static_web_folder_path.resolve()
    dashboard_file_path = static_web_folder_path / (dashboard_file_name + ".html")
    dashboard_file_path_str = dashboard_file_path.resolve()

    rmtree(static_web_folder_path_str, ignore_errors=True)
    makedirs(static_web_folder_path_str, exist_ok=True)

    def gen_body():
        return """
<form>
  <input type="textbox" id="stock_box">
  <input type="button" id="stock_button">
</form>
<script>
  (function () {
    var xhr = new XMLHttpRequest();
    document.getElementById("stock_button").addEventListener('click', () => {
      console.log("button pressed: " + document.getElementById("stock_box").value);
      xhr.open("POST", '/callback', true);
      xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
      xhr.send("response=" + document.getElementById("stock_box").value);
    });
  })();
</script>
        """

    input_template = f"""
    <!doctype html>
    <html lang="en">
    <head>
        <!-- Required meta tags -->
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

        <!-- Bootstrap CSS -->
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.3.1/dist/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">

        {gen_body()}

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
