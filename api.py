from flask_restful import Api, Resource
from flask import jsonify
import sqlite3

def get_db_connection():
    conn = sqlite3.connect('banco.db')
    conn.row_factory = sqlite3.Row
    return conn

class ClientesAPI(Resource):
    def get(self):
        conn = get_db_connection()
        clientes = conn.execute('SELECT * FROM clientes').fetchall()
        conn.close()
        return jsonify([dict(cliente) for cliente in clientes])

class OrdemServicoAPI(Resource):
    def get(self, id=None):
        conn = get_db_connection()
        
        if id is None:
            # Retorna todas as ordens de serviço
            ordens = conn.execute('''
                SELECT os.*, c.nome as cliente_nome, 
                       GROUP_CONCAT(s.descricao) as servicos,
                       GROUP_CONCAT(s.valor) as valores
                FROM ordens_servico os
                JOIN clientes c ON os.cliente_id = c.id
                LEFT JOIN servicos_os s ON os.id = s.ordem_servico_id
                GROUP BY os.id
            ''').fetchall()
            
            result = []
            for ordem in ordens:
                ordem_dict = dict(ordem)
                # Converte as strings concatenadas em listas
                ordem_dict['servicos'] = ordem_dict['servicos'].split(',') if ordem_dict['servicos'] else []
                ordem_dict['valores'] = [float(v) for v in ordem_dict['valores'].split(',')] if ordem_dict['valores'] else []
                result.append(ordem_dict)
                
            conn.close()
            return jsonify(result)
        else:
            # Retorna uma ordem específica
            ordem = conn.execute('''
                SELECT os.*, c.nome as cliente_nome 
                FROM ordens_servico os
                JOIN clientes c ON os.cliente_id = c.id
                WHERE os.id = ?
            ''', (id,)).fetchone()
            
            if ordem is None:
                conn.close()
                return {'message': 'Ordem not found'}, 404
                
            # Buscar serviços desta ordem
            servicos = conn.execute('''
                SELECT descricao, valor 
                FROM servicos_os 
                WHERE ordem_servico_id = ?
            ''', (id,)).fetchall()
            
            ordem_dict = dict(ordem)
            ordem_dict['servicos'] = [dict(s) for s in servicos]
            
            conn.close()
            return jsonify(ordem_dict)

class ServicosAPI(Resource):
    def get(self, os_id):
        conn = get_db_connection()
        servicos = conn.execute('''
            SELECT * FROM servicos_os WHERE ordem_servico_id = ?
        ''', (os_id,)).fetchall()
        conn.close()
        return jsonify([dict(servico) for servico in servicos])

def init_api(app):
    api = Api(app)
    
    # Rotas da API
    api.add_resource(ClientesAPI, '/api/clientes')
    api.add_resource(OrdemServicoAPI, '/api/os', '/api/os/<int:id>')
    api.add_resource(ServicosAPI, '/api/os/<int:os_id>/servicos')
