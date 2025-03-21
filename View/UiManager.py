
import tkinter as tk
from tkinter import BooleanVar


class UiManager:
    def __init__(self, config, scale_factor=0.8):
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
        self.light_theme = {
            'bg': 'white',
            'fg': 'black',
            'button_bg': 'lightgrey',
            'button_fg': 'black',
            'checkbox_bg': 'lightgrey',
            'checkbox_fg': 'black'
        }
        self.dark_theme = {
            'bg': 'black',
            'fg': 'white',
            'button_bg': 'white',
            'button_fg': 'black',
            'checkbox_bg':'white',
            'checkbox_fg':'orange'
        }
        self.current_theme = 'dark'
        self.root = config['root']
        self.QOL = config['QOL']
        self.infoVariables = config['infoVariables']
        self.scale_factor = scale_factor
        self.days_in_month = 31

        self.t_wages_whole_month_var1 = BooleanVar()
        self.t_income_from_shops_var2 = BooleanVar()
        self.t_set_up_shifts_for_all_days_var3 = BooleanVar()

        self.conrtoller = None

        self.setup_ui()

    def toggle_theme(self):
        if self.current_theme == 'dark':
            self.apply_theme(self.light_theme)
            self.current_theme = 'light'
        else:
            self.apply_theme(self.dark_theme)
            self.current_theme = 'dark'

    def apply_theme(self, theme):
        self.root.configure(bg=theme['bg'])
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Button):
                widget.configure(bg=theme['button_bg'], fg=theme['button_fg'])
            elif isinstance(widget, tk.Checkbutton):
                widget.configure(bg=theme['checkbox_bg'], fg=theme['checkbox_fg'])
            else:
                widget.configure(bg=theme['bg'], fg=theme['fg'])

    def nothing_picked(self):
        self.label_error_info.config(
            text="Выберите хотя бы \nодну функцию❎", font=("Arial", 16, "bold"))
        self.root.after(3000, lambda: self.label_error_info.config(text=""))

    def success(self):
        self.label_success_info.config(
            text="Успех!☑", font=("Arial", 24, "bold"))
        self.root.after(3000, lambda: self.label_success_info.config(text=""))

    def show_error(self, message):
        print(f"Error: {message}")

    def on_button_click(self, month):
        checkboxes = {
            'wages': self.t_wages_whole_month_var1.get(),
            'income': self.t_income_from_shops_var2.get(),
            'shifts': self.t_set_up_shifts_for_all_days_var3.get()
        }
        if self.controller:
            self.controller.send_request(month, checkboxes, self.days_in_month)
        else:
            print("controller is not set!")
            print(self.controller)

    def toggle_days(self):
        if self.t_wages_whole_month_var1.get() or self.t_set_up_shifts_for_all_days_var3.get():
            self.label_error_info.config(text=" ")
        if self.days_in_month == 15:
            self.days_in_month = 31
            self.controller.toggle_RP_button(self.days_in_month)
            self.label_period_info.config(
                text=f"{self.days_in_month - 15}    -    {self.days_in_month}")
            print("Поменял РП с \"1 до 15\" на \"16 до 31\"")
        else:
            self.days_in_month = 15
            self.controller.toggle_RP_button(self.days_in_month)
            self.label_period_info.config(
                text=f" {self.days_in_month - 14}    -    {self.days_in_month}")
            print("Поменял РП с \"16 до 31\" на \"1 до 15\" ")

    def toggle_Inc_key(self):
        self.controller.toggleINCKey()
    def delete_ranges(self):
        if self.controller:
            self.controller.sentRdelete()
            self.success()

    def setup_ui(self):
        self.root.configure(bg="black")
        btn_width = int(18 * self.scale_factor)
        font_size = int(20 * self.scale_factor)
        padx = int(8 * self.scale_factor)
        pady = int(8 * self.scale_factor)

        num_columns = 4

        for i, month in enumerate(self.infoVariables.months):
            button = tk.Button(self.root, text=month, height=2, width=btn_width,
                               command=lambda m=month: self.on_button_click(m),
                               bg="white", fg="black",
                               font=("Arial", font_size, "bold"), relief="sunken")
            row = i // num_columns
            column = i % num_columns
            button.grid(row=row, column=column, padx=padx,
                        pady=pady, sticky="nsew")

        for i in range(num_columns):
            self.root.grid_columnconfigure(i, weight=1, uniform="equal")
        for i in range((len(self.infoVariables.months) + num_columns - 1) // num_columns):
            self.root.grid_rowconfigure(i, weight=1, uniform="equal")

        self.toggle_button = tk.Button(
            self.root,
            text=self.infoVariables.change,
            font=("Roboto", int(24 * self.scale_factor)),
            bg="white", fg="black", padx=btn_width//2,
            command=self.toggle_days
        )
        
        self.toggle_button.grid(row=6, column=1, pady=int(
            24 * self.scale_factor), columnspan=3)
        
        self.toggle_INCbutton = tk.Button(
            self.root,
            text="Сменить ключ\nРасчета прихода",
            font=("Roboto", int(20 * self.scale_factor)),
            bg="white", fg="black", padx=btn_width//2,
            command=self.toggle_Inc_key
        )
        self.toggle_INCbutton.grid(row=9, column=2, pady=int(
            24 * self.scale_factor))

        self.delete_button = tk.Button(
            self.root,
            text=" 🗑️ ? ",
            font=("Roboto", int(16 * self.scale_factor)),
            bg="white", fg="black",
            command=self.delete_ranges
        )
        self.delete_button.grid(
            row=7, column=3, pady=int(24 * self.scale_factor))

        self.language_button = tk.Button(
            self.root,
            text="LANG 🌐 / ЯЗЫК 🌐",
            font=("Roboto", int(16 * self.scale_factor)),
            bg="white", fg="black",
            command=self.toggle_language
        )
        self.language_button.grid(row=9, column=3, pady=int(24 * self.scale_factor))

        self.theme_button = tk.Button(
            self.root,
            text="Theme color\nЦвет темы",
            font=("Roboto", int(16 * self.scale_factor)),
            bg="white", fg="black",
            command=self.toggle_theme
        )
        self.theme_button.grid(row=10, column=3, pady=int(24 * self.scale_factor))

        self.t_wages_whole_month_check = tk.Checkbutton(
            self.root,
            text=self.infoVariables.allshifts,
            variable=self.t_wages_whole_month_var1,
            bg="white", fg="black",
            font=("Roboto", int(15 * self.scale_factor), "bold")
        )
        self.t_wages_whole_month_check.grid(
            row=7, column=0, pady=pady, padx=padx)

        self.t_income_from_shops_check = tk.Checkbutton(
            self.root,
            text=self.infoVariables.income_from_shopsINFO,
            variable=self.t_income_from_shops_var2,
            bg="white", fg="black",
            font=("Roboto", int(15 * self.scale_factor), "bold")
        )
        self.t_income_from_shops_check.grid(
            row=7, column=2, pady=pady, padx=padx)

        self.t_set_up_shifts_for_all_days_check = tk.Checkbutton(
            self.root,
            text=self.infoVariables.infoAboutShiftEveryday,
            variable=self.t_set_up_shifts_for_all_days_var3,
            bg="white", fg="black",
            font=("Roboto", int(15 * self.scale_factor), "bold")
        )
        self.t_set_up_shifts_for_all_days_check.grid(
            row=7, column=1, pady=pady, padx=padx)

        self.label_period_info = tk.Label(
            self.root,
            text=f"{self.days_in_month - 15}    -    {self.days_in_month}",
            font=("Roboto", int(20 * self.scale_factor), "bold"),
            bg="black", fg="white"
        )
        self.label_period_info.grid(
            row=6, column=0, pady=pady, padx=padx, columnspan=3)

        self.label_instructions = tk.Label(
            self.root,
            text=self.infoVariables.infoAboutPeriodsAndbuttons,
            font=("Roboto", int(12 * self.scale_factor), "bold"),
            bg="black", fg="white"
        )
        self.label_instructions.grid(row=3, column=1, pady=pady, columnspan=2)

        self.labelDeleteInfo = tk.Label(
            self.root,
            text=self.infoVariables.infoAboutDeleteButton,
            font=("Roboto", int(15 * self.scale_factor), "bold"),
            bg="black", fg="white"
        )
        self.labelDeleteInfo.grid(row=8, column=3)

        self.label_wages_info = tk.Label(
            self.root,
            text=self.infoVariables.infoaboutWagesFunc,
            font=("Roboto", int(12 * self.scale_factor), "bold"),
            bg="black", fg="white"
        )
        self.label_wages_info.grid(
            row=8, column=0, pady=int(16 * self.scale_factor))

        self.label_income_info = tk.Label(
            self.root,
            text=self.infoVariables.infoaboutIncomeFunc,
            font=("Roboto", int(12 * self.scale_factor), "bold"),
            bg="black", fg="white"
        )
        self.label_income_info.grid(
            row=8, column=2, pady=int(16 * self.scale_factor))

        self.label_footer_info = tk.Label(
            self.root,
            text="и мне не надо слов\nя все поняла\nver 0.2.5",
            bg="black", fg="white",
            font=("Arial", int(12 * self.scale_factor), "bold")
        )
        self.label_footer_info.grid(row=10, column=0, columnspan=4)

        self.label_daily_info = tk.Label(
            self.root,
            text=self.infoVariables.infoAboutShiftEverydayFunc,
            font=("Roboto", int(12 * self.scale_factor), "bold"),
            bg="black", fg="white"
        )
        self.label_daily_info.grid(
            row=8, column=1, pady=int(16 * self.scale_factor))

        self.label_error_info = tk.Label(
            self.root,
            text="",
            bg="black", fg="red",
            font=("Arial", int(12 * self.scale_factor))
        )
        self.label_error_info.grid(row=6, column=0)

        self.label_success_info = tk.Label(
            self.root,
            text="",
            bg="black", fg="lightgreen",
            font=("Arial", int(12 * self.scale_factor))
        )
        self.label_success_info.grid(row=6, column=3)

        self.apply_theme(self.dark_theme)

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
