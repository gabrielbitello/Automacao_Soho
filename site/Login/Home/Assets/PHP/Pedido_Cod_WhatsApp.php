<?php
if (session_status() == PHP_SESSION_NONE) {
    session_start();
}

function RequestWatsAppCode($id_User) {
    global $dsn, $db_user, $db_pass, $options;

    $UID = uniqid($id_User . '_', true);
    $h_registro = date("Y-m-d H:i:s");
    $status = 1; // Exemplo de valor para a coluna Status
    $COD = 'some_cod_value'; // Defina o valor de COD conforme necessário

    try {
        // Conectar ao banco de dados usando PDO
        $pdo = new PDO($dsn, $db_user, $db_pass, $options);
        $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

        // Inserir valores na tabela Whatsapp
        $stmt = $pdo->prepare("
            INSERT INTO soho_geral.Whatsapp (UID, Status, COD, h_registro)
            VALUES (:UID, :Status, :COD, :h_registro)
        ");
        $stmt->bindParam(':UID', $UID, PDO::PARAM_STR);
        $stmt->bindParam(':Status', $status, PDO::PARAM_INT);
        $stmt->bindParam(':COD', $COD, PDO::PARAM_STR); // Certifique-se de que $COD está definido
        $stmt->bindParam(':h_registro', $h_registro, PDO::PARAM_STR);

        if ($stmt->execute()) {
            echo 'Código de WhatsApp solicitado com sucesso';
        } else {
            echo 'Falha ao solicitar o código de WhatsApp';
        }
    } catch (PDOException $e) {
        return 'Erro: ' . $e->getMessage();
    }
}
?>