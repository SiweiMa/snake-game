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
snake_initial_pos = (rows//2, rows//2)
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
        self.direction = (1, 0)

    def move(self, direction, grow,):
        self.direction = direction
        added_head = Cube(pos=(self.body[0].pos[0] + self.direction[0], self.body[0].pos[1] + self.direction[1]),
                          color=self.color)
        self.body.insert(0, added_head)

        print('before', self.body[0].pos)

        for cube in self.body:
            if cube.pos[0] > rows:
                cube.pos = (0, cube.pos[1])
            if cube.pos[0] < 0:
                cube.pos = (rows, cube.pos[1])
            if cube.pos[1] > rows:
                cube.pos = (cube.pos[0], 0)
            if cube.pos[1] < 0:
                cube.pos = (cube.pos[0], rows)

        print('after', self.body[0].pos)
        
        if grow is False:
            self.body.pop()

    def reset(self):
        self.body = []
        self.body.append(Cube(pos=snake_initial_pos, color=snake_color))
        # self.direction = (1,0)

    def draw(self, win):
        # draw the eye of snake
        for i, c in enumerate(self.body):
            if i == 0:
                c.draw(win, True)
            else:
                c.draw(win)

# def draw_grid(win_width, rows, surface):
#     size_between = win_width // rows
#
#     x = 0
#     y = 0
#
#     for l in range(rows):
#         x = x + size_between
#         y = y + size_between
#
#         pygame.draw.line(surface, (255, 255, 255), (x, 0), (x, win_width))
#         pygame.draw.line(surface, (255, 255, 255), (0, y), (win_width, y))


def draw_window(win, snake, snack):
    # fill the surface with black
    win.fill((0, 0, 0))
    snake.draw(win)
    # snack is a Cube object
    snack.draw(win)
    # draw_grid(win_width, rows, win)
    pygame.display.update()


def random_pos(rows, snake):
    positions = snake.body  # snake.body is list with elements of cube

    while True:
        x = random.randrange(rows)  # return int, stop before rows
        y = random.randrange(rows)  # return int
        if len(list(filter(lambda z: z.pos == (x, y), positions))) > 0:  # filter(lambda function, list) -
            # use lambda function to filter the list
            continue
        else:
            break
    return x, y


def main():
    # global win_width, rows, s, snack
    # initialization
    win = pygame.display.set_mode((win_width, win_width))
    pygame.display.set_caption("Level 1")

    # prepare game objects
    clock = pygame.time.Clock()
    # snake color = red, position = 10,10
    snake = Snake(pos=snake_initial_pos, color=snake_color)
    # random_snack(rows, s) return x,y coordinate
    snack = Cube(pos=random_pos(rows, snake), color=snack_color)
    direction = (1, 0)
    temp_direction = (1, 0)
    delay_countdown = 0

    # main loop
    while True:
        clock.tick(5)
        pygame.time.delay(50)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                # import intro
                # intro.main()
                print("haha")
            elif event.type == KEYDOWN and event.key == K_r:
                snake.reset()
            elif event.type == KEYDOWN and event.key == K_UP:
                temp_direction = (0, -1)
                delay_countdown = 5
            elif event.type == KEYDOWN and event.key == K_DOWN:
                temp_direction = (0, 1)
                delay_countdown = 5
            elif event.type == KEYDOWN and event.key == K_LEFT:
                temp_direction = (-1, 0)
                delay_countdown = 5
            elif event.type == KEYDOWN and event.key == K_RIGHT:
                temp_direction = (1, 0)
                delay_countdown = 5

        # detect eating snack
        if snake.body[0].pos == snack.pos:
            grow = True
            snack = Cube(pos=random_pos(rows, snake), color=snack_color)
        else:
            grow = False

        # detect collisions, some issues
        for x in range(len(snake.body)):
            if snake.body[x].pos in list(map(lambda z: z.pos, snake.body[x + 1:])):
                print('Score:', len(snake.body))
                snake.reset()
                break

        # handle player input
        if delay_countdown > 0:
            delay_countdown -= 1
        else:
            direction = temp_direction

        snake.move(direction, grow)

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
