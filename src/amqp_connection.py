from pika import BlockingConnection
from pika import ConnectionParameters
from pika.credentials import PlainCredentials
from config import Config


class ChannelFactory:
    def __init__(self):
        credentials = PlainCredentials(Config.rabbit_user, Config.rabbit_password)
        connection = BlockingConnection(
            ConnectionParameters(Config.rabbit_host, Config.rabbit_port, Config.rabbit_user, credentials))
        self.channel = connection.channel()

    def get_channel(self):
        return self.channel
