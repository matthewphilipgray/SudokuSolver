"""
grid class exist to package the numbers into 9 grids from the board class to simplify calculation

"""

class Collection:


    def __init__(self):

        self.cells = []
        self.solved = []
        self.unsolved = []
        self.possibles = []
        self.calcPossibles()

    def addCell(self, cell):
        if cell.isSolved():
            self.solved.append(cell)
        else:
            self.unsolved.append(cell)
            
        self.cells.append(cell)

    def setCellValue(self, value, index):

        self.cells[index].num = value

    def calcPossibles(self):

        self.possibles = []
        for cell in self.unsolved:
            cellPossibles = cell.getPossible()
            for val in cellPossibles:
                if val not in self.possibles:
                    self.possibles.append(val)


    def removePossibleValues(self):
        pass

    def getSolvedValues(self):

        solved = []
        for cell in self.cells:
            if cell.isSolved():
                solved.append(cell.getVal())
        return solved

    def printVals(self):
        print(len(self.unsolved))
        print(self.possibles)
        string = ""
        for cell in self.unsolved:
            string += str(cell)

        print(string)

    def updateSolved(self):

        for cell in self.unsolved:
            if cell.isSolved():
                self.solved.append(cell)
                self.unsolved.remove(cell)

    def cancel(self):

        to_remove = [cell.getVal() for cell in self.solved]
        for cell in self.unsolved:
            cell.removePossibleValues(to_remove)

    def unique(self):
        self.calcPossibles()

        for possible in self.possibles:
            oneCell = False
            index = -1
            for i in range(len(self.unsolved)):
                if possible in self.unsolved[i].getPossible():
                    if oneCell:
                        oneCell = False
                        break
                    else:
                        index = i
                        oneCell = True

            if oneCell:
                self.unsolved[index].setPossible([possible])

    #NOTE: THIS DOES NOT ACCOUNT FOR WHEN NOT ALL POSSIBLE VALUES ARE PRESENT IN TRIPLETS AND QUADRUPLETS
    def hiddenNVals(self):

        n  = 2
        vals_with_n = 0
        index_of_hidden = []
        vals = []
        for val in self.possibles:
            indexs = []
            count_cells = 0
            for i in range(len(self.unsolved)):
                if val in self.unsolved[i].getPossible():
                    count_cells += 1
                    if count_cells > n:
                        break
                    else:
                        indexs.append(i)
            if count_cells == n:
                vals_with_n += 1
                if vals_with_n > n:
                    break
                else:
                    vals.append(val)
                    index_of_hidden.append(indexs)

        if vals_with_n == n:
            if index_of_hidden[0][0] == index_of_hidden[1][0] and index_of_hidden[0][1] == index_of_hidden[1][1]:
                self.unsolved[index_of_hidden[0][0]].setPossible(vals)
                self.unsolved[index_of_hidden[0][1]].setPossible(vals)




