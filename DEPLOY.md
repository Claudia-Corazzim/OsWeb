# Deploy no Railway - Guia Passo a Passo

## 🚀 Como fazer deploy do OsWeb no Railway

### 1. Preparação do Projeto

O projeto já está configurado com os arquivos necessários:
- `requirements.txt` - Dependências otimizadas para produção
- `railway.json` - Configuração específica do Railway
- `Procfile` - Comando de inicialização alternativo
- `.env.example` - Exemplo de variáveis de ambiente

### 2. Subir o código para o GitHub

```bash
# Se ainda não tem um repositório Git
git init
git add .
git commit -m "Preparar projeto para deploy no Railway"

# Crie um repositório no GitHub e conecte
git remote add origin https://github.com/SEU_USUARIO/SEU_REPOSITORIO.git
git branch -M main
git push -u origin main
```

### 3. Deploy no Railway

1. **Acesse [railway.app](https://railway.app)**
2. **Faça login** com GitHub
3. **Clique em "New Project"**
4. **Selecione "Deploy from GitHub repo"**
5. **Escolha seu repositório OsWeb**
6. **Aguarde o build automático**

### 4. Adicionar PostgreSQL

1. **No dashboard do projeto, clique em "Add Service"**
2. **Selecione "PostgreSQL"**
3. **O Railway criará automaticamente:**
   - Base de dados PostgreSQL
   - Variável `DATABASE_URL` conectada ao app

### 5. Configurar Variáveis de Ambiente

1. **Vá na aba "Variables" do seu app**
2. **Adicione a variável:**
   ```
   SECRET_KEY=sua_chave_secreta_super_segura_aqui_123456789
   ```

### 6. Verificar o Deploy

1. **Vá na aba "Deployments"**
2. **Aguarde o status "Success"**
3. **Clique no link da aplicação** (ex: `https://osweb-production.railway.app`)

### 7. Primeira Execução

Na primeira vez que acessar a aplicação:
1. **As tabelas serão criadas automaticamente**
2. **Você pode começar a cadastrar clientes**
3. **O sistema estará funcionando em produção**

## 🔧 Configurações Avançadas

### Domínio Personalizado
1. Na aba "Settings" do projeto
2. Clique em "Custom Domain"
3. Adicione seu domínio

### Logs da Aplicação
1. Na aba "Deployments"
2. Clique no deployment ativo
3. Veja os logs em tempo real

### Backup do Banco
O Railway faz backup automático do PostgreSQL, mas você pode:
1. Conectar via cliente SQL usando a `DATABASE_URL`
2. Fazer dumps manuais se necessário

## 🚨 Troubleshooting

### Se o deploy falhar:

1. **Verifique os logs** na aba "Deployments"
2. **Problemas comuns:**
   - Dependências em `requirements.txt`
   - Problemas de conexão com PostgreSQL
   - Variáveis de ambiente faltando

### Se a aplicação não carregar:

1. **Verifique se o PostgreSQL está conectado**
2. **Teste a variável DATABASE_URL**
3. **Verifique se a porta está configurada corretamente**

## 💡 Dicas

- **O Railway oferece $5 de créditos gratuitos por mês**
- **PostgreSQL e aplicação contam separadamente**
- **Monitore o uso na aba "Usage"**
- **Configure alertas de limite de gastos**

## 📋 Custos Estimados

- **Hobby Plan**: Grátis até $5/mês
- **PostgreSQL**: ~$5-10/mês dependendo do uso
- **App**: ~$0-5/mês dependendo do tráfego

O projeto é otimizado para usar recursos mínimos na nuvem.

## ✅ Checklist Pré-Deploy

- [ ] Código commitado no GitHub
- [ ] `requirements.txt` atualizado
- [ ] Variáveis de ambiente configuradas
- [ ] Testado localmente
- [ ] Railway conectado ao GitHub
- [ ] PostgreSQL adicionado ao projeto
