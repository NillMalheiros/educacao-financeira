# --------------------------------------------------------------------------
# app.py - Versão Final com Banco de Dados para Deploy no Render
# --------------------------------------------------------------------------

import os
from flask import Flask, render_template, request, redirect, url_for
from markupsafe import escape
from flask_sqlalchemy import SQLAlchemy

# --- 1. Configuração da Aplicação e do Banco de Dados ---

app = Flask(__name__)

# Lê a URL do banco de dados e a chave secreta das variáveis de ambiente do Render.
# Isso torna o código seguro e portável.
DATABASE_URL = os.environ.get('DATABASE_URL')
SECRET_KEY = os.environ.get('SECRET_KEY', 'chave-secreta-para-teste-local')

# Substitui 'postgres://' por 'postgresql://' se necessário (Render pode usar o primeiro)
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Opcional: desativa avisos
app.config['SECRET_KEY'] = SECRET_KEY

# Inicializa a extensão SQLAlchemy com a nossa aplicação
db = SQLAlchemy(app)

# --- 2. Modelo da Tabela do Banco de Dados ---

# Define a estrutura (schema) da nossa tabela de feedbacks.
# Cada instância desta classe representará uma linha na tabela.
class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Chave primária única
    nome = db.Column(db.String(100), nullable=False)
    tipo = db.Column(db.String(50), nullable=False)
    mensagem = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'<Feedback de {self.nome}>'

# --- 3. Funções de Lógica (se não estiverem em arquivo separado) ---

# Para manter o código autocontido, as funções financeiras podem estar aqui
# ou no arquivo 'funcoes_financeiras.py'
try:
    from funcoes_financeiras import simulador_orcamento, calcular_acertos_quiz
except ImportError:
    print("AVISO: 'funcoes_financeiras.py' não encontrado. Usando funções de exemplo.")
    def simulador_orcamento(r, d): return ("Função de simulação não encontrada", "resultado-negativo")
    def calcular_acertos_quiz(respostas): return 0

# --- 4. Rotas da Aplicação ---

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

# ROTA DE FEEDBACK MODIFICADA PARA USAR O BANCO DE DADOS
@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if request.method == 'POST':
        try:
            nome = escape(request.form.get('nome', 'Anônimo').strip()) or "Anônimo"
            tipo = escape(request.form.get('tipo', 'Outro'))
            mensagem = escape(request.form.get('mensagem', '').strip())

            if not mensagem:
                return render_template('feedback.html', resposta="Por favor, escreva uma mensagem válida.")

            # Cria um objeto Feedback com os dados do formulário
            novo_feedback = Feedback(nome=nome, tipo=tipo, mensagem=mensagem)

            # Adiciona o novo objeto à sessão do banco de dados e salva (commit)
            db.session.add(novo_feedback)
            db.session.commit()

            print(f"✅ Feedback de '{nome}' salvo no banco de dados.")
            # Redireciona o usuário para a página do painel após o envio
            return redirect(url_for('painel'))

        except Exception as e:
            db.session.rollback()  # Desfaz a operação em caso de erro
            print(f"Erro ao salvar feedback no banco de dados: {e}")
            return render_template('feedback.html', resposta="Ocorreu um erro ao salvar seu feedback.")

    # Se o método for GET, apenas exibe a página do formulário
    return render_template('feedback.html')

# ROTA DO PAINEL MODIFICADA PARA LER DO BANCO DE DADOS
@app.route('/painel')
def painel():
    try:
        # Busca todos os registros da tabela Feedback, ordenando pelos mais recentes
        todos_feedbacks = Feedback.query.order_by(Feedback.id.desc()).all()
        return render_template('painel.html', feedbacks=todos_feedbacks)
    except Exception as e:
        print(f"Erro ao buscar feedbacks do banco de dados: {e}")
        return "<h1>Erro ao carregar os feedbacks. Tente novamente mais tarde.</h1>"

# --- 5. Inicialização e Criação do Banco de Dados ---

# Este bloco é executado antes da primeira requisição ao servidor.
# Ele garante que as tabelas definidas em nossos modelos sejam criadas no banco de dados.
@app.before_request
def create_tables():
    # A função `create_all` é segura e só cria tabelas que ainda não existem.
    db.create_all()

# Bloco para rodar o servidor localmente para testes
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    # 'debug=True' é útil para desenvolvimento, mas o Render o ignora em produção.
    app.run(host='0.0.0.0', port=port, debug=True)
