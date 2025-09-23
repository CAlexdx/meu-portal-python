# scripts/calculadora.py

def calcular(operacao, a, b):
    """
    operacao: 'soma', 'sub', 'mul', 'div', 'pow'
    a, b: números (float)
    """
    try:
        a = float(a)
        b = float(b)
    except:
        return None, "Entradas inválidas"

    if operacao == "soma":
        return a + b, None
    if operacao == "sub":
        return a - b, None
    if operacao == "mul":
        return a * b, None
    if operacao == "div":
        if b == 0:
            return None, "Divisão por zero"
        return a / b, None
    if operacao == "pow":
        return a ** b, None
    return None, "Operação desconhecida"
