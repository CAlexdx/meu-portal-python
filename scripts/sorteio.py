import random

def sortear(nomes):
    lista = [n.strip() for n in nomes.split(",") if n.strip()]
    if not lista:
        return "Nenhum nome válido informado."
    return f"Sorteado: {random.choice(lista)}"
