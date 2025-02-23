import tkinter as tk

def checkWindowDPI():
    root = tk.Tk()
    scaling_factor = root.winfo_fpixels('1i') / 96  # Базовый DPI — 96
    root.destroy()
    return scaling_factor

def configureMonthBurronsInterface(root : object, btn_width : int, padx : int, pady : int, font_size : int, on_button_click : object):
    months = ["Январь", "Февраль", "Март", "Апрель", "Май", "Июнь", "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"]

    for i, month in enumerate(months):
        button = tk.Button(root, text=month, width=btn_width, command=lambda m=month: on_button_click(m), bg="#000000", fg="black",
                        font=("Arial", font_size,"bold"), relief="sunken")
        button.grid(row=i // 3, column=i % 3, padx=padx, pady=pady)
