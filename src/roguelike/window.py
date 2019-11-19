import pygame
from roguelike.consts import *
import re

class Window:
    """ウィンドウの基本クラス"""
    EDGE_WIDTH = 4

    def __init__(self, rect):
        self.font = pygame.font.SysFont(DEFAULT_FONT, 20)
        self.rect = rect
        self.inner_rect = self.rect.inflate(-self.EDGE_WIDTH *
                                            2, -self.EDGE_WIDTH * 2)
        self.cur_page = 0
        self.text = []
        self.is_visible = False  # ウィンドウを表示中か？

    def draw(self, screen):
        """ウィンドウを描画"""
        if self.is_visible is False:
            return
        pygame.draw.rect(screen, (255, 255, 255), self.rect, 0)
        pygame.draw.rect(screen, (0, 0, 0), self.inner_rect, 0)

    def draw_msg(self, screen, set_data, set_script_data, game_count):
        """ウィンドウと文章を表示する"""
        # TODO: drawと入れ替えるべきでは？ウィンドウもメッセージも描画しているので。
        screen.fill((40, 40, 40))  # 前の画面をリセット

        self.show()
        self.draw(screen)

        self.draw_effect(screen, set_script_data)

        blitx = self.blitx
        blity = self.blity

        show_text = [x[2] for x in set_data if x[1]
                     == str(self.cur_page)]  # cur_pageが同じリストを抜き出す
        self.next_show_text = [x[2] for x in set_data if x[1]
                               == str(self.cur_page + 1)]  # 次の文字
        # 最後のページでない場合に▼を追加する。
        # 点滅する
        if len(self.next_show_text) and (game_count % 10) > 5:
            show_text.append("▼")

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

            # ループの最初だけflipさせる。flipの意味がよくわからない。
            # if self.first_flip == 0:
            #     pygame.display.flip()
            #     self.first_flip += 1

            blitx += jtext.get_rect().w

    def draw_effect(self, screen, set_script_data):
        """スクリプトを読み込んで特殊効果を描画する"""
        # TODO: 効果スクリプトを追加する
        self.script_stack = []
        script_list = self.msg_engine.argument_script_list
        s = []
        for p in range(self.cur_page + 1):
            self.script_stack += [x[0] for x in set_script_data if x[1] == str(p)]
        # リストを逆にして、最初にマッチしたbgだけ実行する = リストの最後だけ実行
        for x in self.script_stack[::-1]:
            s = re.search(r"bg='(.*)'", x)
            if s:
                if s.group(1) == '':
                    screen.fill((0, 0, 0))  # 画面をリセット
                    break
                else:
                    self.msg_engine.script_bg(s.group(1), screen)
                    break

    def show(self):
        """ウィンドウ表示"""
        self.is_visible = True

    def hide(self):
        """ウィンドウを隠す"""
        self.in_visible = False

    def update(self):
        """画面を更新"""
        pass

    def next(self):
        """メッセージを先に進める。なかったらcur_pageをリセットする"""
        self.cur_page += 1
        self.cur_pos = 0
        self.first_flip = 0
        if len(self.next_show_text) == 0:
            self.cur_page = 0
