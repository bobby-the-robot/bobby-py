from stomp import *
from config import Config


class ImageSender:
    def __init__(self):
        self.c = Connection([Config.streaming_connection_url])
        self.c.set_listener('', PrintingListener())
        #self.c.connect('admin', 'password', wait=True)
        self.c.connect(wait=True)
        self.c.subscribe('/client', "123")

    def send(self, message):
        self.c.send('/client', message)

