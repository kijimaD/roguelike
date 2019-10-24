# coding: utf-8

import pygame
from pygame.locals import *
import sys
import time
import pygame.mixer
import numpy as np
import json
import xml.etree.ElementTree as ET

# バトルディッガーのクローンを作成する。

SCREEN = Rect(0, 0, 640, 480)
SCR_W = 640
SCR_H = 320
TITLE, WINDOWTEXT, FIELD, FULLTEXT, COMMAND = range(5)
DEFAULT_FONT = "Noto Sans CJK JP"

class PyRPG:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN.size))
        pygame.display.set_caption("Roguelike")
        self.msg_engine = MessageEngine()
        self.title = Title(self.msg_engine)
        self.fulltext = Fulltext(Rect(0, 0, 640, 480), self.msg_engine)
        self.windowtext = WindowText(Rect(0, 0, 640, 480), self.msg_engine)
        # テキストを読み込み
        self.root = ET.parse('scenario_data.xml').getroot()
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
            self.windowtext.update()

    def render(self):
        """ゲームオブジェクトのレンダリング"""
        if self.game_state == TITLE:
            self.title.draw(self.screen, self.cursor_y)
        elif self.game_state == FULLTEXT:
            self.fulltext.draw(self.screen, self.set_data, self.set_script_data)
        elif self.game_state == WINDOWTEXT:
            self.windowtext.draw(self.screen, self.set_data, self.set_script_data)

    def check_event(self):
        """イベントハンドラ"""
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
            elif self.game_state == FULLTEXT:
                self.fulltext_handler(event)
            elif self.game_state == WINDOWTEXT:
                self.windowtext_handler(event)

    def title_handler(self, event):
        """タイトル画面のイベントハンドラ"""
        if event.type == KEYDOWN:
            if event.key == K_1:
                # 最初から（モノローグへ）
                print("タイトルモードで1を押しました")
                self.game_state = FULLTEXT
                self.set_data = self.msg_engine.set(self.load_xml(self.root, 'monologue0'))
                self.set_script_data = self.msg_engine.set_script(self.set_data)
            if event.key == K_2:
                # 途中から
                self.game_state = FIELD
            if event.key == K_UP:
                if self.cursor_y > 0:
                    print(self.cursor_y)
                    self.cursor_y += -1
            if event.key == K_DOWN:
                if self.cursor_y < 1:
                    print(self.cursor_y)
                    self.cursor_y += 1
            if event.key == K_RETURN:
                if self.cursor_y == 0:
                    self.game_state = FULLTEXT
                    self.set_data = self.msg_engine.set(self.load_xml(self.root, 'monologue0'))
                    time.sleep(0.1)
                if self.cursor_y == 1:
                    pass

    def fulltext_handler(self, event):
        """フルテキストモードのイベントハンドラ"""
        # TODO: 個別のイベントと分離させて汎用したい
        if event.type == KEYDOWN:
            if event.key == K_1:
                # テスト用
                print("フルテキストモードで1を押しました")
            if event.key == K_RETURN:
                # ページ送り
                print("フルテキストモードでENTERを押しました")
                self.fulltext.next()
                if len(self.fulltext.next_show_text) == 0:
                    self.game_state = WINDOWTEXT
                    self.set_data = self.msg_engine.set(self.load_xml(self.root, 'intro0'))

    def windowtext_handler(self, event):
        """ウィンドウテキストのイベントハンドラ"""
        if event.type == KEYDOWN:
            if event.key == K_RETURN:
                # ページ送り
                print('ウィンドウテキストモードでENTERを押しました')
                self.windowtext.next()

    def load_xml(self,root,search):
        """xmlの中から検索し、1行にして返す"""
        reg = ".//evt[@id='{}']"
        set_reg = reg.format(search)
        for e in root.findall(set_reg):
            # print("これは検索した結果です:", e.text)
            pass
        goal_text = e.text.strip().replace('\n','').replace(' ','') # タブ文字と改行文字の削除
        return goal_text


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

    def draw(self, screen, set_data, set_script_data):
        """ウィンドウと文章を表示する"""
        # TODO: 最後のページでない場合に▼を表示する
        screen.fill((40, 40, 40))  # 前の画面をリセット
        Window.show(self)
        Window.draw(self, screen)

        blitx = 10
        blity = 10

        show_text = [x[2] for x in set_data if x[1]
                     == str(self.cur_page)]  # cur_pageが同じリストを抜き出す
        self.next_show_text = [x[2] for x in set_data if x[1]
                               == str(self.cur_page + 1)]  # 次の文字が空か判定する
        for c in show_text:
            # テキスト表示用Surfaceを作る
            jtext = self.font.render(c, True, (255, 255, 255))

            # TODO: シナリオ内のコマンドシーケンスを解釈するには？引数もとる。
            # 描画用の1文字ループと、解釈用のループを分けたほうがいい？
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

        # 各スクリプトの描画
        cur_script = [x[1] for x in set_script_data if x[0] == str(self.cur_page)]
        print(cur_script)

    def next(self):
        """メッセージを先に進める"""
        self.cur_page += 1
        self.cur_pos = 0
        self.first_flip = 0


class WindowText:
    """通常のウィンドウメッセージ"""
    # TODO: シナリオ＋演出データをタグ形式にして演出データを追加していく。
    EDGE_WIDTH = 4

    def __init__(self, rect, msg_engine):
        Window.__init__(self, rect)
        self.font = pygame.font.SysFont(DEFAULT_FONT, 20)
        self.msg_engine = msg_engine
        self.cur_pos = 0
        self.cur_page = 0

    def draw(self, screen, set_data, set_script_data):
        """ウィンドウと文章を表示する"""
        screen.fill((40, 40, 40))
        Window.show(self)
        Window.draw_msgwindow(self, screen)

        pygame.draw.rect(screen, (0, 0, 0), Rect(10, 260, 620, 200), 3)
        self.draw_left_character(screen)
        self.draw_left_bubble(screen)

        blitx = 10
        blity = 260

        show_text = [x[2] for x in set_data if x[1]
                     == str(self.cur_page)]  # cur_pageが同じリストを抜き出す
        self.next_show_text = [x[2] for x in set_data if x[1]
                               == str(self.cur_page + 1)]  # 次の文字が空か判定する
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
                blity = 260
                continue

            # blitの前にはみ出さないかチェック
            if blitx + jtext.get_rect().w >= SCR_W:
                blitx = 10
                blity += jtext.get_rect().h

            screen.blit(jtext, (blitx, blity))
            blitx += jtext.get_rect().w

        # 各スクリプトの描画
        cur_script = [x[1] for x in set_script_data if x[0] == str(self.cur_page)]
        print(cur_script)

    def next(self):
        """メッセージを先に進める"""
        self.cur_page += 1
        self.cur_pos = 0
        self.first_flip = 0

    def draw_left_character(self, screen):
        """人物モデル（左）"""
        pygame.draw.circle(screen, (255, 0, 0), (120, 140), 40)

    def draw_right_character(self, screen):
        """人物モデル（右）"""
        pygame.draw.circle(screen, (0, 0, 255), (520, 140), 40)

    def draw_left_bubble(self, screen):
        """吹き出し（左）"""
        pygame.draw.line(screen, (0, 0, 0), (260, 260), (220, 220), 3)
        pygame.draw.line(screen, (0, 0, 0), (220, 220), (180, 220), 3)

    def draw_right_bubble(self, screen):
        """吹き出し（右）"""
        pygame.draw.line(screen, (0, 0, 0), (380, 260), (420, 220), 3)
        pygame.draw.line(screen, (0, 0, 0), (420, 220), (460, 220), 3)

    def update(self):
        pass


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

    def draw_msgwindow(self, screen):
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

    def set(self, message):
        """全体の文字の位置を求めて、リストを作成する。※改ページの処理に過ぎない"""
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
            # if ch == "/":
                # 注:fulltext.draw()に完全対応していない
                # continue
            if ch == "|":
                count_page += 1
                count_pos += 1
                continue
            else:
                self.text = np.append(self.text, np.array(
                    [[count_pos, count_page, ch]]), axis=0)
                p += 1
                count_pos += 1

        return self.text

    def set_script(self, set_data):
        set_script = []
        set_text = []

        # if match a='{}':

        return set_script


class Map:
    def __init__(self):
        pass

    def is_movable(self):
        pass

    def get_message(self):
        pass

    def draw(self):
        pass


class Buttle:
    pass


class FieldView:
    pass


class Command:
    pass


class Item:
    pass


class PlayerCharacter:
    """マップ上での操作キャラクター"""
    pass


class Character:
    """登場人物"""

    # TODO: シーンセットのプロトタイプを作る

    def __init__(self, icon, message):
        self.icon = icon
        self.message = message

    def talk(self):
        pass

    def draw(self, draw_side):
        if draw_side == L:
            pass


class Enemy:
    pass


class Hero:
    pass


if __name__ == "__main__":
    PyRPG()
