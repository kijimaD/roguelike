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
            new_game = ">はじめから[1]"
            continue_game = " つづきから[2]"
        elif cursor_y == 1:
            new_game = " はじめから[1]"
            continue_game = ">つづきから[2]"
        self.msg_engine.draw(screen, 10, 10, "クローンディッガー")
        self.msg_engine.draw(screen, 10, 100, new_game)
        self.msg_engine.draw(screen, 10, 120, continue_game)
