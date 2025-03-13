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
                "Получает данные о доходах из торговых точек\n за выбранный период."
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
