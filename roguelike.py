import pygame
from pygame.locals import *
import math
import sys
import pygame.mixer

SCREEN = Rect(0, 0, 400, 400)


class Title():
    def __init__(self, x, y):
        self.sysfont = pygame.font.SysFont("源ノ角ゴシックcodejpr", 20)
        (self.x, self.y) = (x, y)

    def draw(self, screen):
        img = self.sysfont.render(
            "Dungeonへようこそ。", True, (255, 255, 255))
        screen.blit(img, (self.x, self.y))

    def new_start(self, screen):
        img = self.sysfont.render(
            "冒険をはじめる", True, (255, 255, 255))
        screen.blit(img, (self.x, self.y))

    def continue_start(self, screen):
        img = self.sysfont.render(
            "続きから", True, (255, 255, 255))
        screen.blit(img, (self.x, self.y))


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN.size))
    pygame.display.set_caption("Roguelike")

    title = Title(10, 10)
    new_start = Title(10, 300)
    continue_start = Title(10, 320)

    clock = pygame.time.Clock()

    while (1):
        # フレームレート
        clock.tick(60)
        screen.fill((0, 20, 0))
        # タイトルを描画
        title.draw(screen)
        new_start.new_start(screen)
        continue_start.continue_start(screen)
        # 画面更新
        pygame.display.update()

        # キーイベント（終了）
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
    end_message = "終了しました"
    print(end_message)


if __name__ == "__main__":
    main()
