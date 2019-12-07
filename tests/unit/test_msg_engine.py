import numpy as np
import os
import pytest
import re
import xml.etree.ElementTree as ET
from mock import Mock
from mock import MagicMock
from roguelike.main import Game
from roguelike.msg_engine import MessageEngine
from roguelike.consts import *

class TestMsgEngine(object):
    pygame.init()
    game = Game()
    msg_engine = MessageEngine()

    def setup(self):
        """xmlからロードする
        """
        # TODO: テスト用の別ファイルを用意する.
        test_file = os.path.join(TEXT_DIR, 'scenario_data.xml')
        self.root = ET.parse(test_file).getroot()

    @pytest.fixture
    def input(self):
        m = Mock

    def check_const(self):
        """定数を読み込んだか確認する
        """
        assert TITLE == 0
        assert FULLTEXT == 3

    def test_set(self):
        """テキスト＋スクリプトの配列を作る
        """
        # TODO: どうやってテストする？
        pass

    def test_set_script(self):
        """script配列作成の入出力比較によるテスト
        """
        test_input = "@A\nこんにちは|\nbgm='morning'こんばんは"
        test = self.msg_engine.set_script(test_input)
        prepare = np.array([["bgm='morning'", '1'],
                            ['@A', '0'],
                            ])
        # ndarrayの比較(リストではなく多次元配列)
        assert (test == prepare).all()

    def test_set_text(self):
        """text配列作成の入出力比較によるテスト
        """
        test_input = 'こん|に|ちは'
        test = self.msg_engine.set_text(test_input)
        prepare = np.array([['0', '0', 'こ'],
                            ['1', '0', 'ん'],
                            ['3', '1', 'に'],
                            ['5', '2', 'ち'],
                            ['6', '2', 'は']
                            ])
        assert (test == prepare).all()

    # 正規表現生成=======================================

    def test_get_script_argument_output(self):
        """スクリプト引数取得の正規表現の出力チェック
        """
        # @[AB]は例外的
        pattern = [
            "(bgm='.*')",
            "(@[AB])",
        ]
        test = self.msg_engine.get_script_argument(pattern)

        test_expect = [
            "bgm='(.*)'",
            "@([AB])",
        ]
        assert test == test_expect

    def test_draw_effect(self):
        # テストではなく、実験用!!!!!
        """
        """
        # print(self.msg_engine.script_d)
        text = ['@A', '@B']
        self.goal = []
        for p in text:
            reg = re.search('@([AB])', p)
            self.goal.append(reg.group(1))

        assert self.goal == ['A', 'B']
        # draw_effectでは同じことができない。

    def test_get_script_delete_list_output(self):
        """スクリプト削除の正規表現の出力チェック
        """
        pattern = [
            "(bgm='.*')",
        ]
        test = self.msg_engine.get_script_delete_list(pattern)

        test_expect = [
            "bgm='.*'",
        ]
        assert test == test_expect

    # xml内スクリプト=======================================

    def test_script_change_music(self):
        """BGM再生の入出力チェック
        """
        no_change = self.msg_engine.script_change_music("title.mp3", "title.mp3")
        assert no_change == "title.mp3"
        # なぜmorningはできる？
        change = self.msg_engine.script_change_music("title.mp3", "diffrent_bgm")
        assert change == "title.mp3"

    def test_choice(self):
        """
        """
        input_choice = [['助ける', 'help1'],
                        ['助けない', 'no-help'],
                        ]
        # ?: 選んだものをどうやって取得する？
        # test = choice(input_choice)

        # right = np.array([WINDOWTEXT, 'help1'])
        # assert test == right

    def test_conv_choice(self):
        """
        """
        input = ['犬を助ける', 'dog1-1', '助けない', 'dog1-2']
        test = MessageEngine.conv_choice(self, input)
        right = [['犬を助ける', 'dog1-1'],
                 ['助けない', 'dog1-2'],
                 ]
        assert (test == right).all()

    # raw_text関連=====================================

    def test_file_input_char(self):
        """ファイル入力を文字数でチェック
        """
        root = self.msg_engine.file_input()
        assert len(str(root)) > 0

    def test_load_xml_input(self):
        """シーン検索を入力テスト。
        """
        mock = MagicMock()
        search = 'monologue0'

        # TODO: Mockへの値の入れ方がわからない。値を変えられないのであまり意味がない。
        load_value = self.msg_engine.load_xml(mock, search)
        assert load_value == ""

        load_value = self.msg_engine.load_xml(self.root, search)
        assert len(str(load_value)) > 0

    def test_stlips_text(self):
        """改行文字・空白文字の除去ができているかのテスト
        """
        raw_text = "  こん\nに ち は\t"
        test = self.msg_engine.stlips_text(raw_text)
        assert test == "こんにちは"

        raw_text = ""
        test = self.msg_engine.stlips_text(raw_text)
        assert test == ""

    def test_del_script(self):
        """スクリプト部分の削除のテスト
        """
        # raw_text = "こ@Aん@Bにbg=''ちbgm=''は"
        # ↑これは""が大きく解釈されてエラーになる。どうやって回避する？
        raw_text = "こ@Aん@Bにちbgm=''は"
        test = self.msg_engine.del_script(raw_text)
        assert test == 'こんにちは'

    def test_create_text_data(self):
        """スクリプト削除＋空白文字削除ができているかテスト
        """
        raw_text = "こ@A\nん@B にbg=''ち\nは"
        test = self.msg_engine.create_text_data(raw_text)
        assert test == 'こんにちは'
