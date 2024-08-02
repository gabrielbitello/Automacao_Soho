<?php
include 'Config.php';

header('Content-Type: application/json charset=utf-8');

// Cria a conexão
$conn = new mysqli($host_Geral_Mysql, $user_Geral_Mysql, $password_Geral_Mysql, $database_Geral_Mysql);

// Verifica a conexão
if ($conn->connect_error) {
    die(json_encode(array("error" => "Falha na conexão: " . $conn->connect_error)));
}

// Obtém o horário atual de São Paulo
date_default_timezone_set('America/Sao_Paulo');
$horario_atual_sp = date('Y-m-d H:i:s');

// Query SQL para atualizar o campo h_termino
$sql = "UPDATE ofertas_ativa SET ativa = 0, h_termino = ? WHERE ativa = 1 LIMIT 1";
$stmt = $conn->prepare($sql);
$stmt->bind_param("s", $horario_atual_sp);

if ($stmt->execute()) {
    $response = array("success" => "O horário de término foi atualizado com sucesso.");
} else {
    $response = array("error" => "Erro ao atualizar o horário de término: " . $stmt->error);
}

echo json_encode($response);

$stmt->close();
$conn->close();
?>