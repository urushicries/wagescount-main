# WagesCount

**WagesCount** – это программа на Python для автоматизации расчёта заработной платы с использованием данных из Google Sheets. Программа извлекает информацию о сменах и доходах из различных таблиц Google Sheets, обрабатывает эти данные и обновляет сводные таблицы зарплат.

## Возможности

- **Извлечение данных**: Получение информации о сменах и доходах из нескольких листов Google Sheets.
- **Обработка периодов**: Поддержка двух периодов месяца:
  - С 1 по 15 число (формат ячеек `15.xx.xxxx`)
  - С 15 по 31 число (форматы ячеек `31.xx.xxxx`, `30.xx.xxxx`, `29.xx.xxxx`, `28.xx.xxxx`)
- **Анализ смен**: Парсинг строк с информацией о сменах сотрудников, суммирование их рабочего времени.
- **Обновление таблиц**: Автоматическое обновление таблиц зарплат:
  - Общая сумма смен за месяц.
  - Смены по дням для сотрудников.
  - Информация по торговым площадкам.
- **Очистка диапазонов**: Возможность очистки заданных диапазонов в таблице (например, в листе `WGSlist`).
- **Переключение периода**: Функция для автоматической смены значения ячейки (E93) в зависимости от выбранного периода (15 или 31).

## Требования

- **Python 3.10+** (использование синтаксиса `int | None`).
- Библиотеки:
  - [gspread](https://github.com/burnash/gspread) — для работы с Google Sheets.
  - [oauth2client](https://github.com/googleapis/oauth2client) — для авторизации в Google API.
  - `logging` — стандартный модуль для ведения логов.
- Аккаунт сервисного доступа Google с соответствующим JSON-файлом учетных данных.
- Включённый Google Sheets API в консоли Google Cloud.

## Установка

1. **Клонируйте репозиторий:**

   ```bash
   git clone https://github.com/yourusername/wagescount.git
   ```

2. **Создайте виртуальное окружение и активируйте его:**

   ```bash
   cd wagescount
   python -m venv venv
   source venv/bin/activate  # Для Windows: venv\Scripts\activate
   ```

3. **Установите зависимости:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Сохраните файл с учётными данными** (например, `credentials.json`) в корневой каталог проекта.

## Настройка

Обновите в коде путь к вашему JSON-файлу с учётными данными и проверьте доступ к нужным таблицам. Пример настройки авторизации:

```python
import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('path/to/credentials.json', scope)
client = gspread.authorize(credentials)
```

Убедитесь, что у сервисного аккаунта есть доступ к таблицам, с которыми вы планируете работать.

## Использование

Ниже приведён пример интеграции основных функций из модуля:

```python
import wagescount

# Авторизация и подключение к Google Sheets
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('path/to/credentials.json', scope)
client = gspread.authorize(credentials)

# Открытие необходимых листов по ID и имени листа
sheetKOM = client.open_by_key('spreadsheet_id_KOM').worksheet('KOM')
sheetPIK = client.open_by_key('spreadsheet_id_PIK').worksheet('PIK')
sheetJUNE = client.open_by_key('spreadsheet_id_JUNE').worksheet('JUNE')
sheetLM = client.open_by_key('spreadsheet_id_LM').worksheet('LM')

# Получение данных для периода с 1 по 15 число
data15KOM, data15PIK, data15LM, data15JUNE = wagescount.makeDataFromSheets(15, sheetKOM, sheetPIK, sheetJUNE, sheetLM)

# Парсинг информации о сменах сотрудников
employee_shifts = wagescount.parseDataNamesShift(data15KOM, data15PIK, data15JUNE, data15LM)

# Подсчёт суммарного количества смен для каждого сотрудника
employee_shift_dict = wagescount.makeDictEmpTot(employee_shifts)

# Обновление таблицы зарплат
sheetWGSlist = client.open_by_key('spreadsheet_id_WGSlist').worksheet('WGSlist')
wagescount.update_info_WAGES(employee_shift_dict, employee_shifts, sheetWGSlist)
```

Функции из модулей:
- `ffcwp15(sheet)` — находит первую ячейку с форматом `15.xx.xxxx` в первом столбце.
- `ffcwpend(sheet)` — находит первую ячейку с одним из форматов (`31.xx.xxxx`, `30.xx.xxxx` и т.д.) с приоритетом 31, 30, 29, 28.
- `makeDataFromSheets(pattern, *sheets)` — получает данные из нескольких листов для указанного периода (15 или 31).
- `find_cells_by_type_content(client, spreadsheet_id, sheet_name)` — находит ячейки, содержащие числовые значения (доходы).
- `parseINCOMEfromSHEETS(client, month, *sheet_ids)` — парсит данные о доходах с указанных листов.
- `parseDataNamesShift(*datasets)` — извлекает данные о сменах сотрудников.
- `makeDictEmpTot(emp_shift)` — агрегирует смены для каждого сотрудника.
- `update_info_WAGES(...)` — обновляет сводную информацию о сменах за месяц.
- `update_info_everyday(...)` и `update_info_everyday_TRADEPLACES(...)` — обновляют данные по сменам для каждого дня.
- `update_table_from_lists(sheetLink, *lists)` — обновляет таблицу доходов.
- `clear_wgslist_ranges(service, spreadsheet_id, ranges)` — очищает заданные диапазоны в таблице.
- `toggle_cell_value(sheet, days_in_month)` — переключает значение ячейки (E93) в зависимости от выбранного периода.


## Вклад в проект

Если у вас есть предложения или вы обнаружили ошибку, создайте issue или отправьте pull request с улучшениями.
