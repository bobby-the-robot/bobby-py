from motion import Motion
from message_receiver import MessageReceiver
from image_slicer import ImageSender
from remote_control import RemoteControl

remote_control = RemoteControl()

ImageSender(remote_control)
MessageReceiver(remote_control, Motion())
