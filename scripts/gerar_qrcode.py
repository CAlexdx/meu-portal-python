# scripts/gerar_qrcode.py
import pyqrcode
from uuid import uuid4
import os

MAX_QR_TEXT = 2000

def gerar_qrcode(texto, pasta="outputs"):
    if not texto or len(texto) > MAX_QR_TEXT:
        raise ValueError(f"Texto inválido ou muito grande (max {MAX_QR_TEXT} chars).")
    qr = pyqrcode.create(texto)
    os.makedirs(pasta, exist_ok=True)
    nome = f"qrcode_{uuid4().hex}.png"
    caminho = os.path.join(pasta, nome)
    # pyqrcode usa png module — verifique requirements
    qr.png(caminho, scale=6)
    return caminho
