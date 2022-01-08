import time
from gpiozero import Motor

right = Motor(26, 12)
left = Motor(22,23)
right.forward()
left.forward()
time.sleep(5)
