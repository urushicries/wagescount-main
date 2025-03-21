from Addons.QOL import QOL


class Updater:
    """    
    Updater class provides methods to update employee shift information and income data in a Google Sheets document.
       **Methods**:

            update_info_WAGES(employee_shift_dict: dict, sheetLink) -> None:
                    Updates employee shift information in the wages table.

                    employee_shift_dict (dict): Dictionary containing employee shift information.
                    sheetLink (object): Google Sheets link object to interact with.

            update_info_everyday(days_in_month: int, employee_shiftsList: list, sheetLink) -> None:
                Updates employee shift information in the wages table for each day of the month.

                    days_in_month (int): Number of days in the month.
                    employee_shiftsList (list): List of employee shifts by day.
                    sheetLink (object): Google Sheets link object to interact with.


            update_info_everyday_TRADEPLACES(days_in_month: int, employee_shiftsList: list, sheetLink) -> None:
                Updates employee shift information by trade places (arenas) for each day of the selected month.

                    days_in_month (int): Number of days in the month.
                    employee_shiftsList (list): List of employee shifts with trade places.
                    sheetLink (object): Google Sheets link object to interact with.


            update_table_from_lists(sheetLink, *lists) -> None:

                    sheetLink (object): Google Sheets link object to interact with.


            send_emp_list(emp_list: list, sheetlink) -> None:
                Replaces the employee list in the Google Sheets document.

                    emp_list (list): List of employees from EMP_creator.
                    sheetlink (object): Google Sheets link object to interact with.

    """
    @staticmethod
    def update_info_WAGES(employee_shift_dict: dict, sheetLink) -> None:
        """
        Обновляет информацию о сменах сотрудников в таблице заработной платы.

        Args:
            employee_shift_dict (dict): Словарь, содержащий информацию о сменах сотрудников.
            employee_shifts_list (list): Список смен сотрудников за месяц.
            sheet_link (str или объект): Ссылка или идентификатор таблицы для обновления.

        Returns:
            None: lol
        """
        print("starting update_info_WAGES")
        _cntr = 97 + len(QOL.process_employees(sheetLink))
        print("вот такой _cntr", _cntr)
        rangeEMPNAMES = f'C97:D{_cntr}'  # Assuming these are employee names

        # Get current data from the sheet
        cell_values = sheetLink.get(rangeEMPNAMES)

        # Prepare batch updates for the employee shifts
        updates = []

        # Iterate through employee shifts for the whole month
        for i_, row in enumerate(cell_values, start=97):
            if row:
                name = row[0]
            else:
                print("Empty row encountered")
                continue

            # Update employee's shift for the entire month (using employee_shift_dict)
            if name in employee_shift_dict:
                updates.append({
                    'range': f'D{i_}',
                    'values': [[employee_shift_dict[name]]]
                })
                print(f"adding shifts {employee_shift_dict[name]} for {name}")
            # Batch update the sheet with the new values
        if updates:
            sheetLink.batch_update(updates)
    @staticmethod
    def update_info_everyday(days_in_month: int, employee_shiftsList: list, sheetLink) -> None:
        """
        Обновляет информацию о сменах сотрудников в таблице заработной платы за каждый день месяца.

        Args:
            days_in_month (int): Количество дней в месяце.
            employee_shifts_list (list): Список смен сотрудников по дням.
            sheet_link (str или объект): Ссылка или идентификатор таблицы для обновления.

        Returns:
            None: ur mom gay
        """
        print("starting update_info_everyday")

        # Map employee names to column indices in the range
        employee_to_column = QOL.process_employees(sheetLink)

        # Extract the starting cell's coordinates
        start_row15, start_col15 = 21, ord('D')  # Row 21 and column 'D'
        # Extract the starting cell's coordinates
        start_rowend, start_colend = 36, ord('D')  # Row 35 and column 'D'
        # Prepare updates based on employee_shiftsList
        updates = []
        if days_in_month == 15:
            for employee, value, day, dataset, tp_shft in employee_shiftsList:
                if employee in employee_to_column:
                    column_offset = employee_to_column[employee]
                    # Convert column index to letter
                    col_letter = chr(start_col15 + column_offset - 1)
                    row = start_row15 + day - 1  # Map the day to the corresponding row
                    cell_address = f"{col_letter}{row}"
                    updates.append(
                        {"range": cell_address, "values": [[value]]})
                    print(
                        f" {employee} |  смена типа {value} | числа: {day} | на арене {dataset} | {cell_address}")
        elif days_in_month == 31:
            for employee, value, day, dataset, tp_shft in employee_shiftsList:
                if employee in employee_to_column:
                    column_offset = employee_to_column[employee]
                    # Convert column index to letter
                    col_letter = chr(start_colend + column_offset - 1)
                    row = start_rowend + day - 1  # Map the day to the corresponding row
                    cell_address = f"{col_letter}{row}"
                    updates.append(
                        {"range": cell_address, "values": [[value]]})
                    print(
                        f" {employee} |  смена типа {value} | числа: {day} | на арене {dataset}")
        # Batch update the sheet with the new values
        if updates:
            sheetLink.batch_update(updates)
    @staticmethod
    def update_info_everyday_TRADEPLACES(days_in_month: int, employee_shiftsList: list, sheetLink) -> None:
        """
        Обновляет информацию о сменах сотрудников по торговым точкам (аренам) 
        за каждый день в выбранном месяце.

        Args:
            days_in_month (int): Количество дней в месяце.
            employee_shifts_list (list): Список смен сотрудников с указанием торговых точек.
            sheet_link (str или объект): Ссылка или идентификатор таблицы для обновления.

        Returns:
            None: i am hunted by fbi
        """
        print("Starting to do update_info_everyday_TRADEPLACES")

        employee_to_column = QOL.process_employees(sheetLink)

        # Extract the starting cell's coordinates
        start_row15, start_col15 = 59, ord('D')  # Row 59 and column 'D'
        # Extract the starting cell's coordinates
        start_rowend, start_colend = 74, ord('D')  # Row 74 and column 'D'
        # Prepare updates based on employee_shiftsList
        updates = []
        if days_in_month == 15:
            for employee, value, day, dataset, tp_shft in employee_shiftsList:
                if employee in employee_to_column:
                    column_offset = employee_to_column[employee]
                    # Convert column index to letter
                    col_letter = chr(start_col15 + column_offset - 1)
                    row = start_row15 + day - 1  # Map the day to the corresponding row
                    cell_address = f"{col_letter}{row}"
                    tpSHIFTFIN = QOL.replace_letter(tp_shft)
                    value_fin = dataset + f"_{tpSHIFTFIN}"
                    updates.append(
                        {"range": cell_address, "values": [[value_fin]]})
                    print(f"{employee} смена в арене {dataset} числа: {day}")
        elif days_in_month == 31:
            for employee, value, day, dataset, tp_shft in employee_shiftsList:
                if employee in employee_to_column:
                    column_offset = employee_to_column[employee]
                    # Convert column index to letter
                    col_letter = chr(start_colend + column_offset - 1)
                    row = start_rowend + day - 1  # Map the day to the corresponding row
                    tpSHIFTFIN = QOL.replace_letter(tp_shft)
                    value_fin = dataset + f"_{tpSHIFTFIN}"
                    cell_address = f"{col_letter}{row}"
                    updates.append(
                        {"range": cell_address, "values": [[value_fin]]})
                    print(f"{employee} смена в арене {dataset} числа: {day + 15}")
        # Batch update the sheet with the new values
        if updates:
            sheetLink.batch_update(updates)
    @staticmethod
    def update_table_from_lists(sheetLink, *lists) -> None:
        """
        Updates table data for columns with INCOME from TRADEPLACES based on provided lists.

        Args:
            lists (list): A list of four lists, each containing tuples with (day_index, value).
            sheetLink: Google Sheets link object to interact with.
        """
        incomeLSTKOM,NPKOM, incomeLSTPIK,NPPIK, incomeLSTJUNE,JUNENP, incomeLSTLM,LMNP = lists
        fullincomeList = [incomeLSTKOM,
                          incomeLSTPIK, incomeLSTJUNE, incomeLSTLM]
        # Define the starting row and columns for the range
        start_row = 21
        columns = ['AA', 'AB', 'AC', 'AD']  # Corresponding columns for each list

        # Prepare batch updates
        updates = []
        print("starting update_income")
        for i, data_list in enumerate(fullincomeList):
            # Determine the column based on the list index
            column_letter = columns[i]
            for day_index, value in data_list:
                # Calculate the row number based on the day index
                row = start_row + day_index - 1
                # Prepare the cell address
                cell_address = f"{column_letter}{row}"
                # Append the update to the batch
                updates.append({"range": cell_address, "values": [[value]]})
                print(f"В список обновлений добавлено {value} из списка {i}")
        # Perform batch update on the sheet
        updates.append({'range': 'AA58', 'values': [[NPKOM]]})
        updates.append({'range': 'AB58', 'values': [[NPPIK]]})
        updates.append({'range': 'AC58', 'values': [[JUNENP]]})
        updates.append({'range': 'AD58', 'values': [[LMNP]]})
        if updates:
            print("Updates to be sent:",updates)
            sheetLink.batch_update(updates)

    @staticmethod
    def send_emp_list(emp_list: list, sheetlink) -> None:
        """
        Функция предназначена для замены списка работников.

        :param sheetlink:
            Объект Google Sheet.
        :param emp_list:
            Список работников из EMP_creator.
        :return:
            None
        """
        length_emp = len(emp_list)
        if length_emp == 0:
            return

        updates = []
        try:
            for i_, emp in enumerate(emp_list):
                cell_address = f"C{97 + i_}"  # Исправил ошибку с индексами
                updates.append({"range": cell_address, "values": [[emp]]})  # `values` должен быть списком списков

        except Exception as e:
            print(f"Что-то пошло не так: {e}")

        if updates:
            try:
                sheetlink.batch_update(updates)
                print("Список сотрудников успешно обновлён!")
            except Exception as e:
                print(f"Ошибка при обновлении таблицы: {e}")