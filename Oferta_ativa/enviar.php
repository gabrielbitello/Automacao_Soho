<?php
// Dados para conexão com o banco de dados
$host = "localhost";
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
$stmt = $conn->prepare("INSERT INTO soho_geral.ofertas_ativa (total, ativa, h_registro) VALUES (?, ?, ?)");

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

header("Refresh: 4; URL=index.html");

// Fechar statement
$stmt->close();

// Fechar conexão
$conn->close();
?>