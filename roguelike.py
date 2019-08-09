import pygame
from pygame.locals import *
import codecs
import math
import os
import sys
import time
import pygame.mixer

# バトルディッガーのクローンを作成する。

SCREEN = Rect(0, 0, 640, 480)
SCR_W = 640
SCR_H = 320
TITLE, FIELD, FULLTEXT = range(3)


# class Title():
#     def __init__(self, x, y):
#         self.sysfont = pygame.font.SysFont("RictyDiminishedDiscord", 20)
#         (self.x, self.y) = (x, y)
#
#     def draw(self, screen, letter):
#         img = self.sysfont.render(
#             letter, True, (255, 255, 255))
#         screen.blit(img, (self.x, self.y))

class PyRPG:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN.size))
        pygame.display.set_caption("Roguelike")
        self.msg_engine = MessageEngine()
        # タイトル画面
        self.title = Title(self.msg_engine)
        # フルテキスト画面
        self.fulltext = Fulltext(Rect(0,0,640,480), self.msg_engine)
        # メインループを起動
        self.game_state = TITLE
        self.mainloop()

    def mainloop(self):
        # メインループ
        clock = pygame.time.Clock()
        while True:
            clock.tick(60)
            self.update()
            self.render()
            pygame.display.update()
            self.check_event()

    def update(self):
        # ゲーム状態の更新
        if self.game_state == TITLE:
            self.title.update()
        elif self.game_state == FULLTEXT:
            self.fulltext.update()

    def render(self):
        # ゲームオブジェクトのレンダリング
        if self.game_state == TITLE:
            self.title.draw(self.screen)
        elif self.game_state == FULLTEXT:
            self.fulltext.draw(self.screen)

    def check_event(self):
        # キーイベント（終了）
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

    def title_handler(self, event):
        # タイトル画面のイベントハンドラ
        if event.type == KEYUP and event.key == K_1:
            # モノローグへ
            print("タイトルモードで1を押しました")
            self.game_state = FULLTEXT
            time.sleep(0.2)
        if event.type == KEYUP and event.key == K_2:
            # 途中から
            self.game_state = FIELD

    def fulltext_handler(self, event):
        if event.type == KEYUP and event.key == K_1:
            # モノローグ
            print("フルテキストモードで1を押しました")
        if event.type == KEYUP and event.key == K_RETURN:
            # ページ送り
            print("フルテキストモードでENTERを押しました")

class Title:
    # タイトル画面
    START, CONTINUE, EXIT = 0, 1, 2

    def __init__(self, msg_engine):
        self.msg_engine = msg_engine
        self.menu = self.START

    def update(self):
        pass

    def draw(self, screen):
        screen.fill((0, 0, 0))
        self.msg_engine.draw(screen, 10, 10, "クローンディッガー")
        self.msg_engine.draw(screen, 10, 100, "はじめから[1]")
        self.msg_engine.draw(screen, 10, 120, "つづきから[2]")


class Fulltext:
    # 全画面文字モード
    MAX_CHARS_PER_LINE = 20     # １行の最大文字数
    MAX_LINES_PER_PAGE = 3      # １ページの最大行数
    MAX_CHARS_PER_PAGE = 20 * 3 # １ページの最大文字数
    MAX_LINES = 30              # 行間の大きさ
    LINE_HEIGHT = 8
    EDGE_WIDTH = 4

    def __init__(self, rect, msg_engine):
        Window.__init__(self,rect)
        self.msg_engine = msg_engine

        self.font = pygame.font.SysFont("RictyDiminishedDiscord", 20)
    def update(self):
        pass

    def message(self,screen,text):
        self.msg_engine.draw(screen,10,10,text)

    def draw(self, screen):
        # TODO: 文章を解析して改行や改ページを行いたい。

        screen.fill((40, 40, 40)) # 前の画面をリセット
        Window.show(self)
        Window.draw(self,screen)

        jstr = "人類は古代の昔から「遺跡」に惹かれ挑み続けてきた。/古代人たちは粗末な武器で遺跡に挑んだ。/そしてわずかな戦利品が残しほとんどが行方不明となった。//何が彼らを惹きつけたのか？/「最深部にある3つの珠を集めるとどんな願いも叶う」という言い伝えである。/言い伝えというと胡散臭いものに感じるが、遺跡の構造は現代でもほとんど解明されていない。/彼らには魔法に見えたかもしれない。/言い伝えを信じ、語り継いできたのも不思議ではない。&ときは変わって、現代。/新動力や機械技術の発展、科学の解明により生活は一変した。//そして戦車、戦闘機、戦艦…戦争の舞台や形が様変わりした。/遺跡の探索方法も一変した。/戦車に乗り、より下層まで潜ることが可能になったのだ。/しかし国家の関心事はもはや遺跡になく、今では謎の解明やお宝を追い求めてハンターや無法者が挑むのみである。//これから始まるのは、ハンターたちの物語。"

        blitx = 10
        blity = 10
        for c in jstr:
            # テキスト表示用Surfaceを作る
            jtext = self.font.render(c, True, (255,255,255))

            if c == "/": # /の場合は改行する
                blitx = 10
                blity += jtext.get_rect().h
                continue
            elif c == "&": # &だと改ページ
                screen.fill((40,40,40))
                blitx = 10
                blity = 10
                continue # 自動で改行しまう、キーボード押下で次に行くようにしたい。
            # blitの前にはみ出さないかチェック
            if blitx + jtext.get_rect().w >= SCR_W:
               blitx = 10
               blity += jtext.get_rect().h

            screen.blit(jtext,(blitx,blity))

            # pygame.display.flip() # 無限ループに入ってチカチカする。一度だけにしたいのだが…
            blitx += jtext.get_rect().w

        # self.message(screen, content)


class MessageWindow:
    # 通常のウィンドウメッセージ

    def __init__(self,rect, msg_engine):
        Window.__init__(self,rect)
        self.msg_engine = msg_engine

class Window:
    # ウィンドウの基本クラス
    EDGE_WIDTH = 4
    # クラス内の大文字変数の取扱方法がわからない。

    def __init__(self, rect):
        self.rect = rect
        self.inner_rect = self.rect.inflate(-self.EDGE_WIDTH * 2, -             self.EDGE_WIDTH * 2) # 疑問:よくわからない
        self.is_visible = False # ウィンドウを表示中か？

    def draw(self, screen):
        # ウィンドウを描画
        if self.is_visible == False:
            return
        pygame.draw.rect(screen, (255,255,255), self.rect, 0)
        pygame.draw.rect(screen, (0, 0, 0), self.inner_rect, 0)

    def show(self):
        # ウィンドウを描画
        self.is_visible = True

    def hide(self):
        self.in_visible = False

class MessageEngine:

    def __init__(self):
        self.font = pygame.font.SysFont("RictyDiminishedDiscord", 20)

    def draw(self, screen, x, y, text):
        screen.blit(self.font.render(text, True, (255, 255, 255)), [x, y])

if __name__ == "__main__":
    PyRPG()
