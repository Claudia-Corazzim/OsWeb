# Interpretação dos Resultados de Testes - OSweb

Este documento oferece orientações sobre como interpretar os resultados dos testes automatizados do sistema OSweb.

## Testes Unitários

### Resultados dos Testes

Ao executar os testes unitários com o comando `python -m unittest discover -s tests` ou `python run_tests.py`, você verá uma saída semelhante a esta:

```
...............F.............
======================================================================
FAIL: test_consulta_cep (tests.test_app.FlaskTestCase)
Testa a consulta de CEP
----------------------------------------------------------------------
Traceback (most recent call last):
  File "...\tests\test_app.py", line 89, in test_consulta_cep
    self.assertIn('endereco', data)
AssertionError: 'endereco' not found in {'cep': '01001-000', 'logradouro': 'Praça da Sé', ...}
----------------------------------------------------------------------
Ran 28 tests in 3.214s

FAILED (failures=1)
```

**Como interpretar:**

- Cada ponto (`.`) representa um teste que passou com sucesso.
- `F` indica um teste que falhou.
- `E` indica um erro durante a execução do teste.
- `s` indica um teste que foi pulado.

Após a execução, você verá um resumo dos testes que falharam ou causaram erros, com a localização exata e a razão da falha.

### Relatório de Cobertura

Se você executar os testes com cobertura (usando `coverage run -m unittest discover -s tests` ou `python run_tests.py`), você verá um relatório como este:

```
Name       Stmts   Miss  Cover
------------------------------
app.py       325     78    76%
api.py        42      7    83%
gerar_pdf.py  21      2    90%
------------------------------
TOTAL        388     87    78%
```

**Como interpretar:**

- **Stmts**: Número total de declarações no código.
- **Miss**: Número de declarações que não foram executadas pelos testes.
- **Cover**: Porcentagem de código coberto pelos testes.

Uma cobertura acima de 70-80% é geralmente considerada boa para projetos em desenvolvimento.

## Tipos Comuns de Falhas e Como Corrigi-las

### 1. AssertionError

```
AssertionError: 'endereco' not found in {'cep': '01001-000', ...}
```

**Causa**: O teste esperava encontrar uma chave 'endereco' em um dicionário, mas ela não estava presente.

**Solução**: 
- Verifique se a API externa mudou seu formato de resposta.
- Atualize o código para usar a nova estrutura de dados.
- Ou atualize o teste para verificar a chave correta.

### 2. TypeError

```
TypeError: 'NoneType' object is not subscriptable
```

**Causa**: O código está tentando acessar um elemento de um objeto que é None.

**Solução**:
- Verifique se uma consulta ao banco de dados está retornando resultados.
- Adicione verificações para None antes de acessar propriedades.

### 3. ImportError

```
ImportError: No module named 'some_module'
```

**Causa**: Um módulo necessário não está instalado ou não está no PYTHONPATH.

**Solução**:
- Instale o pacote necessário com pip.
- Verifique se o módulo está no local correto.

### 4. DatabaseError

```
sqlite3.OperationalError: no such table: clientes
```

**Causa**: A tabela esperada não existe no banco de dados de teste.

**Solução**:
- Verifique se a função de criação de tabelas está sendo chamada corretamente.
- Verifique se o schema do banco de dados está correto.

## Melhores Práticas para Corrigir Falhas

1. **Isolamento**: Corrija uma falha de cada vez, começando pelas mais simples.

2. **Reprodução**: Certifique-se de que você pode reproduzir consistentemente o problema.

3. **Entendimento**: Compreenda completamente por que o teste está falhando antes de tentar corrigi-lo.

4. **Verificação Cruzada**: Depois de corrigir um teste, execute todos os testes novamente para garantir que sua correção não quebrou outros testes.

5. **Refatoração**: Se você encontrar muitos testes falhando relacionados a uma mudança, considere refatorar o código para melhor testabilidade.

## Critérios para Aprovação nos Testes

Para que o sistema seja considerado aprovado nos testes, os seguintes critérios devem ser atendidos:

1. **Todos os testes unitários devem passar**: Zero falhas e erros.

2. **Cobertura de código adequada**: Pelo menos 70% de cobertura para componentes críticos.

3. **Testes manuais passando**: Todos os cenários críticos descritos em `testes_manuais.md` devem passar.

4. **Desempenho aceitável**: Os testes não devem demorar muito para executar (mais de 10 segundos pode indicar problemas).

5. **Sem efeitos colaterais**: Os testes não devem deixar o sistema em um estado inconsistente (banco de dados corrompido, arquivos temporários, etc.).

## Rotina Recomendada de Testes

1. Execute os testes unitários após cada mudança significativa no código.
2. Execute o relatório de cobertura semanalmente.
3. Execute os testes manuais antes de cada release.
4. Adicione novos testes para cada nova funcionalidade implementada.
5. Adicione testes para qualquer bug encontrado antes de corrigi-lo.
