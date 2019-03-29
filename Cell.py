import tkinter.font as tkfont
class Cell:

    def __init__(self, row, col, size, num):

        self.num = num
        self.size = size
        self.row = row
        self.col = col
        self.fontColour = '#000000'
        self.x = col * self.size
        self.y = row * self.size
        self.colour = '#FFFFFF'
        self.grid = 3 * (row // 3) + col // 3
        self._solved = False
        self.setVal(num)
        self.possibleValues = range(1,10)

        #print(repr(self))

    def __str__(self):
        return str(self.num)

    def __repr__(self):
        return str(self.num)

    def copy(self):
        return Cell(self.num)

    def getVal(self):
        return self.num

    def resetPossible(self):
        if self._solved:
            self.possibleValues = [self.num]
        else:
            self.possibleValues = range(1,10)

    def setVal(self, val):

        self.num = val
        if self.num != 0:
            self.possibleValues = [self.num]
            self._solved = True
        else:
            self.possibleValues = range(1,10)
            self._solved = False

    def getPossible(self):
        return self.possibleValues
    def getGrid(self):
        return self.grid

    def setPossible(self, values):

        self.possibleValues = values

    def removePossibleValues(self, remove):

        self.possibleValues = [val for val in self.possibleValues if val not in remove]

    def isSolved(self):
        return self._solved

    def check(self):

        if len(self.possibleValues) == 1:
            self.num = self.possibleValues[0]
            self._solved = True
            return True
        else:
            self._solved = False
            return False
    def changeColour(self, colour):
        self.colour = colour

    def printCell(self):

        print('Value =  ', self.num)
        print('Row = ', self.row)
        print('Col = ', self.col)
        print('pos val = ', self.possibleValues)
        print('Solved = ', self._solved)

    def draw(self,canvas):
        canvas.create_rectangle(self.x, self.y, self.x + self.size, self.y + self.size, fill=self.colour)
        if self.row == 0 and self.col == 8:
            print("Drawong")
        if self._solved:
            font = tkfont.Font(size=3*self.size // 5)
            canvas.create_text(self.x + self.size // 2, self.y + self.size // 2, text=str(self.num),fill=self.fontColour, font=font)
        else:

            font=tkfont.Font(size =8)
            for i in self.possibleValues:
                x = self.x + self.size // 6 * (1 + 2*((i - 1) % 3))
                y = self.y + self.size // 6 * (1+2*((i - 1) // 3))
                canvas.create_text(x, y, text=str(i), fill='#FF0000',font=font)

