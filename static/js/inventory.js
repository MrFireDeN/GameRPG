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
            var $itemImg = $('#' + itemId); // Select the image element

            if ($itemImg.length > 0) {
                // If the image element exists
                var itemSrc = '../static/img/items/' + item.name + '.png'; // Assuming item.name holds the image filename
                $itemImg.attr('src', itemSrc); // Update the image source
                $itemImg.attr('alt', item.name); // Update the alt attribute if needed
            } else {
                console.error('Image element with id ' + itemId + ' not found.');
            }

            var weapon = data.weapon;
            var armor = data.armor;
            var consumable1 = data.consumable1;
            var consumable2 = data.consumable2;
            var consumable3 = data.consumable3;

            // Update weapon
            if (weapon) {
                $('#weapon img').attr('src', '../static/img/items/' + weapon.name + '.png');
                $('#weapon p').text(weapon.name);
            }

            // Update armor
            if (armor) {
                $('#armor img').attr('src', '../static/img/items/' + armor.name + '.png');
                $('#armor p').text(armor.name);
            }

            // Update consumable1
            if (consumable1) {
                $('#consumable1 img').attr('src', '../static/img/items/' + consumable1.name + '.png');
                $('#consumable1 p').text(consumable1.name);
            }

            // Update consumable2
            if (consumable2) {
                $('#consumable2 img').attr('src', '../static/img/items/' + consumable2.name + '.png');
                $('#consumable2 p').text(consumable2.name);
            }

            // Update consumable3
            if (consumable3) {
                $('#consumable3 img').attr('src', '../static/img/items/' + consumable3.name + '.png');
                $('#consumable3 p').text(consumable3.name);
            }
        }
    }

    $(document).on('click', '.item-link', function(e) {
        e.preventDefault(); // Prevent the default action
        var itemIndex = $(this).data('index'); // Assuming data-index attribute contains the item index
        $.ajax({
            type: 'POST',
            url: '/get-item/',
            data: {'item': itemIndex}, // Send item index to the server
            success: function(response) {
                console.log(response);
                if (response.name) {
                    updateItem(response);
                }
            },
            error: function(xhr, status, error) {
                console.error('Error while retrieving item:', error);
            }
        });
    });

    function updateItem(data) {
        name = data.name;
        note = data.note;

        $('.info img').attr('src', '../static/img/items/' + name + '.png');
        $('.info h2').text(name);
        $('.info p').text(note);
    }
});
