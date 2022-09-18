import threading
from gpiozero import Motor

right_forward_pin = 26
right_backward_pin = 12
left_forward_pin = 22
left_backward_pin = 23


class Motion:
    def __init__(self):
        self.is_locked = False
        self.right = Motor(right_forward_pin, right_backward_pin)
        self.left = Motor(left_forward_pin, left_backward_pin)

    def stop(self):
        print("stopping, unlocking")
        self.stop_motion()
        self.is_locked = False

    def move(self, direction):
        self.move_forward()
        if self.is_locked:
            print("can't move, locked")
            return
        print("Direction [%r] received" % direction)
        self.is_locked = True
        if direction == "FORWARD":
            print("moving fwd")
            self.move_forward()
        elif direction == "RIGHT":
            self.turn_right()
        elif direction == "LEFT":
            self.turn_left()
        elif direction == "BACK":
            self.move_backward()
        elif direction == "STOP":
            self.stop_motion()
        else:
            print("Direction [%r] not recognized" % direction)
        timer = threading.Timer(0.33, self.stop)
        timer.start()

    def move_forward(self):
        self.right.forward()
        self.left.forward()

    def turn_right(self):
        self.right.forward()
        self.left.backward()

    def turn_left(self):
        self.right.backward()
        self.left.forward()

    def move_backward(self):
        self.right.backward()
        self.left.backward()

    def stop_motion(self):
        self.right.stop()
        self.left.stop()
