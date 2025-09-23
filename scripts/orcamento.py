# scripts/orcamento.py  (atualizado)
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
        if ":" in l:
            desc, val = l.split(":", 1)
            try:
                v = float(val.strip().replace(",", "."))
            except:
                raise ValueError(f"Valor inválido na linha: {l}")
            if abs(v) > MAX_VALOR:
                raise ValueError("Valor muito grande em alguma linha.")
            itens.append((desc.strip(), v))
    return itens

def resumir(receitas_texto, despesas_texto):
    receitas = parse_linhas(receitas_texto or "")
    despesas = parse_linhas(despesas_texto or "")

    total_receitas = sum(v for _, v in receitas)
    total_despesas = sum(v for _, v in despesas)
    saldo = total_receitas - total_despesas
    status = "Superávit" if saldo >= 0 else "Déficit"

    percentuais_despesas = []
    for desc, v in despesas:
        pct = (v / total_receitas * 100) if total_receitas > 0 else 0
        percentuais_despesas.append((desc, v, round(pct, 2)))

    resumo = {
        "receitas": receitas,
        "despesas": despesas,
        "total_receitas": round(total_receitas, 2),
        "total_despesas": round(total_despesas, 2),
        "saldo": round(saldo, 2),
        "status": status,
        "percentuais_despesas": percentuais_despesas,
        "gerado_em": datetime.utcnow().isoformat()
    }
    return resumo
