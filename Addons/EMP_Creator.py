import tkinter as tk

class EMP_list_creator:
    """Диалоговое окно задания списка работников"""

    def __init__(self, parent=None):
        """Создает окно записания списка работников"""

        self.root = tk.Toplevel(parent) if parent else tk.Tk()
        self.root.resizable(False, False)
        self.root.title("Employee Creator")
        self.root.attributes('-topmost', 1)
        self.employees_list = []
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        position_x = (screen_width - 300) // 2
        position_y = (screen_height - 300) // 2

        self.root.geometry(f'450x540+{position_x}+{position_y}')

        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

        self.label = tk.Label(
            self.root, text="Enter employees (one per line):\nЗапишите сотрудников (Каждый сотрудник на своей линии)\nВ случае, если менять список сотрудников не нужно,\n то просто нажмите на кнопку ниже,\n при этом не вводя имена сотрудников.", font=("Arial", 11, "bold"))
        self.label.grid(row=0, column=0)


        self.textbox = tk.Text(self.root,bg='white', fg='black',height=20,width=40 ,font=("Arial", 9, "bold"))
        self.textbox.grid(row=2, column=0)

        self.btn_choose = tk.Button(
            self.root, text="Отправить", height=2, width=10, font=("Arial", 12), command=self.make_list_of_emp
        )
        self.btn_choose.grid(row=4, column=0)

    def make_list_of_emp(self):
        """Создание списка работников в таблицу"""
        string_input = self.textbox.get("1.0", 'end-1c')
        self.employees_list = string_input.split("\n")  # Разделяем по строкам
        self.employees_list = [emp.strip() for emp in self.employees_list if emp.strip()]
        self.root.destroy()

    def get_list(self):
        """Запуск окна и возврат выбранного списка."""
        self.root.mainloop()
        return self.employees_list
