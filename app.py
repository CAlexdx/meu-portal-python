from werkzeug.utils import secure_filename
from flask import Flask, render_template, request, send_from_directory, flash
import os
from PIL import Image, UnidentifiedImageError
from uuid import uuid4

# Imports dos módulos (ajuste conforme seus scripts disponíveis)
from scripts import (
    calendario, gerar_qrcode, PYtube, conversor, media_escolar,
    conversor_temperatura, senhas, sorteio, sorteio_equipes, texto_stats, imc,
    editor_imagem, quiz, orcamento, calculadora, tradutor, encurtador
)

app = Flask(__name__)
app.secret_key = "segredo"
OUTPUTS = "outputs"
os.makedirs(OUTPUTS, exist_ok=True)

# Lista de extensões permitidas para o editor de imagens
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def index():
    return render_template("index.html")

# ==========================
# Calendário
# ==========================
@app.route("/calendario", methods=["GET", "POST"])
def calendario_page():
    try:
        ano = int(request.form.get("ano", 2025))
        mes = int(request.form.get("mes", 9))
    except ValueError:
        flash("Ano ou mês inválido.", "error")
        return render_template("calendario.html", resultado=None, feriados=None)

    if not (1900 <= ano <= 2100) or not (1 <= mes <= 12):
        flash("Ano ou mês fora do intervalo permitido.", "error")
        return render_template("calendario.html", resultado=None, feriados=None, ano=ano, mes=mes)

    resultado, feriados = calendario.gerar_calendario(ano, mes)
    return render_template("calendario.html", resultado=resultado, feriados=feriados, ano=ano, mes=mes)

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
        erro = "⚠️ Este recurso só funciona na versão local do portal."
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
        try:
            notas = [
                float(request.form.get("nota1", 0)),
                float(request.form.get("nota2", 0)),
                float(request.form.get("nota3", 0)),
            ]
            resultado = media_escolar.calcular_media(notas)
        except ValueError:
            flash("Notas inválidas.", "error")
    return render_template("media_escolar.html", resultado=resultado)

# ==========================
# Conversor de temperatura
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
# Sorteio simples
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
# Sorteio de equipes
# ==========================
@app.route("/equipes", methods=["GET", "POST"])
def equipes_page():
    equipes, erro = None, None
    if request.method == "POST":
        nomes = request.form.get("nomes", "")
        try:
            qtd = int(request.form.get("qtd", 2))
            equipes, erro = sorteio_equipes.sortear_equipes(nomes, qtd)
        except ValueError:
            erro = "Número de equipes inválido."
    return render_template("equipes.html", equipes=equipes, erro=erro)

# ==========================
# Texto Stats
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
    arquivo = None
    if request.method == "POST":
        if "imagem" not in request.files:
            flash("Nenhum arquivo enviado.", "error")
        else:
            imagem = request.files["imagem"]
            if imagem.filename == "":
                flash("Nenhum arquivo selecionado.", "error")
            elif not allowed_file(imagem.filename):
                flash("Extensão não permitida.", "error")
            else:
                try:
                    nome_seguro = f"{uuid4().hex}_{secure_filename(imagem.filename)}"
                    caminho_temp = os.path.join(OUTPUTS, nome_seguro)
                    imagem.save(caminho_temp)
                    Image.open(caminho_temp).verify()
                    filtro = request.form.get("filtro", "bw")
                    arquivo_processado_path = editor_imagem.aplicar_filtro(caminho_temp, filtro, OUTPUTS)
                    arquivo = os.path.basename(arquivo_processado_path)
                    flash("Filtro aplicado com sucesso!", "success")
                except UnidentifiedImageError:
                    flash("Arquivo inválido ou corrompido.", "error")
                    if os.path.exists(caminho_temp):
                        os.remove(caminho_temp)
    return render_template("editor_imagem.html", arquivo=arquivo)

# ==========================
# Quiz
# ==========================
@app.route("/quiz", methods=["GET", "POST"])
def quiz_page():
    pergunta = quiz.pegar_pergunta()
    resultado = None
    if request.method == "POST":
        resposta = request.form.get("resposta")
        correta = request.form.get("correta")
        resultado = "✅ Resposta correta!" if resposta == correta else f"❌ Errado! O certo era: {correta}"
    return render_template("quiz.html", pergunta=pergunta, resultado=resultado)

# ==========================
# Orçamento
# ==========================
@app.route("/orcamento", methods=["GET", "POST"])
def orcamento_page():
    resumo, csv_file = None, None
    if request.method == "POST":
        receitas = request.form.get("receitas", "")
        despesas = request.form.get("despesas", "")
        try:
            resumo = orcamento.resumir(receitas, despesas)
            caminho_csv = orcamento.gerar_csv(resumo, OUTPUTS)
            csv_file = os.path.basename(caminho_csv)
        except ValueError as e:
            flash(str(e), "error")
    return render_template("orcamento.html", resumo=resumo, csv_file=csv_file)

# ==========================
# Calculadora
# ==========================
@app.route("/calculadora", methods=["GET", "POST"])
def calculadora_page():
    resultado, erro = None, None
    if request.method == "POST":
        oper = request.form.get("operacao")
        a = request.form.get("a")
        b = request.form.get("b")
        res, err = calculadora.calcular(oper, a, b)
        if err:
            erro = err
        else:
            resultado = round(res, 6) if isinstance(res, (int, float)) else res
    return render_template("calculadora.html", resultado=resultado, erro=erro)

# ==========================
# Tradutor
# ==========================
@app.route("/tradutor", methods=["GET", "POST"])
def tradutor_page():
    traducao, erro = None, None
    if request.method == "POST":
        texto = request.form.get("texto", "")
        target = request.form.get("target", "en")
        traduzido = tradutor.traduzir(texto, source="pt", target=target)
        if traduzido:
            traducao = traduzido
        else:
            erro = "Não foi possível traduzir no momento."
    return render_template("tradutor.html", traducao=traducao, erro=erro)

# ==========================
# Encurtador de links
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
# Outputs
# ==========================
@app.route("/outputs/<path:filename>")
def arquivos(filename):
    return send_from_directory(OUTPUTS, filename)

if __name__ == "__main__":
    app.run(debug=True)
