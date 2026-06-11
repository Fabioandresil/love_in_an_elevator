# =============================================================
# chamadas.py — Lógica de negócio das chamadas de elevador
# US-04: Escolha do mais próximo | US-05: Movimentação completa
# Sprint 2 -> US-08: Fila de chamadas | US-09: Múltiplos usuários
# Regra 2: Calcular Distância com abs()
# =============================================================

import elevadores as mod_elevadores
import interface


# -------------------------------------------------------------
# Criação e fila de chamadas (US-08)
# -------------------------------------------------------------

def criar_chamada(usuario, origem, destino):
    """Cada chamada é um dicionário com os dados do atendimento."""
    return {"usuario": usuario, "origem": origem, "destino": destino}


def adicionar_na_fila(fila, chamada):
    """
    Adiciona a chamada ao FINAL da lista (FIFO: quem chega primeiro
    é atendido primeiro — dor do cliente: 'Filas Eternas').
    """
    fila.append(chamada)
    posicao = len(fila)
    interface.log_chamada_na_fila(chamada, posicao)


# -------------------------------------------------------------
# Escolha do elevador (US-04 / Regra 2)
# -------------------------------------------------------------

def escolher_elevador(andar_usuario, elevadores, candidatos=None):
    """
    Decide qual elevador atende a chamada.
    Critério: MENOR distância até o usuário, calculada com
    abs(posicao_elevador - andar_usuario)  -> Regra 2 do desafio.

    'candidatos' permite restringir a escolha aos elevadores ainda
    livres na rodada (US-09). Se None, considera todos.

    Critério de desempate (decisão de projeto, documentada para a
    banca): em caso de empate vence o elevador de nome alfabético
    menor ("A"), garantindo comportamento previsível e testável.

    Retorna: (nome_do_escolhido, dicionario_de_distancias)
    """
    if candidatos is None:
        candidatos = list(elevadores.keys())

    distancias = {}
    for nome in candidatos:
        distancias[nome] = abs(elevadores[nome]["andar_atual"] - andar_usuario)

    # min() com chave dupla: 1º menor distância, 2º ordem alfabética
    escolhido = min(distancias, key=lambda nome: (distancias[nome], nome))
    return escolhido, distancias


# -------------------------------------------------------------
# Execução de uma viagem (US-05)
# -------------------------------------------------------------

def executar_viagem(nome_elevador, chamada, elevadores):
    """
    Executa as etapas 3 e 4 da simulação oficial do PDF:
    busca do passageiro -> embarque -> viagem -> desembarque.
    Atualiza o status do elevador durante o atendimento.
    """
    elevadores[nome_elevador]["status"] = "ocupado"

    print()
    print(f"🚶 BUSCA DO PASSAGEIRO — {chamada['usuario']}")
    mod_elevadores.mover_elevador(elevadores, nome_elevador, chamada["origem"])
    interface.log_embarque(nome_elevador, chamada["origem"], chamada["usuario"])

    print()
    print(f"🎯 VIAGEM AO DESTINO — {chamada['usuario']}")
    mod_elevadores.mover_elevador(elevadores, nome_elevador, chamada["destino"])
    interface.log_desembarque(nome_elevador, chamada["destino"],
                              chamada["usuario"])

    elevadores[nome_elevador]["status"] = "livre"


def atender_chamada_imediata(chamada, elevadores):
    """
    Atendimento direto (comportamento da Sprint 1), agora com
    usuário identificado. Reproduz as 4 etapas do PDF.
    """
    interface.log_chamada_recebida(chamada)
    escolhido, distancias = escolher_elevador(chamada["origem"], elevadores)
    interface.log_escolha(escolhido, distancias)
    executar_viagem(escolhido, chamada, elevadores)


# -------------------------------------------------------------
# Processamento da fila em rodadas (US-08 + US-09)
# -------------------------------------------------------------

def processar_fila(fila, elevadores):
    """
    Atende TODAS as chamadas pendentes em rodadas de paralelo
    lógico: em cada rodada, cada elevador livre assume UMA chamada
    da fila (na ordem FIFO), e a mais antiga fica com o elevador
    mais próximo. Assim os dois elevadores trabalham juntos,
    atacando as dores 'Filas Eternas' e 'Caos no Pico'.
    """
    if not fila:
        interface.log_erro("A fila está vazia — nada a processar.")
        return

    rodada = 0
    while fila:  # laço principal: enquanto houver chamadas pendentes
        rodada += 1

        # 1) Monta a rodada: distribui chamadas entre elevadores livres
        atribuicoes = []
        disponiveis = [nome for nome, e in elevadores.items()
                       if e["status"] == "livre"]

        while fila and disponiveis:
            chamada = fila.pop(0)  # FIFO: remove a mais antiga
            escolhido, distancias = escolher_elevador(
                chamada["origem"], elevadores, candidatos=disponiveis
            )
            disponiveis.remove(escolhido)  # cada elevador, 1 chamada/rodada
            atribuicoes.append((escolhido, chamada, distancias))

        # 2) Anuncia as alocações da rodada (quem atende quem)
        interface.log_rodada(rodada, atribuicoes, restantes=len(fila))

        # 3) Executa as viagens da rodada
        for nome_elevador, chamada, _ in atribuicoes:
            executar_viagem(nome_elevador, chamada, elevadores)

    print()
    print("🎉 Fila totalmente atendida!")
