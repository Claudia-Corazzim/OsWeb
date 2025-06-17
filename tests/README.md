# Guia de Execução de Testes - OSweb

Este guia descreve como executar os testes automatizados e manuais para o sistema OSweb.

## Testes Automatizados

### Requisitos

- Python 3.6 ou superior
- Flask
- SQLite3
- FPDF
- Unittest (embutido no Python)

### Executando Todos os Testes

Para executar todos os testes automatizados de uma vez, use o seguinte comando no terminal:

```bash
python -m unittest discover -s tests
```

Este comando procurará todos os arquivos de teste no diretório `tests` e os executará.

### Executando Testes Específicos

Para executar um arquivo de teste específico:

```bash
# Teste de extração de valor
python -m unittest tests.test_extracao_valor

# Teste de banco de dados
python -m unittest tests.test_database

# Teste da aplicação web
python -m unittest tests.test_app

# Teste da API REST
python -m unittest tests.test_api

# Teste de geração de PDF
python -m unittest tests.test_pdf
```

Para executar um método de teste específico:

```bash
python -m unittest tests.test_extracao_valor.TestExtracaoValor.test_valor_com_r_cifrão
```

### Verificação de Cobertura

Para verificar a cobertura dos testes, instale o pacote `coverage`:

```bash
pip install coverage
```

Em seguida, execute os testes com o coverage:

```bash
coverage run -m unittest discover -s tests
```

E gere um relatório:

```bash
coverage report
```

Para um relatório HTML mais detalhado:

```bash
coverage html
```

Os relatórios HTML serão gerados em uma pasta chamada `htmlcov`.

## Testes Manuais

Para os testes manuais, siga o roteiro detalhado em `tests/testes_manuais.md`, que inclui:

1. Testes de Funcionalidades do Cliente
2. Testes de Ordens de Serviço
3. Testes de Acessibilidade
4. Testes de Responsividade
5. Testes de API

### Executando o Aplicativo para Testes Manuais

Para executar o aplicativo para realizar testes manuais:

```bash
python app.py
```

O aplicativo estará disponível em `http://localhost:5000`.

## Registro de Resultados

Ao executar os testes, é importante registrar:

1. Data e hora da execução
2. Ambiente de teste (sistema operacional, versão do Python, etc.)
3. Número total de testes executados
4. Número de testes bem-sucedidos
5. Número de falhas
6. Descrição das falhas encontradas
7. Ações corretivas tomadas

Mantenha um registro desses resultados para acompanhar o progresso do desenvolvimento e garantir que as correções não introduzam novas falhas.

## Solução de Problemas Comuns

### Erro ao Conectar ao Banco de Dados

Se ocorrerem erros de conexão com o banco de dados durante os testes, verifique:
- Se o arquivo do banco de dados existe
- Se as permissões de acesso estão corretas
- Se o caminho do arquivo está correto

### Falhas em Testes de API

Para testes de API que falham:
- Verifique se a API está sendo inicializada corretamente nos testes
- Confirme se os formatos de dados esperados estão corretos
- Verifique se as rotas da API estão corretas

### Falhas em Testes de PDF

Para testes de PDF que falham:
- Verifique se a biblioteca FPDF está instalada corretamente
- Certifique-se de que o diretório de armazenamento temporário tem permissões de escrita
- Confirme se os arquivos de recursos (como logos) estão no caminho esperado
