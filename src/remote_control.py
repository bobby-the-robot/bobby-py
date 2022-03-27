from websocket import create_connection
import stomper
import random


class RemoteControl:
    def connect(self, url, destination):
        return RemoteControlConnection(create_connection(url), destination)

    def subscribe(self, url, destination):
        connection = create_connection(url)
        connection_id = random.randint(1, 1000)
        connection.send(stomper.subscribe(destination, connection_id, ack="client"))
        return RemoteControlConnection(connection, destination)


class RemoteControlConnection:
    def __init__(self, connection, destination):
        self.connection = connection
        self.destination = destination

    def send(self, payload):
        self.connection.send(stomper.send(self.destination, payload))

    def apply_callback(self, callback):
        while True:
            message = self.connection.recv()
            callback(message)
