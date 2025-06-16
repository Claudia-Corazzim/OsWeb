"""
Módulo para consumo de APIs externas
"""
import requests
import json

def buscar_cep(cep):
    """
    Busca informações de endereço a partir de um CEP usando a API ViaCEP
    
    Args:
        cep (str): O CEP a ser consultado, apenas números
        
    Returns:
        dict: Dicionário com os dados do endereço ou mensagem de erro
    """
    # Remover caracteres não numéricos do CEP
    cep = ''.join(filter(str.isdigit, cep))
    
    # Verificar se o CEP tem o tamanho correto
    if len(cep) != 8:
        return {'erro': 'CEP deve ter 8 dígitos'}
    
    # Fazer a requisição para a API ViaCEP
    try:
        response = requests.get(f'https://viacep.com.br/ws/{cep}/json/')
        
        # Verificar se a requisição foi bem-sucedida
        if response.status_code == 200:
            dados = response.json()
              # Verificar se o CEP foi encontrado
            if 'erro' in dados:
                return {'erro': 'CEP não encontrado'}
            
            return {
                'success': True,
                'endereco': {
                    'logradouro': dados.get('logradouro', ''),
                    'bairro': dados.get('bairro', ''),
                    'cidade': dados.get('localidade', ''),
                    'estado': dados.get('uf', ''),
                    'cep': dados.get('cep', '')
                }
            }
        else:
            return {'erro': f'Erro na requisição: {response.status_code}'}
    except Exception as e:
        return {'erro': f'Erro ao consultar o CEP: {str(e)}'}
