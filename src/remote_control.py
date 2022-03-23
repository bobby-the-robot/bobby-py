from websocket import create_connection
import stomper


class RemoteControl:
    def connect(self, url, destination):
        return RemoteControlConnection(create_connection(url), destination)


class RemoteControlConnection:
    def __init__(self, connection, destination):
        self.connection = connection
        self.destination = destination

    def send(self, payload):
        self.connection.send(stomper.send(self.destination, payload))
