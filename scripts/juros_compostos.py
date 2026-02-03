# scripts/juros_compostos.py

def calcular_juros_compostos(capital_inicial, taxa_juros_anual, tempo, periodo="meses", aporte_mensal=0):
    """
    Calcula o montante final de um investimento com juros compostos, considerando aporte mensal opcional.

    Args:
        capital_inicial (float): Valor inicial investido.
        taxa_juros_anual (float): Taxa de juros anual em % (ex: 20 para 20% ao ano).
        tempo (int): Duração do investimento.
        periodo (str): 'anos' ou 'meses'. Define unidade do tempo.
        aporte_mensal (float): Valor adicional aplicado todo mês (opcional).

    Returns:
        dict ou (None, erro): Se sucesso, retorna dict com montante_final, total_investido e total_juros.
    """
    try:
        capital_inicial = float(capital_inicial)
        taxa_juros_anual = float(taxa_juros_anual) / 100  # converte para decimal
        tempo = int(tempo)
        aporte_mensal = float(aporte_mensal)
    except Exception:
        return None, "Valores inválidos. Verifique os campos."

    if capital_inicial < 0 or taxa_juros_anual < 0 or tempo < 0 or aporte_mensal < 0:
        return None, "Valores devem ser positivos."

    # Converte anos para meses se necessário
    if periodo == "anos":
        tempo_meses = tempo * 12
    else:
        tempo_meses = tempo

    # Calcula taxa mensal
    taxa_mensal = (1 + taxa_juros_anual) ** (1/12) - 1

    montante = capital_inicial
    total_investido = capital_inicial

    for _ in range(tempo_meses):
        montante = montante * (1 + taxa_mensal) + aporte_mensal
        total_investido += aporte_mensal

    total_juros = montante - total_investido

    resultado = {
        "montante_final": f"{montante:,.2f}",
        "total_investido": f"{total_investido:,.2f}",
        "total_juros": f"{total_juros:,.2f}"
    }
    return resultado, None
