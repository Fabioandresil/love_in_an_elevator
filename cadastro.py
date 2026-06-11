# =============================================================
# cadastro.py — Base de usuários identificados pela catraca
# US-10: Cadastro de usuários
# =============================================================
# A catraca do SENAC já identifica quem entra no prédio. Este
# módulo representa o cadastro consultado nessa identificação:
# matrícula -> nome, perfil (comum/pcd/vip/funcionario) e o
# andar da sala onde a pessoa estuda/trabalha.
#
# LGPD by design: todos os dados abaixo são FICTÍCIOS. Em
# produção, este módulo seria substituído pela consulta ao
# sistema acadêmico real — a interface (funções) seria a mesma.

USUARIOS = {
    "1001": {"nome": "Maria",           "perfil": "comum",       "andar_sala": 3},
    "1002": {"nome": "João",            "perfil": "comum",       "andar_sala": 2},
    "1003": {"nome": "Ana",             "perfil": "pcd",         "andar_sala": 1},
    "1004": {"nome": "Pedro",           "perfil": "comum",       "andar_sala": 4},
    "1005": {"nome": "Lia",             "perfil": "comum",       "andar_sala": 2},
    "1006": {"nome": "Profª Maristela", "perfil": "vip",         "andar_sala": 4},
    "1007": {"nome": "Carlos",          "perfil": "comum",       "andar_sala": 1},
    "1008": {"nome": "Bia",             "perfil": "comum",       "andar_sala": 3},
    "1009": {"nome": "Davi",            "perfil": "comum",       "andar_sala": 2},
    "1010": {"nome": "Rita",            "perfil": "funcionario", "andar_sala": 4},
    "1011": {"nome": "Tom",             "perfil": "comum",       "andar_sala": 1},
    "1012": {"nome": "Vera",            "perfil": "comum",       "andar_sala": 3},
    "1013": {"nome": "Igor",            "perfil": "comum",       "andar_sala": 2},
    "1014": {"nome": "Sol",             "perfil": "comum",       "andar_sala": 1},
    "1015": {"nome": "Edu",             "perfil": "comum",       "andar_sala": 3},
}


def buscar(matricula):
    """Consulta um usuário pela matrícula. Retorna None se não existir."""
    return USUARIOS.get(matricula)


def listar_matriculas():
    """Lista de matrículas cadastradas (usada na simulação de grupo)."""
    return list(USUARIOS.keys())
