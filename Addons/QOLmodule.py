class QOL:
    """
    Класс QOL (Quality of Life) содержит вспомогательные методы для работы с текстом, 
    обработкой данных сотрудников и управления Google Sheets через API.

    Методы:
        replace_letter(letter: str) -> str:
            Заменяет английские буквы A, O, C на соответствующие русские аналоги.

        is_valid_price(cell_value: str) -> bool:
            Проверяет, соответствует ли строка формату цены с окончанием ",00".

        makeDictEmpTot(emp_shift: list) -> dict:
            Преобразует список смен сотрудников в словарь с их общим временем смен.

        process_employees(worksheet: object) -> dict:
            Обрабатывает данные сотрудников из строки 20 рабочего листа Google Sheets 
            и создает словарь, где ключ — имя сотрудника, а значение — порядковый номер.

        clear_wgslist_ranges(service: object, spreadsheet_id: str) -> None:
            Очищает заданные диапазоны данных в таблице Google Sheets.

        toggle_cell_value(sheet: object, days_in_month: int) -> None:
            (Метод не реализован) Переключает значения ячеек в зависимости от количества дней в месяце.
    """

    def replace_letter(letter: str) -> str:
        """Меняет английские А и О, С на русские"""
        return {"A": "А", "O": "О","C": "О","С":"О"}.get(letter, letter)

    def is_valid_price(cell_value:str) -> bool:
        """Проверяет, соответствует ли строка формату цены с ,00 в конце."""
        if ",00"  in cell_value:
            return True
        else:
            return False
        
    def makeDictEmpTot (emp_shift:list) -> dict:
        """emp_shift list to dictionary"""
        employee_totals = {}

        for employee, shift, j_ , i_, o_ in emp_shift:
            if employee in employee_totals:
                employee_totals[employee] += shift  
            else:
                employee_totals[employee] = shift  
        return employee_totals

    def process_employees(worksheet:object) -> dict:
        """
        Обрабатывает сотрудников из двух строк рабочего листа Google Sheets:

        Для строки 20:
        - Начинаем с колонки D (индекс 3).
        - Перебираем ячейки до ячейки, содержащей "Коменда".
        - Аналогичным образом обрабатываем значение ячейки, заменяя пустые на "_" и присваивая порядковый номер.

        Args:
            worksheet: объект рабочего листа Google Sheets.
            
        Returns:
            словарь:
            - Второй словарь (row20_dict): ключ — значение ячейки (или "_" для пустых), значение — порядковый номер в строке 20.
        """

        # Обработка строки 20
        row20_dict = {}
        order20 = 1
        row20 = worksheet.row_values(20)  # Получаем всю строку 20 в виде списка
        cntr = 0
        for cell in row20[3:]:  # начинаем с колонки D (индекс 3)
            if cell == "Коменда":
                break
            employee = cell.strip() if cell and cell.strip() else f"Пропуск {cntr}"
            cntr += 1
            row20_dict[employee] = order20
            order20 += 1
        print("печатаю список сотрудников взятых из таблицы\n",row20_dict)
        return row20_dict

    def clear_wgslist_ranges(service:object, spreadsheet_id:str)-> None:
        """
        Удаляет данные из заданных диапазонов в таблице WGSlist.
        Args:
            service(object): Авторизованный объект сервиса Google Sheets API.
            spreadsheet_id: ID таблицы Google Sheets.
        :return nothing: haha lol
        """
        ranges = [
            "WGSlist!D21:P51",
            "WGSlist!D97:D111",
            "WGSlist!Q21:T51",
            "WGSlist!D59:P89"
        ]

        try:
            body = {
                "ranges": ranges
            }
            service.spreadsheets().values().batchClear(
                spreadsheetId=spreadsheet_id, body=body
            ).execute()
            print("Данные успешно удалены из указанных диапазонов.")
        except Exception as e:
            print(f"Ошибка при удалении данных: {e}")

    def toggle_cell_value(sheet: object, days_in_month: int) -> None:
        """
        Функция принимает объект листа и меняет значение ячейки E93 на листе WGSlist:
        если текущее значение равно "31", меняет на "15", иначе – на "31".

        Args:
            sheet(object): Объект листа (например, gspread.Worksheet), содержащий лист WGSlist.
            days_in_month(int): ключ внутри ячейки
        """
        try:
            cell = sheet.acell('E93')
            current_value = cell.value.strip() if cell.value else ""

            if str(days_in_month) != current_value:
                new_value = "31" if str(days_in_month) == "31" else "15"
                # Обновляем значение ячейки E93
                sheet.update_acell('E93', new_value)
                print(f"Значение ячейки E93 изменено с {current_value} на {new_value}")
        except Exception as e:
            print(f"Ошибка при обновлении ячейки: {e}")