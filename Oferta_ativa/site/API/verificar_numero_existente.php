<?php
include 'Config.php';

header('Content-Type: application/json');

// Cria a conexão
$conn = new mysqli($host_Geral_Mysql, $user_Geral_Mysql, $password_Geral_Mysql, $database_Geral_Mysql);

// Verifica a conexão
if ($conn->connect_error) {
    die(json_encode(array("error" => "Falha na conexão: " . $conn->connect_error)));
}

// Obtém o número do POST
$numero = $_POST['numero'];

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
                // O número existe, e a última data registrada tem mais de 30 dias, e não está bloqueado o envio de mensagem
                $response['can_send_message'] = false;
            } else {
                // O número existe, e a última data registrada tem mais de 30 dias, e está bloqueado o envio de mensagem
                $response['can_send_message'] = true;
            }
        } else {
            // O número existe, e a última data registrada tem mais de 30 dias, e está bloqueado o envio de mensagem
            $response['can_send_message'] = true;
        }
    } else {
        // O número existe, mas a última data registrada tem menos de 30 dias
        $response['can_send_message'] = true;
    }
} else {
    // O número não existe
    $response['can_send_message'] = false;
}

echo json_encode($response);

$stmt->close();
$conn->close();
?>