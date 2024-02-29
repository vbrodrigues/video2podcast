import os
from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel

from youtube import VideoHandler
from transcription import Transcriber
from chat import Chat
from podcast import Podcast
from google.cloud.storage import Client as StorageClient


app = FastAPI()


class RequestDTO(BaseModel):
    video_url: str
    user_id: str
    video_id: str
    person1: str
    person2: str
    skip_podcast: bool


class ResponseDTO(BaseModel):
    success: bool
    message: Optional[str]


AUDIO_OUTPUT_PATH='./data/audios'
TRANSCRIPTION_OUTPUT_PATH='./data/transcriptions'
CHAT_OUTPUT_PATH='./data/chats'
PODCAST_OUTPUT_PATH='./data/podcast'


def remove_special_chars(text: str) -> str:
    return ''.join(e for e in text if e.isalnum() or e.isspace())


@app.post('/video2podcast')
def video2podcast(request: RequestDTO) -> ResponseDTO:
    try:

        audio_path = None
        transcription_path = None
        keypoints_path = None
        chat_path = None
        podcast_path = None

        # TODO: Checar se video_id está PENDING no Firestore

        if request.video_url:
            video_handler = VideoHandler(AUDIO_OUTPUT_PATH)
            transcriber = Transcriber(TRANSCRIPTION_OUTPUT_PATH, transcription_mode='openai')
            chat = Chat(CHAT_OUTPUT_PATH)
            podcast = Podcast(PODCAST_OUTPUT_PATH)

            video_title = video_handler.get_video_title(request.video_url)
            video_description = video_handler.get_video_description(request.video_url)
            context = video_title + ': ' + video_description if video_description is not None else video_title

            print('\n\n--- Video2PodCast ---:\n\n', context, '\n\n')

            # TODO: Manter tudo in memory sem precisar salvar no disco

            audio_path = video_handler.download_audio(request.video_url, filename='_'.join(remove_special_chars(video_title).split(' ')) + '.mp4')
            transcription_path = transcriber.transcribe(audio_path, initial_prompt=context, filename='_'.join(remove_special_chars(video_title).split(' ')) + '.txt')
            keypoints_path = chat.extract_keypoints(transcription_path, context=context, max_tokens=2000, filename='keypoints_' + '_'.join(remove_special_chars(video_title).split(' ')) + '.txt')
            chat_path = chat.create_chat(keypoints_path, context=context, person1=request.person1, person2=request.person2, max_tokens=2000, filename='chat_' + '_'.join(remove_special_chars(video_title).split(' ')) + '.txt')

            if not request.skip_podcast:
                podcast_path = podcast.create_podcast(chat_path, person1=request.person1, person2=request.person2)

            print('Podcast created!')
            print('Full chat: \n')
            with open(chat_path, 'r') as f:
                print(f.read())

            if not request.skip_podcast:
                storage_client = StorageClient()
                bucket = storage_client.get_bucket('video2podcast')
                blob = bucket.blob(f'{request.video_id}_{request.user_id}.wav')
                blob.upload_from_filename(podcast_path)
                print('Podcast uploaded to GCS!', f'{request.video_id}_{request.user_id}.wav')

            # TODO: Atualizar video_id para DONE no Firestore e salvar path do áudio
        return ResponseDTO(success=True, message='Podcast created!')
    except Exception as e:
        return ResponseDTO(success=False, message=str(e))
    finally:
        if audio_path and os.path.exists(audio_path):
            os.remove(audio_path)
        if transcription_path and os.path.exists(transcription_path):
            os.remove(transcription_path)
        if keypoints_path and os.path.exists(keypoints_path):
            os.remove(keypoints_path)
        if chat_path and os.path.exists(chat_path):
            os.remove(chat_path)
        if podcast_path and os.path.exists(podcast_path):
            os.remove(podcast_path)
        print('Files removed!')
