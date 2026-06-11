# =============================================================
# config.py — Estrutura do prédio do SENAC e constantes gerais
# US-01: Estrutura do prédio | US-13: Capacidade
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
# (iguais ao exemplo oficial do PDF: A no Térreo, B no 4º)
POSICAO_INICIAL = {"A": 0, "B": 4}

# US-13: limite de pessoas por cabine
CAPACIDADE_MAXIMA = 8

# Andar da catraca (entrada principal do prédio)
ANDAR_CATRACA = 0

# Andares válidos para SAÍDA do prédio (térreo e garagens)
ANDARES_SAIDA = [0, -1, -2]

# US-14/US-15: ordem de prioridade na fila (menor = mais prioritário)
PRIORIDADES = {"pcd": 0, "vip": 1, "funcionario": 2, "comum": 3}

# Ícone de cada perfil, para os logs
ICONES_PERFIL = {"pcd": "♿", "vip": "⭐", "funcionario": "👔", "comum": "🧍"}

# US-15: senha do modo VIP (professores/diretoria)
SENHA_VIP = "senac123"

# US-18: chance de evento aleatório por rodada no Modo Caos (0 a 1)
CHANCE_EVENTO_CAOS = 0.35
