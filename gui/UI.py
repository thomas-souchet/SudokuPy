import customtkinter as ctk
from core.sudoku import Sudoku

# -------------------
# HEADER
# -------------------


class Header(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(
            master,
            corner_radius=0,
            fg_color='#2cc985'
        )
        self.grid_columnconfigure(0, weight=1)

        self.logo_label = ctk.CTkLabel(
            self,
            text="SudokuPy",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#ffffff"
        )
        self.logo_label.grid(row=0, column=0, pady=24)

# -------------------
# SUDOKU GRID
# -------------------


class SudokuGrid(ctk.CTkFrame):
    def __init__(self, master, sudoku_size, frame_size):
        self.n = sudoku_size
        self.size = frame_size
        self.__entries = []

        super().__init__(
            master,
            width=self.size,
            height=self.size,
            corner_radius=0,
            fg_color='transparent',
            border_width=2,
            border_color='#000000'
        )

        self.__build_sub_frames()

    def __calc_pad(self, a, b):
        x, y = (0, 0), (0, 0)
        if a == 0:
            x = (1, 0)
        elif a == self.n - 1:
            x = (0, 1)
        if b == 0:
            y = (1, 0)
        elif b == self.n - 1:
            y = (0, 1)
        return x, y

    def __build_sub_frames(self):
        for i in range(self.n):
            for j in range(self.n):
                pad = self.__calc_pad(i, j)
                self.sub_frame = ctk.CTkFrame(
                    self,
                    width=(self.size/self.n),
                    height=(self.size/self.n),
                    corner_radius=0,
                    fg_color='transparent',
                    border_width=2,
                    border_color='#000000'
                )
                self.sub_frame.grid(row=i, column=j, padx=pad[1], pady=pad[0])
                self.__build_entries(self.sub_frame, j*self.n, i*self.n)

    def __build_entries(self, sub_frame, x_inc, y_inc):
        for i in range(self.n):
            for j in range(self.n):
                pad = self.__calc_pad(i, j)
                self.entry = ctk.CTkEntry(
                    sub_frame,
                    width=(self.size / (self.n ** 2)),
                    height=(self.size / (self.n ** 2)),
                    corner_radius=0, font=('Arial', 96/self.n),
                    border_width=1,
                    justify='center'
                )
                self.entry.configure(
                    validate='key',
                    validatecommand=(self.master.register(self.__sudoku_character_validation), "%P")
                )
                self.entry.grid(row=i, column=j, padx=pad[1], pady=pad[0], sticky="nsew")
                self.__entries.append((j+x_inc, i+y_inc, self.entry))

    def __sudoku_character_validation(self, text):
        if self.n**2 > 9:
            raise ValueError("Unsupported size for sudoku_character_validation")
        valid_characters = ['']
        for i in range(1, self.n**2 + 1):
            valid_characters.append(str(i))
        if len(text) > 1:
            return False
        return text in valid_characters

    def get_grid(self):
        grid_value = Sudoku(self.n)
        for e in self.__entries:
            v = e[2].get()
            grid_value.add((e[0], e[1], int(v) if v != '' else -1))
        return grid_value.get()

    def set_grid(self, grid):
        if type(grid) is not Sudoku:
            raise TypeError('grid must be of type Sudoku')
        if grid.size != self.n**2:
            raise ValueError('incompatible size of grid')
        self.clear_grid()
        for e in self.__entries:
            e[2].insert(0, grid.get_by_coordinates(e[0], e[1]))

    def clear_grid(self):
        for e in self.__entries:
            e[2].delete(0)

# -------------------
# SIDEBAR
# -------------------


class Sidebar(ctk.CTkFrame):
    SPACING = 24

    def __init__(self, master, clear_command, change_grid_command, solve_command):
        self.clear_command = clear_command
        self.change_grid_command = change_grid_command
        self.solve_command = solve_command
        self.font = ctk.CTkFont(family='Arial', size=14, weight="bold")

        super().__init__(
            master,
            width=80,
            corner_radius=0,
            fg_color="#ffffff"
        )
        self.grid_columnconfigure(0, weight=1)

        # size choice
        self.size_options = ctk.CTkSegmentedButton(
            self,
            values=["3x3", "2x2"],
            fg_color="#ffffff",
            unselected_color="#9cb0a4",
            border_width=0,
            command=self.change_grid_command,
        )
        self.size_options.set("3x3")
        self.size_options.grid(row=0, column=0, padx=32, pady=(32, 0), sticky="ew")

        # clear btn
        self.clear_btn = ctk.CTkButton(
            self,
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
        self.resolve_button = ctk.CTkButton(
            self,
            text="Solve Sudoku",
            font=self.font,
            border_spacing=10,
            command=self.solve_command
        )
        self.resolve_button.grid(row=2, column=0, padx=32, pady=(self.SPACING, 8), sticky="ew")

        self.time_lbl = ctk.CTkLabel(self, text="Solved in 0s")
        self.time_lbl.grid(row=3, column=0, sticky="s")

    def update_clear_command(self, command):
        self.clear_command = command
        self.clear_btn.configure(command=self.clear_command)

    def update_time(self, new_time):
        self.time_lbl.configure(text="Solved in " + str(new_time) + "s")
