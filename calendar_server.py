import requests
import Event
import io
from flask import Flask, render_template
import base64

def get_calendar(cal_url):
    return requests.get(cal_url).text

def get_events(cal):
    return cal.split("BEGIN:VEVENT")

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index/index.html")

@app.route("/instruction")
def instruction():
    return render_template("index/instruction.html")

@app.route("/about")
def about():
    return render_template("index/about.html")

@app.route("/footer")
def footer():
    return render_template("index/footer.html")

# @app.route("/")
# def index():

@app.route("/cal/<b64>")
def submit(b64):
    decoded_url = base64.b64decode(b64).decode("utf-8")

    cal = get_calendar(decoded_url)
    for e in get_events(cal)[1:]:
        event = Event.Event(e)
        event.fix()
        cal = cal.replace(e, event.fixedEvent)

    return cal

if __name__ == "__main__":
    app.run(port=4343)