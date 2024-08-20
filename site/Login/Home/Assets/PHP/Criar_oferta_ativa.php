<?php

function Registrar_Oferta($mensagem, $numero, $id){
    require (ROOT_PATH . '/Global/config.php');

    $pdo = new PDO($dsn, $db_user, $db_pass, $options);
    $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

    // Inicializa variáveis
    $ativa = 1;
    $pessoa = 1;
    $h_registro = date("Y-m-d H:i:s");

    $PE = isset($_POST['PE']) ? true : false;
    $Numero_telefone = $_POST['Numero_telefone'] ?? null;
    $Nome_cliente = $_POST['Nome_cliente'] ?? null;
    $Nome = $_POST['Nome'] ?? null;

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
}

?>