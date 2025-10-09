import os
import io
import base64
from uuid import uuid4

from flask import Flask, render_template, jsonify, request, send_from_directory, flash, session, redirect, url_for
from werkzeug.utils import secure_filename
from PIL import Image, UnidentifiedImageError
from scripts.tradutor import traduzir

# Imports dos módulos
from scripts import (
    calendario, gerar_qrcode, PYtube, conversor, media_escolar,
    conversor_temperatura, senhas, sorteio, sorteio_equipes, texto_stats, imc,
    editor_imagem, quiz, orcamento, calculadora, tradutor, encurtador, juros_compostos, mapa_turistico,
    clima
)

# Configuração básica
app = Flask(__name__)
app.secret_key = "segredo"
OUTPUTS = "outputs"
os.makedirs(OUTPUTS, exist_ok=True)

# Extensões permitidas para upload de imagens
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/")
def index():
    return render_template("index.html")


# ==========================
# Calendário
# ==========================
from scripts.calendario import gerar_calendario, MESES_PT, DIAS_PT # Importa tudo o que precisamos

@app.route("/calendario", methods=["GET", "POST"])
def calendario_page():
    try:
        ano = int(request.form.get("ano", 2025))
        mes = int(request.form.get("mes", 9))
    except ValueError:
        flash("Ano ou mês inválido.", "error")
        # Passa MESES_PT e DIAS_PT para o template, mesmo em caso de erro
        return render_template("calendario.html", dias_do_mes=None, feriados=None, ano=ano, mes=mes, MESES_PT=MESES_PT, dias_semana=DIAS_PT)

    if not (1900 <= ano <= 2100) or not (1 <= mes <= 12):
        flash("Ano ou mês fora do intervalo permitido.", "error")
        # Passa MESES_PT e DIAS_PT para o template, mesmo em caso de erro
        return render_template("calendario.html", dias_do_mes=None, feriados=None, ano=ano, mes=mes, MESES_PT=MESES_PT, dias_semana=DIAS_PT)

    # Agora a função retorna dias_do_mes, dias_semana e feriados
    dias_do_mes, dias_semana, feriados = gerar_calendario(ano, mes)
    return render_template("calendario.html", dias_do_mes=dias_do_mes, feriados=feriados, ano=ano, mes=mes, MESES_PT=MESES_PT, dias_semana=dias_semana)


# ==========================
# QR Code
# ==========================
@app.route("/qrcode", methods=["GET", "POST"])
def qrcode_page():
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


# ==========================
# YouTube Downloader
# ==========================
@app.route("/youtube", methods=["GET", "POST"])
def youtube_page():
    arquivo = None
    erro = None
    if os.environ.get("RENDER") == "true":
        erro = ( "⚠️ O módulo de download do YouTube não está disponível na versão online. "
        "Por motivos de segurança e restrições da plataforma Render, "
        "o servidor em nuvem não permite conexões diretas com o YouTube. "
        "Para utilizar este recurso, execute o portal localmente no seu computador."
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


# ==========================
# Conversor de moedas
# ==========================
@app.route("/conversor", methods=["GET", "POST"])
def conversor_page():
    resultado, erro, valor = None, None, None
    de, para = "USD", "BRL"
    if request.method == "POST":
        try:
            valor = float(request.form.get("valor", 0))
            de = request.form.get("de", "USD")
            para = request.form.get("para", "BRL")
            resultado = conversor.converter(valor, de, para)
            if resultado is None:
                erro = "Não foi possível obter a taxa de câmbio."
        except ValueError:
            erro = "Valor inválido."
    return render_template("conversor.html", resultado=resultado, erro=erro, valor=valor, de=de, para=para)


# ==========================
# Média Escolar
# ==========================
@app.route("/media", methods=["GET", "POST"])
def media_page():
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

# ==========================
# Conversor de Temperatura
# ==========================
@app.route("/temperatura", methods=["GET", "POST"])
def temperatura_page():
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


# ==========================
# Gerador de Senhas
# ==========================
@app.route("/senhas", methods=["GET", "POST"])
def senhas_page():
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


# ==========================
# Sorteio Simples
# ==========================
@app.route("/sorteio", methods=["GET", "POST"])
def sorteio_page():
    resultado = None
    if request.method == "POST":
        nomes = request.form.get("nomes", "")
        resultado, err = sorteio.sortear(nomes)
        if err:
            flash(err, "error")
    return render_template("sorteio.html", resultado=resultado)


# ==========================
# Sorteio de Equipes
# ==========================
@app.route("/equipes", methods=["GET", "POST"])
def equipes_page():
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


# ==========================
# Analisador de Texto
# ==========================
@app.route("/texto", methods=["GET", "POST"])
def texto_page():
    resultado = None
    if request.method == "POST":
        texto = request.form.get("texto", "")
        resultado, err = texto_stats.analisar_texto(texto)
        if err:
            flash(err, "error")
    return render_template("texto_stats.html", resultado=resultado)


# ==========================
# IMC
# ==========================
@app.route("/imc", methods=["GET", "POST"])
def imc_page():
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

# ==========================
# Editor de Imagens
# ==========================
@app.route("/editor", methods=["GET", "POST"])
def editor_page():
    imagem_processada = None
    erro = None

    if request.method == "POST":
        # Verifique se o arquivo está presente
        if "imagem" not in request.files or request.files["imagem"].filename == "":
            erro = "Nenhum arquivo enviado ou selecionado."
        else:
            imagem_file = request.files["imagem"]
            # Verifique se a extensão é permitida
            if not allowed_file(imagem_file.filename):
                erro = "Extensão de arquivo não permitida."
            else:
                try:
                    img = Image.open(imagem_file.stream)

                    # Obtenha o filtro selecionado (apenas um)
                    filtro_selecionado = request.form.get("filtro", "original")

                    # Obtenha e converta os valores dos sliders (de 0-200 para 0-2.0)
                    brilho = float(request.form.get("brilho", 100)) / 100
                    contraste = float(request.form.get("contraste", 100)) / 100
                    nitidez = float(request.form.get("nitidez", 100)) / 100

                    # Aplique o filtro, se não for o "original"
                    if filtro_selecionado != "original":
                        img = editor_imagem.aplicar_filtros(img, [filtro_selecionado])

                    # Aplique os ajustes de imagem
                    img_editada = editor_imagem.ajustar_imagem(img, brilho, contraste, nitidez)
                    
                    # Salve a imagem em memória
                    img_byte_arr = io.BytesIO()
                    img_editada.save(img_byte_arr, format="PNG")
                    img_byte_arr = img_byte_arr.getvalue()
                    imagem_processada = base64.b64encode(img_byte_arr).decode('ascii')

                except Exception as e:
                    erro = f"Erro ao processar imagem: {e}"

    return render_template("editor_imagem.html", imagem_processada=imagem_processada, erro=erro)

# ==========================
# Quiz de Programação
# ==========================
@app.route("/iniciar_quiz")
def iniciar_quiz():
    quiz.inicializar_quiz(session)
    return redirect(url_for('quiz_page'))

@app.route("/quiz", methods=["GET", "POST"])
def quiz_page():
    if 'perguntas_restantes_ids' not in session:
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


# ==========================
# Orçamento
# ==========================
@app.route("/orcamento", methods=["GET", "POST"])
def orcamento_page():
    resumo, erro, csv_file = None, None, None
    if request.method == "POST":
        receitas_texto = request.form.get("receitas", "").strip()
        despesas_texto = request.form.get("despesas", "").strip()

        if not receitas_texto and not despesas_texto:
            erro = "Por favor, digite algumas receitas ou despesas."
        else:
            try:
                resumo = orcamento.resumir(receitas_texto, despesas_texto)
                # Caso queira gerar CSV: csv_file = orcamento.gerar_csv(resumo, OUTPUTS)
            except ValueError as e:
                erro = str(e)
            except Exception as e:
                erro = f"Ocorreu um erro inesperado: {e}"

    return render_template("orcamento.html", resumo=resumo, erro=erro, csv_file=csv_file)

@app.route("/downloads/<filename>")
def download_file(filename):
    return send_from_directory(OUTPUTS, filename, as_attachment=True)


# ==========================
# Calculadora
# ==========================
@app.route("/calculadora", methods=["GET", "POST"])
def calculadora_page():
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
            # Arredonda para 6 casas decimais se for um número, senão mantém o valor
            resultado = round(res, 6) if isinstance(res, (int, float)) else res

    return render_template("calculadora.html", resultado=resultado, erro=erro, a=a, b=b, operacao=operacao)



# ==========================
# Tradutor
# ==========================
@app.route("/tradutor", methods=["GET", "POST"])
def tradutor_page():
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


# ==========================
# Encurtador de Links
# ==========================
@app.route("/encurtador", methods=["GET", "POST"])
def encurtador_page():
    short, erro = None, None
    if request.method == "POST":
        link = request.form.get("link", "")
        short = encurtador.encurtar(link)
        if not short:
            erro = "Falha ao encurtar. Verifique o link."
    return render_template("encurtador.html", short=short, erro=erro)

# ==========================
# Juros Compostos
# ==========================
@app.route("/juros_compostos", methods=["GET", "POST"])
def juros_compostos_page():
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

# ==========================
# Clima
# ==========================
@app.route("/clima", methods=["GET", "POST"])
def clima_page():
    dados = None
    cidade = ""
    if request.method == "POST":
        cidade = request.form.get("cidade", "").strip()
        if cidade:
            dados = clima.obter_clima(cidade)
    return render_template("clima.html", dados=dados, cidade=cidade)

# ==========================
# Mapa Turístico
# ==========================
@app.route("/mapa_turistico")
def mapa_turistico_view():
    return render_template("mapa_turistico.html")

@app.route("/pontos_turisticos")
def pontos_turisticos_json():
    return jsonify(mapa_turistico.obter_pontos_turisticos())

# ==========================
# Outputs
# ==========================
@app.route("/outputs/<path:filename>")
def arquivos(filename):
    return send_from_directory(OUTPUTS, filename)


# ==========================
# Inicialização
# ==========================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Usa a porta do Render ou 5000 localmente
    app.run(host="0.0.0.0", port=port, debug=True)
