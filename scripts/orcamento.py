# scripts/orcamento.py
from datetime import datetime
import os

MAX_LINHAS = 200
MAX_VALOR = 1e9

def parse_linhas(texto):
    """Converte linhas no formato 'Descrição: Valor' para lista de tuplas."""
    linhas = [l.strip() for l in texto.splitlines() if l.strip()]
    if len(linhas) > MAX_LINHAS:
        raise ValueError(f"Muitas linhas (máx {MAX_LINHAS}).")
    itens = []
    for l in linhas:
        if ":" not in l:
            raise ValueError(f"Formato inválido na linha: '{l}'. Use 'Descrição: Valor'.")
        desc, val = l.split(":", 1)
        try:
            v = float(val.strip().replace(",", "."))
        except ValueError:
            raise ValueError(f"Valor inválido na linha: {l}")
        if abs(v) > MAX_VALOR:
            raise ValueError("Valor muito grande em alguma linha.")
        itens.append((desc.strip(), v))
    return itens

def resumir(receitas_texto, despesas_texto):
    """Gera um resumo financeiro com receitas, despesas e saldo."""
    receitas_parsed = parse_linhas(receitas_texto) if receitas_texto else []
    despesas_parsed = parse_linhas(despesas_texto) if despesas_texto else []

    total_receitas = sum(v for _, v in receitas_parsed)
    total_despesas = sum(v for _, v in despesas_parsed)
    saldo = total_receitas - total_despesas
    status = "Superávit" if saldo >= 0 else "Déficit"

    percentuais_despesas = []
    if total_receitas > 0:
        for desc, v in despesas_parsed:
            pct = (v / total_receitas * 100)
            percentuais_despesas.append((desc, v, round(pct, 2)))
    else:
        for desc, v in despesas_parsed:
            percentuais_despesas.append((desc, v, 0.0))

    return {
        "receitas": receitas_parsed,
        "despesas": despesas_parsed,
        "total_receitas": round(total_receitas, 2),
        "total_despesas": round(total_despesas, 2),
        "saldo": round(saldo, 2),
        "status": status,
        "percentuais_despesas": percentuais_despesas,
        "gerado_em": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    }
