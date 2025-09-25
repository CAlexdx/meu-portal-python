import calendar
import holidays

MESES_PT = [
    "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
    "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"
]

DIAS_PT = ["Do", "Se", "Te", "Qa", "Qi", "Se", "Sa"]

def gerar_calendario(ano=2025, mes=9):
    cal = calendar.Calendar(firstweekday=6)
    semanas = cal.monthdayscalendar(ano, mes)

    # Monta texto
    texto = f"{MESES_PT[mes-1]} {ano}\n"
    texto += " ".join(DIAS_PT) + "\n"
    for semana in semanas:
        linha = " ".join(f"{d:2}" if d != 0 else "  " for d in semana)
        texto += linha + "\n"

    # Feriados
    feriados = {}
    try:
        br_holidays = holidays.Brazil(years=ano)
        for dia, nome in br_holidays.items():
            if dia.month == mes:
                feriados[dia.day] = nome
    except Exception:
        feriados = {}

    return texto, feriados
