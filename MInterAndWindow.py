import ctypes
import os, sys


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