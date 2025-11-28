# scripts/calendario.py
import calendar
from datetime import date

MESES_PT = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
            "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]

DIAS_PT = ["Dom", "Seg", "Ter", "Qua", "Qui", "Sex", "Sáb"]

# Feriados fixos com nomes 100% em PT-BR
FERIADOS_FIXOS = {
    1:  {1: "Confraternização Universal"},
    4:  {21: "Tiradentes"},
    5:  {1: "Dia do Trabalho"},
    9:  {7: "Independência do Brasil"},
    10: {12: "Nossa Senhora Aparecida"},
    11: {2: "Finados", 15: "Proclamação da República"},
    12: {25: "Natal"},
}

def calcular_pascoa(ano):
    """
    Calcula a data da Páscoa usando o algoritmo de Gauss (preciso para 1900-2100).
    Retorna (mes, dia)
    """
    a = ano // 100
    b = ano % 100
    c = (3 * (a + 25)) // 4
    d = (3 * (a + 25) + 8) // 4 - b
    e = (8 * (b + 11)) // 25
    f = (5 * a + b - e - d + 308) // 10
    g = (f % 7) * 10
    h = (f + 11) % 30
    m = 3 + (h - g + 90) // 25
    n = (h - g + 19) % 30
    p = (n + 32) % 7
    q = (20 * n + p * 9 + 158) // 5
    dia = q - 7 * ((q // 7) * 2 // 4)
    mes = 3 + q // 26
    return mes, dia

def gerar_feriados_moveis(ano):
    """
    Calcula feriados móveis (Páscoa, Carnaval, Corpus Christi) com nomes em PT-BR.
    """
    feriados_moveis = {}
    
    # Páscoa
    mes_pascoa, dia_pascoa = calcular_pascoa(ano)
    feriados_moveis[(mes_pascoa, dia_pascoa)] = "Páscoa"
    
    # Sexta-feira Santa (2 dias antes da Páscoa)
    mes_sexta, dia_sexta = mes_pascoa, dia_pascoa - 2
    if dia_sexta <= 0:
        mes_sexta -= 1
        if mes_sexta == 0:
            mes_sexta = 12
        # Ajuste simples para março (raramente cruza)
        dias_mes_anterior = calendar.monthrange(ano if mes_sexta != 12 else ano-1, mes_sexta)[1]
        dia_sexta = dias_mes_anterior + dia_sexta
    feriados_moveis[(mes_sexta, dia_sexta)] = "Sexta-feira Santa"
    
    # Carnaval (47 dias antes da Páscoa: Quarta-feira de Cinzas -1 = Terça; -2 = Segunda)
    dias_carnaval = 47
    mes_carnaval, dia_carnaval = mes_pascoa, dia_pascoa - dias_carnaval
    while dia_carnaval <= 0:
        mes_carnaval -= 1
        if mes_carnaval == 0:
            mes_carnaval = 12
            ano_anterior = ano - 1
        else:
            ano_anterior = ano
        dias_mes = calendar.monthrange(ano_anterior, mes_carnaval)[1]
        dia_carnaval += dias_mes
    
    # Segunda e Terça de Carnaval
    feriados_moveis[(mes_carnaval, dia_carnaval)] = "Segunda-feira de Carnaval"
    feriados_moveis[(mes_carnaval, dia_carnaval + 1)] = "Terça-feira de Carnaval"
    
    # Corpus Christi (60 dias após Páscoa)
    mes_corpus, dia_corpus = mes_pascoa, dia_pascoa + 60
    while dia_corpus > calendar.monthrange(ano, mes_corpus)[1]:
        dia_corpus -= calendar.monthrange(ano, mes_corpus)[1]
        mes_corpus += 1
        if mes_corpus > 12:
            mes_corpus = 1
            # Não cruza ano pra Corpus
    feriados_moveis[(mes_corpus, dia_corpus)] = "Corpus Christi"
    
    return feriados_moveis

def gerar_calendario(ano=2025, mes=9):
    """
    Gera calendário com TODOS os feriados brasileiros em PT-BR puro.
    Sem dependência de bibliotecas externas pra tradução!
    """
    cal = calendar.Calendar(firstweekday=6)  # Domingo primeiro
    semanas = cal.monthdayscalendar(ano, mes)
    dias_do_mes = []
    for semana in semanas:
        dias_do_mes.append([d if d != 0 else '' for d in semana])

    feriados_do_mes = {}

    # Feriados fixos
    if mes in FERIADOS_FIXOS:
        feriados_do_mes.update(FERIADOS_FIXOS[mes])

    # Feriados móveis
    feriados_moveis = gerar_feriados_moveis(ano)
    for (m, d), nome in feriados_moveis.items():
        if m == mes:
            feriados_do_mes[d] = nome

    return dias_do_mes, DIAS_PT, feriados_do_mes
