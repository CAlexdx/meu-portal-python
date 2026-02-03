# scripts/tradutor.py
from deep_translator import GoogleTranslator

def traduzir(texto, target='en'):
    """
    Traduz um texto para o idioma de destino usando DeepTranslator.
    target: código do idioma (ex: 'en', 'pt', 'es', etc.)
    """
    try:
        traducao = GoogleTranslator(source='auto', target=target).translate(texto)
        return traducao, None
    except Exception as e:
        return None, f"Erro ao traduzir: {e}"
