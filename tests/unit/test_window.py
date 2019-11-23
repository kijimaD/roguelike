import numpy as np
from mock import Mock
from roguelike.window import Window

class TestWindow(object):
    def test_load_effect(self):
        """ページごとにエフェクトを読み込めているかテスト
        """
        prepare  = np.array([["bgm='10.mp3'", '0'],
                             ["bg='cave.jpg'", '0'],
                             ["bg='ball.jpg'", '1'],
                             ["bg='cave.jpg'", '3'],
        ])

        expected0 = ["bgm='10.mp3'", "bg='cave.jpg'"]
        expected1 = ["bgm='10.mp3'", "bg='cave.jpg'", "bg='ball.jpg'"]
        expected2 = ["bgm='10.mp3'", "bg='cave.jpg'", "bg='ball.jpg'"]
        expected3 = ["bgm='10.mp3'", "bg='cave.jpg'", "bg='ball.jpg'", "bg='cave.jpg'"]

        test0 = Window.load_effect(self, prepare, 0)
        test1 = Window.load_effect(self, prepare, 1)
        test2 = Window.load_effect(self, prepare, 2)
        test3 = Window.load_effect(self, prepare, 3)

        assert (expected0 == test0)
        assert (expected1 == test1)
        assert (expected2 == test2)
        assert (expected3 == test3)
