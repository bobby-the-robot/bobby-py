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
        if direction == "FORWARD":
            self.motion_module.move_forward()
        elif direction == "RIGHT":
            self.motion_module.turn_right()
        elif direction == "LEFT":
            self.motion_module.turn_left()
        elif direction == "BACK":
            self.motion_module.move_backward()
        elif direction == "STOP":
            self.motion_module.stop_motion()
        else:
            print("Direction [%r] not recognized" % direction)

    def init(self):
        self.remote_control_connection.apply_callback(self.callback)
