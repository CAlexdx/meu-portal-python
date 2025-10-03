import calendar
import holidays

MESES_PT = [
    "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
    "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"
]

DIAS_PT = ["Dom", "Seg", "Ter", "Qua", "Qui", "Sex", "Sáb"]

def gerar_calendario(ano=2025, mes=9):
    """
    Gera uma estrutura de calendário para exibição em HTML, além dos feriados.

    Args:
        ano (int): Ano desejado.
        mes (int): Mês desejado.

    Returns:
        tuple: (dias_do_mes_list, lista_dias_semana_list, dicionário de feriados)
    """
    cal = calendar.Calendar(firstweekday=6)  # começa no domingo
    semanas = cal.monthdayscalendar(ano, mes)

    # Convertendo para uma lista de listas mais fácil de iterar no Jinja
    dias_do_mes = []
    for semana in semanas:
        dias_do_mes.append([d if d != 0 else '' for d in semana]) # Use '' para dias fora do mês

    feriados = {}
    try:
        br_holidays = holidays.Brazil(years=ano, locale='pt_BR')
        for dia, nome in br_holidays.items():
            if dia.month == mes:
                feriados[dia.day] = nome
    except Exception:
        feriados = {}

    return dias_do_mes, DIAS_PT, feriados # Retorna os dias do mês, os nomes dos dias da semana e os feriados
