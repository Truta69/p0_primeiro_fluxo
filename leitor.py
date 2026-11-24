with open('texto_recebido.txt','r',encoding='utf-8')as arquivo:
    conteudo=arquivo.read().strip()
    if not conteudo:
        print('Texto para leitura está vazio!')
    else:
        print('Texto válido:')
    print(conteudo)