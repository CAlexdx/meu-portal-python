# scripts/encurtador.py
import requests

def encurtar(link: str) -> str | None:
    """
    Encurta um link usando a API pública do is.gd.
    Retorna o link encurtado ou None em caso de erro.
    """
    try:
        url = "https://is.gd/create.php"
        params = {"format": "simple", "url": link}
        r = requests.get(url, params=params, timeout=6)

        if r.status_code == 200:
            short = r.text.strip()
            if short.startswith("http"):
                return short  # Retorna o link encurtado válido
        return None
    except Exception:
        return None
