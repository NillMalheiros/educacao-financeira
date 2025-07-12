# 📊 Módulo: funcoes_financeiras.py
# Funções auxiliares para o simulador de orçamento e quiz

def simulador_orcamento(receita, despesas):
    """
    Calcula o saldo mensal com base na receita e despesas,
    retornando uma mensagem personalizada sobre a saúde financeira.
    """
    saldo = receita - despesas

    if saldo > 0:
        return f"Parabéns! Você economizou R$ {saldo:.2f} este mês.", "resultado-positivo"
    elif saldo == 0:
        return "Você gastou exatamente o que ganhou. Fique atenta nos próximos meses.", "resultado-neutro"
    else:
        return f"Atenção! Suas despesas superaram sua receita em R$ {abs(saldo):.2f}. 🚨", "resultado-negativo"


def calcular_acertos_quiz(respostas):
    """
    Compara as respostas do usuário com o gabarito oficial
    e retorna a quantidade de acertos.
    """
    gabarito = {
        'p1': 'b',
        'p2': 'c',
        'p3': 'a'
    }

    acertos = sum(
        1 for pergunta, resposta in respostas.items()
        if resposta == gabarito.get(pergunta)
    )

    return acertos