import asyncio
from motion import Motion
from message_receiver import MessageReceiver
from image_sender import ImageSender
from amqp_connection import ChannelFactory

amqp_channel_factory = ChannelFactory()
ampq_channel = amqp_channel_factory.get_channel()

#MessageReceiver(ampq_channel, Motion())

print("Start image sender")

ImageSender(ampq_channel) #check if it blocks anything

print("Bingo!")

#run forever
loop = asyncio.get_event_loop()
try:
    loop.run_forever()
finally:
    loop.close()
