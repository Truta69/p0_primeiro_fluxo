from cliente_llm import analisar_texto

conteudo = input("Digite o texto para verificação:\n").strip()

if not conteudo:
    print("Nenhum texto informado para análise.")
else:
    analise = analisar_texto(conteudo)

    print("\n--- Análise da IA ---")

    if "erro" in analise:
        print(analise["erro"])
    else:
        print(f"Classificação: {analise.get('classificacao')}")
        print(f"Nível de Risco: {analise.get('nivel_risco')}/10")

        sinais = analise.get("sinais_alerta", [])
        if sinais:
            print("Sinais de Alerta:")
            for sinal in sinais:
                print(f"  - {sinal}")
        else:
            print("Sinais de Alerta: Nenhum identificado.")

        print(f"Explicação: {analise.get('explicacao')}")
