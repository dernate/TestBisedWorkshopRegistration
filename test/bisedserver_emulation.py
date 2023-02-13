#!/usr/bin/env python3

from http.server import BaseHTTPRequestHandler, HTTPServer
from time import sleep

PORT = 80
FORM = """
<p><b>Name</b><br /><input maxlength="50" name="Name" size="50" type="text" />&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
<p><b>Vorname:</b><br /><input maxlength="50" name="Vorname" size="50" type="text" /></p>
<select id="status" name="status">                      
<option value="0">--Select Status--</option>
<option value="1">Lehrkraft</option>
<option value="2">Studierende*r</option>
<option value="3">Lehramtsanw&auml;rter*in</option>
<option value="4">Teilnehmer*in des Programms Lehrkr&auml;ftePlus</option>
<option value="5">Sonstige</option>
</select>

<p><b>Institution:</b><br /><input maxlength="50" name="Schule" size="50" type="text" /></p>
<p><b>E-Mail-Adresse:</b><br /><input maxlength="50" name="Mail" size="50" type="text" /></p>
<p><b>E-Mail-Best&auml;tigung:</b><br /><input maxlength="50" name="CompareMail" size="50" type="text" /></p>
"""
#onclick="location.href = '/submit';"
BUTTON = """ <p><input id="submitbutton" type="submit" value="verbindliche Anmeldung absenden" /></p>"""
SUBMIT = """<center><h1>Vielen Dank f&uuml;r Ihre Anmeldung!</h1></center>"""
BUTTON_JS = """<script type="text/javascript">
    document.getElementById("submitbutton").onclick = function () {
        //check if all fields are filled
        var name = document.getElementsByName("Name")[0].value;
        var firstname = document.getElementsByName("Vorname")[0].value;
        var status = document.getElementsByName("status")[0].value;
        var mail = document.getElementsByName("Mail")[0].value;
        var comparemail = document.getElementsByName("CompareMail")[0].value;
        if (name == "" || firstname == "" || status == "0" || mail == "" || comparemail == "") {
            alert("Bitte f&uuml;llen Sie alle Felder aus!");
            return false;
        }
        //check if mail is valid
        if (!mail.includes("@")) {
            alert("Die E-Mail-Adresse ist ung&uuml;ltig!");
            return false;
        }
        //check if mail and comparemail are the same
        if (mail != comparemail) {
            alert("Die E-Mail-Adressen stimmen nicht &uuml;berein!");
            return false;
        }
        //redirect to submit page
        location.href = '/submit';
    };
</script>"""


def load_input_html() -> str:
    with open("input.html", "r") as f:
        return f.read()


class MyServer(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        if self.path == "/submit":
            self.wfile.write(bytes("<html><head><title>Test</title></head><body>", "utf-8"))
            self.wfile.write(bytes(SUBMIT, "utf-8"))
            self.wfile.write(bytes(f"</body>{BUTTON_JS}</html>", "utf-8"))
        elif self.path == "/testeanmeldung":
            self.wfile.write(bytes(load_input_html(), "utf-8"))
        elif self.path == "/testeanmeldung_err_redirect":
            sleep(60)
        elif self.path == "/error":
            self.wfile.write(bytes("<html><head><title>Test</title></head><body>", "utf-8"))
            self.wfile.write(bytes("<h1>Error</h1>", "utf-8")) # Real site is possibly more complex
            self.wfile.write(bytes("</body></html>", "utf-8"))


if __name__ == '__main__':
    print("Starting HTTP-Server")
    server = HTTPServer(('', PORT), MyServer)
    server.serve_forever()
