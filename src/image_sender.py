from websocket import create_connection
import stomper
from config import Config


class ImageSender:
    def __init__(self):
        self.ws = create_connection(Config.streaming_connection_url)
        self.ws.send("CONNECT\naccept-version:1.0,1.1,2.0\n\n\x00\n")
        self.ws.send(stomper.subscribe("/client", "MyuniqueId", ack="auto"))
        self.ws.send(stomper.send("/client", "Hello there1"))
        self.ws.send(stomper.send("/client", "Hello there2"))
        self.ws.send(stomper.send("/client", "Hello there3"))

    def send(self, message):
        self.ws.send(stomper.send("/client", message))
