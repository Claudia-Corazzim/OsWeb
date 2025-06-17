# Plano de Testes para OSweb

Este documento descreve um plano de testes abrangente para o sistema OSweb, incluindo testes automatizados e manuais.

## 1. Testes Unitários

### 1.1 Função de Extração de Valor (`test_extracao_valor.py`)

✅ **Já implementado:**
- Teste para extração de valor com formato R$ XX,XX
- Teste para extração de valor sem o R$
- Teste para extração de valor sem centavos
- Teste para comportamento quando não há valor na descrição

### 1.2 Banco de Dados (`test_database.py`)

✅ **Já implementado:**
- Teste de inserção de cliente
- Teste de inserção de ordem de serviço
- Teste de inserção de serviços

**Testes adicionais sugeridos:**
- Teste de atualização de cliente
- Teste de atualização de ordem de serviço
- Teste de exclusão de cliente
- Teste de exclusão de ordem de serviço
- Teste de exclusão de serviço
- Teste de consulta de cliente por ID
- Teste de consulta de ordem de serviço por ID
- Teste de consulta de serviços por ordem de serviço ID

### 1.3 Aplicação Web (`test_app.py`)

✅ **Já implementado:**
- Teste de acesso à página de clientes
- Teste de adição de cliente
- Teste de acesso à página de ordens de serviço
- Teste de acesso à página de estoque
- Teste de API de listagem de clientes
- Teste de API de criação de cliente
- Teste de consulta de CEP

**Testes adicionais sugeridos:**
- Teste de adição de ordem de serviço
- Teste de edição de ordem de serviço
- Teste de exclusão de ordem de serviço
- Teste de geração de PDF
- Teste de listagem de serviços via API
- Teste de adição de serviço via API
- Teste de edição de serviço via API

### 1.4 API REST (`test_api.py`)

**Testes sugeridos:**
- Teste de obtenção da lista de clientes
- Teste de obtenção de um cliente específico
- Teste de criação de cliente
- Teste de atualização de cliente
- Teste de exclusão de cliente
- Teste de obtenção da lista de ordens de serviço
- Teste de obtenção de uma ordem de serviço específica
- Teste de criação de ordem de serviço
- Teste de atualização de ordem de serviço
- Teste de exclusão de ordem de serviço
- Teste de obtenção de serviços de uma ordem de serviço
- Teste de adição de serviço a uma ordem de serviço
- Teste de atualização de serviço
- Teste de exclusão de serviço

### 1.5 Geração de PDF (`test_pdf.py`)

**Testes sugeridos:**
- Teste de geração de PDF para uma ordem de serviço com um serviço
- Teste de geração de PDF para uma ordem de serviço com múltiplos serviços
- Teste de geração de PDF com informações de cliente
- Teste de formatação correta do PDF

## 2. Testes de Integração

### 2.1 Fluxo Completo de Ordem de Serviço

**Testes sugeridos:**
- Teste de criação de cliente, seguido de criação de ordem de serviço e adição de serviços
- Teste de edição de ordem de serviço com alteração de serviços
- Teste de consulta e exclusão de ordem de serviço

### 2.2 Integração com API Externa

✅ **Já implementado:**
- Teste de consulta de CEP

**Testes adicionais sugeridos:**
- Teste de comportamento do sistema quando a API externa está indisponível
- Teste de validação de dados da API externa

## 3. Testes de Interface do Usuário

### 3.1 Testes de Acessibilidade

✅ **Já documentado em testes manuais:**
- Navegação por teclado
- Compatibilidade com leitor de tela

**Testes adicionais sugeridos:**
- Teste de contraste de cores
- Teste de redimensionamento de texto
- Teste de alternativas textuais para imagens

### 3.2 Testes de Responsividade

✅ **Já documentado em testes manuais:**
- Visualização em dispositivos móveis

**Testes adicionais sugeridos:**
- Teste em diferentes navegadores (Chrome, Firefox, Safari, Edge)
- Teste em diferentes tamanhos de tela (desktop, tablet, smartphone)

## 4. Testes de Desempenho

**Testes sugeridos:**
- Teste de carga para simulação de múltiplos usuários simultâneos
- Teste de tempo de resposta para operações comuns
- Teste de comportamento com banco de dados grande

## 5. Testes de Segurança

**Testes sugeridos:**
- Teste de validação de entrada
- Teste de proteção contra injeção SQL
- Teste de proteção contra XSS (Cross-Site Scripting)
- Teste de autenticação e autorização (se implementados)

## 6. Testes de Usabilidade

**Testes sugeridos:**
- Avaliação de usabilidade com usuários reais
- Teste de fluxos de trabalho comuns
- Avaliação de mensagens de erro e feedback

## 7. Execução dos Testes

### 7.1 Testes Unitários e de Integração Automatizados

Para executar os testes automatizados:

```bash
# Executar todos os testes
python -m unittest discover -s tests

# Executar um teste específico
python -m unittest tests.test_extracao_valor
python -m unittest tests.test_database
python -m unittest tests.test_app
```

### 7.2 Testes Manuais

Seguir os procedimentos documentados em `tests/testes_manuais.md` para:
- Testes de funcionalidades do cliente
- Testes de ordens de serviço
- Testes de acessibilidade
- Testes de responsividade
- Testes de API

## 8. Relatórios de Teste

Ao executar os testes, documentar:
- Número total de testes executados
- Número de testes bem-sucedidos
- Número de falhas
- Descrição das falhas encontradas
- Ações corretivas tomadas

## 9. Critérios de Aceitação

- Todos os testes unitários devem passar
- Todos os testes de integração devem passar
- Pelo menos 90% dos testes manuais devem passar
- Não deve haver erros críticos ou bloqueadores
- O sistema deve atender a todos os requisitos da UNIVESP
