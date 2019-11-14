# coding: utf-8

# TODO: テストで共通に読み込むようにしたい。
import pygame
from pygame.locals import *
import pygame.mixer
import pytest
from mock import Mock

from roguelike.roguelike import MessageEngine
from roguelike.consts import *

class TestMsgEngine(object):
    pygame.init()
    msg_engine = MessageEngine()

    @pytest.fixture
    def input(self):
        m = Mock

    def check_const(self):
        """定数を読みこんだか確認する"""
        assert TITLE == 0
        assert FULLTEXT == 3

    def test_draw(self):
        """drawのテスト"""
        # TODO: 描画はテストが困難？
        pass

    def test_set(self):
        # assert isinstance(self.msg_engine.page_index, list) == True
        pass

    def test_load_xml(self):
        pass



