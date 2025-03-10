import tkinter as tk
import os

import gspread
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.discovery import build


# Model
from Model.Updater import Updater
from Model.Parser import Parser

# View
from View.UI import UiManager

# Presenter
from Presenter.presenter import WebPresenter

# addons
from Addons.ResChooser import ResChooser  #Выбор размер окна
from Addons.EMP_Creator import EMP_list_creator #Создание списка или изменение списка работников при необходимости
from Addons.OptimizedWindows import OptimizedWindows #Оптимизация под масштаб в винде(для ноутов)
from Addons.VARIABLES_WC import Variables_WC # Модуль с информационными переменными
from Addons.QOL import QOL # Модуль с методами для упрощения жизни

if __name__ == "__main__":

    OptimizedWindows.optForWindowSize()
    bundle_dir = OptimizedWindows.optIfAppIsCompiled()

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

    days_in_month = Variables_WC.days_in_month
    sheetKOM = Variables_WC.sheetKOM
    shtKOM_id = Variables_WC.shtKOM_id
    sheetPIK = Variables_WC.sheetPIK
    shtPIK_id = Variables_WC.shtPIK_id
    sheetJUNE = Variables_WC.sheetJUNE
    shtJUN_id = Variables_WC.shtJUN_id
    sheetLM = Variables_WC.sheetLM
    shtLM_id = Variables_WC.shtLM_id
    dataKOM = Variables_WC.dataKOM
    dataPIK = Variables_WC.dataPIK
    dataJUNE = Variables_WC.dataJUNE
    dataLM = Variables_WC.dataLM

    QOL.ensure_cell_value(sheetWAGES,31)
    #Вызываю набор списка работников
    empCRTR = EMP_list_creator()
    list_of_emp = empCRTR.get_list()
    Updater.send_emp_list(list_of_emp,sheetWAGES)

    # вызываю выбор разрешения
    chooser = ResChooser()
    selected_resolution = chooser.get_resolution()

    width, height = map(int, selected_resolution.split("x"))
    scaling_factor, screen_height, screen_width = OptimizedWindows.checkWindowDPI()

    root = tk.Tk()
    root.resizable(False, False)
    root.title("shifts and income AW")

    window_width, window_height, position_x, position_y, scale_factor = OptimizedWindows.adjust_window_size(
        screen_width, screen_height, width, height)
    root.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")

    # Создаём экземпляр View
    ui = UiManager(root, QOL, Variables_WC, scale_factor)

    # Создаем Presenter, передавая в него все необходимые зависимости и ссылку на View
    presenter = WebPresenter(ui, client, QOL, Parser, Updater, Variables_WC,
                             service, sheetWAGES, shtKOM_id, shtPIK_id, shtJUN_id, shtLM_id)

    # Передаем Presenter в View
    ui.presenter = presenter
    ui.run()
