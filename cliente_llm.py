import logging
import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)


def carregar_configuracoes():
    url = os.getenv("LLM_API_URL", "").strip()
    chave = os.getenv("LLM_API_KEY", "").strip()
    temperatura = float(os.getenv("LLM_TEMPERATURE", "0.2").strip() or 0.2)
    max_tokens = int(os.getenv("LLM_MAX_OUTPUT_TOKENS", "500").strip() or 500)
    return url, chave, temperatura, max_tokens


def analisar_texto(texto_usuario):
    url, chave, temperatura, max_tokens = carregar_configuracoes()
    if not url or not url.startswith("http"):
        return {"erro": "URL da API não encontrada ou inválida."}
    if not chave:
        return {"erro": "Chave da API não encontrada."}
    headers = {"x-goog-api-key": chave}

    prompt = f"""
    Analise a seguinte mensagem para identificar possíveis golpes, fraudes ou fake news.
    Responda estritamente no formato JSON com estas chaves exatas:
    - "classificacao": ("Golpe ou Fake News", "Suspeito" ou "Seguro")
    - "nivel_risco": (número inteiro de 0 a 10)
    - "sinais_alerta": (lista de strings com os motivos; se não houver, lista vazia [])
    - "explicacao": (resumo claro e direto em português)

    Mensagem: {texto_usuario}
    """

    dados = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "responseMimeType": "application/json",
            "temperature": temperatura,
            "maxOutputTokens": max_tokens,
        },
    }
    logger.info("Enviando solicitação para a API LLM.")

    try:
        resposta = requests.post(url, headers=headers, json=dados, timeout=10)
        if resposta.status_code in [400, 401, 403]:
            logger.error(
                "Erro de autenticação/permissão na API (código %s).",
                resposta.status_code,
            )
            return {
                "erro": f"Credencial inválida ou sem permissão (código {resposta.status_code}). Verifique a LLM_API_KEY no arquivo .env."
            }
        if resposta.status_code == 503:
            logger.error("Serviço indisponível na API (código 503).")
            return {
                "erro": "Serviço indisponível (código 503). Tente novamente mais tarde."
            }
        resposta_json = resposta.json()
        if "candidates" in resposta_json:
            texto_ia = resposta_json["candidates"][0]["content"]["parts"][0][
                "text"
            ].strip()
            if not texto_ia:
                logger.warning("A resposta da API veio vazia.")
                return {"erro": "A resposta da API está vazia."}
            logger.info("Resposta da API recebida e interpretada com sucesso.")
            return json.loads(texto_ia)
        else:
            logger.warning("Resposta da API sem campo 'candidates'.")
            return {"erro": f"Aviso do servidor: {resposta_json}"}
    except requests.exceptions.Timeout:
        logger.error("Timeout ao aguardar resposta da API.")
        return {
            "erro": "Tempo de resposta da API excedido. Tente novamente mais tarde."
        }
    except json.JSONDecodeError:
        logger.error("Falha ao decodificar JSON retornado pela API.")
        return {
            "erro": "Falha ao decodificar a resposta da API. A resposta não está no formato JSON esperado."
        }
    except Exception as e:
        logger.error("Falha na comunicação com a API: %s", type(e).__name__)
        return {"erro": f"Falha na comunicação com a API: {e}"}
