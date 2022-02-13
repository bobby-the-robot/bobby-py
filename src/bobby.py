import asyncio
import threading
from motion import Motion
from message_receiver import MessageReceiver
from image_sender import ImageSender
from amqp_connection import ChannelFactory

amqp_channel_factory = ChannelFactory()


#def start_message_receiver():
#    MessageReceiver(amqp_channel_factory.get_channel(), Motion())

MessageReceiver(amqp_channel_factory.get_channel(), Motion())

#def start_image_sender():
#    ImageSender(amqp_channel_factory.get_channel())


#msg_thread = threading.Thread(target=start_message_receiver)
#streaming_thread = threading.Thread(target=start_image_sender)

#msg_thread.start()
#streaming_thread.start()

#msg_thread.join()
#streaming_thread.join()

#run forever
#loop = asyncio.get_event_loop()
#try:
#    loop.run_forever()
#finally:
#    loop.close()
