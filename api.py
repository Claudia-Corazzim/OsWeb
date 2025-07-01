import psycopg2
from psycopg2.extras import DictCursor
from flask_restful import Api, Resource
from flask import jsonify, current_app

def get_db_connection():
    conn = psycopg2.connect(
        host="localhost",
        database="osweb",
        user="admin",
        password="admin",
        cursor_factory=DictCursor
    )
    return conn

class ClientesAPI(Resource):
    def get(self):
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT * FROM clientes')
        clientes = cur.fetchall()
        cur.close()
        conn.close()
        return jsonify([dict(cliente) for cliente in clientes])

class OrdemServicoAPI(Resource):
    def get(self, id=None):
        conn = get_db_connection()
        cur = conn.cursor()
        
        if id is None:
            cur.execute('''
                SELECT os.*, c.nome as cliente_nome, 
                       string_agg(s.descricao, ',') as servicos,
                       string_agg(CAST(s.valor AS text), ',') as valores
                FROM ordens_servico os
                JOIN clientes c ON os.cliente_id = c.id
                LEFT JOIN servicos_os s ON os.id = s.ordem_servico_id
                GROUP BY os.id, c.nome
            ''')
            ordens = cur.fetchall()
            
            result = []
            for ordem in ordens:
                ordem_dict = dict(ordem)
                ordem_dict['servicos'] = ordem_dict['servicos'].split(',') if ordem_dict['servicos'] else []
                ordem_dict['valores'] = [float(v) for v in ordem_dict['valores'].split(',')] if ordem_dict['valores'] else []
                result.append(ordem_dict)
            
            cur.close()
            conn.close()
            return jsonify(result)
        else:
            cur.execute('''
                SELECT os.*, c.nome as cliente_nome 
                FROM ordens_servico os
                JOIN clientes c ON os.cliente_id = c.id
                WHERE os.id = %s
            ''', (id,))
            ordem = cur.fetchone()
            
            if ordem is None:
                cur.close()
                conn.close()
                return {'message': 'Ordem de serviço não encontrada'}, 404
                
            cur.execute('''
                SELECT descricao, valor
                FROM servicos_os
                WHERE ordem_servico_id = %s
            ''', (id,))
            servicos = cur.fetchall()
            
            ordem_dict = dict(ordem)
            ordem_dict['servicos'] = [s['descricao'] for s in servicos]
            ordem_dict['valores'] = [float(s['valor']) for s in servicos]
            
            cur.close()
            conn.close()
            return jsonify(ordem_dict)

class EstoqueAPI(Resource):
    def get(self):
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT * FROM estoque')
        itens = cur.fetchall()
        cur.close()
        conn.close()
        return jsonify([dict(item) for item in itens])

def init_api(app):
    api = Api(app)
    api.add_resource(ClientesAPI, '/api/clientes')
    api.add_resource(OrdemServicoAPI, '/api/ordens', '/api/ordens/<int:id>')
    api.add_resource(EstoqueAPI, '/api/estoque')
