import logging

from cliente_llm import analisar_texto

logging.basicConfig(
    filename="execucao.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    encoding="utf-8",
)
logger = logging.getLogger(__name__)
logger.info("Aplicação iniciada.")

conteudo = input("Digite o texto para verificação:\n").strip()

if not conteudo:
    logger.warning("Fim da execução.")
    print("Nenhum texto informado para análise.")
else:
    logger.info("Texto recebido (%d caracteres). Iniciando análise.", len(conteudo))
    analise = analisar_texto(conteudo)

    print("\n--- Análise da IA ---")

    if "erro" in analise:
        logger.error("Erro na análise: %s", analise["erro"])
        print(analise["erro"])
    else:
        logger.info(
            "Análise concluída. Classificação: %s, Nível de Risco: %s",
            analise.get("classificacao"),
            analise.get("nivel_risco"),
        )
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
