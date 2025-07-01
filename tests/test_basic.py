import unittest
from app import app

class TestApp(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_home_status_code(self):
        """Teste da página inicial"""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 302)  # Redirect para /clientes

    def test_clientes_page(self):
        """Teste da página de clientes"""
        response = self.app.get('/clientes')
        self.assertEqual(response.status_code, 200)

    def test_estoque_page(self):
        """Teste da página de estoque"""
        response = self.app.get('/estoque')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
