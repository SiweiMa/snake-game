#!/usr/bin/env python3
# encoding: utf-8

import pygame
import sys
from constant import *
from button import *


class Menu:

    pygame.init()  # initialize pygame
    icon = pygame.image.load('img/snake.jpg')  # icon shown in window title bar
    pygame.display.set_icon(icon)  # set logo
    pygame.display.set_caption("Drunk Snake")  # set caption of window

    def __init__(self):
        """
        Attributes:
                win: a display Surface in pygame
                clock: a clock object that can be used to track time
                buttons: a tuple containing button instance with three difficulty levels
        """
        self.win = pygame.display.set_mode(size=(win_width_menu, win_width_menu)) # size of 500 pixel * 500 pixel
        self.clock = pygame.time.Clock()
        self.buttons = self.create_button()
        self.create_level_desc()

    def create_level_desc(self):
        """
        Create description above difficulty level buttons.
        We need to set font at first, then utilize render method of font to create a Surface with "How drunk is snake"
        Then get the rectangular area of the surface and blit Surface win with Surface text_surface
        """
        font = pygame.font.Font(None, 50)
        text_surface = font.render("SNAKE DRUNK LEVEL", True, grey)  # arg: text, antialias, color, background
        text_rect = text_surface.get_rect(center=(win_width_menu // 2, win_width_menu // 4))
        self.win.blit(text_surface, text_rect)

    def create_button(self):
        """
        Return a tuple containing three instances of subclass of Button
        Each instance corresponds to a difficulty level
        """
        button_easy = EasyButton(rect=[win_width_menu // 2 - 50, 200, 100, 50], text="SLOW REACTION")  # SLOW REACTION
        button_medium = MediumButton(rect=[win_width_menu // 2 - 50, 250, 100, 50], text="CONFUSION")  # CONFUSION
        button_hard = HardButton(rect=[win_width_menu // 2 - 50, 300, 100, 50], text="I'M FINEEEEEEE")  # ILLUSION

        return button_easy, button_medium, button_hard

    def start(self):
        """
        main while loop to keep the program running
        """
        while True:
            # set frame rate of the program. The program will never run at more than 50 frames per second
            self.clock.tick(50)

            # if mouse hover on a button, the color changes
            for button in self.buttons:
                button.button_text(self.win, pygame.mouse.get_pos())

            # using pygame.event.get() to get all the events happening in the program window
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for button in self.buttons:
                        if button.hover(pygame.mouse.get_pos()):
                            button.on_click()  # enter game

            pygame.display.update()


if __name__ == "__main__":
    menu = Menu()
    menu.start()
