from yt_dlp import YoutubeDL

url = 'https://youtu.be/vBDzOP4e38g?si=0OPZtyC1VfKVCG1r'

params = {
    'quiet': True,
    'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best'
}

YoutubeDL(params).download(url)
