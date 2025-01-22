import math
import random
import webbrowser

import maliang
from maliang import animation, theme, toolbox
from maliang.color import convert, rgb
from maliang.core import configs, virtual
from maliang.standard import dialogs, features, images, shapes, texts

tk = maliang.Tk(title="Basic Test")
tk.center()
cv = maliang.Canvas(auto_zoom=True, keep_ratio="min", free_anchor=True)
cv.place(width=1280, height=720, x=640, y=360, anchor="center")

if toolbox.load_font("./assets/fonts/LXGWWenKai-Regular.ttf"):
    configs.Font.family = "LXGW WenKai"

configs.Font.size = -24

ORIGIN_SYSTEM = configs.Env.system

img = maliang.Image(cv, (0, 0), image=maliang.PhotoImage(
    file=f"./assets/images/{theme.get_color_mode()}.png"))

theme.register_event(lambda theme: img.set(
    maliang.PhotoImage(file=f"./assets/images/{theme}.png")))


### Data Card (RGBA - Experimental) ###


maliang.Label(cv, (620, 390), (240, 310)).style.set(
    bg=("#448AFF33", "#00BFA533"), ol=("#448AFF", "#00BFA5"))

maliang.Text(cv, (740, 430), text="— RGBA Card —", anchor="center")
maliang.UnderlineButton(
    cv, (740, 490), text="Home Page", capture_events=False, anchor="center",
    command=lambda: webbrowser.open_new_tab("https://xiaokang2022.github.io/maliang/"))
maliang.UnderlineButton(
    cv, (740, 530), text="GitHub (Source)", capture_events=False, anchor="center",
    command=lambda: webbrowser.open_new_tab("https://github.com/Xiaokang2022/maliang"))
maliang.UnderlineButton(
    cv, (740, 570), text="Gitee (Mirror)", capture_events=False, anchor="center",
    command=lambda: webbrowser.open_new_tab("https://gitee.com/xiaokang-2022/maliang"))
maliang.UnderlineButton(
    cv, (740, 610), text="GitCode (Mirror)", capture_events=False, anchor="center",
    command=lambda: webbrowser.open_new_tab("https://gitcode.com/Xiaokang2022/maliang"))
maliang.UnderlineButton(
    cv, (740, 650), text="Bug Reports", capture_events=False, anchor="center",
    command=lambda: webbrowser.open_new_tab("https://github.com/Xiaokang2022/maliang/issues"))


### Here's the customization section ###


class MyToplevel(maliang.Toplevel):
    """My Customized Toplevel."""

    def __init__(self, *args, **kwargs) -> None:
        configs.Env.system = ORIGIN_SYSTEM
        super().__init__(*args, size=(720, 405), **kwargs)
        self.transient(self.master)
        self.center(refer=self.master)
        self.canvas = canvas = maliang.Canvas(self, free_anchor=True, expand="")
        canvas.place(width=720, height=405, x=360, y=202, anchor="center")
        canvas.create_rectangle(40, 40, 120, 120, dash="-", outline="grey")
        canvas.create_text(80, 25, text="Shape", fill="grey")
        self.s = canvas.create_text(80, 80, fill="red", justify="center")
        canvas.create_line([120, 80, 180, 80, 180, 160, 220, 160], fill="grey", arrow="last")
        canvas.create_rectangle(40, 160, 120, 240, dash="-", outline="grey")
        canvas.create_text(80, 145, text="Text", fill="grey")
        canvas.create_line(120, 202.5, 220, 202.5, fill="grey", arrow="last")
        canvas.create_rectangle(40, 280, 120, 360, dash="-", outline="grey")
        canvas.create_text(80, 265, text="Image", fill="grey")
        canvas.create_line([120, 320, 180, 320, 180, 240, 220, 240], fill="grey", arrow="last")
        canvas.create_rectangle(540, 40, 680, 120, dash="-", outline="grey")
        canvas.create_text(610, 25, text="Feature", fill="grey")
        self.f = canvas.create_text(610, 80, fill="purple")
        canvas.create_rectangle(540, 160, 680, 240, dash="-", outline="grey")
        canvas.create_text(610, 145, text="Style", fill="grey")
        canvas.create_text(610, 200, text="Random", fill="grey")
        canvas.create_rectangle(220, 70, 500, 350, dash=".", outline="red")
        canvas.create_text(360, 40, text="Widget", fill="red")

        self.shape: type[virtual.Shape] | None = None
        self.text: type[virtual.Text] = texts.Information
        self.image: type[virtual.Image] = images.StillImage
        self.widget: virtual.Widget | None = None

        maliang.Button(canvas, (720-20, 405-80), text="Clear", command=self.clear, anchor="se")
        maliang.Button(canvas, (720-20, 405-20), text="Generate", command=self.generate, anchor="se")

    def generate(self) -> None:
        """Generate a Widget randomly."""
        self.clear()
        self.shape = random.choice(
            [shapes.Rectangle, shapes.Oval, shapes.Parallelogram,
             shapes.SharpRectangle, shapes.RegularPolygon,
             shapes.RoundedRectangle, shapes.SemicircularRectangle])
        feature = random.choice(
            [features.LabelFeature, features.ButtonFeature, features.Underline, features.Highlight])
        name = random.choice(["C", "C++", "C#", "Python", "Java", "Minecraft", "Ubuntu", "Windows", "Linux"])
        image = maliang.PhotoImage(file=f"./assets/images/logo-{name}.png").resize(64, 64)
        self.widget = virtual.Widget(self.canvas, (300, 162), (120, 80))
        kw = {}
        match self.shape:
            case shapes.RegularPolygon: kw["side"] = random.randint(3, 9)
            case shapes.Parallelogram: kw["theta"] = random.uniform(-math.pi/6, math.pi/3)
            case shapes.RoundedRectangle: kw["radius"] = random.randint(4, 25)
            case shapes.SharpRectangle:
                kw["theta"] = random.uniform(math.pi/6, math.pi/3)
                kw["ratio"] = random.uniform(0, 1), random.uniform(0, 1)
        try:
            self.shape(self.widget, **kw)
            self.shape(self.widget, (-280, -120), **kw)

            self.widget.style.init(0)
            self.widget.style[0]["normal"] = {"fill": self.randcolor(), "outline": self.randcolor()}
            self.widget.style[0]["hover"] = {"fill": self.randcolor(), "outline": self.randcolor()}
            self.widget.style[0]["active"] = {"fill": self.randcolor(), "outline": self.randcolor()}
        except Exception:
            self.canvas.itemconfigure(self.s, text="Param\nError")

        dx, dy = round(self.widget.size[0]/2), round(self.widget.size[1]/2)
        self.image(self.widget, (dx-32, dy-32), size=(64, 64), image=image)
        self.image(self.widget, (-280 + dx - 32, 120 + dy - 32), (64, 64), image=image)

        text = random.choice(["歪比八卜", "锟斤拷", "烫烫烫", ":-)", "$#4&.^%!"])
        self.text(self.widget, text=text)
        self.text(self.widget, (-280, 0), text=text)

        self.widget.style.init(2)
        self.widget.style[2]["normal"] = {"fill": self.randcolor()}
        self.widget.style[2]["hover"] = {"fill": self.randcolor()}
        self.widget.style[2]["active"] = {"fill": self.randcolor()}

        self.canvas.itemconfigure(self.f, text=feature.__name__)
        self.widget.feature = feature(self.widget)
        self.widget.update()

    def randcolor(self) -> str:
        """Get a random color string."""
        num = random.randint(0, (1 << 24) - 1)
        return f"#{num:06X}"

    def clear(self) -> None:
        """Clear Widget."""
        if self.widget is not None:
            self.widget.destroy()
            self.widget = None
        self.canvas.itemconfigure(self.s, text="")
        self.canvas.itemconfigure(self.f, text="")


### Below is the section of the style following system ###


maliang.Switch(cv, (50, 35), default=theme.get_color_mode() == "dark",
               command=lambda b: theme.set_color_mode("dark" if b else "light"))
maliang.CheckBox(cv, (125, 35), command=tk.fullscreen)


t0 = maliang.Text(cv, (440, 50), fontsize=26, anchor="center", auto_update=False,
                  text="maliang 3: a Brand New UI Framework")

maliang.HighlightButton(cv, (790, 50), text="Get More!",
                        command=MyToplevel, anchor="center")

maliang.Button(cv, (900, 405), (360, 50), text="Call a Nested Window",
               command=lambda: toolbox.embed_window(maliang.Toplevel(), tk))
maliang.Button(cv, (900, 465), (360, 50),
               text="Call a Font Chooser", command=dialogs.TkFontChooser)
maliang.Button(cv, (900, 525), (360, 50),
               text="Call a Color Chooser", command=dialogs.TkColorChooser)

maliang.Button(cv, (900, 585), (175, 50), text="Information",
               command=lambda: dialogs.TkMessage(icon="info")
               ).style.set(bg=("royalblue", "deepskyblue"))

maliang.Button(cv, (900 + 185, 585), (175, 50), text="Question",
               command=lambda: dialogs.TkMessage(icon="question")
               ).style.set(bg=("green", "forestgreen"))

maliang.Button(cv, (900, 645), (175, 50), text="Warning",
               command=lambda: dialogs.TkMessage(icon="warning")
               ).style.set(bg=("darkorange", "orange"))

maliang.Button(cv, (900 + 185, 645), (175, 50), text="Error",
               command=lambda: dialogs.TkMessage(icon="error")
               ).style.set(bg=("darkred", "red"))


random_color = f"#{random.randint(0, (1 << 24) - 1):06X}"
contast_color = convert.rgb_to_hex(rgb.contrast(convert.str_to_rgb(random_color)))

animation.GradientItem(
    cv, t0.texts[0].items[0], "fill", (random_color, contast_color), 2000,
    repeat=-1, controller=lambda x: math.sin(x*math.pi)).start()


### Here's the part for customizing the system ###


configs.Env.system = "Windows11"

maliang.Label(cv, (50, 100), (120, 50), text="Label")
maliang.Label(cv, (180, 100), (120, 50), text="Label").disable()
maliang.Label(cv, (310, 100), (120, 50), text="Label").style.set(
    fg=("#5E8BDE", "#FFAC33"), bg=("", ""), ol=("#5E8BDE", "#FFAC33"))

maliang.Button(cv, (50, 180), (120, 50), text="Button")
maliang.Button(cv, (180, 180), (120, 50), text="Button").disable()
maliang.Button(cv, (310, 180), (120, 50), text="Button").style.set(
    bg=("#5E8BDE", "#CCCC00", "#FFAC33"), ol=("#5E8BDE", "#CCCC00", "#FFAC33"))

pb1 = maliang.ProgressBar(cv, (50, 260), (380, 8))
pb2 = maliang.ProgressBar(cv, (50, 280), (380, 8))
pb2.style.set(bg_slot="", ol_slot="", bg_bar="gold", ol_bar="gold")

animation.Animation(2000, pb1.set, controller=animation.smooth,
                    fps=60, repeat=-1).start(delay=1500)
animation.Animation(2000, pb2.set, controller=animation.smooth,
                    fps=60, repeat=-1).start(delay=1000)

pb3 = maliang.ProgressBar(cv, (50, 315), (380, 20))
pb4 = maliang.ProgressBar(cv, (50, 350), (380, 20))
pb4.style.set(bg_slot="", ol_slot="grey", bg_bar="red", ol_bar="red")

animation.Animation(2000, pb3.set, controller=animation.smooth,
                    fps=60, repeat=-1).start(delay=500)
animation.Animation(2000, pb4.set, controller=animation.smooth,
                    fps=60, repeat=-1).start()

maliang.CheckBox(cv, (50, 390))
maliang.Text(cv, (165, 390 + 15), text="CheckBox", anchor="center")
rb1 = maliang.RadioBox(cv, (250, 390 + 3))
maliang.Text(cv, (355, 390 + 15), text="RadioBox", anchor="center")
maliang.Text(cv, (460, 390 + 15), text="Off", anchor="center")
maliang.Switch(cv, (490, 390))
maliang.Text(cv, (580, 390 + 15), text="On", anchor="center")

maliang.CheckBox(cv, (50, 440), default=True).disable()
maliang.Text(cv, (165, 440 + 15), text="CheckBox", anchor="center").disable()
maliang.RadioBox(cv, (250, 440 + 3), default=True).disable()
maliang.Text(cv, (355, 440 + 15), text="RadioBox", anchor="center").disable()
maliang.Text(cv, (460, 440 + 15), text="Off", anchor="center").disable()
maliang.Switch(cv, (490, 440), default=True).disable()
maliang.Text(cv, (580, 440 + 15), text="On", anchor="center").disable()

maliang.InputBox(cv, (50, 595 - 5), (270, 50), placeholder="Placeholder")
ib = maliang.InputBox(cv, (50, 655 - 5), (270, 50))
ib.set("Input")
ib.disable()

configs.Env.system = "Windows10"

maliang.Label(cv, (50 + 410, 100), (120, 50), text="Label")
maliang.Label(cv, (180 + 410, 100), (120, 50), text="Label").disable()
maliang.Label(cv, (310 + 410, 100), (120, 50), text="Label", auto_update=False)

maliang.Button(cv, (50 + 410, 180), (120, 50), text="Button")
maliang.Button(cv, (180 + 410, 180), (120, 50), text="Button").disable()
maliang.Button(cv, (310 + 410, 180), (120, 50), text="Button").style.set(
    bg=("", "yellow"), fg=("", "black"), ol=("", "red"))

pb5 = maliang.ProgressBar(cv, (50 + 410, 260), (380, 8))
pb6 = maliang.ProgressBar(cv, (50 + 410, 280), (380, 8))
pb6.style.set(bg_slot="orange", ol_slot="orange", bg_bar="red", ol_bar="red")

animation.Animation(2000, pb5.set, controller=animation.linear,
                    fps=60, repeat=-1).start()
animation.Animation(2000, pb6.set, controller=animation.linear,
                    fps=60, repeat=-1).start(delay=500)

pb7 = maliang.ProgressBar(cv, (50 + 410, 315), (380, 20))
pb8 = maliang.ProgressBar(cv, (50 + 410, 350), (380, 20))
pb8.style.set(bg_slot="", ol_slot="", bg_bar="purple", ol_bar="cyan")

animation.Animation(2000, pb7.set, controller=animation.linear,
                    fps=60, repeat=-1).start(delay=1000)
animation.Animation(2000, pb8.set, controller=animation.linear,
                    fps=60, repeat=-1).start(delay=1500)

maliang.CheckBox(cv, (50, 490))
maliang.Text(cv, (165, 490 + 15), text="CheckBox", anchor="center")
rb2 = maliang.RadioBox(cv, (250, 490 + 3))
maliang.Text(cv, (355, 490 + 15), text="RadioBox", anchor="center")
maliang.Text(cv, (460, 490 + 15), text="Off", anchor="center")
maliang.Switch(cv, (490, 490))
maliang.Text(cv, (580, 490 + 15), text="On", anchor="center")

maliang.CheckBox(cv, (50, 540)).disable()
maliang.Text(cv, (165, 540 + 15), text="CheckBox", anchor="center").disable()
maliang.RadioBox(cv, (250, 540 + 3)).disable()
maliang.Text(cv, (355, 540 + 15), text="RadioBox", anchor="center").disable()
maliang.Text(cv, (460, 540 + 15), text="Off", anchor="center").disable()
maliang.Switch(cv, (490, 540)).disable()
maliang.Text(cv, (580, 540 + 15), text="On", anchor="center").disable()

maliang.RadioBox.group(rb1, rb2)

maliang.InputBox(cv, (50 + 280, 595 - 5), (270, 50), align="center").style.set(bg=("", "", ""))
maliang.InputBox(cv, (50 + 280, 655 - 5), (270, 50)).disable()

t1 = maliang.Text(cv, (1210, 20), text="0%", anchor="nw")
maliang.Slider(cv, (900, 20), (300, 30),
               command=lambda k: (t1.set(f"{int(k*100):d}%"), tk.alpha(k))).set(0.95)
maliang.Slider(cv, (900, 60), (300, 30)).disable()

maliang.IconButton(cv, (900, 200), text="C", image=maliang.PhotoImage(
    file="./assets/images/logo-C.png"))
maliang.IconButton(cv, (980, 200), text="C++", image=maliang.PhotoImage(
    file="./assets/images/logo-C++.png"))
maliang.IconButton(cv, (1090, 200), text="C#", image=maliang.PhotoImage(
    file="./assets/images/logo-C#.png"))

maliang.IconButton(cv, (900, 300), text="Minecraft", image=maliang.PhotoImage(
    file="./assets/images/logo-Minecraft.png"))
maliang.IconButton(cv, (1070, 300), text="Ubuntu", image=maliang.PhotoImage(
    file="./assets/images/logo-Ubuntu.png"))

configs.Env.system = "Windows11"

t2 = maliang.Text(cv, (1210, 100), text="0%", anchor="nw")
maliang.Slider(cv, (900, 100), (300, 30),
               command=lambda k: t2.set(f"{int(k*100):d}%")).set(0.5)
maliang.Slider(cv, (900, 140), (300, 30)).disable()

maliang.IconButton(cv, (900, 250), text="Python", image=maliang.PhotoImage(
    file="./assets/images/logo-Python.png"))
maliang.IconButton(cv, (1040, 250), text="Java", image=maliang.PhotoImage(
    file="./assets/images/logo-Java.png"))
maliang.IconButton(cv, (1150, 250), text="maliang", image=maliang.PhotoImage(
    file="./assets/images/logo.png"))

maliang.IconButton(cv, (900, 350), text="Windows", image=maliang.PhotoImage(
    file="./assets/images/logo-Windows.png"))
maliang.IconButton(cv, (1060, 350), text="Linux", image=maliang.PhotoImage(
    file="./assets/images/logo-Linux.png"))

tk.mainloop()
