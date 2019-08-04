import pygame
from pygame.locals import *
import codecs
import math
import os
import sys
import time
import pygame.mixer

# バトルディッガーのクローンを作成する。

SCREEN = Rect(0, 0, 400, 400)

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
        self.fulltext = Fulltext(self.msg_engine)
        # メインループを起動
        self.game_state = TITLE
        self.mainloop()

    def mainloop(self):
        # メインループ
        clock = pygame.time.Clock()
        while True:
            # 画面更新
            clock.tick(60)
            self.update()
            self.render()
            # タイトルを描画
            # title.draw(screen, "クローンディッガー")
            # start1.draw(screen, "冒険をはじめる[1]")
            # start2.draw(screen, "続きから[2]")
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
            time.sleep(1)
        if event.type == KEYUP and event.key == K_2:
            # 途中から
            self.game_state = FIELD

    def fulltext_handler(self, event):
        if event.type == KEYUP and event.key == K_1:
            # モノローグへ
            print("フルテキストモードで1を押しました")
        pass


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
        self.msg_engine.draw_string(screen, 10, 10, "クローンディッガー")
        self.msg_engine.draw_string(screen, 10, 100, "はじめから[1]")
        self.msg_engine.draw_string(screen, 10, 120, "つづきから[2]")


class Fulltext:

    def __init__(self, msg_engine):
        self.msg_engine = msg_engine

    def update(self):
        pass

    def draw(self, screen):
        screen.fill((0, 0, 0))
        self.msg_engine.draw_string(screen, 10, 10, "「遺跡」が発見されてすべてが変わった。")


class MessageEngine:

    def __init__(self):
        self.font = pygame.font.SysFont("RictyDiminishedDiscord", 20)

    def draw_string(self, screen, x, y, text):
        screen.blit(self.font.render(text, True, (255, 255, 255)), [x, y])


if __name__ == "__main__":
    PyRPG()
