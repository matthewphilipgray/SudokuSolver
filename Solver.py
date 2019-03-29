import numpy as np
from Board import Board
# from Cell import Cell
# from Grid import Grid
#

def unpack(linear):

    settings = [[0 for _ in range(9)] for _ in range(9)]
    for i in range(81):
        row = i // 9
        col = i % 9
        settings[row][col] = int(linear[i])

    return settings
#
#

from tkinter import *

class Application(Frame):

    def cancelCells(self):
        self.board.checkCancellations()
        self.drawPuzzle()

    def unique(self):
        self.board.checkUnique()
        self.drawPuzzle()

    def pairs(self):
        self.board.checkHidden()
        self.drawPuzzle()


    def createWidgets(self):
        self.QUIT = Button(self)
        self.QUIT["text"] = "QUIT"
        self.QUIT["fg"]   = "red"
        self.QUIT["command"] =  self.quit

        self.QUIT.pack({"side": "left"})

        self.cancelButton = Button(self)
        self.cancelButton["text"] = "cancel"
        self.cancelButton["fg"] = "red"
        self.cancelButton["command"] = self.cancelCells
        self.cancelButton.pack({"side": "left"})

        self.uniqueButton = Button(self)
        self.uniqueButton["text"] = "unique"
        self.uniqueButton["fg"] = "red"
        self.uniqueButton["command"] = self.unique

        self.uniqueButton.pack({"side": "left"})

        self.pairsButton = Button(self)
        self.pairsButton["text"] = "pairs"
        self.pairsButton["fg"] = "red"
        self.pairsButton["command"] = self.pairs

        self.pairsButton.pack({"side": "left"})



    def drawPuzzle(self):

        self.canvas.create_rectangle(0, 0, self.canvasWidth, self.canvasHeight, fill='#FFFFFF')
        self.board.draw(self.canvas)
        diff = 3*(self.canvasWidth // 9)
        self.canvas.create_line(diff, 0, diff, self.canvasHeight,width=2)
        self.canvas.create_line(2*diff, 0, 2*diff, self.canvasHeight, width=2)
        self.canvas.create_line(0, diff, self.canvasHeight, diff, width=2)
        self.canvas.create_line(0, 2*diff, self.canvasHeight, 2*diff, width=2)

    def callback(self, event):
        self.canvas.focus_set()
        print("clicked at", event.x, event.y)
        self.board.selectCell(event.x, event.y, self.canvas)


    def key(self, event):
        print("pressed", int(event.char))


    def __init__(self, master=None):
        Frame.__init__(self, master)

        self.canvasWidth = 600
        self.canvasHeight = self.canvasWidth

        self.canvas = Canvas(root, width=self.canvasWidth, height=self.canvasHeight)
        self.canvas.bind("<Key>", self.key)
        self.canvas.bind("<Button-1>", self.callback)

        self.canvas.pack()
        self.pack()

        settings = [[0 for _ in range(9)] for _ in range(9)]

        self.boards = []
        self.boardNumber = 1

        with open('hardSudoku.txt') as file:
            linear = file.readline()
            self.boards.append(unpack(linear))
            while linear:
                linear = file.readline()
                if len(linear) == 81:
                    self.boards.append(unpack(linear))

        self.board = Board(self.canvasWidth, self.boards[0])


        self.createWidgets()

        #print('Solved {0:d}/{1:d}'.format(count, total))

        self.drawPuzzle()

root = Tk()
app = Application(master=root)
app.mainloop()
root.destroy()