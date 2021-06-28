
import pygame
from random import randint
import numpy as np


class GameAI:
    def __init__(self, width=400, height=300, speed=1) -> None:
        pygame.init()
        self.clock = pygame.time.Clock()
        self.dis = pygame.display.set_mode((width, height))
        pygame.display.update()
        pygame.display.set_caption('Snake')
        self.game_over = False
        self.masterX, self.masterY = pygame.display.get_surface().get_size()

        self.SPEED_CONSTENT = speed
        self.x_speed = self.SPEED_CONSTENT
        self.y_speed = 0

        #currents
        self.white = (255, 255, 255)
        self.yellow = (255, 255, 102)
        self.black = (0, 0, 0)
        self.red = (213, 50, 80)
        self.green = (0, 255, 0)
        self.blue = (50, 153, 213)

        #game variables
        self.score = 0
        self.last_score = 0
        self.record = 0
        self.gen = 0

        self.prev = 0

        #list of snakses
        self.snakes = []
        self.snake_coords = []
        self.snake_head = pygame.draw.rect(
            self.dis, self.white, (self.masterX/2, self.masterY/2, 20, 20))
        self.snakes.append(self.snake_head)
        self.snake_coords.append(self.snake_head)
        
        self.font_style = pygame.font.SysFont(None, 25)

        self.apple = None
        self.reset_apple()

    #lose coditons if they cross the screen
    def lost(self):
        screen = self.dis.get_rect()
        if self.snake_head.right > screen.right:
            return True
        if self.snake_head.left < screen.left:
            return True
        if self.snake_head.top < screen.top:
            return True
        if self.snake_head.bottom > screen.bottom:
            return True
        return False 


    def self_colision(self):
        for i in range(1, len(self.snakes)):
            if self.snake_head == self.snakes[i]:
                return True
        return False


    def near_collison(self):
        for i in range(1, len(self.snakes)):
            if self.snake_head.right + 1 == self.snakes[i].left:
                return True
            elif self.snake_head.left - 1 == self.snakes[i].right:
                return True
            elif self.snake_head.top - 1 == self.snakes[i].bottom:
                return True
            elif self.snake_head.bottom + 1 == self.snakes[i].top:
                return True
        return False

    #reset the game
    def reset(self, gen, record):
        self.dis.fill(self.black)
        self.game_over = False
        self.score = 0
        self.last_score = 0
        self.clock = pygame.time.Clock()
        pygame.display.update()
        self.x_speed = 0
        self.y_speed = 0
        self.reset_snake()
        self.reset_apple()
        self.gen = gen
        self.record = record
        self.run()


    def left(self):
        if self.going_right():
            return self.right()
        self.x_speed = -self.SPEED_CONSTENT
        self.y_speed = 0
        self.prev = 1
    

    def going_left(self):
        return self.prev == 1

    def stop(self):
        self.x_speed = 0
        self.y_speed = 0

    def right(self):
        if self.going_left():
            return self.left()
        self.x_speed = self.SPEED_CONSTENT
        self.y_speed = 0
        self.prev = 2
    

    def going_right(self):
        return self.prev == 2


    def up(self):
        if self.going_down():
            return self.down()
        self.x_speed = 0
        self.y_speed = -self.SPEED_CONSTENT
        self.prev = 3
    

    def going_up(self):
        return self.prev == 3

    def down(self):
        if self.going_up():
            return self.up()
        self.x_speed = 0
        self.y_speed = self.SPEED_CONSTENT
        self.prev = 4
    
    def going_down(self):
        return self.prev == 4

    def increment_score(self):
        self.score += 1
        self.add_body()
        self.reset_apple()

    #return the current state
    def get_state(self):
        state = [x for x in range(12)]
        
        screen = self.dis.get_rect()
        temp = self.snake_head

        #if almost collision
        state[0] = temp.left - self.SPEED_CONSTENT < screen.left

        state[1] = temp.right + self.SPEED_CONSTENT > screen.right

        state[2] = temp.top - self.SPEED_CONSTENT < screen.top

        state[3] = temp.bottom + self.SPEED_CONSTENT > screen.bottom

        state[4] = self.going_left() and not self.game_over  # going left
        state[5] = self.going_right() and not self.game_over  # right
        state[6] = self.going_up() and not self.game_over  # up
        state[7] = self.going_down() and not self.game_over  # down

        snakex = self.snake_head.centerx
        snakey = self.snake_head.centery
        applex = self.apple.centerx
        appley = self.apple.centery

        temp = self.snake_head

        #if almost apple
        t = temp.move(-1 * self.SPEED_CONSTENT,0)
        state[8] = (snakex > applex or t.colliderect(self.apple)) and not self.game_over # food left
        
        t = temp.move(self.SPEED_CONSTENT,0)
        state[9] = (snakex < applex or t.colliderect(self.apple)) and not self.game_over  # right
        
        t = temp.move(0,-1 * self.SPEED_CONSTENT)
        state[10] = (snakey > appley or t.colliderect(self.apple)) and not self.game_over  # up
        
        t = temp.move(0,self.SPEED_CONSTENT)
        state[11] = (snakey < appley or t.colliderect(self.apple)) and not self.game_over  # down
        
        return np.array(state, dtype=int)

    def play_move(self, move):
        if move[0] == 1:
            self.left()

        elif move[1] == 1:
            self.right()

        elif move[2] == 1:
            self.up()

        elif move[3] == 1:
            self.down()

        self.run()

        reward = -1

        if self.game_over:
            reward = -1000

        elif self.last_score is not self.score:
            reward = 1000
            self.last_score = self.score
        
        self.stop()

        return reward, self.game_over, self.score


    def movement(self):
        if self.game_over:
            return
        if self.lost():
            self.game_over = True
            return 
        self.dis.fill(self.black)
        

    def update_score(self):
        value = self.font_style.render(
            "Gen: " + str(self.gen) + " Score: " + str(self.score) 
            + " Record: " + str(self.record), True, self.blue)
        self.dis.blit(value, [0, 0])


    def update(self):
        pygame.draw.rect(self.dis, self.red, self.apple)
        self.draw_snake()
        self.update_score()
        pygame.display.update()
        self.clock.tick(40)


    def run(self):
        self.movement()
        if self.ate_apple():
            self.increment_score()
        self.update()


    def reset_apple(self):
        apple_x = randint(0, self.masterX - 20)
        # max dimensions, place in window
        apple_y = randint(0, self.masterY - 20)
        self.apple = pygame.draw.rect(
            self.dis, self.red, (apple_x, apple_y, 20, 20))


    def ate_apple(self):
        return self.apple.colliderect(self.snake_head)

    #reset the snake
    def reset_snake(self):
        self.snakes = []
        self.snake_coords = []
        self.snake_head = pygame.draw.rect(
            self.dis, self.white, (self.masterX/2, self.masterY/2, 20, 20))
        self.snakes.append(self.snake_head)
        self.snake_coords.append(self.snake_head)


    def add_body(self):
        snake_body = self.snakes[-1]
        self.snakes.append(snake_body)
        self.snake_coords.append(snake_body)
        self.draw_snake()

    #draw the snake
    def draw_snake(self):
        self.snake_head = self.snake_head.move(self.x_speed, self.y_speed)
        pygame.draw.rect(self.dis, self.white, self.snake_head)
        self.snakes[0] = self.snake_head
        for i in range(1, len(self.snakes)):
            temp = self.snake_coords[i-1]
            self.snakes[i] = temp
            self.snake_coords[i-1] = self.snakes[i-1]
            pygame.draw.rect(self.dis, self.white, self.snakes[i])
        self.snake_coords[-1] = self.snakes[-1]


if __name__ == '__main__':
    g = GameAI()
    while True:
        g.run()
