import os
from enum import Enum

DEFAULT_FRAME_RATE = 1
DEFAULT_ROWS = 5
DEFAULT_COLS = 5
COLLAGE_IMAGE_NAME = "collage.jpg"
SPEECH_FILE_NAME = "speech.mp3"
VIDEO_CODEC = 'libx264'
AUDIO_CODEC = 'aac'
NARRATION_MODEL = "tts-1"
DESCRIPTION_MODEL = "gpt-4o"
MAX_TOKENS = 300
S3_BUCKET_NAME = 'video-api-bucket'

# Load API keys from environment variables or a secrets manager
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
AWS_ACCESS_KEY = os.getenv('AWS_ACCESS_KEY', '')
AWS_SECRET_KEY = os.getenv('AWS_SECRET_KEY', '')


class Voice(Enum):
    ALLOY = "alloy"
    ECHO = "echo"
    FABLE = "fable"
    ONYX = "onyx"
    NOVA = "nova"
    SHIMMER = "shimmer"
