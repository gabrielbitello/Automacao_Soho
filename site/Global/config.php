<?php
require_once 'config_path.php';

// Mysql database credentials
$host = 'localhost';
$db = 'soho_geral';
$db_user = 'soho_geral';
$db_pass = 'Soho2024!';
$dsn = "mysql:host=$host;dbname=$db;charset=utf8mb4";

$options = [
    PDO::ATTR_ERRMODE            => PDO::ERRMODE_EXCEPTION,
    PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
    PDO::ATTR_EMULATE_PREPARES   => false,
];
?>
