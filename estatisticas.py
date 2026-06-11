# =============================================================
# estatisticas.py — Coleta de dados e relatório BI (US-19/US-21)
# Premissa 7 do escopo: app com BI de uso dos elevadores
# =============================================================

from config import NOMES_ANDARES, ICONES_PERFIL, CAPACIDADE_MAXIMA
import ia_previsao

# Cada viagem registrada: dicionário com os dados do atendimento
_viagens = []


def registrar_viagem(nome_elevador, origem, paradas, passageiros):
    """Chamado ao final de cada viagem concluída."""
    _viagens.append({
        "elevador": nome_elevador,
        "origem": origem,
        "paradas": list(paradas),
        "qtd_passageiros": len(passageiros),
        "perfis": [p["perfil"] for p in passageiros],
        "nomes": [p["usuario"] for p in passageiros],
    })


def _barra(valor, maximo, largura=20):
    """Gráfico de barras em ASCII para o terminal."""
    if maximo == 0:
        return ""
    cheio = int(round(largura * valor / maximo))
    return "█" * cheio


def exibir_relatorio(elevadores):
    """Relatório BI completo no terminal (US-21)."""
    print()
    print("=" * 56)
    print("📈 RELATÓRIO BI — USO DOS ELEVADORES NA SESSÃO".center(56))
    print("=" * 56)

    if not _viagens:
        print("   Nenhuma viagem registrada ainda.")
        return

    total_pax = sum(v["qtd_passageiros"] for v in _viagens)
    print(f"\n🧮 Viagens realizadas: {len(_viagens)} | "
          f"Passageiros transportados: {total_pax}")

    # --- Uso por elevador -----------------------------------
    print("\n🛗 USO POR ELEVADOR")
    for nome, elevador in elevadores.items():
        viagens_elev = [v for v in _viagens if v["elevador"] == nome]
        pax = sum(v["qtd_passageiros"] for v in viagens_elev)
        print(f"   Elevador {nome}: {len(viagens_elev)} viagem(ns), "
              f"{pax} passageiro(s), "
              f"{elevador['andares_percorridos']} andar(es) percorrido(s)")

    # --- Ranking de andares mais demandados (memória da IA) --
    frequencias = ia_previsao.obter_frequencias()
    if frequencias:
        print("\n🏢 ANDARES MAIS DEMANDADOS (destinos)")
        maximo = max(frequencias.values())
        ordenado = sorted(frequencias.items(), key=lambda i: -i[1])
        for andar, qtd in ordenado:
            print(f"   {NOMES_ANDARES[andar]:<32} {qtd:>2}x "
                  f"{_barra(qtd, maximo)}")

    # --- Atendimentos por perfil ------------------------------
    print("\n👥 ATENDIMENTOS POR PERFIL")
    contagem = {}
    for viagem in _viagens:
        for perfil in viagem["perfis"]:
            contagem[perfil] = contagem.get(perfil, 0) + 1
    for perfil, qtd in sorted(contagem.items(), key=lambda i: -i[1]):
        print(f"   {ICONES_PERFIL[perfil]} {perfil:<12} {qtd:>2} pessoa(s)")

    # --- Ocupação média (eficiência das viagens) -------------
    ocupacao_media = total_pax / len(_viagens)
    percentual = 100 * ocupacao_media / CAPACIDADE_MAXIMA
    print(f"\n📦 Ocupação média: {ocupacao_media:.1f} de "
          f"{CAPACIDADE_MAXIMA} lugares ({percentual:.0f}%)")
    print("=" * 56)


def exportar_csv(caminho="relatorio_uso_elevadores.csv"):
    """
    Exporta as viagens para CSV ao encerrar (US-19) — base para
    o futuro dashboard web (US-22, roadmap).
    """
    if not _viagens:
        return None
    with open(caminho, "w", encoding="utf-8") as arquivo:
        arquivo.write("viagem;elevador;origem;paradas;passageiros;perfis;nomes\n")
        for numero, v in enumerate(_viagens, start=1):
            arquivo.write(
                f"{numero};{v['elevador']};{v['origem']};"
                f"{'|'.join(str(p) for p in v['paradas'])};"
                f"{v['qtd_passageiros']};"
                f"{'|'.join(v['perfis'])};"
                f"{'|'.join(v['nomes'])}\n"
            )
    return caminho
