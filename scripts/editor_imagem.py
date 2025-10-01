from PIL import Image, ImageEnhance, ImageFilter
import os

OUTPUT_DIR = "outputs"

def salvar_imagem(imagem, nome_base, extensao="png"):
    """Salva a imagem processada na pasta outputs."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    caminho = os.path.join(OUTPUT_DIR, f"{nome_base}.{extensao}")
    imagem.save(caminho)
    return caminho

def aplicar_filtro(imagem_path, filtro, brilho=1.0, contraste=1.0, nitidez=1.0):
    """
    Aplica filtros e ajustes na imagem.
    
    Args:
        imagem_path (str): Caminho da imagem original.
        filtro (str): Nome do filtro (blur, contorno, escala_cinza, original).
        brilho (float): Fator de brilho.
        contraste (float): Fator de contraste.
        nitidez (float): Fator de nitidez.

    Returns:
        str: Caminho da nova imagem gerada.
    """
    img = Image.open(imagem_path)

    # Filtros básicos
    if filtro == "blur":
        img = img.filter(ImageFilter.BLUR)
    elif filtro == "contorno":
        img = img.filter(ImageFilter.CONTOUR)
    elif filtro == "escala_cinza":
        img = img.convert("L")

    # Ajustes
    img = ImageEnhance.Brightness(img).enhance(brilho)
    img = ImageEnhance.Contrast(img).enhance(contraste)
    img = ImageEnhance.Sharpness(img).enhance(nitidez)

    nome_base = os.path.splitext(os.path.basename(imagem_path))[0] + "_editada"
    return salvar_imagem(img, nome_base)
