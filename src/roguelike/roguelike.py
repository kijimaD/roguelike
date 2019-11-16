# coding: utf-8

import pygame
import pygame.mixer
from pygame.locals import *
import time
import sys
import numpy as np
import xml.etree.ElementTree as ET
import re
import os

# TODO: 外部ファイルから読み込みたい。（テストは外部ファイル読み込みだが、このファイルでうまくいかない）
SCREEN = Rect(0, 0, 640, 480)
SCR_W = 640
SCR_H = 320
TITLE, WINDOWTEXT, FIELD, FULLTEXT, COMMAND = range(5)
DEFAULT_FONT = "Yu Mincho"
HOME_DIR = os.getcwd() + "/../../"
IMG_DIR = (HOME_DIR + "img")
TEXT_DIR = (HOME_DIR + "data")


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN.size))
        pygame.display.set_caption("Roguelike")
        self.msg_engine = MessageEngine()
        self.plot = Plot(self.msg_engine)
        self.title = Title(self.msg_engine)
        self.fulltext = Fulltext(Rect(0, 0, 640, 480), self.msg_engine)
        self.windowtext = WindowText(Rect(0, 0, 640, 480), self.msg_engine)
        self.root = self.msg_engine.file_input()
        self.cursor_y = 0
        self.plot_count = 0
        self.game_count = 0
        self.game_state = TITLE

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
        self.game_count = self.game_counter(self.game_count)
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
            self.fulltext.draw_msg(self.screen, self.msg_engine.set_data, self.msg_engine.set_script_data,
                                   self.game_count)
        elif self.game_state == WINDOWTEXT:
            self.windowtext.draw_unify(self.screen, self.msg_engine.set_data, self.msg_engine.set_script_data,
                                       self.game_count)

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
            else:
                print("game_state range error!")
                pygame.quit()
                sys.exit()

    def title_handler(self, event):
        """タイトル画面のイベントハンドラ"""
        if event.type == KEYDOWN:
            if event.key == K_1:
                # 最初から（OPへ）
                print("タイトルモードで1を押しました")
                self.game_state = self.plot.opening(self.root)
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
                    self.game_state = self.plot.opening(self.root)
                if self.cursor_y == 1:
                    pass

    def fulltext_handler(self, event):
        """フルテキストモードのイベントハンドラ"""
        if event.type == KEYDOWN:
            if event.key == K_1:
                print("フルテキストモードで1を押しました")
            if event.key == K_RETURN:
                # ページ送り
                print("フルテキストモードでENTERを押しました")
                self.fulltext.next()
                if len(self.fulltext.next_show_text) == 0:
                    self.plot.plot_count += 1
                    self.game_state = self.plot.opening(self.root)

    def windowtext_handler(self, event):
        """ウィンドウテキストのイベントハンドラ"""
        if event.type == KEYDOWN:
            if event.key == K_RETURN:
                # ページ送り
                print('ウィンドウテキストモードでENTERを押しました')
                self.windowtext.next()
                if len(self.windowtext.next_show_text) == 0:
                    self.plot.plot_count += 1
                    self.game_state = self.plot.opening(self.root)

    def game_counter(self, game_count):
        """描画に使用するカウンタ。"""
        game_count += 1
        if game_count > 100:
            game_count = 0
        return game_count


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
        # pygame.draw.rect(screen, (255, 255, 255), (10, 100 + cursor_y * 20, 100, 18), 1)
        if cursor_y == 0:
            new_game = "＞はじめから[1]"
            continue_game = "　つづきから[2]"
        elif cursor_y == 1:
            new_game = "　はじめから[1]"
            continue_game = "＞つづきから[2]"
        self.msg_engine.draw(screen, 10, 10, "クローンディッガー")
        self.msg_engine.draw(screen, 10, 100, new_game)
        self.msg_engine.draw(screen, 10, 120, continue_game)


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
        script_list = self.msg_engine.get_script_argument()
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


class Fulltext(Window):
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
        self.text = []
        self.cur_pos = 0
        self.next_flag = False
        self.hide_flag = False
        self.frame = 0
        self.first_flip = 0
        self.next_show_text = []
        self.blitx = 10
        self.blity = 10


class WindowText(Window):
    """通常のウィンドウメッセージ"""
    EDGE_WIDTH = 4

    def __init__(self, rect, msg_engine):
        Window.__init__(self, rect)
        self.msg_engine = msg_engine
        self.cur_pos = 0
        self.blitx = 10
        self.blity = 260

    def draw_unify(self, screen, set_data, set_script_data, game_count):
        self.draw_msg(screen, set_data, set_script_data, game_count)
        pygame.draw.rect(screen, (255, 255, 255), Rect(10, 260, 620, 200), 3)

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


class MessageEngine:
    """メッセージエンジンクラス"""

    def __init__(self):
        self.font = pygame.font.SysFont(DEFAULT_FONT, 20)

    def draw(self, screen, x, y, text):
        """メッセージの描画"""
        screen.blit(self.font.render(text, True, (255, 255, 255)), [x, y])

    def set(self, root, search):
        """テキストとスクリプト用の配列を作成する"""
        self.raw_text = self.load_xml(root, search)
        self.set_script_data = self.set_script(self.raw_text)  # scriptとcur_pageのリスト作成
        self.shaped_text = self.create_text_data(self.raw_text)  # 整形
        self.set_data = self.set_text(self.shaped_text)  # テキストとページ位置のリスト作成

    def set_script(self, text):
        """scriptとcur_pageのリストを作成する"""
        self.page_index = []
        self.script_index = np.empty([0, 2])  # [script, cur_page]

        # 改ページ文字の位置を検索
        for m in re.finditer("\\|", text, re.MULTILINE):
            self.page_index.append(m.start())
        # スクリプト部分を検索し、リストをくっつけて配列にする
        pattern = self.get_script_list()
        for pat in pattern:
            for s in re.finditer(pat, text, re.MULTILINE):
                # print(s.group()) # script
                # print(s.start()) # 位置
                # 位置を比較してcur_pageを導出
                for p in range(len(self.page_index)):
                    if s.start() < self.page_index[p]:
                        self.script_index = np.append(self.script_index, np.array(
                            [[s.group(), p]]), axis=0)
                        break
                # 最後のページ
                if max(self.page_index) < s.start():
                    self.script_index = np.append(self.script_index, np.array(
                        [[s.group(), len(self.page_index)]]), axis=0)
                    break

        return self.script_index

    def set_text(self, text):
        """全体の文字の位置を求めて、リストを作成する。※改ページの処理に過ぎない。
        [['文字位置','ページ位置','文字']]
        'こん|に|ちは'は、
        [['0','0','こ'],
         ['1','0','ん'],
         ['3','1','に'],
         ['5','2','ち'],
         ['6','2','は']] てな具合になる。
        """

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

    # script関連=================

    def get_script_list(self):
        """スクリプトのリストを生成する（検索用）"""
        # TODO: 定数で渡したほうがよくないか？
        pattern = []
        pattern += [
            "([ab]='.*')",
            "(bgm='.*')",
            "(bg='.*')",
            "(\\@[AB])",
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
        # print("これは引数取得用", goal_pattern)
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

    # raw_text生成=================

    def file_input(self):
        """xmlファイルを読み込み"""
        text_locate = TEXT_DIR + "/scenario_data.xml"
        root = ET.parse(text_locate).getroot()
        return root

    def load_xml(self, root, search):
        """xmlの中からシーン検索する"""
        reg = ".//evt[@id='{}']"
        set_reg = reg.format(search)

        goal_text = ""
        for e in root.findall(set_reg):
            goal_text += e.text

        return goal_text

    def stlips_text(self, input):
        """タブ文字改行文字を削除する"""
        # 削除しないと、setできない？
        goal_text = input.strip().replace(' ', '').replace('\n', '')  # タブ文字と改行文字と空白の削除
        return goal_text

    def del_script(self, raw_text):
        """スクリプト部分を削除する"""
        del_pattern = self.get_script_delete_list()
        goal_text = raw_text  # raw_textを使うのは最初だけ！
        for pat in del_pattern:
            goal_text = re.sub(pat, "", goal_text)
        return goal_text

    def create_text_data(self, raw_text):
        """テキスト用データを生成する。スクリプト削除＋余計な文字削除"""
        remove_text = self.del_script(raw_text)
        goal_text = self.stlips_text(remove_text)
        return goal_text


class Plot:
    def __init__(self, msg_engine):
        self.msg_engine = msg_engine
        self.plot_count = 0
        self.game_state = 0

    def opening(self, root):
        """オープニング。gamestateを返すのを忘れないように"""
        if self.plot_count == 0:
            self.game_state = FULLTEXT
            self.msg_engine.set(root, 'monologue0')
        elif self.plot_count == 1:
            self.game_state = WINDOWTEXT
            self.msg_engine.set(root, 'intro0')
        elif self.plot_count == 2:
            self.game_state = FULLTEXT
            self.msg_engine.set(root, 'monologue0')
        else:
            self.plot_count = 0
        return self.game_state


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
    game = Game()
    game.mainloop()
