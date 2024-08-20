<?php
session_start();
include '../../Global/config.php';
include 'Assets/PHP/Criar_oferta_ativa.php';
include 'Assets/PHP/PopUp.php';
include 'Assets/PHP/Pedido_Cod_WhatsApp.php';
include 'Assets/PHP/Status_WhatsApp.php';
include 'Assets/PHP/att_status_whatsapp.php';
include 'Assets/PHP/COD_whatsapp.php';

ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);
error_reporting(E_ALL);


if (!isset($_SESSION['user_id'])) {
    header('Location: ../Login/Login.php');
    exit;
}

$id_User = $_SESSION['user_id'];
$UID = $_SESSION['UID'] ?? null;

$id = $_POST['id'] ?? 0;
$Popup = null;
$COD = null;

$SW = $_POST['att_status_whatsapp'] ?? '0';
if ($SW == 1) {
    Att_status_whatsapp($UID, $id_User);
}


if ($_SERVER["REQUEST_METHOD"] == "POST" && $id != 0) {
    $numero = $_POST['numero'] ?? '0';
    $mensagem = $_POST['mensagem'] ?? '0';
    $Popup = $_POST['popup'] ?? null;

    switch ($id) {
        case 1:
            if ($numero != 0) {
                if (WhatsAppStatus($id_User) != 1) {
                    $Popup = 2;
                    RequestWatsAppCode($id_User);
                    break;
                }
                Registrar_Oferta($mensagem, $numero, $id_User);
                $Popup = 1;
            } else {
                $Erro = 'Ocorreu um erro ao enviar a oferta.';
                $Popup = 0;
            }
            $id = null;
            break;
        case 2:
            $UID = $_POST['UID'] ?? null;
            $COD = WatsAppCOD($UID);
            $Popup = 2;
            $id = null;
            break;
        case 3:
            // Ação para o caso 2
            echo "Caso 2 executado.";
            $id = null;
            break;
        default:
            // Ação para qualquer outro valor
            echo "Valor não reconhecido.";
            $id = null;
            break;
    }
}









if ($Popup != null) {
    switch ($Popup) {
        case 0:
            $titulo = '<div>
                            <h1 id="PopUp-ERRO">Erro</h1>
                            <svg class="PopUp-ERRO"><use xlink:href="../../Global/SVG/alert.svg#alert"></use></svg>
                        </div>
                    ';
            $Corpo = '<div>
                        <h2 id="PopUp-ERRO">ERRO: '.$Erro.'</h2>
                    </div>
                ';
            PopUp($titulo, $Corpo);
            break;
        case 1:
            $titulo = '<div>
                            <h1 id="PopUp-OA">Oferta Ativa</h1>
                        </div>
                    ';
            $Corpo = '<div>
                        <h2 id="PopUp-OA">Oferta ativa enviada com sucesso, iniciando em ate 1 minuto</h2>
                    </div>
                ';
            PopUp($titulo, $Corpo);
            break;
        case 2:
            $titulo = '<div>
                            <h1 id="PopUp-OA"WhatsApp</h1>
                            <svg class="PopUp-ERRO"><use xlink:href="../../Global/SVG/alert.svg#alert"></use></svg>
                        </div>
                    ';
            if ($COD == null) {
                $Corpo = '<div>
                        <h2 id="PopUp-OA">O WhatsApp não está conectado...</h2>
                        <p>Aguarde alguns instantes por um código</p>
                    </div>
                    <div>
                        <p>Aperte o botão para verificar se o código já existe, isso pode levar até 2 minutos</p>
                        <form method="post" action="Home.php">
                            <input type="hidden" name="id" value="2">
                            <input type="hidden" name="popup" value="2">
                            <button>Buscar</button>
                        </form>
                    </div>
                ';
            } else {
                $Corpo = '<div>
                        <h2 id="PopUp-OA">O WhatsApp não está conectado...</h2>
                        <p>Verifique se o código foi gerad</p>
                    </div>
                    <div>
                        <p>Acesse seu WhatsApp e adicione uma conexão, ao apertar para escanear selecione usar código</p>
                        <p>'.$COD.'</p>
                        <form method="post" action="Home.php">
                            <input type="hidden" name="att_status_whatsapp" value="1">
                            <button>Confirmar</button>
                        </form>
                    </div>
                ';
            }
            
            PopUp($titulo, $Corpo);
            break;
        default:
            break;
    }
}


?>
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sistema de Automação</title>
    <link rel="stylesheet" href="Assets/CSS/reset.css">
    <link rel="stylesheet" href="Assets/CSS/Style.css">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
</head>
<body>
    <header>
        <nav id="nav1">
            <ul>
                <li><a href="#">Status</a></li>
                <li><a href="#">Suporte</a></li>
                <li><a href="#">Notificacoes</a></li>
            </ul>
            <a href="#" id="Perfil"><svg class="user"><use xlink:href="../../Global/SVG/user.svg#user"></use></svg></a>
        </nav>
    </header>
    <main>
        <nav id="nav2">
            <ul>
                <li><a href="#">Funil</a></li>
                <li><a href="OfertaAtiva/OA.html">Oferta ativa</a></li>
                <li><a href="#">Documentos</a></li>
                <li><a href="#">Estatísticas</a></li>
            </ul>
        </nav>
        <div id="Funil">
            <h1>Funil de contatos</h1>
            <p>Veja o status de seus contatos e saiba em qual etapa do funil eles se encontram.</p>
            <nav>
                <ul>
                    <li><a href="#Enviado">Enviado</a></li>
                    <li><a href="#Interesse">Interesse</a></li>
                    <li><a href="#Aguardando">Aguardando</a></li>
                    <li><a href="#Visita">Visita</a></li>
                    <li><a href="#Proposta">Proposta</a></li>
                    <li><a href="#Fechado">Fechado</a></li>
                    <li><a href="#">Pesquisa</a></li>
                    <li><a href="#">ADD</a></li>
                </ul>
            </nav>
            <div class="Grafico-funil">
                <div id="Enviado" class="dropzone">
                    <h2>Enviado</h2>
                    <ul>
                        <li class="draggable" draggable="true">
                            <div>
                                <p>Nome: Fulano de tal e tal</p>
                                <p>Numero: +55 41 99999-9999</p>
                            </div>
                            <div>
                                <button>Editar</button>
                                <button>Remover</button>
                            </div>
                        </li>
                    </ul>
                </div>
                <div id="Interesse" class="dropzone" data-status="Enviado">
                    <h2>Interesse</h2>
                    <ul>
                        <li id="Fulano2" class="draggable" draggable="true"  data-status="Enviado">
                            <div>
                                <p>Nome: Fulano de tal e tal</p>
                                <p>Numero: +55 41 99999-9999</p>
                            </div>
                            <div>
                                <button>Editar</button>
                                <button>Remover</button>
                            </div>
                        </li>
                    </ul>
                </div>
                <div id="Aguardando" class="dropzone" data-status="Enviado">
                    <h2>Aguardando</h2>
                    <ul>
                        <li class="draggable" draggable="true" data-status="Enviado">
                            <div>
                                <p>Nome: Fulano de tal e tal</p>
                                <p>Numero: +55 41 99999-9999</p>
                            </div>
                            <div>
                                <button>Editar</button>
                                <button>Remover</button>
                            </div>
                        </li>
                    </ul>
                </div>
                <div id="Visita" class="dropzone">
                    <h2>Visita</h2>
                    <ul>
                        <li class="draggable" draggable="true">
                            <div>
                                <p>Nome: Fulano de tal e tal</p>
                                <p>Numero: +55 41 99999-9999</p>
                                <p>Data: </p>
                            </div>
                            <div>
                                <button>Editar</button>
                                <button>Remover</button>
                            </div>
                        </li>
                    </ul>
                </div>
                <div id="Proposta" class="dropzone">
                    <h2>Proposta</h2>
                    <ul>
                        <li class="draggable" draggable="true">
                            <div>
                                <p>Nome: Fulano de tal e tal</p>
                                <p>Numero: +55 41 99999-9999</p>
                                <p>Data: 20/12/2100 18:40</p>
                                <p>Doc: 000.000.000-00</p>
                            </div>
                            <div>
                                <button>Editar</button>
                                <button>Remover</button>
                            </div>
                        </li>
                    </ul>
                </div>
                <div id="Fechado" class="dropzone">
                    <h2>Fechado</h2>
                    <ul>
                        <li class="draggable" draggable="true">
                            <div>
                                <p>Nome: Fulano de tal e tal</p>
                                <p>Numero: +55 41 99999-9999</p>
                                <p>Data: 20/12/2100 18:40</p>
                                <p>Doc: 000.000.000-00</p>
                            </div>
                            <div>
                                <button>Editar</button>
                                <button>Remover</button>
                            </div>
                        </li>
                    </ul>
                </div>
            </div>
        </div>



        <div id="Oferta_ativa">
            <section>
                <h1>Oferta Ativa</h1>
                <p>Envie mensagens personalizadas para seus clientes de forma rápida e eficiente.</p>
                <div class="grafico-container">
                    <div class="grafico-item">
                        <h2>Limite Diário de Ofertas</h2>
                        <canvas id="grafico-diario"></canvas>
                        <p class="valor-limite" style="display:none;">80</p>
                    </div>
                    <div class="grafico-item">
                        <h2>Limite Mensal de Ofertas</h2>
                        <canvas id="grafico-mensal"></canvas>
                        <p class="valor-limite" style="display:none;">250</p>
                    </div>
                </div>
            </section>
            <section class="formulario_OA">
                <h2>Solicitar oferta</h2>
                <form method="post" id="meuFormulario" action="Home.php">
                <select name="mensagem" id="opcoesSelect">
                    <option value="Neutro">Neutro</option>
                </select>
                <input type="number" id="inputNumero" name="numero" min="1" max="180">
                <input type="hidden" name="id" value="1"> 
                <button type="submit">OK</button>
            </form>

            </section>
        </div>
    </main>
    <!--<main>
        <div id="Documentos">
            
        </div>
    </main>
    <main>
        <div id="Estatisticas">
            
        </div>
        
    </main>-->
    <footer>
        <p>©2024 Sistema de Automação. Todos os direitos reservados.</p>
        <p>Contato: <a href="mailto:vg.bitello@gmail.com">vg.bitello@gmail.com</a></p>
    </footer>
    <script src="Assets/JS/graficos.js"></script>
    <script src="Assets/JS/funil.js"></script>
    <script>
        // Função para fechar o pop-up
        function closePopup() {
            document.getElementById("popup").style.display = "none";
        }
    </script>
</body>
</html>
