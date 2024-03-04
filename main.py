import customtkinter

customtkinter.set_appearance_mode("system")
customtkinter.set_default_color_theme("green")


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("SudokuPy")
        self.geometry(f"{1100}x{580}")

        # configure grid layout (2x2)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=3)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=3)

        # create header frame
        self.header_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color=('#2cc985', '#2cc985'))
        self.header_frame.grid(row=0, column=0, columnspan=2, sticky="nsew")
        self.logo_label = customtkinter.CTkLabel(self.header_frame, text="SudokuPy",
                                                 font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.pack(pady=24, fill="both", expand=True)

        # create sidebar frame
        self.sidebar_frame = customtkinter.CTkFrame(self, width=100, corner_radius=0)
        self.sidebar_frame.grid(row=1, column=0, sticky="nsew")
        # size choice
        self.size_frame = customtkinter.CTkFrame(self.sidebar_frame)
        self.size_frame.pack(pady=16)
        self.size_lbl = customtkinter.CTkLabel(self.size_frame, text="Size : ")
        self.size_lbl.pack()
        self.size_entry = customtkinter.CTkOptionMenu(self.size_frame, values=["size", "1x1", "2x2", "3x3", "4x4", "5x5"])
        self.size_entry.pack()
        # clear btn
        self.clear_btn = customtkinter.CTkButton(self.sidebar_frame, text="Clear", font=("Arial", 14, "bold"),)
        self.clear_btn.pack(padx=32, pady=16, fill="x")
        # resolve btn
        self.resolve_button = customtkinter.CTkButton(self.sidebar_frame, text="Resolve", font=("Arial", 14, "bold"))
        self.resolve_button.pack(padx=32, pady=16, fill="x")
        # solving time
        self.time_lbl = customtkinter.CTkLabel(self.sidebar_frame, text="Time : 32.6s")
        self.time_lbl.pack(pady=16)

        self.buildGrid(3)

    def buildGrid(self, size):
        fs = 400
        sudoku_frame = customtkinter.CTkFrame(self, width=fs, height=fs, corner_radius=0, fg_color='transparent')
        sudoku_frame.grid(row=1, column=1, sticky="nsew")

        for i in range(size):
            for j in range(size):
                sub_frame = customtkinter.CTkFrame(sudoku_frame, width=200, height=200, corner_radius=0)
                sub_frame.grid(row=i, column=j, padx=5, pady=5)
                self.build_sub_grid(sub_frame, size)

    def build_sub_grid(self, sf, size):
        for i in range(size):
            for j in range(size):
                entry = customtkinter.CTkEntry(sf, width=20, height=32, corner_radius=0, font=('Arial', 32), border_width=0)
                entry.grid(row=i, column=j, sticky="nsew")


if __name__ == "__main__":
    app = App()
    app.mainloop()
