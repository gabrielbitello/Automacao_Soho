<?php
include 'config.php'; // Incluir o arquivo de configuração

// Verifica a conexão
if ($conn->connect_error) {
    die("Falha na conexão: " . $conn->connect_error);
}

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    // Inicializa variáveis
    $mensagem = $_POST['mensagem'];
    $numero = isset($_POST['numero']) ? intval($_POST['numero']) : null;
    $PE = isset($_POST['PE']) ? true : false;
    $Numero_telefone = isset($_POST['Numero_telefone']) ? $_POST['Numero_telefone'] : null;
    $Nome_cliente = isset($_POST['Nome_cliente']) ? $_POST['Nome_cliente'] : null;
    $Nome = isset($_POST['Nome']) ? $_POST['Nome'] : null;
    $ativa = 1; // Exemplo de valor fixo para o campo ativa
    $pessoa = 1; // Exemplo de valor fixo para o campo pessoa
    $h_registro = date("Y-m-d H:i:s"); // Registro do horário atual

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
        $sql = "INSERT INTO ofertas_ativa (total, ativa, mensagem, pessoa, numero, nome_pessoa, nome_passou, h_registro) VALUES (?, ?, ?, ?, ?, ?, ?, ?)";
        $stmt = $conn->prepare($sql);
        $stmt->bind_param("iissssss", $numero, $ativa, $mensagem, $pessoa, $Numero_telefone, $Nome_cliente, $Nome, $h_registro);
    } else {
        // Lógica para quando Pessoas Específicas não está marcado
        $sql = "INSERT INTO ofertas_ativa (total, ativa, mensagem, h_registro) VALUES (?, ?, ?, ?)";
        $stmt = $conn->prepare($sql);
        $stmt->bind_param("iiss", $numero, $ativa, $mensagem, $h_registro);
    }

    if ($stmt->execute()) {
        echo "<p>Formulário enviado com sucesso!</p>";
    } else {
        echo "<p>Erro ao enviar formulário: " . $stmt->error . "</p>";
    }

    header("Refresh: 8; URL=index.html");
    $stmt->close();
} else {
    // Redireciona de volta para o formulário se o acesso não for via POST
    header("Location: index.html");
    exit;
}

$conn->close();
?>