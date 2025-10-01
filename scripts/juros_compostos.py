# scripts/juros_compostos.py

def calcular_juros_compostos(capital_inicial, taxa_juros, tempo_meses):
    """
    Calcula o montante final em um investimento com juros compostos.

    Args:
        capital_inicial (float): Valor inicial investido.
        taxa_juros (float): Taxa de juros anual em formato decimal (ex: 0.05 para 5%).
        tempo_meses (int): Duração do investimento em meses.

    Returns:
        tuple: (montante_final, erro) → Se erro, retorna (None, mensagem).
    """
    try:
        capital_inicial = float(capital_inicial)
        taxa_juros = float(taxa_juros)
        tempo_meses = int(tempo_meses)
    except Exception:
        return None, "Valores inválidos. Verifique os campos."

    if capital_inicial <= 0 or taxa_juros < 0 or tempo_meses < 0:
        return None, "Valores devem ser positivos. A taxa de juros pode ser zero."

    # Converte taxa anual para mensal
    taxa_juros_mensal = (1 + taxa_juros) ** (1/12) - 1

    # Fórmula dos juros compostos
    montante_final = capital_inicial * (1 + taxa_juros_mensal) ** tempo_meses
    return round(montante_final, 2), None
