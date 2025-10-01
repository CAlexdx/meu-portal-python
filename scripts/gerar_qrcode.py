# scripts/gerar_qrcode.py
import pyqrcode
from uuid import uuid4
import os

MAX_QR_TEXT = 2000

def gerar_qrcode(texto: str, pasta: str = "outputs") -> str:
    """
    Gera um QR Code a partir de um texto.
    Retorna o caminho do arquivo gerado.
    """
    if not texto or len(texto) > MAX_QR_TEXT:
        raise ValueError(f"Texto inválido ou muito grande (máx {MAX_QR_TEXT} caracteres).")

    qr = pyqrcode.create(texto)
    os.makedirs(pasta, exist_ok=True)

    nome = f"qrcode_{uuid4().hex}.png"
    caminho = os.path.join(pasta, nome)

    qr.png(caminho, scale=6)
    return caminho
