$(document).ready(function(){
    const rowsCount = field.rows.length;
    const columnsCount = field.rows[0].cells.length;

    // Функция для обновления данных о поле
    function updateField() {
        $.ajax({
            type: 'GET',
            url: '/get-field',
            data: {X: 0, Y: 0}, // Параметры X и Y, замените на нужные значения
            success: function(response){
                // Обновляем поле с помощью данных из JSON-ответа
                updateFieldView(response);
            },
            error: function(xhr, status, error){
                console.error('Произошла ошибка при обновлении поля.');
            }
        });
    }

    // Обновляем поле при загрузке страницы
    updateField();

    // Обновляем поле при нажатии клавиш
    $(document).keydown(function(event) {
        var key = event.key;
        $.ajax({
            type: 'POST',
            url: '/move',
            data: {key: key}, // Отправляем нажатую клавишу на сервер для обработки движения
            success: function(response){
                // После успешного обновления положения игрока обновляем поле
                updateField();
            },
            error: function(xhr, status, error){
                console.error('Произошла ошибка при отправке данных о движении.');
            }
        });
    });

    // Функция для обновления визуального представления поля
    function updateFieldView(data) {
        $('#field td').removeClass('wall');
        $('#field td').removeClass('door');


        // Получаем координаты игрока
        var playerX = data.player.x;
        var playerY = data.player.y;

        // Добавляем класс 'wall' к ячейкам, соответствующим стенам
        data.walls.forEach(function(wall) {
            var wallX = Math.round(wall.x - playerX + columnsCount / 2) - 1;
            var wallY = Math.round(wall.y - playerY + rowsCount / 2) - 1;
            if (wallX >= 0 && wallX < columnsCount &&
                wallY >=0 && wallY < rowsCount) {
                $('#field tr:eq(' + wallY + ') td:eq(' + wallX + ')').addClass('wall');
            }
        });

        // Добавляем класс 'door' к ячейкам, соответствующим дверям
        data.doors.forEach(function(door) {
            var doorX = Math.round(door.x - playerX + columnsCount / 2) - 1;
            var doorY = Math.round(door.y - playerY + rowsCount / 2) - 1;
            console.log(doorY, doorX)
            if (doorX >= 0 && doorX < columnsCount &&
                doorY >= 0 && doorY < rowsCount) {
                $('#field tr:eq(' + doorY + ') td:eq(' + doorX + ')').addClass('door');
            }
        });
    }
});