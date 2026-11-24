with open('texto_recebido.txt','r',encoding='utf-8')as arquivo:
    conteudo=arquivo.read()
    print('Arquivo lido!')
    print(conteudo)