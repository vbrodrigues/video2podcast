from pytube import YouTube


def get_video_title(url) -> str:
    yt = YouTube(url)
    return yt.title


def get_video_description(url) -> str:
    yt = YouTube(url)
    return yt.description


def download_audio(url, path):
    print('Downloading audio from YouTube video:', url)
    yt = YouTube(url)
    output_path = '/'.join(path.split('/')[:-1])
    filename = path.split('/')[-1]
    yt.streams.filter(only_audio=True).first().download(output_path, filename=filename)
    print('Audio saved on:', path)
    return yt.title

def download_video(url, path):
    yt = YouTube(url)
    yt.streams.filter(progressive=True).first().download(path)
    return yt.title