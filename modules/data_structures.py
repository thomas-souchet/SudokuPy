class Sudoku:
    def __init__(self, size):
        self.size = size**2
        self.__grid = []

    def add(self, t):
        if type(t) is not tuple:
            raise TypeError('The element type must be tuple')
        if len(t) != 3:
            raise ValueError('The tuple must have three elements')
        for i in range(len(t)):
            if type(t[i]) is not int:
                raise TypeError('The element must only contains integers')
            if i <= 1 and (t[i] < 0 or t[i] > self.size-1):
                raise ValueError('The first two elements must be between 1 and %d' % (self.size-1))
        self.__grid.append(t)

    def remove_all(self):
        self.__grid = []

    def get(self):
        return self.__grid

    def get_by_coordinates(self, x, y):
        if x < 0 or x >= self.size or y < 0 or y >= self.size:
            raise ValueError('Coordinates out of bounds')
        for c in self.__grid:
            if c[0] == x and c[1] == y:
                return c[2]
        return -2
