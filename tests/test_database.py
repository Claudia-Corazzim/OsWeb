import unittest
import sys
import os
import sqlite3

# Adicionar o diretório pai ao path para importar o app
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Importar funções do app
from app import get_db_connection

class TestDatabase(unittest.TestCase):
    """Testes para operações de banco de dados"""
    
    def setUp(self):
        """Configuração antes de cada teste"""
        # Usar um banco de dados temporário para testes
        self.test_db_path = 'test_banco.db'
        
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
        conn.close()
    
    def tearDown(self):
        """Limpeza após cada teste"""
        if os.path.exists(self.test_db_path):
            os.remove(self.test_db_path)
    
    def test_insercao_cliente(self):
        """Testa inserção de cliente no banco de dados"""
        conn = sqlite3.connect(self.test_db_path)
        conn.row_factory = sqlite3.Row
        
        # Inserir um cliente
        conn.execute('''
            INSERT INTO clientes (nome, telefone, email, endereco)
            VALUES (?, ?, ?, ?)
        ''', ('João Silva', '11987654321', 'joao@teste.com', 'Av. Principal, 100'))
        conn.commit()
        
        # Verificar se o cliente foi inserido
        cliente = conn.execute('SELECT * FROM clientes WHERE nome = ?', ('João Silva',)).fetchone()
        conn.close()
        
        self.assertIsNotNone(cliente)
        self.assertEqual(cliente['nome'], 'João Silva')
        self.assertEqual(cliente['telefone'], '11987654321')
    
    def test_insercao_ordem_servico(self):
        """Testa inserção de ordem de serviço no banco de dados"""
        conn = sqlite3.connect(self.test_db_path)
        conn.row_factory = sqlite3.Row
        
        # Inserir um cliente primeiro
        cursor = conn.execute('''
            INSERT INTO clientes (nome, telefone, email, endereco)
            VALUES (?, ?, ?, ?)
        ''', ('Maria Santos', '11912345678', 'maria@teste.com', 'Rua Secundária, 200'))
        conn.commit()
        cliente_id = cursor.lastrowid
        
        # Inserir uma ordem de serviço
        conn.execute('''
            INSERT INTO ordens_servico (cliente_id, descricao, data, veiculo, placa, valor, observacoes)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (cliente_id, 'Manutenção', '2025-06-17', 'Fiat Uno', 'ABC-1234', 150.0, 'Urgente'))
        conn.commit()
        
        # Verificar se a ordem foi inserida
        ordem = conn.execute('SELECT * FROM ordens_servico WHERE cliente_id = ?', (cliente_id,)).fetchone()
        conn.close()
        
        self.assertIsNotNone(ordem)
        self.assertEqual(ordem['descricao'], 'Manutenção')
        self.assertEqual(ordem['veiculo'], 'Fiat Uno')
        self.assertEqual(float(ordem['valor']), 150.0)
    
    def test_insercao_servicos(self):
        """Testa inserção de serviços em uma ordem de serviço"""
        conn = sqlite3.connect(self.test_db_path)
        conn.row_factory = sqlite3.Row
        
        # Inserir cliente e ordem de serviço
        cursor = conn.execute('INSERT INTO clientes (nome) VALUES (?)', ('Pedro Oliveira',))
        cliente_id = cursor.lastrowid
        
        cursor = conn.execute('''
            INSERT INTO ordens_servico (cliente_id, descricao, data)
            VALUES (?, ?, ?)
        ''', (cliente_id, 'Revisão geral', '2025-06-17'))
        ordem_id = cursor.lastrowid
        
        # Inserir serviços
        servicos = [
            ('Troca de óleo - R$ 50,00', 50.0),
            ('Filtro de ar - R$ 30,00', 30.0),
            ('Alinhamento - R$ 80,00', 80.0)
        ]
        
        for desc, valor in servicos:
            conn.execute('''
                INSERT INTO servicos_os (ordem_servico_id, descricao, valor)
                VALUES (?, ?, ?)
            ''', (ordem_id, desc, valor))
        
        conn.commit()
        
        # Verificar serviços inseridos
        servicos_db = conn.execute('SELECT * FROM servicos_os WHERE ordem_servico_id = ?', (ordem_id,)).fetchall()
        conn.close()
        
        self.assertEqual(len(servicos_db), 3)
        total_valor = sum([float(s['valor']) for s in servicos_db])
        self.assertEqual(total_valor, 160.0)

if __name__ == '__main__':
    unittest.main()
