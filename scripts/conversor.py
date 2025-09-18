import requests

def converter(valor, de="USD", para="BRL"):
    url = f"https://api.frankfurter.app/latest?amount={valor}&from={de}&to={para}"
    r = requests.get(url).json()
    if "rates" in r and para in r["rates"]:
        return round(r["rates"][para], 2)
    else:
        return None
