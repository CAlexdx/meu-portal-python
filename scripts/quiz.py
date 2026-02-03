# scripts/quiz.py
import random

# Lista de perguntas
perguntas = [
    {"id": 1, "pergunta": "Qual função imprime algo no Python?", "opcoes": ["echo()", "print()", "log()", "say()"], "resposta": "print()"},
    {"id": 2, "pergunta": "Qual símbolo é usado para comentários?", "opcoes": ["//", "#", "--", "/* */"], "resposta": "#"},
    {"id": 3, "pergunta": "Qual tipo representa números decimais?", "opcoes": ["int", "float", "str", "bool"], "resposta": "float"},
    {"id": 4, "pergunta": "Qual biblioteca é usada para ciência de dados?", "opcoes": ["numpy", "requests", "flask", "random"], "resposta": "numpy"},
    {"id": 5, "pergunta": "Qual estrutura de dados armazena itens em ordem?", "opcoes": ["set", "dict", "tuple", "list"], "resposta": "list"},
    {"id": 6, "pergunta": "Qual operador é usado para potenciação?", "opcoes": ["^", "**", "*", "//"], "resposta": "**"}
]

def inicializar_quiz(session):
    """Inicia um quiz armazenando progresso na sessão Flask."""
    session['perguntas_restantes_ids'] = [p['id'] for p in perguntas]
    session['pontuacao'] = 0
    session['total_perguntas_respondidas'] = 0

def pegar_proxima_pergunta(session):
    """Retorna uma pergunta aleatória não respondida ainda."""
    if not session.get('perguntas_restantes_ids'):
        return None
    pergunta_id_atual = random.choice(session['perguntas_restantes_ids'])
    return next((p for p in perguntas if p['id'] == pergunta_id_atual), None)

def get_todas_perguntas():
    """Retorna todas as perguntas disponíveis."""
    return perguntas
