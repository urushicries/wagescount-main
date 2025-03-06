
class Variables_WC:
    """Класс, содержащий текстовые инструкции и описания функций расчета.

    Атрибуты:
        infoAboutPeriodsAndbuttons (str): Инструкция по выбору периода и кнопок.
        infoaboutWagesFunc (str): Описание функции расчета заработной платы.
        infoaboutIncomeFunc (str): Описание функции расчета доходов торговых точек (арен).
        infoAboutShiftEverydayFunc (str): Описание функции расчета ежедневной зарплаты.
        infoAboutDeleteButton (str): Описание функции кнопки удаления данных.
    """
    # Текст для инструкции по выбору периода и кнопок
    infoAboutPeriodsAndbuttons = (
        "Select the calculation period and the corresponding function. \n"
        "Click on the desired month and choose the required options."
    )

    # Text describing the wage calculation function
    infoaboutWagesFunc = (
        "Wage calculation function:\n"
        "Calculates the total number of shifts\n"
        "for the selected period."
    )

    # Text describing the income calculation function for retail locations (arenas)
    infoaboutIncomeFunc = (
        "Income calculation function:\n"
        "Retrieves income data from retail locations\n for the selected period."
    )

    # Text describing the function for daily wage calculation
    infoAboutShiftEverydayFunc = (
        "Calculates daily wages\n tracks worker location,\n and assigns shifts by day.")

    infoAboutDeleteButton = "Deletes all input info from table"

    income_from_shopsINFO = "Count income from shops?"
    months = [
        "Январь ❄️", "Февраль 🌨️", "Март 🌸", "Апрель 🌹", "Май 🌺", "Июнь ☀️",
        "Июль 🌞", "Август 😢", "Сентябрь 😭", "Октябрь🍁 ", "Ноябрь 🍂", "Декабрь ☃️"
    ]


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
