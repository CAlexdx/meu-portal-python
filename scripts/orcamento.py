# scripts/orcamento.py
from datetime import datetime
import csv
import os

def parse_linhas(texto):
    """
    Recebe texto com linhas no formato:
      descricao:valor
    Exemplo:
      Salário:2500
      Aluguel:800
    Retorna lista de (descricao, valor_float)
    """
    linhas = [l.strip() for l in texto.splitlines() if l.strip()]
    itens = []
    for l in linhas:
        if ":" in l:
            desc, val = l.split(":", 1)
            try:
                v = float(val.strip().replace(",", "."))
            except:
                v = 0.0
            itens.append((desc.strip(), v))
    return itens

def resumir(receitas_texto, despesas_texto):
    receitas = parse_linhas(receitas_texto or "")
    despesas = parse_linhas(despesas_texto or "")

    total_receitas = sum(v for _, v in receitas)
    total_despesas = sum(v for _, v in despesas)
    saldo = total_receitas - total_despesas
    status = "Superávit" if saldo >= 0 else "Déficit"

    # percentuais de cada despesa (se houver)
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

def gerar_csv(resumo, pasta="outputs"):
    os.makedirs(pasta, exist_ok=True)
    nome = f"orcamento_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}.csv"
    caminho = os.path.join(pasta, nome)
    with open(caminho, "w", newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Tipo", "Descrição", "Valor"])
        for desc, v in resumo["receitas"]:
            writer.writerow(["Receita", desc, v])
        for desc, v in resumo["despesas"]:
            writer.writerow(["Despesa", desc, v])
        writer.writerow([])
        writer.writerow(["Total Receitas", resumo["total_receitas"]])
        writer.writerow(["Total Despesas", resumo["total_despesas"]])
        writer.writerow(["Saldo", resumo["saldo"]])
        writer.writerow(["Status", resumo["status"]])
    return caminho
