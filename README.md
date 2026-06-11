# 🛗 Sistema Inteligente de Elevadores — SENAC (Versão Final)

Projeto da Gincana Python — Lógica de Programação (Profª Maristela)
**Equipe Scrum:** Eric (Dev) · Diogo (Scrum Master) · Fabio (Product Owner) · Yuri (Dev)

## A ideia em uma frase

Ao passar pela **catraca de identificação que já existe no SENAC**, o sistema
reconhece a pessoa (perfil e andar da sala) e **antecipa a chamada do
elevador**, agrupando quem chega junto por destino — o conceito de
**Destination Dispatch** usado em prédios corporativos reais, adaptado à
faculdade e implementado 100% em Python puro.

## Como executar

```
python main.py
```

Sem bibliotecas externas. Senha VIP da demonstração: `senac123` (config.py).

## Roteiro de demonstração sugerido (5 min)

1. **[7]** Status inicial (A no Térreo, B no 4º — igual ao exemplo do PDF)
2. **[1]** Entradas pela catraca: `1001`, `1002`, `1004`, `1005`, **`1003`
   (Ana ♿ PCD)**, `1007`, `1008`, `1009`, `1011` — note que a chamada nasce
   sozinha, com o andar da sala de cada um
3. **[1]** `1006` (Profª Maristela ⭐ VIP) + senha `senac123` → viagem expressa
4. **[1]** `9999` → visitante não cadastrado é orientado à chamada manual
5. **[6]** Ver a fila (11 chamadas, EXPRESSO sinalizado)
6. **[5]** Processar: na Rodada 1, **Ana embarca PRIMEIRO mesmo tendo chegado
   em 5º** (prioridade PCD), cabine lota em **8/8**, paradas no 1º, 2º, 3º e
   4º com desembarques anunciados; a VIP viaja expressa no outro elevador;
   excedente vai para a Rodada 2
7. **[9] + [4] + [5]** Ligar o Modo Caos e simular um grupo: panes e
   manutenções aleatórias com redirecionamento automático
8. **[8]** Relatório BI da sessão · **[0]** sair (exporta CSV)

## Módulos (modularização = pontos extras de Organização)

| Arquivo | Responsabilidade | User Stories |
|---|---|---|
| `config.py` | Estrutura do prédio, capacidade, prioridades, constantes | US-01, US-13 |
| `cadastro.py` | Usuários fictícios identificados pela catraca (LGPD by design) | US-10 |
| `catraca.py` | Eventos de entrada/saída → chamada antecipada; senha VIP | US-11, US-15 |
| `chamadas.py` | Fila com prioridades, despacho por destino, rodadas paralelas | US-04, US-08, US-09, US-12, US-13, US-14 |
| `elevadores.py` | Estado das cabines e movimentação andar a andar (`abs()`) | US-03, US-05 |
| `eventos.py` | Modo Caos com `random`: pane, conserto e redirecionamento | US-18 |
| `ia_previsao.py` | IA simples: frequência de destinos + pré-posicionamento | US-20 |
| `estatisticas.py` | Coleta de dados, relatório BI no terminal e exportação CSV | US-19, US-21 |
| `validacao.py` | Toda entrada do usuário validada em laços `while` | US-02 |
| `interface.py` | Painel de embarque, logs e menu (Regra 6) | US-05, US-06 |
| `main.py` | Loop principal — apenas orquestra | US-06, US-07 |

## Conceitos Python aplicados (premissa 5 do escopo)

Variáveis e condicionais (`if/elif/else` em toda a lógica de decisão) ·
Laços (`while` no menu, validações e rodadas; `for` na movimentação e
agrupamento) · Funções (`def escolher_elevador()`, `def montar_viagem()`...) ·
Listas e `abs()` (fila de chamadas, andares válidos, distâncias) ·
Dicionários (elevadores, cadastro, memória da IA) · `random` (Modo Caos) ·
**Modularização em 11 arquivos com responsabilidade única**.

## Decisões de projeto (para a banca)

- **Catraca como sensor:** o prédio já identifica quem entra; o módulo
  `catraca.py` simula esses eventos com a MESMA interface que uma integração
  real teria. Nenhum dado pessoal real é usado.
- **Destination Dispatch:** agrupar por destino antes do embarque é a
  tecnologia usada por Schindler (PORT) e TK Elevator em prédios corporativos
  — aplicada aqui às 4 dores do cliente (demora, filas, escolhas estranhas,
  caos no pico).
- **Prioridade justa:** ordenação por perfil (PCD > VIP > funcionário >
  comum) com desempate FIFO — o `sort` estável do Python preserva a ordem de
  chegada dentro de cada prioridade.
- **Capacidade 8/cabine:** excedente vai automaticamente para a próxima
  viagem, com aviso — ninguém é esquecido.
- **Desempate de distância alfabético** ("A" vence): previsível e testável.
- **Modo Caos com trava de segurança:** se todos os elevadores quebrarem com
  fila pendente, a manutenção de emergência religa um — o sistema nunca trava.

## Casos de teste verificados ✅

1. **Exemplo oficial do PDF:** A no Térreo, B no 4º; chamada Subsolo 1 → 3º.
   Distâncias A=1, B=5 → A escolhido.
2. **Intervalo com 11 chamadas:** PCD chegou em 5º e embarcou em 1º; cabine
   lotou em 8/8; VIP expressa em paralelo; excedente na Rodada 2; saída para
   a garagem atendida.
3. **Modo Caos (3 execuções):** panes e consertos aleatórios, fila sempre
   100% atendida, sem travamentos.
4. **Entradas inválidas:** texto, andar 7, origem=destino, matrícula
   inexistente e senha VIP errada (3 tentativas → rebaixa para comum).

## Histórico Scrum

- **Sprint 1:** núcleo de movimentação (US-01 a US-06)
- **Sprint 2:** fila FIFO e rodadas paralelas (US-08, US-09)
- **Sprint 3+4 (entrega final):** catraca, despacho por destino, capacidade,
  PCD/VIP, Modo Caos, IA simples e BI (US-10 a US-15, US-18 a US-21)
- **Roadmap (não entregue por decisão de escopo do PO):** horário de pico
  (US-17), modo emergência (US-16), dashboard BI web (US-22) — o CSV
  exportado já é a base de dados para essa evolução.
