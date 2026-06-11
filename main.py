# =============================================================
# main.py — Ponto de entrada do sistema (US-06: Loop principal)
# Sprint 2: fila de chamadas (US-08) e modo lote (US-09)
# =============================================================
# Papel deste arquivo: APENAS orquestrar. Nenhuma lógica de
# negócio mora aqui — ela está nos módulos especializados:
#   config.py      -> estrutura do prédio
#   elevadores.py  -> estado e movimentação
#   chamadas.py    -> escolha, fila e ciclo das viagens
#   validacao.py   -> entradas do usuário
#   interface.py   -> exibição no terminal
#
# Para executar:  python main.py

import elevadores as mod_elevadores
import chamadas
import validacao
import interface


def registrar_chamada_na_fila(fila):
    """Lê os dados de uma chamada e a coloca na fila (US-08)."""
    usuario, origem, destino = validacao.ler_dados_chamada()
    chamada = chamadas.criar_chamada(usuario, origem, destino)
    chamadas.adicionar_na_fila(fila, chamada)


def modo_lote(fila):
    """
    Registra várias chamadas de uma vez (US-09), simulando um
    cenário real de intervalo de aulas com vários usuários.
    """
    quantidade = validacao.ler_quantidade(
        "   Quantas chamadas deseja registrar (1 a 20)? "
    )
    for numero in range(1, quantidade + 1):
        print(f"\n   --- Chamada {numero} de {quantidade} ---")
        registrar_chamada_na_fila(fila)


def main():
    interface.exibir_titulo()

    # Estado inicial: elevadores (A no Térreo, B no 4º) e fila vazia
    elevadores = mod_elevadores.criar_elevadores()
    fila_chamadas = []  # US-08: lista de chamadas pendentes (FIFO)
    interface.exibir_status(elevadores)

    # Laço principal: mantém o sistema rodando até o operador sair
    while True:
        interface.exibir_menu()
        opcao = validacao.ler_opcao_menu()

        if opcao == "1":
            # Atendimento imediato (comportamento da Sprint 1)
            usuario, origem, destino = validacao.ler_dados_chamada()
            chamada = chamadas.criar_chamada(usuario, origem, destino)
            chamadas.atender_chamada_imediata(chamada, elevadores)

        elif opcao == "2":
            registrar_chamada_na_fila(fila_chamadas)

        elif opcao == "3":
            modo_lote(fila_chamadas)

        elif opcao == "4":
            chamadas.processar_fila(fila_chamadas, elevadores)

        elif opcao == "5":
            interface.exibir_fila(fila_chamadas)

        elif opcao == "6":
            interface.exibir_status(elevadores)

        elif opcao == "0":
            if fila_chamadas:
                interface.log_erro(
                    f"Atenção: {len(fila_chamadas)} chamada(s) ainda na fila."
                )
            interface.log_despedida()
            break  # encerra o laço principal

        else:
            interface.log_erro(
                f"Opção '{opcao}' inválida. Use 1 a 6 ou 0."
            )


# Executa main() apenas quando este arquivo é rodado diretamente
if __name__ == "__main__":
    main()
