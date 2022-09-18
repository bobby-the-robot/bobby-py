from config import Config
from threading import Thread


class MessageReceiver:
    def __init__(self, remote_control, motion_module):
        print("Initializing message receiver...")
        self.remote_control_connection = remote_control.subscribe(Config.motion_control_topic)
        self.motion_module = motion_module
        new_thread = Thread(target=self.init)
        new_thread.start()

    def callback(self, direction):
        print("Direction [%r] received" % direction)
        self.motion_module.move(direction)

    def init(self):
        self.remote_control_connection.apply_callback(self.callback)
