import random 
import tkinter as tk
from tkinter import *
from tkinter import ttk

from Apple import Apple
from Snake import Snake


class Board():
    def __init__(self, master=None):
        self.master = master
        self.masterX = self.master.winfo_screenwidth() #window dimensions
        self.masterY = self.master.winfo_screenheight()

        # canvas object to create shape
        self.canvas = Canvas(master)
        self.canvas.configure(bg='black')

        self.score = 0
        self.score_text = self.canvas.create_text(100, 100, text="Score: " + str(self.score), fill="white") #create score
        self.canvas.coords(self.score_text, self.masterX - 35, 15)

        self.canvas.pack(fill=tk.BOTH, expand=1)

        self.apple = Apple(master, self.canvas)

        self.snake = Snake(master, self.canvas)
        
        self.last_score = 0
        self.game_over = False
        self.movement()

    def lost(self):
        x1, y1, x2, y2 = self.canvas.coords(self.snake.snake_head)

        if x1 < 0 or x2 > self.masterX or y1 < 0 or y2 > self.masterY: #out of bounds
            return True

        for i in range(2, len(self.snake.snake_coords)):
            a1, b1, a2, b2 = self.snake.snake_coords[i]
            if (a1 == x1 and a2 == x2) and (y1 == b1 and b2 == y2): #if snake_head touchs snake body
                return True

        return False

    def increment_score(self):
        self.score += 1
        self.canvas.itemconfig(self.score_text, text="Score: " + str(self.score))

        if self.score == 10:
            self.canvas.coords(self.score_text, self.masterX - 36, 15) #push back one pixel to acount for bigger score
        
        elif self.score == 100:
            self.canvas.coords(self.score_text, self.masterX - 37, 15)
        
        elif self.score == 1000:
            self.canvas.coords(self.score_text, self.masterX - 38, 15)

    def movement(self):
        if self.game_over:
            return

        if self.lost():
            self.gameOver()

        if self.apple.ate_apple(self.canvas):
            self.increment_score()
            self.apple.reset_apple()
            self.snake.ate_apple(canvas=self.canvas) #add body

        self.snake.movement()
        self.canvas.after(100, self.movement)

    def gameOver(self):
        self.game_over = True
        self.snake.gameOver()

    def reset(self):
        self.canvas.delete('all')

        self.score_text = self.canvas.create_text(100, 100, text="Score: " + str(self.score), fill="white") #create score
        self.canvas.coords(self.score_text, self.masterX - 35, 15)

        self.canvas.pack(fill=tk.BOTH, expand=1)

        self.apple = Apple(self.master, self.canvas)

        self.snake = Snake(self.master, self.canvas)

        self.game_over = False
        self.movement()

    




    

    
