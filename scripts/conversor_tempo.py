def converter_tempo(valor, unidade_origem, unidade_destino):
    """
    Converte tempo entre várias unidades: segundos, minutos, horas, dias, semanas, meses, anos.
    Args:
        valor (float): Valor a converter.
        unidade_origem (str): Unidade de origem.
        unidade_destino (str): Unidade de destino.
    Returns:
        tuple: (resultado ou None, mensagem de erro ou None)
    """
    try:
        valor = float(valor)
        if valor < 0:
            return None, "Erro: O valor não pode ser negativo."
        unidades = ["segundos", "minutos", "horas", "dias", "semanas", "meses", "anos"]
        if unidade_origem not in unidades or unidade_destino not in unidades:
            return None, "Erro: Unidades inválidas. Escolha entre segundos, minutos, horas, dias, semanas, meses ou anos."

        # Fatores de conversão para segundos (base)
        fatores = {
            "segundos": 1,
            "minutos": 60,
            "horas": 3600,
            "dias": 86400,
            "semanas": 604800,
            "meses": 2592000,  # Aproximado: 30 dias
            "anos": 31536000   # Aproximado: 365 dias
        }

        # Converter para segundos
        segundos = valor * fatores[unidade_origem]

        # Converter para unidade destino
        resultado = segundos / fatores[unidade_destino]
        return f"{resultado:.2f} {unidade_destino}", None
    except ValueError:
        return None, "Erro: Insira um valor numérico válido."