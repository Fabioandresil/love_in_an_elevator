# =============================================================
# validacao.py — Validação de todas as entradas do usuário
# US-02 | Sprint 2: nome do usuário e quantidade do lote
# Regra 5: Validar Entradas
# =============================================================

from config import ANDARES_VALIDOS
import interface

# Contador global para nomear usuários que não informam o nome
_contador_usuarios = 0


def ler_andar(mensagem):
    """
    Pergunta um andar ao usuário e só retorna quando a resposta
    for válida. Trata dois problemas:
      1) Entrada que não é número (ex.: "abc") -> não quebra o programa
      2) Andar fora do prédio (ex.: 7) -> rejeitado com mensagem clara
    Usa um laço while: o programa insiste até receber um andar válido.
    """
    while True:
        resposta = input(mensagem).strip()

        # 1) Garante que a entrada é um número inteiro (aceita negativos)
        try:
            andar = int(resposta)
        except ValueError:
            interface.log_erro(
                f"'{resposta}' não é um número. Digite um andar entre "
                f"{min(ANDARES_VALIDOS)} e {max(ANDARES_VALIDOS)}."
            )
            continue  # volta ao início do laço e pergunta de novo

        # 2) Garante que o andar existe no prédio
        if andar not in ANDARES_VALIDOS:
            interface.log_erro(
                f"Andar {andar} não existe no SENAC. Andares válidos: "
                f"{min(ANDARES_VALIDOS)} a {max(ANDARES_VALIDOS)}."
            )
            continue

        return andar  # entrada válida: sai do laço


def ler_nome_usuario():
    """
    Lê o nome de quem está chamando o elevador (US-09: o log
    identifica qual elevador atendeu qual usuário).
    Se deixar em branco, gera um nome automático (Usuário 1, 2...).
    """
    global _contador_usuarios
    nome = input("   Nome do usuário (Enter para automático): ").strip()
    if nome == "":
        _contador_usuarios += 1
        nome = f"Usuário {_contador_usuarios}"
    return nome


def ler_dados_chamada():
    """
    Lê uma chamada completa: nome, origem e destino.
    Regra extra: origem igual ao destino não gera viagem.
    Retorna a tupla (usuario, origem, destino).
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


def ler_quantidade(mensagem, minimo=1, maximo=20):
    """
    Lê um número inteiro dentro de um intervalo (usado no modo
    lote da US-09). Mesmo padrão de laço while da ler_andar.
    """
    while True:
        resposta = input(mensagem).strip()
        try:
            quantidade = int(resposta)
        except ValueError:
            interface.log_erro(f"'{resposta}' não é um número inteiro.")
            continue

        if quantidade < minimo or quantidade > maximo:
            interface.log_erro(
                f"Informe um valor entre {minimo} e {maximo}."
            )
            continue

        return quantidade


def ler_opcao_menu():
    """Lê a opção do menu principal (US-06)."""
    return input("Escolha uma opção: ").strip()
