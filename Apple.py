from random import randint


class Apple:
    def __init__(self, master, canvas):
        self.canvas = canvas
        self.apple = self.canvas.create_rectangle(5, 5, 25, 25, fill="red", tags='apple')
        self.apple_x, self.apple_y = 0, 0

        self.master = master

        self.masterX = self.master.winfo_screenwidth()
        self.masterY = self.master.winfo_screenheight()

        self.reset_apple()
        self.canvas.coords(self.apple, self.apple_x - 20, self.apple_y - 20, self.apple_x, self.apple_y)

    def reset_apple(self):
        self.apple_x = randint(20, self.masterX - 20)
        self.apple_y = randint(20, self.masterY - 20)
        self.canvas.coords(self.apple, self.apple_x - 20, self.apple_y - 20, self.apple_x, self.apple_y)

    def eating_apple(self, canvas):
        self.canvas = canvas
        for item in self.canvas.find_all():
            tags = self.canvas.gettags(item)
            if 'snake' in tags:
                # current item is an input of the moved object
                # Get the items coordinates
                coords = self.canvas.coords(item)
                # Find if we overlap with other objects
                closest = self.canvas.find_overlapping(coords[0], coords[1], coords[2], coords[3])
                for closest_item in closest:
                    closest_tags = self.canvas.gettags(closest_item)
                    if 'apple' in closest_tags:
                        # If we overlap with another object, print connected and the appropriate tags
                        print("Ate Apple")
                        return True
