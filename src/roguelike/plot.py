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
