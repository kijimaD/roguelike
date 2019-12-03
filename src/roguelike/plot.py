import numpy as np
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
        # game_state = 0
        # if self.plot_count == 0:
        #     game_state = FULLTEXT
        #     self.msg_engine.set(root, 'monologue0')
        # elif self.plot_count == 1:
        #     game_state = WINDOWTEXT
        #     self.msg_engine.set(root, 'intro0')
        # elif self.plot_count == 2:
        #     game_state = WINDOWTEXT
        #     self.msg_engine.set(root, 'dog1-1')

        scenario_sequence = np.array([[FULLTEXT, 'monologue0'],
                                      [WINDOWTEXT, 'intro0'],
                                      [WINDOWTEXT, 'dog1-1'],
                                      ])
        game_state = int(scenario_sequence[self.plot_count][0])  # なぜか文字列で出るので、変換する。
        # game_state = FULLTEXT
        self.msg_engine.set(root, scenario_sequence[self.plot_count][1])

        if self.plot_count >= len(scenario_sequence[:, 0])-1:  # countは0始まり、lenは1始まりなので調整している
            self.plot_count = 0

        # 使用予定文=====================

        # choice = [['助ける', 'help'],
        #         ['助けない', 'no_help'],
        #          ]
        # 直前のBGMや背景を保持したい、が…
        # draw_choice(choice)  # 選択肢描画メソッド

        # 押下されたときのボタンID(ここでは0、1)を保存し、ここで読み込む
        # append(selected)  # 選択したものをリストに挿入する

        # =====================

        return game_state
