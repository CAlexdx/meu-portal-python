# scripts/calculadora.py

MAX_ABS = 1e12

def calcular(operacao, a, b):
    """
    Executa operações básicas entre dois números.

    Args:
        operacao (str): 'soma', 'sub', 'mul', 'div', 'pow'.
        a, b (float): valores de entrada.

    Returns:
        tuple: (resultado ou None, mensagem de erro ou None)
    """
    try:
        a = float(str(a).replace(",", "."))
        b = float(str(b).replace(",", "."))
    except:
        return None, "Entradas inválidas."

    if abs(a) > MAX_ABS or abs(b) > MAX_ABS:
        return None, "Números muito grandes."

    if operacao == "soma":
        return a + b, None
    elif operacao == "sub":
        return a - b, None
    elif operacao == "mul":
        return a * b, None
    elif operacao == "div":
        if b == 0:
            return None, "Divisão por zero."
        return a / b, None
    elif operacao == "pow":
        if abs(b) > 1000:
            return None, "Expoente muito grande."
        return a ** b, None

    return None, "Operação desconhecida."
