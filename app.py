from werkzeug.utils import secure_filename
from flask import Flask, render_template, request, send_from_directory, flash
import os
from PIL import Image, UnidentifiedImageError # Importe Image e UnidentifiedImageError
# from scripts import calendario, gerar_qrcode, PYtube, conversor, media_escolar, conversor_temperatura, senhas, sorteio, texto_stats, imc, editor_imagem, quiz
# ^^^ Comentei para evitar erros se você não tiver todos os scripts, descomente no seu ambiente real

# Ajuste os imports para o seu projeto real
from scripts import (
    calendario, gerar_qrcode, PYtube, conversor, media_escolar,
    conversor_temperatura, senhas, sorteio, texto_stats, imc,
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

@app.route("/calendario", methods=["GET", "POST"])
def calendario_page():
    # Adicionando validação para ano e mês (se desejar, similar ao editor_imagem)
    ano = int(request.form.get("ano", 2025))
    mes = int(request.form.get("mes", 9))

    # Exemplo de validação de ano/mês no servidor:
    if not (1900 <= ano <= 2100) or not (1 <= mes <= 12):
        flash("Ano ou mês inválido. Por favor, insira valores válidos (ex: Ano 1900-2100, Mês 1-12).", "error")
        return render_template("calendario.html", resultado=None, ano=ano, mes=mes)


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
        except ValueError: # Captura erro se o valor não for um número válido
            erro = "Valor inválido. Por favor, insira um número."
        except Exception as e:
            erro = f"Erro: {e}"

    return render_template("conversor.html", resultado=resultado, erro=erro, valor=valor, de=de, para=para)


@app.route("/media", methods=["GET", "POST"])
def media_page():
    resultado = None
    if request.method == "POST":
        try:
            nota1 = float(request.form.get("nota1", 0))
            nota2 = float(request.form.get("nota2", 0))
            nota3 = float(request.form.get("nota3", 0))
            resultado = media_escolar.calcular_media([nota1, nota2, nota3])
        except ValueError:
            flash("Notas inválidas. Por favor, insira números válidos para as notas.", "error")
    return render_template("media_escolar.html", resultado=resultado)

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
            flash("Valor inválido. Por favor, insira um número para a temperatura.", "error")
    return render_template("conversor_temperatura.html", resultado=resultado)

@app.route("/senhas", methods=["GET", "POST"])
def senhas_page():
    senha = None
    if request.method == "POST":
        try:
            tamanho = int(request.form.get("tamanho", 12))
            if not (4 <= tamanho <= 32): # Exemplo de limite de tamanho
                flash("Tamanho da senha inválido. Deve ser entre 4 e 32 caracteres.", "error")
            else:
                senha = senhas.gerar_senha(tamanho)
        except ValueError:
            flash("Tamanho inválido. Por favor, insira um número inteiro.", "error")
    return render_template("senhas.html", senha=senha)

@app.route("/sorteio", methods=["GET", "POST"])
def sorteio_page():
    resultado = None
    if request.method == "POST":
        nomes = request.form.get("nomes", "")
        if not nomes.strip():
            flash("Por favor, insira nomes para o sorteio.", "error")
        else:
            resultado = sorteio.sortear(nomes)
    return render_template("sorteio.html", resultado=resultado)

@app.route("/texto", methods=["GET", "POST"])
def texto_page():
    resultado = None
    if request.method == "POST":
        texto = request.form.get("texto", "")
        resultado = texto_stats.analisar_texto(texto)
    return render_template("texto_stats.html", resultado=resultado)

@app.route("/imc", methods=["GET", "POST"])
def imc_page():
    resultado = None
    if request.method == "POST":
        try:
            peso = float(request.form.get("peso", 0))
            altura = float(request.form.get("altura", 1))
            if altura <= 0: # Prevenir divisão por zero
                 flash("Altura deve ser maior que zero.", "error")
            else:
                resultado = imc.calcular_imc(peso, altura)
        except ValueError:
            flash("Valores inválidos. Por favor, insira números para peso e altura.", "error")
    return render_template("imc.html", resultado=resultado)

# =======================================================
# Rota do Editor de Imagens com validação aprimorada
# =======================================================
@app.route("/editor", methods=["GET", "POST"])
def editor_page():
    arquivo = None
    # Removi a variável 'erro' aqui e usarei 'flash' para mensagens de erro/sucesso
    if request.method == "POST":
        if "imagem" not in request.files:
            flash("Nenhum arquivo de imagem foi enviado.", "error")
        else:
            imagem = request.files["imagem"]
            
            if imagem.filename == "":
                flash("Nenhum arquivo selecionado.", "error")
            elif not allowed_file(imagem.filename):
                flash("Extensão de arquivo não permitida. Por favor, envie arquivos com extensão .png, .jpg, .jpeg ou .gif.", "error")
            else:
                try:
                    # Salva o arquivo temporariamente para permitir a checagem do mimetype pelo PIL
                    caminho_temp = os.path.join(OUTPUTS, secure_filename(imagem.filename))
                    imagem.save(caminho_temp)

                    # Tenta abrir o arquivo com PIL para verificar se é uma imagem válida
                    Image.open(caminho_temp).verify() # .verify() tenta carregar o cabeçalho
                    
                    # Se chegou até aqui, é uma imagem válida e tem extensão permitida
                    filtro = request.form.get("filtro", "bw")
                    arquivo_processado_path = editor_imagem.aplicar_filtro(caminho_temp, filtro, OUTPUTS)
                    arquivo = os.path.basename(arquivo_processado_path)
                    flash("Filtro aplicado com sucesso!", "success")
                    
                    # Opcional: Remover o arquivo temporário original se você não precisar dele
                    # os.remove(caminho_temp)

                except UnidentifiedImageError:
                    # Se o PIL não conseguir identificar como imagem
                    flash("O arquivo enviado não é uma imagem válida ou está corrompido.", "error")
                    if os.path.exists(caminho_temp): # Limpa o arquivo inválido
                        os.remove(caminho_temp)
                except Exception as e:
                    # Outros erros durante o processamento da imagem
                    flash(f"Ocorreu um erro ao processar a imagem: {e}", "error")
                    if os.path.exists(caminho_temp): # Limpa o arquivo se deu erro
                        os.remove(caminho_temp)
    return render_template("editor_imagem.html", arquivo=arquivo)

@app.route("/quiz", methods=["GET", "POST"])
def quiz_page():
    pergunta = quiz.pegar_pergunta()
    resultado = None
    if request.method == "POST":
        resposta = request.form.get("resposta")
        correta = request.form.get("correta")
        if resposta == correta:
            resultado = "✅ Resposta correta!"
        else:
            resultado = f"❌ Resposta errada! O certo era: {correta}"
    return render_template("quiz.html", pergunta=pergunta, resultado=resultado)

@app.route("/orcamento", methods=["GET", "POST"])
def orcamento_page():
    resumo = None
    csv_file = None
    if request.method == "POST":
        receitas = request.form.get("receitas", "")
        despesas = request.form.get("despesas", "")
        resumo = orcamento.resumir(receitas, despesas)
        # gerar csv (opcional)
        caminho_csv = orcamento.gerar_csv(resumo, OUTPUTS)
        csv_file = os.path.basename(caminho_csv)
    return render_template("orcamento.html", resumo=resumo, csv_file=csv_file)

@app.route("/calculadora", methods=["GET", "POST"])
def calculadora_page():
    resultado = None
    erro = None
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

@app.route("/tradutor", methods=["GET", "POST"])
def tradutor_page():
    traducao = None
    erro = None
    if request.method == "POST":
        texto = request.form.get("texto", "")
        target = request.form.get("target", "en")
        traduzido = tradutor.traduzir(texto, source="pt", target=target)
        if traduzido:
            traducao = traduzido
        else:
            erro = "Não foi possível traduzir no momento. Tente novamente mais tarde."
    return render_template("tradutor.html", traducao=traducao, erro=erro)

@app.route("/encurtador", methods=["GET", "POST"])
def encurtador_page():
    short = None
    erro = None
    if request.method == "POST":
        link = request.form.get("link", "")
        short = encurtador.encurtar(link)
        if not short:
            erro = "Falha ao encurtar. Verifique o link e tente novamente."
    return render_template("encurtador.html", short=short, erro=erro)


@app.route("/outputs/<path:filename>")
def arquivos(filename):
    return send_from_directory(OUTPUTS, filename)

if __name__ == "__main__":
    app.run(debug=True)
