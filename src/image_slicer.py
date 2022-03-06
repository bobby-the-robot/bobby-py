import io
from picamera import PiCamera
from threading import Condition
from threading import Thread
import base64

from websocket import create_connection
import stomper
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
    def __init__(self):
        print("Initializing video streaming...")
        self.camera = PiCamera(resolution='640x480', framerate=10)
        #self.camera = PiCamera(resolution='120x80', framerate=24)
        thread1 = Thread(target=self.run)
        thread1.start()

    def run(self):
        output = StreamingOutput()
        self.camera.rotation = 180
        self.camera.start_recording(output, format='mjpeg')
        try:
            ws = create_connection(Config.streaming_connection_url)
            ws.send("CONNECT\naccept-version:1.0,1.1,2.0\n\n\x00\n")
            ws.send(stomper.subscribe("/client", "MyuniqueId1", ack="client"))
            print("subscribed to topic")
            while True:
                with output.condition:
                    print("awaiting for condition")
                    output.condition.wait()
                    print("converting payload to base64")
                    msg = base64.b64encode(output.frame).decode('ascii')
                    ws.send(stomper.send("/client", msg))
        finally:
            self.camera.stop_recording()
            self.camera.close()
