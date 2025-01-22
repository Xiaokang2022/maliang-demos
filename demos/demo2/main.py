import math
import tkinter
import typing

import maliang
import maliang.animation as animation
import maliang.core.configs as configs
import maliang.core.virtual as virtual
import maliang.standard.dialogs as dialogs
import maliang.standard.features as features
import maliang.standard.shapes as shapes
import maliang.standard.texts as texts
import maliang.theme as theme
import maliang.toolbox as toolbox

if toolbox.load_font("./assets/fonts/LXGWWenKai-Regular.ttf"):  # 加载指定字体文件
    configs.Font.family = "LXGW WenKai"  # 指定全局字体

# theme.set_theme_map(light="./demos/demo2/mytheme", dark="./demos/demo2/mytheme",
#                 folder="./demos/demo2")  # 设置自定义的颜色主题


class Circle(shapes.Oval):
    """圆形形状"""

    def detect(self, x: int, y: int) -> bool:
        """自定义检测方式，半径小于指定大小则返回 True"""
        return math.hypot(x-self.position[0]-self.size[0]/2, y-self.position[1]-self.size[1]/2) <= self.size[0]/2


class Piece(virtual.Widget):
    """继承小部件基类，具化为棋子类"""

    def __init__(
        self,
        master: maliang.Canvas,
        position: tuple[int, int],
        color: typing.Literal["white", "black"],
        text: str,
    ) -> None:
        virtual.Widget.__init__(
            self, master, index_to_position(*position), (60, 60))
        Circle(self, name=f".{color}")
        texts.Information(self, text=text, fontsize=32)
        self.feature = features.ButtonFeature(
            self, command=lambda: move_mark(self.bx, self.by))
        self.color = color
        self.bx, self.by = position
        board[self.bx][self.by] = self


class Board(virtual.Shape):

    def display(self) -> None:
        self.items = [
            canvas.create_line(50, 50, 550, 550, fill="black"),
            canvas.create_line(550, 50, 50, 550, fill="black"),
            canvas.create_line(300, 50, 300, 550, fill="black"),
            canvas.create_line(50, 50, 550, 50, fill="black"),
            canvas.create_line(50, 550, 550, 550, fill="black"),
            canvas.create_line(175, 175, 425, 175, fill="black"),
            canvas.create_line(175, 425, 425, 425, fill="black"),
            canvas.create_line(175, 300, 425, 300, fill="black"),
        ]

        for x in range(5):
            for y in range(5):
                if board[x][y] == -1:
                    cx, cy = x*125 + 20 + 30, y*125 + 20 + 30
                    canvas.create_oval(cx-30, cy-30, cx+30, cy+30,
                                       outline="black", fill=canvas["bg"])

    def coords(self, size: tuple[float, float] | None = None, position: tuple[float, float] | None = None) -> None:
        return super().coords(size, position)


def index_to_position(x: int, y: int) -> tuple[int, int]:
    """棋盘索引转换为画布实际位置"""
    return x*125 + 20, y*125 + 20


def position_to_index(x: int, y: int, delta: float = math.inf) -> tuple[int, int] | None:
    """画布实际位置转换为棋盘索引，delta 为判定半径，距离交点 delta 以内则判定成功"""
    x, y = x-50, y-50
    ix, iy = round(x/125), round(y/125)
    if board[ix][iy] is not None and math.hypot(ix*125 - x, iy*125 - y) < delta:
        return ix, iy


def move_cursor(event: tkinter.Event) -> None:
    """移动游标的位置"""
    global cursor_index
    k = min(canvas.ratios)
    x, y = event.x/k, event.y/k
    result = position_to_index(x, y)
    if result is not None and result != cursor_index:
        delta = (result[0]-cursor_index[0])*125 * \
            k, (result[1]-cursor_index[1])*125*k
        cursor_index = result
        animation.MoveItem(canvas, cursor, delta, 240,
                           controller=animation.smooth, fps=60).start()


def move_mark(x: int, y: int) -> None:
    """移动标记的位置"""
    if player != board[x][y].color:
        return
    global selected_piece
    selected_piece = board[x][y]
    k = min(canvas.ratios)
    x, y = index_to_position(x, y)
    canvas.coords(mark, (x-5)*k, (y-5)*k, (x+60+5)*k, (y+60+5)*k)


def init() -> None:
    """初始化棋盘"""
    canvas.create_line(50, 50, 550, 550, fill="black")
    canvas.create_line(550, 50, 50, 550, fill="black")
    canvas.create_line(300, 50, 300, 550, fill="black")
    canvas.create_line(50, 50, 550, 50, fill="black")
    canvas.create_line(50, 550, 550, 550, fill="black")
    canvas.create_line(175, 175, 425, 175, fill="black")
    canvas.create_line(175, 425, 425, 425, fill="black")
    canvas.create_line(175, 300, 425, 300, fill="black")

    for x in range(5):
        for y in range(5):
            if board[x][y] == -1:
                cx, cy = x*125 + 20 + 30, y*125 + 20 + 30
                canvas.create_oval(cx-30, cy-30, cx+30, cy+30,
                                   outline="black", fill=canvas["bg"])

    Piece(canvas, (0, 0), "black", "将")
    Piece(canvas, (2, 0), "black", "将")
    Piece(canvas, (4, 0), "black", "将")
    Piece(canvas, (1, 1), "black", "将")
    Piece(canvas, (2, 1), "black", "将")
    Piece(canvas, (3, 1), "black", "将")
    Piece(canvas, (1, 2), "black", "将")
    Piece(canvas, (3, 2), "black", "将")
    Piece(canvas, (2, 2), "white", "王")


def click(event: tkinter.Event) -> None:
    """点击事件的处理"""
    global selected_piece, player
    k = min(canvas.ratios)
    x, y = event.x/k, event.y/k
    result = position_to_index(x, y)
    if result is not None and selected_piece is not None:
        ok = get_ok_pos(selected_piece)
        pos = [data[:-1] for data in ok]
        if result in pos:
            dx, dy = result[0]-selected_piece.bx, result[1]-selected_piece.by
            delta = dx*125*k, dy*125*k
            animation.MoveWidget(selected_piece, delta, 500,
                                 controller=animation.smooth, fps=60).start()
            if ok[pos.index(result)][-1]:
                kx, ky = result[0]-dx//2, result[1]-dy//2
                board[kx][ky].destroy()
                board[kx][ky] = -1
            board[selected_piece.bx][selected_piece.by] = -1
            board[result[0]][result[1]] = selected_piece
            selected_piece.bx, selected_piece.by = result[0], result[1]
            if winner() is True:
                dialogs.TkMessage("The white win!")
            elif winner() is False:
                dialogs.TkMessage("The black win!")
            player = "black" if player == "white" else "white"
    canvas.coords(mark, 0, 0, 0, 0)
    selected_piece = None


def is_one_line(c1: tuple[int, int], c2: tuple[int, int]) -> bool:
    """判断两点是否在同一直线上"""
    if c1[1] == c2[1]:
        return True
    if c1[0] == 2 and c2[0] == 2:
        return True
    if c1[0] == c1[1] and c2[0] == c2[1]:
        return True
    if c1[0] == 4-c1[1] and c2[0] == 4-c2[1]:
        return True
    return False


def get_ok_pos(piece: Piece) -> list[tuple[int, int, bool]]:
    """获取指定棋子可走的位置"""
    x, y = piece.bx, piece.by
    ok = list((*pos, False)
              for pos in filter(lambda p: board[p[0]][p[1]] == -1, GRAPH[(x, y)]))
    if piece.color == "white":
        for pos in GRAPH[(x, y)]:
            if board[pos[0]][pos[1]] != -1:
                for pos2 in GRAPH[pos]:
                    if board[pos2[0]][pos2[1]] == -1:
                        if is_one_line((x, y), pos2):
                            ok.append((*pos2, True))
    return ok


def winner() -> bool | None:
    """判断当前是否出现输赢的情况"""
    has_black = False
    for line in board:
        for piece in line:
            if isinstance(piece, Piece):
                if piece.color == "black":
                    has_black = True
                elif piece.color == "white":
                    if not get_ok_pos(piece):
                        return False  # 白方输
    if not has_black:
        return True  # 黑方输
    return None


GRAPH = {  # 棋盘位置连通数据
    (0, 0): [(2, 0), (1, 1)],
    (2, 0): [(0, 0), (2, 1), (4, 0)],
    (4, 0): [(2, 0), (3, 1)],
    (0, 4): [(2, 4), (1, 3)],
    (2, 4): [(0, 4), (2, 3), (4, 4)],
    (4, 4): [(2, 4), (3, 3)],
    (1, 1): [(0, 0), (2, 1), (2, 2)],
    (2, 1): [(1, 1), (2, 0), (3, 1), (2, 2)],
    (3, 1): [(4, 0), (2, 1), (2, 2)],
    (1, 3): [(0, 4), (2, 3), (2, 2)],
    (2, 3): [(1, 3), (2, 4), (3, 3), (2, 2)],
    (3, 3): [(4, 4), (2, 3), (2, 2)],
    (1, 2): [(2, 2)],
    (2, 2): [(1, 2), (2, 1), (3, 2), (2, 3), (1, 1), (3, 1), (1, 3), (3, 3)],
    (3, 2): [(2, 2)],
}

board = [  # 棋盘
    [-1,   None, -1,   None, -1],
    [None, -1,   -1,   -1,   None],
    [None, -1,   -1,   -1,   None],
    [None, -1,   -1,   -1,   None],
    [-1,   None, -1,   None, -1],
]

board = [list(line) for line in zip(*board)]  # 棋盘转置（方便后续编写索引）
cursor_index = 2, 2  # 游标位置
selected_piece: Piece | None = None  # 当前被选中的棋子
player: typing.Literal["white", "black"] = "white"  # 当前玩家

root = maliang.Tk((600, 600), title="Simple Game")  # 根窗口
root.center()  # 窗口屏幕居中
canvas = maliang.Canvas(auto_zoom=True, keep_ratio="min", zoom_all_items=True,
                        free_anchor=True)  # 主画布
canvas.place(width=600, height=600, x=300, y=300, anchor="center")
canvas.bind("<Motion>", move_cursor, add="+")  # 绑定鼠标移动事件
canvas.bind("<Button-1>", click, add="+")  # 绑定鼠标左键点击事件
canvas["bg"] = "#d57125"  # 设定画布背景颜色

init()  # 绘制棋盘

cursor = canvas.create_oval(
    300-30-5, 300-30-5, 300+30+5, 300+30+5, dash="-", outline="white")  # 游标初始化
mark = canvas.create_oval(0, 0, 0, 0, outline="red", width=2)  # 标记点初始化

root.mainloop()  # 进入事件循环
