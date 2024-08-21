<?php
if (session_status() == PHP_SESSION_NONE) {
    session_start();
}

require (ROOT_PATH . '/Global/config.php');

header('Content-Type: application/json');

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $data = json_decode(file_get_contents('php://input'), true);

    if (isset($data['id']) && isset($data['oldStatus']) && isset($data['newStatus'])) {
        $itemId = $data['id'];
        $oldStatus = $data['oldStatus'];
        $newStatus = $data['newStatus'];
        $specialTransition = $data['specialTransition'] ?? false;

        try {
            // Conectar ao banco de dados usando PDO
            $pdo = new PDO($dsn, $db_user, $db_pass, $options);
            $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

            // Atualizar a posição do item no banco de dados
            $stmt = $pdo->prepare("UPDATE items SET status = :newStatus WHERE id = :itemId");
            $stmt->bindParam(':newStatus', $newStatus, PDO::PARAM_STR);
            $stmt->bindParam(':itemId', $itemId, PDO::PARAM_INT);

            if ($stmt->execute()) {
                // Se a transição for especial, execute a lógica adicional
                if ($specialTransition) {
                    // Lógica especial, como notificar ou atualizar registros
                    // Exemplo: Registrar a transição especial em outra tabela
                    $stmtSpecial = $pdo->prepare("INSERT INTO special_transitions (item_id, old_status, new_status) VALUES (:itemId, :oldStatus, :newStatus)");
                    $stmtSpecial->bindParam(':itemId', $itemId, PDO::PARAM_INT);
                    $stmtSpecial->bindParam(':oldStatus', $oldStatus, PDO::PARAM_STR);
                    $stmtSpecial->bindParam(':newStatus', $newStatus, PDO::PARAM_STR);
                    $stmtSpecial->execute();
                }
                echo json_encode(['success' => true]);
            } else {
                echo json_encode(['success' => false, 'error' => 'Failed to execute query']);
            }
        } catch (PDOException $e) {
            echo json_encode(['success' => false, 'error' => $e->getMessage()]);
        }
    } else {
        echo json_encode(['success' => false, 'error' => 'Invalid input']);
    }
}
?>
