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

$sql = "SELECT IdCorretor, UID, Status FROM Whatsapp WHERE Status = 1 AND COD = NULL ORDER BY idWhatsapp ASC LIMIT 1";
$result = $conn->query($sql);

$row = $result->fetch_assoc();

$response = array($row['IdCorretor'], $row['UID'], $row['Status']);


echo json_encode($response);

$conn->close();
$result->close();
?>