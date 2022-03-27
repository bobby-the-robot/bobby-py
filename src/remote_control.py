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
        self.connection.send("CONNECT\naccept-version:1.0,1.1,2.0\n\n\x00\n")
        print(stomper.subscribe(destination, connection_id))
        self.connection.send(stomper.subscribe(destination, connection_id))
        return RemoteControlConnection(self.connection, destination)


class RemoteControlConnection:
    def __init__(self, connection, destination):
        self.connection = connection
        self.destination = destination

    def send(self, payload):
        self.connection.send(stomper.send(self.destination, payload))

    def apply_callback(self, callback):
        self.connection.send(stomper.subscribe(self.destination, 'aasd'))

        while True:
            print("before receive")
            message = self.connection.recv()
            print("after receive")
            print(message)
            #callback(message)
