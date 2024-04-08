$(document).ready(function() {
    // Функция для обновления данных о инвентаре
    function updateInventory() {
        $.ajax({
            type: 'GET',
            url: '/get-inventory',
            success: function (response) {
                // Обновляем инвентарь с помощью данных из JSON-ответа
                updateInventoryView(response);
            },
            error: function (xhr, status, error) {
                console.error('Произошла ошибка при обновлении инвентаря.');
            }
        });
    }

    // Обновляем окно при загрузке страницы
    updateInventory();

    function updateInventoryView(data) {
        var items = data.items;
        console.log(items);

        for (var i = 0; i < items.length; i++) {
            var item = items[i];
            var itemId = 'item_' + i;
            var $itemImg = $('#' + itemId); // Выбираем элемент изображения

            if ($itemImg.length > 0) {
                // Если элемент изображения существует
                var itemSrc = '../static/img/items/' + item.name + '.png'; // Предполагаем, что item.name содержит имя файла изображения
                $itemImg.attr('src', itemSrc); // Обновляем источник изображения
                $itemImg.attr('alt', item.name); // Обновляем атрибут alt при необходимости
            } else {
                console.error('Элемент изображения с id ' + itemId + ' не найден.');
            }

            var weapon = data.weapon;
            var armor = data.armor;
            var consumable1 = data.consumable1;
            var consumable2 = data.consumable2;
            var consumable3 = data.consumable3;

        
        }

        updateElement('#weapon', weapon.name);
        updateElement('#armor', armor.name);
        updateElement('#consumable1', consumable1.name);
        updateElement('#consumable2', consumable2.name);
        updateElement('#consumable3', consumable3.name);
    }

    function updateElement(selector, name) {
        $(selector + ' img').attr('src', `../static/img/items/${name}.png`);
        $(selector + ' p').text(name);
    }


    $(document).on('click', '.item-link', function(e) {
        e.preventDefault(); // Предотвращаем выполнение стандартного действия
        var itemIndex = $(this).data('index'); // Предполагаем, что атрибут data-index содержит индекс элемента
        $.ajax({
            type: 'POST',
            url: '/get-item/',
            data: {'item': itemIndex}, // Отправляем индекс элемента на сервер
            success: function(response) {
                console.log(response);
                if (response.name) {
                    updateItem(response);
                }
            },
            error: function(xhr, status, error) {
                console.error('Ошибка при получении элемента:', error);
            }
        });
    });

    function updateItem(data) {
        var itemName = data.name;
        var itemNote = data.note;
        $('.info img').attr('src', '../static/img/items/' + itemName + '.png');
        $('.info h2').text(itemName);
        $('.info p').text(itemNote);
    }
});
