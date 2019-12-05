import numpy as np
import pygame.mixer
from roguelike.consts import *
from roguelike.utils import Utils


class Plot:

    choice_mode = 0

    def __init__(self, msg_engine):
        self.msg_engine = msg_engine
        self.plot_count = 0
        self.choice_mode = 0

    def opening(self, root):
        """オープニング。
        """
        # TODO: sequenceの最初に戻ったときBGMが再生されないバグがある。
        scenario_sequence = np.array([[FULLTEXT, 'monologue0'],
                                      [WINDOWTEXT, 'intro0'],
                                      [WINDOWTEXT, 'top'],
                                      ])
        game_state = int(scenario_sequence[self.plot_count][0])  # なぜか文字列で出るので、変換する。
        # game_state = FULLTEXT
        self.msg_engine.set(root, scenario_sequence[self.plot_count][1])

        if self.plot_count >= len(scenario_sequence[:, 0])-1:  # countは0始まり、lenは1始まりなので調整している
            self.plot_count = -1  # TODO: 先にインクリメントするので、-1で初期化。あとで修正する。

        return game_state

    def choice(self, screen, choice):
        """選択肢の使用予定文。直前のBGMや背景を保持したい
        """
        # TODO: Plotにあるのはおかしいかもしれない。

        # choice = [['助ける', 'help'],
        #           ['助けない', 'no_help'],
        #           ]
        # 引数choiceをイベント名とアイコン名に分割して、各メソッドに渡す。

        self.choice_mode = 1  # イベントハンドラを選択肢モードにする。(game_stateはwindowtextで、キーイベントだけ変える)

        Plot.choice_mode = 1

        self.msg_engine.draw_choice(screen, choice)  # 選択肢描画メソッド

        # 選択したものを返す。
        # return(selected)
