# scripts/sorteio.py
import random

MAX_NOMES = 500

def sortear(nomes):
    """Sorteia um nome de uma lista informada em string separada por vírgulas."""
    if not isinstance(nomes, str):
        return None, "Entrada inválida."

    lista = [n.strip() for n in nomes.split(",") if n.strip()]
    seen = set()
    lista = [x for x in lista if not (x in seen or seen.add(x))]

    if not lista:
        return None, "Nenhum nome válido informado."
    if len(lista) > MAX_NOMES:
        return None, f"Muitos nomes. Máximo permitido: {MAX_NOMES}."

    return f"Sorteado: {random.choice(lista)}", None
