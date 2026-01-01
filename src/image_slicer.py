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

        # Create a small, low-res stream for speed (240x160 @ ~10fps)
        config = self.camera.create_video_configuration(
            main={"size": (240, 160), "format": "RGB888"}
        )
        self.camera.configure(config)

        # 180° rotation: easiest is flip both axes
        # (equivalent to rotate 180)
        try:
            self.camera.set_controls({"ScalerCrop": self.camera.camera_controls.get("ScalerCrop")})
        except Exception:
            pass  # harmless if not supported / not needed

        # Limit frame rate (microseconds per frame)
        # 10 fps => 100000 us per frame
        self.camera.set_controls({"FrameDurationLimits": (100000, 100000)})

        self.camera.start()

        new_thread = Thread(target=self.run, daemon=True)
        new_thread.start()

    def run(self):
        remote_connection = self.remote_control.connect(Config.video_streaming_endpoint)

        try:
            while True:
                # Capture a frame as a numpy array (RGB)
                frame = self.camera.capture_array()

                # Rotate 180° (flip both axes). If you don't need rotation, remove this.
                frame = cv2.flip(frame, -1)

                # Encode to JPEG bytes
                ok, jpg = cv2.imencode(".jpg", frame, [int(cv2.IMWRITE_JPEG_QUALITY), 70])
                if not ok:
                    continue

                msg = base64.b64encode(jpg.tobytes()).decode("ascii")
                remote_connection.send(msg)

        finally:
            self.camera.stop()
            self.camera.close()
