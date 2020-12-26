import random
import pygame
from pygame.locals import *
import sys
import loan_main

# set some colors in RGB
grey = (224, 224, 224)
light_yellow = (255, 255, 153)
black = (0, 0, 0)
# some game constant
win_width = 800
rows = 40
dis = win_width // rows
snake_initial_pos = (rows // 2, rows // 2)
snake_color = grey
snack_color = light_yellow


class Cube(object):
    # s.head instance pass in position of (10,10) tuple as start
    def __init__(self, pos, color):
        self.pos = pos
        self.color = color

    def draw(self, win, eyes=False):
        x_row = self.pos[0]
        y_row = self.pos[1]
        # 3rd argument (left,top, width, height), for example i*dis+1: left line's x coordinate in pixel
        pygame.draw.rect(win, self.color,
                         (x_row * dis, y_row * dis, dis, dis))  # arg: surface object, color, coordinate

        if eyes:
            centre = dis // 2
            radius = 3
            circle_middle1 = (x_row * dis + centre - radius, y_row * dis + 8)
            circle_middle2 = (x_row * dis + dis - radius * 2, y_row * dis + 8)
            pygame.draw.circle(win, (0, 0, 0), circle_middle1, radius)
            pygame.draw.circle(win, (0, 0, 0), circle_middle2, radius)


class Snake(object):
    # s instance pass in red color and position of (10,10) tuple.
    def __init__(self, pos, color):
        self.body = []  # self.body = [].append(self.head) no!!!
        self.body.append(Cube(pos, color))
        self.color = color
        self.score = 1

    def move(self, direction, snack):

        added_head = Cube(pos=(self.body[0].pos[0] + direction[0], self.body[0].pos[1] + direction[1]),
                          color=self.color)
        self.body.insert(0, added_head)

        # detect eating snack
        grow = False
        if self.body[0].pos != snack.pos:
            self.body.pop()
        else:
            grow = True
            self.score += 1

        # screen wrapping
        for cube in self.body:
            if cube.pos[0] > rows-1:
                cube.pos = (0, cube.pos[1])
            if cube.pos[0] < 0:
                cube.pos = (rows-1, cube.pos[1])
            if cube.pos[1] > rows-1:
                cube.pos = (cube.pos[0], 0)
            if cube.pos[1] < 0:
                cube.pos = (cube.pos[0], rows-1)

        return grow

    def collision(self):
        # detect collisions, some issues
        pos_snake_head = self.body[0].pos
        pos_snake_w_o_head = [cube.pos for cube in self.body[1:]]

        if pos_snake_head in pos_snake_w_o_head:
            self.reset()

    def reset(self):
        self.body = []
        self.body.append(Cube(pos=snake_initial_pos, color=snake_color))
        self.score = 1

    def draw(self, win):
        # draw the eye of snake
        for i, c in enumerate(self.body):
            if i == 0:
                c.draw(win, True)
            else:
                c.draw(win)


def draw_grid(win_width, rows, surface):
    size_between = win_width // rows

    x = 0
    y = 0

    for l in range(rows):
        x = x + size_between
        y = y + size_between

        pygame.draw.line(surface, (96, 96, 96), (x, 0), (x, win_width))
        pygame.draw.line(surface, (96, 96, 96), (0, y), (win_width, y))


def draw_window(win, snake, snack, fake_snacks):

    # fill the surface with black
    win.fill((0, 0, 0))
    snake.draw(win)
    # snack is a Cube object
    snack.draw(win)

    for fake_snack in fake_snacks:
        fake_snack.draw(win)

    draw_grid(win_width, rows, win)

    f = pygame.font.Font(None, 50)
    g = f.render('Score: '+str(snake.score), True, grey)
    win.blit(g, (600, 50))

    pygame.display.update()


def random_pos(rows, positions):
    """
    :param rows: total rows of win
    :param positions: snake.body which is list with elements of cube
    :return: random x,y row number
    """

    while True:
        x = random.sample(range(rows), 5)  # return list, stop before rows
        y = random.sample(range(rows), 5)   # return list
        zip_x_y = list(zip(x, y))
        for item in zip_x_y:
            if len(list(filter(lambda z: z.pos == item, positions))) > 0:  # filter(lambda function, list) -
                # use lambda function to filter the list
                break
        else:
            return zip_x_y


def main():
    # global win_width, rows, s, snack
    # initialization
    win = pygame.display.set_mode((win_width, win_width))
    pygame.display.set_caption("Level 2")

    # prepare game objects
    clock = pygame.time.Clock()
    # snake color = red, position = 10,10
    snake = Snake(pos=snake_initial_pos, color=snake_color)
    # random_snack(rows, s) return x,y coordinate
    snack_pos = random_pos(rows, snake.body)[0]
    snack = Cube(pos=snack_pos, color=snack_color)

    fake_snack_poss = random_pos(rows, snake.body)[1:]
    fake_snacks = [Cube(pos=fake_snack_pos, color=snack_color) for fake_snack_pos in fake_snack_poss]

    temp_direction = [1, 0]

    # main loop
    while True:
        clock.tick(5)
        pygame.time.delay(50)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    loan_main.load()
                if event.key == K_r:
                    snake.reset()
                if event.key == K_UP:
                    temp_direction = (0, -1)
                if event.key == K_DOWN:
                    temp_direction = (0, 1)
                if event.key == K_LEFT:
                    temp_direction = (-1, 0)
                if event.key == K_RIGHT:
                    temp_direction = (1, 0)

        direction = temp_direction

        grow = snake.move(direction, snack)

        if grow is True:
            snack_pos = random_pos(rows, snake.body)[0]
            snack = Cube(pos=snack_pos, color=snack_color)
            fake_snack_poss = random_pos(rows, snake.body)[1:]
            fake_snacks = [Cube(pos=fake_snack_pos, color=snack_color) for fake_snack_pos in fake_snack_poss]

        snake.collision()

        # draw everything
        draw_window(win, snake, snack, fake_snacks)

    # handles 'play again' situation
    # end = 1
    # while end:
    #     event = pygame.event.wait()
    #     if event.type == QUIT:
    #         end = 0
    #     if event.type != KEYDOWN:
    #         continue
    #     if event.key == K_ESCAPE:
    #         end = 0
    #     elif event.key == K_n:
    #         end = 0
    #     elif event.key == K_y:
    #         main(1)
