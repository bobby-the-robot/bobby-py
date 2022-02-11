from motion import Motion
from message_receiver import MessageReceiver
from image_sender import ImageSender

ImageSender()
motion_module = Motion()
MessageReceiver(motion_module)
