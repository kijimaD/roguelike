import pytest

from roguelike.utils import Utils

class TestUtils(object):
    def test_load_image_raise(self):
        """ファイル入力の例外テスト"""
        Utils.load_image('ball.jpg')
        with pytest.raises(SystemExit):
            Utils.load_image('error.jpg')

    def test_load_sound_raise(self):
        """ファイル入力の例外テスト"""
        Utils.load_sound('beamgun.mp3')
        with pytest.raises(SystemExit):
            Utils.load_image('error.mp3')
