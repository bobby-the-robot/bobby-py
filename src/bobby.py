from motion import Motion
from message_receiver import MessageReceiver
from image_slicer import ImageSender
from amqp_connection import ChannelFactory
from remote_control import RemoteControl

amqp_channel_factory = ChannelFactory()

ImageSender(RemoteControl())
MessageReceiver(amqp_channel_factory.get_channel(), Motion())
