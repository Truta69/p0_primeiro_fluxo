import os
import requests
from dotenv import load_dotenv

load_dotenv()

with open('texto_recebido.txt', 'r', encoding='utf-8') as arquivo:
    conteudo = arquivo.read().strip()

if not conteudo:
    print('Texto para leitura está vazio!')
else:
    print('Texto para análise:')
    print(conteudo)

    url = os.getenv('LLM_API_URL')
    headers = {'x-goog-api-key': os.getenv('LLM_API_KEY')}
    prompt = (
        'Analise a mensagem abaixo e explique, em um parágrafo de curto'
        'de leitura fácil para um leigo, se há sinais de fake news ou golpe e por quê. '
        'Escreva em texto limpo, sem usar asteriscos, negrito ou tópicos:\n\n'
        f'{conteudo}'
    )
    dados = {'contents':[{'parts':[{'text':prompt}]}],
             'generationConfig': {'maxOutputTokens': 1000}}

    resposta = requests.post(url, headers=headers, json=dados).json()

    print('\n--- Análise da IA ---')
    if 'candidates' in resposta:
        print(resposta['candidates'][0]['content']['parts'][0]['text'])
    else:
        print('Aviso do servidor:', resposta)