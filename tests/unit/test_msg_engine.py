# coding: utf-8

# TODO: テストで共通に読み込むようにしたい。
import pygame
import pygame.mixer
from pygame.locals import *
import time
import sys
import numpy as np
import xml.etree.ElementTree as ET
import re
import os

from roguelike.roguelike import Game
import pytest
from mock import Mock
from mock import MagicMock

from roguelike.roguelike import MessageEngine
from roguelike.consts import *


class TestMsgEngine(object):
    pygame.init()
    game = Game()
    msg_engine = MessageEngine()

    @pytest.fixture
    def input(self):
        m = Mock

    def check_const(self):
        """定数を読み込んだか確認する"""
        assert TITLE == 0
        assert FULLTEXT == 3

    def test_set(self):
        """テキストデータの検証。"""
        # root = 'aa\nfa'
        # search = 'monologue0'
        # self.msg_engine.set(root, search)
        pass

    def test_load_xml(self):
        """シーン検索をテスト。"""
        # TODO: 入力を検証するにはどうしたらいい？
        # file_inputを使いたいが、ユニットテストにならない。
        # しかし、使わないとrootを準備できない。どうやってfindallできるような中身を準備するのか？

        self.game.file_input = Mock()
        mock = MagicMock()

        search = 'monologue0'
        load_value = self.msg_engine.load_xml(mock, search)

        assert load_value == ""

