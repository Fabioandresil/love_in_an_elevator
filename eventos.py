# =============================================================
# eventos.py — Modo Caos da Faculdade (US-18)
# =============================================================
# Usa o módulo random (sugestão oficial do PDF) para simular
# imprevistos reais: elevador quebra e é consertado. Quando um
# elevador quebra, suas chamadas são automaticamente atendidas
# pelo outro — pois só elevadores LIVRES recebem viagens.

import random

from config import CHANCE_EVENTO_CAOS
import interface


def sortear_evento(elevadores, caos_ativo):
    """Chamado no início de cada rodada de processamento."""
    if not caos_ativo:
        return

    if random.random() > CHANCE_EVENTO_CAOS:
        return  # rodada tranquila, sem evento

    quebrados = [n for n, e in elevadores.items() if e["status"] == "quebrado"]
    livres = [n for n, e in elevadores.items() if e["status"] == "livre"]

    # Se já há elevador quebrado, o evento é o conserto dele
    if quebrados:
        nome = random.choice(quebrados)
        elevadores[nome]["status"] = "livre"
        interface.log_evento(f"🔧 Manutenção concluída: Elevador {nome} "
                             f"voltou a operar!")
    elif livres:
        nome = random.choice(livres)
        elevadores[nome]["status"] = "quebrado"
        interface.log_evento(f"💥 PANE! Elevador {nome} quebrou — chamadas "
                             f"redirecionadas para o outro elevador.")


def garantir_elevador_operante(elevadores):
    """
    Trava de segurança: se TODOS quebrarem com fila pendente,
    aciona a manutenção de emergência para não travar o sistema.
    """
    livres = [n for n, e in elevadores.items() if e["status"] == "livre"]
    if livres:
        return
    nome = list(elevadores.keys())[0]
    elevadores[nome]["status"] = "livre"
    interface.log_evento(f"🚒 Manutenção de EMERGÊNCIA: Elevador {nome} "
                         f"religado para atender a fila.")
