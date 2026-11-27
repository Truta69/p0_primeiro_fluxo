Este aplicativo, feito em Python, recebe um texto pelo terminal e verifica indícios de que possa se tratar de um texto fake.

Estrutura do projeto:
leitor.py: Arquivo principal do projeto que interage com o usuário. Primeiro, recebe o texto para ser verificado e, depois, retorna uma análise indicando se esse texto apresenta sinais de fake ou não. Também faz a validação do texto e da resposta.
cliente_llm.py: Aqui é onde ocorre a comunicação efetiva com a API e onde ocorrem os tratamentos de erros.
O requirements.txt é o lugar onde as bibliotecas do projeto ficam. O .env.example é o arquivo com as configurações necessárias para o projeto.

Para executar:
Faça o clone do repositório do GitHub, [https://github.com/Truta69/p0_primeiro_fluxo](https://github.com/Truta69/p0_primeiro_fluxo). Depois, na pasta salva (atenção para abrir na mesma pasta), abra-a pelo Git Bash (ou terminal do VS Code) e configure o ambiente virtual para a execução do app com "python -m venv venv" e "source venv/Scripts/activate". Por fim, instale os pacotes (pip install -r requirements.txt), crie o .env baseado no .env.example, coloque sua chave de acesso à LLM e a URL da API e, depois, rode no terminal (VS Code) python leitor.py.