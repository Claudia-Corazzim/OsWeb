import unittest
import sys
import os
import sqlite3

# Adicionar o diretório pai ao path para importar o app
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Importar funções do app
from app import get_db_connection

class TestDatabaseOperations(unittest.TestCase):
    """Testes adicionais para operações de banco de dados"""
    
    def setUp(self):
        """Configuração antes de cada teste"""
        # Usar um banco de dados temporário para testes
        self.test_db_path = 'test_banco_operations.db'
        
        # Criar tabelas de teste
        conn = sqlite3.connect(self.test_db_path)
        conn.executescript('''
            CREATE TABLE IF NOT EXISTS clientes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                telefone TEXT,
                email TEXT,
                endereco TEXT
            );
            
            CREATE TABLE IF NOT EXISTS ordens_servico (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cliente_id INTEGER NOT NULL,
                descricao TEXT NOT NULL,
                data TEXT NOT NULL,
                veiculo TEXT,
                placa TEXT,
                valor REAL,
                observacoes TEXT,
                FOREIGN KEY (cliente_id) REFERENCES clientes (id)
            );
            
            CREATE TABLE IF NOT EXISTS servicos_os (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ordem_servico_id INTEGER NOT NULL,
                descricao TEXT NOT NULL,
                valor REAL NOT NULL DEFAULT 0,
                FOREIGN KEY (ordem_servico_id) REFERENCES ordens_servico (id)
            );
        ''')
        
        # Inserir dados de teste
        conn.execute('''
            INSERT INTO clientes (nome, telefone, email, endereco)
            VALUES (?, ?, ?, ?)
        ''', ('Cliente Teste', '11987654321', 'teste@email.com', 'Rua Teste, 123'))
        self.cliente_id = conn.execute('SELECT last_insert_rowid()').fetchone()[0]
        
        conn.execute('''
            INSERT INTO ordens_servico (cliente_id, descricao, data, veiculo, placa, valor, observacoes)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (self.cliente_id, 'OS Teste', '2023-06-20', 'Gol', 'ABC-1234', 100.0, 'Observação teste'))
        self.os_id = conn.execute('SELECT last_insert_rowid()').fetchone()[0]
        
        conn.execute('''
            INSERT INTO servicos_os (ordem_servico_id, descricao, valor)
            VALUES (?, ?, ?)
        ''', (self.os_id, 'Serviço Teste - R$ 100,00', 100.0))
        self.servico_id = conn.execute('SELECT last_insert_rowid()').fetchone()[0]
        
        conn.commit()
        conn.close()
    
    def tearDown(self):
        """Limpeza após cada teste"""
        if os.path.exists(self.test_db_path):
            os.remove(self.test_db_path)
    
    def test_atualizacao_cliente(self):
        """Testa atualização de cliente no banco de dados"""
        conn = sqlite3.connect(self.test_db_path)
        conn.row_factory = sqlite3.Row
        
        # Atualizar o cliente
        conn.execute('''
            UPDATE clientes
            SET nome = ?, telefone = ?
            WHERE id = ?
        ''', ('Cliente Atualizado', '11912345678', self.cliente_id))
        conn.commit()
        
        # Verificar se o cliente foi atualizado
        cliente = conn.execute('SELECT * FROM clientes WHERE id = ?', (self.cliente_id,)).fetchone()
        conn.close()
        
        self.assertEqual(cliente['nome'], 'Cliente Atualizado')
        self.assertEqual(cliente['telefone'], '11912345678')
    
    def test_atualizacao_ordem_servico(self):
        """Testa atualização de ordem de serviço no banco de dados"""
        conn = sqlite3.connect(self.test_db_path)
        conn.row_factory = sqlite3.Row
        
        # Atualizar a ordem de serviço
        conn.execute('''
            UPDATE ordens_servico
            SET descricao = ?, valor = ?
            WHERE id = ?
        ''', ('OS Atualizada', 150.0, self.os_id))
        conn.commit()
        
        # Verificar se a ordem foi atualizada
        ordem = conn.execute('SELECT * FROM ordens_servico WHERE id = ?', (self.os_id,)).fetchone()
        conn.close()
        
        self.assertEqual(ordem['descricao'], 'OS Atualizada')
        self.assertEqual(float(ordem['valor']), 150.0)
    
    def test_exclusao_cliente(self):
        """Testa exclusão de cliente no banco de dados"""
        conn = sqlite3.connect(self.test_db_path)
        
        # Primeiro, excluímos as ordens de serviço relacionadas
        conn.execute('DELETE FROM servicos_os WHERE ordem_servico_id IN (SELECT id FROM ordens_servico WHERE cliente_id = ?)', (self.cliente_id,))
        conn.execute('DELETE FROM ordens_servico WHERE cliente_id = ?', (self.cliente_id,))
        
        # Agora excluímos o cliente
        conn.execute('DELETE FROM clientes WHERE id = ?', (self.cliente_id,))
        conn.commit()
        
        # Verificar se o cliente foi excluído
        cliente = conn.execute('SELECT * FROM clientes WHERE id = ?', (self.cliente_id,)).fetchone()
        conn.close()
        
        self.assertIsNone(cliente)
    
    def test_exclusao_ordem_servico(self):
        """Testa exclusão de ordem de serviço no banco de dados"""
        conn = sqlite3.connect(self.test_db_path)
        
        # Primeiro, excluímos os serviços relacionados
        conn.execute('DELETE FROM servicos_os WHERE ordem_servico_id = ?', (self.os_id,))
        
        # Agora excluímos a ordem de serviço
        conn.execute('DELETE FROM ordens_servico WHERE id = ?', (self.os_id,))
        conn.commit()
        
        # Verificar se a ordem foi excluída
        ordem = conn.execute('SELECT * FROM ordens_servico WHERE id = ?', (self.os_id,)).fetchone()
        servicos = conn.execute('SELECT * FROM servicos_os WHERE ordem_servico_id = ?', (self.os_id,)).fetchall()
        conn.close()
        
        self.assertIsNone(ordem)
        self.assertEqual(len(servicos), 0)
    
    def test_consulta_cliente_por_id(self):
        """Testa consulta de cliente por ID"""
        conn = sqlite3.connect(self.test_db_path)
        conn.row_factory = sqlite3.Row
        
        # Consultar o cliente
        cliente = conn.execute('SELECT * FROM clientes WHERE id = ?', (self.cliente_id,)).fetchone()
        conn.close()
        
        self.assertIsNotNone(cliente)
        self.assertEqual(cliente['nome'], 'Cliente Teste')
        self.assertEqual(cliente['telefone'], '11987654321')
    
    def test_consulta_ordem_servico_por_id(self):
        """Testa consulta de ordem de serviço por ID"""
        conn = sqlite3.connect(self.test_db_path)
        conn.row_factory = sqlite3.Row
        
        # Consultar a ordem de serviço
        ordem = conn.execute('SELECT * FROM ordens_servico WHERE id = ?', (self.os_id,)).fetchone()
        conn.close()
        
        self.assertIsNotNone(ordem)
        self.assertEqual(ordem['descricao'], 'OS Teste')
        self.assertEqual(float(ordem['valor']), 100.0)
    
    def test_consulta_servicos_por_ordem_id(self):
        """Testa consulta de serviços por ordem de serviço ID"""
        conn = sqlite3.connect(self.test_db_path)
        conn.row_factory = sqlite3.Row
        
        # Consultar os serviços da ordem
        servicos = conn.execute('SELECT * FROM servicos_os WHERE ordem_servico_id = ?', (self.os_id,)).fetchall()
        conn.close()
        
        self.assertEqual(len(servicos), 1)
        self.assertEqual(servicos[0]['descricao'], 'Serviço Teste - R$ 100,00')
        self.assertEqual(float(servicos[0]['valor']), 100.0)

if __name__ == '__main__':
    unittest.main()
