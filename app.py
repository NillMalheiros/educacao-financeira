from flask import Flask, render_template, request
from funcoes_financeiras import simulador_orcamento, calcular_acertos_quiz
import os

app = Flask(__name__)

# ------------------------
# 🌐 Rotas de Navegação
# ------------------------

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/sobre')
def sobre():
    return render_template('sobre.html')

@app.route('/blog')
def blog():
    return render_template('blog.html')

@app.route('/avaliacao')
def avaliacao():
    return render_template('avaliacao.html')

# ------------------------
# 💰 Simulador de Orçamento
# ------------------------

@app.route('/simulador', methods=['GET', 'POST'])
def simulador():
    resultado = None
classe = "resultado-neutro"
if request.method == 'POST':
    try:
        receita = float(request.form.get('receita') or 0)
        despesas = float(request.form.get('despesas') or 0)
        resultado, classe = simulador_orcamento(receita, despesas)
    except ValueError:
        resultado = "Dados inválidos. Por favor, insira números válidos."
        classe = "resultado-negativo"
    except Exception as e:
        resultado = f"Ocorreu um erro inesperado: {str(e)}"
        classe = "resultado-negativo"
            else:
                resultado = "Você gastou exatamente o que ganhou. Fique atenta nos próximos meses."

        except ValueError:
            resultado = "Dados inválidos. Por favor, insira números válidos."
            classe = "resultado-negativo"
        except Exception as e:
            resultado = f"Ocorreu um erro inesperado: {str(e)}"
            classe = "resultado-negativo"

    return render_template('simulador.html', resultado=resultado, classe=classe)

# ------------------------
# 🧠 Quiz Financeiro
# ------------------------

@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    acertos = None
    mensagem = ""
    classe = ""

    if request.method == 'POST':
        try:
            respostas = {
                'p1': (request.form.get('p1') or '').strip().lower(),
                'p2': (request.form.get('p2') or '').strip().lower(),
                'p3': (request.form.get('p3') or '').strip().lower(),
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

# ------------------------
# 📬 Feedback dos Usuários
# ------------------------

@# ------------------------
# 📬 Feedback dos Usuários
# ------------------------

@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    resposta = None

    if request.method == 'POST':
        try:
            nome = request.form.get('nome', 'Anônimo')
            tipo = request.form.get('tipo')
            mensagem = request.form.get('mensagem')

            if not mensagem or not mensagem.strip():
                resposta = "Por favor, escreva uma mensagem válida."
            else:
                resposta = "Obrigada pelo seu feedback! 💌"

        except Exception as e:
            resposta = f"Ocorreu um erro no envio: {str(e)}"

    return render_template('feedback.html', resposta=resposta)

# ------------------------
# 🚀 Inicialização do App
# ------------------------

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)