// Validação de formulários com feedback visual
function validarFormulario() {
    const campos = ['nome', 'telefone', 'email'];
    let isValido = true;

    // Remove mensagens de erro anteriores
    document.querySelectorAll('.erro-validacao').forEach(el => el.remove());

    campos.forEach(campo => {
        const elemento = document.getElementById(campo);
        if (!elemento) return;

        const valor = elemento.value.trim();
        if (valor === '') {
            mostrarErro(elemento, `Por favor, preencha o ${campo}`);
            isValido = false;
        } else if (campo === 'email' && !validarEmail(valor)) {
            mostrarErro(elemento, 'Email inválido');
            isValido = false;
        } else if (campo === 'telefone' && !validarTelefone(valor)) {
            mostrarErro(elemento, 'Telefone inválido');
            isValido = false;
        }
    });

    return isValido;
}

// Função para mostrar erro com feedback visual
function mostrarErro(elemento, mensagem) {
    const erro = document.createElement('div');
    erro.className = 'erro-validacao';
    erro.textContent = mensagem;
    erro.role = 'alert';
    erro.style.color = 'red';
    erro.style.fontSize = '0.8em';
    erro.style.marginTop = '-10px';
    erro.style.marginBottom = '10px';
    elemento.parentNode.insertBefore(erro, elemento.nextSibling);
    elemento.setAttribute('aria-invalid', 'true');
    elemento.focus();
}

// Validação de email
function validarEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

// Validação de telefone
function validarTelefone(telefone) {
    const numero = telefone.replace(/\D/g, '');
    return numero.length >= 10 && numero.length <= 11;
}

// Máscara para telefone com feedback visual
function mascaraTelefone(elemento) {
    let texto = elemento.value;
    texto = texto.replace(/\D/g, '');
    
    if (texto.length > 0) {
        if (texto.length <= 11) {
            if (texto.length === 11) {
                elemento.value = texto.replace(/^(\d{2})(\d{5})(\d{4})$/, '($1) $2-$3');
            } else {
                elemento.value = texto.replace(/^(\d{2})(\d{4})(\d{4})$/, '($1) $2-$3');
            }
            elemento.classList.remove('invalido');
            elemento.setAttribute('aria-invalid', 'false');
        } else {
            elemento.classList.add('invalido');
            elemento.setAttribute('aria-invalid', 'true');
        }
    }
}

// Confirmar exclusão com mensagem acessível
function confirmarExclusao(tipo, id) {
    const mensagem = `Tem certeza que deseja excluir este ${tipo}? Esta ação não pode ser desfeita.`;
    return confirm(mensagem);
}

// Feedback de sucesso
function mostrarSucesso(mensagem) {
    const sucesso = document.createElement('div');
    sucesso.className = 'sucesso-mensagem';
    sucesso.textContent = mensagem;
    sucesso.role = 'alert';
    sucesso.setAttribute('aria-live', 'polite');
    document.querySelector('.container').insertBefore(sucesso, document.querySelector('.container').firstChild);
    
    setTimeout(() => sucesso.remove(), 3000);
}
