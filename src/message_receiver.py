from config import Config
import threading


class MessageReceiver:
    def __init__(self, amqp_channel, motion_module):
        self.queue_name = Config.motion_control_queue
        self.motion_module = motion_module
        self.amqp_channel = amqp_channel
        threading.Thread(target=self.init()).start()

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
        self.amqp_channel.basic_consume(queue=self.queue_name, auto_ack=True, on_message_callback=self.callback)
        print('Motion module initialized')
        self.amqp_channel.start_consuming()
