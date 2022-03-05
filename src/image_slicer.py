import io
from picamera import PiCamera
from threading import Condition
from threading import Thread
import base64
from image_sender import ImageSender


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
        self.sender = ImageSender()
        thread1 = Thread(target=self.run)
        thread1.start()

    def run(self):
        output = StreamingOutput()
        self.camera.rotation = 180
        self.camera.start_recording(output, format='mjpeg')
        try:

            while True:
                with output.condition:
                    output.condition.wait()
                    print(output.frame)
                    self.sender.send(output.frame)
                    #print(output.frame)
                    #payload = 'aaa'
                    #try:
                    #    base64_data = base64.b64encode(output.frame)
                    #    payload = base64_data.decode('utf-8')
                    #    print(payload)
                    #    if payload:
                    #        self.ws.send(stomper.send("/client", payload))
                    #except Exception as e:
                    #    print("ERROR!!!!")
                    #    print(e)
                    #self.ws.send(stomper.send("/client", output.frame))
        finally:
            self.camera.stop_recording()
            self.camera.close()
