from flask import Flask, request
import requests, time

app = Flask(__name__)

@app.route("/")
def hello_world():
    time.sleep(1)
    return "<p>Hello, World!</p>"




# flask --app flask_server run --host=10.11.11.152
# demo-websocket.tuxae.fr
