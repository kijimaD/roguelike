import os
import pygame
import pygame.mixer
from roguelike.consts import *

"""
ツール類
"""


class Utils:
    def __init__():
        pass

    def load_image(file):
        """例外処理を組み込んだload
        """
        file = os.path.join(IMG_DIR, file)
        try:
            surface = pygame.image.load(file)
        except pygame.error:
            raise SystemExit('Could not load image "%s" %s' % (file, pygame.get_error()))
        return surface

    def load_images(*files):
        """複数の画像読み込み
        """
        imgs = []
        for file in files:
            imgs.append(load_image(file))
        return imgs

    def load_sound(file):
        """例外処理を組み込んだload。※wavしか再生できない。
        musicとの違いは、先に読み込んでおくかの違い。soundは短く使用頻度が高いのでメモリに読み込んで、好きなときに使う。なので読み込みと再生が分離する。これはloadするだけ。
        """
        file = os.path.join(SOUND_DIR, file)
        try:
            sound = pygame.mixer.Sound(file)
            return sound
        except pygame.error:
            raise SystemExit('Cound not load sound "%s" %s' % (file, pygame.get_error()))

    def play_bgm(file):
        """ファイルから読み込み、BGMを再生する。soundとは異なり、逐次読み込んで使う。読み込み＋再生。
        """
        file = os.path.join(BGM_DIR, file)
        try:
            pygame.mixer.music.load(file)
        except pygame.error:
            raise SystemExit('Cound not load sound "%s" %s' % (file, pygame.get_error()))
        pygame.mixer.music.play(-1)
