import pygame
from load_image_function import load_image
from game_sizes import CELL_SIZE, TOP_MARGIN
from random import choice


class PackMan(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        self.parent_game = None
        self.x = choice([13, 14])
        self.y = 23
        self.boost_mode = False
        self.direction = 'STOP'  # Направление движения Пакмана
        self.last_direction = 'STOP'
        self.images = {'DOWN': {1: load_image('PACKMAN_DOWN_PHASE_1.png', (0, 0, 0)),
                                2: load_image('PACKMAN_DOWN_PHASE_2.png', (0, 0, 0))},
                       'UP': {1: load_image('PACKMAN_UP_PHASE_1.png', (0, 0, 0)),
                              2: load_image('PACKMAN_UP_PHASE_2.png', (0, 0, 0))},
                       'LEFT': {1: load_image('PACKMAN_LEFT_PHASE_1.png', (0, 0, 0)),
                                2: load_image('PACKMAN_LEFT_PHASE_2.png', (0, 0, 0))},
                       'RIGHT': {1: load_image('PACKMAN_RIGHT_PHASE_1.png', (0, 0, 0)),
                                 2: load_image('PACKMAN_RIGHT_PHASE_2.png', (0, 0, 0))},
                       'STOP': load_image('PACKMAN_PHASE_0.png', (0, 0, 0))}
        self.image = self.images['STOP']
        self.part_of_tile = 0
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x * CELL_SIZE, self.y * CELL_SIZE + TOP_MARGIN)

    def change_image(self, direction, phase=None):
        if direction == 'STOP':
            self.image = self.images[direction]
        else:
            self.image = self.images[direction][phase]
        self.rect.topleft = (self.x * CELL_SIZE + self.part_of_tile * (6 if self.direction in ('RIGHT', 'LEFT') else 0),
                             self.y * CELL_SIZE + self.part_of_tile * (
                                 6 if self.direction in ('UP', 'DOWN') else 0) + TOP_MARGIN)

    def update(self):
        if self.direction != 'STOP':
            if not self.part_of_tile and not self.is_free(*self.next_cell(self.direction)):
                self.direction = 'STOP'
                self.change_image(self.direction)
                return
            self.part_of_tile += 1 if self.direction in ('DOWN', 'RIGHT') else -1
            if self.part_of_tile in (-1, 4):
                self.x, self.y = self.next_cell(self.direction)
                self.part_of_tile = 0 if self.part_of_tile == 4 else 3
            self.change_image(self.direction, self.part_of_tile % 2 + 1)

    def change_direction(self, direction):
        if (direction == 'STOP' or self.is_free(*self.next_cell(direction))) and not self.part_of_tile:
            self.last_direction = self.direction
            self.direction = direction

    def get_position(self):
        return self.x, self.y

    def is_free(self, x, y):
        if x < 0 or y < 0 or x >= len(self.parent_game.board[0]) or y >= len(self.parent_game.board):
            return False
        return self.parent_game.board[y][x] < 3

    def next_cell(self, direction=None):
        movements = {'RIGHT': (1, 0),
                     'LEFT': (-1, 0),
                     'UP': (0, -1),
                     'DOWN': (0, 1)}
        if direction is None:
            direction = self.direction
        if direction == 'RIGHT' and self.get_position() == (27, 14):
            new_x = 0
        elif direction == 'LEFT' and self.get_position() == (0, 14):
            new_x = 27
        else:
            new_x = self.x + movements[direction][0]
        new_y = self.y + movements[direction][1]
        return new_x, new_y
