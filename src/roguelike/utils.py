import os
import pygame
from roguelike.consts import *

"""雑多なツール類"""
class Utils:
    def __init__():
        pass

    def load_image(file):
        file = os.path.join(IMG_DIR, file)
        try:
            surface = pygame.image.load(file)
        except pygame.error:
            raise SystemExit('Could not load image "%s" %s' %(file, pygame.get_error()))
        return surface
