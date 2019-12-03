import pygame.mixer
from roguelike.utils import Utils
from roguelike.consts import *


class Plot:
    def __init__(self, msg_engine):
        self.msg_engine = msg_engine
        self.plot_count = 0

    def opening(self, root):
        """オープニング。
        """
        # 読み込むsetをリスト化する
        game_state = 0
        if self.plot_count == 0:
            game_state = FULLTEXT
            self.msg_engine.set(root, 'monologue0')
        elif self.plot_count == 1:
            game_state = WINDOWTEXT
            self.msg_engine.set(root, 'intro0')
        elif self.plot_count == 2:
            game_state = WINDOWTEXT
            self.msg_engine.set(root, 'dog1-1')

        # 使用予定文=====================

        elif self.plot_count == 3:
            game_state = CHOICE  # キーボードのハンドラだけ変えて、ほかは変えない。
            choice = [['助ける', 'help'],
                      ['助けない', 'no_help'],
                      ]
            # 直前のBGMや背景を保持したい、が…
            draw_choice(choice)  # 選択肢描画メソッド

            # 押下されたときのボタンID(ここでは0、1)を保存し、ここで読み込む
            append(selected)  # 選択したものをリストに挿入する

        # =====================

        else:
            self.plot_count = 0
        return game_state
