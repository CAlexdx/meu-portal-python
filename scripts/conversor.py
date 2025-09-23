# scripts/conversor.py
import requests

API_URL = "https://api.exchangerate.host/convert"

def converter(valor, de="USD", para="BRL"):
    try:
        payload = {"from": de, "to": para, "amount": valor}
        r = requests.get(API_URL, params=payload, timeout=8)
        r.raise_for_status()
        j = r.json()
        # estrutura esperada: j["result"]
        return j.get("result")
    except Exception:
        return None
