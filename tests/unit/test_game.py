# coding: utf-8

# import roguelike as main
# TODO: importできていない。
from roguelike import Game
import pytest


def test_game():
    """"""
    t_1 = "1"
    t_2 = "1"
    assert t_1 == t_2

def test_update():
    """TODO: どうやってテストする？"""
    upd = Game()
    assert upd.game_state == "TITLE"

def test_render():
    pass
