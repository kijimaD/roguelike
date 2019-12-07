from mock import Mock
from roguelike.main import Game
from roguelike.plot import Plot
from roguelike.msg_engine import MessageEngine
from roguelike.consts import *
import pytest
import pygame


class TestGame:

    game = Game()
    msg_engine = MessageEngine()
    # TODO: メソッドからグローバル変数にアクセスする方法がわからない。
    # アクセスできないとメソッドを実行できない。

    def test_title_handler(self):
        """タイトルハンドラのテスト
        """
        # mockは、DBとかWEB、日付で使うもので。
        # self.game.event = Mock(type=self.KEYDOWN, key=self.K_1)

        # キー入力か、イベントを用意できれば、メソッドをテストできると思う。あらかじめ用意しておいて、メソッドがどう動くかみればいい。
        # self.game.event.type = 'K_1'
        pass

    def test_game_counter_range(self):
        """ゲームカウンタの範囲チェック
        """
        assert self.game.game_counter(0) == 1
        assert self.game.game_counter(1) == 2
        assert self.game.game_counter(100) == 0

    def test_var_access(self):
        """
        """
        pass
