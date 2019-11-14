# coding: utf-8

import pytest
from roguelike.roguelike import MessageEngine
from mock import Mock

# TODO: Gameクラスを使いたいが、チェックにならない
# だがどうしようもないように思える。テストどうしの依存がダメであって、メソッドの依存は仕方ないものじゃないのか。
# ユニットテスト…個々のメソッドをチェックすることなので、やはり一つ一つ独立していないといけないんだ。
# モックオブジェクト…を使うのか？

class TestMsgEngine(object):
    # TODO: 定数を読み込めない。
    msg_engine = MessageEngine()
    # ERRER: インスタンス化の時点で失敗している。

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



