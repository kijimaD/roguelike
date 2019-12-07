from mock import Mock
from mock import MagicMock
from roguelike.main import Game
from roguelike.msg_engine import MessageEngine
from roguelike.plot import Plot
from roguelike.consts import *

class TestPlot(object):
    msg_engine = MessageEngine()

    def test_opening(self):
        """正しいgame_stateを返すことを確認
        """

        self.plot_count = 0

        root = self.msg_engine.file_input()

        test = Plot.opening(self, root)
        right = FULLTEXT

        assert test == right
