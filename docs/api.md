# Documentação da API REST - Sistema de Gestão de Ordens de Serviço

Esta documentação descreve os endpoints disponíveis na API REST do sistema OsWeb, incluindo exemplos de uso e formatos de resposta.

## Endpoints Disponíveis

### Clientes

#### Listar todos os clientes
- **URL**: `/api/clientes`
- **Método**: `GET`
- **Descrição**: Retorna a lista de todos os clientes cadastrados no sistema.
- **Exemplo de resposta**:
```json
[
  {
    "id": 1,
    "nome": "João Silva",
    "telefone": "(11) 99999-9999",
    "email": "joao@exemplo.com",
    "endereco": "Rua A, 123, Centro, São Paulo-SP"
  },
  {
    "id": 2,
    "nome": "Maria Oliveira",
    "telefone": "(21) 88888-8888",
    "email": "maria@exemplo.com",
    "endereco": "Av. B, 456, Jardins, Rio de Janeiro-RJ"
  }
]
```

#### Obter um cliente específico
- **URL**: `/api/clientes/<cliente_id>`
- **Método**: `GET`
- **Descrição**: Retorna os dados de um cliente específico.
- **Parâmetros de URL**:
  - `cliente_id` (obrigatório): ID do cliente
- **Exemplo de resposta**:
```json
{
  "id": 1,
  "nome": "João Silva",
  "telefone": "(11) 99999-9999",
  "email": "joao@exemplo.com",
  "endereco": "Rua A, 123, Centro, São Paulo-SP"
}
```

#### Adicionar um novo cliente
- **URL**: `/api/clientes`
- **Método**: `POST`
- **Descrição**: Adiciona um novo cliente ao sistema.
- **Corpo da requisição**:
```json
{
  "nome": "Pedro Santos",
  "telefone": "(31) 77777-7777",
  "email": "pedro@exemplo.com",
  "endereco": "Rua C, 789, Belo Horizonte-MG"
}
```
- **Exemplo de resposta** (código 201 Created):
```json
{
  "id": 3,
  "nome": "Pedro Santos",
  "telefone": "(31) 77777-7777",
  "email": "pedro@exemplo.com",
  "endereco": "Rua C, 789, Belo Horizonte-MG"
}
```

#### Atualizar um cliente
- **URL**: `/api/clientes/<cliente_id>`
- **Método**: `PUT`
- **Descrição**: Atualiza os dados de um cliente existente.
- **Parâmetros de URL**:
  - `cliente_id` (obrigatório): ID do cliente
- **Corpo da requisição** (campos opcionais):
```json
{
  "telefone": "(31) 66666-6666",
  "email": "pedro.novo@exemplo.com"
}
```
- **Exemplo de resposta**:
```json
{
  "id": 3,
  "nome": "Pedro Santos",
  "telefone": "(31) 66666-6666",
  "email": "pedro.novo@exemplo.com",
  "endereco": "Rua C, 789, Belo Horizonte-MG"
}
```

#### Excluir um cliente
- **URL**: `/api/clientes/<cliente_id>`
- **Método**: `DELETE`
- **Descrição**: Remove um cliente do sistema.
- **Parâmetros de URL**:
  - `cliente_id` (obrigatório): ID do cliente
- **Exemplo de resposta** (código 204 No Content)

### Ordens de Serviço

#### Listar todas as ordens de serviço
- **URL**: `/api/os`
- **Método**: `GET`
- **Descrição**: Retorna a lista de todas as ordens de serviço.
- **Exemplo de resposta**:
```json
[
  {
    "id": 1,
    "cliente_id": 1,
    "cliente_nome": "João Silva",
    "descricao": "Manutenção preventiva",
    "data": "2025-06-15",
    "veiculo": "Fiat Uno",
    "placa": "ABC-1234"
  },
  {
    "id": 2,
    "cliente_id": 2,
    "cliente_nome": "Maria Oliveira",
    "descricao": "Troca de óleo",
    "data": "2025-06-16",
    "veiculo": "Honda Civic",
    "placa": "DEF-5678"
  }
]
```

#### Obter uma ordem de serviço específica
- **URL**: `/api/os/<os_id>`
- **Método**: `GET`
- **Descrição**: Retorna os dados de uma ordem de serviço específica.
- **Parâmetros de URL**:
  - `os_id` (obrigatório): ID da ordem de serviço
- **Exemplo de resposta**:
```json
{
  "id": 1,
  "cliente_id": 1,
  "cliente_nome": "João Silva",
  "descricao": "Manutenção preventiva",
  "data": "2025-06-15",
  "veiculo": "Fiat Uno",
  "placa": "ABC-1234"
}
```

#### Adicionar uma nova ordem de serviço
- **URL**: `/api/os`
- **Método**: `POST`
- **Descrição**: Adiciona uma nova ordem de serviço ao sistema.
- **Corpo da requisição**:
```json
{
  "cliente_id": 3,
  "descricao": "Reparo no motor",
  "data": "2025-06-20",
  "veiculo": "VW Gol",
  "placa": "GHI-9012"
}
```
- **Exemplo de resposta** (código 201 Created):
```json
{
  "id": 3,
  "cliente_id": 3,
  "cliente_nome": "Pedro Santos",
  "descricao": "Reparo no motor",
  "data": "2025-06-20",
  "veiculo": "VW Gol",
  "placa": "GHI-9012"
}
```

#### Atualizar uma ordem de serviço
- **URL**: `/api/os/<os_id>`
- **Método**: `PUT`
- **Descrição**: Atualiza os dados de uma ordem de serviço existente.
- **Parâmetros de URL**:
  - `os_id` (obrigatório): ID da ordem de serviço
- **Corpo da requisição** (campos opcionais):
```json
{
  "descricao": "Reparo no motor e troca de filtro",
  "data": "2025-06-22"
}
```
- **Exemplo de resposta**:
```json
{
  "id": 3,
  "cliente_id": 3,
  "cliente_nome": "Pedro Santos",
  "descricao": "Reparo no motor e troca de filtro",
  "data": "2025-06-22",
  "veiculo": "VW Gol",
  "placa": "GHI-9012"
}
```

#### Excluir uma ordem de serviço
- **URL**: `/api/os/<os_id>`
- **Método**: `DELETE`
- **Descrição**: Remove uma ordem de serviço do sistema.
- **Parâmetros de URL**:
  - `os_id` (obrigatório): ID da ordem de serviço
- **Exemplo de resposta** (código 204 No Content)

### Estoque

#### Listar todos os itens do estoque
- **URL**: `/api/estoque`
- **Método**: `GET`
- **Descrição**: Retorna a lista de todos os itens do estoque.
- **Exemplo de resposta**:
```json
[
  {
    "id": 1,
    "nome": "Óleo de motor",
    "quantidade": 15,
    "valor": 25.90
  },
  {
    "id": 2,
    "nome": "Filtro de ar",
    "quantidade": 8,
    "valor": 35.50
  }
]
```

#### Obter um item específico do estoque
- **URL**: `/api/estoque/<peca_id>`
- **Método**: `GET`
- **Descrição**: Retorna os dados de um item específico do estoque.
- **Parâmetros de URL**:
  - `peca_id` (obrigatório): ID da peça
- **Exemplo de resposta**:
```json
{
  "id": 1,
  "nome": "Óleo de motor",
  "quantidade": 15,
  "valor": 25.90
}
```

#### Adicionar um novo item ao estoque
- **URL**: `/api/estoque`
- **Método**: `POST`
- **Descrição**: Adiciona um novo item ao estoque.
- **Corpo da requisição**:
```json
{
  "nome": "Pastilhas de freio",
  "quantidade": 6,
  "valor": 89.90
}
```
- **Exemplo de resposta** (código 201 Created):
```json
{
  "id": 3,
  "nome": "Pastilhas de freio",
  "quantidade": 6,
  "valor": 89.90
}
```

#### Atualizar um item do estoque
- **URL**: `/api/estoque/<peca_id>`
- **Método**: `PUT`
- **Descrição**: Atualiza os dados de um item existente no estoque.
- **Parâmetros de URL**:
  - `peca_id` (obrigatório): ID da peça
- **Corpo da requisição** (campos opcionais):
```json
{
  "quantidade": 4,
  "valor": 92.50
}
```
- **Exemplo de resposta**:
```json
{
  "id": 3,
  "nome": "Pastilhas de freio",
  "quantidade": 4,
  "valor": 92.50
}
```

#### Excluir um item do estoque
- **URL**: `/api/estoque/<peca_id>`
- **Método**: `DELETE`
- **Descrição**: Remove um item do estoque.
- **Parâmetros de URL**:
  - `peca_id` (obrigatório): ID da peça
- **Exemplo de resposta** (código 204 No Content)

### Consulta de CEP

#### Consultar endereço por CEP
- **URL**: `/api/consulta_cep/<cep>`
- **Método**: `GET`
- **Descrição**: Consulta um endereço a partir do CEP utilizando a API ViaCEP.
- **Parâmetros de URL**:
  - `cep` (obrigatório): CEP a ser consultado (apenas números)
- **Exemplo de resposta**:
```json
{
  "success": true,
  "endereco": {
    "logradouro": "Avenida Paulista",
    "bairro": "Bela Vista",
    "cidade": "São Paulo",
    "estado": "SP",
    "cep": "01310-100"
  }
}
```

## Códigos de Status HTTP

- `200 OK`: Requisição bem-sucedida
- `201 Created`: Recurso criado com sucesso
- `204 No Content`: Requisição bem-sucedida, sem conteúdo para retornar (normalmente usado em exclusões)
- `400 Bad Request`: Erro na requisição (dados inválidos)
- `404 Not Found`: Recurso não encontrado
- `500 Internal Server Error`: Erro interno do servidor

## Como Consumir a API

### Exemplos com cURL

#### Listar todos os clientes:
```bash
curl -X GET http://localhost:5000/api/clientes
```

#### Adicionar um novo cliente:
```bash
curl -X POST http://localhost:5000/api/clientes \
  -H "Content-Type: application/json" \
  -d '{"nome": "Ana Souza", "telefone": "(41) 55555-5555", "email": "ana@exemplo.com", "endereco": "Rua D, 321, Curitiba-PR"}'
```

### Exemplos com JavaScript (Fetch API)

#### Listar todos os clientes:
```javascript
fetch('http://localhost:5000/api/clientes')
  .then(response => response.json())
  .then(data => console.log(data))
  .catch(error => console.error('Erro:', error));
```

#### Adicionar um novo cliente:
```javascript
fetch('http://localhost:5000/api/clientes', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    nome: "Ana Souza", 
    telefone: "(41) 55555-5555", 
    email: "ana@exemplo.com", 
    endereco: "Rua D, 321, Curitiba-PR"
  }),
})
.then(response => response.json())
.then(data => console.log(data))
.catch(error => console.error('Erro:', error));
```
