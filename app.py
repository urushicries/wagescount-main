import tkinter as tk


import gspread
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.discovery import build


from RES import ResChooser # Модуль выбора разрешения окна проги
from DIRandUI import UandBundOpt # Модуль оптимизации размера окна под масштаб(в винде под ноуты)
from VARIABLES import infoVariables #Модуль с информациооными переменными
from UI import UiManager # Модуль с настройкой UI и его функциональности
from UPDT import Updater # модуль с методами обновления таблицы ЗП
from PARSmod import Parser # Модуль с методами с копированием информации с отчетов и компоновкой ее в удобоворимый формат для обновления.
from QOLmodule import QOL # Модуль с методами для упрощения жизни (quality of life)



#вызываю выбор разрешения
chooser = ResChooser()
selected_resolution = chooser.get_resolution()

width, height = map(int, selected_resolution.split("x"))
scaling_factor = UandBundOpt.checkWindowDPI()


UandBundOpt.optForWindowSize()
bundle_dir = UandBundOpt.optIfAppIsCompiled()

root = tk.Tk()
root.resizable(0, 0)
root.title("Программа для расчет З/П Another World")

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()


# Базовое разрешение, относительно которого настраиваем масштаб
base_width, base_height = screen_width, screen_height

# Вычисляем коэффициент масштабирования
scaling_factor = min(width / base_width, height / base_height)

# Подгоняем итоговый коэффициент
scale_factor = 1 / scaling_factor if scaling_factor > 1 else scaling_factor



window_width = int(width * scale_factor)
window_height = int(height * scale_factor)



position_x = (screen_width - window_width) // 2
position_y = (screen_height - window_height) // 2

root.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")


# Build the correct path to the JSON file

json_path = "/Library/imp_files/key.json"

SERVICE_ACCOUNT_FILE = json_path   
SCOPES = ["https://www.googleapis.com/auth/spreadsheets", 
          "https://www.googleapis.com/auth/drive"]


if SERVICE_ACCOUNT_FILE is None:
    raise ValueError("The GOOGLE_APPLICATION_CREDENTIALS environment variable is not set or points to a non-existent file.")

credentials = ServiceAccountCredentials.from_json_keyfile_name(SERVICE_ACCOUNT_FILE, SCOPES)

client = gspread.authorize(credentials)
service = build('sheets', 'v4', credentials=credentials)

sheetWAGES = client.open("! Таблица расчета зарплаты").worksheet("WGSlist")

days_in_month = 15

sheetKOM =  None
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


UiManager(root,client,QOL,Parser,Updater,infoVariables,service,sheetWAGES,shtKOM_id,shtPIK_id,shtJUN_id,shtLM_id,scale_factor)
root.mainloop()