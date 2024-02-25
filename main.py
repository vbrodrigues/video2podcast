import argparse
from chat import Chat
from podcast import Podcast
from transcription import Transcriber
from youtube import VideoHandler


AUDIO_OUTPUT_PATH='./data/audios'
TRANSCRIPTION_OUTPUT_PATH='./data/transcriptions'
CHAT_OUTPUT_PATH='./data/chats'
PODCAST_OUTPUT_PATH='./data/podcast'


def remove_special_chars(text: str) -> str:
    return ''.join(e for e in text if e.isalnum() or e.isspace())


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Transform YouTube videos into a PodCast!')

    parser.add_argument('--url', type=str, help='URL of the YouTube video')
    parser.add_argument('--person1', type=str, help='Name of the first person')
    parser.add_argument('--person2', type=str, help='Name of the second person')
    parser.add_argument('--transcribe_method', choices=['openai', 'local'], default='openai')
    parser.add_argument('--skip_podcast', action='store_true')

    args = parser.parse_args()

    if args.url:

        video_handler = VideoHandler(AUDIO_OUTPUT_PATH)
        transcriber = Transcriber(TRANSCRIPTION_OUTPUT_PATH, transcription_mode=args.transcribe_method)
        chat = Chat(CHAT_OUTPUT_PATH)
        podcast = Podcast(PODCAST_OUTPUT_PATH)

        video_title = video_handler.get_video_title(args.url)
        video_description = video_handler.get_video_description(args.url)
        context = video_title + ': ' + video_description if video_description is not None else video_title

        print('\n\n--- Video2PodCast ---:\n\n', context, '\n\n')

        audio_path = video_handler.download_audio(args.url, filename='_'.join(remove_special_chars(video_title).split(' ')) + '.mp4')
        transcription_path = transcriber.transcribe(audio_path, initial_prompt=context, filename='_'.join(remove_special_chars(video_title).split(' ')) + '.txt')
        keypoints_path = chat.extract_keypoints(transcription_path, context=context, max_tokens=2000, filename='keypoints_' + '_'.join(remove_special_chars(video_title).split(' ')) + '.txt')
        chat_path = chat.create_chat(keypoints_path, context=context, person1='Liz', person2='John', max_tokens=2000, filename='chat_' + '_'.join(remove_special_chars(video_title).split(' ')) + '.txt')

        if not args.skip_podcast:
            podcast.create_podcast(chat_path, person1='Liz', person2='John')
