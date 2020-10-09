import sys
import random
from PIL import Image, ImageTk
from tkinter import Tk, Frame, Canvas, ALL, NW

# constants used in game
class Constants:
    BOARD_WIDTH = 600
    BOARD_HEIGHT = 600
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

    # load images from disk
    def loadImages(self):
        try:
            self.idot = Image.open("dot.png")
            self.dot = ImageTk.PhotoImage(self.idot)
            self.ihead = Image.open("head.png")
            self.head = ImageTk.PhotoImage(self.ihead)
            self.iapple = Image.open("apple.png")
            self.apple = ImageTk.PhotoImage(self.iapple)

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
    # if snake "eats" apple, increase score by 1
    def checkAppleCollision(self):
        apple = self.find_withtag("apple")
        head = self.find_withtag("head")

        x1, y1, x2, y2 = self.bbox(head)
        overlap = self.find_overlapping(x1, y1, x2, y2)

        for i in overlap:
            if apple[0] == i:
                self.score += 1
                x, y = self.coordinates(apple)
                self.create_image(x, y, image=self.dot, anchor=NW, tag="dot")
                self.locateApple()

    # moves snake object
    def moveSnake(self):
        dots = self.find_withtag("dot")
        head = self.find_withtag("head")

        snake = dots + head

        spot = 0

        while spot < len(snake) - 1:
            coordinate1 = self.coordinates(snake[spot])
            coordinate2 = self.coordinates(snake[spot + 1])
            self.move(snake[spot], coordinate2[0] - coordinate1[0], coordinate2[1] - coordinate1[1])
            spot += 1

        self.move(head, self.moveX, self.moveY)

    # check for collisions
    # if snake collides with itself, game over
    def checkCollisions(self):
        dots = self.find_withtag("dot")
        head = self.find_withtag("head")

        x1, y1, x2, y2 = self.bbox(head)
        overlap = self.find_overlapping(x1, y1, x2, y2)

        for dot in dots:
            for i in overlap:
                if i == dot:
                    self.inGame = False

        if x1 < 0:
            self.inGame = False
        if x1 > Constants.BOARD_WIDTH - Constants.DOT_SIZE:
            self.inGame = False
        if y1 < 0:
            self.inGame = False
        if y1 > Constants.BOARD_HEIGHT - Constants.DOT_SIZE:
            self.inGame = False

    # puts apple on Canvas
    def locateApple(self):
        apple = self.find_withtag("apple")
        self.delete(apple[0])

        rand = random.randint(0, Constants.MAX_RAND_POS)
        self.appleX = rand * Constants.DOT_SIZE
        rand = random.randint(0, Constants.MAX_RAND_POS)
        self.appleY = rand * Constants.DOT_SIZE

        self.create_image(self.appleX, self.appleY, anchor=NW, image=self.apple, tag="apple")

    # controls direction variables when cursor key is press
    def onKeyPressed(self, e):
        key = e.keysym

        LEFT_CURSOR_KEY = "Left"
        if key == LEFT_CURSOR_KEY and self.moveX <= 0:
            self.moveX = -Constants.DOT_SIZE
            self.moveY = 0

        RIGHT_CURSOR_KEY = "Right"
        if key == RIGHT_CURSOR_KEY and self.moveX >= 0:
            self.moveX = Constants.DOT_SIZE
            self.moveY = 0

        UP_CURSOR_KEY = "Up"
        if key == UP_CURSOR_KEY and self.moveY <= 0:
            self.moveX = 0
            self.moveY = -Constants.DOT_SIZE

        DOWN_CURSOR_KEY = "Down"
        if key == DOWN_CURSOR_KEY and self.moveY >= 0:
            self.moveX = 0
            self.moveY = Constants.DOT_SIZE

    # creates new game each timer event
    def onTimer(self):
        self.drawScore()
        self.checkCollisions()

        if self.inGame:
            self.checkAppleCollision()
            self.moveSnake()
            self.after(Constants.DELAY, self.onTimer)
        else:
            self.gameOver()

    # draws score
    def drawScore(self):
        score = self.find_withtag("score")
        self.itemconfigure(score, text="Score: {0}".format(self.score))

    # deletes all objects on board and draws game over message
    def gameOver(self):
        self.delete(ALL)
        self.create_text(self.winfo_width() / 2, self.winfo_height() / 2, text="Game Over! Score {0}".format(self.score), fill="white")

class Snake(Frame):
    def __init__(self):
        super().__init__()

        self.master.title("Snake")
        self.board = Board()
        self.pack()

def main():
    root = Tk()
    nib = Snake()
    root.mainloop()

if __name__ == "__main__":
    main()