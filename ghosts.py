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

class Pinky(Ghost):
    def __init__(self, group):
        super().__init__(11, 14, group)
        self.respawn_point = (11, 14)
        for direction, phases in list(self.images.items())[:-1]:
            if direction != 'EYES':
                for phase in phases.keys():
                    file_name = f'PINKY_{direction}_PHASE_{phase}.png'
                    self.images[direction][phase] = load_image(file_name, (0, 0, 0))

    def calculate_target_cell(self, packman_pos):
        if self.mode == 'HARASSMENT':
            # Для Pinky целью является клетка перед Пакманом
            x, y = packman_pos
            if self.parent_game.packman.direction == 'UP':
                return x, y - 4
            elif self.parent_game.packman.direction == 'DOWN':
                return x, y + 4
            elif self.parent_game.packman.direction == 'LEFT':
                return x - 4, y
            elif self.parent_game.packman.direction == 'RIGHT':
                return x + 4, y
            else:
                return self.get_position()
        elif self.mode == 'FRIGHT':
            next_steps = list(filter(lambda x: self.is_free(*x) and x != self.get_last_position(),
                                     map(lambda z: (self.x + z[0], self.y + z[1]), [(1, 0), (0, 1), (-1, 0), (0, -1)])))
            return choice(next_steps)
        else:
            return self.respawn_point

    def update(self, packman_pos):
        if self.find_path_step(self.get_position(), self.calculate_target_cell(packman_pos)) == self.get_position():
            return
        if not self.part_of_tile:
            self.move(self.calculate_target_cell(packman_pos))
        self.part_of_tile += -1 if self.direction in ('LEFT', 'UP') else 1
        if abs(self.part_of_tile) == 2:
            self.last_x, self.last_y = self.x, self.y
            self.x, self.y = self.next_x, self.next_y
            self.part_of_tile *= -1

        self.change_image(self.direction, self.part_of_tile % 2 + 1)


class Inky(Ghost):
    def __init__(self, group):
        super().__init__(choice([14, 13]), 14, group)
        self.respawn_point = (16, 14)
        for direction, phases in list(self.images.items())[:-1]:
            if direction != 'EYES':
                for phase in phases.keys():
                    file_name = f'INKY_{direction}_PHASE_{phase}.png'
                    self.images[direction][phase] = load_image(file_name, (0, 0, 0))

    def calculate_target_cell(self, packman_pos):
        if self.mode == 'HARASSMENT':
            # Для Inky целью является клетка, находящаяся на прямой линии от Пакмана до Blinky
            packman_x, packman_y = packman_pos
            blinky_x, blinky_y = self.parent_game.blinky.get_position()

            target_x = 2 * blinky_x - packman_x
            target_y = 2 * blinky_y - packman_y

            target_x = max(0, min(target_x, len(self.parent_game.board[0]) - 1))
            target_y = max(0, min(target_y, len(self.parent_game.board) - 1))

            return target_x, target_y
        elif self.mode == 'FRIGHT':
            next_steps = list(filter(lambda x: self.is_free(*x) and x != self.get_last_position(),
                                     map(lambda z: (self.x + z[0], self.y + z[1]), [(1, 0), (0, 1), (-1, 0), (0, -1)])))
            return choice(next_steps)
        else:
            return self.respawn_point

    def update(self, packman_pos):
        if self.find_path_step(self.get_position(), self.calculate_target_cell(packman_pos)) == self.get_position():
            return
        if not self.part_of_tile:
            self.move(self.calculate_target_cell(packman_pos))
        self.part_of_tile += -1 if self.direction in ('LEFT', 'UP') else 1
        if abs(self.part_of_tile) == 2:
            self.last_x, self.last_y = self.x, self.y
            self.x, self.y = self.next_x, self.next_y
            self.part_of_tile *= -1

        self.change_image(self.direction, self.part_of_tile % 2 + 1)


class Clyde(Ghost):
    def __init__(self, group):
        super().__init__(16, 14, group)
        self.respawn_point = (16, 14)
        for direction, phases in list(self.images.items())[:-1]:
            if direction != 'EYES':
                for phase in phases.keys():
                    file_name = f'CLYDE_{direction}_PHASE_{phase}.png'
                    self.images[direction][phase] = load_image(file_name, (0, 0, 0))

    def calculate_target_cell(self, packman_pos):
        if self.mode == 'HARASSMENT':
            # Для Clyde целью является Пакман, если расстояние больше 8 клеток, иначе - клетка возле дома
            packman_x, packman_y = packman_pos
            clyde_x, clyde_y = self.get_position()
            distance_to_pacman = abs(packman_x - clyde_x) + abs(packman_y - clyde_y)

            if distance_to_pacman > 8:
                return packman_pos
            else:
                return self.respawn_point
        elif self.mode == 'FRIGHT':
            next_steps = list(filter(lambda x: self.is_free(*x) and x != self.get_last_position(),
                                     map(lambda z: (self.x + z[0], self.y + z[1]), [(1, 0), (0, 1), (-1, 0), (0, -1)])))
            return choice(next_steps)
        else:
            return self.respawn_point

    def update(self, packman_pos):
        if self.find_path_step(self.get_position(), self.calculate_target_cell(packman_pos)) == self.get_position():
            return
        if not self.part_of_tile:
            self.move(self.calculate_target_cell(packman_pos))
        self.part_of_tile += -1 if self.direction in ('LEFT', 'UP') else 1
        if abs(self.part_of_tile) == 2:
            self.last_x, self.last_y = self.x, self.y
            self.x, self.y = self.next_x, self.next_y
            self.part_of_tile *= -1

        self.change_image(self.direction, self.part_of_tile % 2 + 1)
