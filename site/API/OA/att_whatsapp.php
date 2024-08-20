<?php
include '../../Global/Config.php';

header('Content-Type: application/json; charset=utf-8');

// Cria a conexão
$conn = new mysqli($host, $db_user, $db_pass, $db);

// Verifica a conexão
if ($conn->connect_error) {
    die(json_encode(array("error" => "Falha na conexão: " . $conn->connect_error)));
}

$id = $_POST['id'] ?? '';

if (empty($id)) {
    die(json_encode(array("error" => "ID não fornecido.")));
}

// Define a codificação para UTF-8
$conn->set_charset("utf8");

// Obtém o horário atual de São Paulo
date_default_timezone_set('America/Sao_Paulo');
$horario_atual_sp = date('Y-m-d H:i:s');

// Query SQL para atualizar o campo StatusWhatsapp
$sql = "UPDATE Corretores SET StatusWhatsapp = 1 WHERE idCorretores = ?";
$stmt = $conn->prepare($sql);

if ($stmt === false) {
    die(json_encode(array("error" => "Erro na preparação da declaração: " . $conn->error)));
}

$stmt->bind_param("i", $id);

if ($stmt->execute()) {
    $response = array("success" => "O StatusWhatsapp foi atualizado com sucesso.");
} else {
    $response = array("error" => "Erro ao atualizar o StatusWhatsapp: " . $stmt->error);
}

$stmt->close();
$conn->close();

echo json_encode($response);
?>