def calcular_media(notas):
    media = sum(notas) / len(notas)
    if media >= 7:
        return f"Média: {media:.2f} ✅ Aprovado"
    elif media >= 5:
        return f"Média: {media:.2f} ⚠️ Recuperação"
    else:
        return f"Média: {media:.2f} ❌ Reprovado"
