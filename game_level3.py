import pygame
import sys
from snake import *
from pygame.locals import *
from game_core import GameCore


class GameLevel3(GameCore):

    def __init__(self):
        super().__init__()
        pygame.display.set_caption("Level 3")
        fake_snack_poss = self.random_pos(self.snake.body)[1:]
        self.fake_snacks = [Cube(pos=fake_snack_pos, color=snack_color) for fake_snack_pos in fake_snack_poss]

    def reset_snack(self):
        super(GameLevel3, self).reset_snack()
        self.fake_snacks = [Cube(pos=fake_snack_pos, color=snack_color) for fake_snack_pos in
                            self.random_pos(self.snake.body)[1:]]

    def draw_window(self):
        super(GameLevel3, self).draw_window()
        for fake_snack in self.fake_snacks:
            fake_snack.draw(self.win)

    def start(self):
        while True:
            self.clock.tick(5)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key == K_r:
                        self.snake.reset()
                    if event.key == K_UP:
                        self.temp_direction = [0, -1]
                    elif event.key == K_DOWN:
                        self.temp_direction = [0, 1]
                    elif event.key == K_LEFT:
                        self.temp_direction = [-1, 0]
                    elif event.key == K_RIGHT:
                        self.temp_direction = [1, 0]

            self.direction = self.temp_direction

            self.eat_snack()
            self.snake.collision()
            self.draw_window()

            pygame.display.update()