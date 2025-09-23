# scripts/tradutor.py
import requests

# endpoint público (uso moderado)
LIBRE_URL = "https://libretranslate.de/translate"

def traduzir(texto, source="pt", target="en"):
    try:
        payload = {
            "q": texto,
            "source": source,
            "target": target,
            "format": "text"
        }
        r = requests.post(LIBRE_URL, data=payload, timeout=10)
        j = r.json()
        if "translatedText" in j:
            return j["translatedText"]
        # algumas instâncias retornam 'translation' ou outro; fallback:
        return j.get("translatedText") or j.get("translation") or None
    except Exception as e:
        return None
