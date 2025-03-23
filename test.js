function onEdit(e) {
    var sheet = e.source.getActiveSheet();
    var editedRow = e.range.getRow();
    var nextRow = editedRow + 1;

    // Получаем значение следующей строки в первом столбце (A)
    var nextRowValue = sheet.getRange(nextRow, 1).getValue();

    // Если в следующей строке написано "ИТОГО за день", вставляем новую строку перед ней
    if (nextRowValue == "ИТОГО за день") {
        sheet.insertRowBefore(nextRow);

        // Копируем значение из A[editedRow] в новую строку
        var prevValue = sheet.getRange(editedRow, 1).getValue();
        sheet.getRange(nextRow, 1).setValue(prevValue);

        // Обновляем формулы в столбцах D-I в строке "ИТОГО за день" (которая теперь находится на row = nextRow+1)
        var totalRow = nextRow + 1;
        var columns = ['D', 'E', 'F', 'G', 'H', 'I'];
        for (var i = 0; i < columns.length; i++) {
            var cell = sheet.getRange(totalRow, columnToLetter(columns[i]));
            var formula = cell.getFormula();
            if (formula) {
                // Заменяем только номер строки конца диапазона в формуле вида =Сумм(ПЕРВАЯ_ЯЧЕЙКА:ВТОРАЯ_ЯЧЕЙКА)
                var updatedFormula = formula.replace(/(=Сумм\([A-Z]+\d+:[A-Z]+)(\d+)(\).*)/i, function (match, p1, p2, p3) {
                    return p1 + nextRow + p3;
                });
                cell.setFormula(updatedFormula);
            }
        }
    }
}

function columnToLetter(col) {
    var letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
    return letters.indexOf(col) + 1;
}
