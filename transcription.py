import whisper


def transcribe_audio(audio_path, initial_prompt: str = None, output_path: str = None):
    print('Transcribing audio:', audio_path)
    model = whisper.load_model('base')
    result = model.transcribe('data/audios/audio.mp4', initial_prompt=initial_prompt, verbose=True)

    output_path = output_path if output_path is not None else 'data/transcriptions/audio.txt'
    with open(output_path, 'w') as f:
        f.write(result['text'])