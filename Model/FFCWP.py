import re


def ffcwp15(sheet:object) -> int | None:
    """
    Находит первую ячейку в первом столбце с следующим форматом:
    '15.xx.xxxx'
    Args:
        sheet(object): таблица зп
    Returns:
        cell_id(int)
    """
    pattern = re.compile(r"^15\.\d{2}\.\d{4}$")
    column_data = sheet.col_values(1)  # Get all values in the first column

    return next(
        (row_num for row_num, value in enumerate(column_data, start=1) if pattern.match(value)),
        None
    )

def ffcwpend(sheet:object) -> int | None:
    """
    Находит первую ячейку в первом столбце с одним из следующих форматов:
    '31.xx.xxxx', '30.xx.xxxx', '29.xx.xxxx' или '28.xx.xxxx'.
    Приоритет: сначала '31.xx.xxxx', затем остальные по порядку.
    Args:
        sheet(object): таблица зп
    Returns:
        cell_id(int)
    """
    # Compile regexes once
    pattern31 = re.compile(r"^31\.\d{2}\.\d{4}$")
    pattern30 = re.compile(r"^30\.\d{2}\.\d{4}$")
    pattern29 = re.compile(r"^29\.\d{2}\.\d{4}$")
    pattern28 = re.compile(r"^28\.\d{2}\.\d{4}$")
    
    column_data = sheet.col_values(1)  

    cell_id_31 = None
    cell_id_30 = None
    cell_id_29 = None
    cell_id_28 = None

  
    for row_num, value in enumerate(column_data, start=1):
        if cell_id_31 is None and pattern31.match(value):
            cell_id_31 = row_num
        if cell_id_30 is None and pattern30.match(value):
            cell_id_30 = row_num
        if cell_id_29 is None and pattern29.match(value):
            cell_id_29 = row_num
        if cell_id_28 is None and pattern28.match(value):
            cell_id_28 = row_num

   
    if cell_id_31 is not None:
        return cell_id_31
    if cell_id_30 is not None:
        return cell_id_30
    if cell_id_29 is not None:
        return cell_id_29
    if cell_id_28 is not None:
        return cell_id_28

    return None  

def makeDataFromSheets(pattern : int,*sheets) -> tuple | None : 
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
        #1-15 числа
        data15KOMENDA = sheetKOM.get(f'A1:M{ffcwp15(sheetKOM)}')
        data15PIK = sheetPIK.get(f'A1:M{ffcwp15(sheetPIK)}')
        data15JUNE = sheetJUNE.get(f'A1:M{ffcwp15(sheetJUNE)}')
        data15LM = sheetLM.get(f'A1:M{ffcwp15(sheetLM)}')
        return  data15KOMENDA, data15PIK, data15LM, data15JUNE

    if pattern == 31:
        #15-31 числа
        data31KOMENDA = sheetKOM.get(f'A{ffcwp15(sheetKOM)}:M{ffcwpend(sheetKOM)+20}')
        data31PIK = sheetPIK.get(f'A{ffcwp15(sheetPIK)}:M{ffcwpend(sheetPIK)+20}')
        data31JUNE = sheetJUNE.get(f'A{ffcwp15(sheetJUNE)}:M{ffcwpend(sheetJUNE)+20}')
        data31LM = sheetLM.get(f'A{ffcwp15(sheetLM)}:M{ffcwpend(sheetLM)+20}')
        return  data31KOMENDA, data31PIK, data31LM, data31JUNE
    
    return None
