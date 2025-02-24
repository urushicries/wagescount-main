import tkinter as tk
from tkinter import BooleanVar

class UiManager:
    """
    A class responsible for managing the graphical user interface (GUI) in the application.
    """
    def __init__(self, root, client, QOL, Parser, Updater, infoVariables, service, sheetWAGES,
                 shtKOM_id, shtPIK_id, shtJUN_id, shtLM_id, scale_factor=1):
        self.root = root
        self.client = client
        self.QOL = QOL
        self.Parser = Parser
        self.Updater = Updater
        self.infoVariables = infoVariables
        self.service = service
        self.sheetWAGES = sheetWAGES
        self.shtKOM_id = shtKOM_id
        self.shtPIK_id = shtPIK_id
        self.shtJUN_id = shtJUN_id
        self.shtLM_id = shtLM_id
        self.scale_factor = scale_factor
        
        self.days_in_month = 31  # Default period value
        
        # Initialize Tkinter variables
        self.t_wages_whole_month_var1 = BooleanVar()
        self.t_income_from_shops_var2 = BooleanVar()
        self.t_set_up_shifts_for_all_days_var3 = BooleanVar()
        
        # Setup the UI
        self.setup_ui()
        self.run()
    
    def delete_ranges(self):
        self.QOL.clear_wgslist_ranges(self.service, "14FtsvGplg1jKXJvLJCueI8iEEnjJUtjk17NuPqeCnqo")
        self.success()
    
    def toggle_days(self):
        # Clear error if any of the checkboxes are True
        if (self.t_wages_whole_month_var1.get() or 
            self.t_set_up_shifts_for_all_days_var3.get()):
            self.label_error_info.config(text=" ")
        
        if self.days_in_month == 15:
            self.days_in_month = 31
            self.label_period_info.config(text=f"Count from {self.days_in_month - 15}    to:    {self.days_in_month}")
            print("Поменял РП с \"1 до 15\" на \" 16 до 31\"")
            self.toggle_RP_button(self.days_in_month)
        else:
            self.days_in_month = 15
            self.label_period_info.config(text=f"Count from {self.days_in_month - 14}    to:    {self.days_in_month}")
            print("Поменял РП с \" 16 до 31\" на \"1 до 15\" ")
            self.toggle_RP_button(self.days_in_month)
    
    def nothing_picked(self):
        self.label_error_info.config(text="Выберите хотя бы \nодну функцию❎", font=("Arial", 30, "bold"))
        self.root.after(3000, lambda: self.label_error_info.config(text=""))
    
    def success(self):
        self.label_success_info.config(text="Успех!☑", font=("Arial", 30, "bold"))
        self.root.after(3000, lambda: self.label_success_info.config(text=""))
    
    def toggle_RP_button(self, days_in_month):
        self.QOL.toggle_cell_value(self.sheetWAGES, days_in_month)
    
    def on_button_click(self, month):
        months_data = {
            "Январь": {"sheet_suffix": "Январь25", "days": self.days_in_month},
            "Февраль": {"sheet_suffix": "Февраль25", "days": self.days_in_month},
            "Март": {"sheet_suffix": "Март25", "days": self.days_in_month},
            "Апрель": {"sheet_suffix": "Апрель25", "days": self.days_in_month},
            "Май": {"sheet_suffix": "Май25", "days": self.days_in_month},
            "Июнь": {"sheet_suffix": "Июнь25", "days": self.days_in_month},
            "Июль": {"sheet_suffix": "Июль25", "days": self.days_in_month},
            "Август": {"sheet_suffix": "Август25", "days": self.days_in_month},
            "Сентябрь": {"sheet_suffix": "Сентябрь25", "days": self.days_in_month},
            "Октябрь": {"sheet_suffix": "Октябрь25", "days": self.days_in_month},
            "Ноябрь": {"sheet_suffix": "Ноябрь25", "days": self.days_in_month},
            "Декабрь": {"sheet_suffix": "Декабрь25", "days": self.days_in_month}
        }
        
        month_data = months_data.get(month)
        if not month_data:
            print(f"Unknown month: {month}")
            return
        
        try:
            if (not self.t_wages_whole_month_var1.get() and 
                not self.t_set_up_shifts_for_all_days_var3.get() and 
                not self.t_income_from_shops_var2.get()):
                self.nothing_picked()
            else:
                # Open sheets for the given month
                sheetKOM = self.client.open("Коменда отчет").worksheet(month_data["sheet_suffix"])
                sheetPIK = self.client.open("Пик отчет").worksheet(month_data["sheet_suffix"])
                sheetJUNE = self.client.open("Июнь отчет").worksheet(month_data["sheet_suffix"])
                sheetLM = self.client.open("Лондон отчет").worksheet(month_data["sheet_suffix"])
                
                if self.t_wages_whole_month_var1.get() or self.t_set_up_shifts_for_all_days_var3.get():
                    dataKOM, dataPIK, dataJUNE, dataLM = self.Parser.parseDataAboutShifts(
                        month_data["days"], sheetKOM, sheetPIK, sheetJUNE, sheetLM
                    )
                    emp_shiftLST = self.Parser.parseDataNamesShift(dataKOM, dataPIK, dataJUNE, dataLM)
                    dictEMPSHIFT = self.QOL.makeDictEmpTot(emp_shiftLST)
                
                if self.t_income_from_shops_var2.get():
                    incomeKOM, incomePIK, incomeJUNE, incomeLM = self.Parser.parseINCOMEfromSHEETS(
                        self.client, month_data["sheet_suffix"],
                        self.shtKOM_id, self.shtPIK_id, self.shtJUN_id, self.shtLM_id
                    )
                
                # Process according to selected functions
                if self.t_wages_whole_month_var1.get():
                    if dictEMPSHIFT and emp_shiftLST:
                        self.Updater.update_info_WAGES(dictEMPSHIFT, self.sheetWAGES)
                
                if self.t_set_up_shifts_for_all_days_var3.get():
                    if emp_shiftLST and dictEMPSHIFT:
                        self.Updater.update_info_everyday_TRADEPLACES(month_data["days"], emp_shiftLST, self.sheetWAGES)
                        self.Updater.update_info_everyday(month_data["days"], emp_shiftLST, self.sheetWAGES)
                
                if self.t_income_from_shops_var2.get():
                    if incomeKOM and incomePIK and incomeJUNE and incomeLM:
                        self.Updater.update_table_from_lists(self.sheetWAGES, incomeKOM, incomePIK, incomeJUNE, incomeLM)
                self.success()
        except Exception as e:
            print(f"Error occurred while processing sheets for {month}: {e}")
    
    def setup_ui(self):
        self.root.configure(bg="black")
        btn_width = int(22 * self.scale_factor)
        font_size = int(25 * self.scale_factor)
        padx = int(10 * self.scale_factor)
        pady = int(10 * self.scale_factor)
        
        months = [
            "Январь", "Февраль", "Март", "Апрель", "Май", "Июнь",
            "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"
        ]
        num_columns = 4  # Adjust the number of columns as needed
        
        # Create buttons for each month
        for i, month in enumerate(months):
            button = tk.Button(self.root, text=month, height=2, width=btn_width,
                               command=lambda m=month: self.on_button_click(m),
                               bg="#000000", fg="black",
                               font=("Arial", font_size+12, "bold"), relief="sunken")
            row = i // num_columns
            column = i % num_columns
            button.grid(row=row, column=column, padx=padx, pady=pady, sticky="nsew")
        
        # Allow grid cells to expand equally
        for i in range(num_columns):
            self.root.grid_columnconfigure(i, weight=1, uniform="equal")
        for i in range((len(months) + num_columns - 1) // num_columns):
            self.root.grid_rowconfigure(i, weight=1, uniform="equal")
        
        # Additional Labels and Buttons
        self.label_period_info = tk.Label(
            self.root,
            text=f"Count from {self.days_in_month - 15}    to:    {self.days_in_month}",
            font=("Roboto", int(25 * self.scale_factor), "bold"),
            bg="black", fg="white"
        )
        self.label_period_info.grid(row=6, column=0, pady=pady, padx=padx,columnspan=3)
        
        self.label_instructions = tk.Label(
            self.root,
            text=self.infoVariables.infoAboutPeriodsAndbuttons,
            font=("Roboto", int(15 * self.scale_factor), "bold"),
            bg="black", fg="white"
        )
        self.label_instructions.grid(row=3, column=1, pady=pady, columnspan=2)
        
        self.toggle_button = tk.Button(
            self.root,
            text="Change period?🔄",
            font=("Roboto", int(30 * self.scale_factor)),
            bg="black", fg="black",padx=btn_width//2,
            command=self.toggle_days
        )
        self.toggle_button.grid(row=6, column=1, pady=int(30 * self.scale_factor),columnspan=3)
        
        self.delete_button = tk.Button(
            self.root,
            text="Clear everything up? 🗑️",
            font=("Roboto", int(30 * self.scale_factor)),
            bg="black", fg="black",
            command=self.delete_ranges
        )
        self.delete_button.grid(row=7, column=3, pady=int(30 * self.scale_factor))

        self.labelDeleteInfo = tk.Label(
            self.root,
            text=self.infoVariables.infoAboutDeleteButton,
            font=("Roboto", int(15 * self.scale_factor),"bold"),
            bg="black", fg="white"
        )
        self.labelDeleteInfo.grid(row=8,column=3)

        self.label_wages_info = tk.Label(
            self.root,
            text=self.infoVariables.infoaboutWagesFunc,
            font=("Roboto", int(15 * self.scale_factor), "bold"),
            bg="black", fg="white"
        )
        self.label_wages_info.grid(row=8, column=1, pady=int(20 * self.scale_factor))
        
        self.t_wages_whole_month_check = tk.Checkbutton(
            self.root,
            text="All shifts for period?",
            variable=self.t_wages_whole_month_var1,
            bg="white", fg="black",
            font=("Roboto", int(24 * self.scale_factor), "bold")
        )
        self.t_wages_whole_month_check.grid(row=7, column=0, pady=pady, padx=padx)
        
        self.label_income_info = tk.Label(
            self.root,
            text=self.infoVariables.infoaboutIncomeFunc,
            font=("Roboto", int(15 * self.scale_factor), "bold"),
            bg="black", fg="white"
        )
        self.label_income_info.grid(row=8, column=0, pady=int(20 * self.scale_factor))
        
        self.t_income_from_shops_check = tk.Checkbutton(
            self.root,
            text="Income from arenas?",
            variable=self.t_income_from_shops_var2,
            bg="white", fg="black",
            font=("Roboto", int(24 * self.scale_factor), "bold")
        )
        self.t_income_from_shops_check.grid(row=7, column=2, pady=pady, padx=padx)
        
        self.label_daily_info = tk.Label(
            self.root,
            text=self.infoVariables.infoAboutShiftEverydayFunc,
            font=("Roboto", int(15 * self.scale_factor), "bold"),
            bg="black", fg="white"
        )
        self.label_daily_info.grid(row=8, column=2, pady=int(18 * self.scale_factor))
        
        self.t_set_up_shifts_for_all_days_check = tk.Checkbutton(
            self.root,
            text="Shifts for every day?",
            variable=self.t_set_up_shifts_for_all_days_var3,
            bg="white", fg="black",
            font=("Roboto", int(24 * self.scale_factor), "bold")
        )
        self.t_set_up_shifts_for_all_days_check.grid(row=7, column=1, pady=pady, padx=padx)
        
        self.label_footer_info = tk.Label(
            self.root,
            text="закрываю глаза, а там все еще ты...\nDose, FEDUK\nver 0.0.9",
            bg="black", fg="white",
            font=("Arial", int(14 * self.scale_factor), "bold")
        )
        self.label_footer_info.grid(row=10, column=0,columnspan=4)
        
        self.label_error_info = tk.Label(
            self.root,
            text="",
            bg="black", fg="red",
            font=("Arial", int(15 * self.scale_factor))
        )
        self.label_error_info.grid(row=5, column=0)
        
        self.label_success_info = tk.Label(
            self.root,
            text="",
            bg="black", fg="lightgreen",
            font=("Arial", int(15 * self.scale_factor))
        )
        self.label_success_info.grid(row=5, column=2)
    
    def run(self):
        self.root.mainloop()

