# scripts/calculadora.py
MAX_ABS = 1e12

def calcular(operacao, a, b):
    try:
        a = float(str(a).replace(",", "."))
        b = float(str(b).replace(",", "."))
    except:
        return None, "Entradas inválidas"

    if abs(a) > MAX_ABS or abs(b) > MAX_ABS:
        return None, "Números muito grandes."

    if operacao == "soma":
        return a + b, None
    if operacao == "sub":
        return a - b, None
    if operacao == "mul":
        return a * b, None
    if operacao == "div":
        if b == 0:
            return None, "Divisão por zero."
        return a / b, None
    if operacao == "pow":
        # limitar expoente por segurança
        if abs(b) > 1000:
            return None, "Expoente muito grande."
        return a ** b, None
    return None, "Operação desconhecida"
