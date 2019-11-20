import pytest

from roguelike.utils import Utils

class TestUtils(object):
    def test_load_image_raise(self):
        """ファイル入力の例外テスト"""
        Utils.load_image('ball.jpg') # これは問題ない
        with pytest.raises(SystemExit):
            Utils.load_image('error.jpg')
