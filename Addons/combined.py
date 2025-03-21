import ctypes
import sys
import os
import tkinter as tk

import re

import gspread

from tkinter import BooleanVar

#view
class UiManager:
    def __init__(self, config, scale_factor=0.8):
        self.label_success_info = None
        self.label_error_info = None
        self.label_footer_info = None
        self.label_daily_info = None
        self.t_set_up_shifts_for_all_days_check = None
        self.t_income_from_shops_check = None
        self.label_income_info = None
        self.delete_button = None
        self.label_wages_info = None
        self.t_wages_whole_month_check = None
        self.labelDeleteInfo = None
        self.toggle_button = None
        self.label_instructions = None
        self.label_period_info = None
        self.light_theme = {
            'bg': 'white',
            'fg': 'black',
            'button_bg': 'lightgrey',
            'button_fg': 'black',
            'checkbox_bg': 'lightgrey',
            'checkbox_fg': 'black'
        }
        self.dark_theme = {
            'bg': 'black',
            'fg': 'white',
            'button_bg': 'white',
            'button_fg': 'black',
            'checkbox_bg':'white',
            'checkbox_fg':'orange'
        }
        self.current_theme = 'dark'
        self.root = config['root']
        self.QOL = config['QOL']
        self.infoVariables = config['infoVariables']
        self.scale_factor = scale_factor
        self.days_in_month = 31

        self.t_wages_whole_month_var1 = BooleanVar()
        self.t_income_from_shops_var2 = BooleanVar()
        self.t_set_up_shifts_for_all_days_var3 = BooleanVar()

        self.conrtoller = None

        self.setup_ui()

    def toggle_theme(self):
        if self.current_theme == 'dark':
            self.apply_theme(self.light_theme)
            self.current_theme = 'light'
        else:
            self.apply_theme(self.dark_theme)
            self.current_theme = 'dark'

    def apply_theme(self, theme):
        self.root.configure(bg=theme['bg'])
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Button):
                widget.configure(bg=theme['button_bg'], fg=theme['button_fg'])
            elif isinstance(widget, tk.Checkbutton):
                widget.configure(bg=theme['checkbox_bg'], fg=theme['checkbox_fg'])
            else:
                widget.configure(bg=theme['bg'], fg=theme['fg'])

    def nothing_picked(self):
        self.label_error_info.config(
            text="Выберите хотя бы \nодну функцию❎", font=("Arial", 16, "bold"))
        self.root.after(3000, lambda: self.label_error_info.config(text=""))

    def success(self):
        self.label_success_info.config(
            text="Успех!☑", font=("Arial", 24, "bold"))
        self.root.after(3000, lambda: self.label_success_info.config(text=""))

    def show_error(self, message):
        print(f"Error: {message}")

    def on_button_click(self, month):
        checkboxes = {
            'wages': self.t_wages_whole_month_var1.get(),
            'income': self.t_income_from_shops_var2.get(),
            'shifts': self.t_set_up_shifts_for_all_days_var3.get()
        }
        if self.controller:
            self.controller.send_request(month, checkboxes, self.days_in_month)
        else:
            print("controller is not set!")
            print(self.controller)

    def toggle_days(self):
        if self.t_wages_whole_month_var1.get() or self.t_set_up_shifts_for_all_days_var3.get():
            self.label_error_info.config(text=" ")
        if self.days_in_month == 15:
            self.days_in_month = 31
            self.controller.toggle_RP_button(self.days_in_month)
            self.label_period_info.config(
                text=f"{self.days_in_month - 15}    -    {self.days_in_month}")
            print("Поменял РП с \"1 до 15\" на \"16 до 31\"")
        else:
            self.days_in_month = 15
            self.controller.toggle_RP_button(self.days_in_month)
            self.label_period_info.config(
                text=f" {self.days_in_month - 14}    -    {self.days_in_month}")
            print("Поменял РП с \"16 до 31\" на \"1 до 15\" ")

    def toggle_Inc_key(self):
        self.controller.toggleINCKey()
    def delete_ranges(self):
        if self.controller:
            self.controller.sentRdelete()
            self.success()

    def setup_ui(self):
        self.root.configure(bg="black")
        btn_width = int(18 * self.scale_factor)
        font_size = int(20 * self.scale_factor)
        padx = int(8 * self.scale_factor)
        pady = int(8 * self.scale_factor)

        num_columns = 4

        for i, month in enumerate(self.infoVariables.months):
            button = tk.Button(self.root, text=month, height=2, width=btn_width,
                               command=lambda m=month: self.on_button_click(m),
                               bg="white", fg="black",
                               font=("Arial", font_size, "bold"), relief="sunken")
            row = i // num_columns
            column = i % num_columns
            button.grid(row=row, column=column, padx=padx,
                        pady=pady, sticky="nsew")

        for i in range(num_columns):
            self.root.grid_columnconfigure(i, weight=1, uniform="equal")
        for i in range((len(self.infoVariables.months) + num_columns - 1) // num_columns):
            self.root.grid_rowconfigure(i, weight=1, uniform="equal")

        self.toggle_button = tk.Button(
            self.root,
            text=self.infoVariables.change,
            font=("Roboto", int(24 * self.scale_factor)),
            bg="white", fg="black", padx=btn_width//2,
            command=self.toggle_days
        )
        
        self.toggle_button.grid(row=6, column=1, pady=int(
            24 * self.scale_factor), columnspan=3)
        
        self.toggle_INCbutton = tk.Button(
            self.root,
            text="Сменить ключ\nРасчета прихода",
            font=("Roboto", int(20 * self.scale_factor)),
            bg="white", fg="black", padx=btn_width//2,
            command=self.toggle_Inc_key
        )
        self.toggle_INCbutton.grid(row=9, column=2, pady=int(
            24 * self.scale_factor))

        self.delete_button = tk.Button(
            self.root,
            text=" 🗑️ ? ",
            font=("Roboto", int(16 * self.scale_factor)),
            bg="white", fg="black",
            command=self.delete_ranges
        )
        self.delete_button.grid(
            row=7, column=3, pady=int(24 * self.scale_factor))

        self.language_button = tk.Button(
            self.root,
            text="LANG 🌐 / ЯЗЫК 🌐",
            font=("Roboto", int(16 * self.scale_factor)),
            bg="white", fg="black",
            command=self.toggle_language
        )
        self.language_button.grid(row=9, column=3, pady=int(24 * self.scale_factor))

        self.theme_button = tk.Button(
            self.root,
            text="Theme color\nЦвет темы",
            font=("Roboto", int(16 * self.scale_factor)),
            bg="white", fg="black",
            command=self.toggle_theme
        )
        self.theme_button.grid(row=10, column=3, pady=int(24 * self.scale_factor))

        self.t_wages_whole_month_check = tk.Checkbutton(
            self.root,
            text=self.infoVariables.allshifts,
            variable=self.t_wages_whole_month_var1,
            bg="white", fg="black",
            font=("Roboto", int(15 * self.scale_factor), "bold")
        )
        self.t_wages_whole_month_check.grid(
            row=7, column=0, pady=pady, padx=padx)

        self.t_income_from_shops_check = tk.Checkbutton(
            self.root,
            text=self.infoVariables.income_from_shopsINFO,
            variable=self.t_income_from_shops_var2,
            bg="white", fg="black",
            font=("Roboto", int(15 * self.scale_factor), "bold")
        )
        self.t_income_from_shops_check.grid(
            row=7, column=2, pady=pady, padx=padx)

        self.t_set_up_shifts_for_all_days_check = tk.Checkbutton(
            self.root,
            text=self.infoVariables.infoAboutShiftEveryday,
            variable=self.t_set_up_shifts_for_all_days_var3,
            bg="white", fg="black",
            font=("Roboto", int(15 * self.scale_factor), "bold")
        )
        self.t_set_up_shifts_for_all_days_check.grid(
            row=7, column=1, pady=pady, padx=padx)

        self.label_period_info = tk.Label(
            self.root,
            text=f"{self.days_in_month - 15}    -    {self.days_in_month}",
            font=("Roboto", int(20 * self.scale_factor), "bold"),
            bg="black", fg="white"
        )
        self.label_period_info.grid(
            row=6, column=0, pady=pady, padx=padx, columnspan=3)

        self.label_instructions = tk.Label(
            self.root,
            text=self.infoVariables.infoAboutPeriodsAndbuttons,
            font=("Roboto", int(12 * self.scale_factor), "bold"),
            bg="black", fg="white"
        )
        self.label_instructions.grid(row=3, column=1, pady=pady, columnspan=2)

        self.labelDeleteInfo = tk.Label(
            self.root,
            text=self.infoVariables.infoAboutDeleteButton,
            font=("Roboto", int(15 * self.scale_factor), "bold"),
            bg="black", fg="white"
        )
        self.labelDeleteInfo.grid(row=8, column=3)

        self.label_wages_info = tk.Label(
            self.root,
            text=self.infoVariables.infoaboutWagesFunc,
            font=("Roboto", int(12 * self.scale_factor), "bold"),
            bg="black", fg="white"
        )
        self.label_wages_info.grid(
            row=8, column=0, pady=int(16 * self.scale_factor))

        self.label_income_info = tk.Label(
            self.root,
            text=self.infoVariables.infoaboutIncomeFunc,
            font=("Roboto", int(12 * self.scale_factor), "bold"),
            bg="black", fg="white"
        )
        self.label_income_info.grid(
            row=8, column=2, pady=int(16 * self.scale_factor))

        self.label_footer_info = tk.Label(
            self.root,
            text="и мне не надо слов\nя все поняла\nver 0.2.5",
            bg="black", fg="white",
            font=("Arial", int(12 * self.scale_factor), "bold")
        )
        self.label_footer_info.grid(row=10, column=0, columnspan=4)

        self.label_daily_info = tk.Label(
            self.root,
            text=self.infoVariables.infoAboutShiftEverydayFunc,
            font=("Roboto", int(12 * self.scale_factor), "bold"),
            bg="black", fg="white"
        )
        self.label_daily_info.grid(
            row=8, column=1, pady=int(16 * self.scale_factor))

        self.label_error_info = tk.Label(
            self.root,
            text="",
            bg="black", fg="red",
            font=("Arial", int(12 * self.scale_factor))
        )
        self.label_error_info.grid(row=6, column=0)

        self.label_success_info = tk.Label(
            self.root,
            text="",
            bg="black", fg="lightgreen",
            font=("Arial", int(12 * self.scale_factor))
        )
        self.label_success_info.grid(row=6, column=3)

        self.apply_theme(self.dark_theme)

    def toggle_language(self):
        self.infoVariables.switch_language()
        self.update_ui_texts()

    def update_ui_texts(self):
        self.label_instructions.config(text=self.infoVariables.infoAboutPeriodsAndbuttons)
        self.labelDeleteInfo.config(text=self.infoVariables.infoAboutDeleteButton)
        self.label_wages_info.config(text=self.infoVariables.infoaboutWagesFunc)
        self.label_income_info.config(text=self.infoVariables.infoaboutIncomeFunc)
        self.label_daily_info.config(text=self.infoVariables.infoAboutShiftEverydayFunc)
        self.t_set_up_shifts_for_all_days_check.config(text=self.infoVariables.infoAboutShiftEveryday)
        self.t_income_from_shops_check.config(text=self.infoVariables.income_from_shopsINFO)
        self.t_wages_whole_month_check.config(text=self.infoVariables.allshifts)
        self.toggle_button.config(text=self.infoVariables.change)
        for i, month in enumerate(self.infoVariables.months):
            self.root.grid_slaves(row=i // 4, column=i % 4)[0].config(text=month)

    def run(self):
        self.root.mainloop()
#model
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
    
    @staticmethod
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
    
    @staticmethod
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
        cells_with_money_type_NP = []

        try:
            # Получаем значения 10-го столбца (столбец J)
            all_values_inc = sheet.col_values(10)
            all_values_NP = sheet.col_values(8)
        except Exception as e:
            print(f"Произошла ошибка при получении данных с листа: {e}")
            return None

        print(all_values_inc)
        print(all_values_NP)
        day_idx = 0
        # Перебираем каждое значение ячейки (номер строки начинается с 1)
        for row_index, cell_value in enumerate(all_values_inc, start=1):

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

        for row_index, cell_value in enumerate(all_values_NP, start=1):

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
                cells_with_money_type_NP.append((day_idx, numeric_value))

        total_income_NP = sum(value for _, value in cells_with_money_type_NP)

        print(f"Total income NP: {total_income_NP}")

        return cells_with_money_type, total_income_NP  
    
    @staticmethod
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
        list_with_income_KOM, KOM_NP = Parser.parseInfoAboutIncome(
            client, sheetKOM, month)
        print("INFORMATION ABOUT income IN PIK")
        list_with_income_PIK, PIK_NP = Parser.parseInfoAboutIncome(
            client, sheetPIK, month)
        print("INFORMATION ABOUT income IN JUNE")
        list_with_income_JUNE, JUNE_NP = Parser.parseInfoAboutIncome(
            client, sheetJUNE, month)
        print("INFORMATION ABOUT income IN LM")
        list_with_income_LM, LM_NP = Parser.parseInfoAboutIncome(
            client, sheetLM, month)
        return list_with_income_KOM, KOM_NP, list_with_income_PIK, PIK_NP, list_with_income_JUNE, JUNE_NP, list_with_income_LM, LM_NP  
     
    @staticmethod
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

class ffcwp:
    """ 
    The `ffcwp` class provides static methods to find specific patterns in the first column of a sheet and process data from multiple sheets based on a given pattern.

        Methods:
            find_first_matching_cell(sheet, patterns):

            ffcwp15(sheet):

            ffcwpend(sheet):

            makeDataFromSheets(pattern: int, *sheets) -> tuple | None:
                Processes data from sheets by some pattern.
                    pattern (int): Key for calculation either until the end of the month or until the middle.
                    sheets (tuple): Report tables.
                    tuple | None: A tuple containing data from the sheets based on the pattern, or None if the pattern is not recognized.
        """
    @staticmethod
    def find_first_matching_cell(sheet, patterns):
        """
        Finds the first cell in the first column that matches any of the given patterns.
        Args:
            sheet (object): The sheet object to search.
            patterns (list): List of compiled regex patterns to match.
        Returns:
            int | None: The row number of the first matching cell, or None if no match is found.
        """
        column_data = sheet.col_values(1)  # Get all values in the first column

        for row_num, value in enumerate(column_data, start=1):
            for pattern in patterns:
                if pattern.match(value):
                    return row_num
        return None
    
    @staticmethod
    def ffcwp15(sheet):
        """
        Finds the first cell in the first column with the format '15.xx.xxxx'.
        Args:
            sheet (object): The sheet object to search.
        Returns:
            int | None: The row number of the first matching cell, or None if no match is found.
        """
        pattern = re.compile(r"^15\.\d{2}\.\d{4}$")
        return ffcwp.find_first_matching_cell(sheet, [pattern])

    @staticmethod
    def ffcwpend(sheet):
        """
        Finds the first cell in the first column with one of the following formats:
        '31.xx.xxxx', '30.xx.xxxx', '29.xx.xxxx', or '28.xx.xxxx'.
        Priority: '31.xx.xxxx' first, then the others in order.
        Args:
            sheet (object): The sheet object to search.
        Returns:
            int | None: The row number of the first matching cell, or None if no match is found.
        """
        patterns = [
            re.compile(r"^31\.\d{2}\.\d{4}$"),
            re.compile(r"^30\.\d{2}\.\d{4}$"),
            re.compile(r"^29\.\d{2}\.\d{4}$"),
            re.compile(r"^28\.\d{2}\.\d{4}$")
        ]
        return ffcwp.find_first_matching_cell(sheet, patterns)

    @staticmethod
    def makeDataFromSheets(pattern: int, *sheets) -> tuple | None:
        """
        Procesess data from  sheets by some pattern.
        Args:
            sheets(tuple): таблицы отчетов
            pattern(int):ключ для расчет либо до  конца месяца либо до середины
        Returns:
            nothing
        """
        sheetKOM, sheetPIK, sheetJUNE, sheetLM = sheets
        if pattern == 15:
            # 1-15 числа
            data15KOMENDA = sheetKOM.get(
                f'A1:M{ffcwp.ffcwp.ffcwp15(sheetKOM)}')
            data15PIK = sheetPIK.get(f'A1:M{ffcwp.ffcwp.ffcwp15(sheetPIK)}')
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
#controller
class WebController:
    """A class used to represent a Web Controller that handles data processing and updates for various sheets.

    Attributes:
        view: The view component to interact with the user interface.
        client: The client used to interact with the sheets.
        QOL: Quality of Life utilities for various operations.
        Parser: The parser used to parse data from sheets.
        Updater: The updater used to update data in sheets.
        infoVariables: Additional information variables.
        service: The service used for sheet operations.
        sheetWAGES: The sheet where wages data is stored.
        shtKOM_id: The ID of the KOM sheet.
        shtPIK_id: The ID of the PIK sheet.
        shtJUN_id: The ID of the JUN sheet.
        shtLM_id: The ID of the LM sheet.
        days_in_month: The number of days in the current month.

    Methods:
        send_request(month, checkboxes, days_in_month):
            Sends a request to process data for a given month based on selected options.
        
        sentRdelete():
        
        toggle_RP_button(days_in_month):"""
    
    def __init__(self, config):
        self.view = config['view']
        self.client = config['client']
        self.QOL = config['QOL']
        self.Parser = config['Parser']
        self.Updater = config['Updater']
        self.infoVariables = config['infoVariables']
        self.service = config['service']
        self.sheetWAGES = config['sheetWAGES']
        self.shtKOM_id = config['shtKOM_id']
        self.shtPIK_id = config['shtPIK_id']
        self.shtJUN_id = config['shtJUN_id']
        self.shtLM_id = config['shtLM_id']
        self.days_in_month = 31


    def send_request(self, month, checkboxes, days_in_month):
        """Sends a request to process data for a given month based on selected options.

        Args:
            month (str): The month for which data is to be processed.
            checkboxes (dict): A dictionary with boolean values indicating which data to process:
                - 'wages': Process wages data.
                - 'income': Process income data from rents.
                - 'shifts': Process shifts data for each day.
            days_in_month (int): The number of days in the specified month.

        Returns:
            None

        Raises:
            Exception: If an error occurs while processing the sheets.

        The function performs the following steps:
            1. Checks if at least one option is selected in the checkboxes.
            2. Retrieves the data for the specified month.
            3. Opens the relevant sheets for the specified month.
            4. Parses data about shifts if 'wages' or 'shifts' is selected.
            5. Parses income data if 'income' is selected.
            6. Updates wages information if 'wages' is selected.
            7. Updates shifts information if 'shifts' is selected.
            8. Updates income information if 'income' is selected.
            9. Notifies the view of success or failure."""

        # Если ни одна функция не выбрана, сообщаем об ошибке через View
        if not (checkboxes.get('wages') or checkboxes.get('income') or checkboxes.get('shifts')):
            self.view.nothing_picked()
            return
        
        months_data = {
            "January ❄️": {"sheet_suffix": "Январь25", "days": days_in_month},
            "February 🌨️": {"sheet_suffix": "Февраль25", "days": days_in_month},
            "March 🌸": {"sheet_suffix": "Март25", "days": days_in_month},
            "April 🌹": {"sheet_suffix": "Апрель25", "days": days_in_month},
            "May 🌺": {"sheet_suffix": "Май25", "days": days_in_month},
            "June ☀️": {"sheet_suffix": "Июнь25", "days": days_in_month},
            "July 🌞": {"sheet_suffix": "Июль25", "days": days_in_month},
            "August 😢": {"sheet_suffix": "Август25", "days": days_in_month},
            "September 😭": {"sheet_suffix": "Сентябрь25", "days": days_in_month},
            "October 🍁": {"sheet_suffix": "Октябрь25", "days": days_in_month},
            "November 🍂": {"sheet_suffix": "Ноябрь25", "days": days_in_month},
            "December ☃️": {"sheet_suffix": "Декабрь25", "days": days_in_month}
            }
        
        print(month, self.infoVariables.current_language)
        month_data = months_data.get(month)
        print(month_data)
        if not month_data:
            print(f"Unknown month: {month}")
            return

        try:
            # Открываем листы для выбранного месяца
            sheetKOM = self.client.open("Коменда отчет").worksheet(
                month_data["sheet_suffix"])
            sheetPIK = self.client.open("Пик отчет").worksheet(
                month_data["sheet_suffix"])
            sheetJUNE = self.client.open("Июнь отчет").worksheet(
                month_data["sheet_suffix"])
            sheetLM = self.client.open("Лондон отчет").worksheet(
                month_data["sheet_suffix"])
            # Initialize income variables with default values
            incomeKOM = incomePIK = incomeJUNE = incomeLM = None
            NPKOM = NPPIK = NPJUN = NPLM = None

            dictEMPSHIFT = None
            emp_shiftLST = None
            if checkboxes.get('wages') or checkboxes.get('shifts'):
                dataKOM, dataPIK, dataJUNE, dataLM = self.Parser.parseDataAboutShifts(
                    month_data["days"], sheetKOM, sheetPIK, sheetJUNE, sheetLM
                )
                emp_shiftLST = self.Parser.parseDataNamesShift(
                    dataKOM, dataPIK, dataJUNE, dataLM)
                dictEMPSHIFT = self.QOL.makeDictEmpTot(emp_shiftLST)

            if checkboxes.get('income'):
                incomeKOM, NPKOM, incomePIK, NPPIK, incomeJUNE, NPJUN, incomeLM, NPLM = self.Parser.parseINCOMEfromSHEETS(
                    self.client, month_data["sheet_suffix"],
                    self.shtKOM_id, self.shtPIK_id, self.shtJUN_id, self.shtLM_id
                )
            print("Income data:", incomeKOM, NPKOM, incomePIK, NPPIK, incomeJUNE, NPJUN, incomeLM, NPLM)

            if checkboxes.get('wages'):
                if dictEMPSHIFT and emp_shiftLST:
                    self.Updater.update_info_WAGES(
                        dictEMPSHIFT, self.sheetWAGES)

            if checkboxes.get('shifts'):
                if emp_shiftLST and dictEMPSHIFT:
                    self.Updater.update_info_everyday_TRADEPLACES(
                        month_data["days"], emp_shiftLST, self.sheetWAGES)
                    self.Updater.update_info_everyday(
                        month_data["days"], emp_shiftLST, self.sheetWAGES)

            if checkboxes.get('income'):
                if incomeKOM and incomePIK and incomeJUNE and incomeLM:
                    self.Updater.update_table_from_lists(
                        self.sheetWAGES, incomeKOM, NPKOM, incomePIK, NPPIK, incomeJUNE, NPJUN, incomeLM, NPLM)

            # Если всё прошло успешно – уведомляем View
            self.view.success()
        except Exception as e:
            print(f"Error occurred while processing sheets for {month}: {e}")
            self.view.show_error(str(e))

    def sentRdelete(self):
        """
        Deletes the specified ranges from the wages list.

        This method clears the ranges in the wages list identified by the given
        service and spreadsheet ID.

        Args:
            None

        Returns:
            None
        """
        self.QOL.clear_wgslist_ranges(
            self.service, "14FtsvGplg1jKXJvLJCueI8iEEnjJUtjk17NuPqeCnqo")

    def toggle_RP_button(self, days_in_month):
        """
        Toggles the RP button for the given number of days in a month.

        Args:
            days_in_month (int): The number of days in the current month.
        """
        self.QOL.toggle_cell_value(self.sheetWAGES, days_in_month)
        
    def toggleINCKey(self):
        self.QOL.toggle_incKEY(self.sheetWAGES)
#addons
class Variables_WC:
    """Класс, содержащий текстовые инструкции и описания функций расчета.

    Атрибуты:
        infoAboutPeriodsAndbuttons (str): Инструкция по выбору периода и кнопок.
        infoaboutWagesFunc (str): Описание функции расчета заработной платы.
        infoaboutIncomeFunc (str): Описание функции расчета доходов торговых точек (арен).
        infoAboutShiftEverydayFunc (str): Описание функции расчета ежедневной зарплаты.
        infoAboutDeleteButton (str): Описание функции кнопки удаления данных.
    """
    
    # Language attribute
    current_language = 'en'

    # Texts in different languages
    texts = {
        'en': {
            'allshifts':"All shifts for period?",
            'infoAboutPeriodsAndbuttons': (
                "Select the calculation period and the corresponding function. \n"
                "Click on the desired month and choose the required options."
            ),
            'infoaboutWagesFunc': (
                "Wage calculation function:\n"
                "Calculates the total number of shifts\n"
                "for the selected period."
            ),
            'infoaboutIncomeFunc': (
                "Income calculation function:\n"
                "Retrieves income data from retail locations\n for the selected period."
            ),
            'infoAboutShiftEverydayFunc': (
                "Calculates daily wages\n tracks worker location,\n and assigns shifts by day."
            ),
            'infoaboutShiftEveryday':"Shifts for every day?",
            'infoAboutDeleteButton': "Deletes all input info from table",
            'income_from_shopsINFO': "Count income from shops?",
              'months': [
                "January ❄️", "February 🌨️", "March 🌸", "April 🌹", "May 🌺", "June ☀️",
                "July 🌞", "August 😢", "September 😭", "October🍁 ", "November 🍂", "December ☃️"
            ],
            'change':"Change period?🌗",
        },
        'ru': {
            'change':"Сменить период?🌗",
            'allshifts':"Сумма смен за РП?",
            'infoAboutPeriodsAndbuttons': (
                "Выберите период расчета и соответствующую функцию. \n"
                "Нажмите на нужный месяц и выберите необходимые параметры."
            ),
            'infoaboutWagesFunc': (
                "Функция расчета заработной платы:\n"
                "Рассчитывает общее количество смен\n"
                "за выбранный период."
            ),
            'infoaboutShiftEveryday':"Смены за каждый день?",
            'infoaboutIncomeFunc': (
                "Функция расчета доходов:\n"
                "Получает данные о доходах\n из торговых точек\n за выбранный период."
            ),
            'infoAboutShiftEverydayFunc': (
                "Рассчитывает ежедневную зарплату\n отслеживает местоположение работника,\n и назначает смены по дням."
            ),
            'infoAboutDeleteButton': "Удаляет всю введенную \nинформацию из таблицы",
            'income_from_shopsINFO': "Доходы из магазинов?",      
                'months': [
                "Январь ❄️", "Февраль 🌨️", "Март 🌸", "Апрель 🌹", "Май 🌺", "Июнь ☀️",
                "Июль 🌞", "Август 😢", "Сентябрь 😭", "Октябрь🍁 ", "Ноябрь 🍂", "Декабрь ☃️"
            ]

        }
    }

    # Method to switch language
    @classmethod
    def switch_language(cls):
        cls.current_language = 'en' if cls.current_language == 'ru' else 'ru'
        cls.update_texts()

    # Method to update texts based on current language
    @classmethod
    def update_texts(cls):
        lang = cls.current_language
        cls.infoAboutPeriodsAndbuttons = cls.texts[lang]['infoAboutPeriodsAndbuttons']
        cls.infoaboutWagesFunc = cls.texts[lang]['infoaboutWagesFunc']
        cls.infoaboutIncomeFunc = cls.texts[lang]['infoaboutIncomeFunc']
        cls.infoAboutShiftEverydayFunc = cls.texts[lang]['infoAboutShiftEverydayFunc']
        cls.infoAboutShiftEveryday = cls.texts[lang]['infoaboutShiftEveryday']
        cls.infoAboutDeleteButton = cls.texts[lang]['infoAboutDeleteButton']
        cls.income_from_shopsINFO = cls.texts[lang]['income_from_shopsINFO']
        cls.allshifts = cls.texts[lang]['allshifts']
        cls.months = cls.texts[lang]['months']
        cls.change = cls.texts[lang]['change']

    # data variables for computations
    days_in_month = 31
    sheetKOM = None
    shtKOM_id = "1vAVIeR4UWVAx7KwAR6x23yT_Ha1KTuc8VjcTVjnTM_8"

    sheetPIK = None
    shtPIK_id = "1DlRu9fzlzJj4Uor4FvXp9IEwi4FJfKq4bD7cN9GbtW0"

    sheetJUNE = None
    shtJUN_id = "17tnMhq5fp9IEatRqLnlyeemhbNP4aGOblGWpJ4_ABYs"

    sheetLM = None
    shtLM_id = "1PIICQiP3Tr1gmw4CsQ1bxVbkaU4mOPm_6409W-b7K3E"

    dataKOM = None

    dataPIK = None

    dataJUNE = None

    dataLM = None

# Initialize texts
Variables_WC.update_texts()

class ResChooser:
    """
    A class to create a resolution chooser window using Tkinter.

    Attributes
    ----------
    main_window_res : str
        The default resolution for the main window.
    RESOLUTIONS : dict
        A dictionary containing resolution options.

    Methods
    -------
    __init__(parent=None)
        Initializes the ResChooser window with resolution options.
    choose_resolution()
        Selects a resolution from the list and closes the window.
    get_resolution()
        Starts the window main loop and returns the selected resolution.
    """

    def __init__(self, parent=None):
        """Создает окно выбора разрешения."""
        
        self.root = tk.Toplevel(parent) if parent else tk.Tk()
        self.root.resizable(0, 0)
        self.root.title("Resolution Choice")
        self.root.attributes('-topmost', 1)
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        self.RESOLUTIONS = {
            "small | маленькое": f"{int(screen_width * 0.65)}x{int(screen_height * 0.65)}",
            "medium | среднее": f"{int(screen_width * 0.75)}x{int(screen_height * 0.75)}",
            "big | большое": f"{int(screen_width * 0.85)}x{int(screen_height * 0.85)}"
        }
        self.main_window_res = self.RESOLUTIONS["medium | среднее"]  # Значение по умолчанию


        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        position_x = (screen_width - 300) // 2
        position_y = (screen_height - 300) // 2
        self.root.geometry(f"240x220+{position_x}+{position_y}")

        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

        self.label = tk.Label(
            self.root, text="Choose preferred resolution:\nВыберете желаемый размер окна:\n(для ноутов рекомендую маленький)", font=("Arial", 9, "bold"))
        self.label.grid(row=0, column=0)

        self.listbox = tk.Listbox(
            self.root, selectmode="single", height=len(self.RESOLUTIONS), width=20)
        for res in self.RESOLUTIONS:
            self.listbox.insert("end", res)
        self.listbox.grid(row=1, column=0)

        self.btn_choose = tk.Button(
            self.root, text="Выбрать", height=2, width=10, font=("Arial", 12), command=self.choose_resolution
        )
        self.btn_choose.grid(row=2, column=0)

    def choose_resolution(self):
        """Выбор разрешения из списка и закрытие окна."""
        selected = self.listbox.curselection()
        if selected:
            self.main_window_res = self.RESOLUTIONS[self.listbox.get(
                selected[0])]
        self.root.destroy()

    def get_resolution(self):
        """Запуск окна и возврат выбранного разрешения."""
        self.root.mainloop()
        return self.main_window_res

class EMP_list_creator:
    """Диалоговое окно задания списка работников"""

    def __init__(self, parent=None):
        """Создает окно записания списка работников"""

        self.root = tk.Toplevel(parent) if parent else tk.Tk()
        self.root.resizable(False, False)
        self.root.title("Employee Creator")
        self.root.attributes('-topmost', 1)
        self.employees_list = []
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        position_x = (screen_width - 300) // 2
        position_y = (screen_height - 300) // 2

        self.root.geometry(f'450x540+{position_x}+{position_y}')

        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

        self.label = tk.Label(
            self.root, text="Enter employees (one per line):\nЗапишите сотрудников (Каждый сотрудник на своей линии)\nВ случае, если менять список сотрудников не нужно,\n то просто нажмите на кнопку ниже,\n при этом не вводя имена сотрудников.", font=("Arial", 11, "bold"))
        self.label.grid(row=0, column=0)


        self.textbox = tk.Text(self.root,bg='white', fg='black',height=20,width=40 ,font=("Arial", 9, "bold"))
        self.textbox.grid(row=2, column=0)

        self.btn_choose = tk.Button(
            self.root, text="Отправить", height=2, width=10, font=("Arial", 12), command=self.make_list_of_emp
        )
        self.btn_choose.grid(row=4, column=0)

    def make_list_of_emp(self):
        """Создание списка работников в таблицу"""
        string_input = self.textbox.get("1.0", 'end-1c')
        self.employees_list = string_input.split("\n")  # Разделяем по строкам
        self.employees_list = [emp.strip() for emp in self.employees_list if emp.strip()]
        self.root.destroy()

    def get_list(self):
        """Запуск окна и возврат выбранного списка."""
        self.root.mainloop()
        return self.employees_list


class OptimizedWindows:
    """Класс, содержащий утилитарные методы для настройки DPI, определения пути исполняемого файла
    и проверки масштабирования окна.

    Методы:
        optForWindowSize() -> None:
            Устанавливает DPI-осведомленность процесса для предотвращения размытия интерфейса.

        optIfAppIsCompiled() -> str:
            Определяет путь к исполняемому файлу, учитывая запуск из скомпилированного пакета (PyInstaller).

        checkWindowDPI() -> float:
            Проверяет масштабирование окна, возвращая коэффициент DPI.
    """

    @staticmethod
    def optForWindowSize() -> None:
        """Устанавливает DPI-осведомленность процесса для предотвращения размытия интерфейса."""
        try:
            ctypes.windll.shcore.SetProcessDpiAwareness(
                2)  # Per-monitor DPI awareness
        except AttributeError:
            pass

    @staticmethod
    def optIfAppIsCompiled() -> str:
        """Определяет путь к исполняемому файлу, учитывая запуск из скомпилированного пакета (PyInstaller)."""
        if getattr(sys, 'frozen', False):
            return sys._MEIPASS
        return os.path.abspath(os.path.dirname(__file__))

    @staticmethod
    def checkWindowDPI():
        """Проверяет масштабирование окна, возвращая коэффициент DPI."""
        root = tk.Tk()
        scaling_factor = root.winfo_fpixels('1i') / 96  # Базовый DPI — 96
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        root.destroy()
        return scaling_factor, screen_height, screen_width

    @staticmethod
    def adjust_window_size(screen_width, screen_height, width, height):
        """
        Этот метод настраивает размер и позицию окна в зависимости от разрешения экрана и желаемых размеров.

        Аргументы:
            screen_width (int): Ширина экрана.
            screen_height (int): Высота экрана.
            width (int): Желаемая ширина окна.
            height (int): Желаемая высота окна.

        Возвращает:
            tuple: Новый размер окна (ширина, высота) и его позиция (x, y).
        """
        # Базовое разрешение, относительно которого настраиваем масштаб
        base_width, base_height = screen_width, screen_height

        # Вычисляем коэффициент масштабирования
        scaling_factor = min(width / base_width, height / base_height)

        # Подгоняем итоговый коэффициент
        scale_factor = 1 / scaling_factor if scaling_factor > 1 else scaling_factor

        # Вычисляем итоговый размер окна с учетом масштабирования
        window_width = int(width * scale_factor)
        window_height = int(height * scale_factor)

        # Рассчитываем позицию окна для центрирования
        position_x = (screen_width - window_width) // 2
        position_y = (screen_height - window_height) // 2

        return window_width, window_height, position_x, position_y, scale_factor
