import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

def analisar_texto(texto_usuario):
    url=os.getenv("LLM_API_URL","").strip()
    chave=os.getenv("LLM_API_KEY","").strip()
    if not url or not url.startswith("http"):       
        return {"erro": "URL da API não encontrada ou inválida."}
    if not chave:
        return {"erro": "Chave da API não encontrada."}
    url = os.getenv("LLM_API_URL")
    headers = {"x-goog-api-key": os.getenv("LLM_API_KEY")}
    
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
        "generationConfig": {"responseMimeType": "application/json"}
    }

    try:
        resposta = requests.post(url, headers=headers, json=dados)
        if resposta.status_code in [400, 401, 403]:
                return {"erro": f"Credencial inválida ou sem permissão (código {resposta.status_code}). Verifique a LLM_API_KEY no arquivo .env."}
        if resposta.status_code==503:
            return {"erro": "Serviço indisponível (código 503). Tente novamente mais tarde."}
        resposta_json = resposta.json()
        if "candidates" in resposta_json:
            texto_ia = resposta_json["candidates"][0]["content"]["parts"][0]["text"]
            return json.loads(texto_ia)
        else:
            return {"erro": f"Aviso do servidor: {resposta_json}"}
            
    except Exception as e:
        return {"erro": f"Falha na comunicação com a API: {e}"}