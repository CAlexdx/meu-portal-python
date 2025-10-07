# scripts/senhas.py
import random
import string

def gerar_senha(tamanho=12):
    """Gera uma senha aleatória segura."""
    if tamanho < 4:
        tamanho = 4
    elif tamanho > 64:
        tamanho = 64

    caracteres = string.ascii_letters + string.digits + "!@#$%&*?"
    return "".join(random.choice(caracteres) for _ in range(tamanho))
