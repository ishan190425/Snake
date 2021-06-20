from tkinter.constants import TRUE
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

        self.white = (255, 255, 255)
        self.yellow = (255, 255, 102)
        self.black = (0, 0, 0)
        self.red = (213, 50, 80)
        self.green = (0, 255, 0)
        self.blue = (50, 153, 213)

        self.score = 0
        self.last_score = 0
        self.record = 0
        self.gen = 0
        self.snakes = []
        self.snake_coords = []
        self.snake_head = pygame.draw.rect(
            self.dis, self.white, (5, 5, 20, 20))
        self.snakes.append(self.snake_head)
        self.snake_coords.append(self.snake_head)
        self.add_body()
        self.add_body()
        self.font_style = pygame.font.SysFont(None, 25)

        self.apple = None
        self.reset_apple()

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
        return False or self.self_colision()

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
        self.x_speed = -self.SPEED_CONSTENT
        self.y_speed = 0

    def right(self):
        self.x_speed = self.SPEED_CONSTENT
        self.y_speed = 0

    def up(self):
        self.x_speed = 0
        self.y_speed = -self.SPEED_CONSTENT

    def down(self):
        self.x_speed = 0
        self.y_speed = self.SPEED_CONSTENT

    def increment_score(self):
        self.score += 1
        self.add_body()
        self.reset_apple()

    def get_state(self):
        state = [x for x in range(13)]
        screen = self.dis.get_rect()

        state[0] = 1 if self.snake_head.top +1  <= screen.top else 0  # colsion up
        state[1] = 1 if self.snake_head.bottom -1 >= screen.bottom else 0  # down
        state[2] = 1 if self.snake_head.left -1  <= screen.left else 0  # left
        state[3] = 1 if self.snake_head.right +1  >= screen.right else 0  # right

        state[4] = 1 if self.x_speed < 0 else 0  # going left
        state[5] = 1 if self.x_speed > 0 else 0  # right
        state[6] = 1 if self.y_speed < 0 else 0  # up
        state[7] = 1 if self.y_speed > 0 else 0  # down

        state[8] = 1 if self.snake_head.left > self.apple.right else 0  # food left
        state[9] = 1 if self.snake_head.right < self.apple.left else 0  # right
        state[10] = 1 if self.snake_head.top > self.apple.bottom else 0  # up
        state[11] = 1 if self.snake_head.bottom < self.apple.top else 0  # down

        state[12] = self.score
        return np.array(state, dtype=int)

    def play_move(self, move):
        reward = 0
        if move[0] == 1:
            self.left()

        elif move[1] == 1:
            self.right()

        elif move[2] == 1:
            self.up()

        elif move[3] == 1:
            self.down()

        else:
            self.x_speed = 0
            self.y_speed = 0

        self.run()
        if self.game_over:
            reward = -10

        elif self.last_score is not self.score:
            reward = 10
            self.last_score = self.score
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
            "Gen: " + str(self.gen) + " Score: " + str(self.score) + " Record: " + str(self.record), True, self.blue)
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

    def reset_snake(self):
        self.snakes = []
        self.snake_coords = []
        self.snake_head = pygame.draw.rect(
            self.dis, self.white, (5, 5, 20, 20))
        self.snakes.append(self.snake_head)
        self.snake_coords.append(self.snake_head)

    def add_body(self):
        snake_body = self.snakes[-1]
        self.snakes.append(snake_body)
        self.snake_coords.append(snake_body)
        self.draw_snake()

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
