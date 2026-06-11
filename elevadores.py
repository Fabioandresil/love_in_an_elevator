# =============================================================
# elevadores.py — Estado e movimentação das cabines
# US-03: Estado dos elevadores | Regras 1, 3 e 4
# =============================================================

from config import POSICAO_INICIAL
import interface


def criar_elevadores():
    """
    Cria o estado inicial dos elevadores (Regra 1: o sistema
    conhece onde cada elevador está a qualquer momento).
    Estrutura: dicionário de dicionários, ex.:
        {"A": {"andar_atual": 0}, "B": {"andar_atual": 4}}
    Campos extras (ocupação, status) entram nas próximas sprints.
    """
    elevadores = {}
    for nome, andar in POSICAO_INICIAL.items():
        elevadores[nome] = {"andar_atual": andar}
    return elevadores


def mover_elevador(elevadores, nome_elevador, andar_destino):
    """
    Move um elevador andar a andar até o destino (Regra 3) e
    ATUALIZA o estado ao final (Regra 4: registrar a nova posição
    após cada movimentação).
    O laço for percorre os andares intermediários para que o log
    mostre o trajeto completo (Regra 6).
    """
    elevador = elevadores[nome_elevador]
    andar_atual = elevador["andar_atual"]

    if andar_atual == andar_destino:
        print(f"   🛗 Elevador {nome_elevador} já está no "
              f"{interface.nome_andar(andar_destino)}.")
        return

    # Define o sentido: +1 subindo, -1 descendo
    if andar_destino > andar_atual:
        passo = 1
        print(f"   ⬆️  Elevador {nome_elevador} SUBINDO de "
              f"{interface.nome_andar(andar_atual)} para "
              f"{interface.nome_andar(andar_destino)}")
    else:
        passo = -1
        print(f"   ⬇️  Elevador {nome_elevador} DESCENDO de "
              f"{interface.nome_andar(andar_atual)} para "
              f"{interface.nome_andar(andar_destino)}")

    # Percorre cada andar do trajeto, um a um
    for andar in range(andar_atual + passo, andar_destino + passo, passo):
        interface.log_passo(nome_elevador, andar)

    # Regra 4: atualizar o estado depois de TODA movimentação
    elevador["andar_atual"] = andar_destino
