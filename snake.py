import pygame
from constant import *

class Cube(object):
    def __init__(self, pos, color):
        """
        :param pos: a tuple of row number pair
        :param color: color of a cube
        """
        self.pos = pos
        self.color = color

    def draw(self, win, eyes=False):
        """
        Draw cube on Surface win. If eyes is True, draw eyes on cube
        """
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
    def __init__(self, pos, color):
        """
        Attributes:
            body: a list of Cube instances. The initial body has only one cube
            color: snake color
            score: the length of body. The initial score is 1.
        """
        self.body = []  # self.body = [].append(self.head) no!!!
        self.body.append(Cube(pos, color))
        self.color = color
        self.score = 1

    def move(self, direction, snack):
        """
        To move the snake, we simply add cube in the moving direction as new head and drop the last cube in body
        Return grow as a boolean value
        """
        added_head = Cube(pos=(self.body[0].pos[0] + direction[0], self.body[0].pos[1] + direction[1]),
                          color=self.color)
        self.body.insert(0, added_head)

        # detect eating snack. If snake eats a snack, set grow as True
        grow = False
        if self.body[0].pos != snack.pos:
            self.body.pop()
        else:
            grow = True
            self.score += 1

        # screen wrapping which means no walls in the game
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
        pos_snake_head = self.body[0].pos
        pos_snake_w_o_head = [cube.pos for cube in self.body[1:]]

        if pos_snake_head in pos_snake_w_o_head:
            self.reset()

    def reset(self):
        self.body = []
        self.body.append(Cube(pos=snake_initial_pos, color=self.color))
        self.score = 1

    def draw(self, win):
        # draw the eye of snake
        for i, c in enumerate(self.body):
            if i == 0:
                c.draw(win, True)
            else:
                c.draw(win)

