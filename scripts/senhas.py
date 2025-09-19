import random, string

def gerar_senha(tamanho=12):
    caracteres = string.ascii_letters + string.digits + "!@#$%&*?"
    return "".join(random.choice(caracteres) for _ in range(tamanho))
