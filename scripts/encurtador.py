# scripts/encurtador.py
import requests

def encurtar(link):
    try:
        # is.gd API: https://is.gd/create.php?format=simple&url=...
        url = "https://is.gd/create.php"
        params = {"format": "simple", "url": link}
        r = requests.get(url, params=params, timeout=8)
        if r.status_code == 200:
            short = r.text.strip()
            return short
        return None
    except:
        return None
