import requests

def converter(valor, de="USD", para="BRL"):
    url = f"https://api.exchangerate.host/convert?from={de}&to={para}&amount={valor}"
    r = requests.get(url).json()
    if "result" in r and r["result"] is not None:
        return round(r["result"], 2)
    else:
        return None
