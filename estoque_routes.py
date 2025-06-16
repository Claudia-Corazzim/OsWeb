import sqlite3
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('banco.db')
    conn.row_factory = sqlite3.Row
    return conn

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
