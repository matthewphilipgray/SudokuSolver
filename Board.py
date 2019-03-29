"""
board is used to store the full set of cells of the board as a matrix and as separate grids
this makes checking the grids easier each time

"""

from Collection import Collection
from Cell import Cell
from Grid import Grid
import numpy as np
import time


class Board:

    def __init__(self, width, settings=[]):

        self.size = len(settings)
        self.width = width
        self.cellWidth = width // 9
        self.settings = [[Cell(row, col, self.cellWidth, settings[row][col]) for col in range(self.size)]
                         for row in range(self.size)]
        self.unsolved = []
        self.rows = [Collection() for _ in range(self.size)]
        self.cols = [Collection() for _ in range(self.size)]
        self.grids = [Grid() for _ in range(self.size)]
        self.__setUnsolved()



        for i in range(self.size):
            for j in range(self.size):
                self.rows[i].addCell(self.settings[i][j])
                self.cols[j].addCell(self.settings[i][j])
                self.grids[self.settings[i][j].getGrid()].addCell(self.settings[i][j])

        self.lookup = [self.rows, self.cols, self.grids]

    def __setUnsolved(self):
        unsolved = []
        for i in range(self.size):
            for j in range(self.size):
                if not self.settings[i][j].isSolved():
                    unsolved.append(self.settings[i][j])

        self.unsolved = unsolved

    def resetBoard(self, settings):

        for i in range(self.size):
            for j in range(self.size):
                self.settings[i][j].setVal(settings[i][j])
        self.__setUnsolved()

    def __str__(self):
        print("A")

    def printBoard(self):

        string = ''

        for i in range(9):
            for j in range(9):
                string += str(self.settings[i][j])
                if j != 8:
                    if j % 3 == 2:
                        string += '   '
                    else:
                        string += ' '
            string += '\n'
            if i % 3 == 2 and i != 8:
                string += '\n'

        print(string)

    def draw(self, canvas):
        for row in self.settings:
            for cell in row:
                cell.changeColour("#FFFFFF")
        for cell in self.unsolved:
            cell.changeColour("#FFFFAA")
        for row in self.settings:
            for cell in row:
                cell.draw(canvas)

    def selectCell(self, x, y, canvas):
        row = y // self.cellWidth
        col = x // self.cellWidth
        print(row, col)
        print(self.settings[row][col].getPossible())
#
#=======================================================================================================================
#start of logic
#=======================================================================================================================
#

    def checkSolved(self):


        for cell in self.unsolved:
            cell.check()

        self.unsolved = [cell for cell in self.unsolved if not cell.isSolved()]
        for collections in self.lookup:
            for collection in collections:
                collection.updateSolved()

        self.rows[7].printVals()


    def checkCancellations(self):
        for collections in self.lookup:
            for collection in collections:
                collection.cancel()
        self.checkSolved()

    def checkUnique(self):

        for collections in self.lookup:
            for collection in collections:
                collection.unique()
        self.checkSolved()

    def checkHidden(self):
        for collections in self.lookup:
            for collection in collections:
                collection.hiddenNVals()
        self.checkSolved()