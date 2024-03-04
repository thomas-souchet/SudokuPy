import customtkinter

customtkinter.set_appearance_mode("system")
customtkinter.set_default_color_theme("green")


class SudokuGrid(customtkinter.CTkFrame):
    def __init__(self, master, sudoku_size, frame_size):
        super().__init__(master)
        self.n = sudoku_size
        self.size = frame_size

        self.main_frame = customtkinter.CTkFrame(master, width=self.size, height=self.size, corner_radius=0, fg_color='transparent', border_width=2, border_color='#000000')
        # Create sub frames
        for i in range(self.n):
            for j in range(self.n):
                x = (0, 0)
                y = (0, 0)
                if j == 0:
                    x = (1, 0)
                elif j == self.n-1:
                    x = (0, 1)
                if i == 0:
                    y = (1, 0)
                elif i == self.n-1:
                    y = (0, 1)
                self.sub_frame = customtkinter.CTkFrame(self.main_frame, width=(self.size/self.n), height=(self.size/self.n), corner_radius=0, fg_color='transparent', border_width=2, border_color='#000000')
                self.sub_frame.grid(row=i, column=j, padx=x, pady=y)
                # Build sub grid
                for k in range(self.n):
                    for l in range(self.n):
                        xx = (0, 0)
                        yy = (0, 0)
                        if l == 0:
                            xx = (1, 0)
                        elif l == self.n - 1:
                            xx = (0, 1)
                        if k == 0:
                            yy = (1, 0)
                        elif k == self.n - 1:
                            yy = (0, 1)
                        self.entry = customtkinter.CTkEntry(self.sub_frame, width=(self.size/(self.n**2)), height=(self.size/(self.n**2)), corner_radius=0, font=('Arial', 32), border_width=1, justify='center')
                        self.entry.configure(validate='key', validatecommand=(self.master.register(self.one_character_validation), "%P"))
                        self.entry.grid(row=k, column=l, padx=xx, pady=yy, sticky="nsew")

    def one_character_validation(self, text):
        return len(text) <= 1


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("SudokuPy")
        self.geometry("1100x580")

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
        self.size_entry = customtkinter.CTkOptionMenu(self.size_frame, values=["3x3", "2x2", "4x4"])
        self.size_entry.pack()
        # clear btn
        self.clear_btn = customtkinter.CTkButton(self.sidebar_frame, text="Clear", font=("Arial", 14, "bold"), fg_color="#ffffff", text_color="#000000", hover_color="#c4c4c4")
        self.clear_btn.pack(padx=32, pady=16, fill="x")
        # resolve btn
        self.resolve_button = customtkinter.CTkButton(self.sidebar_frame, text="Resolve", font=("Arial", 14, "bold"))
        self.resolve_button.pack(padx=32, pady=16, fill="x")
        # solving time
        self.time_lbl = customtkinter.CTkLabel(self.sidebar_frame, text="Solved in : 32.6s")
        self.time_lbl.pack(pady=16)

        self.sudoku_grid = SudokuGrid(self, 3, 400)
        self.sudoku_grid.main_frame.grid(row=1, column=1)


if __name__ == "__main__":
    app = App()
    app.mainloop()
