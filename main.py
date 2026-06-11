# =============================================================
# main.py — Ponto de entrada do sistema (US-06: Loop principal)
# =============================================================
# Papel deste arquivo: APENAS orquestrar. Nenhuma lógica de
# negócio mora aqui — ela está nos módulos especializados:
#   config.py      -> estrutura do prédio
#   elevadores.py  -> estado e movimentação
#   chamadas.py    -> escolha do elevador e ciclo da viagem
#   validacao.py   -> entradas do usuário
#   interface.py   -> exibição no terminal
#
# Para executar:  python main.py

import elevadores as mod_elevadores
import chamadas
import validacao
import interface


def main():
    interface.exibir_titulo()

    # Cria o estado inicial (A no Térreo, B no 4º — ver config.py)
    elevadores = mod_elevadores.criar_elevadores()
    interface.exibir_status(elevadores)

    # Laço principal: mantém o sistema rodando até o operador sair
    while True:
        interface.exibir_menu()
        opcao = validacao.ler_opcao_menu()

        if opcao == "1":
            origem, destino = validacao.ler_chamada()
            chamadas.atender_chamada(origem, destino, elevadores)

        elif opcao == "2":
            interface.exibir_status(elevadores)

        elif opcao == "0":
            interface.log_despedida()
            break  # encerra o laço principal

        else:
            interface.log_erro(
                f"Opção '{opcao}' inválida. Use 1, 2 ou 0."
            )


# Executa main() apenas quando este arquivo é rodado diretamente
if __name__ == "__main__":
    main()
