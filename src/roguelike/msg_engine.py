import pygame
import numpy as np
import re
import xml.etree.ElementTree as ET
from roguelike.consts import *
from roguelike.utils import Utils

class MessageEngine:
    """メッセージエンジンクラス
    """

    def __init__(self):
        self.font = pygame.font.SysFont(DEFAULT_FONT, 20)
        base_script_list = self.get_script_list()
        self.argument_script_list = self.get_script_argument(self.get_script_list())
        self.delete_script_list = self.get_script_delete_list(self.get_script_list())

    def draw(self, screen, x, y, text):
        """メッセージの描画
        """
        screen.blit(self.font.render(text, True, (255, 255, 255)), [x, y])

    def set(self, root, search):
        """テキストとスクリプト用の配列を作成し、各インスタンス変数に格納する
        """
        # raw_textから2つに分岐する感じ。
        raw_text = self.load_xml(root, search)
        self.set_script_data = self.set_script(raw_text)  # scriptとcur_pageのリスト作成
        shaped_text = self.create_text_data(raw_text)  # 整形
        self.set_data = self.set_text(shaped_text)  # テキストとページ位置のリスト作成

    def set_script(self, text):
        """scriptとcur_pageのリストを作成する
        [['スクリプト','ページ番号']]
        "bgm='morning'@Aおはよう|bgm='evening'@Bこんばんは"
        [["bgm='morning'",'0'],
         ["bgm='evening'",'1'],
         ['@A','0']
         ['@B','1']]
        """
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
                # 最後のページ。
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

    # 正規表現生成=================
    # 元データ/引数取得用/削除用の正規表現パターンを作成する。

    def get_script_list(self):
        """スクリプトのリストを生成する（検索用）
        例) "(bgm='.*)"
        """

        pattern = []
        pattern += [
            "([ab]='.*')",
            "(bgm='.*')",
            "(bg='.*')",
            "(\\@[AB])",
        ]
        return pattern

    def get_script_argument(self, pattern):
        """スクリプトの引数取得用リストを生成する
        例) "bgm='(.*)'"
        """

        goal_pattern = []
        # TODO: 一発で加工したい。
        for s in pattern:
            text = re.sub(r'\(', '', s)
            text = re.sub(r'\)', '', text)
            text = re.sub(r"'(.*)'", r"'(.*)'", text)
            goal_pattern.append(text)
        # print("これは引数取得用", goal_pattern)
        return goal_pattern

    def get_script_delete_list(self, pattern):
        """削除用リストを生成する
        例) "bgm='.*'"
        """

        goal_pattern = []
        for s in pattern:
            text0 = re.sub(r'\(', '', s)
            text1 = re.sub(r'\)', '', text0)
            goal_pattern.append(text1)
        return goal_pattern

    def script_bg(self, bg, screen):
        """背景を変更する
        """
        # bg_image = pygame.image.load(dir)
        bg_image = Utils.load_image(bg)
        screen.blit(bg_image, (10, 10))

    # raw_text生成=================

    def file_input(self):
        """xmlファイルを読み込む
        """
        text_locate = TEXT_DIR + "/scenario_data.xml"
        root = ET.parse(text_locate).getroot()
        return root

    def load_xml(self, root, search):
        """xmlの中からシーン検索する
        """
        reg = ".//evt[@id='{}']"
        set_reg = reg.format(search)

        goal_text = ""
        for e in root.findall(set_reg):
            goal_text += e.text

        return goal_text

    def stlips_text(self, input):
        """タブ文字改行文字を削除する
        """
        # 削除しないと、setできない？
        goal_text = input.strip().replace(' ', '').replace('\n', '')  # タブ文字と改行文字と空白の削除
        return goal_text

    def del_script(self, raw_text):
        """スクリプト部分を削除する
        """
        del_pattern = self.get_script_delete_list(self.get_script_list())
        goal_text = raw_text  # raw_textを使うのは最初だけ！
        for pat in del_pattern:
            goal_text = re.sub(pat, "", goal_text)
        return goal_text

    def create_text_data(self, raw_text):
        """テキスト用データを生成する。スクリプト削除＋余計な文字削除
        """
        remove_text = self.del_script(raw_text)
        goal_text = self.stlips_text(remove_text)
        return goal_text
