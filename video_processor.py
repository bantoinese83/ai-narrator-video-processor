import logging
from pathlib import Path

import cv2
import numpy as np
from PIL import Image
from moviepy.editor import VideoFileClip, AudioFileClip

from config import *
from openai_utils import OpenAIClient
from s3_utils import S3Client

logging.basicConfig(level=logging.INFO)


class VideoProcessor:
    def __init__(self, video_file_path, voice=Voice.ALLOY):
        self.video_file_path = video_file_path
        self.voice = voice
        self.openai_client = OpenAIClient(api_key=OPENAI_API_KEY)
        self.s3_client = S3Client(S3_BUCKET_NAME, AWS_ACCESS_KEY, AWS_SECRET_KEY)
        self.frames = []
        project_root = Path(__file__).parent
        output_folder = project_root / 'output_folder'
        output_folder.mkdir(exist_ok=True)
        self.speech_file_path = output_folder / SPEECH_FILE_NAME
        self.collage_image_path = output_folder / COLLAGE_IMAGE_NAME

    def extract_frames(self, frame_rate=DEFAULT_FRAME_RATE):
        video_capture = cv2.VideoCapture(self.video_file_path)
        frame_count = 0
        while video_capture.isOpened():
            ret, frame = video_capture.read()
            if not ret:
                break
            if frame_count % frame_rate == 0:
                self.frames.append(frame)
            frame_count += 1
        video_capture.release()

    def create_collage(self, rows=DEFAULT_ROWS, cols=DEFAULT_COLS):
        frame_height, frame_width, _ = self.frames[0].shape
        collage = np.zeros((frame_height * rows, frame_width * cols, 3), dtype=np.uint8)
        for i in range(rows):
            for j in range(cols):
                if i * cols + j < len(self.frames):
                    collage[i * frame_height: (i + 1) * frame_height, j * frame_width: (j + 1) * frame_width] = \
                        self.frames[i * cols + j]
        Image.fromarray(collage).save(self.collage_image_path)

    def generate_narration(self, text_input):
        try:
            self.openai_client.generate_speech(text_input, self.voice.value, self.speech_file_path)
        except Exception as e:
            logging.error(f"Failed to generate narration: {e}")
            raise

    def get_video_narration(self):
        self.extract_frames()
        self.create_collage()
        s3_file_name = self.collage_image_path.name
        self.s3_client.upload_file(str(self.collage_image_path), s3_file_name)
        url = self.s3_client.generate_presigned_url(s3_file_name)

        try:
            narration_text = self.openai_client.get_narration(url)
            self.generate_narration(narration_text)
        except Exception as e:
            logging.error(f"Failed to get video narration: {e}")
            raise

    def add_narration_to_video(self):
        try:
            video_clip = VideoFileClip(self.video_file_path)
            narration_audio = AudioFileClip(str(self.speech_file_path))
            final_clip = video_clip.set_audio(narration_audio)
            output_folder = Path(__file__).parent / 'narrated_folder'
            output_folder.mkdir(exist_ok=True)
            output_file_path = output_folder / Path(self.video_file_path).with_suffix('.narrated.mp4').name
            final_clip.write_videofile(str(output_file_path), codec=VIDEO_CODEC, audio_codec=AUDIO_CODEC)
            return output_file_path
        except Exception as error:
            logging.error(f"Failed to add narration to video: {error}")
            raise

    def process_video(self):
        try:
            self.get_video_narration()
            narrated_video_file_path = self.add_narration_to_video()
            return narrated_video_file_path
        except Exception as e:
            logging.error(f"Failed to process video: {e}")
            raise
