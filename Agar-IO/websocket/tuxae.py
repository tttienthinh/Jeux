"""
import asyncio
from websockets.sync.client import connect

def hello():
    with connect("ws://demo-websocket.tuxae.fr:80") as websocket:
        websocket.send("Hello world!")
        message = websocket.recv()
        print(f"Received: {message}")

hello()
"""
import asyncio
from websockets.sync.client import connect

def hello():
    with connect("wss://demo-websocket.tuxae.fr:443") as websocket:
        websocket.send("Hello world!")
        message = websocket.recv()
        print(f"Received: {message}")

hello()