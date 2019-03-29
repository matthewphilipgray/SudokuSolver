import numpy as np
from Board import Board
# from Cell import Cell
# from Grid import Grid
#

def unpack(linear):

    settings = np.zeros((9, 9), int)
    for i in range(81):
        row = i // 9
        col = i % 9
        settings[row ,col] = int(linear[i])


    return settings
#
#

from tkinter import *

class Application(Frame):
    def iterate(self):
        self.board.solve()
        self.drawPuzzle()

    def oops(self):
        self.board.errorSearch()
        self.drawPuzzle()

    def update(self):

        settings = 0
        if self.boards[self.boardNumber]:
            settings = self.boards[self.boardNumber]
            settings = unpack(settings)
            self.board.resetBoard(settings)
            self.board.solve()
            self.boardNumber += 1
        self.drawPuzzle()


    def createWidgets(self):
        self.QUIT = Button(self)
        self.QUIT["text"] = "QUIT"
        self.QUIT["fg"]   = "red"
        self.QUIT["command"] =  self.quit

        self.QUIT.pack({"side": "left"})



        self.hi_there = Button(self)
        self.hi_there["text"] = "run",
        self.hi_there["command"] = self.iterate

        self.hi_there.pack({"side": "left"})

        self.cancel = Button(self)
        self.cancel["text"] = "special",
        self.cancel["command"] = self.oops
        self.cancel.pack({"side": "left"})

        self.yop = Button(self)
        self.yop["text"] = "update",
        self.yop["command"] = self.update
        self.yop.pack({"side": "left"})







    def drawPuzzle(self):

        self.canvas.create_rectangle(0, 0, self.canvasWidth, self.canvasHeight, fill='#FFFFFF')
        self.board.draw(self.canvas)
        diff = 3*(self.canvasWidth // 9)
        self.canvas.create_line(diff, 0, diff, self.canvasHeight,width=2)
        self.canvas.create_line(2*diff, 0, 2*diff, self.canvasHeight, width=2)
        self.canvas.create_line(0, diff, self.canvasHeight, diff, width=2)
        self.canvas.create_line(0, 2*diff, self.canvasHeight, 2*diff, width=2)
        self.canvas.create_text(0, self.canvasHeight // 2, text=selected)

    def callback(self, event):
        self.canvas.focus_set()
        print("clicked at", event.x, event.y)
        self.board.selectCell(event.x, event.y, self.canvas)
        #self.drawPuzzle()

    def key(self, event):
        print("pressed", int(event.char))
        if int(event.char) in range(10):
            print('made it in')
            self.board.changeCell(int(event.char))
            self.drawPuzzle()
        else:
            print('not working')

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.check = []
        for i in range(10):
            self.check.append(str(i))
        print(self.check)

        self.canvasWidth = 600
        self.canvasHeight = self.canvasWidth

        a = np.array([[1,2,3],[4,5,6],[7,8,9]])
        print(a)
        a.T
        print(a)



        self.canvas = Canvas(root, width=self.canvasWidth, height=self.canvasHeight)
        #self.canvas.pack()
        self.canvas.bind("<Key>", self.key)
        self.canvas.bind("<Button-1>", self.callback)

        self.canvas.pack()
        self.pack()
        self.createWidgets()
        settings = np.zeros((9, 9), int)

        self.board = Board(self.canvasWidth, settings)

        self.boards = []
        self.boardNumber = 1
        with open('hardSudoku.txt') as file:

            linear = file.readline()
            self.boards.append(linear)
            settings = unpack(linear)
            self.board.resetBoard(settings)
            #self.board.solve()
            while linear:
                linear = file.readline()
                self.boards.append(linear)
        #linear = '0' * 81
        #settings = unpack(linear)
        #self.board.resetBoard(settings)




        self.board.printBoard()

        #print('Solved {0:d}/{1:d}'.format(count, total))

        self.drawPuzzle()

root = Tk()
app = Application(master=root)
app.mainloop()
root.destroy()