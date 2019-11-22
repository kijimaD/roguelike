#!/usr/bin/python3

import os
import pygame
import pygame.mixer
import sys
import time
import numpy as np
import re
import xml.etree.ElementTree as ET
from pygame.locals import *

from roguelike.consts import *
from roguelike import Title
from roguelike import Window
from roguelike import Fulltext
from roguelike import WindowText
from roguelike import MessageEngine
from roguelike import FieldView
from roguelike import Plot
from roguelike import Command
from roguelike import PlayerCharacter
from roguelike import Character
from roguelike import Enemy
from roguelike import Utils

class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        # self.screen = pygame.display.set_mode((SCREEN.size))
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
        Utils.play_bgm('title.mp3') # 暫定。各ゲームモードで一回だけ実行されるようなフックがない。

    def mainloop(self):
        """メインループ
        """
        clock = pygame.time.Clock()
        while True:
            clock.tick(60)
            self.update()
            self.render()
            pygame.display.update()
            self.check_event()

    def update(self):
        """ゲーム状態の更新
        """
        self.game_count = self.game_counter(self.game_count)
        if self.game_state == TITLE:
            self.title.update()
        elif self.game_state == FULLTEXT:
            self.fulltext.update()
        elif self.game_state == WINDOWTEXT:
            self.windowtext.update()

    def render(self):
        """ゲームオブジェクトのレンダリング
        """
        if self.game_state == TITLE:
            self.title.draw(self.screen, self.cursor_y)
        elif self.game_state == FULLTEXT:
            self.fulltext.draw_msg(self.screen, self.msg_engine.set_data, self.msg_engine.set_script_data,
                                   self.game_count)
        elif self.game_state == WINDOWTEXT:
            self.windowtext.draw_unify(self.screen, self.msg_engine.set_data, self.msg_engine.set_script_data,
                                       self.game_count)

    def check_event(self):
        """イベントハンドラ
        """
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
        """タイトル画面のイベントハンドラ
        """
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
        """フルテキストモードのイベントハンドラ
        """
        if event.type == KEYDOWN:
            if event.key == K_1:
                print("フルテキストモードで1を押しました")
            if event.key == K_RETURN:
                # ページ送り
                print("フルテキストモードでENTERを押しました")
                self.fulltext.next()
                # TODO: 操作と再生のタイムラグが酷い、操作と同時に鳴らしたい。
                next_sound = Utils.load_sound('next_short.wav')
                next_sound.play()
                if len(self.fulltext.next_show_text) == 0:
                    self.plot.plot_count += 1
                    self.game_state = self.plot.opening(self.root)

    def windowtext_handler(self, event):
        """ウィンドウテキストのイベントハンドラ
        """
        if event.type == KEYDOWN:
            if event.key == K_RETURN:
                # ページ送り
                print('ウィンドウテキストモードでENTERを押しました')
                self.windowtext.next()
                if len(self.windowtext.next_show_text) == 0:
                    self.plot.plot_count += 1
                    self.game_state = self.plot.opening(self.root)

    def game_counter(self, game_count):
        """描画に使用するカウンタ。
        """
        game_count += 1
        if game_count > 100:
            game_count = 0
        return game_count

if __name__ == "__main__":
    game = Game()
    game.screen = pygame.display.set_mode((SCREEN.size)) # テストにウィンドウが出るのを避けるためここに置く
    game.mainloop()
