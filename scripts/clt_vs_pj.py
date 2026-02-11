# scripts/clt_vs_pj.py

def calcular_clt_vs_pj(salario_bruto, dependentes=0):
    """
    Calcula o salário líquido de CLT vs PJ.
    
    Args:
        salario_bruto: Salário bruto mensal
        dependentes: Número de dependentes (para CLT)
    
    Returns:
        dict com os cálculos de CLT e PJ
    """
    try:
        salario_bruto = float(salario_bruto)
        dependentes = int(dependentes)
        
        if salario_bruto <= 0:
            return None, "Salário deve ser maior que zero."
        
        if dependentes < 0:
            return None, "Número de dependentes inválido."
            
    except (ValueError, TypeError):
        return None, "Valores inválidos."
    
    # ===== CÁLCULO CLT =====
    
    # INSS (2024)
    inss = 0
    if salario_bruto <= 1320.00:
        inss = salario_bruto * 0.075
    elif salario_bruto <= 2571.29:
        inss = 1320.00 * 0.075 + (salario_bruto - 1320.00) * 0.09
    elif salario_bruto <= 3856.94:
        inss = 1320.00 * 0.075 + (2571.29 - 1320.00) * 0.09 + (salario_bruto - 2571.29) * 0.12
    else:
        inss = 1320.00 * 0.075 + (2571.29 - 1320.00) * 0.09 + (3856.94 - 2571.29) * 0.12 + (salario_bruto - 3856.94) * 0.14
    
    # Teto do INSS
    if inss > 908.85:
        inss = 908.85
    
    # Base de cálculo do IRRF
    base_irrf = salario_bruto - inss - (189.59 * dependentes)
    
    # IRRF (2024)
    irrf = 0
    if base_irrf <= 2112.00:
        irrf = 0
    elif base_irrf <= 2826.65:
        irrf = base_irrf * 0.075 - 158.40
    elif base_irrf <= 3751.05:
        irrf = base_irrf * 0.15 - 370.40
    elif base_irrf <= 4664.68:
        irrf = base_irrf * 0.225 - 651.73
    else:
        irrf = base_irrf * 0.275 - 884.96
    
    if irrf < 0:
        irrf = 0
    
    # Vale Transporte (6% opcional)
    vale_transporte = salario_bruto * 0.06
    
    # Vale Refeição (desconto médio de R$ 20/mês)
    vale_refeicao = 20.00
    
    # Salário líquido CLT
    salario_liquido_clt = salario_bruto - inss - irrf - vale_transporte - vale_refeicao
    
    # Benefícios CLT (estimativa)
    ferias = salario_bruto / 12  # 1/12 por mês
    decimo_terceiro = salario_bruto / 12  # 1/12 por mês
    fgts = salario_bruto * 0.08  # 8% por mês
    
    total_beneficios_clt = ferias + decimo_terceiro + fgts
    
    # Total CLT (líquido + benefícios proporcionais)
    total_mensal_clt = salario_liquido_clt + total_beneficios_clt
    
    # ===== CÁLCULO PJ =====
    
    # Simples Nacional - Anexo III (Serviços)
    # Faixa 1: até R$ 180.000/ano = 6%
    impostos_pj = salario_bruto * 0.06
    
    # Pró-labore (retirada mínima para INSS)
    pro_labore = 1320.00  # Salário mínimo
    inss_pj = pro_labore * 0.11  # 11% sobre pró-labore
    
    # Contador (média mensal)
    contador = 200.00
    
    # Salário líquido PJ
    salario_liquido_pj = salario_bruto - impostos_pj - inss_pj - contador
    
    # ===== COMPARAÇÃO =====
    
    diferenca = salario_liquido_pj - total_mensal_clt
    percentual = ((salario_liquido_pj / total_mensal_clt) - 1) * 100 if total_mensal_clt > 0 else 0
    
    resultado = {
        "salario_bruto": round(salario_bruto, 2),
        "clt": {
            "inss": round(inss, 2),
            "irrf": round(irrf, 2),
            "vale_transporte": round(vale_transporte, 2),
            "vale_refeicao": round(vale_refeicao, 2),
            "salario_liquido": round(salario_liquido_clt, 2),
            "ferias_proporcional": round(ferias, 2),
            "decimo_terceiro_proporcional": round(decimo_terceiro, 2),
            "fgts": round(fgts, 2),
            "total_mensal": round(total_mensal_clt, 2)
        },
        "pj": {
            "impostos_simples": round(impostos_pj, 2),
            "inss": round(inss_pj, 2),
            "contador": round(contador, 2),
            "salario_liquido": round(salario_liquido_pj, 2)
        },
        "comparacao": {
            "diferenca": round(diferenca, 2),
            "percentual": round(percentual, 2),
            "melhor": "PJ" if diferenca > 0 else "CLT"
        }
    }
    
    return resultado, None
