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


days_in_month = infoVariables.days_in_month
sheetKOM = infoVariables.sheetKOM
shtKOM_id = infoVariables.shtKOM_id
sheetPIK = infoVariables.sheetPIK
shtPIK_id = infoVariables.shtPIK_id
sheetJUNE = infoVariables.sheetJUNE
shtJUN_id = infoVariables.shtJUN_id
sheetLM = infoVariables.sheetLM
shtLM_id = infoVariables.shtLM_id
dataKOM = infoVariables.dataKOM
dataPIK = infoVariables.dataPIK
dataJUNE = infoVariables.dataJUNE
dataLM = infoVariables.dataLM


#вызываю выбор разрешения
chooser = ResChooser()
selected_resolution = chooser.get_resolution()

width, height = map(int, selected_resolution.split("x"))
scaling_factor, screen_height, screen_width = UandBundOpt.checkWindowDPI()


UandBundOpt.optForWindowSize()
bundle_dir = UandBundOpt.optIfAppIsCompiled()

root = tk.Tk()
root.resizable(0, 0)
root.title("Программа для расчет З/П Another World")



window_width, window_height, position_x, position_y , scale_factor = UandBundOpt.adjust_window_size(screen_width, screen_height, width, height)

root.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")


# Build the correct path to the JSON file
json_path = "/Library/imp_files/key.json"

SERVICE_ACCOUNT_FILE = json_path   

try:
    open(SERVICE_ACCOUNT_FILE,'r')
except FileNotFoundError as e:
    print(f"\033[31mFile path is wrong, dumbass - error code : {e}\033[0m")
    exit(1)
SCOPES = ["https://www.googleapis.com/auth/spreadsheets", 
          "https://www.googleapis.com/auth/drive"]


credentials = ServiceAccountCredentials.from_json_keyfile_name(SERVICE_ACCOUNT_FILE, SCOPES)

client = gspread.authorize(credentials)
service = build('sheets', 'v4', credentials=credentials)

sheetWAGES = client.open("! Таблица расчета зарплаты").worksheet("WGSlist")



UiManager(root,client, QOL, Parser, Updater, infoVariables, service, sheetWAGES, shtKOM_id, shtPIK_id, shtJUN_id, shtLM_id, scale_factor)