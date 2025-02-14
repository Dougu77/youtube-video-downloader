from flask import Flask, render_template, request, send_file, after_this_request
import yt_dlp
import os
import time

app = Flask(__name__)

# Função para baixar o vídeo usando yt-dlp
def download_video(url):
    # Obtém o diretório onde o script está sendo executado
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Diretório de download (relativo ao diretório do script)
    download_dir = os.path.join(base_dir, "downloads")
    
    # Cria o diretório 'downloads' caso não exista
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)
    
    # Definindo as opções do yt-dlp
    ydl_opts = {
        'outtmpl': os.path.join(download_dir, '%(title)s.%(ext)s'),
        'format': 'best',  # Melhor qualidade disponível
        'quiet': True  # Não mostrar logs
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info_dict)
        return filename

# Rota inicial para a página de upload
@app.route('/')
def index():
    return render_template('index.html')

# Rota para processar o download
@app.route('/download', methods=['POST'])
def download():
    url = request.form['url']
    
    if not url:
        return "Por favor, forneça uma URL válida."
    
    try:
        # Baixar o vídeo
        video_file = download_video(url)

        # Retorna o vídeo para download
        return send_file(video_file, as_attachment=True)

    except Exception as e:
        return f"Erro ao baixar o vídeo: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True)
