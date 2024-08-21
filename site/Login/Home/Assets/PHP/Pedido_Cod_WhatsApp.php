<?php
if (session_status() == PHP_SESSION_NONE) {
    session_start();
}

function RequestWatsAppCode($id_User) {
    global $dsn, $db_user, $db_pass, $options;

    $UID = uniqid($id_User . '_', true);
    $h_registro = date("Y-m-d H:i:s");
    $status = 1; // Exemplo de valor para a coluna Status

    try {
        // Conectar ao banco de dados usando PDO
        $pdo = new PDO($dsn, $db_user, $db_pass, $options);
        $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
        echo 'Conexão com o banco de dados estabelecida<br>';

        // Inserir valores na tabela Whatsapp
        $stmt = $pdo->prepare("
            INSERT INTO Whatsapp (UID, IdCorretor, Data_pedido)
            VALUES (:UID, :IdCorretor, :Data_pedido)
        ");
        $stmt->bindParam(':UID', $UID, PDO::PARAM_STR);
        $stmt->bindParam(':IdCorretor', $id_User, PDO::PARAM_INT);
        $stmt->bindParam(':Data_pedido', $h_registro, PDO::PARAM_STR);

        if ($stmt->execute()) {
            echo 'Código de WhatsApp solicitado com sucesso';
        } else {
            echo 'Falha ao solicitar o código de WhatsApp';
        }
    } catch (PDOException $e) {
        echo 'Erro: ' . $e->getMessage();
    }
}

?>