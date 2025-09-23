# scripts/tradutor.py
import requests

LIBRE_URL = "https://libretranslate.de/translate"
MAX_TEXT = 5000  # limite para tradução

def traduzir(texto, source="pt", target="en"):
    if not texto or len(texto) > MAX_TEXT:
        return None
    try:
        payload = {"q": texto, "source": source, "target": target, "format": "text"}
        r = requests.post(LIBRE_URL, data=payload, timeout=8)
        r.raise_for_status()
        j = r.json()
        # várias instâncias regresam chaves diferentes; buscar a tradução
        return j.get("translatedText") or j.get("translation") or None
    except requests.exceptions.RequestException:
        return None
