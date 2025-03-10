import gspread
from Model.FFCWP import ffcwp
from Addons.QOL import QOL


class Parser:
    """
    Parser class for transferring information from one place to another.
    It includes several methods for working with various data sources.

    Methods:
        parseDataAboutShifts(pattern: int, *sheets) -> tuple | None:
            Extracts data from report tables on the total number of employee shifts.
            Supported sheets: KOM, PIK, JUNE, LONDONMALL.

        parseInfoAboutIncome(client, spreadsheet_id: str, sheet_name: str) -> list:
            Finds cells containing numerical (financial) values in Google Sheets and returns a list of tuples (row_index, cell_value).

        parseINCOMEfromSHEETS(client: object, month: str, *sheet_ids: tuple) -> tuple[list, list, list, list]:
            Extracts income data from the provided sheets.

        parseDataNamesShift(*datasets: tuple) -> list:
            Parses employee shifts from multiple datasets.
    """
    def parseDataAboutShifts(pattern: int, *sheets) -> tuple | None:
        """data for different time\nsheets: KOM | PIK | JUNE | LONDONMALL"""
        sheetKOM, sheetPIK, sheetJUNE, sheetLM = sheets
        if pattern == 15:
            # 1-15 числа
            data15KOMENDA = sheetKOM.get(f'A1:M{ffcwp.ffcwp15(sheetKOM)}')
            data15PIK = sheetPIK.get(f'A1:M{ffcwp.ffcwp15(sheetPIK)}')
            data15JUNE = sheetJUNE.get(f'A1:M{ffcwp.ffcwp15(sheetJUNE)}')
            data15LM = sheetLM.get(f'A1:M{ffcwp.ffcwp15(sheetLM)}')
            return data15KOMENDA, data15PIK, data15LM, data15JUNE

        if pattern == 31:
            # 15-31 числа
            data31KOMENDA = sheetKOM.get(
                f'A{ffcwp.ffcwp15(sheetKOM)}:M{ffcwp.ffcwpend(sheetKOM)+20}')
            data31PIK = sheetPIK.get(
                f'A{ffcwp.ffcwp15(sheetPIK)}:M{ffcwp.ffcwpend(sheetPIK)+20}')
            data31JUNE = sheetJUNE.get(
                f'A{ffcwp.ffcwp15(sheetJUNE)}:M{ffcwp.ffcwpend(sheetJUNE)+20}')
            data31LM = sheetLM.get(
                f'A{ffcwp.ffcwp15(sheetLM)}:M{ffcwp.ffcwpend(sheetLM)+20}')
            return data31KOMENDA, data31PIK, data31LM, data31JUNE

        return None

    def parseInfoAboutIncome(client, spreadsheet_id: str, sheet_name: str) -> list:
        """
        Находит ячейки, содержащие числовые (финансовые) значения в Google Sheets, и возвращает список кортежей (row_index, cell_value).

        Args:
            spreadsheet_id: ID таблицы Google Sheets.
            sheet_name: Название листа.

        Returns:
            Список кортежей (row_index, cell_value) или пустой список, если ячейки не найдены.
            Возвращает None в случае ошибки подключения или доступа.

        Raises:
            ValueError: Если spreadsheet_id или sheet_name не являются строками.
        """
        if not isinstance(spreadsheet_id, str):
            raise ValueError("spreadsheet_id должен быть строкой.")
        if not isinstance(sheet_name, str):
            raise ValueError("sheet_name должен быть строкой.")

        try:
            spreadsheet = client.open_by_key(spreadsheet_id)
            sheet = spreadsheet.worksheet(sheet_name)
        except gspread.exceptions.SpreadsheetNotFound:
            print(f"Ошибка: Таблица с ID '{spreadsheet_id}' не найдена.")
            return None
        except gspread.exceptions.WorksheetNotFound:
            print(f"Ошибка: Лист с именем '{sheet_name}' не найден в таблице.")
            return None
        except Exception as e:
            print(f"Произошла ошибка при доступе к Google Sheets: {e}")
            return None

        print("Успешно подключился к таблице")
        cells_with_money_type = []

        try:
            # Получаем значения 10-го столбца (столбец J)
            all_values = sheet.col_values(10)
        except Exception as e:
            print(f"Произошла ошибка при получении данных с листа: {e}")
            return None

        print(all_values)
        day_idx = 0
        # Перебираем каждое значение ячейки (номер строки начинается с 1)
        for row_index, cell_value in enumerate(all_values, start=1):

            if QOL.is_valid_price(cell_value):
                # Заменяем запятую на точку и удаляем неразрывный пробел
                cleaned_value = cell_value.replace(
                    ",", ".").replace("\xa0", "")
                day_idx += 1
                try:
                    numeric_value = float(cleaned_value)
                except ValueError:
                    # Если преобразование не удалось, пропускаем значение
                    continue
                cells_with_money_type.append((day_idx, numeric_value))
                print(f"adding this thing to income table - {cleaned_value}")
        print("вот список из f_c_b_t_c", cells_with_money_type)
        return cells_with_money_type

    def parseINCOMEfromSHEETS(client: object, month: str, *sheet_ids: tuple) -> tuple[list, list, list, list]:
        """
        Извлекает данные о доходах из переданных листов.

        Args:
            client (object): Клиент для работы с таблицами.
            month (str): Название месяца, за который нужно получить данные.
            *sheet_ids (tuple): Идентификаторы листов, откуда извлекаются данные.

        Returns:
            tuple: Четыре значения доходов - KOM, PIK, JUNE, LM.
        """
        sheetKOM, sheetPIK, sheetJUNE, sheetLM = sheet_ids

        print("INFORMATION ABOUT income IN KOMENDA")
        list_with_income_KOM = Parser.parseInfoAboutIncome(
            client, sheetKOM, month)
        print("INFORMATION ABOUT income IN PIK")
        list_with_income_PIK = Parser.parseInfoAboutIncome(
            client, sheetPIK, month)
        print("INFORMATION ABOUT income IN JUNE")
        list_with_income_JUNE = Parser.parseInfoAboutIncome(
            client, sheetJUNE, month)
        print("INFORMATION ABOUT income IN LM")
        list_with_income_LM = Parser.parseInfoAboutIncome(
            client, sheetLM, month)
        return list_with_income_KOM, list_with_income_PIK, list_with_income_JUNE, list_with_income_LM

    def parseDataNamesShift(*datasets: tuple) -> list:
        """
        Parses employee shifts from multiple datasets.

        Params:
            datasets: Variable number of datasets (e.g., dataKOM, data15PIK, etc.).
                    Each dataset is a list of rows, where each row is a list of cell strings.

        Returns:
            list: A list of tuples (name, shift, day_index, dataset_name), where:
                - name (str): Employee name.
                - shift (float): Employee shift.
                - day_index (int): The sequential day index within the dataset.
                - dataset_name (str): Name associated with the dataset.
        """
        employee_shifts = []
        dataset_names = {1: "KOMENDA", 2: "PIK", 3: "LM", 4: "JUNE"}

        for sheet_number, dataset in enumerate(datasets, start=1):
            dataset_name = dataset_names.get(sheet_number, "UNKNOWN")
            print(f"INFORMATION ABOUT SHIFTS IN {dataset_name}")
            day_index = 0  # reset day index for each dataset

            for row in dataset:
                for cell in row:
                    if "На смене:" in cell:
                        day_index += 1  # increment day index for every cell indicating a day
                        if "(" in cell and ")" in cell:
                            # Split the cell by whitespace and process each entry
                            entries = cell.split()
                            for entry in entries:
                                if "(" in entry and ")" in entry:
                                    try:
                                        name, shift_str = entry.split("(", 1)
                                    except ValueError:
                                        continue  # Skip if splitting fails
                                    name = name.strip()
                                    try:
                                        shift_stru, type_of_shift = shift_str.split(
                                            ";", 1)
                                    except ValueError:
                                        continue
                                    type_of_shift = type_of_shift.strip(")")
                                    shift_num = shift_stru.replace(",", ".")
                                    try:
                                        shift = float(shift_num)
                                    except ValueError:
                                        continue  # Skip invalid shift values
                                    print(
                                        f"name: {name} | shift: {shift} | on day {day_index}")
                                    employee_shifts.append(
                                        (name, shift, day_index, dataset_name, type_of_shift))
                                    print("вот тебе один вывод", (name, shift,
                                          day_index, dataset_name, type_of_shift))

        return employee_shifts
