# scripts/editor_imagem.py
from PIL import Image, ImageEnhance, ImageFilter

def aplicar_filtros(img, filtros=[]):
    """ Aplica múltiplos filtros pré-definidos na imagem. filtros: lista de strings com nomes dos filtros """
    for filtro in filtros:
        if filtro == "blur":
            img = img.filter(ImageFilter.BLUR)
        elif filtro == "contorno":
            img = img.filter(ImageFilter.CONTOUR)
        elif filtro == "escala_cinza":
            img = img.convert("L").convert("RGB")
        elif filtro == "detalhe":
            img = img.filter(ImageFilter.DETAIL)
        elif filtro == "borda":
            img = img.filter(ImageFilter.EDGE_ENHANCE)
    return img

def ajustar_imagem(img, brilho=1.0, contraste=1.0, nitidez=1.0):
    """ Ajusta brilho, contraste e nitidez da imagem. """
    img = ImageEnhance.Brightness(img).enhance(brilho)
    img = ImageEnhance.Contrast(img).enhance(contraste)
    img = ImageEnhance.Sharpness(img).enhance(nitidez)
    return img
