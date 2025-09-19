from flask import Flask, render_template, request, send_from_directory, flash
import os
from scripts import calendario, gerar_qrcode, PYtube, conversor, media_escolar, conversor_temperatura, senhas, sorteio

app = Flask(__name__)
app.secret_key = "segredo"
OUTPUTS = "outputs"
os.makedirs(OUTPUTS, exist_ok=True)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/calendario", methods=["GET", "POST"])
def calendario_page():
    ano = int(request.form.get("ano", 2025))
    mes = int(request.form.get("mes", 9))
    resultado = calendario.gerar_calendario(ano, mes)
    return render_template("calendario.html", resultado=resultado, ano=ano, mes=mes)

@app.route("/qrcode", methods=["GET", "POST"])
def qrcode_page():
    arquivo = None
    if request.method == "POST":
        texto = request.form.get("texto")
        if texto:
            arquivo = gerar_qrcode.gerar_qrcode(texto, OUTPUTS)
            arquivo = os.path.basename(arquivo)
    return render_template("qrcode.html", arquivo=arquivo)

@app.route("/youtube", methods=["GET", "POST"])
def youtube_page():
    arquivo = None
    erro = None
    # Se estiver rodando no Render, mostra mensagem de aviso
    if os.environ.get("RENDER") == "true":
        erro = "⚠️ Este recurso está disponível apenas na versão local do portal."
    else:
        if request.method == "POST":
            link = request.form.get("link")
            if link:
                try:
                    arquivo = PYtube.baixar_youtube(link, OUTPUTS)
                except Exception as e:
                    erro = f"Erro ao baixar: {e}"
    return render_template("youtube.html", arquivo=arquivo, erro=erro)


@app.route("/conversor", methods=["GET", "POST"])
def conversor_page():
    resultado = None
    erro = None
    valor = None
    de = "USD"
    para = "BRL"

    if request.method == "POST":
        try:
            valor = float(request.form.get("valor", 0))
            de = request.form.get("de", "USD")
            para = request.form.get("para", "BRL")
            resultado = conversor.converter(valor, de, para)
            if resultado is None:
                erro = "Não foi possível obter a taxa de câmbio. Tente novamente."
        except Exception as e:
            erro = f"Erro: {e}"

    return render_template("conversor.html", resultado=resultado, erro=erro, valor=valor, de=de, para=para)


@app.route("/media", methods=["GET", "POST"])
def media_page():
    resultado = None
    if request.method == "POST":
        nota1 = float(request.form.get("nota1", 0))
        nota2 = float(request.form.get("nota2", 0))
        nota3 = float(request.form.get("nota3", 0))
        resultado = media_escolar.calcular_media([nota1, nota2, nota3])
    return render_template("media_escolar.html", resultado=resultado)

@app.route("/temperatura", methods=["GET", "POST"])
def temperatura_page():
    resultado = None
    if request.method == "POST":
        valor = float(request.form.get("valor", 0))
        de = request.form.get("de", "C")
        para = request.form.get("para", "F")
        convertido = conversor_temperatura.converter_temp(valor, de, para)
        resultado = f"{valor} {de} = {convertido:.2f} {para}"
    return render_template("conversor_temperatura.html", resultado=resultado)

@app.route("/senhas", methods=["GET", "POST"])
def senhas_page():
    senha = None
    if request.method == "POST":
        tamanho = int(request.form.get("tamanho", 12))
        senha = senhas.gerar_senha(tamanho)
    return render_template("senhas.html", senha=senha)

@app.route("/sorteio", methods=["GET", "POST"])
def sorteio_page():
    resultado = None
    if request.method == "POST":
        nomes = request.form.get("nomes", "")
        resultado = sorteio.sortear(nomes)
    return render_template("sorteio.html", resultado=resultado)


@app.route("/outputs/<path:filename>")
def arquivos(filename):
    return send_from_directory(OUTPUTS, filename)

if __name__ == "__main__":
    app.run(debug=True)
