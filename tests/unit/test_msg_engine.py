# coding: utf-8

import roguelike
from roguelike import MessageEngine

# TODO: Gameクラスに依存してない？

class TestMsgEngine(object):
    msg_engine = MessageEngine()
    msg_engine.DEFAULT_FONT = roguelike.DEFAULT_FONT

    def test_draw(self):
        """"""
        # TODO: 描画はどうしたら成功だといえる？
        pass

    def test_set(self):
        # assert isinstance(self.msg_engine.page_index, list) == True
        pass

    def load_xml(self, root, search):
