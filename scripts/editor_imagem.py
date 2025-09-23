# scripts/editor_imagem.py
from PIL import Image, ImageOps, ImageFilter
import os
from uuid import uuid4

def aplicar_filtro(caminho, filtro, pasta_saida="outputs"):
    os.makedirs(pasta_saida, exist_ok=True)
    img = Image.open(caminho)
    if filtro == "bw":
        img = ImageOps.grayscale(img)
    elif filtro == "invert":
        img = ImageOps.invert(img.convert("RGB"))
    elif filtro == "blur":
        img = img.filter(ImageFilter.GaussianBlur(4))
    else:
        img = ImageOps.grayscale(img)
    nome = f"editado_{filtro}_{uuid4().hex}.png"
    saida = os.path.join(pasta_saida, nome)
    img.save(saida)
    return saida
