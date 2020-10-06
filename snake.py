import sys
import random
from PIL import Image, ImageTk
from tkinter import Tk, Frame, Canvas, ALL, NW

# constants used in game
class Constants:
    BOARD_WIDTH = 300
    BOARD_HEIGHT = 300
    DELAY = 100
    DOT_SIZE = 10
    MAX_RAND_POS = 27

class Board(Canvas):
    def __init__(self):
        super().__init__(width=Constants.BOARD_WIDTH, height=Constants.BOARD_HEIGHT, background='black', highlightthickness=0)

        self.initGame()
        self.pack()

    # initializes game
    def initGame(self):
        self.inGame = True
        self.dots = 3
        self.score = 0

        # variables used to move snake object
        self.moveX = Constants.DOT_SIZE
        self.moveY = 0

        # starting apple coordinates
        self.appleX = 100
        self.appleY = 190

        self.loadImages()

        self.createObjects()
        self.locateApple()
        self.bind_all("<Key>", self.onKeyPressed)
        self.after(Constants.DELAY, self.onTimer)

    # load imanges from disk
    def loadImages(self):
        try:
            self.idot = Image.open("dot.png")
            self.dot = ImageTk.PhotoImage(self.idot)
            self.ihead = Image.open("head.png")
            self.head = ImageTk.PhotoImage(self.ihead)
            self.iapple = Image.open("apple.png")
            self.apple = ImageTk.PhotoImage(self.apple)

        except IOError as err:
            print(err)
            sys.exit(1)

    # create objects on Canvas
    def createObjects(self):
        self.create_text(30, 10, text="Score: {0}".format(self.score), tag="score", fill="white")
        self.create_image(self.appleX, self.appleY, image=self.apple, anchor=NW, tag="apple")
        self.create_image(50, 50, image=self.head, anchor=NW, tag="head")
        self.create_image(30, 50, image=self.dot, anchor=NW, tag="dot")
        self.create_image(40, 50, image=self.dot, anchor=NW, tag="dot")

    # check if snake head collides with apple
    def checkAppleCollsion(self):
        apple = self.find_withtag("apple")
        head = self.find_withtag("head")

        x1, y1, x2, y2 = self.bbox(head)
        overlap = self.find_overlapping(x1, y1, x2, y2)

        for i in overlap:
            if apple[0] == i:
                self.score += 1
                x, y = self.coords(apple)
                self.create_image(x, y, image=self.dot, anchor=NW, tage="dot")
                self.locateApple()
                