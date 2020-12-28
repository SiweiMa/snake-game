import pygame
import sys
from snake import *
from pygame.locals import *
from game_core import GameCore


class GameLevel2(GameCore):

    def __init__(self):
        super().__init__()
        pygame.display.set_caption("Level 2")
        self.confusion_count = 0

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
                    if event.key == K_UP or event.key == K_DOWN or event.key == K_LEFT or event.key == K_RIGHT:
                        self.confusion_count += 1
                        if event.key == K_UP:
                            self.temp_direction = [0, -1]
                        elif event.key == K_DOWN:
                            self.temp_direction = [0, 1]
                        elif event.key == K_LEFT:
                            self.temp_direction = [-1, 0]
                        elif event.key == K_RIGHT:
                            self.temp_direction = [1, 0]

            if self.confusion_count % 1 == 0:
                self.direction = [-i for i in self.temp_direction]
            else:
                self.direction = self.temp_direction

            self.eat_snack()
            self.snake.collision()
            self.draw_window()

            pygame.display.update()