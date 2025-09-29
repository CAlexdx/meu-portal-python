# scripts/juros_compostos.py

def calcular_juros_compostos(capital_inicial, taxa_juros, tempo_meses):
    """
    Calcula o montante final em um investimento com juros compostos.

    Args:
        capital_inicial (float): O valor principal inicial.
        taxa_juros (float): A taxa de juros anual em formato decimal (e.g., 0.05 para 5%).
                            Será convertida para taxa mensal.
        tempo_meses (int): O tempo do investimento em meses.

    Returns:
        float: O montante final após o período.
    """
    if capital_inicial <= 0 or taxa_juros < 0 or tempo_meses < 0:
        return None, "Valores devem ser positivos. A taxa de juros pode ser zero."

    # Converte a taxa de juros anual para mensal
    taxa_juros_mensal = (1 + taxa_juros)**(1/12) - 1

    # Fórmula dos juros compostos: M = C * (1 + i)^t
    montante_final = capital_inicial * (1 + taxa_juros_mensal)**tempo_meses
    return montante_final, None

