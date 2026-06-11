# =============================================================
# main.py — Ponto de entrada do sistema (US-06: Loop principal)
# =============================================================
# Papel deste arquivo: APENAS orquestrar. A lógica de negócio
# mora nos módulos especializados:
#   config.py        -> estrutura do prédio e constantes
#   cadastro.py      -> usuários identificados pela catraca
#   catraca.py       -> eventos de entrada/saída (chamada antecipada)
#   chamadas.py      -> fila, prioridades, despacho por destino
#   elevadores.py    -> estado e movimentação das cabines
#   eventos.py       -> Modo Caos (módulo random)
#   ia_previsao.py   -> IA simples de demanda e pré-posicionamento
#   estatisticas.py  -> coleta de dados e relatório BI
#   validacao.py     -> entradas do usuário
#   interface.py     -> exibição no terminal
#
# Para executar:  python main.py
# Senha VIP da demonstração: senac123 (ver config.py)

import elevadores as mod_elevadores
import catraca
import chamadas
import estatisticas
import interface
import validacao


def main():
    interface.exibir_titulo()

    # Estado inicial: elevadores (A no Térreo, B no 4º) e fila vazia
    elevadores = mod_elevadores.criar_elevadores()
    fila_chamadas = []      # US-08: chamadas pendentes
    caos_ativo = False      # US-18: Modo Caos desligado por padrão
    interface.exibir_status(elevadores)

    # Laço principal: mantém o sistema rodando até o operador sair
    while True:
        interface.exibir_menu(caos_ativo)
        opcao = validacao.ler_opcao_menu()

        if opcao == "1":
            # US-11: passagem pela catraca gera a chamada sozinha
            matricula = validacao.ler_matricula()
            catraca.entrada(matricula, fila_chamadas)

        elif opcao == "2":
            matricula = validacao.ler_matricula()
            andar_atual = validacao.ler_andar(
                "   Em qual andar a pessoa está agora? "
            )
            destino = validacao.ler_andar_saida()
            catraca.saida(matricula, andar_atual, destino, fila_chamadas)

        elif opcao == "3":
            # Visitante sem cadastro: chamada manual continua existindo
            usuario, origem, destino = validacao.ler_dados_chamada()
            chamada = chamadas.criar_chamada(usuario, origem, destino)
            chamadas.adicionar_na_fila(fila_chamadas, chamada)

        elif opcao == "4":
            quantidade = validacao.ler_quantidade(
                "   Quantas pessoas chegam pela catraca (1 a 15)? "
            )
            catraca.simular_grupo(quantidade, fila_chamadas)

        elif opcao == "5":
            chamadas.processar_fila(fila_chamadas, elevadores, caos_ativo)

        elif opcao == "6":
            interface.exibir_fila(fila_chamadas)

        elif opcao == "7":
            interface.exibir_status(elevadores)

        elif opcao == "8":
            estatisticas.exibir_relatorio(elevadores)

        elif opcao == "9":
            caos_ativo = not caos_ativo
            estado = "LIGADO 🎲" if caos_ativo else "desligado"
            print(f"   🎛️  Modo Caos agora está {estado}.")

        elif opcao == "0":
            if fila_chamadas:
                interface.log_erro(
                    f"Atenção: {len(fila_chamadas)} chamada(s) ainda na fila."
                )
            caminho = estatisticas.exportar_csv()
            interface.log_despedida(caminho)
            break  # encerra o laço principal

        else:
            interface.log_erro(f"Opção '{opcao}' inválida. Use 1 a 9 ou 0.")


# Executa main() apenas quando este arquivo é rodado diretamente
if __name__ == "__main__":
    main()
