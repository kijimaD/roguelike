import pygame
from pygame.locals import *
import os

SCREEN = Rect(0, 0, 640, 480)
SCR_W = 640
SCR_H = 320
TITLE, WINDOWTEXT, FIELD, FULLTEXT, COMMAND = range(5)
DEFAULT_FONT = "Ricty Diminished Discord"
run_dir = os.path.split(os.path.abspath(__file__))[0]
HOME_DIR = os.path.join(run_dir, '../../')
IMG_DIR = os.path.join(HOME_DIR , "img")
TEXT_DIR = os.path.join(HOME_DIR , "data")
