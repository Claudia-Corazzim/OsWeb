import unittest
import os
import sys
import tempfile
import sqlite3

# Adiciona o diretório principal ao caminho do Python
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app, get_db_connection
from gerar_pdf import PDF

class PDFTestCase(unittest.TestCase):
    def setUp(self):
        # Configurar o ambiente de teste
        app.config['TESTING'] = True
        self.client = app.test_client()
        
        # Criar banco de dados temporário
        self.db_fd, app.config['DATABASE'] = tempfile.mkstemp()
        
        # Inicializar o banco de dados com dados de teste
        with app.app_context():
            conn = sqlite3.connect(app.config['DATABASE'])
            conn.row_factory = sqlite3.Row
            
            # Criar tabelas
            conn.executescript('''
                CREATE TABLE clientes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    telefone TEXT,
                    email TEXT,
                    endereco TEXT
                );
                
                CREATE TABLE ordens_servico (
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
                
                CREATE TABLE servicos_os (
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
            ''', ('Cliente PDF Teste', '11987654321', 'pdf@teste.com', 'Rua PDF, 789'))
            cliente_id = conn.execute('SELECT last_insert_rowid()').fetchone()[0]
            
            conn.execute('''
                INSERT INTO ordens_servico (cliente_id, descricao, data, veiculo, placa, valor, observacoes)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (cliente_id, 'OS para teste de PDF', '2023-06-19', 'Fiat Uno', 'DEF-5678', 150.0, 'Teste de PDF'))
            os_id = conn.execute('SELECT last_insert_rowid()').fetchone()[0]
            
            servicos = [
                ('Serviço 1 - R$ 50,00', 50.0),
                ('Serviço 2 - R$ 100,00', 100.0)
            ]
            
            for desc, valor in servicos:
                conn.execute('''
                    INSERT INTO servicos_os (ordem_servico_id, descricao, valor)
                    VALUES (?, ?, ?)
                ''', (os_id, desc, valor))
            
            conn.commit()
            conn.close()
            
            # Armazenar o ID da OS para os testes
            self.os_id = os_id
    
    def tearDown(self):
        # Limpar após os testes
        os.close(self.db_fd)
        os.unlink(app.config['DATABASE'])
    
    def test_criacao_instancia_pdf(self):
        """Testa se a classe PDF pode ser instanciada"""
        with app.app_context():
            pdf = PDF()
            self.assertIsInstance(pdf, PDF)
    
    def test_geracao_pdf_os(self):
        """Testa a geração de PDF para uma OS"""
        with app.app_context():
            # Acessar a rota de geração de PDF
            response = self.client.get(f'/pdf_os/{self.os_id}')
            
            # Verificar se a resposta tem o tipo correto
            self.assertEqual(response.mimetype, 'application/pdf')
            self.assertEqual(response.status_code, 200)
            
            # Verificar se o conteúdo não está vazio
            self.assertTrue(len(response.data) > 0)
    
    def test_conteudo_pdf(self):
        """Teste indireto do conteúdo do PDF através da geração e dados na resposta"""
        with app.app_context():
            # Primeiro verifica os dados que devem estar no PDF
            conn = get_db_connection()
            ordem = conn.execute('''
                SELECT os.*, c.nome as cliente_nome, c.telefone, c.email, c.endereco
                FROM ordens_servico os
                JOIN clientes c ON os.cliente_id = c.id
                WHERE os.id = ?
            ''', (self.os_id,)).fetchone()
            
            servicos = conn.execute('''
                SELECT * FROM servicos_os WHERE ordem_servico_id = ?
            ''', (self.os_id,)).fetchall()
            conn.close()
            
            # Agora gera o PDF
            response = self.client.get(f'/pdf_os/{self.os_id}')
            
            # Verificações básicas (não podemos verificar o conteúdo real do PDF facilmente)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.mimetype, 'application/pdf')
            
            # Verificar o tamanho do PDF (deve ser razoável)
            self.assertTrue(len(response.data) > 1000)  # Um PDF válido deve ter pelo menos esse tamanho

if __name__ == '__main__':
    unittest.main()
