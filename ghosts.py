import pygame
from load_image_function import load_image
from game_sizes import CELL_SIZE, TOP_MARGIN


class Ghost(pygame.sprite.Sprite):
    def __init__(self, x, y, group):
        super().__init__(group)
        self.parent_game = None
        self.x = x
        self.y = y
        self.last_x = x
        self.last_y = y
        self.mode = 'HARASSMENT'  # 'HARASSMENT' - преследование; 'RETURNING_HOME' - возвращение домой;
        # 'FRIGHT' - испуг
        self.part_of_tile = 0
        self.images = {'DOWN': {1: None, 2: None},
                       'UP': {1: None, 2: None},
                       'LEFT': {1: None, 2: None},
                       'RIGHT': {1: None, 2: None},
                       'EYES': {'DOWN': load_image('EYES_DOWN.png', (0, 0, 0)),
                                'UP': load_image('EYES_UP.png', (0, 0, 0)),
                                'LEFT': load_image('EYES_LEFT.png', (0, 0, 0)),
                                'RIGHT': load_image('EYES_RIGHT.png', (0, 0, 0))},
                       'FRIGHT': {1: load_image('FRIGHT_PHASE_1.png', (0, 0, 0)),
                                  2: load_image('FRIGHT_PHASE_2.png', (0, 0, 0))}}

    def change_image(self, direction, phase):
        if self.mode == 'FRIGHT':
            self.image = self.images['FRIGHT'][phase]
        elif self.mode == 'RETURNING_HOME':
            self.image = self.images['EYES'][direction]
        else:
            self.image = self.images[direction][phase]
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        if direction in ('DOWN', 'UP'):
            self.rect.y = self.y * CELL_SIZE + self.part_of_tile * 6 + TOP_MARGIN
            self.rect.x = self.x * CELL_SIZE
        else:
            self.rect.x = self.x * CELL_SIZE + self.part_of_tile * 6
            self.rect.y = self.y * CELL_SIZE + TOP_MARGIN

    def get_position(self):
        return self.x, self.y

    def get_last_position(self):
        return self.last_x, self.last_y
