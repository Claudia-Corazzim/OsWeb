# Configuração para Deploy

Este arquivo contém instruções para o deploy do sistema em diferentes ambientes de produção.

## Deploy no Heroku

### Pré-requisitos
- Conta no [Heroku](https://www.heroku.com/)
- [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli) instalado
- Git instalado

### Passos para deploy

1. Faça login no Heroku via CLI:
```bash
heroku login
```

2. Crie um aplicativo no Heroku:
```bash
heroku create osweb-app
```

3. Adicione um arquivo `Procfile` na raiz do projeto:
```
web: gunicorn app:app
```

4. Verifique se `gunicorn` está nas dependências em `requirements.txt`. Se não estiver, adicione:
```
gunicorn==21.2.0
```

5. Realize o commit das alterações:
```bash
git add Procfile requirements.txt
git commit -m "Configuração para deploy no Heroku"
```

6. Faça o deploy:
```bash
git push heroku master
```

7. Abra o aplicativo:
```bash
heroku open
```

## Deploy na AWS (Elastic Beanstalk)

### Pré-requisitos
- Conta na [AWS](https://aws.amazon.com/)
- [AWS CLI](https://aws.amazon.com/cli/) instalado
- [EB CLI](https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/eb-cli3-install.html) instalado

### Passos para deploy

1. Inicialize o aplicativo Elastic Beanstalk:
```bash
eb init -p python-3.9 osweb
```

2. Crie um ambiente e faça o deploy:
```bash
eb create osweb-env
```

3. Quando o ambiente estiver pronto, acesse a URL fornecida:
```bash
eb open
```

## Deploy em VPS/Servidor Próprio (usando Nginx e Gunicorn)

### Pré-requisitos
- Servidor Linux (Ubuntu/Debian recomendado)
- Nginx instalado
- Python 3.9+ instalado

### Passos para deploy

1. Clone o repositório no servidor:
```bash
git clone https://github.com/Claudia-Corazzim/OsWeb.git
cd OsWeb
```

2. Crie e ative um ambiente virtual:
```bash
python3 -m venv venv
source venv/bin/activate
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
pip install gunicorn
```

4. Teste a aplicação com Gunicorn:
```bash
gunicorn -w 4 -b 127.0.0.1:8000 app:app
```

5. Configure o serviço systemd para gerenciar o Gunicorn:
Crie o arquivo `/etc/systemd/system/osweb.service`:

```ini
[Unit]
Description=OsWeb Gunicorn Service
After=network.target

[Service]
User=ubuntu
Group=ubuntu
WorkingDirectory=/home/ubuntu/OsWeb
ExecStart=/home/ubuntu/OsWeb/venv/bin/gunicorn -w 4 -b 127.0.0.1:8000 app:app
Restart=always

[Install]
WantedBy=multi-user.target
```

6. Inicie e habilite o serviço:
```bash
sudo systemctl start osweb
sudo systemctl enable osweb
```

7. Configure o Nginx:
Crie o arquivo `/etc/nginx/sites-available/osweb`:

```nginx
server {
    listen 80;
    server_name your_domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /static {
        alias /home/ubuntu/OsWeb/static;
    }
}
```

8. Habilite o site e reinicie o Nginx:
```bash
sudo ln -s /etc/nginx/sites-available/osweb /etc/nginx/sites-enabled/
sudo systemctl restart nginx
```

9. Configure o firewall:
```bash
sudo ufw allow 'Nginx Full'
```

## Considerações de Segurança

1. **Banco de Dados**: Em produção, considere usar um banco de dados mais robusto como PostgreSQL ou MySQL.

2. **Variáveis de Ambiente**: Use variáveis de ambiente para armazenar informações sensíveis.
   Crie um arquivo `.env` na raiz do projeto (não incluído no controle de versão) e use a biblioteca `python-dotenv`.

3. **HTTPS**: Configure HTTPS usando Let's Encrypt para garantir conexões seguras.

4. **Backups**: Configure backups regulares do banco de dados.

## Monitoramento

Para monitoramento da aplicação em produção, considere:

1. **Logging**: Configure logs adequados e considere serviços como Papertrail ou ELK Stack.

2. **Métricas de Desempenho**: Use ferramentas como New Relic, Datadog ou Prometheus.

3. **Monitoramento de Disponibilidade**: Configure alertas usando ferramentas como UptimeRobot ou Pingdom.
