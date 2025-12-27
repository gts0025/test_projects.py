
url = "https://www.youtube.com/watch?v=tyKu0uZS86Q&t=2s"
from pytube import YouTube
yt = YouTube(url)

audio = yt.streams.filter(only_audio=True).first()
audio.download()