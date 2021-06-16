import tkinter as tk
from random import randint
from tkinter import *
from tkinter import ttk

from Apple import Apple
from Snake import Snake


class Game:
    def __init__(self, master=None):
        self.master = master
        self.masterX = self.master.winfo_screenwidth()
        self.masterY = self.master.winfo_screenheight()

        # canvas object to create shape
        self.canvas = Canvas(master)
        self.canvas.configure(bg='black')

        self.score = 0
        self.score_text = self.canvas.create_text(100, 100, text="Score: " + str(self.score), fill="white")
        self.canvas.coords(self.score_text, self.masterX - 35, 15)

        self.apple = Apple(master, self.canvas)

        self.snake = Snake(master, self.canvas)

        self.movement()

    def lost(self):
        x1, y1, x2, y2 = self.canvas.coords(self.snake.snake_head)

        if x1 < 0 or x2 > self.masterX or y1 < 0 or y2 > self.masterY:
            return True

        for i in range(2, len(self.snake.snake_coords)):
            a1, b1, a2, b2 = self.snake.snake_coords[i]
            if (a1 == x1 and a2 == x2) and (y1 == b1 and b2 == y2):
                return True

        return False

    def increment_score(self):
        self.score += 1
        self.canvas.itemconfig(self.score_text, text="Score: " + str(self.score))

        if self.score == 10:
            self.canvas.coords(self.score_text, self.masterX - 36, 15)
        elif self.score == 100:
            self.canvas.coords(self.score_text, self.masterX - 37, 15)
        elif self.score == 1000:
            self.canvas.coords(self.score_text, self.masterX - 38, 15)

    def movement(self):
        if self.lost():
            self.canvas.wait_window(self.game_over())

        if self.apple.eating_apple(self.canvas):
            self.increment_score()
            self.apple.reset_apple()
            self.snake.ateApple(canvas=self.canvas)

        self.snake.movement()
        self.canvas.after(100, self.movement)

    def game_over(self):
        lose = tk.Toplevel()
        lose.wm_title("Game Over")
        lose.geometry("300x80")
        loss = tk.Label(lose, text="Game Over!\n" + "Score: " + str(self.score))
        loss.pack()

        b = ttk.Button(lose, text="Okay", command=lose.destroy)
        b.pack()

        b.wait_window(lose)
        quit()


if __name__ == "__main__":
    # object of class Tk, responsible for creating
    # a tkinter toplevel window
    window = Tk()
    board = Game(window)
    window.attributes('-fullscreen', True)
    window.wm_title("Snake")

    # This will bind arrow keys to the tkinter
    # toplevel which will navigate the image or drawing
    window.bind("<KeyPress-Left>", lambda e: board.snake.left())
    window.bind("<KeyPress-Right>", lambda e: board.snake.right())
    window.bind("<KeyPress-Up>", lambda e: board.snake.up())
    window.bind("<KeyPress-Down>", lambda e: board.snake.down())

    # Infinite loop breaks only by interrupt
    mainloop()
