# =============================================================
# validacao.py — Validação de todas as entradas do usuário
# US-02: Validação de entradas | Regra 5: Validar Entradas
# =============================================================

from config import ANDARES_VALIDOS
import interface


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


def ler_chamada():
    """
    Lê origem e destino de uma chamada completa.
    Regra extra: origem igual ao destino não gera viagem.
    Retorna a tupla (origem, destino).
    """
    while True:
        origem = ler_andar("   Em qual andar você está? ")
        destino = ler_andar("   Para qual andar deseja ir? ")

        if origem == destino:
            interface.log_erro(
                "Origem e destino são iguais — você já está nesse andar!"
            )
            continue

        return origem, destino


def ler_opcao_menu():
    """Lê a opção do menu principal (US-06)."""
    return input("Escolha uma opção: ").strip()
