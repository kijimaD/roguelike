import pytest

from roguelike.utils import Utils

class TestUtils(object):
    def test_load_image_raise(self):
        """ファイル入力のテスト
        """
        Utils.load_image('ball.jpg')
        with pytest.raises(SystemExit):
            Utils.load_image('this_nothing.jpg')

    def test_load_sound_raise(self):
        """ファイル入力のテスト
        """
        Utils.load_sound('next_short.wav')
        with pytest.raises(SystemExit):
            Utils.load_image('this_nothing.wav')

    def test_play_bgm(self):
        """ファイル入力のテスト
        """
        Utils.play_bgm('title.mp3')
        with pytest.raises(SystemExit):
            Utils.play_bgm('this_nothing.wav')
