import openai
import os
import subprocess
from dotenv import load_dotenv
from elevenlabs import client, save, Voice, VoiceSettings


class PodcastElevenlabs:

    def __init__(self, data_path: str):
        self.data_path = data_path
        self.__ensure_data_path_exists()

        self.FEMALE = Voice(
            voice_id="EXAVITQu4vr4xnSDxMaL",
            name="Bella",
            category="premade",
            settings=VoiceSettings(stability=0.245, similarity_boost=0.75),
        )

        self.MALE = Voice(
            voice_id="VR6AewLTigWG4xSOukaG",
            name="Arnold",
            category="premade",
            settings=VoiceSettings(stability=0.15, similarity_boost=0.75),
        )

    def __ensure_data_path_exists(self):
        if not os.path.exists(self.data_path):
            os.makedirs(self.data_path)

    def create_podcast(self, text_path: str, person1: str = 'Liz', person2: str = 'John', filename: str = 'podcast.wav') -> str:

        output_path = os.path.join(self.data_path, filename)

        if not os.path.exists(output_path):

            with open(text_path, 'r') as f:
                text = f.read()

            current_speaker = person1
            order = 0
            files_list = []
            for sample_text in text.split('\n'):

                if len(sample_text) > 1 and not sample_text.startswith('[') and not sample_text.startswith('Podcast'):

                    if not sample_text.startswith(person1) and not sample_text.startswith(person2):
                        current_speaker = person1 if current_speaker == person2 else person2

                    audio_path = self.data_path + f'/{order}-{current_speaker}.wav'
                    if not os.path.exists(audio_path):

                        print('Generating audio for:', current_speaker, 'Nº:', order)

                        speaker_text = sample_text.split(f'{current_speaker}:')[-1].strip()

                        el = client.ElevenLabs()
                        audio = el.generate(
                            text=speaker_text,
                            voice=self.FEMALE if current_speaker == person1 else self.MALE,
                            model="eleven_monolingual_v1"
                        )

                        save(audio, filename=audio_path)

                    current_speaker = person1 if current_speaker == person2 else person2
                    files_list.append(audio_path)
                    order += 1

            print('Merging audios into a podcast...')

            with open(self.data_path + '/audio_list.txt', 'w') as f:
                for file in files_list:
                    print(file)
                    f.write(f"file {file.split('/')[-1]}\n")
                    
            subprocess.run(f'ffmpeg -f concat -safe 0 -i {self.data_path}/audio_list.txt -c copy {output_path}', shell=True)
    
        return output_path



class PodcastOpenai:

    def __init__(self, data_path: str):
        self.data_path = data_path
        self.__ensure_data_path_exists()

    def __ensure_data_path_exists(self):
        if not os.path.exists(self.data_path):
            os.makedirs(self.data_path)

    def create_podcast(self, text_path: str, person1: str = 'Liz', person2: str = 'John', filename: str = 'podcast.wav') -> str:

        output_path = os.path.join(self.data_path, filename)

        if not os.path.exists(output_path):

            with open(text_path, 'r') as f:
                text = f.read()

            current_speaker = person1
            order = 0
            files_list = []
            for sample_text in text.split('\n'):

                if len(sample_text) > 1 and not sample_text.startswith('[') and not sample_text.startswith('Podcast'):

                    if not sample_text.startswith(person1) and not sample_text.startswith(person2):
                        current_speaker = person1 if current_speaker == person2 else person2

                    audio_path = self.data_path + f'/{order}-{current_speaker}.wav'
                    if not os.path.exists(audio_path):

                        print('Generating audio for:', current_speaker, 'Nº:', order)

                        speaker_text = sample_text.split(f'{current_speaker}:')[-1].strip()

                        client = openai.OpenAI()
                        with client.audio.speech.with_streaming_response.create(
                            model="tts-1",
                            voice="alloy",
                            input=speaker_text
                        ) as response:
                            response.stream_to_file(audio_path)

                    current_speaker = person1 if current_speaker == person2 else person2
                    files_list.append(audio_path)
                    order += 1

            print('Merging audios into a podcast...')

            with open(self.data_path + '/audio_list.txt', 'w') as f:
                for file in files_list:
                    print(file)
                    f.write(f"file {file.split('/')[-1]}\n")
                    
            subprocess.run(f'ffmpeg -f concat -safe 0 -i {self.data_path}/audio_list.txt -c copy {output_path}', shell=True)
    
        return output_path
