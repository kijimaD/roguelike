# coding: utf-8

import pygame
from pygame.locals import *
import sys
import time
import pygame.mixer
import numpy as np
import xml.etree.ElementTree as ET
import re

# バトルディッガーのクローンを作成する。

SCREEN = Rect(0, 0, 640, 480)
SCR_W = 640
SCR_H = 320
TITLE, WINDOWTEXT, FIELD, FULLTEXT, COMMAND = range(5)
DEFAULT_FONT = "Yu Mincho"
IMG_DIR = ("./img")

class PyRPG:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN.size))
        pygame.display.set_caption("Roguelike")
        self.msg_engine = MessageEngine()
        self.title = Title(self.msg_engine)
        self.fulltext = Fulltext(Rect(0, 0, 640, 480), self.msg_engine)
        self.windowtext = WindowText(Rect(0, 0, 640, 480), self.msg_engine)
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
            self.fulltext.draw(self.screen, self.msg_engine.set_data, self.msg_engine.set_script_data)
        elif self.game_state == WINDOWTEXT:
            self.windowtext.draw(self.screen, self.msg_engine.set_data, self.msg_engine.set_script_data)

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
                self.msg_engine.set(self.root, 'monologue0')
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
                    self.msg_engine.set(self.root, 'monologue0')
                    print(self.set_data)
                    time.sleep(0.1)
                if self.cursor_y == 1:
                    pass

    def fulltext_handler(self, event):
        """フルテキストモードのイベントハンドラ"""
        # TODO: 個別のイベントと分離させて汎用したい
        if event.type == KEYDOWN:
            if event.key == K_1:
                print("フルテキストモードで1を押しました")
            if event.key == K_RETURN:
                # ページ送り
                print("フルテキストモードでENTERを押しました")
                self.fulltext.next()
                if len(self.fulltext.next_show_text) == 0:
                    self.game_state = WINDOWTEXT
                    self.msg_engine.set(self.root, 'intro0')

    def windowtext_handler(self, event):
        """ウィンドウテキストのイベントハンドラ"""
        if event.type == KEYDOWN:
            if event.key == K_RETURN:
                # ページ送り
                print('ウィンドウテキストモードでENTERを押しました')
                self.windowtext.next()


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
        pygame.draw.rect(screen, (255, 255, 255), (10, 110 + cursor_y * 20, 100, 18), 1)
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
        """画面を更新する"""
        pass

    def draw(self, screen, set_data, set_script_data):
        """ウィンドウと文章を表示する"""
        screen.fill((40, 40, 40))  # 前の画面をリセット

        Window.show(self)
        Window.draw(self, screen)

        self.draw_effect(screen, set_script_data)

        blitx = 10
        blity = 10

        show_text = [x[2] for x in set_data if x[1]
                     == str(self.cur_page)]  # cur_pageが同じリストを抜き出す

        # 最後のページでない場合に▼を追加する
        self.next_show_text = [x[2] for x in set_data if x[1]
                               == str(self.cur_page + 1)]  # 次の文字
        if len(self.next_show_text):
            show_text.append("▽")

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
        # TODO: 読み込みに応じたスクリプトを作成する
        curpage_script = [x[0] for x in set_script_data if x[1] == str(self.cur_page)]
        for x in curpage_script:
            s = re.search(r"bg='(.*)'", x)
            if s:
                self.msg_engine.script_bg(s.group(1), screen)

    def next(self):
        """メッセージを先に進める"""
        self.cur_page += 1
        self.cur_pos = 0
        self.first_flip = 0

class WindowText:
    """通常のウィンドウメッセージ"""
    EDGE_WIDTH = 4

    def __init__(self, rect, msg_engine):
        Window.__init__(self, rect)
        self.font = pygame.font.SysFont(DEFAULT_FONT, 20)
        self.msg_engine = msg_engine
        self.cur_pos = 0
        self.cur_page = 0

    def draw(self, screen, set_data, set_script_data):
        """ウィンドウと文章を表示する"""
        # TODO: アニメーションをつける
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
        cur_script = [x for x in set_script_data if x[0] == str(self.cur_page)]

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

    def set(self, root, search):
        self.raw_text = self.load_xml(root, search)
        self.set_script_data = self.set_script(self.raw_text)
        self.shaped_text = self.create_text_data(self.raw_text)
        self.set_data = self.set_text(self.shaped_text)

    def set_script(self, text):
        """scriptとcur_pageのリストを作成する"""
        self.page_index = []
        self.script_index = np.empty([0, 2]) # [script, cur_page]

        # 改ページ文字の位置を検索
        for m in re.finditer("\|", text, re.MULTILINE):
            self.page_index.append(m.start())

        # スクリプト部分を検索し、リストをくっつけて配列にする
        pattern = self.get_script_list()
        for pat in pattern:
            for s in re.finditer(pat, text, re.MULTILINE):
                print(s.group()) # script
                print(s.start()) # 位置
                # 位置を比較してcur_pageを導出
                for p in range(len(self.page_index)):
                    if s.start() < self.page_index[p]:
                        self.script_index = np.append(self.script_index, np.array(
                        [[s.group(), p]]), axis=0)
                        break

        print(self.script_index)

        return self.script_index

    def set_text(self, text):
        """全体の文字の位置を求めて、リストを作成する。※改ページの処理に過ぎない"""
        # （文字列群）最初にパターンマッチで|を探し、それぞれでスクリプトを探す。結果をリストに格納する。['command','cur_page']な具合に。
        self.cur_pos = 0
        self.cur_page = 0
        self.next_flag = False
        self.hide_flag = False
        self.text = np.empty([0, 3])
        count_page = 0
        count_pos = 0

        p = 0
        for i in range(len(text)):
            ch = text[i]  # chとmessage[i]は文字。
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

    def get_script_list(self):
        """スクリプトのリストを生成する（検索用）"""
        pattern = []
        pattern += [
            "([ab]='.*')",
            "(bgm='.*')",
            "(bg='.*')",
            "(\@[AB])",
        ]
        return pattern

    def get_script_argument(self):
        """スクリプトの引数取得用リストを生成する"""
        goal_pattern = []
        pattern = self.get_script_list()
        # 外側のカッコを削除して、''の内側にカッコを挿入する。
        for s in pattern:
            text = re.sub(r'\(', '', s)
            text = re.sub(r'\)', '', text)
            text = re.sub(r"'(.*)'", r"'(.*)'", text)
            goal_pattern.append(text)
        print("これは引数取得用", goal_pattern)
        return goal_pattern

    def get_script_delete_list(self):
        """削除用リストを生成する"""
        goal_pattern = []
        pattern = self.get_script_list()
        for s in pattern:
            text0 = re.sub(r'\(', '', s)
            text1 = re.sub(r'\)', '', text0)
            goal_pattern.append(text1)
        return goal_pattern

    def script_bg(self, bg, screen):
        """背景を変更する"""
        dir = (IMG_DIR + "/" + bg)
        bg_image = pygame.image.load(dir)
        screen.blit(bg_image, (10, 10))

    # ファイル関連 ==============================
    def load_xml(self, root, search):
        """xmlの中からシーン検索する"""
        reg = ".//evt[@id='{}']"
        set_reg = reg.format(search)
        for e in root.findall(set_reg):
            # print("これは検索した結果です:", e.text)
            pass
        goal_text = e.text
        return goal_text

    def split_text(self, input):
        """タブ文字改行文字を削除する"""
        # 削除しないと、setできない？
        goal_text = input.strip().replace(' ', '').replace('\n', '')  # タブ文字と改行文字の削除
        return goal_text

    def del_script(self, raw_text):
        """スクリプト部分を削除する"""
        del_pattern = self.get_script_delete_list()
        goal_text = raw_text # raw_textを使うのは最初だけ！
        for pat in del_pattern:
            goal_text = re.sub(pat, "", goal_text)
        return goal_text

    def create_text_data(self, raw_text):
        """テキスト用データを生成する"""
        remove_text = self.del_script(raw_text)
        goal_text = self.split_text(remove_text)
        return goal_text

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
        pass


class Enemy:
    pass


class Hero:
    pass


if __name__ == "__main__":
    PyRPG()
