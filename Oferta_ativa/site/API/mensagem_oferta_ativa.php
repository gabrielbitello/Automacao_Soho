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

$sql = "SELECT mensagem FROM ofertas_ativa WHERE ativa = 1 ORDER BY idofertas_ativa ASC LIMIT 1";
$result = $conn->query($sql);

if ($result->num_rows > 0) {
    $row = $result->fetch_assoc();
    $response = array("mensagem" => $row['mensagem']);
} else {
    $response = array("mensagem" => "Nenhuma oferta ativa encontrada");
}

echo json_encode($response);

$conn->close();
$result->close();
?>