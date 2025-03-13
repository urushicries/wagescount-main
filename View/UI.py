# ui_manager.py
import tkinter as tk
from tkinter import BooleanVar


class UiManager:
    """
    Manages the user interface for the application.

    Attributes:
        root (tk.Tk): The root window of the Tkinter application.
        QOL (object): Quality of Life object, purpose not specified.
        infoVariables (object): Contains various information variables used in the UI.
        scale_factor (float): Scaling factor for UI elements, default is 1.
        days_in_month (int): Number of days in the current period, default is 31.
        presenter (object): Presenter object to handle business logic, set externally.

    Methods:
        nothing_picked(): Displays an error message when no function is selected.
        success(): Displays a success message.
        show_error(message): Displays a custom error message.
        on_button_click(month): Handles button click events for month buttons, delegates to presenter.
        toggle_days(): Toggles the period between 15 and 31 days and updates the UI.
        delete_ranges(): Handles the delete button click event, delegates to presenter.
        setup_ui(): Sets up the user interface elements.
        run(): Starts the Tkinter main loop.
    """


    def __init__(self, config, scale_factor=1):
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

        self.root = config['root']
        self.QOL = config['QOL']
        self.infoVariables = config['infoVariables']
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
        """
        Displays an error message indicating that at least one function must be selected.
        
        This method updates the `label_error_info` widget to show an error message
        in Russian, prompting the user to select at least one function. The message
        is displayed in bold Arial font with a size of 20. After 3 seconds, the 
        error message is cleared.
        """
        self.label_error_info.config(
            text="Выберите хотя бы \nодну функцию❎", font=("Arial", 20, "bold"))
        self.root.after(3000, lambda: self.label_error_info.config(text=""))

    def success(self):
        """
        Displays a success message on the label_success_info widget for 3 seconds.

        This method updates the text of the label_success_info widget to display
        a success message "Успех!☑" with a specific font style. After 3 seconds,
        the text is cleared.

        Args:
            None

        Returns:
            None
        """
        self.label_success_info.config(
            text="Успех!☑", font=("Arial", 30, "bold"))
        self.root.after(3000, lambda: self.label_success_info.config(text=""))

    def show_error(self, message):
        """
        Displays an error message on the UI for a short duration.

        Args:
            message (str): The error message to be displayed.
        """
        self.label_error_info.config(text=message, font=("Arial", 30, "bold"))
        self.root.after(3000, lambda: self.label_error_info.config(text=""))

    # Обработчик нажатия кнопки месяца – делегирует вызов презентеру
    def on_button_click(self, month):
        """
        Handles the button click event for a given month.

        This method retrieves the state of various checkboxes and sends a request
        to the presenter with the selected month, checkbox states, and the number
        of days in the month. If the presenter is not set, it prints an error message.

        Args:
            month (str): The month for which the request is being made.

        Attributes:
            t_wages_whole_month_var1 (tkinter.Variable): Variable linked to the 'wages' checkbox.
            t_income_from_shops_var2 (tkinter.Variable): Variable linked to the 'income' checkbox.
            t_set_up_shifts_for_all_days_var3 (tkinter.Variable): Variable linked to the 'shifts' checkbox.
            presenter (object): The presenter object responsible for handling the request.
            days_in_month (int): The number of days in the selected month.
        """
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
                text=f"{self.days_in_month - 15}    -    {self.days_in_month}")
            print("Поменял РП с \"1 до 15\" на \"16 до 31\"")
        else:
            self.days_in_month = 15
            self.presenter.toggle_RP_button(self.days_in_month)
            self.label_period_info.config(
                text=f" {self.days_in_month - 14}    -    {self.days_in_month}")
            print("Поменял РП с \"16 до 31\" на \"1 до 15\" ")

    def delete_ranges(self):
        """
        Deletes the selected ranges.

        This method is triggered when the delete button is pressed. It delegates the
        delete action to the presenter, which handles the actual deletion process.
        If the presenter is available, it calls the `sentRdelete` method on the presenter
        and then calls the `success` method to indicate the successful deletion.

        Returns:
            None
        """
        # При нажатии кнопки удаления делегируем вызов Presenter-у
        if self.presenter:
            self.presenter.sentRdelete()
            self.success()

    def setup_ui(self):
        """
        Sets up the user interface for the application.

        This method configures the main window and adds various widgets such as buttons,
        checkboxes, and labels to the interface. The layout is managed using a grid system.

        Widgets:
            - Buttons for each month.
            - Toggle button to change the period.
            - Button to clear all data.
            - Checkboxes for various options.
            - Labels for displaying information and instructions.

        Grid Layout:
            - The buttons are arranged in a grid with a specified number of columns.
            - The columns and rows are configured to distribute space evenly.

        Attributes:
            self.root (tk.Tk): The main window of the application.
            self.scale_factor (float): Scaling factor for adjusting widget sizes.
            self.infoVariables (object): An object containing various information variables.
            self.days_in_month (int): Number of days in the current month.

        Methods:
            on_button_click(month): Handles button click events for month buttons.
            toggle_days(): Toggles the display of days.
            delete_ranges(): Deletes all data ranges.
        """
        
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
            text=self.infoVariables.change,
            font=("Roboto", int(30 * self.scale_factor)),
            bg="white", fg="black", padx=btn_width//2,
            command=self.toggle_days
        )
        self.toggle_button.grid(row=6, column=1, pady=int(
            30 * self.scale_factor), columnspan=3)

        # Кнопка удалить все?
        self.delete_button = tk.Button(
            self.root,
            text=" 🗑️ ? ",
            font=("Roboto", int(20 * self.scale_factor)),
            bg="white", fg="black",
            command=self.delete_ranges
        )
        self.delete_button.grid(
            row=7, column=3, pady=int(30 * self.scale_factor))

        # язык
        self.language_button = tk.Button(
            self.root,
            text="LANG 🌐 / ЯЗЫК 🌐",
            font=("Roboto", int(20 * self.scale_factor)),
            bg="white", fg="black",
            command=self.toggle_language
        )
        self.language_button.grid(row=9, column=3, pady=int(30 * self.scale_factor))

        #CHECK BOXES

        # Переключатель смены за весь РП
        self.t_wages_whole_month_check = tk.Checkbutton(
            self.root,
            text=self.infoVariables.allshifts,
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
            text=self.infoVariables.infoAboutShiftEveryday,
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
            text=f"{self.days_in_month - 15}    -    {self.days_in_month}",
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
            row=8, column=0, pady=int(20 * self.scale_factor))

        # Надпись инфа про приходную функцию
        self.label_income_info = tk.Label(
            self.root,
            text=self.infoVariables.infoaboutIncomeFunc,
            font=("Roboto", int(15 * self.scale_factor), "bold"),
            bg="black", fg="white"
        )
        self.label_income_info.grid(
            row=8, column=2, pady=int(20 * self.scale_factor))

        # Надпись версии
        self.label_footer_info = tk.Label(
            self.root,
            text="i'm just\nplaying my part\nver 0.2.0",
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
            row=8, column=1, pady=int(18 * self.scale_factor))

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


    def toggle_language(self):
        self.infoVariables.switch_language()
        self.update_ui_texts()

    def update_ui_texts(self):
        self.label_instructions.config(text=self.infoVariables.infoAboutPeriodsAndbuttons)
        self.labelDeleteInfo.config(text=self.infoVariables.infoAboutDeleteButton)
        self.label_wages_info.config(text=self.infoVariables.infoaboutWagesFunc)
        self.label_income_info.config(text=self.infoVariables.infoaboutIncomeFunc)
        self.label_daily_info.config(text=self.infoVariables.infoAboutShiftEverydayFunc)
        self.t_set_up_shifts_for_all_days_check.config(text=self.infoVariables.infoAboutShiftEveryday)
        self.t_income_from_shops_check.config(text=self.infoVariables.income_from_shopsINFO)
        self.t_wages_whole_month_check.config(text=self.infoVariables.allshifts)
        self.toggle_button.config(text=self.infoVariables.change)
        for i, month in enumerate(self.infoVariables.months):
            self.root.grid_slaves(row=i // 4, column=i % 4)[0].config(text=month)

    def run(self):
        self.root.mainloop()
