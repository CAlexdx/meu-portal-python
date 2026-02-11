import os
import io
import base64
import json
from uuid import uuid4
from functools import wraps
from dotenv import load_dotenv  # Importante para ler o arquivo .env

from flask import Flask, render_template, jsonify, request, send_from_directory, flash, session, redirect, url_for
from werkzeug.utils import secure_filename
from PIL import Image, UnidentifiedImageError

# Scripts do projeto
from scripts.tradutor import traduzir
from scripts.consumo_combustivel import calcular_consumo_medio
from scripts.calendario import gerar_calendario, MESES_PT, DIAS_PT
from scripts.conversor_tempo import converter_tempo
from scripts.conversor_medidas import converter_medida

from scripts import (
    calendario, conversor_medidas, gerar_qrcode, PYtube, conversor, media_escolar,
    conversor_temperatura, senhas, sorteio, sorteio_equipes, texto_stats, imc,
    editor_imagem, quiz, orcamento, calculadora, tradutor, encurtador, juros_compostos, mapa_turistico,
    clima, clt_vs_pj
)

# ==========================================
# 1. CONFIGURAÇÃO BÁSICA DO APP
# ==========================================
app = Flask(__name__)
app.secret_key = "segredo" # Idealmente, coloque isso no .env também futuramente
OUTPUTS = "outputs"
os.makedirs(OUTPUTS, exist_ok=True)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# ==========================================
# 2. SISTEMA DE SEGURANÇA (ADMIN)
# ==========================================

# Carrega as variáveis do arquivo .env (se existir localmente)
load_dotenv()

# Tenta pegar do sistema (Render/.env). Se não achar, usa o padrão "admin"/"1234"
ADMIN_USER = os.environ.get("ADMIN_USER", "admin")
ADMIN_PASS = os.environ.get("ADMIN_PASS", "1234")

# Decorador que protege a rota
def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        # Verifica se o usuário e senha batem com o configurado no sistema
        if auth and auth.username == ADMIN_USER and auth.password == ADMIN_PASS:
            return f(*args, **kwargs)
        # Se errar, pede login de novo
        return ('Acesso Negado. Login necessário.', 401, 
                {'WWW-Authenticate': 'Basic realm="Login Requerido"'})
    return decorated

# ==========================================
# 3. SISTEMA DE ESTATÍSTICAS (JSON)
# ==========================================

# Função para ler o arquivo JSON
def carregar_stats():
    try:
        if os.path.exists('stats.json'):
            with open('stats.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        # Se não existir, cria o padrão zerado
        return {"total": 0, "ferramentas": {}}
    except:
        return {"total": 0, "ferramentas": {}}

# Função para salvar no arquivo JSON
def salvar_stats(dados):
    try:
        with open('stats.json', 'w', encoding='utf-8') as f:
            json.dump(dados, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"Erro ao salvar stats: {e}")

# Função auxiliar para registrar uso de ferramentas
def registrar_uso(nome_ferramenta):
    stats = carregar_stats()
    stats["ferramentas"][nome_ferramenta] = stats["ferramentas"].get(nome_ferramenta, 0) + 1
    salvar_stats(stats)

# ==========================================
# 4. ROTAS PRINCIPAIS (INDEX E ADMIN)
# ==========================================

@app.route("/")
def index():
    stats = carregar_stats()
    
    # Lógica de contagem de visita única por sessão
    if 'contado' not in session:
        stats["total"] += 1
        salvar_stats(stats)
        session['contado'] = True
    
    return render_template("index.html", total_acessos=stats["total"])

@app.route("/api/stats")
def api_stats():
    stats = carregar_stats()
    return jsonify({"total": stats["total"]})

# Rota protegida pelo login_required
@app.route("/admin")
@login_required
def admin_panel():
    stats = carregar_stats()
    return render_template("admin.html", stats=stats)


# ==========================
# Ferramentas (Com Registro de Uso)
# ==========================

@app.route("/calendario", methods=["GET", "POST"])
def calendario_page():
    registrar_uso("calendario")
    try:
        ano = int(request.form.get("ano", 2025))
        mes = int(request.form.get("mes", 9))
    except ValueError:
        flash("Ano ou mês inválido.", "error")
        return render_template("calendario.html", dias_do_mes=None, feriados=None, ano=ano, mes=mes, MESES_PT=MESES_PT, dias_semana=DIAS_PT)

    if not (1900 <= ano <= 2100) or not (1 <= mes <= 12):
        flash("Ano ou mês fora do intervalo permitido.", "error")
        return render_template("calendario.html", dias_do_mes=None, feriados=None, ano=ano, mes=mes, MESES_PT=MESES_PT, dias_semana=DIAS_PT)

    dias_do_mes, dias_semana, feriados = gerar_calendario(ano, mes)
    return render_template("calendario.html", dias_do_mes=dias_do_mes, feriados=feriados, ano=ano, mes=mes, MESES_PT=MESES_PT, dias_semana=dias_semana)


@app.route("/qrcode", methods=["GET", "POST"])
def qrcode_page():
    registrar_uso("qrcode")
    arquivo = None
    if request.method == "POST":
        texto = request.form.get("texto", "").strip()
        if not texto:
            flash("Digite um texto para gerar o QR Code.", "error")
        else:
            try:
                arquivo = gerar_qrcode.gerar_qrcode(texto, OUTPUTS)
                arquivo = os.path.basename(arquivo)
            except Exception as e:
                flash(f"Erro ao gerar QR Code: {e}", "error")
    return render_template("qrcode.html", arquivo=arquivo)


@app.route("/youtube", methods=["GET", "POST"])
def youtube_page():
    registrar_uso("youtube")
    arquivo = None
    erro = None
    if os.environ.get("RENDER") == "true":
        erro = ( "⚠️ O módulo de download do YouTube não está disponível na versão online. "
        "Por motivos de segurança e restrições da plataforma Render."
        )
    elif request.method == "POST":
        link = request.form.get("link", "").strip()
        if not link.startswith("http"):
            erro = "Link inválido."
        else:
            try:
                arquivo = PYtube.baixar_youtube(link, OUTPUTS)
            except Exception:
                erro = "Erro ao baixar o vídeo (restrição ou serviço indisponível)."
    return render_template("youtube.html", arquivo=arquivo, erro=erro)


@app.route("/conversor", methods=["GET", "POST"])
def conversor_page():
    registrar_uso("conversor_moedas")
    resultado, erro, valor_float = None, None, None
    de, para = "USD", "BRL"
    
    if request.method == "POST":
        try:
            valor_raw = request.form.get("valor", "0").replace(',', '.')
            valor_float = float(valor_raw)
            de = request.form.get("de", "USD")
            para = request.form.get("para", "BRL")
            resultado = conversor.converter(valor_float, de, para)
            
            if resultado is None:
                erro = "Não foi possível obter a taxa de câmbio."
        except ValueError:
            erro = "Por favor, insira um valor numérico válido."
            
    return render_template("conversor.html", resultado=resultado, erro=erro, valor=valor_float, de=de, para=para)


@app.route("/media", methods=["GET", "POST"])
def media_page():
    registrar_uso("media_escolar")
    resultado = None
    if request.method == "POST":
        materias_dict = {}
        for key, value in request.form.items():
            if key.startswith("materia_") and value.strip():
                materia = value.strip()
                idx = key.split("_")[1]
                tipos = request.form.getlist(f"tipo_{idx}[]")
                notas = request.form.getlist(f"nota_{idx}[]")
                avaliacoes = {}
                for t, n in zip(tipos, notas):
                    try:
                        n = float(n)
                        if 0 <= n <= 10:
                            avaliacoes[t] = n
                    except ValueError:
                        continue
                if avaliacoes:
                    materias_dict[materia] = avaliacoes

        resultado = media_escolar.calcular_media(materias_dict)

    return render_template("media_escolar.html", resultado=resultado)


@app.route("/temperatura", methods=["GET", "POST"])
def temperatura_page():
    registrar_uso("conversor_temperatura")
    resultado = None
    if request.method == "POST":
        try:
            valor = float(request.form.get("valor", 0))
            de = request.form.get("de", "C")
            para = request.form.get("para", "F")
            convertido = conversor_temperatura.converter_temp(valor, de, para)
            resultado = f"{valor} {de} = {convertido:.2f} {para}"
        except ValueError:
            flash("Valor inválido.", "error")
    return render_template("conversor_temperatura.html", resultado=resultado)


@app.route("/senhas", methods=["GET", "POST"])
def senhas_page():
    registrar_uso("gerador_senhas")
    senha = None
    if request.method == "POST":
        try:
            tamanho = int(request.form.get("tamanho", 12))
            if not (4 <= tamanho <= 32):
                flash("Tamanho inválido (mín 4, máx 32).", "error")
            else:
                senha = senhas.gerar_senha(tamanho)
        except ValueError:
            flash("Entrada inválida.", "error")
    return render_template("senhas.html", senha=senha)


@app.route("/sorteio", methods=["GET", "POST"])
def sorteio_page():
    registrar_uso("sorteio_simples")
    resultado = None
    if request.method == "POST":
        nomes = request.form.get("nomes", "")
        resultado, err = sorteio.sortear(nomes)
        if err:
            flash(err, "error")
    return render_template("sorteio.html", resultado=resultado)


@app.route("/equipes", methods=["GET", "POST"])
def equipes_page():
    registrar_uso("sorteio_equipes")
    equipes, erro = None, None
    if request.method == "POST":
        nomes = request.form.get("nomes", "")
        try:
            qtd_input = request.form.get("qtd", "2")
            qtd = int(qtd_input) if qtd_input.isdigit() else 2
            equipes, erro = sorteio_equipes.sortear_equipes(nomes, qtd)
        except Exception as e:
            erro = "Erro ao sortear equipes: " + str(e)
    return render_template("equipes.html", equipes=equipes, erro=erro)


@app.route("/texto", methods=["GET", "POST"])
def texto_page():
    registrar_uso("analisador_texto")
    resultado = None
    if request.method == "POST":
        texto = request.form.get("texto", "")
        resultado, err = texto_stats.analisar_texto(texto)
        if err:
            flash(err, "error")
    return render_template("texto_stats.html", resultado=resultado)


@app.route("/imc", methods=["GET", "POST"])
def imc_page():
    registrar_uso("calculadora_imc")
    resultado = None
    if request.method == "POST":
        peso = request.form.get("peso", 0)
        altura = request.form.get("altura", 1)
        res, err = imc.calcular_imc(peso, altura)
        if err:
            flash(err, "error")
        else:
            resultado = res
    return render_template("imc.html", resultado=resultado)


@app.route("/editor", methods=["GET", "POST"])
def editor_page():
    registrar_uso("editor_imagem")
    imagem_processada = None
    erro = None
    filtros_disponiveis = [
        "preto_branco", "sepia", "inverter", "blur", "contorno",
        "bordas", "detalhe", "realce", "saturacao_alta", "saturacao_baixa",
        "nitidez", "escurecer", "clarear"
    ]

    if request.method == "POST":
        try:
            if "imagem" not in request.files:
                erro = "Nenhuma imagem enviada."
                return render_template("editor_filtros.html", erro=erro, filtros=filtros_disponiveis)

            imagem_file = request.files["imagem"]
            if imagem_file.filename == "":
                erro = "Nenhum arquivo selecionado."
                return render_template("editor_filtros.html", erro=erro, filtros=filtros_disponiveis)

            filtro = request.form.get("filtro", "preto_branco")
            from scripts import editor_imagem
            from PIL import Image
            img = Image.open(imagem_file.stream)
            img_editada = editor_imagem.aplicar_filtros(img, [filtro])

            import io, base64
            img_bytes = io.BytesIO()
            img_editada.save(img_bytes, format="PNG")
            img_bytes = img_bytes.getvalue()
            imagem_processada = base64.b64encode(img_bytes).decode('utf-8')

        except Exception as e:
            erro = f"Erro ao processar a imagem: {e}"

    return render_template(
        "editor_imagem.html",
        erro=erro,
        filtros=filtros_disponiveis,
        imagem_processada=imagem_processada
    )


@app.route("/iniciar_quiz")
def iniciar_quiz():
    quiz.inicializar_quiz(session)
    return redirect(url_for('quiz_page'))


@app.route("/quiz", methods=["GET", "POST"])
def quiz_page():
    # Nota: Não coloquei registrar_uso aqui para não contar cada resposta como uma visita nova
    if 'perguntas_restantes_ids' not in session:
        registrar_uso("quiz") # Conta apenas quando inicia
        quiz.inicializar_quiz(session)

    if request.method == "POST":
        resposta_usuario = request.form.get('resposta')
        resposta_correta = request.form.get('correta')
        pergunta_id_respondida = int(request.form.get('pergunta_id'))

        feedback = ""
        if resposta_usuario == resposta_correta:
            session['pontuacao'] += 1
            feedback = "Correto! 🎉"
        else:
            feedback = f"Errado. A resposta correta era: {resposta_correta} 😔"

        session['total_perguntas_respondidas'] += 1
        if pergunta_id_respondida in session['perguntas_restantes_ids']:
            session['perguntas_restantes_ids'].remove(pergunta_id_respondida)

        session['ultimo_feedback'] = feedback

    proxima_pergunta = quiz.pegar_proxima_pergunta(session)

    if proxima_pergunta:
        feedback_para_exibir = session.pop('ultimo_feedback', None)
        return render_template('quiz.html', pergunta=proxima_pergunta, resultado=feedback_para_exibir)
    else:
        pontuacao_final = session.get('pontuacao', 0)
        total_respondidas = session.get('total_perguntas_respondidas', len(quiz.get_todas_perguntas()))
        mensagem_final = f"Fim do Quiz! Sua pontuação final é: {pontuacao_final} de {total_respondidas} perguntas."
        session.clear()
        return render_template('quiz_final.html', mensagem=mensagem_final)


@app.route("/orcamento", methods=["GET", "POST"])
def orcamento_page():
    registrar_uso("orcamento")
    resumo, erro, csv_file = None, None, None
    if request.method == "POST":
        receitas_texto = request.form.get("receitas", "").strip()
        despesas_texto = request.form.get("despesas", "").strip()

        if not receitas_texto and not despesas_texto:
            erro = "Por favor, digite algumas receitas ou despesas."
        else:
            try:
                resumo = orcamento.resumir(receitas_texto, despesas_texto)
            except ValueError as e:
                erro = str(e)
            except Exception as e:
                erro = f"Ocorreu um erro inesperado: {e}"

    return render_template("orcamento.html", resumo=resumo, erro=erro, csv_file=csv_file)


@app.route("/downloads/<filename>")
def download_file(filename):
    return send_from_directory(OUTPUTS, filename, as_attachment=True)


@app.route("/calculadora", methods=["GET", "POST"])
def calculadora_page():
    registrar_uso("calculadora")
    resultado, erro = None, None
    a, b, operacao = None, None, None

    if request.method == "POST":
        operacao = request.form.get("operacao")
        a = request.form.get("a")
        b = request.form.get("b")
        res, err = calculadora.calcular(operacao, a, b)
        if err:
            erro = err
        else:
            resultado = round(res, 6) if isinstance(res, (int, float)) else res

    return render_template("calculadora.html", resultado=resultado, erro=erro, a=a, b=b, operacao=operacao)


@app.route("/tradutor", methods=["GET", "POST"])
def tradutor_page():
    registrar_uso("tradutor")
    traducao, erro = None, None
    texto_original = ""
    target_lang_selected = "en"

    if request.method == "POST":
        texto_original = request.form.get("texto", "").strip()
        target_lang_selected = request.form.get("target", "en")
        
        if not texto_original:
            erro = "Por favor, digite um texto para traduzir."
        else:
            traducao, erro = traduzir(texto_original, target=target_lang_selected)
            
    return render_template("tradutor.html", 
                           traducao=traducao, 
                           erro=erro, 
                           texto_original=texto_original,
                           target_lang_selected=target_lang_selected)


@app.route("/encurtador", methods=["GET", "POST"])
def encurtador_page():
    registrar_uso("encurtador")
    short, erro = None, None
    if request.method == "POST":
        link = request.form.get("link", "")
        short = encurtador.encurtar(link)
        if not short:
            erro = "Falha ao encurtar. Verifique o link."
    return render_template("encurtador.html", short=short, erro=erro)


@app.route("/juros_compostos", methods=["GET", "POST"])
def juros_compostos_page():
    registrar_uso("juros_compostos")
    resultado, erro = None, None

    if request.method == "POST":
        capital_inicial = request.form.get("capital_inicial", 0)
        aporte_mensal = request.form.get("aporte_mensal", 0)
        taxa_juros_anual = request.form.get("taxa_juros_anual", 0)
        tempo = request.form.get("tempo", 0)
        periodo = request.form.get("periodo", "meses")

        resultado, erro = juros_compostos.calcular_juros_compostos(
            capital_inicial, taxa_juros_anual, tempo, periodo, aporte_mensal
        )

    return render_template("juros_compostos.html", resultado=resultado, erro=erro)


@app.route("/clima", methods=["GET", "POST"])
def clima_page():
    registrar_uso("clima")
    dados = None
    cidade = ""
    if request.method == "POST":
        cidade = request.form.get("cidade", "").strip()
        if cidade:
            dados = clima.obter_clima(cidade)
    return render_template("clima.html", dados=dados, cidade=cidade)


@app.route("/mapa_turistico")
def mapa_turistico_view():
    registrar_uso("mapa_turistico")
    return render_template("mapa_turistico.html")

@app.route("/pontos_turisticos")
def pontos_turisticos_json():
    return jsonify(mapa_turistico.obter_pontos_turisticos())


@app.route("/consumo_combustivel", methods=["GET", "POST"])
def consumo_combustivel_page():
    registrar_uso("consumo_combustivel")
    resultado = None
    erro = None
    if request.method == "POST":
        try:
            distancia = float(request.form["distancia"])
            consumo = float(request.form["consumo"])
            preco = float(request.form["preco"])
            ida_volta = "ida_volta" in request.form

            if ida_volta:
                distancia *= 2 

            if consumo <= 0:
                erro = "O consumo médio deve ser maior que zero."
            else:
                litros_gastos = distancia / consumo
                custo_total = litros_gastos * preco
                resultado = (f"Para percorrer {distancia:.2f} km, "
                             f"você gastará aproximadamente {litros_gastos:.2f} litros "
                             f"de combustível, com custo total de R$ {custo_total:.2f}.")
        except ValueError:
            erro = "Por favor, insira apenas números válidos."
    return render_template("consumo_combustivel.html", resultado=resultado, erro=erro)


@app.route("/conversor_tempo", methods=["GET", "POST"])
def conversor_tempo_page():
    registrar_uso("conversor_tempo")
    resultado = None
    erro = None
    if request.method == "POST":
        valor = request.form.get("valor", "").strip()
        unidade_origem = request.form.get("unidade_origem", "").strip()
        unidade_destino = request.form.get("unidade_destino", "").strip()
        if not valor or not unidade_origem or not unidade_destino:
            erro = "Erro: Preencha todos os campos."
        else:
            resultado, erro = converter_tempo(valor, unidade_origem, unidade_destino)
    return render_template("conversor_tempo.html", resultado=resultado, erro=erro)


@app.route("/conversor_medidas", methods=["GET", "POST"])
def conversor_medidas_page():
    registrar_uso("conversor_medidas")
    resultado = erro = None
    if request.method == "POST":
        valor = request.form.get("valor")
        de = request.form.get("de")
        para = request.form.get("para")
        r = converter_medida(valor, de, para)
        if r is None:
            erro = "Não foi possível converter as unidades selecionadas."
        else:
            resultado = round(r, 4)
    return render_template("conversor_medidas.html", resultado=resultado, erro=erro)


@app.route("/clt_vs_pj", methods=["GET", "POST"])
def clt_vs_pj_page():
    registrar_uso("clt_vs_pj")
    resultado = erro = None
    if request.method == "POST":
        salario = request.form.get("salario", 0)
        dependentes = request.form.get("dependentes", 0)
        resultado, erro = clt_vs_pj.calcular_clt_vs_pj(salario, dependentes)
    return render_template("clt_vs_pj.html", resultado=resultado, erro=erro)


@app.route("/outputs/<path:filename>")
def arquivos(filename):
    return send_from_directory(OUTPUTS, filename)
    
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)