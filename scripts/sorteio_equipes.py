import random

MAX_NOMES = 500
MAX_EQUIPES = 20

def sortear_equipes(nomes, qtd_equipes):
    """Sorteia nomes em equipes equilibradas."""
    if not isinstance(nomes, str):
        return None, "Entrada inválida."

    lista = [n.strip() for n in nomes.split(",") if n.strip()]
    seen = set()
    lista = [x for x in lista if not (x in seen or seen.add(x))]

    if not lista:
        return None, "Nenhum nome válido informado."
    if len(lista) > MAX_NOMES:
        return None, f"Muitos nomes. Máximo permitido: {MAX_NOMES}."
    if qtd_equipes < 1:
        return None, "Número de equipes inválido."

    qtd_equipes = min(qtd_equipes, MAX_EQUIPES, len(lista))
    random.shuffle(lista)

    equipes = [[] for _ in range(qtd_equipes)]
    for i, nome in enumerate(lista):
        equipes[i % qtd_equipes].append(nome)

    return equipes, None
