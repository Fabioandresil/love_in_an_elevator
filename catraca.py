# =============================================================
# catraca.py — Integração com a catraca inteligente (US-11)
# =============================================================
# O SENAC já possui catraca com identificação na entrada. Este
# módulo SIMULA os eventos que ela gera: quando alguém passa, o
# sistema consulta o cadastro e cria a chamada AUTOMATICAMENTE
# (Térreo -> andar da sala), sem que a pessoa aperte nada.
# Em produção, bastaria substituir este simulador pelo conector
# do hardware — a interface das funções seria idêntica.

import random

from config import ANDAR_CATRACA, ICONES_PERFIL, SENHA_VIP
import cadastro
import chamadas
import interface


def entrada(matricula, fila, senha_automatica=False):
    """
    Evento: pessoa cadastrada PASSOU pela catraca de entrada.
    Cria a chamada Térreo -> andar da sala cadastrada (US-11).
    Perfil VIP pode validar senha para viagem expressa (US-15).
    """
    usuario = cadastro.buscar(matricula)
    if usuario is None:
        interface.log_visitante(matricula)
        return False

    expresso = False
    if usuario["perfil"] == "vip":
        expresso = _validar_senha_vip(usuario["nome"], senha_automatica)

    chamada = chamadas.criar_chamada(
        usuario=usuario["nome"],
        origem=ANDAR_CATRACA,
        destino=usuario["andar_sala"],
        perfil=usuario["perfil"],
        expresso=expresso,
    )
    interface.log_catraca_entrada(usuario, expresso)
    chamadas.adicionar_na_fila(fila, chamada)
    return True


def saida(matricula, andar_atual, destino_saida, fila):
    """
    Evento: pessoa vai SAIR do prédio. Gera chamada do andar
    atual para o térreo ou para uma das garagens (US-11).
    """
    usuario = cadastro.buscar(matricula)
    if usuario is None:
        interface.log_visitante(matricula)
        return False

    chamada = chamadas.criar_chamada(
        usuario=usuario["nome"],
        origem=andar_atual,
        destino=destino_saida,
        perfil=usuario["perfil"],
    )
    print(f"   🚪 Saída registrada: {ICONES_PERFIL[usuario['perfil']]} "
          f"{usuario['nome']}")
    chamadas.adicionar_na_fila(fila, chamada)
    return True


def simular_grupo(quantidade, fila):
    """
    Modo demonstração: sorteia N pessoas do cadastro passando
    pela catraca em sequência, simulando o horário de chegada.
    VIPs do grupo têm a senha validada automaticamente.
    """
    matriculas = random.sample(cadastro.listar_matriculas(),
                               k=min(quantidade, len(cadastro.USUARIOS)))
    print(f"\n🚧 Simulando {len(matriculas)} pessoa(s) passando pela catraca...")
    for matricula in matriculas:
        entrada(matricula, fila, senha_automatica=True)


def _validar_senha_vip(nome, senha_automatica):
    """
    US-15: 3 tentativas de senha. Acertou -> viagem expressa.
    Errou as 3 -> chamada rebaixada para atendimento comum.
    """
    if senha_automatica:
        print(f"   ⭐ Senha VIP de {nome} validada automaticamente (simulação).")
        return True

    for tentativa in range(1, 4):
        senha = input(f"   ⭐ {nome}, digite a senha VIP "
                      f"(tentativa {tentativa}/3): ").strip()
        if senha == SENHA_VIP:
            print("   ✅ Senha correta — viagem EXPRESSA liberada!")
            return True
        interface.log_erro("Senha incorreta.")

    print(f"   ⚠️  3 tentativas esgotadas — {nome} será atendido(a) "
          f"como chamada comum.")
    return False
