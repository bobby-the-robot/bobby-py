from websocket import create_connection
import stomper
import random


class RemoteControl:
    def __init__(self, url):
        self.connection = create_connection(url)

    def connect(self, destination):
        return RemoteControlConnection(self.connection, destination)

    def subscribe(self, destination):
        connection_id = random.randint(1, 1000)
        self.connection.send(stomper.subscribe(destination, connection_id, ack="client"))
        return RemoteControlConnection(self.connection, destination)


class RemoteControlConnection:
    def __init__(self, connection, destination):
        self.connection = connection
        self.destination = destination

    def send(self, payload):
        self.connection.send(stomper.send(self.destination, payload))

    def apply_callback(self, callback):
        while True:
            print("test!")
            message = self.connection.recv()
            callback(message)
