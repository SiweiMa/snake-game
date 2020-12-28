import pygame
from constant import *
from game_level1 import GameLevel1
from game_level2 import GameLevel2
from game_level3 import GameLevel3


class Button:

    def __init__(self, rect, text="", default_color=grey, hovered_color=light_yellow):
        self.rect = pygame.Rect(rect)  # Rect(left, top, width, height)

        self.default_color = default_color
        self.hovered_color = hovered_color

        self.font = pygame.font.Font(None, 30)
        self.text_default = self.font.render(text, True, default_color)
        self.text_hovered = self.font.render(text, True, hovered_color)

    def hover(self, mouse):
        mouse_rect = pygame.Rect(mouse, [1, 1])  # arg: left, top, width, height # why [1,1]?
        return mouse_rect.colliderect(self.rect)

    def button_text(self, win, mouse_coords):
        if self.hover(mouse_coords):
            win.blit(self.text_hovered, self.text_hovered.get_rect(center=self.rect.center))
        else:
            win.blit(self.text_default, self.text_default.get_rect(center=self.rect.center))


class EasyButton(Button):
    def on_click(self):
        game_level1 = GameLevel1()
        game_level1.start()


class MediumButton(Button):
    def on_click(self):
        game_level2 = GameLevel2()
        game_level2.start()


class HardButton(Button):
    def on_click(self):
        game_level3 = GameLevel3()
        game_level3.start()