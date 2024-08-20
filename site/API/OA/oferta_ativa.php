<?php
include '../../Global/Config.php';

header('Content-Type: application/json; charset=utf-8');

// Cria a conexão
$conn = new mysqli($host, $db_user, $db_pass, $db);

// Verifica a conexão
if ($conn->connect_error) {
    die(json_encode(array("error" => "Falha na conexão: " . $conn->connect_error)));
}

// Obtém o ID da URL
$id = $_GET['id'] ?? ''; // Use $_GET para parâmetros de URL

$conn->set_charset("utf8");

// Query SQL para selecionar dados com base no ID
$sql = "SELECT idofertas_ativa, total, pessoa, numero, nome_pessoa, nome_passou, ID_Corretor, restante FROM ofertas_ativa WHERE idofertas_ativa = ?";
$result = $conn->prepare($sql);

// Verifica se a preparação da consulta foi bem-sucedida
if ($result === false) {
    die(json_encode(array("error" => "Erro na preparação da consulta: " . $conn->error)));
}

$result->bind_param("s", $id);

if (!$result->execute()) {
    die(json_encode(array("error" => "Erro na execução da consulta: " . $result->error)));
}

$resultado_data = $result->get_result()->fetch_assoc();

// Verifica se o resultado contém dados
if ($resultado_data) {
    $response = array($resultado_data);
} else {
    $response = array("error" => "Nenhum dado encontrado para o ID fornecido.");
}

echo json_encode($response);

// Fecha o statement e a conexão
$result->close();
$conn->close();
?>
