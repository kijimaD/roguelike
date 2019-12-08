import pygame
from roguelike.consts import *
from roguelike.msg_engine import MessageEngine
from roguelike.plot import Plot
from roguelike.utils import Utils
import re


class Window:
    """ウィンドウの基本クラス
    """
    EDGE_WIDTH = 4
    CURSOR_X = 0
    def __init__(self, rect):
        self.font = pygame.font.SysFont(DEFAULT_FONT, 20)
        self.rect = rect
        self.inner_rect = self.rect.inflate(-self.EDGE_WIDTH *
                                            2, -self.EDGE_WIDTH * 2)
        self.cur_page = 0
        self.text = []
        self.is_visible = False  # ウィンドウを表示中か？
        self.cur_music = ""
        self.cursor_x = 0

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
        self.script_stack = []  # for内でも保持するためselfを使う
        for p in range(cur_page + 1):
            self.script_stack += [x[0] for x in set_script_data if x[1] == str(p)]
        return self.script_stack

    def draw_effect(self, screen, script_stack):
        """特殊効果を描画する
        """
        self.root = self.msg_engine.file_input()
        # リストを逆にして、最初にマッチした各スクリプトだけ実行する = リストの最後だけ実行

        for p in range(len(self.msg_engine.script_d[:, 0])):
            for x in script_stack[::-1]:
                reg = re.search(self.msg_engine.script_d[p][2], x)

                if reg:
                    if reg.group(1) == '':
                        break
                    else:
                        # f()の定義を動的に変化させる
                        fname = 'minimethod_' + self.msg_engine.script_d[p][0]
                        f = getattr(self, fname)
                        f(reg.group(1), screen)
                        break

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

    # ミニメソッド ======
    # window.draw_effectで呼び出される、各キーワードに割当られたメソッド群。
    # 必要な引数の種類が違うので、分けたい。

    def minimethod_bg(self, bg, screen):
        """背景を変更する
        """
        bg_image = Utils.load_image(bg)
        screen.blit(bg_image, (10, 10))

    def minimethod_bgm(self, bgm, screen):
        """BGMを変更する
        """
        # TODO: 引数screenは必要ない
        self.cur_music = self.msg_engine.script_change_music(bgm, self.cur_music)

    def minimethod_charaA(self, chara, screen):
        """左側のキャラを描画する
        """
        self.msg_engine.draw_left_character(chara, screen)

    def minimethod_charaB(self, chara, screen):
        """右側のキャラを描画する
        """
        self.msg_engine.draw_right_character(chara, screen)

    def minimethod_choice(self, choice, screen):
        """選択肢
        """
        d_choice = MessageEngine.conv_choice(self, choice)
        MessageEngine.draw_choice(self, screen, d_choice)
        MessageEngine.draw_choice_cursor(self, screen, self.CURSOR_X)
        # print('receive:', self.CURSOR_X)
        MessageEngine.choice_mode_enable(self, screen, choice)

    def minimethod_go(self, go, screen):
        """イベントを切り替える(選択肢用)
        """
        self.msg_engine.set(self.root, go)

    def minimethod_flag(self, flag, screen):
        """フラグ
        """
        pass

    def minimethod_side(self, side, screen):
        """吹き出しを描画する
        """
        # 吹き出しを表示しない場合、
        if side == 'A':
            self.msg_engine.draw_left_bubble(screen)
        elif side == 'B':
            self.msg_engine.draw_right_bubble(screen)
        elif side == 'AB':
            self.msg_engine.draw_left_bubble(screen)
            self.msg_engine.draw_right_bubble(screen)
        elif side == 'NONE':
            pass
        else:
            # TODO: 例外を送出する
            pass

    def minimethod_status(self, status, screen):
        """ステータスを変化させる
        """
        pass
