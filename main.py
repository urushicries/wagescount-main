import tkinter as tk
import os

import gspread
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.discovery import build


# Model
from Model.UPDT import Updater

from Model.PARSmod import Parser

# View
from View.UI import UiManager

# Presenter
from Presenter.presenter import WebPresenter

# addons
from Addons.RES import ResChooser  # Модуль выбора разрешения окна проги
# Модуль оптимизации размера окна под масштаб(в винде под ноуты)
from Addons.DIRandUI import UandBundOpt
# Модуль с информациооными переменными
from Addons.VARIABLES import infoVariables
# Модуль с методами для упрощения жизни (quality of life)
from Addons.QOLmodule import QOL

if __name__ == "__main__":

    UandBundOpt.optForWindowSize()
    bundle_dir = UandBundOpt.optIfAppIsCompiled()

    # Define the relative path
    relative_path = "key.json"

    # Join the paths safely
    json_path = os.path.join(bundle_dir, relative_path)

    SERVICE_ACCOUNT_FILE = json_path

    try:
        open(SERVICE_ACCOUNT_FILE, 'r')
    except FileNotFoundError as e:
        print(f"\033[31mFile path is wrong, dumbass - error code : {e}\033[0m")
        exit(1)

    SCOPES = ["https://www.googleapis.com/auth/spreadsheets",
              "https://www.googleapis.com/auth/drive"]

    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        SERVICE_ACCOUNT_FILE, SCOPES)

    client = gspread.authorize(credentials)

    service = build('sheets', 'v4', credentials=credentials)
    sheetWAGES = client.open("! Таблица расчета зарплаты").worksheet("WGSlist")

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

    # вызываю выбор разрешения
    chooser = ResChooser()
    selected_resolution = chooser.get_resolution()

    width, height = map(int, selected_resolution.split("x"))
    scaling_factor, screen_height, screen_width = UandBundOpt.checkWindowDPI()

    root = tk.Tk()
    root.resizable(0, 0)
    root.title("Программа для расчет З/П Another World")

    window_width, window_height, position_x, position_y, scale_factor = UandBundOpt.adjust_window_size(
        screen_width, screen_height, width, height)
    root.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")

    # Создаём экземпляр View
    ui = UiManager(root, QOL, infoVariables, scale_factor)

    # Создаем Presenter, передавая в него все необходимые зависимости и ссылку на View
    presenter = WebPresenter(ui, client, QOL, Parser, Updater, infoVariables,
                             service, sheetWAGES, shtKOM_id, shtPIK_id, shtJUN_id, shtLM_id)

    # Передаем Presenter в View
    ui.presenter = presenter
    ui.run()
