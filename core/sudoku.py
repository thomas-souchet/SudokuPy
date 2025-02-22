from typing import Tuple, Optional

from core.cnf import CNF
from core.dpll import DPLL


class Sudoku:
    """! The Sudoku base class.
    Defines the data structure used to store the Sudoku grid.
    """

    def __init__(self, size: int):
        """! The Sudoku base class initializer.
        @param size  The size of the Sudoku grid.
        @return  An instance of the Sudoku class initialized with the specified size.
        """
        self.n = size
        self.size = size**2
        self.__grid = []

    def add(self, t: Tuple[int, int, int]):
        """! Add a number to the Sudoku grid.
        @param t  A tuple with three numbers, x, y, value.
        """
        if type(t) is not tuple:
            raise TypeError('The element type must be tuple')
        if len(t) != 3:
            raise ValueError('The tuple must have three elements')
        for i in range(len(t)):
            if type(t[i]) is not int:
                raise TypeError('The element must only contains integers')
            if i <= 1 and (t[i] < 0 or t[i] > self.size-1):
                raise ValueError('The first two elements must be between 1 and %d' % (self.size-1))
            if i == 2 and (t[i] > self.size or t[i] <= 0):
                raise ValueError('The third element must be between 1 and %d' % self.size)
        self.__grid.append(t)

    def remove_all(self):
        """! Clear the Sudoku grid.
        """
        self.__grid = []

    def get(self) -> list[Tuple[int, int, int]]:
        """! Get the Sudoku grid.
        @return  The actual Sudoku grid.
        """
        return self.__grid

    def get_by_coordinates(self, x: int, y: int) -> int:
        """! Get the Sudoku grid.
        @param x  The x coordinate.
        @param y  The y coordinate.
        @return  The number at the given coordinates or -2 if the cell is empty.
        """
        if x < 0 or x >= self.size or y < 0 or y >= self.size:
            raise ValueError('Coordinates out of bounds')
        for c in self.__grid:
            if c[0] == x and c[1] == y:
                return c[2]
        return -2

    def __init_list_var(self) -> list[Optional[bool]]:
        """! Initialize the variable list for the CNF. n² variables for each cell
        @return  The variable list for the CNF.
        """
        list_var_grid = []
        if not self.__grid:
            return [None] * self.size**2 * 9
        for i in range(self.size):
            for j in range(self.size):
                for k in range(1, (self.n ** 2) + 1):
                    contraint = self.get_by_coordinates(j, i)
                    if contraint == -2:
                        list_var_grid.append(None)
                    elif contraint == k:
                        list_var_grid.append(True)
                    else:
                        list_var_grid.append(False)
        return list_var_grid

    def __set_grid_from_var(self, list_var_grid: list[Optional[bool]]):
        """! Set the sudoku grid from a CNF variable list."""
        final_grid = []
        if not list_var_grid:
            raise Exception('The variable list is empty')
        for i in range(len(list_var_grid)):
            if list_var_grid[i]:
                x = (i // self.size) % self.size
                y = i // self.n ** 4
                v = (i % self.size)+1
                final_grid.append((x, y, v))
            if list_var_grid[i - 1] is None:
                raise Exception("Variable list is incomplete")
        self.__grid = final_grid

    @staticmethod
    def clause_gen(cl: list[int]) -> list[list[int]]:
        """! Generates corresponding 2-literal clauses from a 4-literal clause.
        @param cl  A clause of 4 literals.
        @return  List of clauses of 2 literals.
        """
        if len(cl) < 2:
            raise ValueError("Invalid clause size")
        if len(cl) == 2:
            return [[-cl[0], -cl[1]]]
        cnf = []
        for k in range(1, len(cl)):
            cnf.append([-cl[0], -cl[k]])
        cnf.extend(Sudoku.clause_gen(cl[1:]))
        return cnf

    def __sudoku_to_cnf(self) -> list[list[int]]:
        """! Generate a CNF formula for the Sudoku grid.
        @return  A CNF formula for the Sudoku grid.
        """
        cnf = []
        num = []
        index = 1
        # Create a table containing all the variable numbers
        for i in range(self.n ** 2):
            num.append([])
            for j in range(self.n ** 2):
                num[i].append([])
                for k in range(self.n ** 2):
                    num[i][j].append(index)
                    index += 1
        # Clauses type 1
        for i in num:
            for j in range(len(i)):
                line = []
                for k in i:
                    line.append(k[j])
                cnf.extend(Sudoku.clause_gen(line))
                cnf.append(line)
        # Clauses type 2
        for c in range(self.n ** 2):
            for j in range(self.n ** 2):
                col = []
                for i in range(self.n ** 2):
                    col.append(num[i][c][j])
                cnf.extend(Sudoku.clause_gen(col))
                cnf.append(col)
        # Clauses type 3
        for start_line in range(0, self.n ** 2, self.n):
            for start_col in range(0, self.n ** 2, self.n):
                for index in range(self.n ** 2):
                    r = []
                    for i in range(self.n):
                        for j in range(self.n):
                            r.append(num[start_line + i][start_col + j][index])
                    cl2 = Sudoku.clause_gen(r)
                    # Checking for duplicates
                    for cl in cl2:
                        if cl not in cnf:
                            cnf.append(cl)
                    cnf.append(r)
        # Clauses type 4
        for i in num:
            for j in i:
                cnf.extend(Sudoku.clause_gen(j))
        return cnf

    def solve(self) -> bool:
        """! Try to solve the sudoku grid.
        @return  True if the Sudoku grid is solved, False otherwise.
        """
        list_var_grid = self.__init_list_var()
        cnf = CNF(self.__sudoku_to_cnf(), list_var_grid)
        dpll = DPLL(cnf)
        solvable = dpll.solve()
        if not solvable:
            return False
        self.__set_grid_from_var(dpll.get_cnf().get_list_var())
        print(self.__grid)
        return True
