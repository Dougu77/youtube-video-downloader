import os
import time
import threading
from flask import Flask, render_template, request, send_file
import yt_dlp

app = Flask(__name__)

# Define the download folder
def get_download_folder():
    base_folder = os.path.dirname(os.path.abspath(__file__))
    download_folder = os.path.join(base_folder, 'downloads')
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)
    return download_folder

# Clean the files periodically
def clean_downloads_folder():
    download_folder = get_download_folder()
    while True:
        time.sleep(90)  # 10 minutes
        
        try:
            for filename in os.listdir(download_folder):
                file_path = os.path.join(download_folder, filename)
                if os.path.isfile(file_path):
                    os.remove(file_path)
                    print(f'Arquivo removido: {file_path}')
        except Exception as e:
            print(f'Erro ao limpar a pasta de downloads: {e}')

# Download the video
def download_video(url):
    download_folder = get_download_folder()
    ydl_opts = {
        'outtmpl': os.path.join(download_folder, '%(title)s.%(ext)s'),
        'format': 'best',
        'quiet': True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info_dict)
        return filename

# Begin the clean thread
def start_cleanup_thread():
    cleanup_thread = threading.Thread(target=clean_downloads_folder)
    cleanup_thread.daemon = True
    cleanup_thread.start()

# Home route
@app.route('/')
def index():
    return render_template('index.html')

# Download route
@app.route('/download', methods=['POST'])
def download():
    url = request.form['url']
    
    if not url:
        return 'Por favor, forneça uma URL válida.'
    
    try:
        video_file = download_video(url)
        return send_file(video_file, as_attachment=True)
    except Exception as e:
        return f'Erro ao baixar o vídeo: {str(e)}'

# Main
if __name__ == '__main__':
    start_cleanup_thread()
    # app.run(debug=True)
