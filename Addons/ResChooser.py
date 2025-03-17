import tkinter as tk


class ResChooser:
    """
    A class to create a resolution chooser window using Tkinter.

    Attributes
    ----------
    main_window_res : str
        The default resolution for the main window.
    RESOLUTIONS : dict
        A dictionary containing resolution options.

    Methods
    -------
    __init__(parent=None)
        Initializes the ResChooser window with resolution options.
    choose_resolution()
        Selects a resolution from the list and closes the window.
    get_resolution()
        Starts the window main loop and returns the selected resolution.
    """

    def __init__(self, parent=None):
        """Создает окно выбора разрешения."""
        self.main_window_res = "1680x850"  # Значение по умолчанию
        self.RESOLUTIONS = {"small | маленькое": "1450x720",
                            "medium | среднее": "1560x900",
                              "big | большое": "1680x850"}

        self.root = tk.Toplevel(parent) if parent else tk.Tk()
        self.root.resizable(0, 0)
        self.root.title("Resolution Choice")
        self.root.attributes('-topmost', 1)

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        position_x = (screen_width - 300) // 2
        position_y = (screen_height - 300) // 2
        self.root.geometry(f"240x220+{position_x}+{position_y}")

        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

        self.label = tk.Label(
            self.root, text="Choose preferred resolution:\nВыберете желаемый размер окна:\n(для ноутов рекомендую маленький)", font=("Arial", 12, "bold"))
        self.label.grid(row=0, column=0)

        self.listbox = tk.Listbox(
            self.root, selectmode="single", height=len(self.RESOLUTIONS), width=20)
        for res in self.RESOLUTIONS:
            self.listbox.insert("end", res)
        self.listbox.grid(row=1, column=0)

        self.btn_choose = tk.Button(
            self.root, text="Выбрать", height=2, width=10, font=("Arial", 12), command=self.choose_resolution
        )
        self.btn_choose.grid(row=2, column=0)

    def choose_resolution(self):
        """Выбор разрешения из списка и закрытие окна."""
        selected = self.listbox.curselection()
        if selected:
            self.main_window_res = self.RESOLUTIONS[self.listbox.get(
                selected[0])]
        self.root.destroy()

    def get_resolution(self):
        """Запуск окна и возврат выбранного разрешения."""
        self.root.mainloop()
        return self.main_window_res
