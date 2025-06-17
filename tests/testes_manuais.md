# Procedimentos de Teste Manual para OSweb

Este documento descreve os procedimentos de teste manual para o sistema OSweb.

## 1. Testes de Funcionalidades do Cliente

### 1.1 Adicionar Cliente

**Objetivo**: Verificar se um novo cliente pode ser adicionado ao sistema.

**Passos**:
1. Acesse a página Clientes (/clientes)
2. Preencha o formulário com os seguintes dados:
   - Nome: Cliente Teste
   - Telefone: (11) 98765-4321
   - Email: cliente.teste@exemplo.com
   - Endereço: Rua de Teste, 123
3. Clique no botão "Adicionar"

**Resultado Esperado**:
- O cliente deve aparecer na lista de clientes
- Não deve ocorrer erros
- A página deve permanecer na tela de clientes

### 1.2 Editar Cliente

**Objetivo**: Verificar se um cliente existente pode ser editado.

**Passos**:
1. Acesse a página Clientes (/clientes)
2. Clique no botão "Editar" ao lado de um cliente existente
3. Modifique o telefone para "(11) 91234-5678"
4. Clique em "Salvar"

**Resultado Esperado**:
- As alterações devem ser salvas
- Ao retornar à lista de clientes, o telefone atualizado deve ser exibido

### 1.3 Excluir Cliente

**Objetivo**: Verificar se um cliente pode ser excluído.

**Passos**:
1. Acesse a página Clientes (/clientes)
2. Clique no botão "Excluir" ao lado de um cliente existente
3. Confirme a exclusão

**Resultado Esperado**:
- O cliente deve ser removido da lista
- Não deve ocorrer erros

## 2. Testes de Ordens de Serviço

### 2.1 Criar Nova OS

**Objetivo**: Verificar se uma nova ordem de serviço pode ser criada.

**Passos**:
1. Acesse a página Ordens de Serviço (/ordens_servico)
2. Selecione um cliente existente no menu suspenso
3. Preencha:
   - Veículo: Fiat Uno
   - Placa: ABC-1234
   - Data: hoje
4. Adicione um serviço com descrição "Troca de óleo - R$ 50,00"
5. Adicione outro serviço com descrição "Filtro de ar - R$ 30,00"
6. Digite alguma observação: "Cliente solicitou urgência"
7. Clique em "Adicionar"

**Resultado Esperado**:
- A OS deve ser criada e aparecer na lista
- Os serviços devem ser registrados corretamente
- O valor total deve ser calculado automaticamente (R$ 80,00)

### 2.2 Editar OS

**Objetivo**: Verificar se uma OS existente pode ser editada.

**Passos**:
1. Acesse a página Ordens de Serviço (/ordens_servico)
2. Clique no botão "Editar" ao lado de uma OS existente
3. Adicione um novo serviço: "Verificação de suspensão - R$ 45,00"
4. Modifique a observação
5. Clique em "Salvar Alterações"

**Resultado Esperado**:
- As alterações devem ser salvas
- O valor total deve ser atualizado para incluir o novo serviço
- A lista de OS deve mostrar as informações atualizadas

### 2.3 Gerar PDF

**Objetivo**: Verificar se um PDF da OS pode ser gerado.

**Passos**:
1. Acesse a página Ordens de Serviço (/ordens_servico)
2. Clique no botão "PDF" ao lado de uma OS existente

**Resultado Esperado**:
- Um PDF deve ser gerado e baixado ou aberto em uma nova aba
- O PDF deve conter:
  - Informações do cliente
  - Detalhes da OS
  - Lista de serviços com valores
  - Valor total
  - Espaço para assinaturas

## 3. Testes de Acessibilidade

### 3.1 Navegação por Teclado

**Objetivo**: Verificar se o sistema pode ser navegado usando apenas o teclado.

**Passos**:
1. Acesse a página inicial
2. Use a tecla Tab para navegar entre elementos
3. Use Enter para ativar links e botões
4. Tente preencher um formulário usando apenas o teclado

**Resultado Esperado**:
- Deve ser possível navegar por todo o sistema usando apenas o teclado
- O foco deve ser visível em todos os elementos
- Todos os elementos interativos devem ser acessíveis

### 3.2 Compatibilidade com Leitor de Tela

**Objetivo**: Verificar se o sistema é compatível com leitores de tela.

**Passos**:
1. Ative um leitor de tela (NVDA, VoiceOver ou similar)
2. Navegue pelo sistema usando as teclas padrão do leitor de tela
3. Verifique se todos os elementos têm descrições adequadas

**Resultado Esperado**:
- Todos os elementos devem ser anunciados corretamente
- Formulários devem ter labels associados
- Mensagens de erro devem ser anunciadas
- Mudanças dinâmicas na página devem ser anunciadas

## 4. Testes de Responsividade

### 4.1 Visualização em Dispositivos Móveis

**Objetivo**: Verificar se o sistema se adapta a telas pequenas.

**Passos**:
1. Acesse o sistema em um smartphone ou use as ferramentas de desenvolvedor do navegador para simular uma tela pequena
2. Navegue pelas diferentes páginas e formulários

**Resultado Esperado**:
- O layout deve se adaptar à tela menor
- Os textos devem ser legíveis
- Os botões e campos devem ser grandes o suficiente para tocar
- Não deve haver rolagem horizontal

## 5. Testes de API

### 5.1 Listar Clientes via API

**Objetivo**: Verificar se a API retorna a lista de clientes.

**Passos**:
1. Acesse /api/clientes em um navegador ou ferramenta como Postman
2. Verifique a resposta JSON

**Resultado Esperado**:
- A API deve retornar um array JSON com os clientes
- O status HTTP deve ser 200 OK

### 5.2 Obter OS via API

**Objetivo**: Verificar se a API retorna os detalhes de uma OS específica.

**Passos**:
1. Acesse /api/os/{id} substituindo {id} por um ID válido de OS
2. Verifique a resposta JSON

**Resultado Esperado**:
- A API deve retornar os detalhes da OS em formato JSON
- Os serviços associados devem estar incluídos
- O status HTTP deve ser 200 OK
