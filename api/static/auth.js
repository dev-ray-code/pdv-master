// Guarda de autenticação do painel administrativo.
// Inclua este script em TODA página que deve exigir login de admin
// (dashboard.html, clientes.html, licencas.html, index.html).
// Não inclua em login.html (senão vira loop de redirecionamento).
(function () {
    var TOKEN_KEY = "pdv_admin_token";
    var token = localStorage.getItem(TOKEN_KEY);

    if (!token) {
        window.location.href = "/login";
        return;
    }

    // Intercepta todo fetch() da página para anexar o token, sem precisar
    // alterar cada chamada individualmente nos outros arquivos .html.
    var fetchOriginal = window.fetch;

    window.fetch = function (url, opcoes) {
        opcoes = opcoes || {};
        opcoes.headers = Object.assign(
            {},
            opcoes.headers || {},
            { "Authorization": "Bearer " + token }
        );

        return fetchOriginal(url, opcoes).then(function (resposta) {
            if (resposta.status === 401 || resposta.status === 403) {
                localStorage.removeItem(TOKEN_KEY);
                window.location.href = "/login";
            }
            return resposta;
        });
    };

    window.logoutAdmin = function () {
        localStorage.removeItem(TOKEN_KEY);
        window.location.href = "/login";
    };
})();