<?php
include 'Config.php';

header('Content-Type: application/json charset=utf-8');

// Cria a conexão
$conn = new mysqli($host_Geral_Mysql, $user_Geral_Mysql, $password_Geral_Mysql, $database_Geral_Mysql);

// Verifica a conexão
if ($conn->connect_error) {
    die(json_encode(array("error" => "Falha na conexão: " . $conn->connect_error)));
}

$id = $_POST['id'] ?? '';

$conn->set_charset("utf8");

$sql = "SELECT idofertas_ativa, total, pessoa, numero, nome_pessoa, nome_passou, ID_Corretor, restante FROM ofertas_ativa WHERE idofertas_ativa = ?";
$result = $conn->prepare($sql_data);
$result->bind_param("s", $id);
$result->execute();
$resultado_data = $result->get_result()->fetch_assoc();

if ($result->num_rows > 0) {
    $response = array($resultado_data);

echo json_encode($response);

$conn->close();
$result->close();
?>