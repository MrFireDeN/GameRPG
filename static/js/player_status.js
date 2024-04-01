$(document).ready(function(){
    // Функция для обновления данных о статусе
    function updatePLayerStatus() {
        $.ajax({
            type: 'GET',
            url: '/get-player-status',
            success: function(response){
                // Обновляем статус с помощью данных из JSON-ответа
                updateStatusView(response);
            },
            error: function(xhr, status, error){
                console.error('Произошла ошибка при обновлении статуса игрока.');
            }
        });
    }

    // Обновляем статус при загрузке страницы
    updatePLayerStatus();

    // Функция для обновления визуального представления статуса игрока
    function updateStatusView(data) {
        var health = data.health;
        var max_health = data.max_health;
        var level = data.level;
        var ep = data.ep;
        var money = data.money;

        playerStatusHtml = '';

        playerStatusHtml += "<div class='status-item'>Здоровье: <span id='health'>" + health + "/" + max_health + "</span></div>"
        playerStatusHtml += "<div class='status-item'>Уровень: <span id='level'>" + level + "</span></div>"
        playerStatusHtml += "<div class='status-item'>Монеты: <span id='coins'>" + money + "</span></div>"

        $(".status-bar").html(playerStatusHtml)

        /*
        <div class="status-item">
            Здоровье: <span id="health">100</span>
        </div>
        <div class="status-item">
            Уровень: <span id="level">5</span>
        </div>
        <div class="status-item">
            Монеты: <span id="coins">50</span>
        </div>
        */
    }
});