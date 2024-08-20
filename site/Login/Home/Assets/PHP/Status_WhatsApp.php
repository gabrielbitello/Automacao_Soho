<?php

function WhatsAppStatus($id){
    require (ROOT_PATH . '/Global/config.php');
    try {
        // Conectar ao banco de dados usando PDO
        $pdo = new PDO($dsn, $db_user, $db_pass, $options);
        $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

        // Buscar o StatusWhatsapp com base no idCorretores
        $stmt = $pdo->prepare("
            SELECT StatusWhatsapp
            FROM Corretores
            WHERE idCorretores = :idCorretores
        ");
        $stmt->bindParam(':idCorretores', $id, PDO::PARAM_INT);

        if ($stmt->execute()) {
            $result = $stmt->fetch(PDO::FETCH_ASSOC);
            if ($result) {
                return $result['StatusWhatsapp'];
            } else {
                return 'Corretor não encontrado';
            }
        } else {
            return 'Falha ao buscar o StatusWhatsapp';
        }
    } catch (PDOException $e) {
        return $e->getMessage();
    }
}
?>