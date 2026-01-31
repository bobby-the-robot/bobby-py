import base64
from threading import Thread

import cv2
from picamera2 import Picamera2

from config import Config


class ImageSender:
    def __init__(self, remote_control):
        print("Initializing video streaming (picamera2)...")
        self.remote_control = remote_control

        self.camera = Picamera2()

        config = self.camera.create_video_configuration(
            main={"size": (240, 160), "format": "RGB888"}
        )
        self.camera.configure(config)

        # Limit FPS to ~10
        self.camera.set_controls({"FrameDurationLimits": (100000, 100000)})

        self.camera.start()

        Thread(target=self.run, daemon=True).start()

    def run(self):
        remote_connection = self.remote_control.connect(Config.video_streaming_endpoint)

        try:
            while True:
                frame = self.camera.capture_array()  # RGB ndarray

                # Rotate 180 degrees (same as flip both axes). Remove if not needed.
                frame = cv2.flip(frame, -1)

                ok, jpg = cv2.imencode(".jpg", frame, [int(cv2.IMWRITE_JPEG_QUALITY), 70])
                if not ok:
                    continue

                msg = base64.b64encode(jpg.tobytes()).decode("ascii")
                remote_connection.send(msg)

        finally:
            self.camera.stop()
            self.camera.close()
