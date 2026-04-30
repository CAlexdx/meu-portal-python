from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import os
from uuid import uuid4

def gerar_curriculo(dados, pasta_saida):
    nome_arquivo = f"curriculo_{uuid4().hex}.pdf"
    caminho = os.path.join(pasta_saida, nome_arquivo)

    c = canvas.Canvas(caminho, pagesize=A4)
    largura, altura = A4

    y = altura - 50

    def escrever(texto, tamanho=12):
        nonlocal y
        c.setFont("Helvetica", tamanho)
        c.drawString(50, y, texto)
        y -= 20

    # Dados principais
    escrever(dados.get("nome", ""), 16)
    escrever(dados.get("email", ""))
    escrever(dados.get("telefone", ""))

    y -= 10
    escrever("Resumo:", 14)
    escrever(dados.get("resumo", ""))

    y -= 10
    escrever("Experiência:", 14)
    escrever(dados.get("experiencia", ""))

    y -= 10
    escrever("Educação:", 14)
    escrever(dados.get("educacao", ""))

    y -= 10
    escrever("Habilidades:", 14)
    escrever(dados.get("habilidades", ""))

    c.save()
    return nome_arquivo