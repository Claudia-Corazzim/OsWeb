from flask import Flask, render_template, request, redirect, url_for, make_response, send_file, jsonify, flash
import psycopg2
from psycopg2.extras import DictCursor
from datetime import datetime
from fpdf import FPDF
import os
import tempfile
import re  # Add this for regex pattern matching
# Para desenvolvimento local, pode comentar as duas linhas abaixo se não tiver .env
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # Em produção (Railway), as variáveis de ambiente já estão disponíveis
    pass

# Importar a API REST
from api import init_api
# Importar a função de geração de PDF
from gerar_pdf import PDF

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'sua_chave_secreta_aqui')  # Usar variável de ambiente
# Inicializar a API REST
init_api(app)

def get_db_connection():
    # Usar variáveis de ambiente para a conexão com PostgreSQL
    database_url = os.getenv('DATABASE_URL')
    
    if database_url:
        # Railway fornece DATABASE_URL
        conn = psycopg2.connect(database_url)
    else:
        # Desenvolvimento local
        conn = psycopg2.connect(
            dbname=os.getenv('DB_NAME', 'osweb'),
            user=os.getenv('DB_USER', 'admin'),
            password=os.getenv('DB_PASSWORD', 'admin'),
            host=os.getenv('DB_HOST', 'localhost'),
            port=os.getenv('DB_PORT', '5432')
        )
    
    conn.cursor_factory = DictCursor
    return conn

# Criação das tabelas (clientes, ordens, peças)
def criar_tabelas():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Criar a tabela de clientes se não existir
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS clientes (
            id SERIAL PRIMARY KEY,
            nome TEXT NOT NULL,
            telefone TEXT,
            email TEXT,
            endereco TEXT
        );
    ''')
    
    # Criar a tabela de ordens de serviço se não existir
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ordens_servico (
            id SERIAL PRIMARY KEY,
            cliente_id INTEGER NOT NULL,
            descricao TEXT NOT NULL,
            data TEXT NOT NULL,
            veiculo TEXT,
            placa TEXT,
            valor NUMERIC DEFAULT 0,
            observacoes TEXT,
            FOREIGN KEY (cliente_id) REFERENCES clientes (id)
        );
    ''')
    
    # Criar a tabela de peças se não existir
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pecas (
            id SERIAL PRIMARY KEY,
            nome TEXT NOT NULL,
            quantidade INTEGER NOT NULL,
            valor NUMERIC,
            valor_instalado NUMERIC
        );
    ''')
    
    # Criar a tabela de serviços se não existir
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS servicos_os (
            id SERIAL PRIMARY KEY,
            ordem_servico_id INTEGER NOT NULL,
            descricao TEXT NOT NULL,
            valor NUMERIC NOT NULL DEFAULT 0,
            FOREIGN KEY (ordem_servico_id) REFERENCES ordens_servico (id)
        )
    ''')

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
    cursor = conn.cursor()
    if request.method == 'POST':
        nome = request.form['nome']
        telefone = request.form['telefone']
        email = request.form.get('email', '')
        endereco = request.form.get('endereco', '')
        cursor.execute('INSERT INTO clientes (nome, telefone, email, endereco) VALUES (%s, %s, %s, %s)', 
                    (nome, telefone, email, endereco))
        conn.commit()
        return redirect(url_for('clientes'))
    cursor.execute('SELECT * FROM clientes')
    clientes = cursor.fetchall()
    conn.close()
    return render_template('clientes.html', clientes=clientes)

@app.route('/adicionar_cliente', methods=['POST'])
def adicionar_cliente():
    conn = get_db_connection()
    cursor = conn.cursor()
    nome = request.form['nome']
    telefone = request.form['telefone']
    email = request.form['email']
    endereco = request.form['endereco']
    cursor.execute('INSERT INTO clientes (nome, telefone, email, endereco) VALUES (%s, %s, %s, %s)', 
                 (nome, telefone, email, endereco))
    conn.commit()
    conn.close()
    return redirect(url_for('clientes'))

@app.route('/editar_cliente/<int:id>', methods=['GET', 'POST'])
def editar_cliente(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    if request.method == 'POST':
        nome = request.form['nome']
        telefone = request.form['telefone']
        email = request.form['email']
        endereco = request.form['endereco']
        cursor.execute('UPDATE clientes SET nome = %s, telefone = %s, email = %s, endereco = %s WHERE id = %s',
                     (nome, telefone, email, endereco, id))
        conn.commit()
        conn.close()
        return redirect(url_for('clientes'))
    cursor.execute('SELECT * FROM clientes WHERE id = %s', (id,))
    cliente = cursor.fetchone()
    conn.close()
    return render_template('editar_cliente.html', cliente=cliente)

@app.route('/excluir_cliente/<int:id>')
def excluir_cliente(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Verificar se o cliente tem ordens de serviço associadas
        cursor.execute('SELECT COUNT(*) FROM ordens_servico WHERE cliente_id = %s', (id,))
        count = cursor.fetchone()[0]
        
        if count > 0:
            flash(f'Não é possível excluir o cliente. Existem {count} ordem(ns) de serviço associada(s) a este cliente.', 'error')
        else:
            # Buscar nome do cliente para mostrar na mensagem
            cursor.execute('SELECT nome FROM clientes WHERE id = %s', (id,))
            cliente = cursor.fetchone()
            
            if cliente:
                cursor.execute('DELETE FROM clientes WHERE id = %s', (id,))
                conn.commit()
                flash(f'Cliente "{cliente["nome"]}" excluído com sucesso!', 'success')
            else:
                flash('Cliente não encontrado.', 'error')
    
    except Exception as e:
        flash(f'Erro ao excluir cliente: {str(e)}', 'error')
    finally:
        conn.close()
    
    return redirect(url_for('clientes'))

# ---------- ROTAS DE ORDENS DE SERVIÇO ----------
@app.route('/ordens_servico', methods=['GET', 'POST'])
def ordens_servico():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT os.id, c.nome AS cliente, os.data, 
               os.cliente_id, os.veiculo, os.placa, os.valor, os.observacoes,
               string_agg(servicos.descricao, ', ') as servicos_descricao
        FROM ordens_servico os
        JOIN clientes c ON os.cliente_id = c.id
        LEFT JOIN servicos_os servicos ON os.id = servicos.ordem_servico_id
        GROUP BY os.id, c.nome
        ORDER BY os.id DESC
    ''')
    os_list = cursor.fetchall()
    
    cursor.execute('SELECT * FROM clientes')
    clientes = cursor.fetchall()
    conn.close()
    
    # Passar a data atual para o template para pré-preencher o campo de data
    today = datetime.now().strftime('%Y-%m-%d')
    return render_template('os.html', os_list=os_list, clientes=clientes, today=today)

@app.route('/adicionar_os', methods=['POST'])
def adicionar_os():
    conn = get_db_connection()
    cursor = conn.cursor()
    cliente_id = request.form['cliente_id']
    data = request.form['data']
    veiculo = request.form.get('veiculo', '')
    placa = request.form.get('placa', '')
    observacoes = request.form.get('observacoes', '')
    
    # Pegar as descrições dos serviços
    descricoes = request.form.getlist('descricoes[]')
    
    # Obter a primeira descrição para usar como descrição principal da OS
    descricao_principal = "Serviço geral" # Valor padrão caso não haja descrições
    if descricoes and len(descricoes) > 0 and descricoes[0]:
        descricao_principal = descricoes[0]
    
    # Criar a ordem de serviço (valor total será atualizado depois)
    cursor.execute('''
        INSERT INTO ordens_servico (cliente_id, descricao, data, veiculo, placa, valor, observacoes)
        VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING id
    ''', (cliente_id, descricao_principal, data, veiculo, placa, 0, observacoes))
    
    # Pegar o ID da ordem recém-criada
    ordem_id = cursor.fetchone()[0]
    
    # Inserir cada serviço - extrair o valor da descrição
    valor_total = 0
    alertas_estoque = []
    
    for descricao in descricoes:
        if descricao.strip():  # Apenas processar linhas não vazias
            # Verificar e atualizar estoque
            alerta = verificar_e_atualizar_estoque(cursor, descricao)
            if alerta:
                alertas_estoque.append(alerta)
            
            # Extrair valor da descrição
            valor = extrair_valor_de_descricao(descricao)
            valor_total += valor
            
            cursor.execute('''
                INSERT INTO servicos_os (ordem_servico_id, descricao, valor)
                VALUES (%s, %s, %s)
            ''', (ordem_id, descricao, valor))
    
    # Atualizar o valor total da OS
    cursor.execute('''
        UPDATE ordens_servico 
        SET valor = %s
        WHERE id = %s
    ''', (valor_total, ordem_id))
    
    conn.commit()
    conn.close()
    
    # Se houver alertas de estoque, mostrar para o usuário
    if alertas_estoque:
        flash('\\n'.join(alertas_estoque), 'warning')
    
    return redirect(url_for('ordens_servico'))

@app.route('/editar_os/<int:id>', methods=['GET', 'POST'])
def editar_os(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    if request.method == 'POST':
        cliente_id = request.form['cliente_id']
        data = request.form['data']
        veiculo = request.form.get('veiculo', '')
        placa = request.form.get('placa', '')
        observacoes = request.form.get('observacoes', '')
        
        # Pegar as descrições dos serviços
        descricoes = request.form.getlist('descricoes[]')
        
        # Obter a primeira descrição para usar como descrição principal da OS
        descricao_principal = "Serviço geral" # Valor padrão caso não haja descrições
        if descricoes and len(descricoes) > 0 and descricoes[0]:
            descricao_principal = descricoes[0]
        
        # Calcular o valor total extraindo valores das descrições
        valor_total = 0
        for descricao in descricoes:
            if descricao.strip():
                valor = extrair_valor_de_descricao(descricao)
                valor_total += valor
        
        # Atualizar a ordem de serviço
        cursor.execute('''
            UPDATE ordens_servico 
            SET cliente_id = %s, descricao = %s, data = %s, veiculo = %s, 
                placa = %s, valor = %s, observacoes = %s 
            WHERE id = %s
        ''', (cliente_id, descricao_principal, data, veiculo, placa, valor_total, observacoes, id))
        
        # Remover serviços antigos
        cursor.execute('DELETE FROM servicos_os WHERE ordem_servico_id = %s', (id,))
        
        # Inserir novos serviços
        for descricao in descricoes:
            if descricao.strip():
                # Extrair valor da descrição
                valor = extrair_valor_de_descricao(descricao)
                cursor.execute('''
                    INSERT INTO servicos_os (ordem_servico_id, descricao, valor)
                    VALUES (%s, %s, %s)
                ''', (id, descricao, valor))
        
        conn.commit()
        return redirect(url_for('ordens_servico'))
    
    cursor.execute('SELECT * FROM ordens_servico WHERE id = %s', (id,))
    ordem = cursor.fetchone()
    cursor.execute('''
        SELECT descricao, valor 
        FROM servicos_os 
        WHERE ordem_servico_id = %s
        ORDER BY id
    ''', (id,))
    servicos = cursor.fetchall()
    cursor.execute('SELECT * FROM clientes')
    clientes = cursor.fetchall()
    conn.close()
    return render_template('editar_os.html', ordem=ordem, clientes=clientes, servicos=servicos)

@app.route('/excluir_os/<int:id>')
def excluir_os(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Primeiro excluir os serviços associados à ordem
        cursor.execute('DELETE FROM servicos_os WHERE ordem_servico_id = %s', (id,))
        
        # Depois excluir a ordem de serviço
        cursor.execute('DELETE FROM ordens_servico WHERE id = %s', (id,))
        
        conn.commit()
        flash('Ordem de serviço excluída com sucesso!', 'success')
    
    except Exception as e:
        conn.rollback()
        flash(f'Erro ao excluir ordem de serviço: {str(e)}', 'error')
    
    finally:
        conn.close()
    
    return redirect(url_for('ordens_servico'))

# Importar a função de geração de PDF
from gerar_pdf import PDF

@app.route('/gerar_pdf_os/<int:id>')
def gerar_pdf_os(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Buscar dados da ordem de serviço e do cliente
        cursor.execute('SELECT * FROM ordens_servico WHERE id = %s', (id,))
        ordem = cursor.fetchone()
        if not ordem:
            return "Ordem de serviço não encontrada", 404
            
        cursor.execute('SELECT * FROM clientes WHERE id = %s', (ordem['cliente_id'],))
        cliente = cursor.fetchone()
        
        # Buscar serviços da OS
        cursor.execute('''
            SELECT descricao, valor 
            FROM servicos_os 
            WHERE ordem_servico_id = %s
            ORDER BY id
        ''', (id,))
        servicos = cursor.fetchall()
        
        # Criar o PDF
        class PDF(FPDF):
            def header(self):                # Logo
                logo_path = os.path.join(app.root_path, 'static', 'img', 'logo.png')
                if os.path.exists(logo_path):
                    self.image(logo_path, 10, 8, 33)                # Informações da empresa
                self.set_font('Arial', 'B', 12)
                self.cell(0, 6, 'Sergio Eduardo Padilha Corazzim', 0, 1, 'C')
                self.set_font('Arial', '', 9)
                self.cell(0, 3, 'Avenida Pedro Botesi, 2352 - Jd Scomparim - Mogi Mirim - SP', 0, 1, 'C')
                self.cell(0, 3, 'WhatsApp: (19) 99676-0164', 0, 1, 'C')
                self.cell(0, 3, 'CNPJ: 08.101.093/0001-52', 0, 1, 'C')
                self.ln(3)
        
        # Instanciar PDF
        pdf = PDF()
        pdf.add_page()        # Título
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(0, 6, f'ORDEM DE SERVIÇO Nº {ordem["id"]}', 0, 1, 'C')
        pdf.ln(1)
        
        # Informações do cliente
        pdf.set_font('Arial', 'B', 10)
        pdf.cell(0, 4, 'Dados do Cliente', 0, 1)
        pdf.set_font('Arial', '', 9)
        pdf.cell(0, 4, f'Nome: {cliente["nome"]}', 0, 1)
        pdf.cell(0, 4, f'Telefone: {cliente["telefone"]}', 0, 1)
        pdf.cell(0, 4, f'E-mail: {cliente["email"] or "Não informado"}', 0, 1)
        pdf.cell(0, 4, f'Endereço: {cliente["endereco"] or "Não informado"}', 0, 1)
        pdf.ln(1)
        
        # Tabela 1: Informações da Ordem
        pdf.set_font('Arial', 'B', 10)
        pdf.cell(0, 6, 'Informações da Ordem de Serviço', 0, 1)
        
        # Configurações da fonte e cor
        pdf.set_font('Arial', 'B', 8)
        pdf.set_fill_color(230, 230, 230)
        
        # Linha 1: Data de Entrada
        pdf.cell(40, 6, 'Data de Entrada:', 1, 0, 'L', 1)
        pdf.set_font('Arial', '', 8)
        pdf.cell(0, 6, ordem["data"], 1, 1, 'L')
        
        # Linha 2: Cliente
        pdf.set_font('Arial', 'B', 8)
        pdf.cell(40, 6, 'Cliente:', 1, 0, 'L', 1)
        pdf.set_font('Arial', '', 8)
        pdf.cell(0, 6, cliente["nome"], 1, 1, 'L')
        
        # Linha 3: Veículo e Placa
        pdf.set_font('Arial', 'B', 8)
        pdf.cell(40, 6, 'Veículo/Placa:', 1, 0, 'L', 1)
        pdf.set_font('Arial', '', 8)
        veiculo_placa = f"{ordem['veiculo'] or 'Não informado'} - {ordem['placa'] or 'Sem placa'}"
        pdf.cell(0, 6, veiculo_placa, 1, 1, 'L')
        
        pdf.ln(2)        # Tabela 2: Descrição dos Serviços e Valores
        pdf.set_font('Arial', 'B', 10)
        pdf.cell(0, 6, 'Descrição dos Serviços', 0, 1)        # Cabeçalho da segunda tabela
        pdf.set_font('Arial', 'B', 9)
        col_width_desc = 150
        col_width_valor = 30
        pdf.cell(col_width_desc, 5, 'Descrição', 1, 0, 'C', 1)
        pdf.cell(col_width_valor, 5, 'Valor (R$)', 1, 1, 'C', 1)
        # Descrição dos serviços na tabela
        pdf.set_font('Arial', '', 9)
        valor_total = 0
        
        for servico in servicos:
            # Salvar a posição X
            x_position = pdf.get_x()
            
            # Registrar posição inicial
            start_y = pdf.get_y()
            
            # Desenhar a célula de descrição
            pdf.multi_cell(col_width_desc, 5, servico['descricao'], 1, 'L')
            
            # Registrar posição final após a multi_cell
            end_y = pdf.get_y()
            cell_height = end_y - start_y
            
            # Voltar para a posição correta para a célula de valor
            pdf.set_xy(x_position + col_width_desc, start_y)
            
            # Usar o valor já extraído e armazenado no banco
            try:
                valor = float(servico['valor'])
                valor_total += valor
                valor_formatado = f"R$ {valor:,.2f}".replace(',', '.')
            except (ValueError, TypeError):
                valor_formatado = "R$ 0,00"
                
            pdf.cell(col_width_valor, cell_height, valor_formatado, 1, 1, 'C')
          # Total
        pdf.set_font('Arial', 'B', 8)
        pdf.cell(col_width_desc, 6, 'Total', 1, 0, 'R', 1)
        valor_total_formatado = f"R$ {valor_total:,.2f}".replace(',', '.')
        pdf.cell(col_width_valor, 6, valor_total_formatado, 1, 1, 'C', 1)
        
        pdf.ln(2)
        
        # Tabela 3: Observações
        pdf.set_font('Arial', 'B', 10)
        pdf.cell(0, 6, 'Observações', 0, 1)        # Observações da OS
        pdf.set_font('Arial', '', 9)
        observacoes_text = ordem['observacoes'] if ordem['observacoes'] else 'Sem observações'
        pdf.multi_cell(0, 4, observacoes_text, 1, 'L')
        
        pdf.ln(2)        # Status e Data de Saída
        pdf.set_font('Arial', 'B', 9)
        pdf.cell(90, 4, 'Data de Saída: ____/____/________', 0, 0, 'L')
        pdf.cell(90, 4, 'Status: _________________________', 0, 1, 'L')
        
        pdf.ln(3)
        
        # Assinaturas
        pdf.cell(90, 4, '_______________________________', 0, 0, 'C')
        pdf.cell(90, 4, '_______________________________', 0, 1, 'C')
        pdf.set_font('Arial', '', 9)
        pdf.cell(90, 3, 'Assinatura do Cliente', 0, 0, 'C')
        pdf.cell(90, 3, 'Assinatura do Responsável', 0, 1, 'C')
        
        # Rodapé
        pdf.ln(10)
        pdf.set_font('Arial', 'I', 7)
        pdf.cell(0, 4, 'Este documento é uma ordem de serviço e não tem valor fiscal.', 0, 1, 'C')
        pdf.cell(0, 4, f'Data de emissão: {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}', 0, 1, 'C')
        
        # Salvar o PDF em um arquivo temporário
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
        pdf_path = temp_file.name
        temp_file.close()
        
        pdf.output(pdf_path)
        
        return send_file(pdf_path, as_attachment=True, download_name=f'ordem_servico_{ordem["id"]}.pdf')
        
    finally:
        conn.close()

# ---------- ROTAS DE ESTOQUE ----------
@app.route('/estoque', methods=['GET', 'POST'])
def estoque():
    conn = get_db_connection()
    cursor = conn.cursor()
    if request.method == 'POST':
        nome = request.form['nome']
        quantidade = request.form['quantidade']
        valor = request.form.get('valor', 0)
        valor_instalado = request.form.get('valor_instalado', 0)
        cursor.execute('INSERT INTO pecas (nome, quantidade, valor, valor_instalado) VALUES (%s, %s, %s, %s)', 
                    (nome, quantidade, valor, valor_instalado))
        conn.commit()
        return redirect(url_for('estoque'))
    cursor.execute('SELECT * FROM pecas ORDER BY nome ASC')  # Ordenar por nome em ordem alfabética
    pecas = cursor.fetchall()
    conn.close()
    return render_template('estoque.html', pecas=pecas)

@app.route('/adicionar_peca', methods=['POST'])
def adicionar_peca():
    conn = get_db_connection()
    cursor = conn.cursor()
    nome = request.form['nome']
    quantidade = request.form['quantidade']
    valor = request.form.get('valor', 0)
    valor_instalado = request.form.get('valor_instalado', 0)
    cursor.execute('INSERT INTO pecas (nome, quantidade, valor, valor_instalado) VALUES (%s, %s, %s, %s)', 
                 (nome, quantidade, valor, valor_instalado))
    conn.commit()
    conn.close()
    return redirect(url_for('estoque'))

@app.route('/editar_peca/<int:id>', methods=['GET', 'POST'])
def editar_peca(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    if request.method == 'POST':
        nome = request.form['nome']
        quantidade = request.form['quantidade']
        valor = request.form.get('valor', 0)
        valor_instalado = request.form.get('valor_instalado', 0)
        cursor.execute('UPDATE pecas SET nome = %s, quantidade = %s, valor = %s, valor_instalado = %s WHERE id = %s',
                     (nome, quantidade, valor, valor_instalado, id))
        conn.commit()
        conn.close()
        return redirect(url_for('estoque'))
    
    cursor.execute('SELECT * FROM pecas WHERE id = %s', (id,))
    peca = cursor.fetchone()
    conn.close()
    return render_template('editar_peca.html', peca=peca)

@app.route('/excluir_peca/<int:id>')
def excluir_peca(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Buscar nome da peça para mostrar na mensagem
        cursor.execute('SELECT nome FROM pecas WHERE id = %s', (id,))
        peca = cursor.fetchone()
        
        if peca:
            cursor.execute('DELETE FROM pecas WHERE id = %s', (id,))
            conn.commit()
            flash(f'Peça "{peca["nome"]}" excluída com sucesso!', 'success')
        else:
            flash('Peça não encontrada.', 'error')
    
    except Exception as e:
        flash(f'Erro ao excluir peça: {str(e)}', 'error')
    
    finally:
        conn.close()
    
    return redirect(url_for('estoque'))

@app.route('/adicionar_servico/<int:os_id>', methods=['POST'])
def adicionar_servico(os_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    descricao = request.form['descricao_servico']
    valor = request.form.get('valor_servico', '0')
    try:
        valor = float(valor)
    except (ValueError, TypeError):
        valor = 0.0
        
    # Inserir o serviço
    cursor.execute('''
        INSERT INTO servicos_os (ordem_servico_id, descricao, valor)
        VALUES (%s, %s, %s)
    ''', (os_id, descricao, valor))
    
    # Atualizar o valor total da OS
    cursor.execute('SELECT valor FROM servicos_os WHERE ordem_servico_id = %s', (os_id,))
    servicos = cursor.fetchall()
    valor_total = sum([s['valor'] for s in servicos])
    
    cursor.execute('UPDATE ordens_servico SET valor = %s WHERE id = %s', (valor_total, os_id))
    
    conn.commit()
    conn.close()
    return redirect(url_for('editar_os', id=os_id))

# Função para extrair o valor de uma descrição de serviço
def extrair_valor_de_descricao(descricao):
    """
    Extrai o valor monetário de uma descrição de serviço.
    Ex: "1 tampa - R$ 30,00" -> 30.00
    """
    # Busca padrões como R$ 30,00 ou 30,00
    # Padrão 1: R$ seguido de números, vírgula e números
    pattern1 = r'R\$\s*(\d+[,.]\d+)'
    # Padrão 2: R$ seguido de números apenas
    pattern2 = r'R\$\s*(\d+)'
    # Padrão 3: Apenas números, vírgula e números no final
    pattern3 = r'(\d+[,.]\d+)$'
    
    match = re.search(pattern1, descricao) or re.search(pattern2, descricao) or re.search(pattern3, descricao)
    
    if match:
        valor_str = match.group(1).replace(',', '.')
        try:
            return float(valor_str)
        except ValueError:
            return 0.0
    return 0.0

# Função para verificar e atualizar estoque
def verificar_e_atualizar_estoque(cursor, descricao):
    """
    Verifica se a peça existe no estoque e atualiza a quantidade.
    Retorna uma mensagem se o estoque estiver baixo (menos de 2 unidades).
    """
    # Extrair nome da peça da descrição (assume que está antes do hífen)
    nome_peca = descricao.split('-')[0].strip() if '-' in descricao else descricao.strip()
    
    # Buscar a peça no estoque
    cursor.execute('SELECT id, quantidade FROM pecas WHERE nome ILIKE %s', (nome_peca,))
    peca = cursor.fetchone()
    
    if peca and peca['quantidade'] > 0:
        nova_quantidade = peca['quantidade'] - 1
        cursor.execute('UPDATE pecas SET quantidade = %s WHERE id = %s', 
                      (nova_quantidade, peca['id']))
        
        # Verificar se o estoque está baixo (menos de 2 unidades)
        if nova_quantidade < 2:
            return f"ATENÇÃO: Estoque CRÍTICO para {nome_peca} (Restam apenas {nova_quantidade} unidade{'s' if nova_quantidade != 1 else ''})"
        elif nova_quantidade == 2:
            return f"ATENÇÃO: Estoque baixo para {nome_peca} (Restam apenas 2 unidades)"
    
    return None

# ---------- API ENDPOINTS ----------
@app.route('/api/clientes', methods=['GET'])
def api_clientes():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM clientes')
    clientes = cursor.fetchall()
    conn.close()
    return jsonify([dict(cliente) for cliente in clientes])

@app.route('/api/os/<int:id>', methods=['GET'])
def api_ordem_servico(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM ordens_servico WHERE id = %s', (id,))
    ordem = cursor.fetchone()
    conn.close()
    if ordem is None:
        return jsonify({'error': 'Ordem de serviço não encontrada'}), 404
    return jsonify(dict(ordem))

@app.route('/api/estoque', methods=['GET'])
def api_estoque():
    conn = get_db_connection()
    cursor = conn.cursor()
    # Se tiver um parâmetro de busca, filtra as peças
    search = request.args.get('search', '').strip()
    if search:
        # Criar o padrão de busca como %termo%
        search_pattern = f'%{search}%'
        cursor.execute('SELECT * FROM pecas WHERE nome ILIKE %s ORDER BY nome ASC', (search_pattern,))
    else:
        cursor.execute('SELECT * FROM pecas ORDER BY nome ASC')
    pecas = cursor.fetchall()
    conn.close()
    return jsonify([dict(peca) for peca in pecas])

# Executar o app
if __name__ == '__main__':
    criar_tabelas()  # Chama a função para criar todas as tabelas antes de iniciar o app
    port = int(os.getenv('PORT', 5000))  # Railway define a porta via variável de ambiente
    app.run(host='0.0.0.0', port=port, debug=False)
