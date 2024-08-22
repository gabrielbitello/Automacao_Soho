<?php
require '../../Global/config.php';
// Cria a conexão
$conn = new mysqli($host, $db_user, $db_pass, $db);

// Verifica a conexão
if ($conn->connect_error) {
    die("Falha na conexão: " . $conn->connect_error);
}

// Obtém o ID e o novo valor de 'restante' do POST
$id = $_POST['id'] ?? '';
$novo_restante = $_POST['restante'] ?? '';

$conn->set_charset("utf8");

// Prepara a query para atualizar o valor de 'restante'
$sql_update = "UPDATE ofertas_ativa SET restante = ? WHERE idofertas_ativa = ?";
$stmt = $conn->prepare($sql_update);
$stmt->bind_param("ds", $novo_restante, $id);

// Executa a atualização
$stmt->execute();

// Fecha a conexão
$stmt->close();
$conn->close();
?>
