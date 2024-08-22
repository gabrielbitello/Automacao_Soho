<?php
require '../../Global/config.php';

header('Content-Type: application/json; charset=utf-8');

// Cria a conexão
$conn = new mysqli($host, $db_user, $db_pass, $db);

// Verifica a conexão
if ($conn->connect_error) {
    die(json_encode(array("error" => "Falha na conexão: " . $conn->connect_error)));
}

$conn->set_charset("utf8");

// Obtém os dados do POST
$id = $_POST['id'];
$cod = $_POST['cod'];
$UID = $_POST['UID_cod'];

// Query SQL para atualizar o campo 'cod' na tabela Corretores
$sql = "UPDATE Whatsapp SET Status = 0 WHERE IdCorretor = ? AND UID = ?";
$stmt = $conn->prepare($sql);
$stmt->bind_param("ss", $cod, $UID);

if ($stmt->execute()) {
    $response = array("success" => "Cliente cadastrado com sucesso.");
} else {
    $response = array("error" => "Erro ao cadastrar cliente: " . $stmt->error);
}

echo json_encode($response);

$stmt->close();
$conn->close();
?>