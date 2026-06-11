# =============================================================
# chamadas.py — Lógica de negócio de uma chamada de elevador
# US-04: Escolha do mais próximo | US-05: Movimentação completa
# Regra 2: Calcular Distância com abs()
# =============================================================

import elevadores as mod_elevadores
import interface


def escolher_elevador(andar_usuario, elevadores):
    """
    Decide qual elevador atende a chamada (US-04).
    Critério: MENOR distância até o usuário, calculada com
    abs(posicao_elevador - andar_usuario)  -> Regra 2 do desafio.

    Critério de desempate (decisão de projeto, documentada para a
    banca): em caso de empate vence o elevador de nome alfabético
    menor ("A"), garantindo comportamento previsível e testável.

    Retorna: (nome_do_escolhido, dicionario_de_distancias)
    """
    distancias = {}
    for nome, elevador in elevadores.items():
        distancias[nome] = abs(elevador["andar_atual"] - andar_usuario)

    # min() com chave dupla: 1º menor distância, 2º ordem alfabética
    escolhido = min(distancias, key=lambda nome: (distancias[nome], nome))
    return escolhido, distancias


def atender_chamada(origem, destino, elevadores):
    """
    Executa o ciclo de vida completo de uma chamada, reproduzindo
    as 4 etapas da simulação oficial do PDF:
      1. Chamada Recebida
      2. Escolha do Elevador
      3. Embarque (elevador vai até o usuário)
      4. Viagem ao destino + Desembarque
    """
    # Etapa 1 — Chamada recebida
    interface.log_chamada_recebida(origem, destino)

    # Etapa 2 — Escolha do elevador mais próximo (abs)
    escolhido, distancias = escolher_elevador(origem, elevadores)
    interface.log_escolha(escolhido, distancias)

    # Etapa 3 — Busca e embarque: elevador vai até o andar do usuário
    print()
    print("🚶 BUSCA DO PASSAGEIRO")
    mod_elevadores.mover_elevador(elevadores, escolhido, origem)
    interface.log_embarque(escolhido, origem)

    # Etapa 4 — Viagem ao destino e desembarque
    print()
    print("🎯 VIAGEM AO DESTINO")
    mod_elevadores.mover_elevador(elevadores, escolhido, destino)
    interface.log_desembarque(escolhido, destino)
