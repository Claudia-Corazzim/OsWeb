#!/usr/bin/env python
"""
Script para executar todos os testes do OSweb.
Executa todos os testes unitários e gera um relatório de cobertura se o pacote coverage estiver instalado.
"""

import unittest
import sys
import os

try:
    import coverage
    HAS_COVERAGE = True
except ImportError:
    HAS_COVERAGE = False

def run_tests():
    """Executa todos os testes descobertos no diretório 'tests'"""
    # Encontra todos os testes
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover('tests')
    
    # Executa os testes
    test_runner = unittest.TextTestRunner(verbosity=2)
    result = test_runner.run(test_suite)
    
    # Retorna 0 se todos os testes passaram, 1 se algum falhou
    return 0 if result.wasSuccessful() else 1

def run_tests_with_coverage():
    """Executa os testes com cobertura, se disponível"""
    cov = coverage.Coverage(
        source=['app.py', 'api.py', 'gerar_pdf.py'],
        omit=['tests/*', '*/site-packages/*']
    )
    cov.start()
    
    # Executa os testes
    result = run_tests()
    
    cov.stop()
    cov.save()
    
    print("\nCoverage Summary:")
    cov.report()
    
    print("\nGerando relatório HTML de cobertura...")
    cov.html_report(directory='htmlcov')
    print("Relatório HTML gerado em 'htmlcov/index.html'")
    
    return result

if __name__ == '__main__':
    print("Executando testes para OSweb")
    print("=" * 70)
    
    if HAS_COVERAGE and '--no-coverage' not in sys.argv:
        print("Executando testes com relatório de cobertura")
        result = run_tests_with_coverage()
    else:
        if not HAS_COVERAGE and '--no-coverage' not in sys.argv:
            print("AVISO: Pacote 'coverage' não encontrado. Instale-o com 'pip install coverage'")
            print("Executando testes sem relatório de cobertura")
        result = run_tests()
    
    sys.exit(result)
