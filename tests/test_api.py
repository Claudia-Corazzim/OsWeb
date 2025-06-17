import unittest
import os
import sys
import tempfile
import json

# Adiciona o diretório principal ao caminho do Python
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import app

class APITestCase(unittest.TestCase):
    def setUp(self):
        # Cria um ambiente de teste temporário
        self.db_fd, app.app.config['DATABASE'] = tempfile.mkstemp()
        app.app.config['TESTING'] = True
        self.client = app.app.test_client()
        
        # Inicializa o banco de dados de teste
        with app.app.app_context():
            app.criar_tabelas()
            app.criar_tabela_servicos()
            
            # Adicionar alguns dados de teste
            conn = app.get_db_connection()
            conn.execute('INSERT INTO clientes (nome, telefone, email, endereco) VALUES (?, ?, ?, ?)',
                        ('Cliente Teste API', '11999999999', 'teste@api.com', 'Rua API, 123'))
            cliente_id = conn.execute('SELECT last_insert_rowid()').fetchone()[0]
            
            conn.execute('''
                INSERT INTO ordens_servico (cliente_id, descricao, data, veiculo, placa, valor, observacoes)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (cliente_id, 'OS Teste API', '2023-06-18', 'Carro Teste', 'ABC-1234', 100.0, 'Observação teste'))
            os_id = conn.execute('SELECT last_insert_rowid()').fetchone()[0]
            
            conn.execute('''
                INSERT INTO servicos_os (ordem_servico_id, descricao, valor)
                VALUES (?, ?, ?)
            ''', (os_id, 'Serviço Teste - R$ 100,00', 100.0))
            
            conn.commit()
            conn.close()
    
    def tearDown(self):
        # Limpa o ambiente de teste
        os.close(self.db_fd)
        os.unlink(app.app.config['DATABASE'])
    
    # Testes de API de Clientes
    def test_listar_clientes(self):
        """Testa a listagem de clientes via API"""
        response = self.client.get('/api/clientes')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(isinstance(data, list))
        self.assertTrue(len(data) > 0)
        self.assertIn('nome', data[0])
        self.assertEqual(data[0]['nome'], 'Cliente Teste API')
    
    def test_criar_cliente(self):
        """Testa a criação de um cliente via API"""
        novo_cliente = {
            'nome': 'Novo Cliente API',
            'telefone': '11888888888',
            'email': 'novo@api.com',
            'endereco': 'Av. Nova API, 456'
        }
        response = self.client.post('/api/clientes', 
            data=json.dumps(novo_cliente),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertEqual(data['nome'], 'Novo Cliente API')
        self.assertIn('id', data)
    
    # Testes de API de Ordens de Serviço
    def test_listar_ordens_servico(self):
        """Testa a listagem de ordens de serviço via API"""
        response = self.client.get('/api/os')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(isinstance(data, list))
        self.assertTrue(len(data) > 0)
        self.assertIn('descricao', data[0])
        self.assertEqual(data[0]['descricao'], 'OS Teste API')
    
    def test_obter_ordem_servico(self):
        """Testa a obtenção de uma ordem de serviço específica via API"""
        # Primeiro, obtém a lista para pegar o ID
        response = self.client.get('/api/os')
        data = json.loads(response.data)
        os_id = data[0]['id']
        
        # Agora, obtém a ordem específica
        response = self.client.get(f'/api/os/{os_id}')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['id'], os_id)
        self.assertEqual(data['descricao'], 'OS Teste API')
        self.assertIn('servicos', data)
    
    # Testes de API de Serviços
    def test_listar_servicos_os(self):
        """Testa a listagem de serviços de uma ordem de serviço via API"""
        # Primeiro, obtém a lista para pegar o ID
        response = self.client.get('/api/os')
        data = json.loads(response.data)
        os_id = data[0]['id']
        
        # Agora, obtém os serviços da ordem
        response = self.client.get(f'/api/os/{os_id}/servicos')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(isinstance(data, list))
        self.assertTrue(len(data) > 0)
        self.assertIn('descricao', data[0])
        self.assertEqual(data[0]['descricao'], 'Serviço Teste - R$ 100,00')

if __name__ == '__main__':
    unittest.main()
