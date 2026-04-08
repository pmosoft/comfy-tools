import yt_dlp
import os

url = "https://www.youtube.com/shorts/RMXXnn1V4-4"

save_dir = r"d:\pycharm-projects\comfy-tools\media\video\youtube_download"
os.makedirs(save_dir, exist_ok=True)

ydl_opts = {
    'format': 'best',
    'outtmpl': os.path.join(save_dir, '%(title)s.%(ext)s')
}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download([url])