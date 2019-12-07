import pygame
from pygame.locals import *
import os

CHOICE_MODE = 0
SCREEN = Rect(0, 0, 640, 480)
SCR_W = 640
SCR_H = 320
TITLE, WINDOWTEXT, FIELD, FULLTEXT, COMMAND = range(5)
DEFAULT_FONT = "Ricty Diminished Discord"
run_dir = os.path.split(os.path.abspath(__file__))[0]  # パッケージから呼び出すとおかしくなる
# HOME_DIR = os.path.join(run_dir, '../../')
HOME_DIR = os.path.join("/home/kijima/roguelike")  # FIXME: パッケージとプロジェクトのディレクトリが異なるので、テストと実行の両立ができない。暫定こうしておく！
TEXT_DIR = os.path.join(HOME_DIR , "data", "text")
IMG_DIR = os.path.join(HOME_DIR , "data", "img")
SOUND_DIR = os.path.join(HOME_DIR , "data", "sound")
BGM_DIR = os.path.join(HOME_DIR , "data", "music")
