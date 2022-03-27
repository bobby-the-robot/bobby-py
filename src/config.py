import os


class Config:
    video_streaming_connection_url = os.getenv("VIDEO_STREAMING_CONNECTION_URL")
    video_streaming_destination = "/video"
    motion_control_connection_url = os.getenv("MOTION_CONTROL_CONNECTION_URL")
    motion_control_topic = "/motion"
