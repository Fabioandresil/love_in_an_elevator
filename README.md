# 🛗 Sistema Inteligente de Elevadores — SENAC (Sprint 1)

Projeto da Gincana Python — Lógica de Programação
**Equipe:** Eric · Diogo (Scrum Master) · Fabio (Product Owner) · Yuri

## Como executar

Requisito: Python 3 (qualquer versão recente). Sem bibliotecas externas.

```
python main.py
```

No GitHub Codespaces: abra o terminal na pasta do projeto e rode o mesmo comando.

## Módulos (US-07 antecipada — modularização vale pontos extras!)

| Arquivo | Responsabilidade | User Stories |
|---|---|---|
| `config.py` | Estrutura do prédio (andares −2 a 4) e constantes | US-01 |
| `validacao.py` | Leitura segura de entradas (rejeita texto, andares inválidos e origem=destino) | US-02 |
| `elevadores.py` | Estado das cabines e movimentação andar a andar | US-03 |
| `chamadas.py` | Escolha do mais próximo com `abs()` e ciclo completo da viagem | US-04, US-05 |
| `interface.py` | Tudo que aparece no terminal (logs, menu, status) | US-05, US-06 |
| `main.py` | Loop principal — apenas orquestra os módulos | US-06 |

## Caso de teste oficial (exemplo do PDF da gincana)

Estado inicial: **A no Térreo (0)** · **B no 4º andar (4)**
Chamada: usuário no **Subsolo 1 (−1)** quer ir à **Biblioteca (3)**

Resultado esperado (✅ verificado):
1. Distâncias: A = abs(0 − (−1)) = **1** · B = abs(4 − (−1)) = **5**
2. Elevador **A** é escolhido
3. A desce ao Subsolo 1 (embarque), sobe ao 3º (desembarque)
4. Status final: A no 3º andar, B segue no 4º

## Decisões de projeto (para apresentar à banca)

- **Desempate na escolha:** a distância igual, vence o elevador "A" (ordem alfabética) — comportamento previsível e testável.
- **Movimentação andar a andar no log:** atende a Regra 6 ("mostra cada etapa de forma clara") e prepara o terreno para paradas intermediárias do agrupamento por destino (Sprint 3).
- **`main.py` sem lógica de negócio:** facilita o trabalho em paralelo da equipe e a evolução para as próximas sprints sem retrabalho.

## Próximas sprints (backlog)

- Sprint 2: fila de chamadas e múltiplos usuários
- Sprint 3: catraca inteligente, despacho por destino, capacidade, PCD/VIP
- Sprint 4: IA de previsão de demanda + dashboard BI
