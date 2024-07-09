<?php
// Dados para conexão com o banco de dados
$host = "mysql.bitello.cloud";
$username = "soho_geral";
$password = "Soho2024!";
$dbname = "soho_geral";

// Conectar ao banco de dados
$conn = new mysqli($host, $username, $password, $dbname);

// Verificar conexão
if ($conn->connect_error) {
    die("Falha na conexão: " . $conn->connect_error);
}

// Definir o fuso horário de São Paulo
date_default_timezone_set('America/Sao_Paulo');

// Preparar a query SQL
$stmt = $conn->prepare("INSERT INTO ofertas_ativas (total, ativa, h_registro) VALUES (?, ?, ?)");

// Verificar se o statement foi preparado corretamente
if ($stmt === false) {
    die("Erro na preparação: " . $conn->error);
}

// Receber o valor do formulário
$total = $_POST['numero'];

// Definir valores para as outras colunas
$ativa = 1;
$h_registro = date('Y-m-d H:i:s'); // Data e hora atual no formato MySQL

// Vincular parâmetros
$stmt->bind_param("iis", $total, $ativa, $h_registro);

// Executar a query
if ($stmt->execute()) {
    echo "Registro inserido com sucesso.";
} else {
    echo "Erro ao inserir registro: " . $stmt->error;
}

// Fechar statement
$stmt->close();

// Fechar conexão
$conn->close();
?>

<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Soho</title>
    <link rel="stylesheet" href="Assets/Css/reset.css">
    <link rel="stylesheet" href="Assets/Css/style.css">
</head>
<body>
    <header>

    </header> 

    <main>
        <form id="solicitacaoForm" method="post">
            <input type="number" name="numero" min="1" max="500" required>
            <button type="submit">OK</button>
        </form>
    </main>
    <footer>

    </footer>

    <div class="overlay"></div>
    <div class="popup">Solicitado</div>

    <script>
        document.getElementById('solicitacaoForm').addEventListener('submit', function(e) {
            e.preventDefault(); // Impede o envio real do formulário
            let popup = document.querySelector('.popup');
            popup.style.top = '-100px'; // Começa fora da tela
            popup.style.display = 'block'; // Mostra o popup
            setTimeout(function() {
                popup.style.top = '0'; // Move para o topo da tela
            }, 100); // Pequeno atraso antes de começar a animação

            setTimeout(function() {
                popup.style.top = '-100px'; // Esconde o popup após 2 segundos
                setTimeout(function() {
                    popup.style.display = 'none'; // Esconde completamente após a animação
                }, 500); // Espera a animação terminar
            }, 8000);
        });
    </script>
</body>
</html>