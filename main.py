import argparse
import os
from gpt import create_chat, extract_keypoints
from podcast import create_podcast
from transcription import transcribe_audio
from youtube import download_audio, get_video_description, get_video_title


AUDIO_OUTPUT_PATH='./data/audios/audio.mp4'
TRANSCRIPTION_OUTPUT_PATH='./data/transcriptions/audio.txt'
KEYPOINTS_OUTPUT_PATH='./data/keypoints/keypoints.txt'
CHAT_OUTPUT_PATH='./data/chats/chat.txt'
PODCAST_OUTPUT_PATH='./data/podcast/podcast.wav'


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Transform YouTube videos into a PodCast!')

    parser.add_argument('--url', type=str, help='URL of the YouTube video')

    args = parser.parse_args()

    if args.url:
        video_title = get_video_title(args.url)
        video_description = get_video_description(args.url)
        context = video_title + ': ' + video_description if video_description is not None else video_title

        print('\n\n--- Video2PodCast ---:\n\n', context)

        if os.path.exists(AUDIO_OUTPUT_PATH) is False:
            download_audio(args.url, AUDIO_OUTPUT_PATH)
        
        if os.path.exists(TRANSCRIPTION_OUTPUT_PATH) is False:
            transcribe_audio(AUDIO_OUTPUT_PATH, initial_prompt=context, output_path=TRANSCRIPTION_OUTPUT_PATH)

        if os.path.exists(KEYPOINTS_OUTPUT_PATH) is False:
            extract_keypoints(TRANSCRIPTION_OUTPUT_PATH, context=context, output_path=KEYPOINTS_OUTPUT_PATH, max_tokens=1000)

        if os.path.exists(CHAT_OUTPUT_PATH) is False:
            create_chat(KEYPOINTS_OUTPUT_PATH, context=context, person1='Liz', person2='John', max_tokens=1000)

        create_podcast(CHAT_OUTPUT_PATH, person1='Liz', person2='John')
