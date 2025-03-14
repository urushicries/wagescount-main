
class WebPresenter:
    """A class used to represent a Web Presenter that handles data processing and updates for various sheets.

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
