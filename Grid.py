"""
grid class exist to package the numbers into 9 grids from the board class to simplify calculation

"""

class Grid:


    def __init__(self, values = []):

        self.values = values

    def addCell(self, cell):
        self.values.append(cell)

    def setCellValue(self, value, index):

        self.values[index].num = value


    def removePossibleValues(self):
        pass