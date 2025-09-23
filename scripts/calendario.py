import calendar
import locale
import holidays

locale.setlocale(locale.LC_TIME, "pt_BR.utf8")

def gerar_calendario(ano=2025, mes=9):
    cal = calendar.TextCalendar(firstweekday=0)
    calendario_str = cal.formatmonth(ano, mes)

    # feriados brasileiros
    feriados = holidays.Brazil(years=ano)

    # adicionar nota de feriados
    feriados_mes = {d.day: nome for d, nome in feriados.items() if d.month == mes}

    return calendario_str, feriados_mes
