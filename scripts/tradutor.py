# scripts/tradutor.py
import requests

# Recomenda-se usar uma URL de uma instância pública conhecida ou hospedar sua própria.
# A instância pública default pode ser sobrecarregada ou bloqueada.
# Por exemplo: https://translate.argosopentech.com/translate
# Ou, se você tem sua própria instância: http://localhost:5000/translate
LIBRE_URL = "https://libretranslate.de/translate" # Mantenha esta, mas esteja ciente de possíveis limites.
# Ou tente: LIBRE_URL = "https://translate.argosopentech.com/translate"

MAX_TEXT = 5000  # limite para tradução

def traduzir(texto, source="pt", target="en"):
    if not texto:
        return None, "O texto para tradução não pode estar vazio." # Retorna erro
    if len(texto) > MAX_TEXT:
        return None, f"O texto excede o limite de {MAX_TEXT} caracteres." # Retorna erro

    try:
        payload = {"q": texto, "source": source, "target": target, "format": "text"}
        # Aumentar o timeout pode ajudar em redes mais lentas ou servidores ocupados
        r = requests.post(LIBRE_URL, data=payload, timeout=15) # Aumentado para 15 segundos
        r.raise_for_status() # Lança um HTTPError para respostas de status 4xx/5xx

        j = r.json()
        translated_text = j.get("translatedText") or j.get("translation")

        if translated_text:
            return translated_text, None # Retorna a tradução e nenhum erro
        else:
            # Se a resposta JSON não contiver os campos esperados, é um erro de API
            return None, "Resposta da API de tradução inválida."

    except requests.exceptions.Timeout:
        return None, "Tempo limite excedido ao tentar conectar com o servidor de tradução."
    except requests.exceptions.ConnectionError:
        return None, "Não foi possível conectar ao servidor de tradução. Verifique sua conexão ou a disponibilidade do serviço."
    except requests.exceptions.HTTPError as e:
        # Erros como 404, 500, etc.
        return None, f"Erro do servidor de tradução: {e.response.status_code} - {e.response.text}"
    except requests.exceptions.RequestException as e:
        # Outros erros de requisição
        return None, f"Ocorreu um erro inesperado na requisição: {e}"
    except ValueError: # Para erros de decodificação JSON
        return None, "Não foi possível decodificar a resposta do servidor de tradução."

