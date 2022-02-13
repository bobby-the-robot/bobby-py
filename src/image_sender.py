import io
from picamera import PiCamera
from threading import Condition
from config import Config
from datetime import datetime


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


class ImageSender:
    def __init__(self, amqp_channel):
        print("Initializing video streaming...")
        self.amqp_channel = amqp_channel
        self.camera = PiCamera(resolution='640x480', framerate=5)
        self.run()

    def run(self):
        output = StreamingOutput()
        self.camera.rotation = 180
        self.camera.start_recording(output, format='mjpeg')
        try:
            while True:
                with output.condition:
                    output.condition.wait()
                    now = datetime.now()

                    current_time = now.strftime("%H:%M:%S:%f")
                    print("Current Time =", current_time)
                    self.amqp_channel.basic_publish(
                        exchange='', routing_key=Config.video_streaming_queue, body=output.frame)
        finally:
            self.camera.stop_recording()
