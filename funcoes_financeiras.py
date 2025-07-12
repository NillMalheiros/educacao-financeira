def simulador_orcamento(receita, despesas):
    """Calcula o saldo do orçamento e retorna uma mensagem e uma classe CSS."""
    saldo = receita - despesas
    if saldo > 0:
        resultado = f"Seu saldo está positivo em R$ {saldo:.2f}! Ótimo trabalho! 👏"
        classe = "resultado-positivo"
    elif saldo < 0:
        resultado = f"Seu saldo está negativo em R$ {abs(saldo):.2f}. Vamos ajustar! 💪"
        classe = "resultado-negativo"
    else:
        resultado = "Seu orçamento está equilibrado. Cuidado para não negativar!"
        classe = "resultado-neutro"
    return resultado, classe

def calcular_acertos_quiz(respostas):
    """Calcula o número de respostas corretas no quiz."""
    acertos = 0
    gabarito = {
        'p1': 'c',  # Exemplo: resposta correta da pergunta 1 é 'c'
        'p2': 'a',  # Exemplo: resposta correta da pergunta 2 é 'a'
        'p3': 'b'   # Exemplo: resposta correta da pergunta 3 é 'b'
    }
    # Adapte o gabarito acima para as respostas corretas do seu quiz!

    for pergunta, resposta_correta in gabarito.items():
        if respostas.get(pergunta) == resposta_correta:
            acertos += 1
    return acertos
