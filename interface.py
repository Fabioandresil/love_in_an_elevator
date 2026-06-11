# =============================================================
# interface.py — Tudo que aparece na tela fica neste módulo
# US-05/US-06 | Sprint 2: logs de fila, lote e rodadas
# Regra 6: Exibir Log
# =============================================================
# Separar a exibição da lógica facilita trocar o terminal por
# uma interface gráfica no futuro sem mexer no resto do código.

from config import NOMES_ANDARES

LARGURA = 56  # largura padrão das molduras do terminal


def nome_andar(andar):
    """Retorna o nome amigável de um andar (ex.: 3 -> '3º Andar (Biblioteca)')."""
    return NOMES_ANDARES[andar]


def exibir_titulo():
    """Cabeçalho exibido uma vez, na abertura do sistema."""
    print("=" * LARGURA)
    print("🏢  SISTEMA INTELIGENTE DE ELEVADORES — SENAC".center(LARGURA))
    print("Gincana Python — Equipe Eric · Diogo · Fabio · Yuri".center(LARGURA))
    print("=" * LARGURA)


def exibir_menu():
    """Menu principal do operador (US-06, ampliado na Sprint 2)."""
    print()
    print("-" * LARGURA)
    print("MENU PRINCIPAL")
    print("  [1] Chamada imediata (atende na hora)")
    print("  [2] Adicionar chamada à fila")
    print("  [3] Modo lote (registrar várias chamadas)")
    print("  [4] Processar fila de chamadas")
    print("  [5] Ver fila de chamadas")
    print("  [6] Ver status dos elevadores")
    print("  [0] Encerrar o sistema")
    print("-" * LARGURA)


def exibir_status(elevadores):
    """Painel com a posição e o status de cada elevador (US-03)."""
    print()
    print("📊 STATUS ATUAL DOS ELEVADORES")
    for nome, elevador in elevadores.items():
        print(f"   🛗 Elevador {nome} [{elevador['status']}] -> "
              f"{nome_andar(elevador['andar_atual'])}")


def exibir_fila(fila):
    """Mostra a fila atual com a posição de cada pessoa (US-08)."""
    print()
    if not fila:
        print("📭 FILA DE CHAMADAS: vazia")
        return
    print(f"📋 FILA DE CHAMADAS ({len(fila)} pendente(s), ordem de chegada):")
    for posicao, chamada in enumerate(fila, start=1):
        print(f"   {posicao}º) {chamada['usuario']}: "
              f"{nome_andar(chamada['origem'])} -> "
              f"{nome_andar(chamada['destino'])}")


def log_chamada_recebida(chamada):
    """Etapa 1 da simulação do PDF: Chamada Recebida."""
    print()
    print(f"📞 CHAMADA RECEBIDA — {chamada['usuario']}")
    print(f"   Origem : {nome_andar(chamada['origem'])}")
    print(f"   Destino: {nome_andar(chamada['destino'])}")


def log_chamada_na_fila(chamada, posicao):
    """Confirmação de entrada na fila (US-08)."""
    print(f"   ✅ {chamada['usuario']} entrou na fila — posição {posicao}º "
          f"({nome_andar(chamada['origem'])} -> "
          f"{nome_andar(chamada['destino'])})")


def log_escolha(escolhido, distancias):
    """Etapa 2: Escolha do Elevador — mostra o cálculo com abs() (Regra 2)."""
    print()
    print("🧠 ESCOLHA DO ELEVADOR (distância = abs(elevador - usuário))")
    for nome, distancia in distancias.items():
        marcador = "✅" if nome == escolhido else "  "
        print(f"   {marcador} Elevador {nome}: distância de {distancia} andar(es)")
    print(f"   ➡️  Elevador {escolhido} selecionado por estar mais próximo.")


def log_rodada(numero, atribuicoes, restantes):
    """
    Anuncia a rodada de atendimento paralelo (US-09): qual elevador
    atende qual usuário, com a distância calculada via abs().
    """
    print()
    print("=" * LARGURA)
    print(f"🔄 RODADA {numero} — atendimento em paralelo")
    for nome_elevador, chamada, distancias in atribuicoes:
        print(f"   🛗 Elevador {nome_elevador} -> {chamada['usuario']} "
              f"(distância {distancias[nome_elevador]} andar(es))")
    if restantes > 0:
        print(f"   ⏳ Aguardando próxima rodada: {restantes} chamada(s)")
    print("=" * LARGURA)


def log_passo(nome_elevador, andar):
    """Movimentação andar a andar (Regra 6: cada etapa de forma clara)."""
    print(f"      🛗 Elevador {nome_elevador} passando por: {nome_andar(andar)}")


def log_embarque(nome_elevador, andar, usuario):
    """Etapa 3: Embarque."""
    print(f"   🚪 Portas abertas — {usuario} EMBARCA no Elevador "
          f"{nome_elevador} ({nome_andar(andar)})")


def log_desembarque(nome_elevador, andar, usuario):
    """Etapa 4: Desembarque no destino."""
    print(f"   🏁 Portas abertas — {usuario} DESEMBARCA "
          f"({nome_andar(andar)})")
    print(f"   ✅ Viagem concluída. Elevador {nome_elevador} aguardando "
          f"no {nome_andar(andar)}.")


def log_erro(mensagem):
    """Mensagens de erro padronizadas (US-02)."""
    print(f"   ❌ {mensagem}")


def log_despedida():
    print()
    print("👋 Sistema encerrado. Obrigado por usar os Elevadores SENAC!")
