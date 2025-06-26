def simulador_orcamento(receita, despesas):
    saldo = receita - despesas
    if saldo > 0:
        return f"Parabéns! Você economizou R$ {saldo:.2f} este mês."
    elif saldo == 0:
        return "Atenção! Você gastou exatamente o que ganhou."
    else:
        return f"Cuidado! Você gastou R$ {-saldo:.2f} a mais do que ganhou."

def calcular_acertos_quiz(respostas):
    gabarito = {
        'p1': 'b',
        'p2': 'c',
        'p3': 'a'
    }
    acertos = 0
    for pergunta, resposta in respostas.items():
        if resposta == gabarito.get(pergunta):
            acertos += 1
    return acertos