import random

perguntas = [
    {
        "pergunta": "Qual função imprime algo no Python?",
        "opcoes": ["echo()", "print()", "log()", "say()"],
        "resposta": "print()"
    },
    {
        "pergunta": "Qual símbolo é usado para comentários?",
        "opcoes": ["//", "#", "--", "/* */"],
        "resposta": "#"
    },
    {
        "pergunta": "Qual tipo representa números decimais?",
        "opcoes": ["int", "float", "str", "bool"],
        "resposta": "float"
    },
    {
        "pergunta": "Qual biblioteca é usada para ciência de dados?",
        "opcoes": ["numpy", "requests", "flask", "random"],
        "resposta": "numpy"
    }
]

def pegar_pergunta():
    return random.choice(perguntas)
