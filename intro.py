import pygame
import sys
import illusion
import confusion
import tipsy_V3


# set some colors in RGB
black = (0, 0, 0)
grey = (224, 224, 224)
white = (255, 255, 255)
light_yellow = (255, 255, 153)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
win_width = 500


# class name should be singular
class Button:
    def __init__(self, rect, text="", default_color=grey, hovered_color=light_yellow):
        # Rect(left, top, width, height)
        self.rect = pygame.Rect(rect)

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


def response_easy():
    tipsy_V3.main()


def response_medium():
    confusion.main()


def response_hard():
    illusion.main()


def main():
    # initialize pygame
    pygame.init()
    # create a display Surface with size of 500 pixel * 500 pixel
    win = pygame.display.set_mode(size=(win_width, win_width))
    # set caption of window
    pygame.display.set_caption("Drunk Snake")
    # set logo
    icon = pygame.image.load('snake.png')
    pygame.display.set_icon(icon)
    # create a clock object that can be used to track time
    clock = pygame.time.Clock()

    # in oder to create text_surface (surface is an object),
    # we need to set font at first
    font = pygame.font.Font(None, 50)
    # render creates a new Surface with "How drunk is snake" rendered on it.
    text_surface = font.render("SNAKE DRUNK LEVEL", True, grey)  # arg: text, antialias, color, background
    # get the rectangular area of the surface
    text_rect = text_surface.get_rect()
    text_rect.center = (win_width // 2, win_width // 4)
    # draw text_surface on win. The position of text_surface is provided by a Rect (object?)
    # for all surface object, text_surface in this case, we need to blit it with an coordinate
    win.blit(text_surface, text_rect)

    # setup button
    button_easy = Button(rect=[win_width // 2 - 50, 200, 100, 50], text="SLOW REACTION") #SLOW REACTION
    button_medium = Button(rect=[win_width // 2 - 50, 250, 100, 50], text="CONFUSION") #CONFUSION
    button_hard = Button(rect=[win_width // 2 - 50, 300, 100, 50], text="I'M FINEEEEEEE") # ILLUSION

    buttons = [
        {
            "button": button_easy,
            "func": response_easy
        },
        {
            "button": button_medium,
            "func": response_medium
        },
        {
            "button": button_hard,
            "func": response_hard
        }
    ]

    # main loop
    # using while loop to keep the program running
    # flag = True # unnecessary as you can just use "break" to exit the loop.
    while True:
        # set frame rate of the program
        # the program will never run at more than 50 frames per second
        clock.tick(50)

        for button in buttons:
            button["button"].button_text(win, pygame.mouse.get_pos())

        # using pygame.event.get() to get all the events happening in the program window
        for event in pygame.event.get():
            # we can quit the program if we press close button of window
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for button in buttons:
                    if button["button"].hover(pygame.mouse.get_pos()):
                        button["func"]() # enter game

        pygame.display.update()  # everytime use win's function, need to update


# ---------------------------------------------------------------------------------------------------------------------#
if __name__ == "__main__":
    main()
