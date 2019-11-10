# coding: utf-8

from roguelike import Game
import pytest


def test_game():
    """"""
    t_1 = "1"
    t_2 = "1"
    assert t_1 == t_2

def test_update():
    """"""
    # TODO: ループをどうやってテストする？インスタンス作成すら、できないじゃない…
    upd = Game()
    assert isinstance(upd.update,str) == False
