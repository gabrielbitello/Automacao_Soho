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

$sql = "SELECT total, pessoa, numero, nome_pessoa, nome_passou, ID_Corretor FROM ofertas_ativa WHERE ativa = 1 LIMIT 1";
$result = $conn->query($sql);

if ($result->num_rows > 0) {
    $row = $result->fetch_assoc();
    $pessoa = $row['pessoa'];
    if ($pessoa == 1) {
        $response = array(2, $row['numero'], $row['nome_pessoa'], $row['nome_passou'], $row['ID_Corretor']);
    } elseif ($pessoa == 0) {
        $response = array(1, $row['total'], $row['ID_Corretor']);
    } else {
        $response = array(0, 0);
    }
} else {
    $response = array(0, 0); // Ou qualquer outro valor que indique que nenhum resultado foi encontrado
}

echo json_encode($response);

$conn->close();
?>