from load_image_function import load_image
import pygame
from game_sizes import CELL_SIZE, TOP_MARGIN


# Класс монетки
class Coin(pygame.sprite.Sprite):
    image = load_image('COIN.png')

    def __init__(self, x, y, group):
        super().__init__(group)
        self.image = Coin.image
        self.rect = self.image.get_rect()
        self.rect.x = x * CELL_SIZE + 10
        self.rect.y = y * CELL_SIZE + 10 + TOP_MARGIN
