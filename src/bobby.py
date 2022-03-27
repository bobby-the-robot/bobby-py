from motion import Motion
from message_receiver import MessageReceiver
from image_slicer import ImageSender
from remote_control import RemoteControl

from config import Config

remote_control = RemoteControl(Config.ws_connection_url)

ImageSender(remote_control)
MessageReceiver(remote_control, Motion())
