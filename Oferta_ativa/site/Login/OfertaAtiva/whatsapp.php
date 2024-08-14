<?php
session_start();
include '../../Global/config.php';

if (!isset($_SESSION['user_id'])) {
    header("Location: login.html");
    exit();
}

$id = $_SESSION['user_id'];

try {
    $pdo = new PDO($dsn, $db_user, $db_pass, $options);
    $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

    // Verifica o status do WhatsApp
    $stmt = $pdo->prepare("SELECT StatusWhatsapp FROM Corretores WHERE idCorretores = :id LIMIT 1");
    $stmt->bindParam(':id', $id, PDO::PARAM_INT);
    $stmt->execute();
    $user = $stmt->fetch(PDO::FETCH_ASSOC);

    // Verifica o campo cod
    $stmt = $pdo->prepare("SELECT cod FROM Corretores WHERE idCorretores = :id LIMIT 1");
    $stmt->bindParam(':id', $id, PDO::PARAM_INT);
    $stmt->execute();
    $user = $stmt->fetch(PDO::FETCH_ASSOC);

    $cod = $user['cod'];
    $start_time = time();
    $timeout = 70;

    while (empty($cod) && (time() - $start_time) < $timeout) {
        sleep(5); 

        // Recarrega o valor do cod
        $stmt->execute();
        $user = $stmt->fetch(PDO::FETCH_ASSOC);
        $cod = $user['cod'];
    }

    // Início do HTML
    echo '<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Verificação do Código</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f5f5f5;
            color: #333;
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }
        .container {
            background-color: #ffffff;
            border-radius: 8px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            padding: 20px;
            max-width: 500px;
            text-align: center;
        }
        h1 {
            color: #5b5b5b;
        }
        p {
            margin: 15px 0;
        }
        .code {
            font-size: 2em;
            font-weight: bold;
            color: #4caf50;
        }
        .warning {
            color: #f44336;
            font-size: 1.2em;
        }
        .btn {
            display: inline-block;
            margin-top: 20px;
            padding: 10px 20px;
            font-size: 1em;
            color: #ffffff;
            background-color: #4caf50;
            border: none;
            border-radius: 4px;
            text-decoration: none;
        }
        .btn:hover {
            background-color: #45a049;
        }
    </style>
</head>
<body>
    <div class="container">';

    if ($user['StatusWhatsapp'] != 1) {
        echo '<h1>WhatsApp Desconectado</h1>
        <p>O WhatsApp está desconectado. Por favor, conecte-se ao WhatsApp para continuar.</p>';
    }

    if (empty($cod)) {
        echo '<p>O código ainda não está disponível.</p>
        <p>Por favor, tente novamente mais tarde.</p>';
    } else {
        echo '<h1>Código Encontrado!</h1>
        <p class="code">Código: ' . htmlspecialchars($cod) . '</p>
        <p class="warning">Você tem 4 minutos para cadastrar este código.</p>';
    }

    echo '<a href="OA.html" class="btn">Voltar para a oferta ativa</a>
    </div>
</body>
</html>';

} catch (PDOException $e) {
    echo "Erro: " . $e->getMessage();
}
?>
