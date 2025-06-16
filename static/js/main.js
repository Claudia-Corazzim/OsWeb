/**
 * Script principal para o Sistema de Gestão de Ordens de Serviço
 * Contém funções para validação de formulários, filtros de tabelas e confirmações
 */

// Aguarda o carregamento completo do DOM
document.addEventListener('DOMContentLoaded', function() {
    // Inicializa os componentes
    initFormValidation();
    initTableFilters();
    initDeleteConfirmations();
    initMaskInputs();
    initCepConsulta();
});

/**
 * Inicializa a validação de formulários
 */
function initFormValidation() {
    const forms = document.querySelectorAll('form');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(event) {
            // Verificar se há campos obrigatórios vazios
            const requiredFields = form.querySelectorAll('[required]');
            let isValid = true;
            
            requiredFields.forEach(field => {
                if (!field.value.trim()) {
                    isValid = false;
                    field.classList.add('invalid-field');
                    
                    // Adiciona mensagem de erro se ainda não existir
                    if (!field.nextElementSibling || !field.nextElementSibling.classList.contains('error-message')) {
                        const errorMsg = document.createElement('div');
                        errorMsg.classList.add('error-message');
                        errorMsg.textContent = 'Este campo é obrigatório';
                        field.parentNode.insertBefore(errorMsg, field.nextSibling);
                    }
                } else {
                    field.classList.remove('invalid-field');
                    
                    // Remove mensagem de erro se existir
                    if (field.nextElementSibling && field.nextElementSibling.classList.contains('error-message')) {
                        field.parentNode.removeChild(field.nextElementSibling);
                    }
                    
                    // Validações específicas
                    if (field.type === 'email' && !validateEmail(field.value)) {
                        isValid = false;
                        field.classList.add('invalid-field');
                        
                        const errorMsg = document.createElement('div');
                        errorMsg.classList.add('error-message');
                        errorMsg.textContent = 'Email inválido';
                        field.parentNode.insertBefore(errorMsg, field.nextSibling);
                    }
                    
                    if (field.id === 'telefone' && !validatePhone(field.value)) {
                        isValid = false;
                        field.classList.add('invalid-field');
                        
                        const errorMsg = document.createElement('div');
                        errorMsg.classList.add('error-message');
                        errorMsg.textContent = 'Telefone inválido';
                        field.parentNode.insertBefore(errorMsg, field.nextSibling);
                    }
                }
            });
            
            if (!isValid) {
                event.preventDefault();
            }
        });
    });
}

/**
 * Inicializa os filtros de tabela
 */
function initTableFilters() {
    // Adiciona campo de busca para cada tabela
    const tables = document.querySelectorAll('table');
    
    tables.forEach(table => {
        // Cria o campo de busca
        const tableContainer = table.parentElement;
        const searchContainer = document.createElement('div');
        searchContainer.classList.add('search-container');
        
        const searchInput = document.createElement('input');
        searchInput.type = 'text';
        searchInput.placeholder = 'Buscar...';
        searchInput.classList.add('search-input');
        
        searchContainer.appendChild(searchInput);
        tableContainer.insertBefore(searchContainer, table);
        
        // Adiciona o evento de busca
        searchInput.addEventListener('keyup', function() {
            const searchTerm = this.value.toLowerCase();
            const rows = table.querySelectorAll('tbody tr');
            
            rows.forEach(row => {
                const text = row.textContent.toLowerCase();
                if (text.includes(searchTerm)) {
                    row.style.display = '';
                } else {
                    row.style.display = 'none';
                }
            });
        });
    });
}

/**
 * Inicializa as confirmações para exclusão
 */
function initDeleteConfirmations() {
    const deleteLinks = document.querySelectorAll('a.delete');
    
    deleteLinks.forEach(link => {
        link.addEventListener('click', function(event) {
            if (!confirm('Tem certeza que deseja excluir este item? Esta ação não pode ser desfeita.')) {
                event.preventDefault();
            }
        });
    });
}

/**
 * Inicializa máscaras para campos de entrada
 */
function initMaskInputs() {
    // Máscaras para telefone
    const phoneInputs = document.querySelectorAll('input[id="telefone"]');
    phoneInputs.forEach(input => {
        input.addEventListener('input', function(e) {
            let value = e.target.value.replace(/\D/g, '');
            
            if (value.length <= 10) {
                // Formato (00) 0000-0000
                value = value.replace(/^(\d{2})(\d)/g, '($1) $2');
                value = value.replace(/(\d)(\d{4})$/, '$1-$2');
            } else {
                // Formato (00) 00000-0000
                value = value.replace(/^(\d{2})(\d)/g, '($1) $2');
                value = value.replace(/(\d)(\d{4})$/, '$1-$2');
            }
            
            e.target.value = value;
        });
    });
    
    // Máscaras para CNPJ/CPF
    const documentInputs = document.querySelectorAll('input[id="documento"]');
    documentInputs.forEach(input => {
        input.addEventListener('input', function(e) {
            let value = e.target.value.replace(/\D/g, '');
            
            if (value.length <= 11) {
                // CPF: 000.000.000-00
                value = value.replace(/^(\d{3})(\d)/g, '$1.$2');
                value = value.replace(/^(\d{3})\.(\d{3})(\d)/g, '$1.$2.$3');
                value = value.replace(/\.(\d{3})(\d)/g, '.$1-$2');
            } else {
                // CNPJ: 00.000.000/0000-00
                value = value.replace(/^(\d{2})(\d)/g, '$1.$2');
                value = value.replace(/^(\d{2})\.(\d{3})(\d)/g, '$1.$2.$3');
                value = value.replace(/\.(\d{3})(\d)/g, '.$1/$2');
                value = value.replace(/(\d{4})(\d)/g, '$1-$2');
            }
            
            e.target.value = value;
        });
    });
    
    // Máscara para CEP
    const cepInputs = document.querySelectorAll('input[id="cep"]');
    cepInputs.forEach(input => {
        input.addEventListener('input', function(e) {
            let value = e.target.value.replace(/\D/g, '');
            
            // Formato 00000-000
            if (value.length > 5) {
                value = value.replace(/^(\d{5})(\d)/, '$1-$2');
            }
            
            e.target.value = value;
        });
    });
}

/**
 * Inicializa a consulta de CEP
 */
function initCepConsulta() {
    const cepInputs = document.querySelectorAll('input[id="cep"]');
    
    cepInputs.forEach(input => {
        input.addEventListener('blur', function() {
            const cep = input.value.replace(/\D/g, '');
            
            if (cep.length !== 8) {
                return;
            }
            
            // Mostrar indicador de carregamento
            const loadingDiv = document.createElement('div');
            loadingDiv.classList.add('loading-indicator');
            loadingDiv.textContent = 'Consultando CEP...';
            input.parentNode.insertBefore(loadingDiv, input.nextSibling);
            
            // Realizar a consulta
            fetch(`/api/consulta_cep/${cep}`)
                .then(response => response.json())
                .then(data => {
                    // Remover indicador de carregamento
                    if (loadingDiv.parentNode) {
                        loadingDiv.parentNode.removeChild(loadingDiv);
                    }
                    
                    if (data.erro) {
                        alert(`Erro: ${data.erro}`);
                        return;
                    }
                    
                    if (data.success) {
                        // Preencher os campos de endereço
                        const endereco = data.endereco;
                        
                        // Montar o endereço completo
                        const enderecoCompleto = `${endereco.logradouro}, ${endereco.bairro}, ${endereco.cidade}-${endereco.estado}, ${endereco.cep}`;
                        
                        // Preencher o campo de endereço
                        const enderecoInput = document.getElementById('endereco');
                        if (enderecoInput) {
                            enderecoInput.value = enderecoCompleto;
                        }
                    }
                })
                .catch(error => {
                    // Remover indicador de carregamento
                    if (loadingDiv.parentNode) {
                        loadingDiv.parentNode.removeChild(loadingDiv);
                    }
                    
                    console.error('Erro ao consultar CEP:', error);
                    alert('Erro ao consultar o CEP. Tente novamente mais tarde.');
                });
        });
    });
}

/**
 * Validar formato de email
 * @param {string} email - O email a ser validado
 * @returns {boolean} - Verdadeiro se o email for válido
 */
function validateEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

/**
 * Validar formato de telefone
 * @param {string} phone - O telefone a ser validado
 * @returns {boolean} - Verdadeiro se o telefone for válido
 */
function validatePhone(phone) {
    // Remove tudo o que não for dígito
    const phoneDigits = phone.replace(/\D/g, '');
    // Verifica se tem pelo menos 10 dígitos (DDD + número)
    return phoneDigits.length >= 10;
}

/**
 * Validar formato de CEP
 * @param {string} cep - O CEP a ser validado
 * @returns {boolean} - Verdadeiro se o CEP for válido
 */
function validateCep(cep) {
    // Remove tudo o que não for dígito
    const cepDigits = cep.replace(/\D/g, '');
    // Verifica se tem 8 dígitos
    return cepDigits.length === 8;
}
