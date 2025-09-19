def analisar_texto(texto: str):
    palavras = len(texto.split())
    caracteres = len(texto)
    frases = texto.count('.') + texto.count('!') + texto.count('?')
    return {
        "palavras": palavras,
        "caracteres": caracteres,
        "frases": frases
    }
