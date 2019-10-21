# coding: utf-8

import pygame
from pygame.locals import *
# import codecs
# import math
# import os
import sys
import time
import pygame.mixer
import numpy as np
import json

# バトルディッガーのクローンを作成する。

SCREEN = Rect(0, 0, 640, 480)
SCR_W = 640
SCR_H = 320
TITLE, WINDOWTEXT, FIELD, FULLTEXT, COMMAND = range(5)
DEFAULT_FONT = "RictyDiminishedDiscord"


class PyRPG:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN.size))
        pygame.display.set_caption("Roguelike")
        self.msg_engine = MessageEngine()
        self.title = Title(self.msg_engine)
        self.fulltext = Fulltext(Rect(0, 0, 640, 480), self.msg_engine)
        self.windowtext = WindowText(Rect(0, 0, 640, 480),self.msg_engine)
        # テキストを読み込み
        file = open('scenario_data.json', 'r', encoding="utf-8")
        self.text_data = json.load(file)
        # メインループを起動
        self.game_state = TITLE
        self.cursor_y = 0
        self.mainloop()

    def mainloop(self):
        """メインループ"""
        clock = pygame.time.Clock()
        while True:
            clock.tick(60)
            self.update()
            self.render()
            pygame.display.update()
            self.check_event()

    def update(self):
        """ ゲーム状態の更新 """
        if self.game_state == TITLE:
            self.title.update()
        elif self.game_state == FULLTEXT:
            self.fulltext.update()
        elif self.game_state == WINDOWTEXT:
            self.windowtext.draw(self.screen)

    def render(self):
        """ゲームオブジェクトのレンダリング"""
        if self.game_state == TITLE:
            self.title.draw(self.screen, self.cursor_y)
        elif self.game_state == FULLTEXT:
            self.fulltext.draw(self.screen)
        elif self.game_state == WINDOWTEXT:
            self.windowtext.draw(self.screen)

    def check_event(self):
        """キーイベント（終了）"""
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
                # 表示されているウィンドウに応じてイベントハンドラを変更
            if self.game_state == TITLE:
                self.title_handler(event)
            if self.game_state == FULLTEXT:
                self.fulltext_handler(event)
            if self.game_state == WINDOWTEXT:
                self.windowtext_handler(event)

    def title_handler(self, event):
        """タイトル画面のイベントハンドラ"""
        if event.type == KEYUP and event.key == K_1:
            # モノローグへ
            print("タイトルモードで1を押しました")
            self.game_state = FULLTEXT
            self.fulltext.set(self.text_data["monologue0"]["text"])
            time.sleep(0.2)
        if event.type == KEYUP and event.key == K_2:
            # 途中から
            self.game_state = FIELD
        if event.type == KEYUP and event.key == K_UP:
            if self.cursor_y > 0:
                print(self.cursor_y)
                self.cursor_y += -1
        if event.type == KEYUP and event.key == K_DOWN:
            if self.cursor_y < 1:
                print(self.cursor_y)
                self.cursor_y += 1
        if event.type == KEYDOWN and event.key == K_RETURN:
            if self.cursor_y == 0:
                # フルテキストモードのenterも1回押してしまう。デバッガーでみると2回ループしてるから？遅延させても不可。
                # タイトルと、フルテキストのenterが競合してどちらも押されてることになってるぽい？
                self.game_state = FULLTEXT
                self.fulltext.set(self.text_data["monologue0"]["text"])
                time.sleep(1)
            if self.cursor_y == 1:
                pass

    def fulltext_handler(self, event):
        """フルテキストモードのイベントハンドラ"""
        if event.type == KEYDOWN and event.key == K_1:
            # モノローグ
            print("フルテキストモードで1を押しました")
        if event.type == KEYDOWN and event.key == K_RETURN:
            # ページ送り
            print("フルテキストモードでENTERを押しました")
            self.fulltext.next()
            if len(self.fulltext.next_show_text) == 0:
                self.game_state = WINDOWTEXT

    def windowtext_handler(selfself, event):
        """ウィンドウテキストのイベントハンドラ"""
        # TODO: 一回textを出力せず何もない空間ができてしまうので修正する。
        if event.type == KEYDOWN and event.key == K_RETURN:
            # ページ送り
            print('ウィンドウテキストモードでENTERを押しました')


class Title:
    """タイトル画面クラス"""
    START, CONTINUE, EXIT = 0, 1, 2

    def __init__(self, msg_engine):
        self.msg_engine = msg_engine
        self.menu = self.START

    def update(self):
        """画面の更新（未実装）"""
        pass

    def draw(self, screen, cursor_y):
        """タイトルの描画"""
        screen.fill((0, 0, 0))
        pygame.draw.rect(screen, (255, 255, 255), (10, 100 + cursor_y * 20, 100, 18), 1)
        self.msg_engine.draw(screen, 10, 10, "クローンディッガー")
        self.msg_engine.draw(screen, 10, 100, "はじめから[1]")
        self.msg_engine.draw(screen, 10, 120, "つづきから[2]")


class Fulltext:
    """全画面の文字表示クラス"""

    # MAX_CHARS_PER_LINE = 20  # １行の最大文字数
    # MAX_LINES_PER_PAGE = 3  # １ページの最大行数
    # MAX_CHARS_PER_PAGE = 20 * 3  # １ページの最大文字数
    # MAX_LINES = 30  # 行間の大きさ
    # LINE_HEIGHT = 8
    EDGE_WIDTH = 4

    def __init__(self, rect, msg_engine):
        Window.__init__(self, rect)
        self.msg_engine = msg_engine

        self.font = pygame.font.SysFont(DEFAULT_FONT, 20)
        self.text = []
        self.cur_pos = 0
        self.cur_page = 0
        self.next_flag = False
        self.hide_flag = False
        self.frame = 0
        self.first_flip = 0
        self.next_show_text = []

    def update(self):
        """画面を更新する（未実装）"""
        pass

    def set(self, message):
        """全体の文字の位置を求めて、リストを作成する"""
        self.cur_pos = 0
        self.cur_page = 0
        self.next_flag = False
        self.hide_flag = False
        self.text = np.empty([0, 3])
        count_page = 0
        count_pos = 0

        p = 0
        for i in range(len(message)):
            ch = message[i]  # chとmessage[i]は文字。
            if ch == "/":
                pass
            elif ch == "&":
                count_page += 1
                count_pos += 1
                continue
            else:
                self.text = np.append(self.text, np.array(
                    [[count_pos, count_page, ch]]), axis=0)
                p += 1
                count_pos += 1

    def draw(self, screen):
        """ウィンドウと文章を表示する"""

        screen.fill((40, 40, 40))  # 前の画面をリセット
        Window.show(self)
        Window.draw(self, screen)

        blitx = 10
        blity = 10

        show_text = [x[2] for x in self.text if x[1]
                          == str(self.cur_page)]  # 配列の3番目の要素を抜き出す
        self.next_show_text =[x[2] for x in self.text if x[1]
                          == str(self.cur_page+1)]  # 次の文章が空か判定する
        for c in show_text:
            # テキスト表示用Surfaceを作る
            jtext = self.font.render(c, True, (255, 255, 255))

            if c == "/":  # /の場合は改行する
                blitx = 10
                blity += jtext.get_rect().h
                continue
            elif c == "&":  # &だと改ページ
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

    def next(self):
        """メッセージを先に進める"""
        self.cur_page += 1
        self.cur_pos = 0
        self.first_flip = 0


class WindowText:
    """通常のウィンドウメッセージ"""
    # TODO: まず文章を表示させる
    # TODO: どうやって文章を取得し、遷移するか考える
    EDGE_WIDTH = 4

    def __init__(self, rect, msg_engine):
        Window.__init__(self, rect)
        self.msg_engine = msg_engine

    def draw(self, screen):
        """ウィンドウと文章を表示する"""
        screen.fill((40, 40, 40))
        Window.show(self)
        Window.draw_msgwindow(self,screen)
        pygame.draw.rect(screen, (0, 0, 0), Rect(10, 260, 620, 200))

    def window_message(self, message):
        self.msg_engine.draw(screen, 10, 260, "クローンディッガー")


class Window:
    """ウィンドウの基本クラス"""
    EDGE_WIDTH = 4

    def __init__(self, rect):
        self.rect = rect
        self.inner_rect = self.rect.inflate(-self.EDGE_WIDTH *
                                            2, -self.EDGE_WIDTH * 2)
        self.is_visible = False  # ウィンドウを表示中か？

    def draw(self, screen):
        """ウィンドウを描画"""
        if self.is_visible is False:
            return
        pygame.draw.rect(screen, (255, 255, 255), self.rect, 0)
        pygame.draw.rect(screen, (0, 0, 0), self.inner_rect, 0)

    def draw_msgwindow(self,screen):
        """メッセージウィンドウを描画"""
        pass

    def show(self):
        """ウィンドウ表示"""
        self.is_visible = True

    def hide(self):
        self.in_visible = False


class MessageEngine:
    """メッセージエンジンクラス"""

    def __init__(self):
        self.font = pygame.font.SysFont(DEFAULT_FONT, 20)

    def draw(self, screen, x, y, text):
        """メッセージの描画"""
        screen.blit(self.font.render(text, True, (255, 255, 255)), [x, y])


class Map:
    pass


class Buttle:
    pass


class FieldView:
    pass


class Command:
    pass


class Item:
    pass


class Character:
    pass


class Enemy:
    pass


class Hero:
    pass


if __name__ == "__main__":
    PyRPG()
