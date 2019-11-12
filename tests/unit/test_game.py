# coding: utf-8

from roguelike import Game
import pytest

class TestGame:
    game = Game()
    def test_game(self):
        """"""
        t_1 = "1"
        t_2 = "1"
        assert t_1 == t_2

    def test_update(self):
        """"""
        pass

    def test_file_input_char(self):
        """"""
        assert len(str(self.game.root)) > 0