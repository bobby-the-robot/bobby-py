from motion import Motion
from message_receiver import MessageReceiver
from image_sender import ImageSender
from amqp_connection import ChannelFactory

amqp_channel_factory = ChannelFactory()

ImageSender()
MessageReceiver(amqp_channel_factory.get_channel(), Motion())
