"""
board is used to store the full set of cells of the board as a matrix and as separate grids
this makes checking the grids easier each time

"""

from Grid import Grid
from Cell import Cell
import numpy as np
import time

class Board:

    def __init__(self, width, settings=[]):

        self.width = width
        self.cellWidth = width // 9
        self.settings = [[Cell(row, col, self.cellWidth, settings[row,col]) for col in range(len(settings[0]))]
                         for row in range(len(settings))]
        self.grids = [[] for i in range(9)]
        self.settings = np.array(self.settings)

        self.setGrids()
        self.__setUnsolved()
        self.selectedCell = [-1,-1]

    def resetBoard(self, settings):

        for i in range(len(self.settings)):
            for j in range(len(self.settings[0])):
                self.settings[i,j].setVal(settings[i,j])
        self.__setUnsolved()

    def __str__(self):
        print("A")

    def selectCell(self, x, y, canvas):
        row = y // self.cellWidth
        col = x // self.cellWidth
        print(row, col)
        self.settings[row,col].changeColour('#AAAAFF')
        self.settings[row, col].draw(canvas)
        self.setBlank()
        if  not self.selectedCell[0] == -1:
            cell = self.settings[self.selectedCell[0], self.selectedCell[1]]
            cell.changeColour('#FFFFFF')
            cell.draw(canvas)

        self.selectedCell = [row, col]

    def changeCell(self, val):

        cell = self.settings[self.selectedCell[0], self.selectedCell[1]]
        cell.setVal(val)
        self.__setUnsolved()
        self.resetPossible()
        self.updatePossibleValues()
        self.setBlank()
        self.checkErrors(cell)
        #self.checkCancellations()
        #self.checkUniques()
    def setBlank(self):

        for row in self.settings:
            for cell in row:
                cell.changeColour('#FFFFFF')

    def getRow(self, row):
        return self.settings[row]

    def getCol(self, col):
        return self.settings[:,col]

    def getCellValue(self, row, col):
        return self.settings[row, col].num

    def getCell(self, row, col):
        return self.settings[row,col]

    def printBoard(self):

        string = ''

        for i in range(9):
            for j in range(9):
                string += str(self.settings[i,j])
                if j != 8:
                    if j % 3 == 2:
                        string += '   '
                    else:
                        string += ' '
            string += '\n'
            if i % 3 == 2 and i != 8:
                string +=  '\n'

        print(string)

    def nMatching(self):

        self.checkMatching(self.settings)
        self.checkMatching(self.settings.T)
        self.checkMatching(self.grids)



    def checkMatching(self, cells):

        for selection in cells:
            #will check for pairs, triplets, quadreplets
            for n in range(2,5):
                #check for all of the possible values
                for i in range(1,10):
                    pass




    def setGrids(self):

        for i in range(9):
            for j in range(9):
                gridNumber = 3*(i // 3) + j // 3
                self.grids[gridNumber].append(self.settings[i, j])

    def __setUnsolved(self):
        unsolved = []
        for i in range(9):
            for j in range(9):
                if not self.settings[i,j].isSolved():
                    unsolved.append(self.settings[i, j])

        self.unsolved = unsolved



    def updatePossibleValues(self):

        self.updateRows()
        self.updateCols()
        self.updateGrids()

    def updateRows(self):

        for row in self.settings:
            indexs = []
            remove = []
            for i in range(len(row)):

                if row[i].isSolved():
                    remove.append(row[i].getVal())
                else:
                    indexs.append(i)
            for index in indexs:
                row[index].removePossibleValues(remove)


    def resetPossible(self):

        for cell in self.unsolved:
            cell.resetPossible()


    def updateCols(self):

        for col in self.settings.T:
            indexs = []
            remove = []
            for i in range(len(col)):

                if col[i].isSolved():
                    remove.append(col[i].getVal())
                else:
                    indexs.append(i)
            for index in indexs:
                col[index].removePossibleValues(remove)
    def updateGrids(self):

        for grid in self.grids:
            indexs = []
            remove = []
            for i in range(len(grid)):

                if grid[i].isSolved():
                    remove.append(grid[i].getVal())
                else:
                    indexs.append(i)
            for index in indexs:
                grid[index].removePossibleValues(remove)

    def checkUniques(self):

        for cell in self.unsolved:
            if self.__checkCells(cell, self.grids[cell.getGrid()]):
                continue
            elif self.__checkCells(cell, self.getRow(cell.row)):
                continue
            elif self.__checkCells(cell, self.getCol(cell.col)):
                continue



    #check cells are the cells that the current cell is checking against
    #if it is found that only the current cell can contain a number then that is the only possible
    def __checkCells(self, cell, checkCells):


        for possible in cell.getPossible():
            unique = True
            for checkCell in checkCells:
                if checkCell != cell:
                    if possible in checkCell.getPossible():
                        unique = False
                        break

            if unique:
                cell.setPossible([possible])
                return True

        return False

    #this function is used to check for cancellations by only having possible values in one row or column of a grid
    #this further increases the accuracy of the program
    def checkCancellations(self):



        for cell in self.unsolved:

            checkCells = self.grids[cell.getGrid()]

            for possible in cell.getPossible():
                freeRow = True
                freeCol = True
                available = True

                for checkCell in checkCells:

                    if checkCell.getVal() == possible:
                        available = False
                        break
                    if cell != checkCell:
                         if possible in checkCell.getPossible():
                             if cell.row == checkCell.row:
                                 freeCol = False
                             if cell.col == checkCell.col:
                                 freeRow = False
                             else:
                                 freeRow = False
                                 freeCol = False

                if not freeRow and not freeCol:
                    break

                if freeRow and available:
                    self.cancelCells(possible, cell.getGrid(), self.getRow(cell.row))

                if freeCol and available:
                    self.cancelCells(possible, cell.getGrid(), self.getCol(cell.col))


    def cancelCells(self, possible, grid, cells):

        for cell in cells:
            #cell.colour = '#0055FF'
            if cell.getGrid() != grid:
                cell.removePossibleValues([possible])




    def printGrid(self, index):
        string = ''
        for i in range(len(self.grids[index])):

            string += str(self.grids[index][i])
            if i != 8:
                if i % 3 == 2:
                    string += '\n'
                else: string += ' '

        print(string)


    def checkErrors(self, cell):

        row = self.getRow(cell.row)
        col = self.getCol(cell.col)
        grid = self.grids[cell.getGrid()]
        a = self.checkAgainst(cell, row)
        b = self.checkAgainst(cell, col)
        c = self.checkAgainst(cell, grid)

        return a or b or c





    def checkAgainst(self, cell, checkCells):
        found = False
        for checkCell in checkCells:
            if checkCell != cell:
                if checkCell.isSolved():
                    if checkCell.num == cell.num:
                        checkCell.changeColour('#FF0000')
                        cell.changeColour('#FF0000')
                        found = True
        return found

    def updateValues(self):
        unsolved = []
        for i in range(len(self.unsolved)):
            if not self.unsolved[i].check():
                unsolved.append(self.unsolved[i])

        if len(self.unsolved) == len(unsolved):
            self.changed = False
        self.unsolved = unsolved

    def run(self):
        self.updatePossibleValues()
        self.checkCancellations()
        self.checkUniques()

    def iterate(self):

        self.updatePossibleValues()
        self.checkCancellations()
        self.checkUniques()
        self.updateValues()

    def iterateCancel(self):

        self.checkCancellations()

        # self.checkUniques()

    def update(self):

        self.updateValues()


        # self.checkUniques()

    def errorSearch(self):


        if not self.solve():

            baseSettings = np.array([[self.settings[i,j].getVal() for j in range(9)] for i in range(9)])

            solved = False
            length = len(self.unsolved)
            i = 0
            while not solved and i < length:
                self.resetBoard(baseSettings)
                possibles = self.unsolved[i].getPossible()
                nPossible = len(possibles)
                j = 0
                while not solved and j < nPossible:
                    self.unsolved[i].setVal(possibles[j])
                    solved = self.solve()
                    if solved:
                        reallySolved = True
                        for row in self.settings:
                            for cell in row:
                                if not self.checkErrors(cell):
                                    reallySolved = False
                                    break
                            if not reallySolved:
                                break

                        solved = reallySolved
                    if not solved:
                        self.resetBoard(baseSettings)
                        possibles = self.unsolved[i].getPossible()
                        j += 1
                i += 1

    def solve(self):
        i = 0
        self.changed = True
        count = 0
        while count < 500 and len(self.unsolved) > 0:
            i += 1

            self.iterate()

            if self.changed:
                count = 0
            else:
                count += 1

        if len(self.unsolved) == 0:
            print("\nsolved\n")
            return True
        else:
            if count == 500:
                print('overrun')
            return False
    def draw(self, canvas):


        for row in self.settings:

            for cell in row:
                cell.draw(canvas)



