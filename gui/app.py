from gui.UI import *
import math
import time


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.error_win = None

        # configure window
        self.title("SudokuPy")
        self.geometry("1100x580")

        # configure grid layout (2x2)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=3)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=3)

        self.header = Header(self)
        self.header.grid(row=0, column=0, columnspan=2, sticky="nsew")

        self.sudoku_grid = SudokuGrid(self, 3, 400)
        self.sudoku_grid.grid(row=1, column=1)

        self.sidebar = Sidebar(self, self.sudoku_grid.clear_grid, self.change_grid_size, self.solve_grid)
        self.sidebar.grid(row=1, column=0, sticky="nsew")

    def change_grid_size(self, value):
        self.sudoku_grid.destroy()
        self.sudoku_grid = SudokuGrid(self, int(value[0]), 400)
        self.sudoku_grid.grid(row=1, column=1)
        self.sidebar.update_clear_command(self.sudoku_grid.clear_grid)

    def set_grid_test(self):
        try:
            g = Sudoku(2)
            for i in range(4):
                for j in range(4):
                    g.add((i, j, i + j))
            self.sudoku_grid.set_grid(g)
            print(self.sudoku_grid.get_grid())
        except Exception as e:
            self.error_win = ErrorWindow(message=repr(e))

    def solve_grid(self):
        print(">>> Start solving sudoku...")
        start = time.time()
        s = self.sudoku_grid.get_grid()
        s.solve()
        self.sudoku_grid.set_grid(s)
        end = time.time()
        self.sidebar.update_time(round(end - start, 2))


class ErrorWindow(ctk.CTkToplevel):
    def __init__(self, message=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("SudokuPy - Error")
        self.geometry("300x100")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.attributes("-topmost", True)

        self.label = ctk.CTkLabel(
            self,
            text="An error has occurred",
            font=ctk.CTkFont(family='Arial', size=14, weight="bold"),
            text_color="red"
        )
        self.label.grid(row=0, column=0)

        if message is not None:
            self.message_label = ctk.CTkLabel(
                self,
                text=message,
                font=ctk.CTkFont(family='Arial', size=10),
                text_color="#C4C4C4"
            )
            self.message_label.grid(row=1, column=0)
