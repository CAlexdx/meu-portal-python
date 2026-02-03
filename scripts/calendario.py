# scripts/calendario.py
import calendar
import holidays

MESES_PT = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
            "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]
DIAS_PT = ["Dom", "Seg", "Ter", "Qua", "Qui", "Sex", "Sáb"]

def gerar_calendario(ano=2025, mes=1):
    # Gera o calendário mensal
    cal = calendar.Calendar(firstweekday=6)  # Domingo como primeiro dia
    semanas = cal.monthdayscalendar(ano, mes)
    dias_do_mes = []
    for semana in semanas:
        dias_do_mes.append([d if d != 0 else '' for d in semana])

    feriados = {}

    try:
        br = holidays.Brazil(years=ano)

        # Dicionário COMPLETO com todos os nomes que a biblioteca pode retornar
        traducao = {
            # Fixos
            "New Year's Day": "Confraternização Universal",
            "Tiradentes' Day": "Tiradentes",
            "Labour Day": "Dia do Trabalho",
            "Independence Day": "Independência do Brasil",
            "Our Lady of Aparecida": "Nossa Senhora Aparecida",
            "All Souls' Day": "Finados",
            "Republic Proclamation Day": "Proclamação da República",
            "Republic's Day": "Proclamação da República",
            "Christmas Day": "Natal",

            # Móveis (os nomes mudam dependendo da versão da biblioteca)
            "Carnival": "Terça-feira de Carnaval",
            "Carnival Monday": "Segunda-feira de Carnaval",
            "Carnival Tuesday": "Terça-feira de Carnaval",
            "Good Friday": "Sexta-feira Santa",
            "Easter Sunday": "Páscoa",
            "Corpus Christi": "Corpus Christi",

            # Alguns anos retornam com acento ou variação
            "Carnaval": "Terça-feira de Carnaval",
            "Sexta-feira Santa": "Sexta-feira Santa",
            "Corpus Christi Day": "Corpus Christi",
        }

        for data, nome_en in br.items():
            if data.month == mes:
                nome_correto = traducao.get(nome_en, nome_en)  # Traduz se existir, senão deixa o original
                feriados[data.day] = nome_correto

                # Garante que Segunda e Terça de Carnaval apareçam mesmo se só vier "Carnival"
                if "Carnival" in nome_en and data.weekday() == 0:  # Segunda-feira
                    feriados[data.day] = "Segunda-feira de Carnaval"
                if "Carnival" in nome_en and data.weekday() == 1:  # Terça-feira
                    feriados[data.day] = "Terça-feira de Carnaval"

    except Exception as e:
        print(f"Erro ao carregar feriados: {e}")
        feriados = {}

    return dias_do_mes, DIAS_PT, feriados
