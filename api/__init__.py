"""
Inicializa a API REST
"""
from flask_restful import Api
from .resources import ClienteAPI, OrdemServicoAPI, EstoqueAPI
from .external import buscar_cep
from flask import jsonify

def init_api(app):
    api = Api(app, prefix='/api')
    
    # Rotas para clientes
    api.add_resource(ClienteAPI, '/clientes', '/clientes/<int:cliente_id>')
    
    # Rotas para ordens de serviço
    api.add_resource(OrdemServicoAPI, '/os', '/os/<int:os_id>')
    
    # Rotas para estoque
    api.add_resource(EstoqueAPI, '/estoque', '/estoque/<int:peca_id>')
    
    # Rota para consulta de CEP
    @app.route('/api/consulta_cep/<cep>')
    def consulta_cep(cep):
        resultado = buscar_cep(cep)
        return jsonify(resultado)
    
    return api
