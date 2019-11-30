import pygame
from roguelike.consts import *
from roguelike.utils import Utils
from roguelike.msg_engine import MessageEngine
import re

class Window:
    """ウィンドウの基本クラス
    """
    EDGE_WIDTH = 4

    def __init__(self, rect):
        self.font = pygame.font.SysFont(DEFAULT_FONT, 20)
        self.rect = rect
        self.inner_rect = self.rect.inflate(-self.EDGE_WIDTH *
                                            2, -self.EDGE_WIDTH * 2)
        self.cur_page = 0
        self.text = []
        self.is_visible = False  # ウィンドウを表示中か？
        self.cur_music = ""

    def draw(self, screen):
        """ウィンドウを描画
        """
        if self.is_visible is False:
            return
        pygame.draw.rect(screen, (255, 255, 255), self.rect, 0)
        pygame.draw.rect(screen, (0, 0, 0), self.inner_rect, 0)

    def draw_msg(self, screen, set_data, set_script_data, game_count):
        """ウィンドウと文章を表示する
        """
        # TODO: drawと入れ替えるべきでは？ウィンドウもメッセージも描画しているので。
        # TODO: 長いので文字加工と表示を分割する
        screen.fill((40, 40, 40))  # 前の画面をリセット

        self.show()
        self.draw(screen)

        script_stack = self.load_effect(set_script_data, self.cur_page)
        self.draw_effect(screen, script_stack)

        blitx = self.blitx
        blity = self.blity

        # cur_pageが同じリストを抜き出す
        show_text = [x[2] for x in set_data if x[1]
                     == str(self.cur_page)]
        # 次の文字のリスト
        self.next_show_text = [x[2] for x in set_data if x[1] == str(self.cur_page + 1)]

        # 最後のページでない場合に▼を追加する。点滅する
        if len(self.next_show_text) and (game_count % 10) > 5:
            show_text.append("▼")

        # 描画
        for c in show_text:
            # テキスト表示用Surfaceを作る
            jtext = self.font.render(c, True, (255, 255, 255))

            if c == "^":  # 改行
                blitx = 10
                blity += jtext.get_rect().h
                continue
            elif c == "|":  # 改ページ
                screen.fill((40, 40, 40))
                Window.show(self)
                Window.draw(self, screen)
                blitx = 10
                blity = 10
                continue

            # blitの前にはみ出さないかチェック
            if blitx + jtext.get_rect().w >= SCR_W:
                blitx = 10
                blity += jtext.get_rect().h
            screen.blit(jtext, (blitx, blity))

            blitx += jtext.get_rect().w

    def load_effect(self, set_script_data, cur_page):
        """ページごとにスクリプトを読み込む
        """
        self.script_stack = [] # for内でも保持するためselfを使う
        for p in range(cur_page + 1):
            self.script_stack += [x[0] for x in set_script_data if x[1] == str(p)]
        return self.script_stack

    def draw_effect(self, screen, script_stack):
        """特殊効果を描画する
        """
        self.root = self.msg_engine.file_input()
        # リストを逆にして、最初にマッチしたbgだけ実行する = リストの最後だけ実行
        # FIXME: 書き方がひどい。同じことを書いている。
        print(script_stack)
        for x in script_stack[::-1]:
            bg = re.search(r"bg='(.*)'", x)
            if bg:
                if bg.group(1) == '':
                    screen.fill((0, 0, 0))  # 画面をリセット
                    break
                else:
                    self.msg_engine.script_change_bg(bg.group(1), screen)
                    break

        for x in script_stack[::-1]:
            bgm = re.search(r"bgm='(.*)'", x)
            if bgm:
                if bgm.group(1) == '':
                    break
                else:
                    # self.cur_music はmainの変数にしたほうがいいかもしれない。
                    self.cur_music = self.msg_engine.script_change_music(bgm.group(1), self.cur_music)
                    break

        for x in script_stack[::-1]:
            left = re.search(r"A='(.*)'", x)
            if left:
                if left.group(1) == '':
                    break
                else:
                    self.msg_engine.draw_left_character(left.group(1), screen)

        for x in script_stack[::-1]:
            right = re.search(r"B='(.*)'", x)
            if right:
                if right.group(1) == '':
                    break
                else:
                    self.msg_engine.draw_right_character(right.group(1), screen)

        for x in script_stack[::-1]:
            bubble = re.search(r"@([AB])", x)
            if bubble:
                if bubble.group(1) == 'A':
                    self.msg_engine.draw_left_bubble(screen)
                    break
                elif bubble.group(1) == 'B':
                    self.msg_engine.draw_right_bubble(screen)
                    break

        for x in script_stack[::-1]:
            to = re.search(r"TO='(.*)'", x)
            if to:
                if to.group(1) == '':
                    break
                else:
                    break
                # こちら側からrootにアクセスするにはどうする？
                # xmlからtoを指定するということはmainから呼び出せないということだ。

    def show(self):
        """ウィンドウ表示
        """
        self.is_visible = True

    def hide(self):
        """ウィンドウを隠す
        """
        self.in_visible = False

    def update(self):
        """画面を更新
        """
        pass

    def next(self):
        """メッセージを先に進める。なかったらcur_pageをリセットする
        """
        self.cur_page += 1
        self.cur_pos = 0
        self.first_flip = 0
        if len(self.next_show_text) == 0:
            self.cur_page = 0
