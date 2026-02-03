def calcular_consumo_medio(distancia, combustivel):
    """
    Calcula o consumo médio de combustível em km/l.
    Args:
        distancia (float): Distância percorrida em km.
        combustivel (float): Combustível consumido em litros.
    Returns:
        tuple: (resultado ou None, mensagem de erro ou None)
    """
    try:
        distancia = float(distancia)
        combustivel = float(combustivel)
        if combustivel == 0:
            return None, "Erro: Combustível não pode ser zero."
        if distancia < 0 or combustivel < 0:
            return None, "Erro: Valores não podem ser negativos."
        consumo = distancia / combustivel
        return f"{consumo:.3f} km/l", None
    except ValueError:
        return None, "Erro: Insira valores numéricos válidos."