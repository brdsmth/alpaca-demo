import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """environment variables"""

    APCA_API_KEY_ID = os.getenv("APCA_API_KEY_ID")
    APCA_API_SECRET_KEY = os.getenv("APCA_API_SECRET_KEY")
    GMAIL_SMTP_PASSWORD = os.getenv("GMAIL_SMTP_PASSWORD")
    DEBUG = os.getenv("DEBUG")
