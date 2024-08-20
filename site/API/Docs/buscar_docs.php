<?php
include '../../Global/Config.php';

header('Content-Type: application/json; charset=utf-8');

// Cria a conexão
$conn = new mysqli($host, $db_user, $db_pass, $db);

// Verifica a conexão
if ($conn->connect_error) {
    die(json_encode(array("error" => "Falha na conexão: " . $conn->connect_error)));
}

$conn->set_charset("utf8");

// Definindo a query para buscar substituições
$sql = "SELECT chave, valor FROM substituicoes";
$result = $conn->query($sql);

$replacements = array();

if ($result->num_rows > 0) {
    // Adiciona cada chave e valor ao array de substituições
    while ($row = $result->fetch_assoc()) {
        $replacements[$row['chave']] = $row['valor'];
    }
} else {
    $replacements = array(); // Retorna um array vazio se nenhuma substituição for encontrada
}

echo json_encode($replacements);

$conn->close();
$result->close();
?>
