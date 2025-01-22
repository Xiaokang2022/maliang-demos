import random

import maliang
from maliang import animation, theme, toolbox
from maliang.core import configs, virtual
from maliang.standard import shapes, styles

if toolbox.load_font("assets/fonts/LXGWWenKai-Regular.ttf"):
    configs.Font.family = "LXGW WenKai"


def alert(text: str) -> None:
    hint.texts[0].set(text)
    animation.MoveWidget(
        hint, (0, -130*cv.ratios[1]), 500, controller=animation.rebound, fps=60).start()
    animation.MoveWidget(
        hint, (0, 130*cv.ratios[1]), 500, controller=animation.smooth, fps=60).start(delay=2000)


def move_right() -> None:
    for widget in login_widgets:
        animation.MoveWidget(widget, (900*cv.ratios[0], 0), 500, controller=animation.smooth, fps=60).start()
    for widget in signup_widgets:
        animation.MoveWidget(widget, (900*cv.ratios[0], 0), 500, controller=animation.ease_out, fps=60).start(delay=100)


def move_left() -> None:
    for widget in login_widgets:
        animation.MoveWidget(widget, (-900*cv.ratios[0], 0), 500, controller=animation.ease_out, fps=60).start(delay=100)
    for widget in signup_widgets:
        animation.MoveWidget(widget, (-900*cv.ratios[0], 0), 500, controller=animation.smooth, fps=60).start()


def get_random_int(min_num: int, max_num: int, interval: int) -> int:
    a = random.randint(min_num, -interval)
    b = random.randint(interval, max_num)
    return random.choice((a, b))


class MyWidget(virtual.Widget):
    """My customized Widget."""

    def __init__(
        self,
        master: maliang.Canvas,
        position: tuple[int, int] = (0, 0),
        size: tuple[int, int] | None = None,
        *,
        capture_events: bool | None = None,
    ) -> None:
        super().__init__(master, position, size, capture_events=capture_events, style=styles.LabelStyle)
        if configs.Env.system == "Windows10":
            shapes.Rectangle(self)
        else:
            shapes.RoundedRectangle(self, radius=16)


tk = maliang.Tk(title="Login Window")
cv = maliang.Canvas(auto_zoom=True, free_anchor=True, keep_ratio="max")
cv.place(width=1280, height=720, x=640, y=360, anchor="center")

img = maliang.Image(cv, (0, 0), image=maliang.PhotoImage(
    file=f"./assets/images/{theme.get_color_mode()}.png"))

theme.register_event(lambda theme: img.set(maliang.PhotoImage(
    file="./assets/images/%s.png" % theme)))


login_widgets = [
    MyWidget(cv, (450, 70), (400, 560)),
    maliang.Switch(cv, (330+440, 20+70), default=theme.get_color_mode() == "dark",
                   command=lambda flag: theme.set_color_mode("dark" if flag else "light")),
    maliang.Text(cv, (200+450, 80+70), text="Login",
                 fontsize=48, weight="bold", anchor="center"),
    maliang.Text(cv, (30+450, 170+70), anchor="w",
                 text="Account", fontsize=24),
    maliang.InputBox(cv, (25+450, 190+70), (350, 50),
                     placeholder="Please enter your account"),
    maliang.Text(cv, (30+450, 280+70), anchor="w",
                 text="Password", fontsize=24),
    maliang.InputBox(cv, (25+450, 300+70), (350, 50),
                     show="●", placeholder="Please enter your password"),
    maliang.Button(cv, (25+450, 380+70), (350, 55),
                   text="Login", command=lambda: alert("Login Success!")),
    maliang.Text(cv, (135+450, 470+70),
                 text="Do not have an account?", fontsize=18, anchor="center"),
    maliang.UnderlineButton(cv, (340+450, 470+70), anchor="center",
                            text="Sign up", fontsize=18, command=move_right)
]
login_widgets[4].style.set(bg_bar=(..., ..., "deepskyblue"))
login_widgets[6].style.set(bg_bar=(..., ..., "deepskyblue"))
login_widgets[-3].style.set(fg=("deepskyblue", "black"), bg=("#00000000", "deepskyblue"), ol=("deepskyblue", "deepskyblue"))

signup_widgets = [
    MyWidget(cv, (450-900, 70), (400, 560)),
    maliang.Text(cv, (200+450-900, 80+70),
                 text="Sign up", fontsize=48, weight="bold", anchor="center"),
    maliang.Text(cv, (30+450-900, 170+70),
                 anchor="w", text="Account", fontsize=24),
    maliang.InputBox(cv, (25+450-900, 190+70), (350, 50),
                     placeholder="Please enter your account"),
    maliang.Text(cv, (30+450-900, 280+70), anchor="w",
                 text="Password", fontsize=24),
    maliang.InputBox(cv, (25+450-900, 300+70), (350, 50),
                     show="●", placeholder="Please enter your password"),
    maliang.Button(cv, (25+450-900, 380+70), (350, 55),
                   text="Sign Up", command=lambda: alert("Sign Up Success!")),
    maliang.Text(cv, (135+450-900, 470+70),
                 text="Already have an account?", fontsize=18, anchor="center"),
    maliang.UnderlineButton(cv, (350+450-900, 470+70), anchor="center",
                            text="Login", fontsize=18, command=move_left)
]
signup_widgets[3].style.set(bg_bar=(..., ..., "#2CDE85"))
signup_widgets[5].style.set(bg_bar=(..., ..., "#2CDE85"))
signup_widgets[-3].style.set(fg=("#2CDB83", "black"), bg=("#00000000", "#2CDE85"), ol=("#2CDB83", "#2CDE85"))

hint = maliang.Label(cv, (960, 730), (300, 100))

tk.mainloop()
