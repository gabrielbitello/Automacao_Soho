<?php
require (ROOT_PATH . '/Global/config.php');

header('Content-Type: application/json charset=utf-8');

// Cria a conexão
$conn = new mysqli($host, $db_user, $db_pass, $db);

// Verifica a conexão
if ($conn->connect_error) {
    die(json_encode(array("error" => "Falha na conexão: " . $conn->connect_error)));
}

$conn->set_charset("utf8");

// Obtém o número do POST
$numero = $_POST['numero'] ?? '';

// Query SQL para buscar a data máxima
$sql_data = "SELECT MAX(Data) AS Data FROM soho_geral.oferta_ativa_Clientes WHERE Numero_F = ?";
$stmt = $conn->prepare($sql_data);
$stmt->bind_param("s", $numero);
$stmt->execute();
$resultado_data = $stmt->get_result()->fetch_assoc();

$response = array();

if ($resultado_data && $resultado_data['Data']) {
    $ultima_data = $resultado_data['Data'];
    try {
        $ultima_data_f = new DateTime($ultima_data);
    } catch (Exception $e) {
        $response['error'] = "Erro na conversão da data: " . $e->getMessage();
        echo json_encode($response);
        exit;
    }

    $trinta_dias_atras = new DateTime();
    $trinta_dias_atras->modify('-30 days');

    if ($ultima_data_f < $trinta_dias_atras) {
        $sql_retorno = "SELECT MAX(Retorno) AS Retorno FROM soho_geral.oferta_ativa_Clientes WHERE Numero_F = ?";
        $stmt = $conn->prepare($sql_retorno);
        $stmt->bind_param("s", $numero);
        $stmt->execute();
        $resultado_retorno = $stmt->get_result()->fetch_assoc();

        if ($resultado_retorno && $resultado_retorno['Retorno'] !== null) {
            if ($resultado_retorno['Retorno'] == 0) {
                $response = false;  // Pode enviar mensagem
            } else {
                $response = true;  // Não pode enviar mensagem
            }
        } else {
            $response = true;  // Não pode enviar mensagem (resultado_retorno é null)
        }
    } else {
        $response = true;  // Não pode enviar mensagem (menos de 30 dias)
    }
} else {
    $response = false;  // O número não existe
}

echo json_encode($response);

$stmt->close();
$conn->close();
?>
