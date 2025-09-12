import requests

def converter(valor, de="USD", para="BRL"):
    # Usando uma API de câmbio gratuita
    url = f"https://api.exchangerate.host/convert?from={de}&to={para}&amount={valor}"
    r = requests.get(url).json()
    return r["result"]
