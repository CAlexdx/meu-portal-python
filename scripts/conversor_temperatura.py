def converter_temp(valor, de, para):
    if de == "C":
        if para == "F": return valor * 9/5 + 32
        if para == "K": return valor + 273.15
    if de == "F":
        if para == "C": return (valor - 32) * 5/9
        if para == "K": return (valor - 32) * 5/9 + 273.15
    if de == "K":
        if para == "C": return valor - 273.15
        if para == "F": return (valor - 273.15) * 9/5 + 32
    return valor
