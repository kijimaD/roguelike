# coding: utf-8

import pytest
import roguelike
from roguelike import MessageEngine
from mock import Mock

# TODO: Gameクラスを使いたいが、依存してるとチェックになるのか？
# だがどうしようもないように思える。テストどうしの依存がダメであって、メソッドの依存は仕方ないものじゃないのか。
# ユニットテスト…個々のメソッドをチェックすることなので、やはり一つ一つ独立していないといけないんだ。
# モックオブジェクト…を使うのか？

class TestMsgEngine(object):
    # TODO: グローバル変数を読み込めない
    msg_engine = MessageEngine()
    msg_engine.DEFAULT_FONT = roguelike.DEFAULT_FONT

    @pytest.fixture
    def input(self):
        m = Mock

    def test_draw(self):
        """"""
        # TODO: 描画はどうしたら成功だといえる？
        pass

    def test_set(self):
        # assert isinstance(self.msg_engine.page_index, list) == True
        pass

    def test_load_xml(self):
        pass



