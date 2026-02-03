# scripts/media_escolar.py

def calcular_media(materias_dict):
    """
    Calcula a média de cada matéria e a média geral.
    
    Args:
        materias_dict (dict): Estrutura de matérias e avaliações, exemplo:
            {
                "Matemática": {"Prova": 7.5, "Trabalho": 8.0},
                "Português": {"Prova": 6.0, "Redação": 7.0}
            }

    Returns:
        dict: {
            "materias": {
                "Matemática": {"avaliacoes": {...}, "media": 7.75},
                "Português": {"avaliacoes": {...}, "media": 6.5}
            },
            "geral": 7.12
        }
    """
    resultado = {}
    todas_notas = []

    for materia, avaliacoes in materias_dict.items():
        notas = []
        for tipo, nota in avaliacoes.items():
            try:
                n = float(nota)
                if 0 <= n <= 10:
                    notas.append(n)
            except ValueError:
                continue
        if notas:
            media = round(sum(notas) / len(notas), 2)
            resultado[materia] = {"avaliacoes": avaliacoes, "media": media}
            todas_notas.extend(notas)

    media_geral = round(sum(todas_notas) / len(todas_notas), 2) if todas_notas else 0
    return {"materias": resultado, "geral": media_geral}
