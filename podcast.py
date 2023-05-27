import os
from elevenlabs import generate, save, set_api_key
import subprocess


set_api_key("")


def create_podcast(text_path: str, person1: str = 'Liz', person2: str = 'John', output_path: str = None) -> str:

    with open(text_path, 'r') as f:
        text = f.read()

    output_path = output_path if output_path is not None else 'data/podcast/podcast.wav'
    base_output_path = '/'.join(output_path.split('/')[:-1])

    current_speaker = person1
    order = 0
    files_list = []
    for sample_text in text.split('\n'):

        if len(sample_text) > 1:
            audio_path = base_output_path + f'/{order}-{current_speaker}.wav'
            if not os.path.exists(audio_path):

                print('Generating audio for:', current_speaker, 'Nº:', order)

                speaker_text = sample_text.split(f'{current_speaker}:')[-1].strip()

                audio = generate(
                    text=speaker_text,
                    voice="Bella" if current_speaker == person1 else "Arnold",
                    model="eleven_monolingual_v1"
                )

                save(audio, filename=audio_path)

            current_speaker = person1 if current_speaker == person2 else person2
            files_list.append(audio_path)
            order += 1

    print('Merging audios into a podcast...')

    with open(base_output_path + '/audio_list.txt', 'w') as f:
        for file in files_list:
            print(file)
            f.write(f"file {file.split('/')[-1]}\n")
            
    subprocess.run(f'ffmpeg -f concat -safe 0 -i {base_output_path}/audio_list.txt -c copy {output_path}', shell=True)
