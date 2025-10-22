# scripts/conversor_medidas.py

def converter_medida(valor, de, para):
    """
    Converte medidas de comprimento, massa, temperatura ou volume.
    Retorna None se não for possível converter.
    """

    try:
        valor = float(valor)
        de = de.lower()
        para = para.lower()

        # Conversões básicas em dicionários de relação (fatores base)
        # Unidade base: metro, quilograma, litro, grau Celsius

        conversoes = {
            "comprimento": {
                "mm": 0.001,
                "cm": 0.01,
                "m": 1,
                "km": 1000,
                "in": 0.0254,
                "ft": 0.3048,
                "yd": 0.9144,
                "mi": 1609.34
            },
            "massa": {
                "mg": 0.000001,
                "g": 0.001,
                "kg": 1,
                "ton": 1000,
                "lb": 0.453592,
                "oz": 0.0283495
            },
            "volume": {
                "ml": 0.001,
                "l": 1,
                "m3": 1000,
                "gal": 3.78541
            }
        }

        # Temperatura — tratada separadamente
        if de in ["c", "f", "k"] and para in ["c", "f", "k"]:
            if de == "c":
                if para == "f":
                    return valor * 9/5 + 32
                elif para == "k":
                    return valor + 273.15
            elif de == "f":
                if para == "c":
                    return (valor - 32) * 5/9
                elif para == "k":
                    return (valor - 32) * 5/9 + 273.15
            elif de == "k":
                if para == "c":
                    return valor - 273.15
                elif para == "f":
                    return (valor - 273.15) * 9/5 + 32
            return valor  # mesma unidade

        # Identifica qual grupo a unidade pertence
        for tipo, unidades in conversoes.items():
            if de in unidades and para in unidades:
                valor_metros = valor * unidades[de]
                return valor_metros / unidades[para]

        return None

    except Exception:
        return None
