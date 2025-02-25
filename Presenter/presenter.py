# presenter.py

class WebPresenter:
    def __init__(self, view, client, QOL, Parser, Updater, infoVariables,
                 service, sheetWAGES, shtKOM_id, shtPIK_id, shtJUN_id, shtLM_id):

        self.view = view  # Ссылка на View (UiManager)
        self.client = client
        self.QOL = QOL
        self.Parser = Parser
        self.Updater = Updater
        self.infoVariables = infoVariables
        self.service = service
        self.sheetWAGES = sheetWAGES
        self.shtKOM_id = shtKOM_id
        self.shtPIK_id = shtPIK_id
        self.shtJUN_id = shtJUN_id
        self.shtLM_id = shtLM_id
        self.days_in_month = 15

    def send_request(self, month, checkboxes, days_in_month):
        """
        checkboxes – словарь с булевыми значениями для ключей:
          'wages'  – для всей зарплаты,
          'income' – для дохода из арен,
          'shifts' – для смен за каждый день.
        """
        # Если ни одна функция не выбрана, сообщаем об ошибке через View
        if not (checkboxes.get('wages') or checkboxes.get('income') or checkboxes.get('shifts')):
            self.view.nothing_picked()
            return

        # Данные по месяцам
        months_data = {
            "Январь": {"sheet_suffix": "Январь25", "days": days_in_month},
            "Февраль": {"sheet_suffix": "Февраль25", "days": days_in_month},
            "Март": {"sheet_suffix": "Март25", "days": days_in_month},
            "Апрель": {"sheet_suffix": "Апрель25", "days": days_in_month},
            "Май": {"sheet_suffix": "Май25", "days": days_in_month},
            "Июнь": {"sheet_suffix": "Июнь25", "days": days_in_month},
            "Июль": {"sheet_suffix": "Июль25", "days": days_in_month},
            "Август": {"sheet_suffix": "Август25", "days": days_in_month},
            "Сентябрь": {"sheet_suffix": "Сентябрь25", "days": days_in_month},
            "Октябрь": {"sheet_suffix": "Октябрь25", "days": days_in_month},
            "Ноябрь": {"sheet_suffix": "Ноябрь25", "days": days_in_month},
            "Декабрь": {"sheet_suffix": "Декабрь25", "days": days_in_month}
        }

        month_data = months_data.get(month)
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
                incomeKOM, incomePIK, incomeJUNE, incomeLM = self.Parser.parseINCOMEfromSHEETS(
                    self.client, month_data["sheet_suffix"],
                    self.shtKOM_id, self.shtPIK_id, self.shtJUN_id, self.shtLM_id
                )

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
                        self.sheetWAGES, incomeKOM, incomePIK, incomeJUNE, incomeLM)

            # Если всё прошло успешно – уведомляем View
            self.view.success()
        except Exception as e:
            print(f"Error occurred while processing sheets for {month}: {e}")
            self.view.show_error(str(e))

    def sentRdelete(self):
        # Пример метода для удаления диапазонов; бизнес-логика в Presenter
        self.QOL.clear_wgslist_ranges(
            self.service, "14FtsvGplg1jKXJvLJCueI8iEEnjJUtjk17NuPqeCnqo")

    def toggle_RP_button(self, days_in_month):
        # Пример вызова бизнес-логики из QOL
        self.QOL.toggle_cell_value(self.sheetWAGES, days_in_month)
