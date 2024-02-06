import pygame
from game_sizes import CELL_SIZE, TOP_MARGIN


# Класс стенки
class Border:
    def __init__(self, x, y):
        self.x = x
        self.y = y


# Класс вертикальной стенки
class VerticalBorder(Border):
    def __init__(self, x, y):
        super().__init__(x, y)

    # Отрисовка стенки
    def draw(self, screen):
        pygame.draw.rect(screen, (50, 18, 122),
                         (self.x * CELL_SIZE + 6, self.y * CELL_SIZE + TOP_MARGIN, 12, CELL_SIZE))


# Класс горизонтальной стенки
class HorizontalBorder(Border):
    def __init__(self, x, y):
        super().__init__(x, y)

    # Отрисовка стенки
    def draw(self, screen):
        pygame.draw.rect(screen, (50, 18, 122),
                         (self.x * CELL_SIZE, self.y * CELL_SIZE + 6 + TOP_MARGIN, CELL_SIZE, 12))


class RoundedBorder(Border):
    def __init__(self, x, y, rounded_corner):
        super().__init__(x, y)
        self.rounded_corner = rounded_corner
        # 1 - правый верхний, 2 - правый нижний, 3 - левый нижний, 4 - левый верхний
        self.btlr = 0  # border_top_left_radius
        self.btrr = 0  # border_top_right_radius
        self.bblr = 0  # border_bottom_left_radius
        self.bbrr = 0  # border_bottom_right_radius
        if self.rounded_corner == 1:
            self.btrr = 18
            self.delta_y = 6
            self.delta_x = 0
        elif self.rounded_corner == 2:
            self.bbrr = 18
            self.delta_y = 0
            self.delta_x = 0
        elif self.rounded_corner == 3:
            self.bblr = 18
            self.delta_y = 0
            self.delta_x = 6
        elif self.rounded_corner == 4:
            self.btlr = 18
            self.delta_y = 6
            self.delta_x = 6

    # Отрисовка стенки
    def draw(self, screen):
        pygame.draw.rect(screen, (50, 18, 122),
                         (self.x * CELL_SIZE + self.delta_x, self.y * CELL_SIZE + self.delta_y + TOP_MARGIN,
                          18, 18),
                         border_top_left_radius=self.btlr, border_top_right_radius=self.btrr,
                         border_bottom_left_radius=self.bblr, border_bottom_right_radius=self.bbrr)
        pygame.draw.rect(screen, (0, 0, 0),
                         (self.x * CELL_SIZE + self.delta_x * 3, self.y * CELL_SIZE + self.delta_y * 3 + TOP_MARGIN,
                          6, 6),
                         border_top_left_radius=self.btlr // 3, border_top_right_radius=self.btrr // 3,
                         border_bottom_left_radius=self.bblr // 3, border_bottom_right_radius=self.bbrr // 3)
