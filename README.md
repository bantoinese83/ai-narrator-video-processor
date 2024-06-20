# AI Narrator Video Processor

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Dependencies](#dependencies)
- [Usage](#usage)


## Overview
AI Narrator Video Processor is a tool that takes a video file, extracts frames, creates a collage, generates a narration in the style using OpenAI's API, and then combines the narration with the original video. The generated narration describes the events in the video collage.

## Features
- Extract frames from a video file.
- Create a collage from extracted frames.
- Upload the collage to AWS S3.
- Use OpenAI API to generate a narration in a storytelling style.
- Combine the generated narration with the original video.

## Installation
### Prerequisites
- Python 3.8 or higher
- AWS credentials with S3 access
- OpenAI API key

### Setup
1. Clone the repository:
    ```sh
    git clone https://github.com/bantoinese83/ai-narrator-video-processor.git
    cd ai_narrator
    ```

2. Create and activate a virtual environment:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

4. Configure your AWS and OpenAI credentials (see [Configuration](#configuration) below).

- AWS_ACCESS_KEY = 'your-aws-access-key'
- AWS_SECRET_KEY = 'your-aws-secret-key'
- S3_BUCKET_NAME = 'your-s3-bucket-name'
- OPENAI_API_KEY = 'your-openai-api-key'


# Dependencies
-  OpenCV
-   NumPy
-   Pillow
-   MoviePy
-   OpenAI Python client
-   Boto3 (AWS SDK for Python)

## Usage
To run the video processor:
```sh
python main.py <input_video_file_path> [<voice_choice>]
