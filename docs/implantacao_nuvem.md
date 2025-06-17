# Guia de Implantação na Nuvem - OSweb

Este documento descreve o processo de implantação do sistema OSweb em diferentes plataformas de nuvem para atender ao requisito da UNIVESP de hospedagem em ambiente de nuvem.

## 1. Preparação para Implantação

### 1.1 Requisitos Básicos

Antes de implantar o sistema, certifique-se de que:

- Todos os testes estão passando (`python run_tests.py`)
- O sistema funciona corretamente no ambiente local
- O arquivo `requirements.txt` está atualizado com todas as dependências

### 1.2 Criação do Arquivo `requirements.txt`

Se ainda não existir, crie um arquivo `requirements.txt` com as dependências do projeto:

```bash
pip freeze > requirements.txt
```

Ou crie manualmente com pelo menos:

```
Flask==2.0.1
fpdf==1.7.2
gunicorn==20.1.0
```

### 1.3 Configuração para Ambiente de Produção

Crie um arquivo `config.py` para configurações específicas de cada ambiente:

```python
import os

class Config:
    DEBUG = False
    TESTING = False
    DATABASE = os.environ.get('DATABASE_URL', 'banco.db')

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    pass

class TestingConfig(Config):
    TESTING = True
    DATABASE = 'test_banco.db'

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
```

### 1.4 Ajustes no Arquivo `app.py`

Modifique o arquivo `app.py` para usar as configurações:

```python
import os
from config import config

# Obter configuração com base na variável de ambiente
config_name = os.environ.get('FLASK_ENV', 'default')
app.config.from_object(config[config_name])

# Alterar a execução do app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
```

## 2. Opções de Implantação na Nuvem

### 2.1 Heroku (Opção Gratuita)

#### Pré-requisitos:
- Conta no [Heroku](https://www.heroku.com/)
- [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli) instalado

#### Passos:

1. **Criar arquivo `Procfile`** (sem extensão) na raiz do projeto:

```
web: gunicorn app:app
```

2. **Iniciar repositório Git** (se ainda não existir):

```bash
git init
git add .
git commit -m "Preparação para implantação no Heroku"
```

3. **Criar aplicativo no Heroku**:

```bash
heroku login
heroku create osweb-app
```

4. **Implantar o código**:

```bash
git push heroku main
```

5. **Configurar variáveis de ambiente**:

```bash
heroku config:set FLASK_ENV=production
```

6. **Abrir o aplicativo**:

```bash
heroku open
```

### 2.2 PythonAnywhere (Opção Gratuita)

#### Pré-requisitos:
- Conta no [PythonAnywhere](https://www.pythonanywhere.com/)

#### Passos:

1. **Fazer login no PythonAnywhere**

2. **Criar um Web App**:
   - Escolha "Web" no menu superior
   - Clique em "Add a new web app"
   - Escolha "Flask" e a versão do Python

3. **Configurar arquivos**:
   - Use o botão "Files" para navegar até o diretório do seu aplicativo web
   - Faça upload dos arquivos do projeto usando o uploader
   - Ou use Git para clonar o repositório

4. **Configurar arquivo WSGI**:
   - Edite o arquivo `*.pythonanywhere.com_wsgi.py`
   - Substitua o conteúdo pelo seguinte:

```python
import sys
import os

# Adicionar o diretório do projeto ao path
path = '/home/<seu_username>/osweb'
if path not in sys.path:
    sys.path.append(path)

# Configurar variáveis de ambiente
os.environ['FLASK_ENV'] = 'production'

# Importar o aplicativo Flask
from app import app as application
```

5. **Instalar dependências**:
   - Vá para "Consoles" e inicie um console Bash
   - Navegue até o diretório do projeto
   - Execute `pip install -r requirements.txt`

6. **Reiniciar o aplicativo**:
   - Volte para a seção "Web"
   - Clique no botão "Reload"

### 2.3 Google Cloud Platform (GCP)

#### Pré-requisitos:
- Conta no [Google Cloud Platform](https://cloud.google.com/)
- [Google Cloud SDK](https://cloud.google.com/sdk/docs/install) instalado

#### Passos:

1. **Criar arquivo `app.yaml`**:

```yaml
runtime: python39

handlers:
- url: /static
  static_dir: static
- url: /.*
  script: auto

env_variables:
  FLASK_ENV: "production"
```

2. **Implantar na App Engine**:

```bash
gcloud init
gcloud app deploy
```

3. **Verificar implantação**:

```bash
gcloud app browse
```

### 2.4 Amazon Web Services (AWS) - Elastic Beanstalk

#### Pré-requisitos:
- Conta na [AWS](https://aws.amazon.com/)
- [AWS CLI](https://aws.amazon.com/cli/) e [EB CLI](https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/eb-cli3-install.html) instalados

#### Passos:

1. **Inicializar aplicativo Elastic Beanstalk**:

```bash
eb init -p python-3.8 osweb
```

2. **Criar ambiente**:

```bash
eb create osweb-env
```

3. **Implantar o aplicativo**:

```bash
eb deploy
```

4. **Abrir no navegador**:

```bash
eb open
```

## 3. Gerenciamento de Banco de Dados na Nuvem

### 3.1 SQLite (Solução Simples)

O SQLite funciona para aplicações com baixo tráfego, mas os dados podem ser perdidos em alguns serviços na nuvem que reiniciam frequentemente.

### 3.2 PostgreSQL no Heroku

1. **Adicionar add-on**:

```bash
heroku addons:create heroku-postgresql:hobby-dev
```

2. **Atualizar o código para usar PostgreSQL**:

```python
import os
import psycopg2
from psycopg2.extras import DictCursor

def get_db_connection():
    DATABASE_URL = os.environ.get('DATABASE_URL')
    if DATABASE_URL:
        # Heroku prepends postgresql:// with postgres://
        if DATABASE_URL.startswith("postgres://"):
            DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
        conn = psycopg2.connect(DATABASE_URL)
        conn.cursor_factory = DictCursor
    else:
        # Local SQLite
        conn = sqlite3.connect('banco.db')
        conn.row_factory = sqlite3.Row
    return conn
```

3. **Adicionar `psycopg2` ao `requirements.txt`**:

```
psycopg2-binary==2.9.1
```

### 3.3 MySQL no PythonAnywhere

1. **Criar banco de dados MySQL** na interface do PythonAnywhere

2. **Atualizar o código para usar MySQL**:

```python
import os
import pymysql
import pymysql.cursors

def get_db_connection():
    if 'PYTHONANYWHERE_DOMAIN' in os.environ:
        conn = pymysql.connect(
            host=os.environ.get('MYSQL_HOST', '<seu_username>.mysql.pythonanywhere-services.com'),
            user=os.environ.get('MYSQL_USER', '<seu_username>'),
            password=os.environ.get('MYSQL_PASSWORD', '<sua_senha>'),
            database=os.environ.get('MYSQL_DATABASE', '<seu_username>$osweb'),
            cursorclass=pymysql.cursors.DictCursor
        )
    else:
        # Local SQLite
        conn = sqlite3.connect('banco.db')
        conn.row_factory = sqlite3.Row
    return conn
```

3. **Adicionar `pymysql` ao `requirements.txt`**:

```
PyMySQL==1.0.2
```

## 4. Verificação Pós-Implantação

Após a implantação, verifique:

1. **Funcionalidades básicas**:
   - Acessar todas as páginas principais
   - Adicionar/editar/excluir clientes
   - Criar/editar ordens de serviço
   - Gerar PDFs

2. **Problemas comuns**:
   - Erros de caminho para arquivos estáticos
   - Problemas de conexão com o banco de dados
   - Erros na geração de PDF (permissões ou caminhos)

3. **Logs da aplicação**:
   - Heroku: `heroku logs --tail`
   - PythonAnywhere: Seção "Logs" na interface web
   - GCP: Console do Cloud Logging
   - AWS: Logs do Elastic Beanstalk

## 5. Documentação para UNIVESP

Para documentar a implementação na nuvem para a UNIVESP, inclua:

1. **Descrição da plataforma escolhida**
2. **Capturas de tela do sistema em execução**
3. **URL pública do sistema**
4. **Descrição das configurações realizadas**
5. **Desafios enfrentados e soluções adotadas**

Exemplo de documento:

```markdown
# Documentação de Implantação na Nuvem - OSweb

## Plataforma Utilizada
Sistema implantado no Heroku, plataforma de nuvem que suporta aplicações Python/Flask.

## URL do Sistema
https://osweb-app.herokuapp.com/

## Configurações Realizadas
- Adaptação do banco de dados SQLite para PostgreSQL
- Configuração de variáveis de ambiente
- Implementação de arquivos de configuração para produção
- Configuração do servidor Gunicorn

## Desafios e Soluções
- Problema: Perda de dados após reinicialização do servidor
  Solução: Migração para PostgreSQL persistente
  
- Problema: Caminhos de arquivos na geração de PDF
  Solução: Uso de caminhos relativos e diretórios temporários

## Comprovação de Funcionamento
[Incluir capturas de tela do sistema em execução na nuvem]
```

## 6. Recursos Adicionais

- [Documentação do Flask sobre Implantação](https://flask.palletsprojects.com/en/2.0.x/deploying/)
- [Documentação do Heroku para Python](https://devcenter.heroku.com/categories/python-support)
- [Documentação do PythonAnywhere](https://help.pythonanywhere.com/pages/)
- [Documentação do Google App Engine para Python](https://cloud.google.com/appengine/docs/standard/python3)
- [Documentação do AWS Elastic Beanstalk para Python](https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/create-deploy-python-flask.html)
