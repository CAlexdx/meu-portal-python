# scripts/imc.py
def calcular_imc(peso, altura):
    """
    Calcula o IMC com validação de entrada.
    Retorna (resultado, erro).
    """
    try:
        peso = float(peso)
        altura = float(altura)
    except Exception:
        return None, "Peso ou altura inválidos."

    if not (0.5 <= peso <= 1000):
        return None, "Peso fora do intervalo aceitável (0.5–1000 kg)."
    if not (0.3 <= altura <= 3.0):
        return None, "Altura fora do intervalo aceitável (0.3–3.0 m)."

    imc = peso / (altura ** 2)
    if imc < 18.5:
        status = "Abaixo do peso"
    elif imc < 25:
        status = "Peso normal"
    elif imc < 30:
        status = "Sobrepeso"
    else:
        status = "Obesidade"

    return f"IMC: {imc:.2f} — {status}", None
