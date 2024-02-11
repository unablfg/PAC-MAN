from load_image_function import load_image
import pygame
from game_sizes import CELL_SIZE, TOP_MARGIN


# Класс энерджайзера
class Boost(pygame.sprite.Sprite):
    image = load_image('BOOST.png')

    def __init__(self, x, y, group):
        super().__init__(group)
        self.image = Boost.image
        self.rect = self.image.get_rect()
        self.rect.x = x * CELL_SIZE + 4
        self.rect.y = y * CELL_SIZE + 4 + TOP_MARGIN
