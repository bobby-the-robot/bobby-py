from gpiozero import Motor

right_forward_pin = 26
right_backward_pin = 12
left_forward_pin = 22
left_backward_pin = 23


class Motion:
    def __init__(self):
        self.right = Motor(26, 12)
        self.left = Motor(22, 23)

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
