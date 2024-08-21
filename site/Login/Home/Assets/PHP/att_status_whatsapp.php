<?php
if (session_status() == PHP_SESSION_NONE) {
    session_start();
}

function Att_status_whatsapp($UID, $id) {
    require (ROOT_PATH . '/Global/config.php');
    $pdo;

    try {
        // Conectar ao banco de dados usando PDO
        $pdo = new PDO($dsn, $db_user, $db_pass, $options);
        $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

        // Inicia uma transação
        $pdo->beginTransaction();

        // Atualizar o status na tabela Whatsapp para 1 onde o UID corresponde ao fornecido
        $stmtWhatsapp = $pdo->prepare("
            UPDATE soho_geral.Whatsapp
            SET Status = 1
            WHERE UID = :UID
        ");
        $stmtWhatsapp->bindParam(':UID', $UID, PDO::PARAM_STR);
        $stmtWhatsapp->execute();

        // Verifica se a atualização na tabela Whatsapp foi bem-sucedida
        if ($stmtWhatsapp->rowCount() > 0) {
            // Atualizar o StatusWhatsapp na tabela Corretores para 1
            $stmtCorretores = $pdo->prepare("
                UPDATE soho_geral.Corretores
                SET StatusWhatsapp = 1
                WHERE idCorretores = :idCorretor
            ");
            $stmtCorretores->bindParam(':idCorretor', $id, PDO::PARAM_INT);
            $stmtCorretores->execute();

            // Verifica se a atualização na tabela Corretores foi bem-sucedida
            if ($stmtCorretores->rowCount() > 0) {
                // Remover UID da sessão
                unset($_SESSION['UID']);
                
                // Finaliza a transação
                $pdo->commit();
                return true;
            } else {
                // Se a atualização na tabela Corretores falhar, reverte a transação
                $pdo->rollBack();
                return false;
            }
        } else {
            // Se a atualização na tabela Whatsapp falhar, reverte a transação
            $pdo->rollBack();
            return false;
        }
    } catch (PDOException $e) {
        // Em caso de erro, reverte a transação e exibe a mensagem de erro
        $pdo->rollBack();
        echo "Erro: " . $e->getMessage();
        return false;
    }
}
?>
