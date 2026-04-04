import yt_dlp

#url = "https://www.youtube.com/shorts/xvkAEhflTCY"
#url = "https://www.youtube.com/shorts/PYb9RPAzNCs"
#url = "https://www.youtube.com/shorts/v7cqzdNCufE"
url = "https://www.youtube.com/shorts/4LCxyNPPs8s"




ydl_opts = {
    'format': 'best',
    'outtmpl': '%(title)s.%(ext)s'
}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download([url])