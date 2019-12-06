import pygame
from roguelike import Window
from pygame.locals import *

class WindowText(Window):
    """通常のウィンドウメッセージ
    """
    EDGE_WIDTH = 4

    def __init__(self, rect, msg_engine):
        Window.__init__(self, rect)
        self.msg_engine = msg_engine
        self.cur_pos = 0
        self.blitx = 10
        self.blity = 260

    def draw_unify(self, screen, set_data, set_script_data, game_count):
        self.draw_msg(screen, set_data, set_script_data, game_count)
        pygame.draw.rect(screen, (255, 255, 255), Rect(10, 260, 620, 200), 3)
