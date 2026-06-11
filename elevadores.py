# =============================================================
# elevadores.py — Estado e movimentação das cabines
# US-03 | Regras 1, 3 e 4 | Sprint 3: status "quebrado" (US-18)
# =============================================================

from config import POSICAO_INICIAL
import interface


def criar_elevadores():
    """
    Estado inicial dos elevadores (Regra 1: o sistema conhece
    onde cada elevador está a qualquer momento).
      status: livre | ocupado | quebrado
      andares_percorridos: alimenta o relatório BI (US-19)
    """
    elevadores = {}
    for nome, andar in POSICAO_INICIAL.items():
        elevadores[nome] = {
            "andar_atual": andar,
            "status": "livre",
            "andares_percorridos": 0,
        }
    return elevadores


def mover_elevador(elevadores, nome_elevador, andar_destino):
    """
    Move um elevador andar a andar até o destino (Regra 3) e
    ATUALIZA o estado ao final (Regra 4). O laço for mostra o
    trajeto completo no terminal (Regra 6).
    """
    elevador = elevadores[nome_elevador]
    andar_atual = elevador["andar_atual"]

    if andar_atual == andar_destino:
        print(f"   🛗 Elevador {nome_elevador} já está no "
              f"{interface.nome_andar(andar_destino)}.")
        return

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

    for andar in range(andar_atual + passo, andar_destino + passo, passo):
        interface.log_passo(nome_elevador, andar)

    # Regra 4: atualizar o estado depois de TODA movimentação
    elevador["andares_percorridos"] += abs(andar_destino - andar_atual)
    elevador["andar_atual"] = andar_destino
