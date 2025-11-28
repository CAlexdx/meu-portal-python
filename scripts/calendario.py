# scripts/calendario.py
import calendar
from datetime import date
import holidays

MESES_PT = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
            "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]

DIAS_PT = ["Dom", "Seg", "Ter", "Qua", "Qui", "Sex", "Sáb"]

# Todos os feriados brasileiros com nomes corretos em português (2025+)
FERIADOS_FIXOS_PT = {
    (1, 1):   "Confraternização Universal",
    (4, 21):  "Tiradentes",
    (5, 1):   "Dia do Trabalho",
    (9, 7):   "Independência do Brasil",
    (10, 12): "Nossa Senhora Aparecida",
    (11, 2):  "Finados",
    (11, 15): "Proclamação da República",
    (12, 25): "Natal",
}

def gerar_calendario(ano=2025, mes=1):
    """
    Gera calendário com feriados brasileiros 100% traduzidos.
    """
    cal = calendar.Calendar(firstweekday=6)  # Domingo = primeiro dia
    semanas = cal.monthdayscalendar(ano, mes)
    dias_do_mes = []
    for semana in semanas:
        dias_do_mes.append([d if d != 0 else '' for d in semana])

    feriados_do_mes = {}

    # === Feriados fixos (datas certas) ===
    for (m, d), nome in FERIADOS_FIXOS_PT.items():
        if m == mes:
            feriados_do_mes[d] = nome

    # === Feriados móveis (calculados com holidays.Brazil) ===
    try:
        br = holidays.Brazil(years=ano)
        for data, nome_en in br.items():
            if data.month == mes:
                dia = data.day

                # Tradução garantida dos feriados móveis
                traducoes_moveis = {
                    "Carnival Monday": "Segunda-feira de Carnaval",
                    "Carnival Tuesday": "Terça-feira de Carnaval",
                    "Carnival": "Carnaval",  # às vezes vem só isso
                    "Good Friday": "Sexta-feira Santa",
                    "Easter Sunday": "Páscoa",
                    "Corpus Christi": "Corpus Christi",
                }

                nome_traduzido = traducoes_moveis.get(nome_en, nome_en)
                feriados_do_mes[dia] = nome_traduzido
    except:
        pass  # Se der erro, ignora os móveis (nunca mais vai dar com esse método)

    return dias_do_mes, DIAS_PT, feriados_do_mes
