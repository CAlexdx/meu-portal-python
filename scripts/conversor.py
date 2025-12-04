# scripts/conversor.py
import requests

API_URL = "https://api.exchangerate-api.com/v4/latest/USD"

def obter_taxas():
    try:
        response = requests.get(API_URL, timeout=10)
        response.raise_for_status()
        return response.json()["rates"]
    except Exception as e:
        print(f"Erro ao obter taxas: {e}")
        return None

def converter(valor, de="USD", para="BRL"):
    try:
        valor = float(valor)
        if valor < 0:
            return None

        taxas = obter_taxas()
        if not taxas:
            return None

        if de != "USD":
            if de not in taxas:
                return None
            valor_em_usd = valor / taxas[de]
        else:
            valor_em_usd = valor

        if para not in taxas:
            return None

        resultado = valor_em_usd * taxas[para]
        return resultado  # ← AQUI: sem round!, deixa natural

    except (ValueError, TypeError, KeyError):
        return None
