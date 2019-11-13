# coding: utf-8

from mock import Mock
from roguelike import Game
import pytest
import pygame

class TestGame:

    game = Game()
    # TODO: メソッドからグローバル変数にアクセスする方法がわからない。
    # アクセスできないとメソッドを実行できない。

    @pytest.fixture()
    def file(self):
        pass

    def test_update(self):
        """"""
        pass
    
    def test_check_event(self):
        """ハンドラのテスト"""
        pass

    def test_title_handler(self):
        """タイトルハンドラのテスト"""
        # イベントをmockできればいい。イベントキューに入れて、それからget()すればエミュレートできる。…そういうものじゃない気もするな。
        # mockは、DBとかWEB、日付で使うもので。
        # self.game.event = Mock(type=self.KEYDOWN, key=self.K_1)

        # キー入力か、イベントを用意できれば、メソッドをテストできると思う。あらかじめ用意しておいて、メソッドがどう動くかみればいい。
        # self.game.event.type = 'K_1'

    def test_game_counter_range(self):
        """ゲームカウンタの範囲チェック"""
        # テストしやすい！こういう風に書く。テストというよりテストしやすいメソッドにする！
        assert self.game.game_counter(0) == 1
        assert self.game.game_counter(1) == 2
        assert self.game.game_counter(100) == 0

    def test_file_input_char(self):
        """ファイル入力を文字数でチェック"""
        root = self.game.file_input()
        assert len(str(root)) > 0