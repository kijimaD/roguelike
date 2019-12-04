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
        scenario_sequence = np.array([[FULLTEXT, 'monologue0'],
                                      [WINDOWTEXT, 'intro0'],
                                      [WINDOWTEXT, 'top'],
                                      ])
        game_state = int(scenario_sequence[self.plot_count][0])  # なぜか文字列で出るので、変換する。
        # game_state = FULLTEXT
        self.msg_engine.set(root, scenario_sequence[self.plot_count][1])

        print(self.plot_count)
        if self.plot_count >= len(scenario_sequence[:, 0])-1:  # countは0始まり、lenは1始まりなので調整している
            self.plot_count = -1  # TODO: 先にインクリメントするので、-1。おかしいので修正する。

        return game_state

    def choice_mode(self, screen, choice):
        """選択肢の使用予定文。直前のBGMや背景を保持したい
        """

        # choice = [['助ける', 'help'],
        #           ['助けない', 'no_help'],
        #           ]
        # 引数choiceをイベント名とアイコン名に分割して、各メソッドに渡す。

        choice_mode = 1  # イベントハンドラを選択肢モードにする。(game_stateはwindowtextで、キーイベントだけ変える)

        self.msg_engine.draw_choice(screen, choice)  # 選択肢描画メソッド

        # 押下されたときの数字を保存し、読み込む
        # append(selected)  # 選択したものをリストに挿入する
