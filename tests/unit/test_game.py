# coding: utf-8

from roguelike import Game
import pytest

class TestGame:
    game = Game()
    
    def test_update(self):
        """"""
        pass

    def test_game_counter_range(self):
        """ゲームカウンタの範囲チェック"""
        assert self.game.game_count >= 0
        assert self.game.game_count <= 100

    def test_file_input_char(self):
        """入力ファイルの文字数チェック"""
        assert len(str(self.game.root)) > 0