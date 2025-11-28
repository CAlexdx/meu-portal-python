# scripts/calendario.py
import calendar
import holidays
MESES_PT = [ "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro" ]
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
    dias_do_mes = []
    for semana in semanas:
        dias_do_mes.append([d if d != 0 else '' for d in semana])

    feriados = {}
    try:
        # Tenta obter os feriados com localidade. Se não funcionar,
        # retornará em inglês.
        br_holidays = holidays.Brazil(years=ano)

        # Mapeamento para traduzir feriados que podem vir em inglês
        traducao_feriados = {
            "New Year's Day": "Confraternização Universal",
            "Carnival": "Carnaval",
            "Good Friday": "Sexta-feira Santa",
            "Tiradentes' Day": "Tiradentes",
            "Labour Day": "Dia do Trabalho",
            "Corpus Christi": "Corpus Christi",
            "Independence Day": "Independência do Brasil",
            "Our Lady of Aparecida": "Nossa Senhora Aparecida",
            "All Souls' Day": "Finados",
            "Republic's Day": "Proclamação da República",
            "Christmas Day": "Natal",
        }

        for dia, nome in br_holidays.items():
            if dia.month == mes:
                nome_traduzido = traducao_feriados.get(nome, nome)
                feriados[dia.day] = nome_traduzido
    except Exception:
        feriados = {}
    
    return dias_do_mes, DIAS_PT, feriados
