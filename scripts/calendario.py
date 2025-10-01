# scripts/calendario.py
import calendar
import holidays

MESES_PT = [
    "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
    "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"
]

DIAS_PT = ["Dom", "Seg", "Ter", "Qua", "Qui", "Sex", "Sáb"]

def gerar_calendario(ano=2025, mes=9):
    """
    Gera um calendário de um mês específico com feriados.

    Args:
        ano (int): Ano desejado.
        mes (int): Mês desejado.

    Returns:
        tuple: (texto_formatado, dicionário de feriados)
    """
    cal = calendar.Calendar(firstweekday=6)  # começa no domingo
    semanas = cal.monthdayscalendar(ano, mes)

    texto = f"{MESES_PT[mes-1]} {ano}\n"
    texto += " ".join(DIAS_PT) + "\n"
    for semana in semanas:
        linha = " ".join(f"{d:2}" if d != 0 else "  " for d in semana)
        texto += linha + "\n"

    feriados = {}
    try:
        br_holidays = holidays.Brazil(years=ano)
        for dia, nome in br_holidays.items():
            if dia.month == mes:
                feriados[dia.day] = nome
    except Exception:
        feriados = {}

    return texto, feriados
