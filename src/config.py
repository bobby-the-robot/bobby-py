import os


class Config:
    rabbit_host = os.getenv("RABBIT_HOST")
    rabbit_port = os.getenv("RABBIT_PORT")
    rabbit_user = os.getenv("RABBIT_USER")
    rabbit_password = os.getenv("RABBIT_PASSWORD")
    streaming_connection_url = os.getenv("STREAMING_CONNECTION_URL")
    motion_control_queue = "motion.control"
