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

    base, ext = os.path.splitext(os.path.basename(caminho))
    nome_saida = f"{base}_{filtro}{ext}"
    saida = os.path.join(pasta_saida, nome_saida)
    img.save(saida)
    return nome_saida # Retorna apenas o nome do arquivo, não o caminho completo