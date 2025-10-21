# scripts/clima.py
import requests
from datetime import datetime

def obter_coordenadas(cidade):
    """
    Usa a API de geocodificação do Open-Meteo para converter o nome da cidade
    em latitude e longitude. Compatível com Render e execução local.
    """
    try:
        url = f"https://geocoding-api.open-meteo.com/v1/search?name={cidade}&count=1&language=pt&format=json"
        r = requests.get(url, timeout=10)
        data = r.json()

        if not data.get("results"):
            return None

        resultado = data["results"][0]
        return float(resultado["latitude"]), float(resultado["longitude"]), resultado.get("timezone", "auto")
    except Exception:
        return None


def obter_clima(cidade):
    """
    Obtém informações de clima atual e previsão para os próximos dias.
    Inclui hora local, temperatura, vento, umidade e precipitação.
    """
    coords = obter_coordenadas(cidade)
    if not coords:
        return {"erro": f"Não foi possível encontrar '{cidade}'."}

    lat, lon, timezone = coords

    try:
        url = (
            f"https://api.open-meteo.com/v1/forecast?"
            f"latitude={lat}&longitude={lon}"
            f"&current_weather=true"
            f"&hourly=temperature_2m,relative_humidity_2m,precipitation"
            f"&daily=temperature_2m_max,temperature_2m_min,precipitation_sum"
            f"&timezone={timezone}"
        )
        r = requests.get(url, timeout=10)
        if r.status_code != 200:
            return {"erro": "Erro ao obter dados do clima."}

        data = r.json()

        clima_atual = data.get("current_weather", {})
        if not clima_atual:
            return {"erro": "Não foi possível obter as informações de clima."}

        # Pega hora local formatada
        hora_local = clima_atual.get("time")
        if hora_local:
            hora_local = datetime.fromisoformat(hora_local).strftime("%d/%m/%Y %H:%M")

        # Dados diários (previsão)
        previsao = []
        dias = data.get("daily", {})
        if dias:
            for i, data_dia in enumerate(dias.get("time", [])[:5]):
                previsao.append({
                    "data": datetime.fromisoformat(data_dia).strftime("%d/%m"),
                    "max": dias["temperature_2m_max"][i],
                    "min": dias["temperature_2m_min"][i],
                    "chuva": dias["precipitation_sum"][i],
                })

        return {
            "cidade": cidade.title(),
            "temperatura": clima_atual.get("temperature"),
            "vento": clima_atual.get("windspeed"),
            "hora_local": hora_local,
            "descricao": "Condições atuais e previsão dos próximos dias",
            "previsao": previsao,
            "lat": lat,
            "lon": lon
        }

    except Exception as e:
        return {"erro": f"Erro ao conectar à API: {e}"}
