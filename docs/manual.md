# Manual do Usuário - Sistema de Gestão de Ordens de Serviço

Este manual contém instruções detalhadas sobre como utilizar todas as funcionalidades do sistema OsWeb.

## Índice

1. [Visão Geral](#visão-geral)
2. [Acesso ao Sistema](#acesso-ao-sistema)
3. [Gestão de Clientes](#gestão-de-clientes)
4. [Gestão de Ordens de Serviço](#gestão-de-ordens-de-serviço)
5. [Controle de Estoque](#controle-de-estoque)
6. [Dicas e Truques](#dicas-e-truques)
7. [Solução de Problemas](#solução-de-problemas)

## Visão Geral

O Sistema de Gestão de Ordens de Serviço (OsWeb) é uma aplicação web desenvolvida para facilitar o gerenciamento de clientes, ordens de serviço e estoque em oficinas mecânicas, assistências técnicas e empresas de prestação de serviços em geral.

### Principais Recursos

- Cadastro e gerenciamento de clientes
- Criação e acompanhamento de ordens de serviço
- Controle de estoque de peças e produtos
- Geração de PDF das ordens de serviço
- Consulta automática de endereço por CEP

## Acesso ao Sistema

Para acessar o sistema, abra um navegador web e digite o endereço onde o sistema está hospedado. Localmente, o endereço será:

```
http://127.0.0.1:5000/
```

A navegação principal é feita através do menu superior, que contém links para as três áreas principais do sistema:

- **Clientes**: Gerenciamento do cadastro de clientes
- **Ordens de Serviço**: Criação e acompanhamento de ordens de serviço
- **Estoque**: Controle de peças e produtos

## Gestão de Clientes

### Visualização de Clientes

A página inicial de clientes mostra uma tabela com todos os clientes cadastrados, exibindo as seguintes informações:

- ID
- Nome
- Telefone
- Email
- Endereço

Você pode usar o campo de busca acima da tabela para filtrar os clientes por qualquer uma dessas informações.

### Adição de Novos Clientes

Para adicionar um novo cliente:

1. Preencha o formulário "Adicionar Cliente" com:
   - Nome (obrigatório)
   - Telefone (obrigatório)
   - Email (obrigatório)
   - CEP (opcional, mas recomendado)
   
2. Ao preencher o CEP e pressionar Tab ou clicar fora do campo, o sistema buscará automaticamente as informações de endereço.

3. Complete os campos restantes:
   - Número (obrigatório)
   - Complemento (opcional)

4. Clique no botão "Adicionar".

### Edição de Clientes

Para editar as informações de um cliente:

1. Na tabela de clientes, clique no botão "Editar" na linha correspondente ao cliente.
2. O sistema abrirá um formulário preenchido com as informações atuais do cliente.
3. Modifique os campos necessários.
4. Clique em "Salvar Alterações" para confirmar ou "Cancelar" para descartar as mudanças.

### Exclusão de Clientes

Para excluir um cliente:

1. Na tabela de clientes, clique no botão "Excluir" na linha correspondente ao cliente.
2. O sistema exibirá uma caixa de diálogo de confirmação.
3. Clique em "OK" para confirmar a exclusão ou "Cancelar" para manter o cliente.

**Atenção**: A exclusão de um cliente removerá também todas as ordens de serviço associadas a ele. Esta ação não pode ser desfeita.

## Gestão de Ordens de Serviço

### Visualização de Ordens de Serviço

A página de ordens de serviço exibe uma tabela com todas as ordens cadastradas, mostrando:

- ID
- Cliente
- Descrição
- Data
- Veículo
- Placa
- Ações (Editar, Excluir, Gerar PDF)

### Criação de Nova Ordem de Serviço

Para criar uma nova ordem de serviço:

1. Preencha o formulário "Adicionar Ordem de Serviço":
   - Cliente (selecione da lista)
   - Descrição do serviço
   - Data
   - Veículo (opcional)
   - Placa (opcional)

2. Clique em "Adicionar".

### Edição de Ordem de Serviço

Para editar uma ordem de serviço:

1. Na tabela de ordens, clique no botão "Editar" na linha correspondente.
2. Modifique os campos necessários.
3. Clique em "Salvar Alterações".

### Geração de PDF

Para gerar um PDF da ordem de serviço:

1. Na tabela de ordens, clique no botão "PDF" na linha correspondente.
2. O sistema gerará e fará o download automático do arquivo PDF.

O PDF contém:
- Logo e informações da empresa
- Número da ordem de serviço
- Data
- Dados do cliente
- Informações do veículo
- Descrição do serviço
- Espaço para assinaturas

## Controle de Estoque

### Visualização do Estoque

A página de estoque mostra uma tabela com todas as peças e produtos cadastrados, exibindo:

- ID
- Nome
- Quantidade
- Valor
- Ações (Editar, Excluir)

### Adição de Nova Peça

Para adicionar uma nova peça ao estoque:

1. Preencha o formulário "Adicionar Peça":
   - Nome (obrigatório)
   - Quantidade (obrigatório)
   - Valor (opcional)

2. Clique em "Adicionar".

### Edição de Peça

Para editar uma peça no estoque:

1. Na tabela de estoque, clique no botão "Editar" na linha correspondente.
2. Modifique os campos necessários.
3. Clique em "Salvar Alterações".

### Exclusão de Peça

Para excluir uma peça do estoque:

1. Na tabela de estoque, clique no botão "Excluir" na linha correspondente.
2. Confirme a exclusão na caixa de diálogo que aparecerá.

## Dicas e Truques

### Busca Rápida

Todas as tabelas do sistema possuem um campo de busca que permite filtrar rapidamente os registros. A busca é realizada em todos os campos visíveis da tabela.

### Consulta de CEP

Ao cadastrar ou editar um cliente, utilize a funcionalidade de consulta de CEP para preencher automaticamente os campos de endereço:

1. Digite o CEP no campo correspondente.
2. Pressione a tecla Tab ou clique fora do campo.
3. Os campos de logradouro, bairro, cidade e estado serão preenchidos automaticamente.
4. Complete apenas o número e complemento, se necessário.

### Validação de Formulários

O sistema valida automaticamente os formulários antes do envio:

- Campos obrigatórios não podem estar vazios
- Emails devem estar em formato válido
- Telefones devem seguir o padrão (XX) XXXXX-XXXX

## Solução de Problemas

### O sistema não encontra o CEP informado

**Possíveis causas e soluções:**
- Verifique se o CEP está correto
- Verifique sua conexão com a internet
- O serviço de CEP pode estar temporariamente indisponível. Tente novamente mais tarde.
- Preencha o endereço manualmente se o problema persistir.

### O PDF não é gerado

**Possíveis causas e soluções:**
- Verifique se o cliente possui todas as informações obrigatórias
- Certifique-se de que a descrição do serviço foi preenchida
- Tente recarregar a página e gerar o PDF novamente

### O sistema está lento

**Possíveis causas e soluções:**
- Muitos registros podem tornar as consultas mais lentas
- Utilize os filtros de busca para limitar a quantidade de registros exibidos
- Feche outras abas ou aplicativos que possam estar consumindo recursos do computador

Para problemas não listados aqui, entre em contato com o suporte técnico.
