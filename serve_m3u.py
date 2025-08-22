from flask import Flask, send_file
import os

app = Flask(__name__)

@app.route("/")
def index():
    return "Serwer działa! Plik M3U dostępny pod /playlist.m3u"

@app.route("/playlist.m3u")
def playlist():
    if os.path.exists("KanałyTV.m3u"):
        return send_file("KanałyTV.m3u", mimetype="audio/x-mpegurl")
    return "#EXTM3U\n"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
