import pygame
from roguelike import Window
from pygame.locals import *

class WindowText(Window):
    """通常のウィンドウメッセージ"""
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

    def draw_left_character(self, screen):
        """人物モデル（左）"""
        pygame.draw.circle(screen, (255, 0, 0), (120, 140), 40)

    def draw_right_character(self, screen):
        """人物モデル（右）"""
        pygame.draw.circle(screen, (0, 0, 255), (520, 140), 40)

    def draw_left_bubble(self, screen):
        """吹き出し（左）"""
        pygame.draw.line(screen, (0, 0, 0), (260, 260), (220, 220), 3)
        pygame.draw.line(screen, (0, 0, 0), (220, 220), (180, 220), 3)

    def draw_right_bubble(self, screen):
        """吹き出し（右）"""
        pygame.draw.line(screen, (0, 0, 0), (380, 260), (420, 220), 3)
        pygame.draw.line(screen, (0, 0, 0), (420, 220), (460, 220), 3)
