# =============================================================
# chamadas.py — Lógica de negócio das chamadas e viagens
# US-04 (abs) | US-05 | US-08 (fila) | US-09 (rodadas)
# US-12: Despacho por Destino | US-13: Capacidade | US-14: PCD
# =============================================================

from config import CAPACIDADE_MAXIMA, PRIORIDADES
import elevadores as mod_elevadores
import interface
import estatisticas
import ia_previsao

# Contador de chegada: garante o desempate FIFO dentro da
# mesma prioridade (quem chegou antes, embarca antes)
_ordem_chegada = 0


# -------------------------------------------------------------
# Criação e fila de chamadas (US-08)
# -------------------------------------------------------------

def criar_chamada(usuario, origem, destino, perfil="comum", expresso=False):
    """Cada chamada é um dicionário com os dados do atendimento."""
    global _ordem_chegada
    _ordem_chegada += 1
    return {
        "usuario": usuario,
        "origem": origem,
        "destino": destino,
        "perfil": perfil,        # comum | pcd | vip | funcionario
        "expresso": expresso,    # US-15: viagem VIP sem paradas
        "ordem": _ordem_chegada,
    }


def adicionar_na_fila(fila, chamada):
    """Adiciona ao final; a prioridade é aplicada no processamento."""
    fila.append(chamada)
    interface.log_chamada_na_fila(chamada, len(fila))


def ordenar_fila(fila):
    """
    US-14: ordena por prioridade do perfil (PCD primeiro) e, dentro
    da mesma prioridade, pela ordem de chegada (FIFO). O sort do
    Python é estável, então a justiça da fila é preservada.
    """
    fila.sort(key=lambda c: (PRIORIDADES[c["perfil"]], c["ordem"]))


# -------------------------------------------------------------
# Escolha do elevador (US-04 / Regra 2)
# -------------------------------------------------------------

def escolher_elevador(andar_usuario, elevadores, candidatos=None):
    """
    Menor distância via abs(posicao_elevador - andar_usuario).
    Desempate: ordem alfabética (decisão documentada para a banca).
    Retorna (nome_do_escolhido, dicionario_de_distancias).
    """
    if candidatos is None:
        candidatos = [n for n, e in elevadores.items()
                      if e["status"] == "livre"]

    distancias = {}
    for nome in candidatos:
        distancias[nome] = abs(elevadores[nome]["andar_atual"] - andar_usuario)

    escolhido = min(distancias, key=lambda nome: (distancias[nome], nome))
    return escolhido, distancias


# -------------------------------------------------------------
# Despacho por Destino (US-12): montagem das viagens em grupo
# -------------------------------------------------------------

def montar_viagem(fila, elevadores, candidatos):
    """
    Monta UMA viagem a partir da fila já ordenada por prioridade:
      1. A chamada mais prioritária define origem e sentido.
      2. VIP expresso viaja sozinho, sem paradas (US-15).
      3. Demais: agrupa quem está na MESMA origem indo no MESMO
         sentido, até a CAPACIDADE_MAXIMA (US-13). Quem exceder
         o limite permanece na fila para a próxima viagem.
      4. O elevador mais próximo da origem assume a viagem.
    Retorna (nome_elevador, lista_de_passageiros, distancias).
    """
    primeira = fila.pop(0)
    passageiros = [primeira]

    if not primeira["expresso"]:
        sentido_sobe = primeira["destino"] > primeira["origem"]
        # Varre a fila buscando companheiros de viagem compatíveis
        for chamada in list(fila):
            if len(passageiros) >= CAPACIDADE_MAXIMA:
                break  # cabine lotada: excedente fica para a próxima
            mesmo_local = chamada["origem"] == primeira["origem"]
            mesmo_sentido = (chamada["destino"] > chamada["origem"]) == sentido_sobe
            if mesmo_local and mesmo_sentido and not chamada["expresso"]:
                passageiros.append(chamada)
                fila.remove(chamada)

    escolhido, distancias = escolher_elevador(
        primeira["origem"], elevadores, candidatos
    )
    return escolhido, passageiros, distancias


# -------------------------------------------------------------
# Execução de uma viagem em grupo (US-05 + US-12 + US-13)
# -------------------------------------------------------------

def executar_viagem_grupo(nome_elevador, passageiros, elevadores):
    """
    Executa a viagem completa: busca na origem, embarque do grupo,
    paradas em cada destino (no sentido do movimento) e registro
    nas estatísticas (US-19) e na memória da IA (US-20).
    """
    elevadores[nome_elevador]["status"] = "ocupado"
    origem = passageiros[0]["origem"]

    # Busca: elevador vai até a origem do grupo
    print()
    interface.log_busca(nome_elevador, passageiros)
    mod_elevadores.mover_elevador(elevadores, nome_elevador, origem)
    interface.log_embarque_grupo(nome_elevador, origem, passageiros)

    # Paradas: destinos ordenados no sentido do deslocamento
    sentido_sobe = passageiros[0]["destino"] > origem
    paradas = sorted({c["destino"] for c in passageiros},
                     reverse=not sentido_sobe)

    a_bordo = list(passageiros)
    for parada in paradas:
        mod_elevadores.mover_elevador(elevadores, nome_elevador, parada)
        descem = [c for c in a_bordo if c["destino"] == parada]
        a_bordo = [c for c in a_bordo if c["destino"] != parada]
        interface.log_parada(nome_elevador, parada, descem, len(a_bordo))
        for chamada in descem:
            ia_previsao.registrar_destino(parada)  # alimenta a IA

    estatisticas.registrar_viagem(nome_elevador, origem, paradas, passageiros)
    elevadores[nome_elevador]["status"] = "livre"
    interface.log_fim_viagem(nome_elevador,
                             elevadores[nome_elevador]["andar_atual"])


# -------------------------------------------------------------
# Processamento da fila em rodadas (US-08 + US-09 + US-18)
# -------------------------------------------------------------

def processar_fila(fila, elevadores, caos_ativo=False):
    """
    Atende TODAS as chamadas pendentes em rodadas de paralelo
    lógico: em cada rodada, cada elevador operante assume UMA
    viagem em grupo. Eventos do Modo Caos (US-18) podem quebrar
    e consertar elevadores entre as rodadas.
    """
    import eventos  # importado aqui para evitar dependência circular

    if not fila:
        interface.log_erro("A fila está vazia — nada a processar.")
        return

    rodada = 0
    while fila:  # laço principal: enquanto houver chamadas pendentes
        rodada += 1

        # Modo Caos: sorteia pane/conserto e garante 1 elevador operante
        eventos.sortear_evento(elevadores, caos_ativo)
        eventos.garantir_elevador_operante(elevadores)

        # US-14: prioridade (PCD > VIP > funcionário > comum) + FIFO
        ordenar_fila(fila)

        # Monta as viagens da rodada (uma por elevador livre)
        atribuicoes = []
        disponiveis = [n for n, e in elevadores.items()
                       if e["status"] == "livre"]
        while fila and disponiveis:
            escolhido, passageiros, distancias = montar_viagem(
                fila, elevadores, disponiveis
            )
            disponiveis.remove(escolhido)
            atribuicoes.append((escolhido, passageiros, distancias))

        # Anuncia o painel de embarque (como no Destination Dispatch real)
        interface.log_rodada(rodada, atribuicoes, restantes=len(fila))

        # Executa as viagens da rodada
        for nome_elevador, passageiros, _ in atribuicoes:
            executar_viagem_grupo(nome_elevador, passageiros, elevadores)

    print()
    print("🎉 Fila totalmente atendida!")

    # US-20: IA reposiciona um elevador para o andar mais demandado
    ia_previsao.reposicionar(elevadores)
