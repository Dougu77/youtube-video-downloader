from flask import Flask, render_template, request, send_file
import yt_dlp
import os

app = Flask(__name__)

# Download the video using yt_dlp
def download_video(url):
    
    # Defenition of the download folder
    base_dir = os.path.dirname(os.path.abspath(__file__))
    download_dir = os.path.join(base_dir, 'downloads')
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)
    
    # Defenition of yt_dlp options
    ydl_opts = {
        'outtmpl': os.path.join(download_dir, '%(title)s.%(ext)s'),
        'format': 'best',
        'quiet': True
    }

    # Video download
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info_dict)
        return filename

# Home route
@app.route('/')
def index():
    return render_template('index.html')

# Download route
@app.route('/download', methods=['POST'])
def download():
    
    # Get the URL
    url = request.form['url']
    
    if not url:
        return 'Por favor, forneça uma URL válida.'
    
    try:
        # Donwloads the video
        video_file = download_video(url)

        # Send the vidoe to the user
        return send_file(video_file, as_attachment=True)

    except Exception as e:
        return f'Erro ao baixar o vídeo: {str(e)}'

if __name__ == '__main__':
    app.run(debug=True)
