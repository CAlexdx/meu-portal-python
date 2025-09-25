from datetime import datetime
import csv, os

MAX_LINHAS = 200
MAX_VALOR = 1e9

def parse_linhas(texto):
    linhas = [l.strip() for l in texto.splitlines() if l.strip()]
    if len(linhas) > MAX_LINHAS:
        raise ValueError(f"Muitas linhas (máx {MAX_LINHAS}).")
    itens = []
    for l in linhas:
        if ":" not in l: # Adicionei uma verificação para garantir o formato "desc: valor"
            raise ValueError(f"Formato inválido na linha: '{l}'. Use 'Descrição: Valor'.")
        desc, val = l.split(":", 1)
        try:
            v = float(val.strip().replace(",", "."))
        except ValueError: # Capturei o erro específico de valor
            raise ValueError(f"Valor inválido na linha: {l}")
        if abs(v) > MAX_VALOR:
            raise ValueError("Valor muito grande em alguma linha.")
        itens.append((desc.strip(), v))
    return itens

def resumir(receitas_texto, despesas_texto):
    # Trate o caso de inputs vazios para evitar erro de parse_linhas em string vazia
    receitas_parsed = []
    if receitas_texto:
        receitas_parsed = parse_linhas(receitas_texto)

    despesas_parsed = []
    if despesas_texto:
        despesas_parsed = parse_linhas(despesas_texto)

    total_receitas = sum(v for _, v in receitas_parsed)
    total_despesas = sum(v for _, v in despesas_parsed)
    saldo = total_receitas - total_despesas
    status = "Superávit" if saldo >= 0 else "Déficit"

    percentuais_despesas = []
    # Calcula percentuais apenas se houver despesas e receitas para evitar divisão por zero
    if total_receitas > 0:
        for desc, v in despesas_parsed:
            pct = (v / total_receitas * 100)
            percentuais_despesas.append((desc, v, round(pct, 2)))
    else: # Se não há receitas, despesas não podem ser percentualizadas em relação a elas
        for desc, v in despesas_parsed:
            percentuais_despesas.append((desc, v, 0.0)) # Ou algum indicador como N/A


    resumo = {
        "receitas": receitas_parsed, # Use os parsed, não os brutos
        "despesas": despesas_parsed, # Use os parsed, não os brutos
        "total_receitas": round(total_receitas, 2),
        "total_despesas": round(total_despesas, 2),
        "saldo": round(saldo, 2),
        "status": status,
        "percentuais_despesas": percentuais_despesas,
        "gerado_em": datetime.now().strftime("%d/%m/%Y %H:%M:%S") # Formato mais amigável
    }
    return resumo