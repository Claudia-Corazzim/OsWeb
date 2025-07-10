// Cache de resultados para evitar requisições repetidas
let searchCache = {};

// Função para criar o dropdown de sugestões
function createSuggestionsDropdown(input) {
    const dropdown = document.createElement('div');
    dropdown.className = 'suggestions-dropdown';
    dropdown.style.display = 'none';
    dropdown.style.position = 'absolute';
    dropdown.style.border = '1px solid #ddd';
    dropdown.style.maxHeight = '200px';
    dropdown.style.overflowY = 'auto';
    dropdown.style.backgroundColor = 'white';
    dropdown.style.zIndex = '1000';
    input.parentNode.style.position = 'relative';
    input.parentNode.appendChild(dropdown);
    return dropdown;
}

// Função para buscar peças do estoque
async function buscarPecas(search) {
    try {
        // Remover símbolos e espaços extras, mantendo apenas letras, números e espaços
        const searchTerm = search.toLowerCase().trim();
        
        if (!searchTerm) return [];

        // Se já temos no cache e não passou muito tempo, retornar do cache
        if (searchCache[searchTerm] && (Date.now() - searchCache[searchTerm].timestamp < 60000)) {
            return searchCache[searchTerm].data;
        }

        const response = await fetch(`/api/estoque?search=${encodeURIComponent(searchTerm)}`);
        const data = await response.json();
        
        // Guardar no cache
        searchCache[searchTerm] = {
            data: data,
            timestamp: Date.now()
        };
        
        // Limpar cache antigo
        Object.keys(searchCache).forEach(key => {
            if (Date.now() - searchCache[key].timestamp > 60000) {
                delete searchCache[key];
            }
        });
        
        return data;
    } catch (error) {
        console.error('Erro ao buscar peças:', error);
        return [];
    }
}

// Aplicar autocomplete em todos os campos de descrição de serviço
document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.descricao-servico').forEach(input => {
        const dropdown = createSuggestionsDropdown(input);
        let timeoutId;

        input.addEventListener('input', function() {
            clearTimeout(timeoutId);
            const search = this.value.trim();

            // Limpar e esconder dropdown se o campo estiver vazio
            if (!search) {
                dropdown.innerHTML = '';
                dropdown.style.display = 'none';
                return;
            }

            // Esperar um pouco antes de fazer a busca para evitar muitas requisições
            timeoutId = setTimeout(async () => {
                const pecas = await buscarPecas(search);
                
                // Limpar dropdown anterior
                dropdown.innerHTML = '';

                if (pecas.length > 0) {
                    // Filtrar e ordenar as peças por relevância
                    const searchLower = search.toLowerCase();
                    const pecasFiltradas = pecas
                        .filter(peca => peca.nome.toLowerCase().includes(searchLower))
                        .sort((a, b) => {
                            const aStartsWith = a.nome.toLowerCase().startsWith(searchLower);
                            const bStartsWith = b.nome.toLowerCase().startsWith(searchLower);
                            if (aStartsWith && !bStartsWith) return -1;
                            if (!aStartsWith && bStartsWith) return 1;
                            return a.nome.localeCompare(b.nome);
                        });

                    pecasFiltradas.forEach(peca => {
                        const item = document.createElement('div');
                        item.className = 'suggestion-item';
                        item.style.padding = '8px';
                        item.style.cursor = 'pointer';
                        item.style.borderBottom = '1px solid #eee';
                        
                        // Destacar parte do texto que corresponde à busca
                        let nome = peca.nome;
                        const searchLower = search.toLowerCase();
                        const index = nome.toLowerCase().indexOf(searchLower);
                        if (index >= 0) {
                            const before = nome.substring(0, index);
                            const match = nome.substring(index, index + search.length);
                            const after = nome.substring(index + search.length);
                            nome = `${before}<strong>${match}</strong>${after}`;
                        }
                        
                        item.innerHTML = `${nome} (Qtd: ${peca.quantidade}) - R$ ${peca.valor_instalado || peca.valor || 0}`;
                        
                        item.addEventListener('mouseenter', () => {
                            item.style.backgroundColor = '#f0f0f0';
                        });
                        
                        item.addEventListener('mouseleave', () => {
                            item.style.backgroundColor = 'white';
                        });

                        item.addEventListener('click', () => {
                            // Ao selecionar, inclui o nome da peça e o valor
                            const valorStr = peca.valor_instalado ? 
                                ` - R$ ${parseFloat(peca.valor_instalado).toFixed(2)}` : 
                                ` - R$ ${parseFloat(peca.valor || 0).toFixed(2)}`;
                            input.value = `${peca.nome}${valorStr}`;
                            dropdown.style.display = 'none';
                        });

                        dropdown.appendChild(item);
                    });

                    dropdown.style.display = 'block';
                    dropdown.style.width = input.offsetWidth + 'px';
                    dropdown.style.top = (input.offsetHeight) + 'px';
                } else {
                    dropdown.style.display = 'none';
                }
            }, 300);
        });

        // Fechar dropdown quando clicar fora
        document.addEventListener('click', function(e) {
            if (!input.contains(e.target) && !dropdown.contains(e.target)) {
                dropdown.style.display = 'none';
            }
        });
    });
});
