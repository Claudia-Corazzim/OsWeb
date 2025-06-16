/**
 * Script para adicionar recursos de acessibilidade ao sistema
 */

document.addEventListener('DOMContentLoaded', function() {
    // Inicializa os recursos de acessibilidade
    initAccessibility();
});

/**
 * Inicializa os recursos de acessibilidade
 */
function initAccessibility() {
    // Adiciona skip links para navegação por teclado
    addSkipLinks();
    
    // Melhora a navegação por teclado
    enhanceKeyboardNavigation();
    
    // Adiciona indicador de foco visual mais forte
    enhanceFocusIndicator();
    
    // Verifica e melhora o contraste de cores
    checkColorContrast();
    
    // Adiciona atributos ARIA onde necessário
    addAriaAttributes();
}

/**
 * Adiciona links de navegação rápida para usuários de teclado
 */
function addSkipLinks() {
    const skipLinks = document.createElement('div');
    skipLinks.className = 'skip-links';
    skipLinks.setAttribute('role', 'navigation');
    skipLinks.setAttribute('aria-label', 'Links de navegação rápida');
    
    // Link para pular para o conteúdo principal
    const mainContent = document.querySelector('main') || document.querySelector('.container');
    if (mainContent) {
        const skipToMain = document.createElement('a');
        skipToMain.href = '#main-content';
        skipToMain.textContent = 'Pular para o conteúdo principal';
        skipToMain.className = 'skip-link';
        skipLinks.appendChild(skipToMain);
        
        // Adiciona um id para o conteúdo principal
        mainContent.id = 'main-content';
        mainContent.setAttribute('tabindex', '-1');
    }
    
    // Adiciona os links ao corpo do documento
    document.body.insertBefore(skipLinks, document.body.firstChild);
}

/**
 * Melhora a navegação por teclado
 */
function enhanceKeyboardNavigation() {
    // Adiciona suporte para navegação por teclado em elementos interativos
    const interactiveElements = document.querySelectorAll('a, button, input, select, textarea, [tabindex]');
    
    interactiveElements.forEach(element => {
        // Adiciona handler para navegação com teclado
        element.addEventListener('keydown', function(e) {
            // Enter ou espaço em links
            if ((e.key === 'Enter' || e.key === ' ') && element.tagName === 'A') {
                e.preventDefault();
                element.click();
            }
        });
    });
}

/**
 * Melhora o indicador de foco para melhor visibilidade
 */
function enhanceFocusIndicator() {
    // Adiciona uma classe CSS global para elementos focados
    const style = document.createElement('style');
    style.textContent = `
        :focus {
            outline: 3px solid #4CAF50 !important;
            outline-offset: 2px !important;
            border-radius: 2px !important;
        }
    `;
    document.head.appendChild(style);
}

/**
 * Verifica e melhora o contraste de cores
 */
function checkColorContrast() {
    // Adiciona classes de alto contraste para textos importantes
    const headings = document.querySelectorAll('h1, h2, h3, h4, h5, h6');
    headings.forEach(heading => {
        heading.classList.add('high-contrast');
    });
    
    const labels = document.querySelectorAll('label');
    labels.forEach(label => {
        label.classList.add('high-contrast');
    });
}

/**
 * Adiciona atributos ARIA onde necessário
 */
function addAriaAttributes() {
    // Adicionar roles e atributos ARIA a elementos de formulário
    const forms = document.querySelectorAll('form');
    forms.forEach((form, index) => {
        form.setAttribute('aria-labelledby', `form-heading-${index}`);
        
        // Encontra o título do formulário
        const formHeading = form.querySelector('h2, h3, h4') || document.createElement('span');
        formHeading.id = `form-heading-${index}`;
        
        // Adiciona role="form" e nome acessível
        form.setAttribute('role', 'form');
    });
    
    // Tabelas
    const tables = document.querySelectorAll('table');
    tables.forEach((table, index) => {
        table.setAttribute('role', 'table');
        table.setAttribute('aria-label', `Tabela de dados ${index + 1}`);
        
        // Adicionar roles para linhas e células
        const rows = table.querySelectorAll('tr');
        rows.forEach(row => {
            row.setAttribute('role', 'row');
        });
        
        const headerCells = table.querySelectorAll('th');
        headerCells.forEach(cell => {
            cell.setAttribute('role', 'columnheader');
        });
        
        const dataCells = table.querySelectorAll('td');
        dataCells.forEach(cell => {
            cell.setAttribute('role', 'cell');
        });
    });
    
    // Botões de ação
    const actionButtons = document.querySelectorAll('input[type="submit"], button, a.delete');
    actionButtons.forEach(button => {
        if (button.classList.contains('delete')) {
            button.setAttribute('aria-label', 'Excluir item');
        }
    });
    
    // Alertas e mensagens
    const alertMessages = document.querySelectorAll('.error-message, .success-message, .info-message');
    alertMessages.forEach(message => {
        message.setAttribute('role', 'alert');
        message.setAttribute('aria-live', 'assertive');
    });
}
