# scripts/encurtador.py
import requests

def encurtar(link):
    try:
        url = "https://is.gd/create.php"
        params = {"format": "simple", "url": link}
        r = requests.get(url, params=params, timeout=6)
        if r.status_code == 200:
            short = r.text.strip()
            # is.gd pode retornar texto de erro; checar esquema
            if short.startswith("http"):
                return short
        return None
    except Exception:
        return None
