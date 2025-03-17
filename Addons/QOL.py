

class QOL:
    """
    The QOL class provides a set of static methods for various utility operations, 
    including string replacement, price validation, dictionary creation from lists, 
    employee processing from Google Sheets, clearing specific ranges in Google Sheets, 
    and ensuring/updating cell values in Google Sheets.

        Methods:
            replace_letter(letter: str) -> str:
                Replaces specific English letters (A, O, C) with their Russian counterparts.

            is_valid_price(cell_value: str) -> bool:
                Checks if a string matches the price format ending with ",00".

            makeDictEmpTot(emp_shift: list) -> dict:
                Converts a list of employee shifts into a dictionary with employee names as keys and total shifts as values.

            process_employees(worksheet: object) -> dict:
                Processes employees from row 20 of a Google Sheets worksheet, creating a dictionary with cell values or placeholders as keys and their order as values.

            clear_wgslist_ranges(service: object, spreadsheet_id: str) -> None:
                Clears data from specified ranges in a Google Sheets document.

            toggle_cell_value(sheet: object, days_in_month: int) -> None:
                Toggles the value of cell E93 in the WGSlist sheet between "31" and "15" based on the provided days_in_month.

            ensure_cell_value(sheet: object, days_in_month: int) -> None:
                Ensures that the value of cell E93 in the WGSlist sheet matches the provided days_in_month, updating it if necessary.
    """

    @staticmethod
    def replace_letter(letter: str) -> str:
        """
        Replaces Latin letters with their Cyrillic equivalents.
        Args:
            letter (str): The Latin letter to be replaced.
        Returns:
            str: The corresponding Cyrillic letter if a match is found; otherwise, returns the original letter.
        """
        
        return {"A": "А", "O": "О","C": "О","С":"О"}.get(letter, letter)

    @staticmethod
    def is_valid_price(cell_value:str) -> bool:
        """
        Checks if the string matches the price format ending with ',00'.

        Args:
            cell_value (str): The string to check.

        Returns:
            bool: True if the string ends with ',00', False otherwise.
        """
        if ",00"  in cell_value:
            return True
        else:
            return False

    @staticmethod
    def makeDictEmpTot (emp_shift:list) -> dict:
        """
            Converts a list of employee shifts into a dictionary with total shift hours per employee.

            Args:
                emp_shift (list): A list of tuples, where each tuple contains:
                    - employee (str): The name or identifier of the employee.
                    - shift (int or float): The number of hours worked in a shift.
                    - j_ (any): An additional parameter (unused in this function).
                    - i_ (any): An additional parameter (unused in this function).
                    - o_ (any): An additional parameter (unused in this function).

            Returns:
                dict: A dictionary where the keys are employee names/identifiers and the values are the total shift hours for each employee.
        """
        employee_totals = {}

        for employee, shift, j_ , i_, o_ in emp_shift:
            if employee in employee_totals:
                employee_totals[employee] += shift  
            else:
                employee_totals[employee] = shift  
        return employee_totals

    @staticmethod
    def process_employees(worksheet:object) -> dict:
        """     
            Processes the employees listed in row 20 of the given worksheet.

            Args:
                worksheet (object): The worksheet object from which to extract employee data.
            Returns:
                dict: A dictionary where the keys are employee names (or placeholders) and the values are their respective order numbers.
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

    @staticmethod
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
            "WGSlist!AA21:AD51",
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
            sheet(object): Объект листа (например, object), содержащий лист WGSlist.
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

    def toggle_incKEY(sheet: object) -> None:
        """
        Функция принимает объект листа и меняет значение ячейки E93 на листе WGSlist:
        если текущее значение равно "31", меняет на "15", иначе – на "31".

        Args:
            sheet(object): Объект листа (например, object), содержащий лист WGSlist.
            days_in_month(int): ключ внутри ячейки
        """
        try:
            cell = sheet.acell('AE53')
            current_value = cell.value.strip() if cell.value else ""

            newValue = "15" if current_value == "31" else "31"
            # Обновляем значение ячейки E93
            sheet.update_acell('AE53', newValue)
            print(f"Значение ячейки AE53 изменено с {current_value} на {newValue}")
        except Exception as e:
            print(f"Ошибка при обновлении ячейки: {e}")

    @staticmethod
    def ensure_cell_value(sheet: object, days_in_month: int) -> None:
        """
        Функция призвана убедиться, что у нас в ключе РП в таблице стоит верное значение.
        Если текущее значение ячейки при инициализации приложения не равно days_in_month, то поменять ее на days_in_month.

        Args:
            sheet(object): Объект листа (например, object), содержащий лист WGSlist.
            days_in_month(int): ключ внутри ячейки
        """
        try:
            cell = sheet.acell('E93')
            current_value = cell.value.strip() if cell.value else ""

            if str(days_in_month) != current_value:
                sheet.update_acell('E93', days_in_month)
                print(f"Made sure that cell E93 is {days_in_month}")
        except Exception as e:
            print(f"smth unexpected happened: {e}")

