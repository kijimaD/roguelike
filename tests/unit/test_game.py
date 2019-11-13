# coding: utf-8

from roguelike import Game
import pytest

class TestGame:
    game = Game()

    # TODO: インスタンス変数？を検証してもユニットテストとは言えないのではないか？

    def test_update(self):
        """"""
        pass

    def test_game_counter_range(self):
        """ゲームカウンタの範囲チェック"""
        # TODO: ユニットテストではない！
        assert self.game.game_count >= 0
        assert self.game.game_count <= 100

    def test_file_input_char(self):
        """ファイル入力を文字数でチェック"""
        root = self.game.file_input()
        assert len(str(root)) > 0