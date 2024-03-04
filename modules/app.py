from modules.UI import *


class App(ctk.CTk):
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

        self.header = Header(self)
        self.header.main.grid(row=0, column=0, columnspan=2, sticky="nsew")

        self.sudoku_grid = SudokuGrid(self, 3, 400)
        self.sudoku_grid.main.grid(row=1, column=1)

        self.sidebar = Sidebar(self, self.sudoku_grid.clear_grid)
        self.sidebar.main.grid(row=1, column=0, sticky="nsew")
