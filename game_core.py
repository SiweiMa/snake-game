import random
import pygame
from constant import *
from snake import *
from pygame.locals import *


class GameCore:

    def __init__(self):
        """
        Attributes:
            win: a display Surface in pygame
            clock: a clock object that can be used to track time
            direction: default moving direction of a snake
            temp_direction: moving direction of a snake responding to a event
            snake: an instance of Snake class
            snack: an instance of Cube class
        """
        self.win = pygame.display.set_mode((win_width_game, win_width_game))
        self.clock = pygame.time.Clock()
        self.direction = [1, 0]
        self.temp_direction = [1, 0]

        self.snake = Snake(pos=snake_initial_pos, color=snake_color)
        self.snack = Cube(pos=self.random_pos(self.snake.body)[0], color=snack_color)

    def random_pos(self, snake_body):
        """
        Obtain five random positions which do not conflict with snake body
        The first random position is the one of snack while the other four are the ones of fake snacks
        Take a list of Cube instances as snake body and return a list of tuples containing random x, y row number pair
        """
        while True:
            x = random.sample(range(rows), 5)
            y = random.sample(range(rows), 5)
            x_y_pairs = list(zip(x, y))
            for item in x_y_pairs:
                if len(list(filter(lambda z: z.pos == item, snake_body))) > 0:
                    break
            else:
                return x_y_pairs

    def eat_snack(self):
        """
        If snake eats a snack, set grow as True. Then reset the location of snack
        """
        grow = self.snake.move(self.direction, self.snack)
        if grow is True:
            self.reset_snack()

    def reset_snack(self):
        self.snack = Cube(pos=self.random_pos(self.snake.body)[0], color=snack_color)

    def draw_grid(self):
        size_between = win_width_game // rows

        x = 0
        y = 0

        for l in range(rows):
            x = x + size_between
            y = y + size_between

            pygame.draw.line(self.win, light_grey, (x, 0), (x, win_width_game))
            pygame.draw.line(self.win, light_grey, (0, y), (win_width_game, y))

    def draw_window(self):
        """
        draw all including snake, snack, grid, score on Surface win
        """

        self.win.fill((0, 0, 0)) # fill the surface with black
        self.snake.draw(self.win)
        self.snack.draw(self.win)
        self.draw_grid()

        # show score as the length of snake
        f = pygame.font.Font(None, 30)
        g = f.render('Score: '+str(self.snake.score), True, grey)
        self.win.blit(g, (350, 50))
