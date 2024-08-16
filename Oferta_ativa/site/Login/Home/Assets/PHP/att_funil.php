<?php
header('Content-Type: application/json');

$data = json_decode(file_get_contents('php://input'), true);

if (isset($data['id']) && isset($data['oldStatus']) && isset($data['newStatus'])) {
    $itemId = $data['id'];
    $oldStatus = $data['oldStatus'];
    $newStatus = $data['newStatus'];
    $specialTransition = $data['specialTransition'] ?? false;

    // Conectar ao banco de dados
    $conn = new mysqli('localhost', 'username', 'password', 'database');

    if ($conn->connect_error) {
        die("Connection failed: " . $conn->connect_error);
    }

    // Atualizar a posição do item no banco de dados
    $stmt = $conn->prepare("UPDATE items SET status = ? WHERE id = ?");
    $stmt->bind_param("si", $newStatus, $itemId);

    if ($stmt->execute()) {
        // Se a transição for especial, execute a lógica adicional
        if ($specialTransition) {
            // Lógica especial, como notificar ou atualizar registros
            // Exemplo: Registrar a transição especial em outra tabela
            $stmtSpecial = $conn->prepare("INSERT INTO special_transitions (item_id, old_status, new_status) VALUES (?, ?, ?)");
            $stmtSpecial->bind_param("iss", $itemId, $oldStatus, $newStatus);
            $stmtSpecial->execute();
            $stmtSpecial->close();
        }
        echo json_encode(['success' => true]);
    } else {
        echo json_encode(['success' => false, 'error' => $stmt->error]);
    }

    $stmt->close();
    $conn->close();
} else {
    echo json_encode(['success' => false, 'error' => 'Invalid input']);
}
?>
EXEMPLO