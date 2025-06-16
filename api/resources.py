"""
API RESTful para o sistema de gestão de ordens de serviço
"""
from flask_restful import Api, Resource, reqparse
import sqlite3
import json
from flask import jsonify, request

# Função para obter conexão com o banco de dados
def get_db_connection():
    conn = sqlite3.connect('banco.db')
    conn.row_factory = sqlite3.Row
    return conn

# Função para converter uma linha do SQLite em um dicionário
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

# Recursos da API
class ClienteAPI(Resource):
    def get(self, cliente_id=None):
        conn = get_db_connection()
        conn.row_factory = dict_factory
        
        if cliente_id:
            # Obter um cliente específico
            cliente = conn.execute('SELECT * FROM clientes WHERE id = ?', (cliente_id,)).fetchone()
            conn.close()
            
            if not cliente:
                return {'error': 'Cliente não encontrado'}, 404
                
            return jsonify(cliente)
        else:
            # Obter todos os clientes
            clientes = conn.execute('SELECT * FROM clientes').fetchall()
            conn.close()
            return jsonify(clientes)
    
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('nome', type=str, required=True, help='Nome é obrigatório')
        parser.add_argument('telefone', type=str, required=True, help='Telefone é obrigatório')
        parser.add_argument('email', type=str)
        parser.add_argument('endereco', type=str)
        args = parser.parse_args()
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute(
                'INSERT INTO clientes (nome, telefone, email, endereco) VALUES (?, ?, ?, ?)',
                (args['nome'], args['telefone'], args['email'], args['endereco'])
            )
            conn.commit()
            
            # Obter o ID do cliente inserido
            cliente_id = cursor.lastrowid
            
            # Buscar o cliente recém-criado
            conn.row_factory = dict_factory
            cliente = conn.execute('SELECT * FROM clientes WHERE id = ?', (cliente_id,)).fetchone()
            
            conn.close()
            return jsonify(cliente), 201
        except Exception as e:
            conn.close()
            return {'error': str(e)}, 500
    
    def put(self, cliente_id):
        parser = reqparse.RequestParser()
        parser.add_argument('nome', type=str)
        parser.add_argument('telefone', type=str)
        parser.add_argument('email', type=str)
        parser.add_argument('endereco', type=str)
        args = parser.parse_args()
        
        conn = get_db_connection()
        
        # Verificar se o cliente existe
        cliente = conn.execute('SELECT * FROM clientes WHERE id = ?', (cliente_id,)).fetchone()
        if not cliente:
            conn.close()
            return {'error': 'Cliente não encontrado'}, 404
        
        # Atualizar apenas os campos fornecidos
        updates = []
        values = []
        
        for field in ['nome', 'telefone', 'email', 'endereco']:
            if args[field] is not None:
                updates.append(f"{field} = ?")
                values.append(args[field])
        
        if not updates:
            conn.close()
            return {'message': 'Nenhuma alteração realizada'}, 200
        
        try:
            values.append(cliente_id)
            conn.execute(
                f"UPDATE clientes SET {', '.join(updates)} WHERE id = ?",
                values
            )
            conn.commit()
            
            # Buscar o cliente atualizado
            conn.row_factory = dict_factory
            cliente_atualizado = conn.execute('SELECT * FROM clientes WHERE id = ?', (cliente_id,)).fetchone()
            
            conn.close()
            return jsonify(cliente_atualizado), 200
        except Exception as e:
            conn.close()
            return {'error': str(e)}, 500
    
    def delete(self, cliente_id):
        conn = get_db_connection()
        
        # Verificar se o cliente existe
        cliente = conn.execute('SELECT * FROM clientes WHERE id = ?', (cliente_id,)).fetchone()
        if not cliente:
            conn.close()
            return {'error': 'Cliente não encontrado'}, 404
        
        try:
            conn.execute('DELETE FROM clientes WHERE id = ?', (cliente_id,))
            conn.commit()
            conn.close()
            return {'message': 'Cliente excluído com sucesso'}, 200
        except Exception as e:
            conn.close()
            return {'error': str(e)}, 500

class OrdemServicoAPI(Resource):
    def get(self, os_id=None):
        conn = get_db_connection()
        conn.row_factory = dict_factory
        
        if os_id:
            # Obter uma OS específica
            os = conn.execute('''
                SELECT os.*, c.nome as cliente_nome 
                FROM ordens_servico os
                JOIN clientes c ON os.cliente_id = c.id
                WHERE os.id = ?
            ''', (os_id,)).fetchone()
            
            conn.close()
            
            if not os:
                return {'error': 'Ordem de serviço não encontrada'}, 404
                
            return jsonify(os)
        else:
            # Obter todas as OS
            os_list = conn.execute('''
                SELECT os.*, c.nome as cliente_nome 
                FROM ordens_servico os
                JOIN clientes c ON os.cliente_id = c.id
            ''').fetchall()
            
            conn.close()
            return jsonify(os_list)
    
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('cliente_id', type=int, required=True, help='ID do cliente é obrigatório')
        parser.add_argument('descricao', type=str, required=True, help='Descrição é obrigatória')
        parser.add_argument('data', type=str, required=True, help='Data é obrigatória')
        parser.add_argument('veiculo', type=str)
        parser.add_argument('placa', type=str)
        args = parser.parse_args()
        
        conn = get_db_connection()
        
        # Verificar se o cliente existe
        cliente = conn.execute('SELECT * FROM clientes WHERE id = ?', (args['cliente_id'],)).fetchone()
        if not cliente:
            conn.close()
            return {'error': 'Cliente não encontrado'}, 404
        
        cursor = conn.cursor()
        
        try:
            cursor.execute(
                'INSERT INTO ordens_servico (cliente_id, descricao, data, veiculo, placa) VALUES (?, ?, ?, ?, ?)',
                (args['cliente_id'], args['descricao'], args['data'], args['veiculo'], args['placa'])
            )
            conn.commit()
            
            # Obter o ID da OS inserida
            os_id = cursor.lastrowid
            
            # Buscar a OS recém-criada
            conn.row_factory = dict_factory
            os = conn.execute('''
                SELECT os.*, c.nome as cliente_nome 
                FROM ordens_servico os
                JOIN clientes c ON os.cliente_id = c.id
                WHERE os.id = ?
            ''', (os_id,)).fetchone()
            
            conn.close()
            return jsonify(os), 201
        except Exception as e:
            conn.close()
            return {'error': str(e)}, 500

    def put(self, os_id):
        parser = reqparse.RequestParser()
        parser.add_argument('cliente_id', type=int)
        parser.add_argument('descricao', type=str)
        parser.add_argument('data', type=str)
        parser.add_argument('veiculo', type=str)
        parser.add_argument('placa', type=str)
        args = parser.parse_args()
        
        conn = get_db_connection()
        
        # Verificar se a OS existe
        os = conn.execute('SELECT * FROM ordens_servico WHERE id = ?', (os_id,)).fetchone()
        if not os:
            conn.close()
            return {'error': 'Ordem de serviço não encontrada'}, 404
        
        # Verificar se o cliente existe (se fornecido)
        if args['cliente_id'] is not None:
            cliente = conn.execute('SELECT * FROM clientes WHERE id = ?', (args['cliente_id'],)).fetchone()
            if not cliente:
                conn.close()
                return {'error': 'Cliente não encontrado'}, 404
        
        # Atualizar apenas os campos fornecidos
        updates = []
        values = []
        
        for field in ['cliente_id', 'descricao', 'data', 'veiculo', 'placa']:
            if args[field] is not None:
                updates.append(f"{field} = ?")
                values.append(args[field])
        
        if not updates:
            conn.close()
            return {'message': 'Nenhuma alteração realizada'}, 200
        
        try:
            values.append(os_id)
            conn.execute(
                f"UPDATE ordens_servico SET {', '.join(updates)} WHERE id = ?",
                values
            )
            conn.commit()
            
            # Buscar a OS atualizada
            conn.row_factory = dict_factory
            os_atualizada = conn.execute('''
                SELECT os.*, c.nome as cliente_nome 
                FROM ordens_servico os
                JOIN clientes c ON os.cliente_id = c.id
                WHERE os.id = ?
            ''', (os_id,)).fetchone()
            
            conn.close()
            return jsonify(os_atualizada), 200
        except Exception as e:
            conn.close()
            return {'error': str(e)}, 500
    
    def delete(self, os_id):
        conn = get_db_connection()
        
        # Verificar se a OS existe
        os = conn.execute('SELECT * FROM ordens_servico WHERE id = ?', (os_id,)).fetchone()
        if not os:
            conn.close()
            return {'error': 'Ordem de serviço não encontrada'}, 404
        
        try:
            conn.execute('DELETE FROM ordens_servico WHERE id = ?', (os_id,))
            conn.commit()
            conn.close()
            return {'message': 'Ordem de serviço excluída com sucesso'}, 200
        except Exception as e:
            conn.close()
            return {'error': str(e)}, 500

class EstoqueAPI(Resource):
    def get(self, peca_id=None):
        conn = get_db_connection()
        conn.row_factory = dict_factory
        
        if peca_id:
            # Obter uma peça específica
            peca = conn.execute('SELECT * FROM pecas WHERE id = ?', (peca_id,)).fetchone()
            conn.close()
            
            if not peca:
                return {'error': 'Peça não encontrada'}, 404
            
            return peca
        else:            # Obter todas as peças
            pecas = conn.execute('SELECT * FROM pecas').fetchall()
            conn.close()
            return pecas
    
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('nome', type=str, required=True, help='Nome é obrigatório')
        parser.add_argument('quantidade', type=int, required=True, help='Quantidade é obrigatória')
        parser.add_argument('valor', type=float)
        parser.add_argument('valor_instalado', type=float)
        args = parser.parse_args()
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute(
                'INSERT INTO pecas (nome, quantidade, valor, valor_instalado) VALUES (?, ?, ?, ?)',
                (args['nome'], args['quantidade'], args.get('valor', 0), args.get('valor_instalado', 0))
            )
            conn.commit()
            
            # Obter o ID da peça inserida
            peca_id = cursor.lastrowid
              # Buscar a peça recém-criada
            conn.row_factory = dict_factory
            peca = conn.execute('SELECT * FROM pecas WHERE id = ?', (peca_id,)).fetchone()
            
            conn.close()
            return peca, 201
        except Exception as e:
            conn.close()
            return {'error': str(e)}, 500
    
    def put(self, peca_id):
        parser = reqparse.RequestParser()
        parser.add_argument('nome', type=str)
        parser.add_argument('quantidade', type=int)
        parser.add_argument('valor', type=float)
        parser.add_argument('valor_instalado', type=float)
        args = parser.parse_args()
        
        conn = get_db_connection()
        
        # Verificar se a peça existe
        peca = conn.execute('SELECT * FROM pecas WHERE id = ?', (peca_id,)).fetchone()
        if not peca:
            conn.close()
            return {'error': 'Peça não encontrada'}, 404
        
        # Atualizar apenas os campos fornecidos
        updates = []
        values = []
        
        for field in ['nome', 'quantidade', 'valor', 'valor_instalado']:
            if args[field] is not None:
                updates.append(f"{field} = ?")
                values.append(args[field])
        
        if not updates:
            conn.close()
            return {'message': 'Nenhuma alteração realizada'}, 200
        
        try:
            values.append(peca_id)
            conn.execute(
                f"UPDATE pecas SET {', '.join(updates)} WHERE id = ?",
                values
            )
            conn.commit()
              # Buscar a peça atualizada
            conn.row_factory = dict_factory
            peca_atualizada = conn.execute('SELECT * FROM pecas WHERE id = ?', (peca_id,)).fetchone()
            
            conn.close()
            return peca_atualizada, 200
        except Exception as e:
            conn.close()
            return {'error': str(e)}, 500
    
    def delete(self, peca_id):
        conn = get_db_connection()
        
        # Verificar se a peça existe
        peca = conn.execute('SELECT * FROM pecas WHERE id = ?', (peca_id,)).fetchone()
        if not peca:
            conn.close()
            return {'error': 'Peça não encontrada'}, 404
        
        try:
            conn.execute('DELETE FROM pecas WHERE id = ?', (peca_id,))
            conn.commit()
            conn.close()
            return {'message': 'Peça excluída com sucesso'}, 200
        except Exception as e:
            conn.close()
            return {'error': str(e)}, 500
            return {'message': 'Peça excluída com sucesso'}, 200
        except Exception as e:
            conn.close()
            return {'error': str(e)}, 500
