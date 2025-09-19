from PIL import Image, ImageOps, ImageFilter
import os

def aplicar_filtro(caminho, filtro, pasta_saida="outputs"):
    os.makedirs(pasta_saida, exist_ok=True)
    img = Image.open(caminho)

    if filtro == "bw":
        img = ImageOps.grayscale(img)
    elif filtro == "invert":
        img = ImageOps.invert(img.convert("RGB"))
    elif filtro == "blur":
        img = img.filter(ImageFilter.GaussianBlur(4))

    saida = os.path.join(pasta_saida, f"editado_{filtro}.png")
    img.save(saida)
    return saida
