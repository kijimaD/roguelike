import pygame.mixer
from roguelike.utils import Utils
from roguelike.consts import *

class Plot:
    def __init__(self, msg_engine):
        self.msg_engine = msg_engine
        self.plot_count = 0

    def opening(self, root):
        """オープニング。
        """
        game_state = 0
        if self.plot_count == 0:
            game_state = FULLTEXT
            self.msg_engine.set(root, 'monologue0')
        elif self.plot_count == 1:
            game_state = WINDOWTEXT
            self.msg_engine.set(root, 'intro0')
        # elif self.plot_count == 2:
        #     game_state = COMMAND
        #     self.msg_engine.set(root, 'intro0')
        else:
            self.plot_count = 0
        return game_state
