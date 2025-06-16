from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

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
    except sqlite3.OperationalError:
        # Se não existir, cria uma nova tabela com as colunas
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
        pass    # Verificar se é necessário atualizar a tabela de peças
    try:
        # Verifica se a coluna valor existe
        conn.execute('SELECT valor FROM pecas LIMIT 1')
    except sqlite3.OperationalError:
        # Se não existir, cria uma nova tabela com a coluna
        conn.execute('DROP TABLE IF EXISTS pecas')
        conn.execute('''
            CREATE TABLE pecas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                quantidade INTEGER NOT NULL,
                valor REAL
            );
        ''')
    else:
        # Se já existir, não faz nada
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

# ---------- ROTAS DE ESTOQUE ----------
@app.route('/estoque', methods=['GET', 'POST'])
def estoque():
    conn = get_db_connection()
    if request.method == 'POST':
        nome = request.form['nome']
        quantidade = request.form['quantidade']
        valor = request.form.get('valor', 0)
        conn.execute('INSERT INTO pecas (nome, quantidade, valor) VALUES (?, ?, ?)', (nome, quantidade, valor))
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
    conn.execute('INSERT INTO pecas (nome, quantidade, valor) VALUES (?, ?, ?)', 
                 (nome, quantidade, valor))
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
        conn.execute('UPDATE pecas SET nome = ?, quantidade = ?, valor = ? WHERE id = ?',
                     (nome, quantidade, valor, id))
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
