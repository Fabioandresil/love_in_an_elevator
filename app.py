# =============================================================
# app.py — Interface WEB do sistema (Flask) | Nível Hacker
# =============================================================
# Este arquivo é uma NOVA CAMADA DE INTERFACE: ele importa os
# MESMOS módulos de negócio usados pelo main.py (terminal) sem
# alterar uma linha deles — demonstração prática do valor da
# modularização. Os logs do terminal são capturados e exibidos
# num painel "central de operações" na página.
#
# Como executar:
#   pip install flask
#   python app.py
#   Abrir http://localhost:5000 (no Codespaces, a porta 5000 é
#   encaminhada automaticamente — clique no aviso que aparece)

import io
import contextlib

from flask import Flask, request, redirect, url_for, render_template_string

from config import (ANDARES_VALIDOS, NOMES_ANDARES, ANDAR_CATRACA,
                    ANDARES_SAIDA, SENHA_VIP, ICONES_PERFIL,
                    CAPACIDADE_MAXIMA)
import cadastro
import catraca
import chamadas
import elevadores as mod_elevadores
import estatisticas
import interface

app = Flask(__name__)

# ----- Estado da demonstração (um único prédio) ---------------
elevadores = mod_elevadores.criar_elevadores()
fila_chamadas = []
caos_ativo = False
ultimo_log = ("Sistema iniciado.\n"
              "🛗 Elevador A no Térreo | 🛗 Elevador B no 4º Andar.\n"
              "Use os controles ao lado para operar a catraca.")


def capturar_saida(funcao, *args, **kwargs):
    """
    Executa uma função dos módulos existentes redirecionando os
    print() para uma string — assim os logs do terminal viram o
    painel de operações da página, sem refatorar nada.
    """
    buffer = io.StringIO()
    with contextlib.redirect_stdout(buffer):
        funcao(*args, **kwargs)
    return buffer.getvalue()


def entrada_web(matricula, senha):
    """
    Adaptador web do evento de catraca: mesma lógica do
    catraca.entrada, mas a senha VIP vem do formulário em vez
    do input() do terminal.
    """
    usuario = cadastro.buscar(matricula)
    if usuario is None:
        interface.log_visitante(matricula)
        return

    expresso = False
    if usuario["perfil"] == "vip":
        if senha == SENHA_VIP:
            print(f"   ✅ Senha VIP de {usuario['nome']} correta — "
                  f"viagem EXPRESSA liberada!")
            expresso = True
        else:
            print(f"   ⚠️  Senha VIP ausente ou incorreta — "
                  f"{usuario['nome']} será atendido(a) como chamada comum.")

    chamada = chamadas.criar_chamada(
        usuario=usuario["nome"],
        origem=ANDAR_CATRACA,
        destino=usuario["andar_sala"],
        perfil=usuario["perfil"],
        expresso=expresso,
    )
    interface.log_catraca_entrada(usuario, expresso)
    chamadas.adicionar_na_fila(fila_chamadas, chamada)


# =============================================================
# Página principal
# =============================================================

PAGINA = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>🛗 Elevadores Inteligentes — SENAC</title>
<style>
  :root { --laranja:#F58220; --escuro:#2b2b2b; }
  * { box-sizing:border-box; }
  body { font-family:Segoe UI, Arial, sans-serif; margin:0;
         background:#f4f4f4; color:#333; }
  header { background:var(--laranja); color:#fff; padding:14px 24px; }
  header h1 { margin:0; font-size:1.3rem; }
  header p  { margin:2px 0 0; font-size:.85rem; opacity:.9; }
  main { display:grid; grid-template-columns: 1fr 1fr; gap:16px;
         padding:16px 24px; max-width:1200px; margin:auto; }
  .card { background:#fff; border-radius:10px; padding:14px 16px;
          box-shadow:0 1px 4px rgba(0,0,0,.12); }
  .card h2 { margin:0 0 10px; font-size:1rem; color:var(--laranja);
             border-bottom:2px solid var(--laranja); padding-bottom:6px; }
  table { width:100%; border-collapse:collapse; font-size:.85rem; }
  td, th { padding:5px 6px; border-bottom:1px solid #eee; text-align:left; }
  .andar-elev { font-weight:bold; }
  .ocupado-A { background:#fff3e6; }
  form { margin:0 0 10px; }
  label { font-size:.8rem; display:block; margin:6px 0 2px; }
  input, select { width:100%; padding:6px; border:1px solid #ccc;
                  border-radius:6px; font-size:.9rem; }
  button { margin-top:8px; background:var(--laranja); color:#fff;
           border:none; padding:8px 14px; border-radius:6px;
           cursor:pointer; font-weight:bold; width:100%; }
  button:hover { filter:brightness(.92); }
  button.cinza { background:#666; }
  .linha { display:flex; gap:8px; }
  .linha > div { flex:1; }
  pre.log { grid-column:1 / -1; background:var(--escuro); color:#9fe89f;
            padding:14px; border-radius:10px; font-size:.8rem;
            white-space:pre-wrap; max-height:420px; overflow:auto; }
  .fila li { font-size:.85rem; margin-bottom:3px; }
  .badge { background:var(--laranja); color:#fff; border-radius:10px;
           padding:1px 8px; font-size:.75rem; }
  footer { text-align:center; font-size:.75rem; color:#888;
           padding:10px 0 20px; }
</style>
</head>
<body>
<header>
  <h1>🛗 Sistema Inteligente de Elevadores — SENAC</h1>
  <p>Catraca integrada · Despacho por Destino · Capacidade {{capacidade}}/cabine ·
     Modo Caos: <strong>{{ 'LIGADO 🎲' if caos else 'desligado' }}</strong></p>
</header>
<main>

  <!-- COLUNA ESQUERDA: prédio, fila e cadastro -->
  <section class="card">
    <h2>🏢 O Prédio agora</h2>
    <table>
      {% for andar in andares %}
      <tr {% if posicoes[andar] %}class="ocupado-A"{% endif %}>
        <td style="width:55%">{{ nomes[andar] }}</td>
        <td class="andar-elev">
          {% for elev in posicoes[andar] %}
            🛗 {{ elev.nome }} <small>({{ elev.status }})</small>
          {% endfor %}
        </td>
      </tr>
      {% endfor %}
    </table>

    <h2 style="margin-top:14px">📋 Fila de chamadas
        <span class="badge">{{ fila|length }}</span></h2>
    {% if fila %}
    <ol class="fila">
      {% for c in fila %}
      <li>{{ icones[c.perfil] }} <strong>{{ c.usuario }}</strong>:
          {{ nomes[c.origem] }} → {{ nomes[c.destino] }}
          {% if c.expresso %}<span class="badge">EXPRESSO</span>{% endif %}</li>
      {% endfor %}
    </ol>
    {% else %}<p style="font-size:.85rem">Fila vazia.</p>{% endif %}

    <h2 style="margin-top:14px">🎫 Cadastro (cole uma matrícula na catraca)</h2>
    <table>
      <tr><th>Matr.</th><th>Nome</th><th>Perfil</th><th>Sala</th></tr>
      {% for m, u in usuarios.items() %}
      <tr><td>{{ m }}</td><td>{{ icones[u.perfil] }} {{ u.nome }}</td>
          <td>{{ u.perfil }}</td><td>{{ nomes[u.andar_sala] }}</td></tr>
      {% endfor %}
    </table>
  </section>

  <!-- COLUNA DIREITA: controles -->
  <section class="card">
    <h2>🎫 Catraca — Entrada</h2>
    <form method="post" action="{{ url_for('rota_entrada') }}">
      <div class="linha">
        <div><label>Matrícula</label>
             <input name="matricula" placeholder="ex.: 1003" required></div>
        <div><label>Senha VIP (só p/ perfil ⭐)</label>
             <input name="senha" type="password" placeholder="opcional"></div>
      </div>
      <button>Passar pela catraca</button>
    </form>

    <h2>🚪 Catraca — Saída do prédio</h2>
    <form method="post" action="{{ url_for('rota_saida') }}">
      <div class="linha">
        <div><label>Matrícula</label><input name="matricula" required></div>
        <div><label>Está no andar</label>
          <select name="andar_atual">
            {% for a in andares %}<option value="{{a}}">{{ nomes[a] }}</option>{% endfor %}
          </select></div>
        <div><label>Sair pelo</label>
          <select name="destino">
            {% for a in saidas %}<option value="{{a}}">{{ nomes[a] }}</option>{% endfor %}
          </select></div>
      </div>
      <button>Registrar saída</button>
    </form>

    <h2>🧍 Chamada manual (visitante)</h2>
    <form method="post" action="{{ url_for('rota_manual') }}">
      <div class="linha">
        <div><label>Nome</label><input name="nome" placeholder="Visitante"></div>
        <div><label>Origem</label>
          <select name="origem">
            {% for a in andares %}<option value="{{a}}">{{ nomes[a] }}</option>{% endfor %}
          </select></div>
        <div><label>Destino</label>
          <select name="destino">
            {% for a in andares %}<option value="{{a}}">{{ nomes[a] }}</option>{% endfor %}
          </select></div>
      </div>
      <button>Adicionar à fila</button>
    </form>

    <h2>⚙️ Operação</h2>
    <form method="post" action="{{ url_for('rota_simular') }}">
      <label>Simular grupo chegando pela catraca</label>
      <div class="linha">
        <div><input name="quantidade" type="number" min="1" max="15" value="8"></div>
        <div><button>Simular chegada</button></div>
      </div>
    </form>
    <form method="post" action="{{ url_for('rota_processar') }}">
      <button>▶️ PROCESSAR EMBARQUES (despacho por destino)</button>
    </form>
    <div class="linha">
      <form method="post" action="{{ url_for('rota_caos') }}" style="flex:1">
        <button class="cinza">🎲 Modo Caos: {{ 'desligar' if caos else 'ligar' }}</button>
      </form>
      <form method="post" action="{{ url_for('rota_relatorio') }}" style="flex:1">
        <button class="cinza">📈 Relatório BI</button>
      </form>
      <form method="post" action="{{ url_for('rota_reiniciar') }}" style="flex:1">
        <button class="cinza">🔄 Reiniciar demo</button>
      </form>
    </div>
  </section>

  <!-- PAINEL DE OPERAÇÕES: os logs do terminal, capturados -->
  <pre class="log">{{ log }}</pre>
</main>
<footer>Gincana Python SENAC — Equipe Eric · Diogo · Fabio · Yuri ·
        Mesma lógica do terminal, nova interface (modularização em ação)</footer>
</body>
</html>
"""


@app.route("/")
def pagina_inicial():
    # Posição de cada elevador por andar, para desenhar o prédio
    posicoes = {andar: [] for andar in ANDARES_VALIDOS}
    for nome, elev in elevadores.items():
        posicoes[elev["andar_atual"]].append(
            {"nome": nome, "status": elev["status"]}
        )
    return render_template_string(
        PAGINA,
        andares=sorted(ANDARES_VALIDOS, reverse=True),  # 4º no topo
        nomes=NOMES_ANDARES,
        posicoes=posicoes,
        fila=fila_chamadas,
        usuarios=cadastro.USUARIOS,
        icones=ICONES_PERFIL,
        saidas=ANDARES_SAIDA,
        capacidade=CAPACIDADE_MAXIMA,
        caos=caos_ativo,
        log=ultimo_log,
    )


@app.route("/catraca/entrada", methods=["POST"])
def rota_entrada():
    global ultimo_log
    matricula = request.form.get("matricula", "").strip()
    senha = request.form.get("senha", "").strip()
    ultimo_log = capturar_saida(entrada_web, matricula, senha)
    return redirect(url_for("pagina_inicial"))


@app.route("/catraca/saida", methods=["POST"])
def rota_saida():
    global ultimo_log
    matricula = request.form.get("matricula", "").strip()
    andar_atual = int(request.form.get("andar_atual"))
    destino = int(request.form.get("destino"))
    if andar_atual == destino:
        ultimo_log = "❌ A pessoa já está no andar de saída escolhido."
    else:
        ultimo_log = capturar_saida(
            catraca.saida, matricula, andar_atual, destino, fila_chamadas
        )
    return redirect(url_for("pagina_inicial"))


@app.route("/chamada/manual", methods=["POST"])
def rota_manual():
    global ultimo_log
    nome = request.form.get("nome", "").strip() or "Visitante"
    origem = int(request.form.get("origem"))
    destino = int(request.form.get("destino"))
    # Regra 5 (Validar Entradas) — selects já limitam aos andares
    # válidos; aqui validamos a regra de negócio origem != destino
    if origem == destino:
        ultimo_log = "❌ Origem e destino são iguais — escolha andares diferentes."
    else:
        chamada = chamadas.criar_chamada(nome, origem, destino)
        ultimo_log = capturar_saida(
            chamadas.adicionar_na_fila, fila_chamadas, chamada
        )
    return redirect(url_for("pagina_inicial"))


@app.route("/simular", methods=["POST"])
def rota_simular():
    global ultimo_log
    quantidade = max(1, min(15, int(request.form.get("quantidade", 8))))
    ultimo_log = capturar_saida(
        catraca.simular_grupo, quantidade, fila_chamadas
    )
    return redirect(url_for("pagina_inicial"))


@app.route("/processar", methods=["POST"])
def rota_processar():
    global ultimo_log
    ultimo_log = capturar_saida(
        chamadas.processar_fila, fila_chamadas, elevadores, caos_ativo
    )
    return redirect(url_for("pagina_inicial"))


@app.route("/caos", methods=["POST"])
def rota_caos():
    global caos_ativo, ultimo_log
    caos_ativo = not caos_ativo
    ultimo_log = (f"🎛️ Modo Caos agora está "
                  f"{'LIGADO 🎲 — imprevistos podem ocorrer!' if caos_ativo else 'desligado.'}")
    return redirect(url_for("pagina_inicial"))


@app.route("/relatorio", methods=["POST"])
def rota_relatorio():
    global ultimo_log
    ultimo_log = capturar_saida(estatisticas.exibir_relatorio, elevadores)
    return redirect(url_for("pagina_inicial"))


@app.route("/reiniciar", methods=["POST"])
def rota_reiniciar():
    """Volta ao estado inicial — útil para ensaiar a demo várias vezes."""
    global elevadores, fila_chamadas, caos_ativo, ultimo_log
    elevadores = mod_elevadores.criar_elevadores()
    fila_chamadas = []
    caos_ativo = False
    ultimo_log = "🔄 Demo reiniciada. Elevador A no Térreo, B no 4º andar."
    return redirect(url_for("pagina_inicial"))


if __name__ == "__main__":
    # host 0.0.0.0 permite o encaminhamento de porta do Codespaces
    app.run(host="0.0.0.0", port=5000, debug=False)
