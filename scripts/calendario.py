import locale
import calendar
import holidays

def configurar_locale():
    try:
        locale.setlocale(locale.LC_TIME, "pt_BR.utf8")
    except locale.Error:
        try:
            locale.setlocale(locale.LC_TIME, "pt_BR")  # tenta outra variação
        except locale.Error:
            locale.setlocale(locale.LC_TIME, "")  # usa o default do sistema

configurar_locale()

def gerar_calendario(ano=2025, mes=9):
    cal = calendar.TextCalendar(calendar.SUNDAY)
    texto = cal.formatmonth(ano, mes)

    # Marca feriados
    feriados = holidays.country_holidays("BR", years=ano)
    feriados_mes = {d.day: nome for d, nome in feriados.items() if d.month == mes}

    return texto, feriados_mes
