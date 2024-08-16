<?php
session_start();
include '../../../Global/config.php';

// Verifica se a sessão foi iniciada e se o ID do corretor está definido
if (!isset($_SESSION['user_id'])) {
    header("Location: login.html");
    exit();
}

$id = $_SESSION['user_id'];

try {
    $pdo = new PDO($dsn, $db_user, $db_pass, $options);
    $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

    // Verifica o status do WhatsApp na tabela Corretores
    $stmt = $pdo->prepare("SELECT StatusWhatsapp FROM Corretores WHERE idCorretores = :id LIMIT 1");
    $stmt->bindParam(':id', $id, PDO::PARAM_INT);
    $stmt->execute();
    $user = $stmt->fetch(PDO::FETCH_ASSOC);

    if ($user['StatusWhatsapp'] != 1) {
        header("Location: whatsapp.php");
        exit();
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
            $erros[] = "O número deve estar entre 1 e 350.";
        }

        // Exibe erros, se houver
        if (!empty($erros)) {
            foreach ($erros as $erro) {
                echo "<p style='color: red;'>$erro</p>";
            }
            echo "<a href='index.html'>Voltar</a>";
            exit;
        }

        // Verifica o limite diário de ofertas ativas
        $dataAtual = date("Y-m-d");
        $stmt = $pdo->prepare("
            SELECT SUM(total) AS total_ofertas
            FROM ofertas_ativa
            WHERE ID_Corretor = :id AND DATE(h_registro) = :dataAtual
        ");
        $stmt->bindParam(':id', $id, PDO::PARAM_INT);
        $stmt->bindParam(':dataAtual', $dataAtual, PDO::PARAM_STR);
        $stmt->execute();
        $resultado = $stmt->fetch(PDO::FETCH_ASSOC);

        $total_ofertas = $resultado['total_ofertas'] ? $resultado['total_ofertas'] : 0;
        $limite_diario = 100;
        $disponivel = $limite_diario - $total_ofertas;

        if ($numero > $disponivel) {
            echo "<p style='color: red;'>Você não pode enviar mais $numero ofertas hoje. Você ainda tem $disponivel ofertas disponíveis no limite diário.</p>";
            echo "<a href='index.html'>Voltar</a>";
            exit();
        }

        // Processamento dos dados
        if ($PE) {
            // Lógica para quando Pessoas Específicas está marcado
            $sql = "INSERT INTO ofertas_ativa (total, ativa, mensagem, pessoa, numero, nome_pessoa, nome_passou, h_registro, ID_Corretor) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)";
            $stmt = $pdo->prepare($sql);
            $stmt->execute([$numero, $ativa, $mensagem, $pessoa, $Numero_telefone, $Nome_cliente, $Nome, $h_registro, $id]);
        } else {
            // Lógica para quando Pessoas Específicas não está marcado
            $sql = "INSERT INTO ofertas_ativa (total, ativa, mensagem, restante, h_registro, ID_Corretor) VALUES (?, ?, ?, ?, ?, ?)";
            $stmt = $pdo->prepare($sql);
            $stmt->execute([$numero, $ativa, $mensagem, $numero, $h_registro, $id]);
        }

        if ($stmt) {
            // Atualiza a quantidade de ofertas após o envio
            $total_ofertas += $numero;
            $disponivel = $limite_diario - $total_ofertas;
            echo "<p>Formulário enviado com sucesso!</p>";
            if ($disponivel > 0) {
                echo "<p>Você ainda pode enviar mais $disponivel ofertas hoje.</p>";
            } else {
                echo "<p>Você atingiu o limite diário de ofertas.</p>";
            }
        } else {
            echo "<p>Erro ao enviar formulário: " . $stmt->errorInfo()[2] . "</p>";
        }

    } else {
        // Redireciona de volta para o formulário se o acesso não for via POST
        header("Location: index.html");
        exit();
    }

    // Redireciona para OA.html se tudo estiver ok
    header("Refresh: 8; URL=OA.html");
    exit();

} catch (PDOException $e) {
    echo "Erro: " . $e->getMessage();
}
?>
