<?php
include 'Config.php';

header('Content-Type: application/json; charset=utf-8');

// Cria a conexão
$conn = new mysqli($host_Geral_Mysql, $user_Geral_Mysql, $password_Geral_Mysql, $database_Geral_Mysql);

// Verifica a conexão
if ($conn->connect_error) {
    die(json_encode(array("error" => "Falha na conexão: " . $conn->connect_error)));
}

$conn->set_charset("utf8");

// Verificar se o ID foi fornecido
if (!isset($_GET['id'])) {
    die(json_encode(["error" => "ID não fornecido"]));
}

$id = intval($_GET['id']);

// Consulta SQL
$sql = "SELECT `idCorretores`, `Nome`, `Numero`, `EmailCRMX`, `SenhaCRMX`, `StatusWhatsapp`, `StatusGeral`, `Plano`, `Genero`  FROM `Corretores` WHERE `idCorretores` = ?";
$stmt = $conn->prepare($sql);
$stmt->bind_param("i", $id);
$stmt->execute();
$result = $stmt->get_result();

$response = array();

if ($result->num_rows > 0) {
    $data = $result->fetch_all(MYSQLI_ASSOC);
    $response = $data;
} else {
    $response = ["error" => "Nenhum corretor encontrado com o ID fornecido"];
}

echo json_encode($response);

$stmt->close();
$conn->close();
?>