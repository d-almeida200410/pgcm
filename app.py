from flask import Flask, render_template, request, send_file
from flask_sqlalchemy import SQLAlchemy
from io import BytesIO
from datetime import datetime
from fpdf import FPDF

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///contratos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Modelo para armazenar contratos
class Contrato(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome_aluno = db.Column(db.String(100), nullable=False)
    data_nascimento = db.Column(db.Date, nullable=False)
    genero = db.Column(db.String(10), nullable=False)
    idade = db.Column(db.Integer, nullable=False)
    escola = db.Column(db.String(100), nullable=False)
    serie = db.Column(db.String(50), nullable=False)
    endereco = db.Column(db.String(200), nullable=False)
    bairro = db.Column(db.String(100), nullable=False)
    nome_responsavel = db.Column(db.String(100), nullable=False)
    ocupacao = db.Column(db.String(100), nullable=False)
    contato = db.Column(db.String(15), nullable=False)
    dias_aula = db.Column(db.String(100), nullable=False)
    horario_entrada = db.Column(db.Time, nullable=False)
    horario_saida = db.Column(db.Time, nullable=False)
    mensalidade_inicio = db.Column(db.Date, nullable=False)
    mensalidade_fim = db.Column(db.Date, nullable=False)
    data_assinatura = db.Column(db.Date, nullable=False)

# Rota principal
@app.route('/')
def index():
    return render_template('index.html')

# Rota para salvar os dados e gerar PDF
@app.route('/salvar', methods=['POST'])
def salvar():
    # Captura os dados do formulário
    nome_aluno = request.form['nomealuno']
    data_nascimento = request.form['datanasc']
    genero = request.form['genero']
    idade = int(request.form['idade'])
    escola = request.form['escola']
    serie = request.form['serie']
    endereco = request.form['endereco']
    bairro = request.form['bairro']
    nome_responsavel = request.form['nomeresp']
    ocupacao = request.form['ocupacao']
    contato = request.form['contato']
    dias_aula = ', '.join(request.form.getlist('dias'))
    horario_entrada = request.form['hora']
    horario_saida = request.form['hora_final']
    mensalidade_inicio = request.form['mensalidade']
    mensalidade_fim = request.form['data_inicio']
    data_assinatura = request.form['mensalidade']

    # Salva no banco de dados
    contrato = Contrato(
        nome_aluno=nome_aluno,
        data_nascimento=datetime.strptime(data_nascimento, '%Y-%m-%d').date(),
        genero=genero,
        idade=idade,
        escola=escola,
        serie=serie,
        endereco=endereco,
        bairro=bairro,
        nome_responsavel=nome_responsavel,
        ocupacao=ocupacao,
        contato=contato,
        dias_aula=dias_aula,
        horario_entrada=datetime.strptime(horario_entrada, '%H:%M').time(),
        horario_saida=datetime.strptime(horario_saida, '%H:%M').time(),
        mensalidade_inicio=datetime.strptime(mensalidade_inicio, '%Y-%m-%d').date(),
        mensalidade_fim=datetime.strptime(mensalidade_fim, '%Y-%m-%d').date(),
        data_assinatura=datetime.strptime(data_assinatura, '%Y-%m-%d').date()
    )
    db.session.add(contrato)
    db.session.commit()

    # Gera o PDF
    pdf = gerar_pdf(contrato)

    return send_file(BytesIO(pdf.output(dest='S').encode('latin1')), 
                     as_attachment=True, 
                     download_name=f"Contrato_{contrato.nome_aluno}.pdf")

# Função para gerar PDF
def gerar_pdf(contrato):
    pdf = FPDF()
    pdf.add_page()

    # Adicionar Logo
    pdf.image("static/images/Rever E Aprender (1).png", 10, 8, 33)  # Caminho da logo, ajuste o tamanho e posição conforme necessário
    pdf.set_font("Arial",style='B' ,size=16)
    pdf.set_text_color(0, 102, 204)  # Azul
    pdf.cell(0, 10, txt="Contrato de Matrícula", ln=True, align='C')
    pdf.ln(20)

  # Identificação do Aluno - em azul, negrito, e fonte maior
    pdf.set_font("Arial", style='B', size=14)
    pdf.set_text_color(0, 102, 204)
    pdf.cell(0, 10, txt="Identificação do Aluno", ln=True)

    # Conteúdo em preto e fonte normal
    pdf.set_font("Arial", size=12)
    pdf.set_text_color(0, 0, 0)
    pdf.multi_cell(0, 10,
                   f"Nome do Aluno: {contrato.nome_aluno}\n"
                   f"Data de Nascimento: {contrato.data_nascimento}\n"
                   f"Gênero: {contrato.genero}\n"
                   f"Idade: {contrato.idade}\n"
                   f"Escola: {contrato.escola}\n"
                   f"Série: {contrato.serie}\n"
                   f"Endereço: {contrato.endereco}, Bairro: {contrato.bairro}\n")

    # Identificação do Responsável - em azul, negrito, e fonte maior
    pdf.set_font("Arial", style='B', size=14)
    pdf.set_text_color(0, 102, 204)
    pdf.cell(0, 10, txt="Identificação do Responsável", ln=True)

    # Conteúdo em preto e fonte normal
    pdf.set_font("Arial", size=12)
    pdf.set_text_color(0, 0, 0)
    pdf.multi_cell(0, 10,
                   f"Nome do Responsável: {contrato.nome_responsavel}\n"
                   f"Ocupação: {contrato.ocupacao}\n"
                   f"Contato: {contrato.contato}\n")

    # Informações do Reforço - em azul, negrito, e fonte maior
    pdf.set_font("Arial", style='B', size=14)
    pdf.set_text_color(0, 102, 204)
    pdf.cell(0, 10, txt="Informações do Reforço", ln=True)

    # Conteúdo em preto e fonte normal
    pdf.set_font("Arial", size=12)
    pdf.set_text_color(0, 0, 0)
    pdf.multi_cell(0, 10,
                   f"Dias de Aula: {contrato.dias_aula}\n"
                   f"Horário de Aula: {contrato.horario_entrada} às {contrato.horario_saida}\n")

    # Mensalidade e Assinaturas - em azul, negrito, e fonte maior
    pdf.set_font("Arial", style='B', size=14)
    pdf.set_text_color(0, 102, 204)
    pdf.cell(0, 10, txt="Mensalidade e Assinaturas", ln=True)

    # Conteúdo em preto e fonte normal
    pdf.set_font("Arial", size=12)
    pdf.set_text_color(0, 0, 0)
    pdf.multi_cell(0, 10,
                   f"Mensalidade de {contrato.mensalidade_inicio} até {contrato.mensalidade_fim}\n"
                   f"Data de Assinatura: {contrato.data_assinatura}\n"
                   f"Assinatura do Contratante: _________________________\n"
                   f"Assinatura da Contratada: _________________________")
    
     # Observações em vermelho e negrito
    pdf.set_font("Arial", style='B', size=7)
    pdf.set_text_color(255, 0, 0)  # Vermelho
    pdf.multi_cell(0, 10,
                   f"Obs: Atividades interdisciplinares, não se encaixam como reforço escolar! "
                   f"(Caso esse serviço seja solicitado será cobrado valor fora parte).\n"
                   f"Obs: Autorização da imagem permitida para divulgar a imagem do meu filho "
                   f"nas redes sociais do reforço escolar.")
    
    # Cnpj
    pdf.set_font("Arial", style='B', size=9)
    pdf.set_text_color(0, 102, 204)
    pdf.cell(0, 10, txt="CNPJ: 19.848.909/0001-22", ln=True)

    return pdf
if __name__ == "__main__":
    with app.app_context():  # Configurar o contexto da aplicação
        db.create_all()  # Criar as tabelas no banco de dados
    app.run(debug=True)
