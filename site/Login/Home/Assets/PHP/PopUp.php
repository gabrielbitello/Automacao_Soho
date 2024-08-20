<?php
function PopUp($title, $content){
    echo '
        <div class="popup-overlay" id="popup" style="display: flex;">
            <div class="popup-content">
                <div class="popup-header">
                    ' . $title . '
                </div>
                <div class="popup-body">
                    ' . $content . '
                </div>
                <div class="popup-footer">
                    <button onclick="closePopup()">Fechar</button>
                </div>
            </div>
        </div>
    ';
};
?>