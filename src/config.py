import os


class Config:
    ws_connection_url = os.getenv("WS_CONNECTION_URL")
    video_streaming_endpoint = "/video"
    motion_control_topic = "/topic/motion"
