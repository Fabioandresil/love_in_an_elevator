# =============================================================
# ia_previsao.py — IA Simples (US-20 / nível Hacker)
# =============================================================
# "Aprende os andares mais chamados e posiciona o elevador
# estrategicamente" (card oficial IA Simples + Economia de
# Energia). A técnica é um contador de frequência de destinos:
# quanto mais um andar é demandado, maior a chance de o próximo
# usuário querer ir até lá — então um elevador ocioso já espera
# por perto, reduzindo o tempo de resposta (dor: 'Demora').

import interface

# Memória da IA: {andar: quantidade de vezes que foi destino}
_frequencia_destinos = {}


def registrar_destino(andar):
    """Alimenta a memória a cada desembarque."""
    _frequencia_destinos[andar] = _frequencia_destinos.get(andar, 0) + 1


def andar_mais_demandado():
    """Retorna o andar 'quente' ou None se ainda não há histórico."""
    if not _frequencia_destinos:
        return None
    return max(_frequencia_destinos, key=_frequencia_destinos.get)


def obter_frequencias():
    """Exposto para o relatório BI (US-21)."""
    return dict(_frequencia_destinos)


def reposicionar(elevadores):
    """
    Pré-posicionamento: ao final do processamento da fila, se
    nenhum elevador livre está no andar mais demandado, o mais
    próximo dele se desloca para lá e fica de prontidão.
    """
    quente = andar_mais_demandado()
    if quente is None:
        return

    livres = {n: e for n, e in elevadores.items() if e["status"] == "livre"}
    if not livres:
        return

    # Já existe elevador de prontidão no andar quente? Nada a fazer.
    if any(e["andar_atual"] == quente for e in livres.values()):
        return

    # Move o elevador livre mais próximo (Regra 2: abs)
    nome = min(livres, key=lambda n: (abs(livres[n]["andar_atual"] - quente), n))
    interface.log_evento(
        f"🤖 IA: andar mais demandado é {interface.nome_andar(quente)} "
        f"({_frequencia_destinos[quente]} chamada(s)). Elevador {nome} "
        f"reposicionado para prontidão."
    )
    import elevadores as mod_elevadores
    mod_elevadores.mover_elevador(elevadores, nome, quente)
