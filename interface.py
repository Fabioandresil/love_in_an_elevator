# =============================================================
# interface.py — Tudo que aparece na tela fica neste módulo
# Regra 6: Exibir Log | US-05/06 e logs das Sprints 2 e 3
# =============================================================

from config import NOMES_ANDARES, ICONES_PERFIL, CAPACIDADE_MAXIMA

LARGURA = 56  # largura padrão das molduras do terminal


def nome_andar(andar):
    """Nome amigável de um andar (ex.: 3 -> '3º Andar (Biblioteca)')."""
    return NOMES_ANDARES[andar]


def rotulo(chamada):
    """Identificação curta de um passageiro: ícone do perfil + nome."""
    return f"{ICONES_PERFIL[chamada['perfil']]} {chamada['usuario']}"


def exibir_titulo():
    print("=" * LARGURA)
    print("🏢  SISTEMA INTELIGENTE DE ELEVADORES — SENAC".center(LARGURA))
    print("Catraca integrada · Despacho por Destino · BI".center(LARGURA))
    print("Equipe: Eric · Diogo · Fabio · Yuri".center(LARGURA))
    print("=" * LARGURA)


def exibir_menu(caos_ativo):
    print()
    print("-" * LARGURA)
    print("MENU PRINCIPAL")
    print("  [1] Catraca — ENTRADA (informar matrícula)")
    print("  [2] Catraca — SAÍDA do prédio")
    print("  [3] Chamada manual (visitante sem cadastro)")
    print("  [4] Simular grupo chegando pela catraca")
    print("  [5] Processar embarques (despacho por destino)")
    print("  [6] Ver fila de chamadas")
    print("  [7] Ver status dos elevadores")
    print("  [8] Relatório BI da sessão")
    print(f"  [9] Modo Caos [{'LIGADO 🎲' if caos_ativo else 'desligado'}]")
    print("  [0] Encerrar o sistema")
    print("-" * LARGURA)


def exibir_status(elevadores):
    print()
    print("📊 STATUS ATUAL DOS ELEVADORES")
    icones_status = {"livre": "🟢", "ocupado": "🟡", "quebrado": "🔴"}
    for nome, elevador in elevadores.items():
        print(f"   {icones_status[elevador['status']]} Elevador {nome} "
              f"[{elevador['status']}] -> "
              f"{nome_andar(elevador['andar_atual'])}")


def exibir_fila(fila):
    print()
    if not fila:
        print("📭 FILA DE CHAMADAS: vazia")
        return
    print(f"📋 FILA DE CHAMADAS ({len(fila)} pendente(s)):")
    for posicao, chamada in enumerate(fila, start=1):
        extra = " [EXPRESSO]" if chamada["expresso"] else ""
        print(f"   {posicao}º) {rotulo(chamada)}: "
              f"{nome_andar(chamada['origem'])} -> "
              f"{nome_andar(chamada['destino'])}{extra}")


def log_catraca_entrada(usuario, expresso):
    """US-11: chamada antecipada gerada pela passagem na catraca."""
    extra = " — viagem EXPRESSA" if expresso else ""
    print(f"   🎫 Catraca identificou: {ICONES_PERFIL[usuario['perfil']]} "
          f"{usuario['nome']} ({usuario['perfil']}) — elevador acionado "
          f"para {nome_andar(usuario['andar_sala'])}{extra}")


def log_visitante(matricula):
    print(f"   ❓ Matrícula '{matricula}' não encontrada no cadastro. "
          f"Visitantes usam a opção [3] Chamada manual.")


def log_chamada_na_fila(chamada, posicao):
    print(f"   ✅ {rotulo(chamada)} entrou na fila — posição {posicao}º")


def log_rodada(numero, atribuicoes, restantes):
    """
    Painel de embarque da rodada (US-12): anuncia a qual elevador
    cada pessoa foi alocada — como nos sistemas de Destination
    Dispatch usados em prédios corporativos reais.
    """
    print()
    print("=" * LARGURA)
    print(f"🔄 RODADA {numero} — PAINEL DE EMBARQUE")
    for nome_elevador, passageiros, distancias in atribuicoes:
        nomes = ", ".join(rotulo(c) for c in passageiros)
        print(f"   🛗 Elevador {nome_elevador} "
              f"(distância {distancias[nome_elevador]}) -> "
              f"{len(passageiros)}/{CAPACIDADE_MAXIMA} passageiro(s):")
        print(f"      {nomes}")
    if restantes > 0:
        print(f"   ⏳ Aguardando próxima viagem: {restantes} chamada(s)")
    print("=" * LARGURA)


def log_busca(nome_elevador, passageiros):
    origem = passageiros[0]["origem"]
    print(f"🚶 Elevador {nome_elevador} indo buscar o grupo no "
          f"{nome_andar(origem)}")


def log_embarque_grupo(nome_elevador, andar, passageiros):
    nomes = ", ".join(rotulo(c) for c in passageiros)
    print(f"   🚪 EMBARQUE no {nome_andar(andar)}: {nomes} "
          f"(ocupação {len(passageiros)}/{CAPACIDADE_MAXIMA})")


def log_parada(nome_elevador, andar, descem, a_bordo):
    if descem:
        nomes = ", ".join(rotulo(c) for c in descem)
        print(f"   🏁 Parada no {nome_andar(andar)} — desembarcam: {nomes} "
              f"(seguem a bordo: {a_bordo})")


def log_fim_viagem(nome_elevador, andar):
    print(f"   ✅ Viagem concluída. Elevador {nome_elevador} livre no "
          f"{nome_andar(andar)}.")


def log_passo(nome_elevador, andar):
    """Movimentação andar a andar (Regra 6)."""
    print(f"      🛗 Elevador {nome_elevador} passando por: {nome_andar(andar)}")


def log_evento(mensagem):
    """Eventos do Modo Caos (US-18) e decisões da IA (US-20)."""
    print()
    print(f"   {mensagem}")


def log_erro(mensagem):
    print(f"   ❌ {mensagem}")


def log_despedida(caminho_csv):
    print()
    if caminho_csv:
        print(f"💾 Dados da sessão exportados para: {caminho_csv}")
    print("👋 Sistema encerrado. Obrigado por usar os Elevadores SENAC!")
