<?php
include 'Config.php';

header('Content-Type: application/json charset=utf-8');

// Cria a conexão
$conn = new mysqli($host_Geral_Mysql, $user_Geral_Mysql, $password_Geral_Mysql, $database_Geral_Mysql);

// Verifica a conexão
if ($conn->connect_error) {
    die(json_encode(array("error" => "Falha na conexão: " . $conn->connect_error)));
}

$conn->set_charset("utf8");

// Obtém os dados do POST
$nome = $_POST['nome'];
$nome_f = $_POST['nome_f'];
$numero = $_POST['numero'];
$numero_f = $_POST['numero_f'];
$status = $_POST['status'];
$mensagem = $_POST['mensagem'];
$ID = $_POST['ID'];

// Data atual
date_default_timezone_set('America/Sao_Paulo');
$data_atual = date('Y-m-d H:i:s');

// Query SQL para inserir os dados na tabela oferta_ativa_Clientes
$sql = "INSERT INTO oferta_ativa_Clientes (Nome, Nome_F, Numero, Numero_F, Status, Mensagem, Data, Corretor) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)";
$stmt = $conn->prepare($sql);
$stmt->bind_param("ssssssss", $nome, $nome_f, $numero, $numero_f, $status, $mensagem, $data_atual, $ID);

if ($stmt->execute()) {
    $response = array("success" => "Cliente cadastrado com sucesso.");
} else {
    $response = array("error" => "Erro ao cadastrar cliente: " . $stmt->error);
}

echo json_encode($response);

$stmt->close();
$conn->close();
?>