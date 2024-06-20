import sys

from config import Voice
from video_processor import VideoProcessor

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script.py <input_video_file_path> [<voice_choice>]")
        sys.exit(1)

    input_video_file_path = sys.argv[1]
    voice_choice = sys.argv[2].lower() if len(sys.argv) > 2 else "alloy"

    # Validate voice choice against enum values
    if voice_choice not in [v.value for v in Voice]:
        print(f"Invalid voice: {voice_choice}. Please choose from 'alloy', 'echo', 'fable', 'onyx', 'nova', 'shimmer'.")
        sys.exit(1)

    # Convert string voice choice to enum member
    voice_enum = Voice[voice_choice.upper()]

    video_processor = VideoProcessor(input_video_file_path, voice=voice_enum)
    try:
        output_narrated_video_file_path = video_processor.process_video()
        print(f"Narrated video saved to {output_narrated_video_file_path}")
    except Exception as e:
        print(f"Error processing video: {e}")
