import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

conteudo=input('Digite o texto para verificação :').strip()

if not conteudo:
    print('Texto para leitura está vazio!')
else:
    print('Texto para análise:')
    print(conteudo)
    url = os.getenv('LLM_API_URL')
    headers = {'x-goog-api-key': os.getenv('LLM_API_KEY')}
    prompt = (
        'Analise a mensagem abaixo e responda ESTRITAMENTE neste formato JSON:\n'
        '{\n' 
        '"classificacao": "Seguro | Suspeito | Golpe ou Fake News",\n'
        '"nivel_risco": 0,\n'
        '"sinais_alerta": ["sinal 1", "sinal 2"],\n'
        '"explicacao": "explicação simples em um parágrafo curto para um leigo"\n'
        '}\n\n'
        f'mensagem:\n{conteudo}'
    )
    dados = {'contents': [{'parts': [{'text': prompt}]}],
        'generationConfig': {
            'maxOutputTokens': 1000,
            'responseMimeType': 'application/json'
        }}

    resposta = requests.post(url, headers=headers, json=dados).json()

    print('\n--- Análise da IA ---')
    if 'candidates' in resposta:
        texto_json = resposta['candidates'][0]['content']['parts'][0]['text']
        try:
            analise = json.loads(texto_json)
            print(f"Classificação: {analise.get('classificacao')}")
            print(f"Nível de Risco: {analise.get('nivel_risco')}/10")
            print("Sinais de Alerta:")
            for sinal in analise.get('sinais_alerta', []):
                print(f"  - {sinal}")
            print(f"Explicação: {analise.get('explicacao')}")
        except json.JSONDecodeError:
            print("Erro ao ler o formato JSON da IA:", texto_json)
    else:
        print('Aviso do servidor:', resposta)