import pygame
from pygame.locals import *
import math
import sys
import pygame.mixer

# バトルディッガーのクローンを作成する。

SCREEN = Rect(0, 0, 400, 400)


class Title():
    def __init__(self, x, y):
        self.sysfont = pygame.font.SysFont("RictyDiminishedDiscord", 20)
        (self.x, self.y) = (x, y)

    def draw(self, screen, letter):
        img = self.sysfont.render(
            letter, True, (255, 255, 255))
        screen.blit(img, (self.x, self.y))


class Sentence():
    def __init__(self, x, y):
        self.sysfont = pygame.font.SysFont("RictyDiminishedDiscord", 20)
        (self.x, self.y) = (x, y)

    def draw(self, screen):
        screen.fill((0, 0, 0))
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        pygame.quit()
                        sys.exit()


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN.size))
    pygame.display.set_caption("Roguelike")

    title = Title(10, 10)
    start1 = Title(10, 300)
    start2 = Title(10, 320)
    sentence = Sentence(10, 10)
    clock = pygame.time.Clock()

    while True:
        # 画面更新
        pygame.display.update()
        clock.tick(60)
        screen.fill((0, 0, 0))
        # タイトルを描画
        title.draw(screen, "クローンディッガー")
        start1.draw(screen, "冒険をはじめる[1]")
        start2.draw(screen, "続きから[2]")

    # キーイベント（終了）
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == K_1:  # ニューゲーム
                    # ここから全面文字画面にしたいが、forを抜け出す方法がわからない。
                    # 抜け出すのではなく、これを押すとモード変数を切り替えるようにする。
                    break
                    # sentence.draw(screen)
                if event.key == K_2:  # コンティニュー
                    break
    end_message = "終了しました"
    print(end_message)


if __name__ == "__main__":
    main()
