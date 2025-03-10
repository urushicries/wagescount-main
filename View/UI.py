# ui_manager.py
import tkinter as tk
from tkinter import BooleanVar


class UiManager:

    """
    UiManager – отвечает за отрисовку UI и сбор пользовательского ввода.
    """

    def __init__(self, root, QOL, infoVariables, scale_factor=1):
        # инициализация объектов переменных для объектов интерфейса
        self.label_success_info = None
        self.label_error_info = None
        self.label_footer_info = None
        self.label_daily_info = None
        self.t_set_up_shifts_for_all_days_check = None
        self.t_income_from_shops_check = None
        self.label_income_info = None
        self.delete_button = None
        self.label_wages_info = None
        self.t_wages_whole_month_check = None
        self.labelDeleteInfo = None
        self.toggle_button = None
        self.label_instructions = None
        self.label_period_info = None

        self.root = root
        self.QOL = QOL
        self.infoVariables = infoVariables
        self.scale_factor = scale_factor
        self.days_in_month = 31  # значение периода по умолчанию

        # переменные для чекбоксов
        self.t_wages_whole_month_var1 = BooleanVar()
        self.t_income_from_shops_var2 = BooleanVar()
        self.t_set_up_shifts_for_all_days_var3 = BooleanVar()

        self.presenter = None  # Presenter будет установлен извне

        self.setup_ui()


    # Методы, вызываемые Presenter-ом для отображения сообщений:
    def nothing_picked(self):
        self.label_error_info.config(
            text="Выберите хотя бы \nодну функцию❎", font=("Arial", 20, "bold"))
        self.root.after(3000, lambda: self.label_error_info.config(text=""))

    def success(self):
        self.label_success_info.config(
            text="Успех!☑", font=("Arial", 30, "bold"))
        self.root.after(3000, lambda: self.label_success_info.config(text=""))

    def show_error(self, message):
        self.label_error_info.config(text=message, font=("Arial", 30, "bold"))
        self.root.after(3000, lambda: self.label_error_info.config(text=""))

    # Обработчик нажатия кнопки месяца – делегирует вызов презентеру
    def on_button_click(self, month):
        checkboxes = {
            'wages': self.t_wages_whole_month_var1.get(),
            'income': self.t_income_from_shops_var2.get(),
            'shifts': self.t_set_up_shifts_for_all_days_var3.get()
        }
        if self.presenter:
            self.presenter.send_request(month, checkboxes, self.days_in_month)
        else:
            print("Presenter is not set!")
            print(self.presenter)

    def toggle_days(self):
        # Логика переключения периода – можно оставить в View
        if self.t_wages_whole_month_var1.get() or self.t_set_up_shifts_for_all_days_var3.get():
            self.label_error_info.config(text=" ")
        if self.days_in_month == 15:
            self.days_in_month = 31
            self.presenter.toggle_RP_button(self.days_in_month)
            self.label_period_info.config(
                text=f"Count from {self.days_in_month - 15}    to:    {self.days_in_month}")
            print("Поменял РП с \"1 до 15\" на \"16 до 31\"")
        else:
            self.days_in_month = 15
            self.presenter.toggle_RP_button(self.days_in_month)
            self.label_period_info.config(
                text=f"Count from {self.days_in_month - 14}    to:    {self.days_in_month}")
            print("Поменял РП с \"16 до 31\" на \"1 до 15\" ")

    def delete_ranges(self):
        # При нажатии кнопки удаления делегируем вызов Presenter-у
        if self.presenter:
            self.presenter.sentRdelete()
            self.success()

    def setup_ui(self):
        self.root.configure(bg="black")
        btn_width = int(22 * self.scale_factor)
        font_size = int(25 * self.scale_factor)
        padx = int(10 * self.scale_factor)
        pady = int(10 * self.scale_factor)


        num_columns = 4  # число колонок

        #BUTTONS

        # Создаем кнопки для каждого месяца
        for i, month in enumerate(self.infoVariables.months):
            button = tk.Button(self.root, text=month, height=2, width=btn_width,
                               command=lambda m=month: self.on_button_click(m),
                               bg="white", fg="black",
                               font=("Arial", font_size, "bold"), relief="sunken")
            row = i // num_columns
            column = i % num_columns
            button.grid(row=row, column=column, padx=padx,
                        pady=pady, sticky="nsew")

        # Равномерное распределение колонок и строк
        for i in range(num_columns):
            self.root.grid_columnconfigure(i, weight=1, uniform="equal")
        for i in range((len(self.infoVariables.months) + num_columns - 1) // num_columns):
            self.root.grid_rowconfigure(i, weight=1, uniform="equal")

        # Переключить РП
        self.toggle_button = tk.Button(
            self.root,
            text="Change period?🌗",
            font=("Roboto", int(30 * self.scale_factor)),
            bg="white", fg="black", padx=btn_width//2,
            command=self.toggle_days
        )
        self.toggle_button.grid(row=6, column=1, pady=int(
            30 * self.scale_factor), columnspan=3)

        # Кнопка удалить все?
        self.delete_button = tk.Button(
            self.root,
            text="Clear everything up? 🗑️",
            font=("Roboto", int(20 * self.scale_factor)),
            bg="white", fg="black",
            command=self.delete_ranges
        )
        self.delete_button.grid(
            row=7, column=3, pady=int(30 * self.scale_factor))


        #CHECK BOXES

        # Переключатель смены за весь РП
        self.t_wages_whole_month_check = tk.Checkbutton(
            self.root,
            text="All shifts for period?",
            variable=self.t_wages_whole_month_var1,
            bg="white", fg="black",
            font=("Roboto", int(24 * self.scale_factor), "bold")
        )
        self.t_wages_whole_month_check.grid(
            row=7, column=0, pady=pady, padx=padx)

        # Переключатель прихода
        self.t_income_from_shops_check = tk.Checkbutton(
            self.root,
            text=self.infoVariables.income_from_shopsINFO,
            variable=self.t_income_from_shops_var2,
            bg="white", fg="black",
            font=("Roboto", int(24 * self.scale_factor), "bold")
        )
        self.t_income_from_shops_check.grid(
            row=7, column=2, pady=pady, padx=padx)

        # Переключатель смены на все дни
        self.t_set_up_shifts_for_all_days_check = tk.Checkbutton(
            self.root,
            text="Shifts for every day?",
            variable=self.t_set_up_shifts_for_all_days_var3,
            bg="white", fg="black",
            font=("Roboto", int(24 * self.scale_factor), "bold")
        )
        self.t_set_up_shifts_for_all_days_check.grid(
            row=7, column=1, pady=pady, padx=padx)


        #LABES

        # Надпись инфа про период
        self.label_period_info = tk.Label(
            self.root,
            text=f"Count from {self.days_in_month - 15}    to:    {self.days_in_month}",
            font=("Roboto", int(25 * self.scale_factor), "bold"),
            bg="black", fg="white"
        )
        self.label_period_info.grid(
            row=6, column=0, pady=pady, padx=padx, columnspan=3)

        # Надписи инструкции
        self.label_instructions = tk.Label(
            self.root,
            text=self.infoVariables.infoAboutPeriodsAndbuttons,
            font=("Roboto", int(15 * self.scale_factor), "bold"),
            bg="black", fg="white"
        )
        self.label_instructions.grid(row=3, column=1, pady=pady, columnspan=2)

        # Надпись инфа про удаление всех данных из ТБ
        self.labelDeleteInfo = tk.Label(
            self.root,
            text=self.infoVariables.infoAboutDeleteButton,
            font=("Roboto", int(19 * self.scale_factor), "bold"),
            bg="black", fg="white"
        )
        self.labelDeleteInfo.grid(row=8, column=3)

        # Надпись инфа про весь РП функции
        self.label_wages_info = tk.Label(
            self.root,
            text=self.infoVariables.infoaboutWagesFunc,
            font=("Roboto", int(15 * self.scale_factor), "bold"),
            bg="black", fg="white"
        )
        self.label_wages_info.grid(
            row=8, column=1, pady=int(20 * self.scale_factor))

        # Надпись инфа про приходную функцию
        self.label_income_info = tk.Label(
            self.root,
            text=self.infoVariables.infoaboutIncomeFunc,
            font=("Roboto", int(15 * self.scale_factor), "bold"),
            bg="black", fg="white"
        )
        self.label_income_info.grid(
            row=8, column=0, pady=int(20 * self.scale_factor))

        # Надпись внизу
        self.label_footer_info = tk.Label(
            self.root,
            text="would i lose?\nnah i'd win\nver 0.1.8",
            bg="black", fg="white",
            font=("Arial", int(14 * self.scale_factor), "bold")
        )
        self.label_footer_info.grid(row=10, column=0, columnspan=4)

        # Надпись инфа про каждодневную функцию
        self.label_daily_info = tk.Label(
            self.root,
            text=self.infoVariables.infoAboutShiftEverydayFunc,
            font=("Roboto", int(15 * self.scale_factor), "bold"),
            bg="black", fg="white"
        )
        self.label_daily_info.grid(
            row=8, column=2, pady=int(18 * self.scale_factor))

        # Надпись ошибка
        self.label_error_info = tk.Label(
            self.root,
            text="",
            bg="black", fg="red",
            font=("Arial", int(15 * self.scale_factor))
        )
        self.label_error_info.grid(row=6, column=0)

        # Надпись успех
        self.label_success_info = tk.Label(
            self.root,
            text="",
            bg="black", fg="lightgreen",
            font=("Arial", int(15 * self.scale_factor))
        )
        self.label_success_info.grid(row=6, column=3)

    def run(self):
        self.root.mainloop()
