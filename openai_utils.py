import logging

from openai import OpenAI

from config import *

logging.basicConfig(level=logging.INFO)


class OpenAIClient:
    def __init__(self, api_key):
        self.client = OpenAI(api_key=api_key)

    def generate_speech(self, text_input, voice, output_path):
        try:
            response = self.client.audio.speech.create(
                model=NARRATION_MODEL,
                voice=voice,
                input=text_input
            )
            response.stream_to_file(output_path)
        except Exception as e:
            logging.error(f"Failed to generate speech: {e}")
            raise

    def get_narration(self, image_url, prompt_file='prompt.md'):
        try:
            with open(prompt_file, 'r') as file:
                prompt_text = file.read()

            response = self.client.chat.completions.create(
                model=DESCRIPTION_MODEL,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt_text},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": image_url
                                },
                            },
                        ]
                    }
                ],
                max_tokens=MAX_TOKENS,
            )
            return response.choices[0].message.content
        except Exception as e:
            logging.error(f"Failed to get narration: {e}")
            raise
