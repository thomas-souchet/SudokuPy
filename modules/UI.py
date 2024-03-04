import customtkinter as ctk


def one_character_validation(text):
    valid_characters = ['', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    if len(text) > 1:
        return False
    return text in valid_characters


class Header(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.main = ctk.CTkFrame(master, corner_radius=0, fg_color='#2cc985')
        self.main.grid_columnconfigure(0, weight=1)
        self.logo_label = ctk.CTkLabel(self.main, text="SudokuPy", font=ctk.CTkFont(size=20, weight="bold"), text_color="#ffffff")
        self.logo_label.grid(row=0, column=0, pady=24)


class SudokuGrid(ctk.CTkFrame):
    def __init__(self, master, sudoku_size, frame_size):
        super().__init__(master)
        self.n = sudoku_size
        self.size = frame_size
        self.entries = []

        self.main = ctk.CTkFrame(master, width=self.size, height=self.size, corner_radius=0, fg_color='transparent', border_width=2, border_color='#000000')
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
                self.sub_frame = ctk.CTkFrame(self.main, width=(self.size/self.n), height=(self.size/self.n), corner_radius=0, fg_color='transparent', border_width=2, border_color='#000000')
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
                        self.entry = ctk.CTkEntry(self.sub_frame, width=(self.size/(self.n**2)), height=(self.size/(self.n**2)), corner_radius=0, font=('Arial', 32), border_width=1, justify='center')
                        self.entry.configure(validate='key', validatecommand=(self.master.register(one_character_validation), "%P"))
                        self.entry.grid(row=k, column=l, padx=xx, pady=yy, sticky="nsew")
                        self.entries.append(self.entry)

    def get_grid(self):
        grid_value = []
        for e in self.entries:
            grid_value.append(e.get())
        return grid_value

    def set_grid(self, grid):
        raise NotImplementedError

    def clear_grid(self):
        for e in self.entries:
            e.delete(0)


class Sidebar(ctk.CTkFrame):
    SPACING = 24

    def __init__(self, master, clear_command):
        super().__init__(master)
        self.clear_command = clear_command
        self.font = ctk.CTkFont(family='Arial', size=14, weight="bold")

        self.main = ctk.CTkFrame(master, width=80, corner_radius=0, fg_color="#ffffff")
        self.main.grid_columnconfigure(0, weight=1)

        # size choice
        self.size_options = ctk.CTkSegmentedButton(
            self.main,
            values=["3x3", "2x2"],
            fg_color="#ffffff",
            unselected_color="#9cb0a4",
            border_width=0,
        )
        self.size_options.grid(row=0, column=0, padx=32, pady=(32, 0), sticky="ew")

        # clear btn
        self.clear_btn = ctk.CTkButton(
            self.main,
            text="Clear grid",
            font=self.font,
            fg_color="#ffffff",
            text_color="#2cc985",
            border_spacing=10,
            border_color="#2cc985",
            border_width=2,
            hover_color="#f0f0f0",
            command=self.clear_command
        )
        self.clear_btn.grid(row=1, column=0, padx=32, pady=(self.SPACING, 0), sticky="ew")

        # solve
        self.resolve_button = ctk.CTkButton(self.main, text="Solve Sudoku", font=self.font, border_spacing=10)
        self.resolve_button.grid(row=2, column=0, padx=32, pady=(self.SPACING, 8), sticky="ew")

        self.time_lbl = ctk.CTkLabel(self.main, text="Solved in 32.6s")
        self.time_lbl.grid(row=3, column=0, sticky="s")
