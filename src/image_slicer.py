import io
from picamera import PiCamera
from threading import Condition
from threading import Thread
import base64

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


class ImageSender:
    def __init__(self, remote_control):
        print("Initializing video streaming...")
        self.camera = PiCamera(resolution='240x160', framerate=10)
        self.remote_control = remote_control
        new_thread = Thread(target=self.run)
        new_thread.start()

    def run(self):
        output = StreamingOutput()
        self.camera.rotation = 180
        self.camera.start_recording(output, format='mjpeg')
        try:
            connection_url = Config.video_streaming_connection_url
            destination = Config.video_streaming_destination
            remote_connection = self.remote_control.connect(connection_url, destination)
            while True:
                with output.condition:
                    output.condition.wait()
                    msg = base64.b64encode(output.frame).decode('ascii')
                    remote_connection.send(msg)
        finally:
            self.camera.stop_recording()
            self.camera.close()
