# coding: utf-8

from roguelike.roguelike import MessageEngine
from roguelike.title import Title

def test_update():
    msg_engine = MessageEngine()
    title = Title(msg_engine)
    upd = title.update()
    assert upd == None
