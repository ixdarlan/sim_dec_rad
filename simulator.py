import random

def simular_decaimento_radioativo(qtd_inicial: int, taxa: float, anos: int):
    quantidade_nucleos = [qtd_inicial]
    anos_passados = [0]
    nucleos_restantes = qtd_inicial
    log = [f"Ano 0: {qtd_inicial} núcleos restantes"]

    for ano in range(1, anos + 1):
        sobreviventes = sum(1 for _ in range(nucleos_restantes) if random.random() > taxa)
        nucleos_restantes = sobreviventes
        anos_passados.append(ano)
        quantidade_nucleos.append(nucleos_restantes)
        log.append(f"Ano {ano}: {nucleos_restantes} núcleos restantes")

    return anos_passados, quantidade_nucleos, log
