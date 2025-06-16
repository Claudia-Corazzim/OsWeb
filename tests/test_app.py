import unittest
import os
import sys
import tempfile
import json

# Adiciona o diretório principal ao caminho do Python
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import app

class FlaskTestCase(unittest.TestCase):
    def setUp(self):
        # Cria um ambiente de teste temporário
        self.db_fd, app.app.config['DATABASE'] = tempfile.mkstemp()
        app.app.config['TESTING'] = True
        self.client = app.app.test_client()
        
        # Inicializa o banco de dados de teste
        with app.app.app_context():
            app.criar_tabelas()
    
    def tearDown(self):
        # Limpa o ambiente de teste
        os.close(self.db_fd)
        os.unlink(app.app.config['DATABASE'])
    
    # Testes de Clientes
    def test_pagina_clientes(self):
        """Verifica se a página de clientes está acessível"""
        response = self.client.get('/clientes')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Gerenciamento de Clientes', response.data)
    
    def test_adicionar_cliente(self):
        """Testa a adição de um novo cliente"""
        response = self.client.post('/adicionar_cliente', data={
            'nome': 'Cliente Teste',
            'telefone': '(11) 99999-9999',
            'email': 'teste@example.com',
            'endereco': 'Rua Teste, 123, Bairro, Cidade-UF'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Cliente Teste', response.data)
    
    # Testes de Ordens de Serviço
    def test_pagina_os(self):
        """Verifica se a página de ordens de serviço está acessível"""
        response = self.client.get('/ordens_servico')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Ordens de Servi', response.data)  # Texto parcial para evitar problemas com caracteres especiais
    
    # Testes de Estoque
    def test_pagina_estoque(self):
        """Verifica se a página de estoque está acessível"""
        response = self.client.get('/estoque')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Gerenciamento de Estoque', response.data)
    
    # Testes da API REST
    def test_api_clientes(self):
        """Testa o endpoint de listagem de clientes da API"""
        response = self.client.get('/api/clientes')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')
    
    def test_api_criar_cliente(self):
        """Testa a criação de cliente via API"""
        response = self.client.post('/api/clientes', 
            data=json.dumps({
                'nome': 'API Cliente',
                'telefone': '(11) 88888-8888',
                'email': 'api@example.com',
                'endereco': 'Av API, 456'
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertEqual(data['nome'], 'API Cliente')
    
    # Teste de integração com API externa
    def test_consulta_cep(self):
        """Testa a consulta de CEP"""
        response = self.client.get('/api/consulta_cep/01001000')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('endereco', data)

if __name__ == '__main__':
    unittest.main()
