import unittest
import sys
import os

# Adicionar o diretório pai ao path para importar o app
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import extrair_valor_de_descricao

class TestExtracaoValor(unittest.TestCase):
    """Testes para a função de extração de valores das descrições"""
    
    def test_valor_com_r_cifrão(self):
        """Testa extração de valor com formato R$ XX,XX"""
        self.assertEqual(extrair_valor_de_descricao("1 tampa - R$ 30,00"), 30.0)
        self.assertEqual(extrair_valor_de_descricao("Conserto freio - R$ 150,50"), 150.5)
        self.assertEqual(extrair_valor_de_descricao("Troca de óleo R$45,90"), 45.9)
    
    def test_valor_sem_r_cifrão(self):
        """Testa extração de valor sem o R$"""
        self.assertEqual(extrair_valor_de_descricao("Lavagem completa 80,00"), 80.0)
        self.assertEqual(extrair_valor_de_descricao("Alinhamento - 120,00"), 120.0)
    
    def test_valor_sem_centavos(self):
        """Testa extração de valor sem centavos"""
        self.assertEqual(extrair_valor_de_descricao("Troca de pneu - R$ 200"), 200.0)
        
    def test_sem_valor(self):
        """Testa comportamento quando não há valor na descrição"""
        self.assertEqual(extrair_valor_de_descricao("Verificação geral"), 0.0)
        self.assertEqual(extrair_valor_de_descricao(""), 0.0)

if __name__ == '__main__':
    unittest.main()
