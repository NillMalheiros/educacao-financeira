# --------------------------------------------------------------------------
# app.py - Versão Final para Deploy
# --------------------------------------------------------------------------

import os
from flask import Flask, render_template, request
from markupsafe import escape

# Tenta importar as funções. Se o arquivo não existir, usa funções placeholder.
try:
    from funcoes_financeiras import simulador_orcamento, calcular_acertos_quiz
except ImportError:
    print("AVISO: Arquivo 'funcoes_financeiras.py' não encontrado. Usando funções de exemplo.")
    def simulador_orcamento(r, d): return ("Função de simulação não encontrada", "resultado-negativo")
    def calcular_acertos_quiz(respostas): return 0

app = Flask(__name__)

# Configuração de segurança essencial para produção.
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'uma-chave-secreta-padrao-para-desenvolvimento')

# AVISO: Esta lista em memória será reiniciada a cada deploy no Render.
feedbacks_recebidos = []

# --- Rotas de Navegação ---
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

# --- Rotas de Funcionalidades ---
@app.route('/simulador', methods=['GET', 'POST'])
def simulador():
    resultado, classe = None, "resultado-neutro"
    if request.method == 'POST':
        try:
            receita = float(request.form.get('receita', '0'))
            despesas = float(request.form.get('despesas', '0'))
            resultado, classe = simulador_orcamento(receita, despesas)
        except ValueError:
            resultado, classe = "Dados inválidos. Insira apenas números.", "resultado-negativo"
        except Exception as e:
            print(f"Erro no simulador: {e}")
            resultado, classe = "Ocorreu um erro inesperado.", "resultado-negativo"
    return render_template('simulador.html', resultado=resultado, classe=classe)

@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    acertos, mensagem, classe = None, "", ""
    if request.method == 'POST':
        try:
            respostas = {f'p{i}': request.form.get(f'p{i}', '').strip().lower() for i in range(1, 4)}
            acertos = calcular_acertos_quiz(respostas)
            if acertos == 3:
                mensagem, classe = "Show! Você domina o assunto! 🎉", "resultado-positivo"
            elif acertos == 2:
                mensagem, classe = "Muito bem! Falta pouco pra dominar 💪", "resultado-neutro"
            else:
                mensagem, classe = "Sem stress! Vamos melhorar juntas! 🌱", "resultado-negativo"
        except Exception as e:
            print(f"Erro no quiz: {e}")
            mensagem, classe = "Ocorreu um erro ao processar o quiz.", "resultado-negativo"
    return render_template('quiz.html', acertos=acertos, mensagem=mensagem, classe=classe)

@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    resposta = None
    if request.method == 'POST':
        try:
            nome = escape(request.form.get('nome', 'Anônimo').strip()) or "Anônimo"
            tipo = escape(request.form.get('tipo', 'Outro'))
            mensagem = escape(request.form.get('mensagem', '').strip())
            if not mensagem:
                resposta = "Por favor, escreva uma mensagem válida."
            else:
                feedbacks_recebidos.append({'nome': nome, 'tipo': tipo, 'mensagem': mensagem})
                resposta = "Obrigada pelo seu feedback! 💌"
                print(f"✅ Feedback recebido: {nome}")
        except Exception as e:
            print(f"Erro no feedback: {e}")
            resposta = "Ocorreu um erro ao salvar o feedback."
    return render_template('feedback.html', resposta=resposta)

@app.route('/painel')
def painel():
    return render_template('painel.html', feedbacks=feedbacks_recebidos)

# --- Bloco de Execução (Apenas para desenvolvimento local) ---
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
