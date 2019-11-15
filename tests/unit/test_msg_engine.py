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

    def setup(self):
        """xmlからロードする"""
        # TODO: テスト用の別ファイルを用意する
        test_file = TEXT_DIR + "/scenario_data.xml"
        self.root = ET.parse(test_file).getroot()

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

    def test_load_xml_input(self):
        """シーン検索を入力テスト。"""
        mock = MagicMock()
        search = 'monologue0'

        load_value = self.msg_engine.load_xml(mock, search)
        assert load_value == ""

        load_value = self.msg_engine.load_xml(self.root, search)
        assert len(str(load_value)) > 0

    def test_stlip_text(self):
        """改行文字・空白文字の除去ができているかのテスト"""
        raw_text = "  正常\nであれば 文字しか見えません"
        test = self.msg_engine.stlips_text(raw_text)
        assert test == "正常であれば文字しか見えません"

        raw_text = ""
        test = self.msg_engine.stlips_text(raw_text)
        assert test == ""