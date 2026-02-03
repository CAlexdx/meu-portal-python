# scripts/PYtube
from pytubefix import YouTube
import os

def baixar_youtube(link, pasta_saida="outputs"):
    """Baixa vídeo do YouTube na maior resolução disponível."""
    os.makedirs(pasta_saida, exist_ok=True)
    yt = YouTube(link)
    stream = yt.streams.get_highest_resolution()
    filename = yt.title.replace(" ", "_") + ".mp4"
    stream.download(pasta_saida, filename)
    return filename
