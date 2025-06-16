/**
 * Módulo para consulta de CEP e preenchimento automático de endereço
 */

document.addEventListener('DOMContentLoaded', function() {
    // Inicializa a consulta de CEP
    initCepLookup();
});

/**
 * Inicializa a busca de CEP nos formulários
 */
function initCepLookup() {
    // Procura por todos os campos de CEP
    const cepFields = document.querySelectorAll('input[id="cep"]');
    
    if (cepFields.length > 0) {
        cepFields.forEach(field => {
            // Adiciona máscara para o CEP (formato: 00000-000)
            field.addEventListener('input', function(e) {
                let value = e.target.value.replace(/\D/g, '');
                if (value.length > 5) {
                    value = value.substring(0, 5) + '-' + value.substring(5);
                }
                e.target.value = value;
            });
            
            // Adiciona evento para buscar o CEP quando o campo perder o foco
            field.addEventListener('blur', function() {
                const cep = this.value.replace(/\D/g, '');
                
                // Verifica se o CEP tem 8 dígitos
                if (cep.length === 8) {
                    // Adiciona indicador de carregamento
                    const loadingSpinner = document.createElement('div');
                    loadingSpinner.classList.add('spinner');
                    loadingSpinner.id = 'cep-loading';
                    this.parentNode.appendChild(loadingSpinner);
                    
                    // Desabilita os campos de endereço
                    disableAddressFields(true);
                    
                    // Busca o CEP na API
                    fetch(`/api/consulta_cep/${cep}`)
                        .then(response => response.json())
                        .then(data => {
                            // Remove o indicador de carregamento
                            const spinner = document.getElementById('cep-loading');
                            if (spinner) {
                                spinner.remove();
                            }
                            
                            // Preenche os campos de endereço
                            if (!data.erro) {
                                document.getElementById('logradouro').value = data.endereco.logradouro;
                                document.getElementById('bairro').value = data.endereco.bairro;
                                document.getElementById('cidade').value = data.endereco.cidade;
                                document.getElementById('estado').value = data.endereco.estado;
                                
                                // Coloca o foco no campo de número
                                const numeroField = document.getElementById('numero');
                                if (numeroField) {
                                    numeroField.focus();
                                }
                            } else {
                                alert('CEP não encontrado. Por favor, verifique o CEP informado.');
                            }
                            
                            // Habilita os campos de endereço
                            disableAddressFields(false);
                        })
                        .catch(error => {
                            console.error('Erro ao buscar CEP:', error);
                            
                            // Remove o indicador de carregamento
                            const spinner = document.getElementById('cep-loading');
                            if (spinner) {
                                spinner.remove();
                            }
                            
                            alert('Erro ao buscar o CEP. Por favor, tente novamente.');
                            
                            // Habilita os campos de endereço
                            disableAddressFields(false);
                        });
                }
            });
        });
    }
}

/**
 * Desabilita ou habilita os campos de endereço durante a consulta do CEP
 * @param {boolean} disable - Se verdadeiro, desabilita os campos
 */
function disableAddressFields(disable) {
    const fields = ['logradouro', 'bairro', 'cidade', 'estado'];
    
    fields.forEach(fieldId => {
        const field = document.getElementById(fieldId);
        if (field) {
            field.disabled = disable;
            if (disable) {
                field.placeholder = 'Carregando...';
            } else {
                field.placeholder = '';
            }
        }
    });
}
