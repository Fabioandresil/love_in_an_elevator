# =============================================================
# app.py — Interface WEB do sistema (Flask) | Nível Hacker
# v3: cabines animadas EM PARALELO + seleção por checkbox +
#     Evento Crítico (30 entram / 25 saem) + regras do Modo Caos
# =============================================================
# Camada de interface: importa os módulos de negócio do main.py
# sem alterá-los. Novidades desta versão:
#  - Checkbox no cadastro: várias pessoas passam pela catraca
#    de uma só vez.
#  - 🚨 EVENTO CRÍTICO: 30 pessoas entram ao mesmo tempo e, em
#    seguida, 25 tentam sair — estresse máximo do sistema.
#  - Animação simultânea: cada elevador tem sua própria trilha,
#    A e B se movem AO MESMO TEMPO, com velocidade adaptativa.
#  - MODO CAOS = protocolO de emergência: viagens expressas e
#    prioridade VIP são SUSPENSAS (PCD continua prioritário).

import io
import random
import contextlib

from flask import Flask, request, redirect, url_for, render_template_string

from config import (ANDARES_VALIDOS, NOMES_ANDARES, ANDAR_CATRACA,
                    ANDARES_SAIDA, SENHA_VIP, ICONES_PERFIL,
                    CAPACIDADE_MAXIMA, PRIORIDADES)
import cadastro
import catraca
import chamadas
import elevadores as mod_elevadores
import estatisticas
import interface

app = Flask(__name__)

# ----- Estado da demonstração ---------------------------------
elevadores = mod_elevadores.criar_elevadores()
fila_chamadas = []
caos_ativo = False
ultimo_log = ("Sistema iniciado.\n"
              "🛗 Elevador A no Térreo | 🛗 Elevador B no 4º Andar.\n"
              "Use os controles ao lado para operar a catraca.")

# Guarda a prioridade VIP original para restaurar ao sair do Caos
VIP_RANK_ORIGINAL = PRIORIDADES["vip"]

# ----- Gravador de movimentos para a animação -----------------
movimentos_registrados = []
_mover_original = mod_elevadores.mover_elevador


def _mover_com_registro(elevadores_, nome_elevador, andar_destino):
    andar_de = elevadores_[nome_elevador]["andar_atual"]
    _mover_original(elevadores_, nome_elevador, andar_destino)
    if andar_de != andar_destino:
        movimentos_registrados.append(
            {"elevador": nome_elevador, "de": andar_de, "para": andar_destino}
        )


mod_elevadores.mover_elevador = _mover_com_registro

animacao_pendente = None


def capturar_saida(funcao, *args, **kwargs):
    """Redireciona os print() dos módulos para o painel da página."""
    buffer = io.StringIO()
    with contextlib.redirect_stdout(buffer):
        funcao(*args, **kwargs)
    return buffer.getvalue()


# ----- Regras do Modo Caos (protocolo de emergência) ----------

def aplicar_regras_caos():
    """
    Em emergência, privilégios VIP são suspensos: viagens
    expressas já na fila viram comuns e o perfil VIP perde a
    prioridade (passa a valer como comum). A prioridade PCD é
    MANTIDA — acessibilidade não se suspende.
    """
    PRIORIDADES["vip"] = PRIORIDADES["comum"]
    suspensos = 0
    for chamada in fila_chamadas:
        if chamada["expresso"]:
            chamada["expresso"] = False
            suspensos += 1
            print(f"   ⚠️  Viagem expressa de {chamada['usuario']} "
                  f"SUSPENSA (protocolo de emergência).")
    if suspensos == 0:
        print("   ⚠️  Privilégios VIP suspensos enquanto o Modo Caos "
              "estiver ativo (prioridade PCD mantida).")


def restaurar_regras_normais():
    PRIORIDADES["vip"] = VIP_RANK_ORIGINAL
    print("   ✅ Operação normal restabelecida: privilégios VIP reativados.")


def entrada_web(matricula, senha, vip_automatico=False):
    """Adaptador web do evento de catraca (senha vem do formulário)."""
    usuario = cadastro.buscar(matricula)
    if usuario is None:
        interface.log_visitante(matricula)
        return

    expresso = False
    if usuario["perfil"] == "vip":
        if caos_ativo:
            print(f"   ⚠️  Modo Caos ativo: privilégio VIP de "
                  f"{usuario['nome']} suspenso — atendimento comum.")
        elif vip_automatico:
            print(f"   ⭐ Senha VIP de {usuario['nome']} validada "
                  f"automaticamente (modo lote).")
            expresso = True
        elif senha == SENHA_VIP:
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


# ----- Geradores do Evento Crítico ----------------------------

def gerar_entradas_criticas():
    """Fase 1: 30 pessoas entram ao mesmo tempo pela catraca."""
    print("👥 PICO DE ENTRADA: 30 pessoas passando pela catraca "
          "simultaneamente!")
    # Os 15 usuários cadastrados...
    for matricula in cadastro.listar_matriculas():
        entrada_web(matricula, senha="", vip_automatico=True)
    # ...mais 15 alunos gerados na hora (dados fictícios)
    for numero in range(1, 16):
        perfil = "pcd" if random.random() < 0.07 else "comum"
        chamada = chamadas.criar_chamada(
            usuario=f"Aluno {numero}",
            origem=ANDAR_CATRACA,
            destino=random.choice([1, 2, 3, 4]),
            perfil=perfil,
        )
        chamadas.adicionar_na_fila(fila_chamadas, chamada)


def gerar_saidas_criticas():
    """Fase 2: 25 pessoas tentam sair do prédio ao mesmo tempo."""
    print("🏃 PICO DE SAÍDA: 25 pessoas chamando o elevador para "
          "deixar o prédio!")
    nomes_pool = ([u["nome"] for u in cadastro.USUARIOS.values()] +
                  [f"Aluno {n}" for n in range(1, 16)])
    for pessoa in random.sample(nomes_pool, k=25):
        chamada = chamadas.criar_chamada(
            usuario=pessoa,
            origem=random.choice([1, 2, 3, 4]),
            destino=random.choice([0, 0, 0, -1, -2]),
        )
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
  :root { --laranja:#F58220; --escuro:#2b2b2b; --vermelho:#c0392b; }
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

  /* ---------- PRÉDIO ANIMADO ---------- */
  .predio { position:relative; border:1px solid #e3e3e3;
            border-radius:8px; overflow:hidden; }
  .andar-row { display:flex; align-items:stretch; height:44px;
               border-bottom:1px dashed #e8e8e8; transition:background .3s; }
  .andar-row:last-child { border-bottom:none; }
  .andar-row.ativo-A, .andar-row.ativo-B { background:#fff3e6; }
  .andar-nome { flex:1; font-size:.8rem; display:flex;
                align-items:center; padding-left:8px; }
  .poco { width:58px; border-left:1px solid #f0e2d2;
          background:repeating-linear-gradient(0deg,#fafafa,#fafafa 6px,
                     #f3f3f3 6px,#f3f3f3 12px); }
  .poco-cab { display:flex; align-items:center; justify-content:center;
              font-size:.7rem; color:#bbb; }
  .cabine { position:absolute; width:48px; height:38px; border-radius:6px;
            background:var(--laranja); color:#fff; font-weight:bold;
            display:flex; align-items:center; justify-content:center;
            box-shadow:0 2px 6px rgba(0,0,0,.35); font-size:.95rem;
            transition: top .38s linear, left .38s linear; z-index:5; }
  .cabine small { font-size:.6rem; margin-left:2px; }
  .cabine.sem-anim { transition:none !important; }
  .status-anim { font-size:.82rem; margin:6px 0 0; min-height:1.2em;
                 color:#a35a00; font-weight:600; }

  form { margin:0 0 10px; }
  label { font-size:.8rem; display:block; margin:6px 0 2px; }
  input, select { width:100%; padding:6px; border:1px solid #ccc;
                  border-radius:6px; font-size:.9rem; }
  input[type=checkbox] { width:auto; }
  button { margin-top:8px; background:var(--laranja); color:#fff;
           border:none; padding:8px 14px; border-radius:6px;
           cursor:pointer; font-weight:bold; width:100%; }
  button:hover { filter:brightness(.92); }
  button.cinza { background:#666; }
  button.critico { background:var(--vermelho); font-size:.95rem; }
  .linha { display:flex; gap:8px; }
  .linha > div { flex:1; }
  pre.log { grid-column:1 / -1; background:var(--escuro); color:#9fe89f;
            padding:14px; border-radius:10px; font-size:.8rem;
            white-space:pre-wrap; max-height:420px; overflow:auto; }
  .fila { max-height:180px; overflow:auto; padding-left:22px; }
  .fila li { font-size:.85rem; margin-bottom:3px; }
  .badge { background:var(--laranja); color:#fff; border-radius:10px;
           padding:1px 8px; font-size:.75rem; }
  .badge-caos { background:var(--vermelho); }
  footer { text-align:center; font-size:.75rem; color:#888;
           padding:10px 0 20px; }
</style>
</head>
<body>
<header>
  <h1>🛗 Sistema Inteligente de Elevadores — SENAC</h1>
  <p>Catraca integrada · Despacho por Destino · Capacidade {{capacidade}}/cabine ·
     Modo Caos: <strong>{{ 'LIGADO 🎲 (privilégios VIP suspensos)' if caos else 'desligado' }}</strong></p>
</header>
<main>

  <!-- COLUNA ESQUERDA: prédio animado, fila e cadastro -->
  <section class="card">
    <h2>🏢 O Prédio agora</h2>
    <div class="predio" id="predio">
      <div class="andar-row" style="height:20px;border-bottom:1px solid #eee">
        <div class="andar-nome"></div>
        <div class="poco poco-cab">A</div>
        <div class="poco poco-cab">B</div>
      </div>
      {% for andar in andares %}
      <div class="andar-row" id="row-{{andar}}">
        <div class="andar-nome">{{ nomes[andar] }}</div>
        <div class="poco" id="poco-A-{{andar}}"></div>
        <div class="poco" id="poco-B-{{andar}}"></div>
      </div>
      {% endfor %}
      <div class="cabine sem-anim" id="cab-A">🛗<small>A</small></div>
      <div class="cabine sem-anim" id="cab-B">🛗<small>B</small></div>
    </div>
    <p class="status-anim" id="status-A"></p>
    <p class="status-anim" id="status-B"></p>

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

    <h2 style="margin-top:14px">🎫 Cadastro — marque e envie em grupo</h2>
    <form method="post" action="{{ url_for('rota_lote') }}">
      <table>
        <tr><th></th><th>Matr.</th><th>Nome</th><th>Perfil</th><th>Sala</th></tr>
        {% for m, u in usuarios.items() %}
        <tr>
          <td><input type="checkbox" name="matriculas" value="{{ m }}"></td>
          <td>{{ m }}</td><td>{{ icones[u.perfil] }} {{ u.nome }}</td>
          <td>{{ u.perfil }}</td><td>{{ nomes[u.andar_sala] }}</td>
        </tr>
        {% endfor %}
      </table>
      <button>🎫 Passar selecionados pela catraca</button>
    </form>
  </section>

  <!-- COLUNA DIREITA: controles -->
  <section class="card">
    <h2>🎫 Catraca — Entrada individual</h2>
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
    <form method="post" action="{{ url_for('rota_evento') }}">
      <button class="critico">🚨 EVENTO CRÍTICO: 30 entram + 25 saem
              (elevadores em ação simultânea)</button>
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

<script>
  const NOMES = {{ nomes_js | tojson }};
  const POSICOES = {{ posicoes_js | tojson }};
  const ANIM = {{ anim | tojson }};

  function setCabine(elev, andar, instantaneo) {
    const cab = document.getElementById('cab-' + elev);
    const celula = document.getElementById('poco-' + elev + '-' + andar);
    if (!cab || !celula) return;
    if (instantaneo) cab.classList.add('sem-anim');
    cab.style.top = (celula.offsetTop + 3) + 'px';
    cab.style.left = (celula.offsetLeft + 5) + 'px';
    if (instantaneo) {
      void cab.offsetHeight;
      cab.classList.remove('sem-anim');
    }
  }

  function destacarAndar(elev, andar, ligado) {
    const row = document.getElementById('row-' + andar);
    if (row) row.classList.toggle('ativo-' + elev, ligado);
  }

  const pausa = (ms) => new Promise(r => setTimeout(r, ms));

  // Toca a trilha de UM elevador (A e B rodam em paralelo)
  async function tocarTrilha(elev, movimentos, ms) {
    const status = document.getElementById('status-' + elev);
    for (const mv of movimentos) {
      const passo = mv.para > mv.de ? 1 : -1;
      const verbo = passo > 0 ? '⬆️ subindo' : '⬇️ descendo';
      status.textContent = `🛗 ${elev} ${verbo}: ` +
                           `${NOMES[mv.de]} → ${NOMES[mv.para]}`;
      let anterior = mv.de;
      for (let andar = mv.de + passo; ; andar += passo) {
        destacarAndar(elev, anterior, false);
        destacarAndar(elev, andar, true);
        setCabine(elev, andar, false);
        await pausa(ms);
        anterior = andar;
        if (andar === mv.para) break;
      }
      destacarAndar(elev, anterior, false);
      await pausa(Math.min(300, ms));   // portas abrindo/fechando
    }
    if (movimentos.length > 0)
      status.textContent = `✅ Elevador ${elev}: movimentação concluída.`;
  }

  async function reproduzirAnimacao() {
    // Cabines começam onde estavam ANTES do processamento
    for (const elev in ANIM.inicio) setCabine(elev, ANIM.inicio[elev], true);

    // Separa os movimentos por elevador (trilhas independentes)
    const trilhas = { A: [], B: [] };
    let passosTotais = 0;
    for (const mv of ANIM.movimentos) {
      trilhas[mv.elevador].push(mv);
      passosTotais += Math.abs(mv.para - mv.de);
    }
    // Velocidade adaptativa: muito movimento -> filme mais rápido
    const ms = passosTotais > 60 ? 150 : passosTotais > 30 ? 250 : 420;
    document.querySelectorAll('.cabine').forEach(c =>
      c.style.transitionDuration = (ms / 1000) + 's');

    await pausa(500);
    // AS DUAS CABINES SE MOVEM AO MESMO TEMPO:
    await Promise.all([
      tocarTrilha('A', trilhas.A, ms),
      tocarTrilha('B', trilhas.B, ms),
    ]);
  }

  window.addEventListener('load', () => {
    if (ANIM && ANIM.movimentos && ANIM.movimentos.length > 0) {
      reproduzirAnimacao();
    } else {
      for (const elev in POSICOES) setCabine(elev, POSICOES[elev], true);
    }
  });
  window.addEventListener('resize', () => {
    if (!ANIM) for (const elev in POSICOES) setCabine(elev, POSICOES[elev], true);
  });
</script>
</body>
</html>
"""


@app.route("/")
def pagina_inicial():
    global animacao_pendente
    anim = animacao_pendente
    animacao_pendente = None  # a animação toca uma vez; F5 mostra o estado final

    return render_template_string(
        PAGINA,
        andares=sorted(ANDARES_VALIDOS, reverse=True),
        nomes=NOMES_ANDARES,
        nomes_js={str(a): NOMES_ANDARES[a] for a in ANDARES_VALIDOS},
        posicoes_js={n: e["andar_atual"] for n, e in elevadores.items()},
        anim=anim,
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


@app.route("/catraca/lote", methods=["POST"])
def rota_lote():
    """Checkboxes do cadastro: várias pessoas entram de uma vez."""
    global ultimo_log
    matriculas = request.form.getlist("matriculas")
    if not matriculas:
        ultimo_log = "❌ Nenhuma pessoa selecionada — marque as caixinhas no cadastro."
        return redirect(url_for("pagina_inicial"))

    def _lote():
        print(f"👥 GRUPO NA CATRACA: {len(matriculas)} pessoa(s) "
              f"entrando ao mesmo tempo!")
        for matricula in matriculas:
            entrada_web(matricula, senha="", vip_automatico=True)

    ultimo_log = capturar_saida(_lote)
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
    global ultimo_log, animacao_pendente
    posicoes_iniciais = {n: e["andar_atual"] for n, e in elevadores.items()}
    movimentos_registrados.clear()

    def _processar():
        if caos_ativo:
            aplicar_regras_caos()
        chamadas.processar_fila(fila_chamadas, elevadores, caos_ativo)

    ultimo_log = capturar_saida(_processar)

    if movimentos_registrados:
        animacao_pendente = {
            "inicio": posicoes_iniciais,
            "movimentos": list(movimentos_registrados),
        }
    return redirect(url_for("pagina_inicial"))


@app.route("/evento-critico", methods=["POST"])
def rota_evento():
    """
    🚨 Estresse máximo: 30 pessoas entram ao mesmo tempo e, na
    sequência, 25 tentam sair. Roda sob protocolo de emergência
    (regras do Modo Caos: VIP suspenso, panes possíveis) e gera
    uma única animação com os DOIS elevadores trabalhando juntos.
    """
    global ultimo_log, animacao_pendente, caos_ativo
    posicoes_iniciais = {n: e["andar_atual"] for n, e in elevadores.items()}
    movimentos_registrados.clear()
    caos_estava_ligado = caos_ativo
    caos_ativo = True  # o evento crítico SEMPRE roda em protocolo de emergência

    def _evento():
        print("=" * 52)
        print("🚨 EVENTO CRÍTICO — PROTOCOLO DE EMERGÊNCIA ATIVADO")
        print("=" * 52)
        aplicar_regras_caos()
        print()
        print("───── FASE 1: PICO DE ENTRADA ─────")
        gerar_entradas_criticas()
        chamadas.processar_fila(fila_chamadas, elevadores, caos_ativo=True)
        print()
        print("───── FASE 2: PICO DE SAÍDA ─────")
        gerar_saidas_criticas()
        chamadas.processar_fila(fila_chamadas, elevadores, caos_ativo=True)
        print()
        print("🏁 EVENTO CRÍTICO ENCERRADO — prédio esvaziado com sucesso.")

    ultimo_log = capturar_saida(_evento)

    # Restaura o estado do Modo Caos como estava antes do evento
    caos_ativo = caos_estava_ligado
    if not caos_ativo:
        ultimo_log += "\n" + capturar_saida(restaurar_regras_normais)

    if movimentos_registrados:
        animacao_pendente = {
            "inicio": posicoes_iniciais,
            "movimentos": list(movimentos_registrados),
        }
    return redirect(url_for("pagina_inicial"))


@app.route("/caos", methods=["POST"])
def rota_caos():
    global caos_ativo, ultimo_log
    caos_ativo = not caos_ativo
    if caos_ativo:
        ultimo_log = ("🎛️ Modo Caos LIGADO 🎲 — protocolo de emergência:\n"
                      + capturar_saida(aplicar_regras_caos))
    else:
        ultimo_log = ("🎛️ Modo Caos desligado.\n"
                      + capturar_saida(restaurar_regras_normais))
    return redirect(url_for("pagina_inicial"))


@app.route("/relatorio", methods=["POST"])
def rota_relatorio():
    global ultimo_log
    ultimo_log = capturar_saida(estatisticas.exibir_relatorio, elevadores)
    return redirect(url_for("pagina_inicial"))


@app.route("/reiniciar", methods=["POST"])
def rota_reiniciar():
    """Volta ao estado inicial — útil para ensaiar a demo várias vezes."""
    global elevadores, fila_chamadas, caos_ativo, ultimo_log, animacao_pendente
    elevadores = mod_elevadores.criar_elevadores()
    fila_chamadas.clear()
    caos_ativo = False
    PRIORIDADES["vip"] = VIP_RANK_ORIGINAL
    animacao_pendente = None
    ultimo_log = "🔄 Demo reiniciada. Elevador A no Térreo, B no 4º andar."
    return redirect(url_for("pagina_inicial"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
