# scripts/texto_stats.py
import re

MAX_TEXT = 50000  # limite de 50 mil caracteres

def analisar_texto(texto: str):
    """Analisa um texto e retorna estatísticas básicas."""
    if not isinstance(texto, str):
        return None, "Texto inválido."
    
    texto = texto.strip()
    if not texto:
        return None, "Nenhum texto informado."
    if len(texto) > MAX_TEXT:
        return None, f"Texto muito grande (máx {MAX_TEXT} caracteres)."

    # normalizar espaços
    texto_norm = re.sub(r'\s+', ' ', texto)

    palavras = len([w for w in texto_norm.split(' ') if w])
    caracteres = len(texto)
    frases = sum(texto.count(c) for c in ".!?")
    linhas = len(texto.splitlines())

    return {
        "palavras": palavras,
        "caracteres": caracteres,
        "frases": frases,
        "linhas": linhas
    }, None
