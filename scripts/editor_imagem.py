# scripts/editor_imagem.py
from PIL import Image, ImageOps, ImageFilter, ImageEnhance
import os
from uuid import uuid4

def aplicar_filtro(caminho, filtro, pasta_saida="outputs"):
    os.makedirs(pasta_saida, exist_ok=True)
    img = Image.open(caminho)

    # Ensure image is in RGB mode for operations that require it
    if img.mode not in ("RGB", "RGBA"):
        img = img.convert("RGB")

    if filtro == "bw":
        img = ImageOps.grayscale(img)
    elif filtro == "invert":
        img = ImageOps.invert(img)
    elif filtro == "blur":
        img = img.filter(ImageFilter.GaussianBlur(4))
    elif filtro == "sharpen": # Novo filtro: Nitidez
        img = img.filter(ImageFilter.SHARPEN)
    elif filtro == "emboss": # Novo filtro: Relevo
        img = img.filter(ImageFilter.EMBOSS)
    elif filtro == "contour": # Novo filtro: Contorno
        img = img.filter(ImageFilter.CONTOUR)
    elif filtro == "sepia": # Novo filtro: Sépia
        # Convert to grayscale first, then apply sepia tone
        img = ImageOps.grayscale(img)
        # Create a new image with sepia colors
        sepia_filter = lambda pixel: (
            min(255, int(pixel[0] * 0.393 + pixel[1] * 0.769 + pixel[2] * 0.189)), # R
            min(255, int(pixel[0] * 0.349 + pixel[1] * 0.686 + pixel[2] * 0.168)), # G
            min(255, int(pixel[0] * 0.272 + pixel[1] * 0.534 + pixel[2] * 0.131))  # B
        )
        img = img.convert("RGB").point(sepia_filter)
    elif filtro == "brightness_boost": # Novo filtro: Aumento de Brilho
        enhancer = ImageEnhance.Brightness(img)
        img = enhancer.enhance(1.5) # Aumenta o brilho em 50%
    elif filtro == "contrast_boost": # Novo filtro: Aumento de Contraste
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(1.5) # Aumenta o contraste em 50%
    else: # Default filter if none is recognized
        img = ImageOps.grayscale(img)

    nome = f"editado_{filtro}_{uuid4().hex}.png"
    saida = os.path.join(pasta_saida, nome)
    img.save(saida)
    return saida
