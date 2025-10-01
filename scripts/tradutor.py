from googletrans import Translator

def traduzir(texto, target='en'):
    """Traduz um texto para o idioma de destino escolhido."""
    translator = Translator()
    try:
        traducao = translator.translate(texto, dest=target)
        return traducao.text, None
    except Exception as e:
        return None, f"Erro ao traduzir: {e}"
