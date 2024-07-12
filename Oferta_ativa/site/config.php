<?php

    $dbHost = "localhost";
    $dbUsername = "soho_geral";
    $dbPassword = "Soho2024!";
    $dbName = "soho_geral";

    $conn = new mysqli($dbHost,$dbUsername,$dbPassword,$dbName);

    if ($conn->connect_error) {
        die("Falha na conexão: " . $conn->connect_error);
    }
?>