from typing import Union
import openai
import os


class Transcriber:

    def __init__(self, data_path: str, transcription_mode: Union['local' 'openai'] = 'local'):
        self.data_path = data_path
        self.__ensure_data_path_exists()
        self.transcription_mode = transcription_mode

    def __ensure_data_path_exists(self):
        if not os.path.exists(self.data_path):
            os.makedirs(self.data_path)

    def _openai_transcribe(self, audio_path: str, initial_prompt: str = None, filename: str = 'audio.txt') -> str:
        
        output_path = os.path.join(self.data_path, filename)
        if not os.path.exists(output_path):
            with open(audio_path, 'rb') as f:
                print('Transcribing audio with OpenAI API:', audio_path)
                client = openai.OpenAI()
                response = client.audio.transcriptions.create(
                    model='whisper-1',
                    file=f, 
                    prompt=initial_prompt,
                )

            transcription = response.text
            
            with open(output_path, 'w') as f:
                f.write(transcription)
        return output_path

    def transcribe(self, audio_path: str, initial_prompt: str = None, filename: str = 'audio.txt') -> str:
        return self._openai_transcribe(audio_path, initial_prompt, filename)
