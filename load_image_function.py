import os
import pygame

pygame.init()


def load_image(name, colorkey=None):
    fullname = os.path.join('images', name)
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = pygame.image.load(fullname)
    return image
