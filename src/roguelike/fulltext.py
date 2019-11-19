from roguelike import Window

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
