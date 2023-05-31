import argparse
import os
from gpt import create_chat, extract_keypoints
from podcast import create_podcast
from transcription import openai_transcribe, transcribe_audio
from youtube import download_audio, get_video_description, get_video_title


AUDIO_OUTPUT_PATH='./data/audios/audio.mp4'
TRANSCRIPTION_OUTPUT_PATH='./data/transcriptions/audio.txt'
KEYPOINTS_OUTPUT_PATH='./data/keypoints/keypoints.txt'
CHAT_OUTPUT_PATH='./data/chats/chat.txt'
PODCAST_OUTPUT_PATH='./data/podcast/podcast.wav'


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Transform YouTube videos into a PodCast!')

    parser.add_argument('--url', type=str, help='URL of the YouTube video')
    parser.add_argument('--person1', type=str, help='Name of the first person')
    parser.add_argument('--person2', type=str, help='Name of the second person')
    parser.add_argument('--transcribe_method', choices=['openai', 'local'], default='openai')
    parser.add_argument('--skip_podcast', action='store_true')

    args = parser.parse_args()

    if args.url:
        video_title = get_video_title(args.url)
        video_description = get_video_description(args.url)
        context = video_title + ': ' + video_description if video_description is not None else video_title

        print('\n\n--- Video2PodCast ---:\n\n', context, '\n\n')

        if not os.path.exists(AUDIO_OUTPUT_PATH):
            download_audio(args.url, AUDIO_OUTPUT_PATH)
        
        if not os.path.exists(TRANSCRIPTION_OUTPUT_PATH):
            if args.transcribe_method == 'local':
                transcribe_audio(AUDIO_OUTPUT_PATH, initial_prompt=context, output_path=TRANSCRIPTION_OUTPUT_PATH)
            else:
                openai_transcribe(AUDIO_OUTPUT_PATH, initial_prompt=context, output_path=TRANSCRIPTION_OUTPUT_PATH)

        if not os.path.exists(KEYPOINTS_OUTPUT_PATH):
            extract_keypoints(TRANSCRIPTION_OUTPUT_PATH, context=context, output_path=KEYPOINTS_OUTPUT_PATH, max_tokens=2000)

        if not os.path.exists(CHAT_OUTPUT_PATH):
            create_chat(KEYPOINTS_OUTPUT_PATH, context=context, person1='Liz', person2='John', max_tokens=2000)

        if not args.skip_podcast:
            create_podcast(CHAT_OUTPUT_PATH, person1='Liz', person2='John')
