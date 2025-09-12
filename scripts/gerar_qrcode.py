import pyqrcode
import os

def gerar_qrcode(texto, pasta_saida="outputs"):
    os.makedirs(pasta_saida, exist_ok=True)
    caminho = os.path.join(pasta_saida, "qrcode.png")
    qr = pyqrcode.create(texto)
    qr.png(caminho, scale=6)
    return caminho
