document.addEventListener('DOMContentLoaded', function() {
    const field = document.getElementById("field");
    const rowsCount = field.rows.length;
    const columnsCount = field.rows[0].cells.length;

    // Найти начальную позицию героя и установить ему класс "hero"
    var heroPosition = { row: 0, col: 0 }; // Например, начальная позиция (0, 0)
    var cells = document.querySelectorAll('#field td');
    var initialCellIndex = heroPosition.row * columnsCount + heroPosition.col; // Предполагается, что таблица имеет 15 столбцов
    cells[initialCellIndex].classList.add('hero');

    // Обработчик нажатия клавиш
    document.addEventListener('keydown', function(event) {
        var key = event.key;
        var newHeroPosition = { row: heroPosition.row, col: heroPosition.col };

        // Обработка нажатий клавиш
        if (key === 'ArrowUp' && newHeroPosition.row > 0) {
            newHeroPosition.row--;
        } else if (key === 'ArrowDown' && newHeroPosition.row < rowsCount-1) {
            newHeroPosition.row++;
        } else if (key === 'ArrowLeft' && newHeroPosition.col > 0) {
            newHeroPosition.col--;
        } else if (key === 'ArrowRight' && newHeroPosition.col < columnsCount-1) {
            newHeroPosition.col++;
        }

        // Удалить класс "hero" с текущей ячейки и добавить его к новой позиции
        cells[heroPosition.row * columnsCount + heroPosition.col].classList.remove('hero');
        cells[newHeroPosition.row * columnsCount + newHeroPosition.col].classList.add('hero');

        // Обновить позицию героя
        heroPosition = newHeroPosition;
    });
});