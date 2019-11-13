# coding: utf-8

from mock import Mock
from roguelike import Game
import pytest


class TestGame:

    game = Game()

    @pytest.fixture()
    def file(self):
        pass

    def test_update(self):
        """"""
        pass

    def test_game_counter_range(self):
        """ゲームカウンタの範囲チェック"""
        # TODO: ユニットテストではない！
        # インスタンス変数？を検証してもユニットテストとは言えないのではないか？メソッドではなく変数をチェックしている
        assert self.game.game_count == 0
        self.game.game_counter()
        assert self.game.game_count == 1

    def test_file_input_char(self):
        """ファイル入力を文字数でチェック"""
        root = self.game.file_input()
        assert len(str(root)) > 0