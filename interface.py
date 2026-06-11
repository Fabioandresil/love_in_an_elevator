# =============================================================
# interface.py — Tudo que aparece na tela fica neste módulo
# US-05 (log) e US-06 (menu) | Regra 6: Exibir Log
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
    """Menu principal do operador (US-06)."""
    print()
    print("-" * LARGURA)
    print("MENU PRINCIPAL")
    print("  [1] Nova chamada de elevador")
    print("  [2] Ver status dos elevadores")
    print("  [0] Encerrar o sistema")
    print("-" * LARGURA)


def exibir_status(elevadores):
    """Painel com a posição atual de cada elevador (US-03 / US-06)."""
    print()
    print("📊 STATUS ATUAL DOS ELEVADORES")
    for nome, elevador in elevadores.items():
        print(f"   🛗 Elevador {nome} -> {nome_andar(elevador['andar_atual'])}")


def log_chamada_recebida(origem, destino):
    """Etapa 1 da simulação do PDF: Chamada Recebida."""
    print()
    print("📞 CHAMADA RECEBIDA")
    print(f"   Origem : {nome_andar(origem)}")
    print(f"   Destino: {nome_andar(destino)}")


def log_escolha(escolhido, distancias):
    """Etapa 2: Escolha do Elevador — mostra o cálculo com abs() (Regra 2)."""
    print()
    print("🧠 ESCOLHA DO ELEVADOR (distância = abs(elevador - usuário))")
    for nome, distancia in distancias.items():
        marcador = "✅" if nome == escolhido else "  "
        print(f"   {marcador} Elevador {nome}: distância de {distancia} andar(es)")
    print(f"   ➡️  Elevador {escolhido} selecionado por estar mais próximo.")


def log_passo(nome_elevador, andar):
    """Movimentação andar a andar (Regra 6: cada etapa de forma clara)."""
    print(f"      🛗 Elevador {nome_elevador} passando por: {nome_andar(andar)}")


def log_embarque(nome_elevador, andar):
    """Etapa 3: Embarque."""
    print(f"   🚪 Portas abertas — EMBARQUE no Elevador {nome_elevador} "
          f"({nome_andar(andar)})")


def log_desembarque(nome_elevador, andar):
    """Etapa 4: Desembarque no destino."""
    print(f"   🏁 Portas abertas — DESEMBARQUE ({nome_andar(andar)})")
    print(f"   ✅ Viagem concluída. Elevador {nome_elevador} aguardando "
          f"no {nome_andar(andar)}.")


def log_erro(mensagem):
    """Mensagens de erro padronizadas (US-02)."""
    print(f"   ❌ {mensagem}")


def log_despedida():
    print()
    print("👋 Sistema encerrado. Obrigado por usar os Elevadores SENAC!")
