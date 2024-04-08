const GAME_STATUS = ['WALKING', 'FIGHTING', 'TALKING', 'LOOKING']

$(document).ready(function(){
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


    // Обработчик события клика для ссылки "Атаковать"
    $(document).on('click', '.attack-link', function(e) {
        e.preventDefault(); // Предотвращаем стандартное действие по клику
        $.ajax({
            type: 'POST', // Метод запроса
            url: '/attack/', // URL-адрес, на который отправляется запрос
            success: function(response) { // Обработка успешного ответа
                updateChat(response);
                updateWindow(); // Обновляем окно
            },
            error: function(xhr, status, error) { // Обработка ошибки запроса
                console.error('Ошибка при выполнении атаки:', error);
                // Дополнительные действия при ошибке выполнения атаки
            }
        });
    });

    function updateChat(data)
    {
        var name = data.name
        var player_message = data.player_message
        var character_message = data.character_message

        console.log('Атака выполнена успешно.');

        saveMessages(player_message, character_message)
    }

    function loadChatHistory(name) {
        //удалаяем старые сообщения
        $('.chat').children().remove()

        // Загружаем сохраненные сообщения
        var loadedMessages = loadMessages(name);
        loadedMessages.forEach(message => {
            addMessage(message.player_message)
            addMessage(message.character_message)
        })
    }

    // Функция для сохранения новых сообщений
    function saveMessages(player_message, character_message) {
        // Получаем текущий массив сообщений из localStorage
        var chatMessages = JSON.parse(localStorage.getItem('chatMessages')) || [];

        // Добавляем новые сообщения
        chatMessages.push({player_message: player_message, character_message: character_message });

        // Сохраняем обновленный массив сообщений
        localStorage.setItem('chatMessages', JSON.stringify(chatMessages));
    }

    // Функция для загрузки сохраненных сообщений
    function loadMessages(name) {
        // Получаем текущий сохраненный name
        var savedName = localStorage.getItem('chatName');

        // Если текущее имя не совпадает с сохраненным, обнуляем массив сообщений
        if (savedName !== name) {
            localStorage.setItem('chatMessages', JSON.stringify([])); // Обнуляем массив сообщений
            localStorage.setItem('chatName', name); // Сохраняем новое имя
        }

        // Получаем массив сообщений из localStorage
        var chatMessages = JSON.parse(localStorage.getItem('chatMessages')) || [];

        return chatMessages;
    }

    Storage.prototype.setObject = function(key, value) {
        this.setItem(key, JSON.stringify(value));
    }

    Storage.prototype.getObject = function(key) {
        var value = this.getItem(key);
        return value && JSON.parse(value);
    }

    // Функция для добавления нового сообщения в чат
    function addMessage(message)
    {
        console.log("Добавить сообщение: " + message)

        // Выбираем блок чата с помощью jQuery
        var $chat = $('.chat');

        // Создаем элемент div с классом 'message' и текстом сообщения
        var $messageDiv = $('<div>').addClass('message').text(message);

        // Добавляем сообщение в чат
        $chat.append($messageDiv);

        // Прокрутка вниз, чтобы показать новое сообщение
        $chat.scrollTop($chat.prop('scrollHeight'));
    }

    // Функция для обновления визуального представления окна
    function updateWindowView(data) {
        console.log(data.game_status)
        loadChatHistory(data.name);

        switch (data.game_status) {
            case GAME_STATUS[0]:
                if (data.name && data.note) {
                    var levelHtml = '';
                    //levelHtml += "<img src='../img/" + data.name + ".png' alt='Image'>"
                    levelHtml += "<h2>" + data.name + "</h2>"
                    levelHtml += "<p>" + data.note + "</p>"

                    $('.info').html(levelHtml);
                }
                else {
                    console.log('ошибка при получении уровня');
                }

                var actionsHtml = '';

                actionsHtml += "<a href=`{{url_for('look')}}`>Осмотреть</a><br>"

                $('.actions').html(actionsHtml);

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
                    characterHtml += "<img src='../img/characters/" + enemy_name + ".png' alt='Image'>"
                    characterHtml += "<h2>" + enemy_name + "</h2>"
                    characterHtml += "<p>" + enemy_note + "</p>"
                    characterHtml += "<div class='health-bar'><div class='bar' style='width: " +
                        (enemy_health/enemy_max_health) * 100 + "%;'></div></div>";

                    console.log(enemy_health);
                    console.log(enemy_max_health);

                    $('.info').html(characterHtml);
                } else {
                    console.log('ошибка при получении противника');
                }

                var actionsHtml = '';

                if (data.player_weapon)
                    actionsHtml += `<a href='#' class='attack-link'>Атаковать ` + data.player_weapon.name + "</a><br>";
                else
                    actionsHtml += "<a href=`{{url_for('attack')}}`>Атаковать рукой</a><br>";

                if (data.player_consumable1)
                    actionsHtml += "<a href='/use_consumable'>Использовать " + data.player_consumable1.name + "</a><br>";
                if (data.player_consumable2)
                    actionsHtml += "<a href='/use_consumable'>Использовать " + data.player_consumable2.name + "</a><br>";
                if (data.player_consumable3)
                    actionsHtml += "<a href='/use_consumable'>Использовать " + data.player_consumable3.name + "</a><br>";

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
