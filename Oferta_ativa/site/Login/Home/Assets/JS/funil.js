document.addEventListener('DOMContentLoaded', function () {
    // Configuração dos eventos para cada item e dropzone
    const items = document.querySelectorAll('.item');
    const dropzones = document.querySelectorAll('.dropzone');

    items.forEach(item => {
        item.addEventListener('dragstart', handleDragStart);
    });

    dropzones.forEach(dropzone => {
        dropzone.addEventListener('dragover', handleDragOver);
        dropzone.addEventListener('drop', handleDrop);
    });
});

function handleDragStart(e) {
    // Armazena o ID do item que está sendo arrastado
    e.dataTransfer.setData('text/plain', e.target.id);
}

function handleDragOver(e) {
    e.preventDefault(); // Permite que o drop aconteça
    e.dataTransfer.dropEffect = 'move';
}

function handleDrop(e) {
    e.preventDefault();

    const data = e.dataTransfer.getData('text/plain');
    const draggedItem = document.getElementById(data);
    const dropzone = e.target.closest('.dropzone');

    if (draggedItem && dropzone) {
        const oldStatus = draggedItem.getAttribute('data-status');
        const newStatus = dropzone.getAttribute('data-status');

        // Adiciona o item à lista da área de destino
        dropzone.querySelector('ul').appendChild(draggedItem);

        // Atualiza o atributo data-status do item
        draggedItem.setAttribute('data-status', newStatus);

        // Atualiza o status do item no servidor
        updateItemStatus(draggedItem.id, oldStatus, newStatus, dropzone.id);
    }
}

function updateItemStatus(itemId, oldStatus, newStatus, newTableId) {
    const specialTransition = (oldStatus === 'Enviado' && newStatus === 'Interesse');

    fetch('update_status.php', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            id: itemId,
            oldStatus: oldStatus,
            newStatus: newStatus,
            newTableId: newTableId,
            specialTransition: specialTransition
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            console.log('Atualização bem-sucedida:', data);
        } else {
            console.error('Erro:', data.error);
        }
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}
