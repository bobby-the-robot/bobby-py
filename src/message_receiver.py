from pika import BlockingConnection
from pika import ConnectionParameters
from pika.credentials import PlainCredentials
from config import Config


class MessageReceiver:
    def __init__(self, motion_module):
        self.queue_name = "motion.control"
        self.motion_module = motion_module

    def callback(self, ch, method, properties, body):
        print(" [x] Received %r" % body)

    def init(self):
        credentials = PlainCredentials(Config.rabbit_user, Config.rabbit_password)
        connection = BlockingConnection(
            ConnectionParameters(Config.rabbit_host, Config.rabbit_port, Config.rabbit_user, credentials))
        channel = connection.channel()
        channel.basic_consume(queue=self.queue_name, auto_ack=True, on_message_callback=self.callback)
        print(' [*] Waiting for messages. To exit press CTRL+C')
        channel.start_consuming()
