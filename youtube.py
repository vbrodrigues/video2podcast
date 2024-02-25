import os
from pytube import YouTube


class VideoHandler:

    def __init__(self, data_path: str):
        self.data_path = data_path
        self.__ensure_data_path_exists()

    def __ensure_data_path_exists(self):
        if not os.path.exists(self.data_path):
            os.makedirs(self.data_path)

    def get_video_title(self, url) -> str:
        yt = YouTube(url)
        return yt.title

    def get_video_description(self, url) -> str:
        yt = YouTube(url)
        return yt.description

    def download_audio(self, url, filename: str = 'audio.mp4') -> str:
        yt = YouTube(url)
        if not os.path.exists(os.path.join(self.data_path, filename)):
            print('Downloading audio...')
            yt.streams.filter(only_audio=True).first().download(self.data_path, filename=filename)
        print('Audio on:', self.data_path)
        return os.path.join(self.data_path, filename)

    def download_video(self, url):
        yt = YouTube(url)
        yt.streams.filter(progressive=True).first().download(self.data_path)
        return yt.title