<?php
session_start();
require '../../Global/config.php';

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $username = trim($_POST['username']);
    $password = trim($_POST['password']);
    
    try {
        $pdo = new PDO($dsn, $db_user, $db_pass, $options);
        $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

        // Preparação da consulta para evitar SQL Injection
        $stmt = $pdo->prepare("SELECT idCorretores, Numero, SenhaCRMX FROM Corretores WHERE Numero = :username LIMIT 1");
        $stmt->bindParam(':username', $username, PDO::PARAM_STR);
        $stmt->execute();
        
        // Verifica se o usuário existe
        if ($stmt->rowCount() > 0) {
            $user = $stmt->fetch(PDO::FETCH_ASSOC);
            
            // Verifica a senha
            if (password_verify($password, $user['password'])) {
                // Autenticação bem-sucedida
                $_SESSION['user_id'] = $user['id'];
                header("Location: dashboard.php");
                exit();
            } else {
                // Senha incorreta
                echo "Usuário ou senha inválidos.";
            }
        } else {
            // Usuário não encontrado
            echo "Usuário ou senha inválidos.";
        }
    } catch (PDOException $e) {
        echo "Erro: " . $e->getMessage();
    }
}
?>
