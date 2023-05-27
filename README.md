# video2podcast

This repository contains Python code to generate an audio file with a conversation between two AI models, discussing the subject of a given YouTube video URL. The `main.py` script is used to run the program.

## Requirements

- Python 3.6 or higher
- Internet connection
- Required Python packages: `pytube`, `openai-whisper`, `tiktoken`, `openai`, `elevenlabs`

You can install the required packages by running the following command:

```shell
pip install -r requirements.txt
```

## Usage

To generate an audio file with a conversation between two AI models based on a YouTube video, follow the steps below:

1. Clone the repository or download the code.

2. Install the required packages as mentioned in the "Requirements" section.

3. Open a terminal or command prompt and navigate to the project directory.

4. Run the following command:

```shell
python main.py --url <youtube_url>
```

Replace <youtube_url> with the URL of the YouTube video you want to generate a conversation about.

5. Wait for the program to process the video. It will download the video using pytube, transcribe the audio, and generate a conversation between the AIs.

6. Once the process is complete, the program will save the generated audio file as podcast.wav in `./data/podcast/podcast.wav`.

## Example

Here's an example command to generate a conversation based on a YouTube video:

```shell
python main.py --url https://www.youtube.com/watch?v=DrxiNfbr63s
```

This command will generate a conversation audio file based on the YouTube video with the given URL.

## Notes

- The program uses AI models to generate the conversation, and the quality of the generated audio file may vary depending on the models and their training data.

- The program requires an internet connection to download the YouTube video and access the AI models.

- Depending on the length and complexity of the video, the processing time may vary. Please be patient while the program completes its tasks.

- The generated audio file will be saved as podcast.wav in the `./data/podcast/podcast.wav`. You can modify the code to change the filename and format if desired.
