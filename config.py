# =============================================================
# config.py — Estrutura do prédio do SENAC e constantes gerais
# US-01: Estrutura do prédio
# =============================================================
# Regra do projeto: NENHUM outro módulo usa números de andar
# "soltos". Tudo referencia as constantes definidas aqui.

# Lista de andares válidos (subsolos usam números negativos)
ANDARES_VALIDOS = [-2, -1, 0, 1, 2, 3, 4]

# Nome de cada andar, para logs claros no terminal (Regra 6)
NOMES_ANDARES = {
    -2: "Subsolo 2 (Garagem inferior)",
    -1: "Subsolo 1 (Garagem superior)",
     0: "Térreo (Entrada principal)",
     1: "1º Andar (Salas de aula)",
     2: "2º Andar (Laboratórios)",
     3: "3º Andar (Biblioteca)",
     4: "4º Andar (Administração)",
}

# Posições iniciais dos elevadores
# (iguais ao exemplo oficial do PDF da gincana: A no Térreo, B no 4º)
POSICAO_INICIAL = {
    "A": 0,
    "B": 4,
}

# Reservado para as próximas sprints
CAPACIDADE_MAXIMA = 8  # pessoas por cabine (Sprint 3 — US-13)
