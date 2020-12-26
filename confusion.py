import random
import pygame
from pygame.locals import *
import sys

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


def draw_window(win, snake, snack):

    # fill the surface with black
    win.fill((0, 0, 0))
    snake.draw(win)
    # snack is a Cube object
    snack.draw(win)
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
        x = random.randrange(rows)  # return int, stop before rows
        y = random.randrange(rows)  # return int
        if len(list(filter(lambda z: z.pos == (x, y), positions))) > 0:  # filter(lambda function, list) -
            # use lambda function to filter the list
            continue
        else:
            break
    return x, y


def collision(snake):
    # detect collisions, some issues
    pos_snake_head = snake.body[0].pos
    pos_snake_w_o_head = [cube.pos for cube in snake.body[1:]]

    if pos_snake_head in pos_snake_w_o_head:
        snake.reset()


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
    snack = Cube(pos=random_pos(rows, snake.body), color=snack_color)

    temp_direction = [1, 0]
    confusion_count = 0

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
                    print("hahah")
                    # import intro
                    # intro.main()
                if event.key == K_r:
                    snake.reset()
                if event.key == K_UP or event.key == K_DOWN or event.key == K_LEFT or event.key == K_RIGHT:
                    confusion_count += 1
                    if event.key == K_UP:
                        temp_direction = [0, -1]
                    elif event.key == K_DOWN:
                        temp_direction = [0, 1]
                    elif event.key == K_LEFT:
                        temp_direction = [-1, 0]
                    elif event.key == K_RIGHT:
                        temp_direction = [1, 0]

        # handle player input
        if confusion_count % 1 == 0:
            direction = [-i for i in temp_direction]
        else:
            direction = temp_direction


        grow = snake.move(direction, snack)

        if grow is True:
            snack = Cube(pos=random_pos(rows, snake.body), color=snack_color)

        snake.collision()

        # draw everything
        draw_window(win, snake, snack)

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
