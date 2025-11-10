# scripts/editor_imagem.py
from PIL import Image, ImageOps, ImageFilter, ImageEnhance

def aplicar_filtros(img, filtros=[]):
    """Aplica múltiplos filtros na imagem."""
    for filtro in filtros:
        if filtro == "preto_branco":
            img = img.convert("L").convert("RGB")
        elif filtro == "sepia":
            sepia = []
            for i in range(255):
                r = int(i * 240 / 255)
                g = int(i * 200 / 255)
                b = int(i * 145 / 255)
                sepia.append((r, g, b))
            img = img.convert("L")
            img.putpalette(sum(sepia, ()))
            img = img.convert("RGB")
        elif filtro == "inverter":
            img = ImageOps.invert(img.convert("RGB"))
        elif filtro == "blur":
            img = img.filter(ImageFilter.BLUR)
        elif filtro == "contorno":
            img = img.filter(ImageFilter.CONTOUR)
        elif filtro == "bordas":
            img = img.filter(ImageFilter.EDGE_ENHANCE)
        elif filtro == "detalhe":
            img = img.filter(ImageFilter.DETAIL)
        elif filtro == "realce":
            img = ImageEnhance.Contrast(img).enhance(1.5)
        elif filtro == "saturacao_alta":
            img = ImageEnhance.Color(img).enhance(1.5)
        elif filtro == "saturacao_baixa":
            img = ImageEnhance.Color(img).enhance(0.5)
        elif filtro == "nitidez":
            img = ImageEnhance.Sharpness(img).enhance(2.0)
        elif filtro == "escurecer":
            img = ImageEnhance.Brightness(img).enhance(0.7)
        elif filtro == "clarear":
            img = ImageEnhance.Brightness(img).enhance(1.3)
    return img
