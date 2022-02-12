from pika import BlockingConnection
from pika import ConnectionParameters
from pika.credentials import PlainCredentials
from config import Config


class ChannelFactory:
    def __init__(self):
        self.credentials = PlainCredentials(Config.rabbit_user, Config.rabbit_password)

    def get_channel(self):
        connection = BlockingConnection(
            ConnectionParameters(Config.rabbit_host, Config.rabbit_port, Config.rabbit_user, self.credentials))
        return connection.channel()
