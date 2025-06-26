from flask import Flask, render_template, request
from funcoes_financeiras import simulador_orcamento, calcular_acertos_quiz

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/simulador', methods=['GET', 'POST'])
def simulador():
    resultado = None
    classe = "resultado-neutro"
    if request.method == 'POST':
        try:
            receita = float(request.form.get('receita', 0))
            despesas = float(request.form.get('despesas', 0))
            saldo = receita - despesas

            if saldo > 0:
                resultado = f"Parabéns! Você economizou R$ {saldo:.2f} este mês. 💚"
                classe = "resultado-positivo"
            elif saldo < 0:
                resultado = f"Atenção! Suas despesas superaram sua receita em R$ {abs(saldo):.2f}. 🚨"
                classe = "resultado-negativo"
            else:
                resultado = "Você gastou exatamente o que ganhou. Fique atenta nos próximos meses."
                classe = "resultado-neutro"
        except ValueError:
            resultado = "Dados inválidos. Por favor, insira números válidos."
        except Exception as e:
            resultado = f"Ocorreu um erro: {str(e)}"
    return render_template('simulador.html', resultado=resultado, classe=classe)

@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    acertos = None
    mensagem = ""
    classe = ""
    if request.method == 'POST':
        try:
            respostas = {
                'p1': request.form.get('p1', '').strip().lower(),
                'p2': request.form.get('p2', '').strip().lower(),
                'p3': request.form.get('p3', '').strip().lower(),
            }
            acertos = calcular_acertos_quiz(respostas)

            if acertos == 3:
                mensagem = "Show! Você domina o assunto! 🎉"
                classe = "resultado-positivo"
            elif acertos == 2:
                mensagem = "Muito bem! Falta pouco pra dominar 💪"
                classe = "resultado-neutro"
            else:
                mensagem = "Sem stress! Vamos melhorar juntas! 🌱"
                classe = "resultado-negativo"

        except Exception as e:
            mensagem = f"Erro ao calcular resultado: {str(e)}"
            classe = "resultado-negativo"

    return render_template('quiz.html', acertos=acertos, mensagem=mensagem, classe=classe)

@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    resposta = None
    if request.method == 'POST':
        nome = request.form.get('nome', 'Anônimo')
        tipo = request.form.get('tipo')
        mensagem = request.form.get('mensagem')

        try:
            with open('feedback.csv', 'a', encoding='utf-8') as arquivo:
                arquivo.write(f"{nome},{tipo},\"{mensagem.strip()}\"\n")
            resposta = "Obrigada pelo seu feedback! 💌"
        except Exception as e:
            resposta = f"Ocorreu um erro ao salvar seu feedback: {str(e)}"

    return render_template('feedback.html', resposta=resposta)

if __name__ == '__main__':
    app.run(debug=True, port=5001)