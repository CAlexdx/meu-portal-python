# scripts/conversor.py
import requests

# API gratuita, sem necessidade de chave para taxas básicas (2025)
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

        # Se a moeda de origem não for USD, convertemos primeiro para USD
        if de != "USD":
            if de not in taxas:
                return None
            valor_em_usd = valor / taxas[de]
        else:
            valor_em_usd = valor

        # Depois convertemos de USD para a moeda destino
        if para not in taxas:
            return None

        resultado = valor_em_usd * taxas[para]
        return round(resultado, 4)

    except (ValueError, TypeError, KeyError):
        return None
