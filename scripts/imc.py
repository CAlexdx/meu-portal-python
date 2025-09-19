def calcular_imc(peso, altura):
    imc = peso / (altura ** 2)
    if imc < 18.5:
        status = "Abaixo do peso"
    elif imc < 25:
        status = "Peso normal"
    elif imc < 30:
        status = "Sobrepeso"
    else:
        status = "Obesidade"
    return f"IMC: {imc:.2f} - {status}"
