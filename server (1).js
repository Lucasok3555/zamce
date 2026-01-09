// Solicita o nome do usuário
let nomeUsuario = prompt("Por favor, digite seu nome:");

// Verifica se o usuário forneceu um nome
if (nomeUsuario === null || nomeUsuario.trim() === "") {
    // Se cancelar ou deixar vazio, oculta o conteúdo da página
    document.body.innerHTML = "<h1 style='text-align: center; margin-top: 50px; color: #666;'>Acesso negado. Você precisa fornecer seu nome para acessar esta página.</h1>";
} else {
    // Se fornecer o nome, exibe mensagem de boas-vindas
    alert("Bem-vindo(a), " + nomeUsuario + "!");
    
    // O conteúdo da página continua visível normalmente
    console.log("Usuário logado:", nomeUsuario);
}