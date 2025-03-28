import tkinter as tk
import os
import sys

import gspread
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.discovery import build
from google.auth.exceptions import RefreshError
import google  # Add this import to fix the NameError
import logging


# Model
from Model.Updater import Updater
from Model.Parser import Parser

# View
from View.UiManager import UiManager

# Presenter
from Controller.Controller import WebController

# addons
from Addons.ResChooser import ResChooser  # Выбор размер окна
# Создание списка или изменение списка работников при необходимости
from Addons.EMP_Creator import EMP_list_creator
# Оптимизация под масштаб в винде(для ноутов)
from Addons.OptimizedWindows import OptimizedWindows
# Модуль с информационными переменными
from Addons.VARIABLES_WC import Variables_WC
from Addons.QOL import QOL  # Модуль с методами для упрощения жизни


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("application.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


if __name__ == "__main__":
    ui = None
    OptimizedWindows.optForWindowSize()
    bundle_dir = OptimizedWindows.optIfAppIsCompiled()

    # Define the relative path
    relative_path = resource_path("key.json")

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

    try:
        credentials = ServiceAccountCredentials.from_json_keyfile_name(
            SERVICE_ACCOUNT_FILE, SCOPES)
        client = gspread.authorize(credentials)
        service = build('sheets', 'v4', credentials=credentials)
        sheetWAGES = client.open(
            "! Таблица расчета зарплаты").worksheet("WGSlist")
    except FileNotFoundError:
        logger.error(
            f"Service account file not found at {SERVICE_ACCOUNT_FILE}. Please check the file path.")
        sys.exit(1)
    except gspread.exceptions.APIError as e:
        logger.error(f"Error accessing Google Sheets API: {e}")
        sys.exit(1)
    except google.auth.exceptions.RefreshError as e:
        logger.error(
            f"Authentication failed: {e}. This may be due to an invalid JWT signature. "
            f"Please ensure the service account key file is valid and has the correct permissions. "
            f"Steps to resolve:\n"
            f"1. Verify the key file at {SERVICE_ACCOUNT_FILE}.\n"
            f"2. Ensure the key file matches the service account in your Google Cloud project.\n"
            f"3. Check that the service account has access to the spreadsheet and the required APIs are enabled.\n"
            f"4. Regenerate the key file if necessary from the Google Cloud Console."
        )
        sys.exit(1)

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

    QOL.ensure_cell_value(sheetWAGES, 31)
    # Вызываю набор списка работников
    empCRTR = EMP_list_creator()
    list_of_emp = empCRTR.get_list()
    Updater.send_emp_list(list_of_emp, sheetWAGES)

    # вызываю выбор разрешения
    chooser = ResChooser()
    selected_resolution = chooser.get_resolution()

    width, height = map(int, selected_resolution.split("x"))
    scaling_factor, screen_height, screen_width = OptimizedWindows.checkWindowDPI()

    root = tk.Tk()
    root.resizable(False, False)
    root.title("AW")

    window_width, window_height, position_x, position_y, scale_factor = OptimizedWindows.adjust_window_size(
        screen_width, screen_height, width, height)
    root.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")

    config = {
        'root': root,
        'client': client,
        'QOL': QOL,
        'Parser': Parser,
        'Updater': Updater,
        'infoVariables': Variables_WC,
        'service': service,
        'sheetWAGES': sheetWAGES,
        'shtKOM_id': shtKOM_id,
        'shtPIK_id': shtPIK_id,
        'shtJUN_id': shtJUN_id,
        'shtLM_id': shtLM_id,
        'view': None
    }

    ui = UiManager(config, scale_factor)
    config['view'] = ui

    controller = WebController(config)

    ui.controller = controller
    ui.run()
