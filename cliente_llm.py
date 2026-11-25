import os
import requests
from dotenv import load_dotenv

load_dotenv()

url = os.getenv("LLM_API_URL")
headers = {"x-goog-api-key": os.getenv("LLM_API_KEY")}
dados = {"contents": [{"parts": [{"text": "Cite seis palavras que podem indicar uma fake news?"}]}]}

resposta = requests.post(url, headers=headers, json=dados).json()

if "candidates" in resposta:
    print(resposta["candidates"][0]["content"]["parts"][0]["text"])
else:
    print("Aviso do servidor:", resposta)