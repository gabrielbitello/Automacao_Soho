<?php
session_start();
include '../Global/config.php';

$id = $_SESSION['id'];

// Verifica a conexão usando PDO
try {
    $pdo = new PDO($dsn, $db_user, $db_pass, $options);
    $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
} catch (PDOException $e) {
    die("Falha na conexão: " . $e->getMessage());
}

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    // Inicializa variáveis
    $mensagem = $_POST['mensagem'];
    $numero = isset($_POST['numero']) ? intval($_POST['numero']) : null;
    $PE = isset($_POST['PE']) ? true : false;
    $Numero_telefone = isset($_POST['Numero_telefone']) ? $_POST['Numero_telefone'] : null;
    $Nome_cliente = isset($_POST['Nome_cliente']) ? $_POST['Nome_cliente'] : null;
    $Nome = isset($_POST['Nome']) ? $_POST['Nome'] : null;
    $ativa = 1; 
    $pessoa = 1; 
    $h_registro = date("Y-m-d H:i:s"); 

    // Validação básica
    $erros = [];
    if (empty($mensagem)) {
        $erros[] = "O campo mensagem é obrigatório.";
    }

    if ($PE && (empty($Numero_telefone) || empty($Nome_cliente))) {
        $erros[] = "O campo Número de telefone e Nome do cliente são obrigatórios quando Pessoas Específicas está marcado.";
    }

    if (!$PE && (is_null($numero) || $numero < 1 || $numero > 500)) {
        $erros[] = "O número deve estar entre 1 e 500.";
    }

    // Exibe erros, se houver
    if (!empty($erros)) {
        foreach ($erros as $erro) {
            echo "<p style='color: red;'>$erro</p>";
        }
        echo "<a href='index.html'>Voltar</a>";
        exit;
    }

    // Processamento dos dados
    if ($PE) {
        // Lógica para quando Pessoas Específicas está marcado
        $sql = "INSERT INTO ofertas_ativa (total, ativa, mensagem, pessoa, numero, nome_pessoa, nome_passou, h_registro, ID_Corretor) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)";
        $stmt = $pdo->prepare($sql);
        $stmt->execute([$numero, $ativa, $mensagem, $pessoa, $Numero_telefone, $Nome_cliente, $Nome, $h_registro, $id]);
    } else {
        // Lógica para quando Pessoas Específicas não está marcado
        $sql = "INSERT INTO ofertas_ativa (total, ativa, mensagem, restante, h_registro) VALUES (?, ?, ?, ?, ?)";
        $stmt = $pdo->prepare($sql);
        $stmt->execute([$numero, $ativa, $mensagem, $numero, $h_registro]);
    }

    if ($stmt) {
        echo "<p>Formulário enviado com sucesso!</p>";
    } else {
        echo "<p>Erro ao enviar formulário: " . $stmt->errorInfo()[2] . "</p>";
    }

    header("Refresh: 8; URL=index.html");
} else {
    // Redireciona de volta para o formulário se o acesso não for via POST
    header("Location: index.html");
    exit;
}
?>
