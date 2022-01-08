import time
from motion import Motion

motion_module = Motion()

motion_module.move_forward()
time.sleep(5)
motion_module.stop_motion()
