import ctypes
import os, sys
import tkinter as tk



class UandBundOpt:
    def optForWindowSize() -> None:
        try:
            ctypes.windll.shcore.SetProcessDpiAwareness(2)  # Per-monitor DPI awareness
        except AttributeError:
            pass 

    def optIfAppIsCompiled() -> str:
        if getattr(sys, 'frozen', False):

            bundle_dir = sys._MEIPASS
        else:
            bundle_dir = os.path.abspath(os.path.dirname(__file__))
        return bundle_dir

    def checkWindowDPI():
        root = tk.Tk()
        scaling_factor = root.winfo_fpixels('1i') / 96  # Базовый DPI — 96
        root.destroy()
        return scaling_factor
