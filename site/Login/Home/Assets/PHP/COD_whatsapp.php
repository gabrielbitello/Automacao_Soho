<?php

function WatsAppCOD($UID){
    session_start();
    require (ROOT_PATH . '/Global/config.php');
    $id = $_SESSION['user_id'];

    $UID = uniqid($id . '_', true);

    try {
        // Conectar ao banco de dados usando PDO
        $pdo = new PDO($dsn, $db_user, $db_pass, $options);
        $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

        // Buscar o COD onde UID é igual ao dado e Status é igual a 1
        $stmt = $pdo->prepare("
            SELECT COD
            FROM soho_geral.Whatsapp
            WHERE UID = :UID
        ");
        $stmt->bindParam(':UID', $UID, PDO::PARAM_STR);

        if ($stmt->execute()) {
            $result = $stmt->fetch(PDO::FETCH_ASSOC);
            if ($result) {
                if ($result['COD'] == null) {
                    return null;
                }else{
                    return $result['COD'];
                }
            } else {
                echo 'Nenhum registro encontrado com o UID fornecido';
            }
        } else {
            echo 'Falha ao buscar o COD';
        }
    } catch (PDOException $e) {
        echo $e->getMessage();
    }
}
?>