# Sistema de Gestão de Ordens de Serviço - OsWeb

Um sistema web completo para gerenciamento de ordens de serviço, cadastro de clientes e controle de estoque, desenvolvido com Flask.

![Python](https://img.shields.io/badge/python-3.9+-blue.svg)
![Flask](https://img.shields.io/badge/flask-3.1.1-lightgrey.svg)
![PostgreSQL](https://img.shields.io/badge/postgresql-17-blue.svg)

## 📋 Funcionalidades

### Gestão de Clientes
- Cadastro completo de clientes com nome, telefone, email e endereço
- Consulta automática de endereço por CEP
- Edição e exclusão de cadastros
- Validação de formulários
- Visualização em lista de todos os clientes

### Ordens de Serviço
- Criação de ordens de serviço vinculadas a clientes
- Registro da descrição do serviço, data, veículo e placa
- Geração de PDF da ordem de serviço com logo e dados da empresa
- Edição e exclusão de ordens
- Visualização de todas as ordens em andamento

### Controle de Estoque
- Cadastro de peças com nome, quantidade e valor
- Atualização de quantidades
- Remoção de itens do estoque
- Visualização do inventário completo

### API RESTful
- Endpoints para operações CRUD em clientes, ordens de serviço e estoque
- Integração com API externa de consulta de CEP
- Documentação completa dos endpoints disponíveis

### Recursos de UX/UI
- Validação de formulários com feedback visual
- Máscaras para campos de telefone, documentos e CEP
- Filtros de busca em tabelas
- Confirmação de exclusão de registros
- Recursos de acessibilidade (ARIA, navegação por teclado)

## 🚀 Instalação e Execução

### Pré-requisitos
- Python 3.9 ou superior
- pip (gerenciador de pacotes Python)
- PostgreSQL 17 ou superior

### Passos para instalação

1. Clone o repositório:
```bash
git clone https://github.com/Claudia-Corazzim/OsWeb.git
cd OsWeb
```

2. Crie e ative um ambiente virtual:
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Configure o PostgreSQL:
```bash
# Criar usuário e banco de dados
psql -U postgres
CREATE USER admin WITH PASSWORD 'admin' SUPERUSER;
CREATE DATABASE osweb OWNER admin;
```

5. Execute a aplicação:
```bash
python app.py
```

6. Acesse no navegador:
```
http://127.0.0.1:5000/
```

## 🧪 Testes

O sistema inclui testes automatizados para garantir o funcionamento correto:

```bash
# Executar todos os testes
python -m unittest discover -s tests

# Executar um teste específico
python -m unittest tests.test_app
```

## 📚 Documentação

A documentação completa do sistema está disponível nos seguintes arquivos:

- [Documentação da API REST](docs/api.md)
- [Guia de Implantação](docs/deploy.md)
- [Manual do Usuário](docs/manual.md)

## 🛠️ Tecnologias Utilizadas

- **Backend**:
  - Flask: Framework web em Python
  - PostgreSQL: Banco de dados relacional
  - psycopg2: Driver PostgreSQL para Python
  - Flask-RESTful: Criação de API REST
  - FPDF: Geração de arquivos PDF

- **Frontend**:
  - HTML/CSS: Estrutura e estilo das páginas
  - JavaScript: Interatividade, validação e consumo de API
  - Jinja2: Engine de templates do Flask

- **Integração e Ferramentas**:
  - Git: Controle de versão
  - Requests: Consumo de APIs externas
  - Unittest: Framework de testes

## 📊 Estrutura do Projeto

```
OsWeb/
├── app.py                 # Arquivo principal da aplicação
├── requirements.txt       # Dependências do projeto
├── .gitignore            # Arquivos ignorados pelo Git
├── README.md             # Documentação principal
├── static/               # Arquivos estáticos
│   ├── css/              # Estilos CSS
│   ├── js/               # Scripts JavaScript
│   └── img/              # Imagens e logos
├── templates/            # Templates HTML
│   ├── base.html         # Template base
│   ├── clientes.html     # Gestão de clientes
│   ├── os.html           # Gestão de ordens de serviço
│   ├── estoque.html      # Gestão de estoque
│   └── ...               # Outros templates
├── api/                  # Módulos da API REST
│   ├── __init__.py       # Inicialização da API
│   ├── resources.py      # Recursos da API
│   └── external.py       # Integrações com APIs externas
├── docs/                 # Documentação
│   ├── api.md            # Documentação da API
│   ├── deploy.md         # Guia de implantação
│   └── manual.md         # Manual do usuário
└── tests/               # Testes automatizados
    └── test_app.py      # Testes da aplicação
```
## GiTHub
- git status
- git add .
- git commit -m "mensagem"
- git push origin master


## 🤝 Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues e pull requests.

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---

Desenvolvido por [Claudia Corazzim](https://github.com/Claudia-Corazzim)
