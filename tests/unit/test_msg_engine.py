# coding: utf-8

# TODO: テストで共通に読み込むようにしたい。
# TODO: 起動するディレクトリを変えると動かない

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
        # TODO: テスト用の別ファイルを用意する.
        test_file = TEXT_DIR + "/scenario_data.xml"
        self.root = ET.parse(test_file).getroot()

    @pytest.fixture
    def input(self):
        m = Mock

    def check_const(self):
        """定数を読み込んだか確認する"""
        # TODO: いらなくない？
        assert TITLE == 0
        assert FULLTEXT == 3

    def test_set(self):
        """テキスト＋スクリプトの配列を作る"""
        # TODO: どうやってテストする？
        pass

    def test_set_script(self):
        """script配列作成の入出力比較によるテスト"""
        test_input = "@A\nこんにちは|\nbgm='morning'こんばんは"
        test = self.msg_engine.set_script(test_input)
        print(test)
        prepare = np.array([["bgm='morning'", '1'],
                            ['@A', '0'],
                            ])
        # ndarrayの比較(リストではなく多次元配列)
        assert (test == prepare).all()

    def test_set_text(self):
        """text配列作成の入出力比較によるテスト"""
        test_input = 'こん|に|ちは'
        test = self.msg_engine.set_text(test_input)
        prepare = np.array([['0', '0', 'こ'],
                            ['1', '0', 'ん'],
                            ['3', '1', 'に'],
                            ['5', '2', 'ち'],
                            ['6', '2', 'は']
                            ])
        assert (test == prepare).all()

    # script関連=======================================

    def test_get_script_list_type(self):
       """型をチェック"""
       test = self.msg_engine.get_script_list()
       assert type(test) is list

    def test_get_script_argument(self):
        """入出力チェック"""
        pattern = [
            "(bgm='.*')",
        ]
        test = self.msg_engine.get_script_argument(pattern)
        
        test_goal = [
            "bgm='(.*)'",
        ]
        assert test == test_goal

    # raw_text関連=====================================
       
    def test_file_input_char(self):
        """ファイル入力を文字数でチェック"""
        root = self.msg_engine.file_input()
        assert len(str(root)) > 0
       
    def test_load_xml_input(self):
        """シーン検索を入力テスト。"""
        mock = MagicMock()
        search = 'monologue0'

        # TODO: Mockへの値の入れ方がわからない。値を変えられないのであまり意味がない。
        load_value = self.msg_engine.load_xml(mock, search)
        assert load_value == ""

        load_value = self.msg_engine.load_xml(self.root, search)
        assert len(str(load_value)) > 0

    def test_stlips_text(self):
        """改行文字・空白文字の除去ができているかのテスト"""
        raw_text = "  こん\nに ち は"
        test = self.msg_engine.stlips_text(raw_text)
        assert test == "こんにちは"

        raw_text = ""
        test = self.msg_engine.stlips_text(raw_text)
        assert test == ""

    def test_del_script(self):
        """スクリプト部分の削除のテスト"""
        raw_text = "こ@Aん@Bにbg=''ちbgm=''は"
        test = self.msg_engine.del_script(raw_text)
        assert test == 'こんにちは'

    def test_create_text_data(self):
        """スクリプト削除＋空白文字削除ができているかテスト"""
        raw_text = "こ@Aん@B にbg=''ち\nは"
        test = self.msg_engine.create_text_data(raw_text)
        assert test == 'こんにちは'
