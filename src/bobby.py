from gpiozero import Robot


bobby = Robot(left=(3,4), right=(25,26))
bobby.forward()
