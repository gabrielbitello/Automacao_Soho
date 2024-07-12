<?php
include 'config.php'; // Incluir o arquivo de configuração


// Definir o fuso horário de São Paulo
date_default_timezone_set('America/Sao_Paulo');

// Preparar a query SQL para incluir a coluna mensagem
$stmt = $conn->prepare("INSERT INTO soho_geral.ofertas_ativa (total, ativa, mensagem, h_registro) VALUES (?, ?, ?, ?)");

// Verificar se o statement foi preparado corretamente
if ($stmt === false) {
    die("Erro na preparação: " . $conn->error);
}

// Receber os valores do formulário
$total = $_POST['numero'];
$mensagem = $_POST['mensagem']; // Receber o valor selecionado no campo 'mensagem'

// Definir valores para as outras colunas
$ativa = 1;
$h_registro = date('Y-m-d H:i:s'); // Data e hora atual no formato MySQL

// Vincular parâmetros
$stmt->bind_param("iiss", $total, $ativa, $mensagem, $h_registro, );

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