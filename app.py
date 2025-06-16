from flask import Flask, render_template, request, redirect, url_for, make_response, send_file
import sqlite3
from datetime import datetime
from fpdf import FPDF
import os
import tempfile
# Importar a API REST
from api import init_api

app = Flask(__name__)
# Inicializar a API REST
init_api(app)

def get_db_connection():
    conn = sqlite3.connect('banco.db')
    conn.row_factory = sqlite3.Row
    return conn

# Criação das tabelas (clientes, ordens, peças)
def criar_tabelas():
    conn = get_db_connection()    
    
    # Verificar se é necessário atualizar a tabela de clientes
    try:
        # Verifica se as colunas email e endereco existem
        conn.execute('SELECT email, endereco FROM clientes LIMIT 1')
    except sqlite3.OperationalError:
        # Se não existir, cria uma nova tabela com as colunas
        conn.execute('DROP TABLE IF EXISTS clientes')
        conn.execute('''
            CREATE TABLE clientes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                telefone TEXT,
                email TEXT,
                endereco TEXT
            );
        ''')
    else:
        # Se já existir, não faz nada
        pass
        
    # Verificar se é necessário atualizar a tabela de ordens de serviço
    try:
        # Verifica se as colunas veiculo e placa existem
        conn.execute('SELECT veiculo, placa FROM ordens_servico LIMIT 1')
    except sqlite3.OperationalError:        # Se não existir, cria uma nova tabela com as colunas
        conn.execute('DROP TABLE IF EXISTS ordens_servico')
        conn.execute('''
            CREATE TABLE ordens_servico (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cliente_id INTEGER NOT NULL,
                descricao TEXT NOT NULL,
                data TEXT NOT NULL,
                veiculo TEXT,
                placa TEXT,
                FOREIGN KEY (cliente_id) REFERENCES clientes (id)
            );
        ''')
    else:
        # Se já existir, não faz nada
        pass
        
    # Verificar se é necessário atualizar a tabela de peças
    try:
        # Verifica se a coluna valor_instalado existe
        conn.execute('SELECT valor_instalado FROM pecas LIMIT 1')
    except sqlite3.OperationalError:
        # Se a coluna valor_instalado não existir, adiciona-a
        try:
            conn.execute('ALTER TABLE pecas ADD COLUMN valor_instalado REAL')
            print("Coluna valor_instalado adicionada com sucesso à tabela pecas")
        except sqlite3.OperationalError as e:
            # Se houver um erro na alteração, recria a tabela
            print(f"Erro ao adicionar coluna: {e}. Recriando tabela...")
            conn.execute('DROP TABLE IF EXISTS pecas')
            conn.execute('''
                CREATE TABLE pecas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    quantidade INTEGER NOT NULL,
                    valor REAL,
                    valor_instalado REAL
                );
            ''')
            print("Tabela pecas recriada com sucesso!")
    else:
        # Se a coluna valor_instalado já existir, não faz nada
        pass

    conn.commit()
    conn.close()

# Rota principal (exemplo simples - redireciona para clientes)
@app.route('/')
def index():
    return redirect(url_for('clientes'))

# ---------- ROTAS DE CLIENTES ----------
@app.route('/clientes', methods=['GET', 'POST'])
def clientes():
    conn = get_db_connection()
    if request.method == 'POST':
        nome = request.form['nome']
        telefone = request.form['telefone']
        email = request.form.get('email', '')
        endereco = request.form.get('endereco', '')
        conn.execute('INSERT INTO clientes (nome, telefone, email, endereco) VALUES (?, ?, ?, ?)', 
                    (nome, telefone, email, endereco))
        conn.commit()
        return redirect(url_for('clientes'))
    clientes = conn.execute('SELECT * FROM clientes').fetchall()
    conn.close()
    return render_template('clientes.html', clientes=clientes)

@app.route('/adicionar_cliente', methods=['POST'])
def adicionar_cliente():
    conn = get_db_connection()
    nome = request.form['nome']
    telefone = request.form['telefone']
    email = request.form['email']
    endereco = request.form['endereco']
    conn.execute('INSERT INTO clientes (nome, telefone, email, endereco) VALUES (?, ?, ?, ?)', 
                 (nome, telefone, email, endereco))
    conn.commit()
    conn.close()
    return redirect(url_for('clientes'))

@app.route('/editar_cliente/<int:id>', methods=['GET', 'POST'])
def editar_cliente(id):
    conn = get_db_connection()
    if request.method == 'POST':
        nome = request.form['nome']
        telefone = request.form['telefone']
        email = request.form['email']
        endereco = request.form['endereco']
        conn.execute('UPDATE clientes SET nome = ?, telefone = ?, email = ?, endereco = ? WHERE id = ?',
                     (nome, telefone, email, endereco, id))
        conn.commit()
        conn.close()
        return redirect(url_for('clientes'))
    cliente = conn.execute('SELECT * FROM clientes WHERE id = ?', (id,)).fetchone()
    conn.close()
    return render_template('editar_cliente.html', cliente=cliente)

@app.route('/excluir_cliente/<int:id>')
def excluir_cliente(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM clientes WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('clientes'))

# ---------- ROTAS DE ORDENS DE SERVIÇO ----------
@app.route('/ordens_servico', methods=['GET', 'POST'])
def ordens_servico():
    conn = get_db_connection()
    if request.method == 'POST':
        cliente_id = request.form['cliente_id']
        descricao = request.form['descricao']
        data = request.form['data']
        veiculo = request.form.get('veiculo', '')
        placa = request.form.get('placa', '')
        conn.execute('INSERT INTO ordens_servico (cliente_id, descricao, data, veiculo, placa) VALUES (?, ?, ?, ?, ?)',
                     (cliente_id, descricao, data, veiculo, placa))
        conn.commit()
        return redirect(url_for('ordens_servico'))
    
    os_list = conn.execute('''
        SELECT os.id, c.nome AS cliente, os.descricao, os.data, os.cliente_id, os.veiculo, os.placa
        FROM ordens_servico os
        JOIN clientes c ON os.cliente_id = c.id
    ''').fetchall()
    clientes = conn.execute('SELECT * FROM clientes').fetchall()
    conn.close()
    return render_template('os.html', os_list=os_list, clientes=clientes)

@app.route('/adicionar_os', methods=['POST'])
def adicionar_os():
    conn = get_db_connection()
    cliente_id = request.form['cliente_id']
    descricao = request.form['descricao']
    data = request.form['data']
    veiculo = request.form.get('veiculo', '')
    placa = request.form.get('placa', '')
    conn.execute('INSERT INTO ordens_servico (cliente_id, descricao, data, veiculo, placa) VALUES (?, ?, ?, ?, ?)',
                 (cliente_id, descricao, data, veiculo, placa))
    conn.commit()
    conn.close()
    return redirect(url_for('ordens_servico'))

@app.route('/editar_os/<int:id>', methods=['GET', 'POST'])
def editar_os(id):
    conn = get_db_connection()
    if request.method == 'POST':
        cliente_id = request.form['cliente_id']
        descricao = request.form['descricao']
        data = request.form['data']
        veiculo = request.form.get('veiculo', '')
        placa = request.form.get('placa', '')
        conn.execute('UPDATE ordens_servico SET cliente_id = ?, descricao = ?, data = ?, veiculo = ?, placa = ? WHERE id = ?',
                     (cliente_id, descricao, data, veiculo, placa, id))
        conn.commit()
        conn.close()
        return redirect(url_for('ordens_servico'))
    
    ordem = conn.execute('SELECT * FROM ordens_servico WHERE id = ?', (id,)).fetchone()
    clientes = conn.execute('SELECT * FROM clientes').fetchall()
    conn.close()
    return render_template('editar_os.html', ordem=ordem, clientes=clientes)

@app.route('/excluir_os/<int:id>')
def excluir_os(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM ordens_servico WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('ordens_servico'))

@app.route('/gerar_pdf_os/<int:id>')
def gerar_pdf_os(id):
    conn = get_db_connection()
    
    # Buscar dados da ordem de serviço e do cliente
    ordem = conn.execute('SELECT * FROM ordens_servico WHERE id = ?', (id,)).fetchone()
    if not ordem:
        conn.close()
        return "Ordem de serviço não encontrada", 404
        
    cliente = conn.execute('SELECT * FROM clientes WHERE id = ?', (ordem['cliente_id'],)).fetchone()
    conn.close()
    
    # Criar o PDF
    class PDF(FPDF):
        def header(self):
            # Logo
            logo_path = os.path.join(app.root_path, 'static', 'img', 'logo.png')
            if os.path.exists(logo_path):
                self.image(logo_path, 10, 8, 33)
                
            # Informações da empresa
            self.set_font('Arial', 'B', 15)
            self.cell(0, 10, 'Sergio Eduardo Padilha Corazzim', 0, 1, 'C')
            self.set_font('Arial', '', 10)
            self.cell(0, 5, 'Avenida Pedro Botesi, 2352 - Jd Scomparim - Mogi Mirim - SP', 0, 1, 'C')
            self.cell(0, 5, 'WhatsApp: (19) 99676-0164', 0, 1, 'C')
            self.cell(0, 5, 'CNPJ: 08.101.093/0001-52', 0, 1, 'C')
            self.ln(10)
    
    # Instanciar PDF
    pdf = PDF()
    pdf.add_page()
    
    # Título
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(0, 10, f'ORDEM DE SERVIÇO Nº {ordem["id"]}', 0, 1, 'C')
    pdf.ln(5)
    
    # Informações do cliente
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, 'Dados do Cliente', 0, 1)
    pdf.set_font('Arial', '', 11)
    pdf.cell(0, 8, f'Nome: {cliente["nome"]}', 0, 1)
    pdf.cell(0, 8, f'Telefone: {cliente["telefone"]}', 0, 1)
    pdf.cell(0, 8, f'E-mail: {cliente["email"] or "Não informado"}', 0, 1)
    pdf.cell(0, 8, f'Endereço: {cliente["endereco"] or "Não informado"}', 0, 1)
    pdf.ln(5)
    
    # Tabela 1: Informações da Ordem
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, 'Informações da Ordem de Serviço', 0, 1)
    
    # Cabeçalho da tabela
    pdf.set_font('Arial', 'B', 10)
    pdf.set_fill_color(230, 230, 230)
    
    # Definir larguras das colunas
    col_width_data = 40
    col_width_cliente = 50
    col_width_veiculo = 50
    col_width_placa = 40
    
    # Cabeçalho da primeira tabela
    pdf.cell(col_width_data, 10, 'Data de Entrada', 1, 0, 'C', 1)
    pdf.cell(col_width_cliente, 10, 'Cliente', 1, 0, 'C', 1)
    pdf.cell(col_width_veiculo, 10, 'Veículo', 1, 0, 'C', 1)
    pdf.cell(col_width_placa, 10, 'Placa', 1, 1, 'C', 1)
    
    # Dados da primeira tabela
    pdf.set_font('Arial', '', 10)
    pdf.cell(col_width_data, 10, ordem["data"], 1, 0, 'C')
    pdf.cell(col_width_cliente, 10, cliente["nome"], 1, 0, 'C')
    pdf.cell(col_width_veiculo, 10, ordem["veiculo"] or "Não informado", 1, 0, 'C')
    pdf.cell(col_width_placa, 10, ordem["placa"] or "Não informada", 1, 1, 'C')
    
    pdf.ln(5)
      # Tabela 2: Descrição do Serviço e Valor
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, 'Descrição do Serviço e Valor', 0, 1)
    
    # Cabeçalho da segunda tabela
    pdf.set_font('Arial', 'B', 10)
    col_width_desc = 140
    col_width_valor = 40
    
    pdf.cell(col_width_desc, 10, 'Descrição', 1, 0, 'C', 1)
    pdf.cell(col_width_valor, 10, 'Valor (R$)', 1, 1, 'C', 1)
    
    # Descrição do serviço na tabela
    pdf.set_font('Arial', '', 10)
    
    # Salvar a posição X
    x_position = pdf.get_x()
    
    # Calcular altura necessária para a descrição
    descricao_text = ordem["descricao"]
    
    # Registrar posição inicial
    start_y = pdf.get_y()
    
    # Desenhar a célula de descrição
    pdf.multi_cell(col_width_desc, 10, descricao_text, 1, 'L')
    
    # Registrar posição final após a multi_cell
    end_y = pdf.get_y()
    cell_height = end_y - start_y
    
    # Voltar para a posição correta para a célula de valor
    pdf.set_xy(x_position + col_width_desc, start_y)
    pdf.cell(col_width_valor, cell_height, "0,00", 1, 1, 'C')  # Valor exemplo, ajuste conforme necessário
    
    # Total
    pdf.set_font('Arial', 'B', 10)
    pdf.cell(col_width_desc, 10, 'Total', 1, 0, 'R', 1)
    pdf.cell(col_width_valor, 10, "0,00", 1, 1, 'C', 1)  # Total exemplo, ajuste conforme necessário
    
    pdf.ln(5)
    
    # Tabela 3: Observações
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, 'Observações', 0, 1)
    
    pdf.set_font('Arial', '', 10)
    pdf.cell(0, 30, '', 1, 1, 'L')  # Caixa vazia para observações manuscritas
    
    pdf.ln(5)
    
    # Status e Data de Saída
    pdf.set_font('Arial', 'B', 10)
    pdf.cell(90, 10, 'Data de Saída: ____/____/________', 0, 0, 'L')
    pdf.cell(90, 10, 'Status: _________________________', 0, 1, 'L')
    
    pdf.ln(10)
    
    # Assinaturas
    pdf.cell(90, 10, '_______________________________', 0, 0, 'C')
    pdf.cell(90, 10, '_______________________________', 0, 1, 'C')
    pdf.cell(90, 5, 'Assinatura do Cliente', 0, 0, 'C')
    pdf.cell(90, 5, 'Assinatura do Responsável', 0, 1, 'C')
    
    # Rodapé
    pdf.ln(15)
    pdf.set_font('Arial', 'I', 8)
    pdf.cell(0, 5, 'Este documento é uma ordem de serviço e não tem valor fiscal.', 0, 1, 'C')
    pdf.cell(0, 5, f'Data de emissão: {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}', 0, 1, 'C')
    
    # Salvar o PDF em um arquivo temporário
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
    pdf_path = temp_file.name
    temp_file.close()
    
    pdf.output(pdf_path)
    
    # Enviar o arquivo para o usuário
    return send_file(pdf_path, as_attachment=True, download_name=f'ordem_servico_{ordem["id"]}.pdf')

# ---------- ROTAS DE ESTOQUE ----------
@app.route('/estoque', methods=['GET', 'POST'])
def estoque():
    conn = get_db_connection()
    if request.method == 'POST':
        nome = request.form['nome']
        quantidade = request.form['quantidade']
        valor = request.form.get('valor', 0)
        valor_instalado = request.form.get('valor_instalado', 0)
        conn.execute('INSERT INTO pecas (nome, quantidade, valor, valor_instalado) VALUES (?, ?, ?, ?)', 
                    (nome, quantidade, valor, valor_instalado))
        conn.commit()
        return redirect(url_for('estoque'))
    pecas = conn.execute('SELECT * FROM pecas').fetchall()
    conn.close()
    return render_template('estoque.html', pecas=pecas)

@app.route('/adicionar_peca', methods=['POST'])
def adicionar_peca():
    conn = get_db_connection()
    nome = request.form['nome']
    quantidade = request.form['quantidade']
    valor = request.form.get('valor', 0)
    valor_instalado = request.form.get('valor_instalado', 0)
    conn.execute('INSERT INTO pecas (nome, quantidade, valor, valor_instalado) VALUES (?, ?, ?, ?)', 
                 (nome, quantidade, valor, valor_instalado))
    conn.commit()
    conn.close()
    return redirect(url_for('estoque'))

@app.route('/editar_peca/<int:id>', methods=['GET', 'POST'])
def editar_peca(id):
    conn = get_db_connection()
    if request.method == 'POST':
        nome = request.form['nome']
        quantidade = request.form['quantidade']
        valor = request.form.get('valor', 0)
        valor_instalado = request.form.get('valor_instalado', 0)
        conn.execute('UPDATE pecas SET nome = ?, quantidade = ?, valor = ?, valor_instalado = ? WHERE id = ?',
                     (nome, quantidade, valor, valor_instalado, id))
        conn.commit()
        conn.close()
        return redirect(url_for('estoque'))
    
    peca = conn.execute('SELECT * FROM pecas WHERE id = ?', (id,)).fetchone()
    conn.close()
    return render_template('editar_peca.html', peca=peca)

@app.route('/excluir_peca/<int:id>')
def excluir_peca(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM pecas WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('estoque'))

# Executar o app
if __name__ == '__main__':
    criar_tabelas()  # Chama a função para criar as tabelas antes de iniciar o app
    app.run(debug=True)
