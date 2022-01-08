from pika import BlockingConnection
from pika import ConnectionParameters
from pika.credentials import PlainCredentials
from config import Config


class MessageReceiver:
    def __init__(self, motion_module):
        self.queue_name = "motion.control"
        self.motion_module = motion_module
        self.init()

    def callback(self, ch, method, properties, body):
        command = body.decode('utf-8')
        print("Command [%r] received" % command)
        if command == "FORWARD":
            self.motion_module.move_forward()
        elif command == "RIGHT":
            self.motion_module.turn_right()
        elif command == "LEFT":
            self.motion_module.turn_left()
        elif command == "BACK":
            self.motion_module.move_backward()
        elif command == "STOP":
            self.motion_module.stop_motion()
        else:
            print("Command [%r] not recognized" % command)

    def init(self):
        credentials = PlainCredentials(Config.rabbit_user, Config.rabbit_password)
        connection = BlockingConnection(
            ConnectionParameters(Config.rabbit_host, Config.rabbit_port, Config.rabbit_user, credentials))
        channel = connection.channel()
        channel.basic_consume(queue=self.queue_name, auto_ack=True, on_message_callback=self.callback)
        print('Motion module initialized')
        channel.start_consuming()
