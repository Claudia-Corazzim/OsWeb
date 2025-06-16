# Sistema de Gestão de Ordens de Serviço - OsWeb

Um sistema web completo para gerenciamento de ordens de serviço, cadastro de clientes e controle de estoque, desenvolvido com Flask.

![Python](https://img.shields.io/badge/python-3.9+-blue.svg)
![Flask](https://img.shields.io/badge/flask-3.1.1-lightgrey.svg)
![SQLite](https://img.shields.io/badge/sqlite-3-green.svg)

## 📋 Funcionalidades

### Gestão de Clientes
- Cadastro completo de clientes com nome, telefone, email e endereço
- Edição e exclusão de cadastros
- Visualização em lista de todos os clientes

### Ordens de Serviço
- Criação de ordens de serviço vinculadas a clientes
- Registro da descrição do serviço e data
- Edição e exclusão de ordens
- Visualização de todas as ordens em andamento

### Controle de Estoque
- Cadastro de peças com nome e quantidade
- Atualização de quantidades
- Remoção de itens do estoque
- Visualização do inventário completo

## 🚀 Instalação e Execução

### Pré-requisitos
- Python 3.9 ou superior
- pip (gerenciador de pacotes Python)

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

4. Execute a aplicação:
```bash
python app.py
```

5. Acesse no navegador:
```
http://127.0.0.1:5000/
```

## 🛠️ Tecnologias Utilizadas

- **Flask**: Framework web em Python
- **SQLite**: Banco de dados relacional
- **HTML/CSS**: Frontend da aplicação
- **Jinja2**: Engine de templates
- **Git**: Controle de versão

## 📊 Estrutura do Projeto

```
OsWeb/
├── app.py              # Arquivo principal da aplicação
├── requirements.txt    # Dependências do projeto
├── banco.db            # Banco de dados SQLite
├── .gitignore          # Arquivos ignorados pelo Git
└── templates/          # Templates HTML
    ├── clientes.html
    ├── editar_cliente.html
    ├── os.html
    ├── editar_os.html
    ├── estoque.html
    └── editar_peca.html
```

## 🤝 Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues e pull requests.

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---

Desenvolvido por [Claudia Corazzim](https://github.com/Claudia-Corazzim)


# GitHub
- cd "c:\Users\claud\OneDrive\Desktop\OSweb" && git status
- cd "c:\Users\claud\OneDrive\Desktop\OSweb" && git commit -m "Adiciona mensagem de alteração"
- cd "c:\Users\claud\OneDrive\Desktop\OSweb" && git push origin master