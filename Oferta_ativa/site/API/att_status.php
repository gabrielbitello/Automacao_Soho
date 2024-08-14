<?php
include 'Config.php';

header('Content-Type: application/json; charset=utf-8');

// Cria a conexão
$conn = new mysqli($host_Geral_Mysql, $user_Geral_Mysql, $password_Geral_Mysql, $database_Geral_Mysql);

// Verifica a conexão
if ($conn->connect_error) {
    die(json_encode(array("error" => "Falha na conexão: " . $conn->connect_error)));
}

// Define a codificação para UTF-8
$conn->set_charset("utf8");

// Obtém o horário atual de São Paulo
date_default_timezone_set('America/Sao_Paulo');
$horario_atual_sp = date('Y-m-d H:i:s');

// Query SQL para atualizar o campo h_termino
$sql = "UPDATE ofertas_ativa SET status = 1 WHERE ativa = 1 AND status = 0 ORDER BY idofertas_ativa ASC LIMIT 1";
$stmt = $conn->prepare($sql);

if ($stmt->execute()) {
    $response = array("success" => "O status foi atualizado com sucesso.");
} else {
    $response = array("error" => "Erro ao atualizar o status: " . $stmt->error);
}

echo json_encode($response);

$stmt->close();
$conn->close();
?>