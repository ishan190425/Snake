import tkinter as tk


class Snake:
    def __init__(self, master, canvas):
        self.master = master
        self.masterX = self.master.winfo_screenwidth()
        self.masterY = self.master.winfo_screenheight()

        self.canvas = canvas

        self.snakes = []

        # to take care movement in x direction
        self.x = 10
        # to take care movement in y direction
        self.y = 0

        # creating rectangle
        self.snake_head = self.canvas.create_rectangle(5, 5, 25, 25, fill="green", tags='snake')
        self.snakes.append(self.snake_head)


        self.snake_coords = []
        self.tempCords = self.canvas.coords(self.snake_head)
        self.snake_coords.append(self.tempCords)

    def left(self):
        self.x = -10
        self.y = 0

    def right(self):
        self.x = 10
        self.y = 0

    def up(self):
        self.x = 0
        self.y = -10

    def down(self):
        self.x = 0
        self.y = 10

    def addBody(self, canvas):
        self.canvas = canvas
        return self.canvas.create_rectangle(1, 1, 1, 1, fill="green", tags='snakeBody')

    def ateApple(self, canvas):
        self.snakes.append(self.addBody(canvas))
        self.tempCords = self.canvas.coords(self.snakes[-1])
        self.snake_coords.append(self.tempCords)

    def movement(self):
        self.snake_coords[0] = self.canvas.coords(self.snake_head)
        self.canvas.move(self.snake_head, self.x, self.y)

        for i in range(1, len(self.snakes)):
            x1, y1, x2, y2 = self.snake_coords[i - 1]
            self.canvas.coords(self.snakes[i], x1, y1, x2, y2)
            self.snake_coords[i - 1] = self.canvas.coords(self.snakes[i - 1])

        self.snake_coords[-1] = self.canvas.coords(self.snakes[-1])
