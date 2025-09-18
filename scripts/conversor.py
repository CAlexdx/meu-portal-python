import requests

def converter(valor, de="USD", para="BRL"):
    url = f"https://api.exchangerate.host/convert?from={de}&to={para}&amount={valor}"
    r = requests.get(url).json()
    return r["result"]
