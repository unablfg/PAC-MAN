from load_image_function import load_image
import pygame
from game_sizes import CELL_SIZE, TOP_MARGIN


# Класс фруктов
class Fruits(pygame.sprite.Sprite):
    fruits_data = [{'image': load_image('CHERRY.png'),
                    'points': 100},
                   {'image': load_image('STRAWBERRY.png'),
                    'points': 300},
                   {'image': load_image('ORANGE.png'),
                    'points': 500}]

    def __init__(self, x, y, sort, group):
        super().__init__(group)
        self.image = Fruits.fruits_data[sort]['image']
        self.points = Fruits.fruits_data[sort]['points']
        self.rect = self.image.get_rect()
        self.rect.x = x * CELL_SIZE
        self.rect.y = y * CELL_SIZE + TOP_MARGIN
