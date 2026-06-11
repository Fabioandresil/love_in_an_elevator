# 🛗 Sistema Inteligente de Elevadores — SENAC (Sprints 1 e 2)

Projeto da Gincana Python — Lógica de Programação
**Equipe:** Eric · Diogo (Scrum Master) · Fabio (Product Owner) · Yuri

## Como executar

Requisito: Python 3 (qualquer versão recente). Sem bibliotecas externas.

```
python main.py
```

No GitHub Codespaces: abra o terminal na pasta do projeto e rode o mesmo comando.

## Módulos

| Arquivo | Responsabilidade | User Stories |
|---|---|---|
| `config.py` | Estrutura do prédio (andares −2 a 4) e constantes | US-01 |
| `validacao.py` | Leitura segura de entradas (texto, andares inválidos, origem=destino, quantidades) | US-02 |
| `elevadores.py` | Estado das cabines (posição + status) e movimentação andar a andar | US-03 |
| `chamadas.py` | Escolha com `abs()`, fila FIFO e processamento em rodadas paralelas | US-04, US-05, US-08, US-09 |
| `interface.py` | Tudo que aparece no terminal (logs, menu, fila, status) | US-05, US-06 |
| `main.py` | Loop principal — apenas orquestra (US-07: modularização) | US-06 |

## Funcionalidades por sprint

**Sprint 1 (✅):** chamada imediata com escolha do elevador mais próximo via
`abs()`, movimentação andar a andar com log, validação total de entradas,
menu em laço `while`.

**Sprint 2 (✅):**
- **Fila de chamadas (US-08):** lista FIFO — quem chega primeiro é atendido
  primeiro. Comando do menu exibe a fila com a posição de cada pessoa.
- **Modo lote (US-09):** registra até 20 chamadas de uma vez, simulando o
  intervalo de aulas.
- **Rodadas em paralelo lógico (US-09):** em cada rodada, cada elevador livre
  assume UMA chamada; a chamada mais antiga fica com o elevador mais próximo.
  O log anuncia a alocação ("Elevador A -> Maria") e quantos aguardam.

## Casos de teste oficiais (✅ verificados)

**1. Exemplo do PDF:** A no Térreo, B no 4º; chamada do Subsolo 1 → Biblioteca.
Distâncias A=1, B=5 → A escolhido; status final A no 3º.

**2. Lote do intervalo (5 usuários):**
| Rodada | Elevador A | Elevador B |
|---|---|---|
| 1 | Maria (Térreo→3º, dist 0) | João (Térreo→2º, dist 4) |
| 2 | Pedro (4º→Térreo, dist 1) | Ana (Subsolo 1→4º, dist 3) |
| 3 | Lia (2º→Subsolo 2, **empate dist 2 → critério alfabético**) | — |

## Decisões de projeto (para apresentar à banca)

- **FIFO + proximidade combinados:** a ordem de chegada define quem é atendido
  na rodada (justiça na fila); a proximidade define QUAL elevador atende
  (eficiência). Ataca as dores "Filas Eternas" e "Escolhas Estranhas".
- **Desempate alfabético** (vence o "A"): comportamento previsível e testável —
  demonstrado ao vivo no caso da Lia.
- **1 chamada por elevador por rodada:** simplificação consciente; na Sprint 3
  o agrupamento por destino permitirá vários passageiros por viagem.
- **`main.py` sem lógica de negócio:** módulos com responsabilidade única
  (pontos extras de Organização).

## Próximas sprints (backlog)

- Sprint 3: catraca inteligente, despacho por destino, capacidade (8/cabine), PCD/VIP/emergência, Modo Caos
- Sprint 4: IA de previsão de demanda + relatório/dashboard BI
