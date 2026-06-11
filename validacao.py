# =============================================================
# validacao.py — Validação de todas as entradas do usuário
# US-02 | Regra 5: Validar Entradas
# =============================================================

from config import ANDARES_VALIDOS, ANDARES_SAIDA
import interface

# Contador para nomear visitantes que não informam o nome
_contador_usuarios = 0


def ler_andar(mensagem, permitidos=None):
    """
    Pergunta um andar e só retorna quando a resposta for válida.
      1) Entrada não numérica (ex.: "abc") -> não quebra o programa
      2) Andar fora do prédio (ex.: 7) -> rejeitado com mensagem
    'permitidos' restringe as opções (ex.: andares de saída).
    """
    if permitidos is None:
        permitidos = ANDARES_VALIDOS

    while True:
        resposta = input(mensagem).strip()

        try:
            andar = int(resposta)
        except ValueError:
            interface.log_erro(
                f"'{resposta}' não é um número. Opções válidas: "
                f"{permitidos}."
            )
            continue  # volta ao início do laço e pergunta de novo

        if andar not in permitidos:
            interface.log_erro(
                f"Andar {andar} não é válido aqui. Opções: {permitidos}."
            )
            continue

        return andar


def ler_andar_saida():
    """Destino de quem sai do prédio: térreo ou garagens (US-11)."""
    return ler_andar(
        f"   Sair para qual andar? {ANDARES_SAIDA} "
        f"(0=Térreo, -1/-2=Garagens): ",
        permitidos=ANDARES_SAIDA,
    )


def ler_matricula(mensagem="   Matrícula: "):
    """Lê a matrícula apresentada à catraca (US-10/US-11)."""
    return input(mensagem).strip()


def ler_nome_usuario():
    """Nome do visitante na chamada manual; Enter gera automático."""
    global _contador_usuarios
    nome = input("   Nome do visitante (Enter para automático): ").strip()
    if nome == "":
        _contador_usuarios += 1
        nome = f"Visitante {_contador_usuarios}"
    return nome


def ler_dados_chamada():
    """
    Chamada manual completa: nome, origem e destino.
    Regra extra: origem igual ao destino não gera viagem.
    """
    usuario = ler_nome_usuario()
    while True:
        origem = ler_andar(f"   Em qual andar {usuario} está? ")
        destino = ler_andar(f"   Para qual andar {usuario} vai? ")

        if origem == destino:
            interface.log_erro(
                "Origem e destino são iguais — você já está nesse andar!"
            )
            continue

        return usuario, origem, destino


def ler_quantidade(mensagem, minimo=1, maximo=15):
    """Número inteiro dentro de um intervalo (simulação de grupo)."""
    while True:
        resposta = input(mensagem).strip()
        try:
            quantidade = int(resposta)
        except ValueError:
            interface.log_erro(f"'{resposta}' não é um número inteiro.")
            continue

        if quantidade < minimo or quantidade > maximo:
            interface.log_erro(f"Informe um valor entre {minimo} e {maximo}.")
            continue

        return quantidade


def ler_opcao_menu():
    """Lê a opção do menu principal (US-06)."""
    return input("Escolha uma opção: ").strip()
