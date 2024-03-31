$(document).ready(function(){
    const GAME_STATUS = ['WALKING', 'FIGHTING', 'TALKING', 'LOOKING']

    // Функция для обновления данных об окне
    function updateWindow() {
        $.ajax({
            type: 'GET',
            url: '/get-window',
            success: function(response){
                // Обновляем окно с помощью данных из JSON-ответа
                updateWindowView(response);
            },
            error: function(xhr, status, error){
                console.error('Произошла ошибка при обновлении окна.');
            }
        });
    }

    // Обновляем окно при загрузке страницы
    updateWindow();

    // Функция для обновления визуального представления окна
    function updateWindowView(data) {
        console.log(data.game_status)

        switch (data.game_status) {
            case GAME_STATUS[0]:
                break;
            case GAME_STATUS[1]:
                if (data.enemy) {
                    // Противник
                    var enemy_name = data.enemy.name;
                    var enemy_max_health = data.enemy.max_health;
                    var enemy_health = data.enemy.health;
                    var enemy_level = data.enemy.level;
                    var enemy_note = data.enemy.note;
                    var enemy_is_alive = data.enemy.is_alive;

                    var characterHtml = '';
                    characterHtml += "<img src='https://via.placeholder.com/150' alt='Image'>"
                    characterHtml += "<h2>" + enemy_name + "</h2>"
                    characterHtml += "<p>" + enemy_note + "</p>"
                    characterHtml += "<div class='health-bar'><div class='bar' style='width: " +
                        (enemy_health/enemy_max_health) * 100 + "%;'></div></div>";

                    console.log(enemy_health)
                    console.log(enemy_max_health)

                    $('.info').html(characterHtml);
                } else {
                    console.log('ошибка при получении противника')
                }

                var actionsHtml = '';

                if (data.player_weapon)
                    actionsHtml += "<a href=`{{url_for('attack')}}`>Атаковать " + data.player_weapon.name + "</a><br>";
                else
                    actionsHtml += "<a href='{{url_for(`attack`)}}'>Атаковать рукой</a><br>";

                if (data.player_consumable1)
                    actionsHtml += "<a href='/use_consumable'>" + data.player_consumable1.name + "</a><br>";
                if (data.player_consumable2)
                    actionsHtml += "<a href='/use_consumable'>" + data.player_consumable2.name + "</a><br>";
                if (data.player_consumable3)
                    actionsHtml += "<a href='/use_consumable'>" + data.player_consumable3.name + "</a><br>";

                $('.actions').html(actionsHtml);

                break;
            case GAME_STATUS[2]:
                break;
            case GAME_STATUS[3]:
                break;
            default:
                console.log("Wrong game_status: " + data.game_status)
                break;
        }
    }
});