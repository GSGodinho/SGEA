function adicionarParametro(param, valor) {
    let url = window.location.href; // Obtém a URL atual
    let separador = url.includes('?') ? '&' : '?'; // Verifica se já existe uma query string

    // Se o parâmetro já existir, substitui, caso contrário, adiciona
    if (url.includes(param)) {
        // Substitui o parâmetro existente
        url = url.replace(new RegExp(param + '=[^&]*'), param + '=' + valor);
    } else {
        // Adiciona o novo parâmetro
        url = url + separador + param + '=' + valor;
    }

    // Redireciona para a URL com o parâmetro adicionado
    window.location.href = url;
}