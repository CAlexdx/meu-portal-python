# scripts/clima.py
import requests

def obter_coordenadas(cidade):
    """Usa a API Nominatim (OpenStreetMap) para converter cidade em latitude e longitude."""
    try:
        url = f"https://nominatim.openstreetmap.org/search?q={cidade}&format=json&limit=1"
        r = requests.get(url, headers={"User-Agent": "MeuPortalPython/1.0"}, timeout=10)
        data = r.json()
        if not data:
            return None
        return float(data[0]["lat"]), float(data[0]["lon"])
    except Exception:
        return None

def obter_clima(cidade):
    """Obtém informações de clima atual de qualquer cidade."""
    coords = obter_coordenadas(cidade)
    if not coords:
        return {"erro": f"Não foi possível encontrar '{cidade}'."}

    lat, lon = coords
    try:
        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
        r = requests.get(url, timeout=10)
        if r.status_code != 200:
            return {"erro": "Erro ao obter clima."}
        data = r.json()
        clima = data.get("current_weather", {})
        return {
            "cidade": cidade.title(),
            "temperatura": clima.get("temperature"),
            "vento": clima.get("windspeed"),
            "descricao": "Clima atual",
            "lat": lat,
            "lon": lon
        }
    except Exception as e:
        return {"erro": str(e)}
