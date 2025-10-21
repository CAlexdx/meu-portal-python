# scripts/clima.py
import requests

def obter_coordenadas(cidade):
    """
    Usa a API de geocodificação do Open-Meteo para converter o nome da cidade
    em latitude e longitude. Compatível com Render e execução local.
    """
    try:
        url = f"https://geocoding-api.open-meteo.com/v1/search?name={cidade}&count=1&language=pt&format=json"
        r = requests.get(url, timeout=10)
        data = r.json()

        # Verifica se encontrou resultados
        if not data.get("results"):
            return None

        resultado = data["results"][0]
        return float(resultado["latitude"]), float(resultado["longitude"])
    except Exception:
        return None


def obter_clima(cidade):
    """
    Obtém informações de clima atual de qualquer cidade do mundo,
    utilizando as coordenadas obtidas pela API de geocodificação.
    """
    coords = obter_coordenadas(cidade)
    if not coords:
        return {"erro": f"Não foi possível encontrar '{cidade}'."}

    lat, lon = coords
    try:
        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
        r = requests.get(url, timeout=10)

        if r.status_code != 200:
            return {"erro": "Erro ao obter dados do clima."}

        data = r.json()
        clima = data.get("current_weather", {})

        if not clima:
            return {"erro": "Não foi possível obter as informações de clima."}

        return {
            "cidade": cidade.title(),
            "temperatura": clima.get("temperature"),
            "vento": clima.get("windspeed"),
            "descricao": "Clima atual",
            "lat": lat,
            "lon": lon
        }

    except Exception as e:
        return {"erro": f"Erro ao conectar à API: {e}"}
