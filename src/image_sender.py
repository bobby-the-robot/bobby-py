import io
import picamera
from threading import Condition

from pika import BlockingConnection
from pika import ConnectionParameters
from pika.credentials import PlainCredentials
from config import Config


class StreamingOutput(object):
    def __init__(self):
        self.frame = None
        self.buffer = io.BytesIO()
        self.condition = Condition()

    def write(self, buf):
        if buf.startswith(b'\xff\xd8'):
            # New frame, copy the existing buffer's content and notify all
            # clients it's available
            self.buffer.truncate()
            with self.condition:
                self.frame = self.buffer.getvalue()
                self.condition.notify_all()
            self.buffer.seek(0)
        return self.buffer.write(buf)


with picamera.PiCamera(resolution='640x480', framerate=24) as camera:
    credentials = PlainCredentials(Config.rabbit_user, Config.rabbit_password)
    connection = BlockingConnection(
        ConnectionParameters(Config.rabbit_host, Config.rabbit_port, Config.rabbit_user, credentials))
    channel = connection.channel()
    #channel.exchange_declare(exchange='video.frames', exchange_type='fanout')
    channel.queue_declare(queue='video.frames')
    output = StreamingOutput()
    #Uncomment the next line to change your Pi's Camera rotation (in degrees)
    #camera.rotation = 90
    camera.start_recording(output, format='mjpeg')
    try:
        while True:
            with output.condition:
                output.condition.wait()
                frame = output.frame
                channel.basic_publish(exchange='', routing_key='video.frames', body=frame)
                print("sent an image")
    finally:
        camera.stop_recording()
