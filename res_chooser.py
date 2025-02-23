import tkinter as tk

class ResChooser:
    def __init__(self, parent=None):
        self.res_of_main_window = "1680x850"  # Значение по умолчанию
        self.resolutions = {"small": "1450x720", "medium": "1560x900", "big": "1680x1050"}
        
        self.root = tk.Toplevel(parent) if parent else tk.Tk()
        self.root.resizable(0, 0)
        self.root.title("Resolution Choice")
        self.root.attributes('-topmost', 1)
        
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        position_x = (screen_width - 300) // 2
        position_y = (screen_height - 300) // 2
        self.root.geometry(f"200x220+{position_x}+{position_y}")
        
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        
        self.label = tk.Label(self.root, text="Choose preferred resolution:", font=("Arial", 12, "bold"))
        self.label.grid(row=0, column=0)
        
        self.listbox = tk.Listbox(self.root, selectmode="single", height=len(self.resolutions), width=20)
        for res in self.resolutions.keys():
            self.listbox.insert("end", res)
        self.listbox.grid(row=1, column=0)
        
        self.btn_choose = tk.Button(self.root, text="Выбрать", height=2, width=10, font=("Arial", 12), command=self.choose_resolution)
        self.btn_choose.grid(row=2, column=0)
    
    def choose_resolution(self):
        selected_index = self.listbox.curselection()
        if selected_index:
            selected_key = self.listbox.get(selected_index[0])
            self.res_of_main_window = self.resolutions[selected_key]
        self.root.destroy()
    
    def get_resolution(self):
        self.root.mainloop()
        return self.res_of_main_window
