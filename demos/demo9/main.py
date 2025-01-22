import itertools
import math
import statistics
import time
import typing
import webbrowser

import maliang
import maliang.animation as animation
import maliang.color as color
import maliang.color.hsl as hsl
import maliang.color.rgb as rgb
import maliang.core.configs as configs
import maliang.mpl as mpl
import maliang.standard.dialogs as dialogs
import maliang.theme as theme
import maliang.three as three
import maliang.toolbox as toolbox
import matplotlib.figure as figure
import numpy

if toolbox.load_font("./assets/fonts/LXGWWenKai-Regular.ttf"):
    configs.Font.family = "LXGW WenKai"

mpl.set_mpl_default_theme(theme.get_color_mode())


class App(maliang.Tk):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        frame_side = maliang.Canvas(self, width=320, expand="x")
        frame_side.pack(fill="y", side="left")
        self.frame_main = frame_main = maliang.Canvas(self, auto_zoom=True)
        frame_main.pack(fill="both", expand=True)

        maliang.Image(frame_main, (480, 240), image=maliang.PhotoImage(
            file="./assets/logo.png"), anchor="center")

        maliang.Text(frame_main, (480, 360), text="Choose a test,\nAnd just have fun!",
                     fontsize=32, justify="center", anchor="center")

        github = "https://github.com/Xiaokang2022/maliang"
        maliang.UnderlineButton(frame_main, (480, 560), text=github, anchor="center",
                                command=lambda: webbrowser.open_new_tab(github))

        self.load_canvas_side(frame_side)

    def load_canvas_side(self, frame: maliang.Canvas) -> None:
        canvas = maliang.Canvas(
            frame, expand="y", highlightthickness=0)
        canvas.place(width=320, height=720)
        title = maliang.Text(canvas, (160, 50), text="maliang",
                             fontsize=32, anchor="center")
        sub_title = maliang.Text(
            canvas, (160, 90), text="3.0.0rc (Pre-release)", anchor="center")

        sizes = ((270, 50),)*10
        text = ("Basic Test", "Window Test", "Text Test", "Image Test",
                "Matplotlib Test", "3D Test", "Animation Test", "Dialog Test",
                "Color Test", "About maliang")

        maliang.SegmentedButton(canvas, (20, 140), sizes,
                                text=text, command=self.call_canvas, layout="vertical")

        animation.GradientItem(
            canvas, title.texts[0].items[0], "fill", ("red", "orange"), 2000, controller=lambda p: math.sin(p*math.pi), repeat=-1).start()
        animation.GradientItem(
            canvas, sub_title.texts[0].items[0], "fill", ("green", "cyan"), 2000, controller=lambda p: math.sin(p*math.pi), repeat=-1).start()

    def call_canvas(self, index: int) -> None:
        """"""
        match index:
            case 0: BasicestCanvas(self.frame_main, auto_zoom=True, free_anchor=True, keep_ratio="min")
            case 1: WindowTestCanvas(self.frame_main, auto_zoom=True, free_anchor=True, keep_ratio="min")
            case 2: TextTestCanvas(self.frame_main, auto_zoom=True, free_anchor=True, keep_ratio="min")
            case 3: ImageTestCanvas(self.frame_main, auto_zoom=True, free_anchor=True, keep_ratio="min")
            case 4: MplTestCanvas(self.frame_main, auto_zoom=True, free_anchor=True, keep_ratio="min")
            case 5: ThreeDTestCanvas(self.frame_main, auto_zoom=True, free_anchor=True, keep_ratio="min")
            case 6: AnimationTestCanvas(self.frame_main, auto_zoom=True, free_anchor=True, keep_ratio="min")
            case 7: DialogTestCanvas(self.frame_main, auto_zoom=True, free_anchor=True, keep_ratio="min")
            case 8: ColorTestCanvas(self.frame_main, auto_zoom=True, free_anchor=True, keep_ratio="min")
            case 9:
                for canvas in self.frame_main.canvases:
                    canvas.destroy()


class BasicestCanvas(maliang.Canvas):

    def __init__(self, master: maliang.Canvas, *args, **kwargs):
        for canvas in master.canvases:
            canvas.destroy()
        super().__init__(master, *args, **kwargs)
        self.place(width=958, height=540, x=481, y=360, anchor="center")

        maliang.Button(self, (20, 20), text="Button")
        maliang.Button(self, (20, 80), text="Disabled Button").disable()

        maliang.Label(self, (220, 20), text="Label")
        maliang.Label(self, (220, 80), text="Disabled Label").disable()

        maliang.ToggleButton(self, (420, 20), text="ToggleButton")
        maliang.ToggleButton(
            self, (420, 80), text="Disabled ToggleButton").disable()

        maliang.IconButton(self, (680, 20), text="IconButton",
                           image=maliang.PhotoImage(file="./assets/images/logo.png"))
        maliang.IconButton(self, (680, 80), text="Disabled IconButton",
                           image=maliang.PhotoImage(file="./assets/images/logo.png")).disable()

        maliang.Switch(self, (20, 200))
        maliang.Switch(self, (20, 260)).disable()
        maliang.Switch(self, (120, 200), default=True)
        maliang.Switch(self, (120, 260), default=True).disable()

        maliang.CheckBox(self, (220, 200))
        maliang.CheckBox(self, (220, 260)).disable()
        maliang.RadioBox(self, (320, 200))
        maliang.RadioBox(self, (320, 260)).disable()
        maliang.ProgressBar(self, (420, 200)).set(0.5)
        maliang.ProgressBar(self, (420, 260)).disable()

        maliang.SegmentedButton(self, (20, 360), text=(
            "Option1", "Option2", "Option3"), default=0)
        maliang.SegmentedButton(self, (20, 440), text=(
            "Option1", "Option2", "Option3"), default=1).disable()
        maliang.SegmentedButton(self, (360, 360), layout="vertical", text=(
            "Option1", "Option2", "Option3"), default=2)
        maliang.SegmentedButton(self, (500, 360), layout="vertical", text=(
            "Option1", "Option2", "Option3")).disable()

        # widgets.OptionButton(self, (640, 360))
        # widgets.ComboBox(self, (640, 440))
        self.update_idletasks()
        self.zoom()


class WindowTestCanvas(maliang.Canvas):

    def __init__(self, master: maliang.Canvas, *args, **kwargs):
        for canvas in master.canvases:
            canvas.destroy()
        super().__init__(master, *args, **kwargs)
        self.place(width=958, height=540, x=481, y=360, anchor="center")

        maliang.Text(self, (20, 20), text="Appearance (Light / Dark)")
        maliang.Switch(self, (20, 60), default=theme.get_color_mode(
        ) == "dark", command=lambda b: theme.set_color_mode("dark" if b else "light"))

        maliang.Text(self, (350, 20), text="Style (Win10 / Win11)")
        maliang.Switch(self, (350, 60), command=lambda b: self.restart(
            "Windows11" if b else "Windows10"), default=configs.Env.system == "Windows11")

        maliang.Text(self, (650, 20), text="HideTitleBar (False / True)")
        maliang.Switch(self, (650, 60), command=lambda b: theme.customize_window(
            root, hide_title_bar=b))

        modes = 'Rectangular', 'SmallRound', 'Round'
        maliang.Text(self, (20, 140), text="BoaderType")
        maliang.SegmentedButton(self, (20, 180), text=modes, command=lambda i: theme.customize_window(
            root, border_type=modes[i].lower()), default=2)

        text = ["All", "MaxMin", "None"]

        maliang.Text(self, (500, 140), text="HideTitleBarButton")
        maliang.SegmentedButton(self, (500, 180), text=text,
                                command=lambda i: theme.customize_window(root, hide_button=text[i].lower()), default=2)

        styles = ("normal", "mica", "acrylic", "aero", "transparent",
                  "optimised", "win7", "inverse", "native", "popup")
        maliang.Text(self, (20, 280),
                     text="Theme (Only Works on Windows OS!)")
        maliang.SegmentedButton(self, (20, 320), text=styles,
                                command=lambda i: theme.apply_theme(root, theme=styles[i]))

        t = maliang.Text(self, (20, 420), text="Alpha (100%)")
        maliang.Slider(self, (20, 460), (350, 30), command=lambda p: (
            t.texts[0].set("Alpha (%d%%)" % (p*100)), root.alpha(p)), default=root.alpha())

        maliang.Text(self, (450, 420), text="DisabledMaxButton")
        maliang.Switch(self, (450, 460), command=lambda b: theme.customize_window(
            root, disable_maximize_button=b))

        maliang.Text(self, (700, 420), text="DisabledMinButton")
        maliang.Switch(self, (700, 460), command=lambda b: theme.customize_window(
            root, disable_minimize_button=b))
        self.update_idletasks()
        self.zoom()

    def restart(self, win: typing.Literal["Windows10", "Windows11"]) -> None:
        global root
        root.update_idletasks()
        root.destroy()
        configs.Env.system = win
        root = App(
            title="%s %s - %s" % (maliang.__name__, maliang.__version__, configs.Env.system))
        root.center()
        root.mainloop()


class TextTestCanvas(maliang.Canvas):

    def __init__(self, master: maliang.Canvas, *args, **kwargs):
        for canvas in master.canvases:
            canvas.destroy()
        super().__init__(master, *args, **kwargs)
        self.place(width=958, height=540, x=481, y=360, anchor="center")

        self.create_text(
            20, 20, text="This line of text is not scaled and does not respond to the color theme", anchor="nw", fill="grey")

        maliang.Text(self, (20, 100),
                     text="This is a Text widget that can be scaled and actively responds to the color theme")

        maliang.Text(self, (20, 200), text="Normal InputBox")
        maliang.InputBox(self, (20, 240))
        maliang.Text(self, (20, 300), text="Password InputBox")
        maliang.InputBox(self, (20, 340), show="●")
        maliang.Text(self, (20, 400), text="Placeholder InputBox")
        maliang.InputBox(self, (20, 440), placeholder="Placeholder")

        maliang.Text(self, (300, 200), text="SpinBox")
        maliang.SpinBox(self, (300, 240))
        self.update_idletasks()
        self.zoom()


class ImageTestCanvas(maliang.Canvas):

    def __init__(self, master: maliang.Canvas, *args, **kwargs):
        for canvas in master.canvases:
            canvas.destroy()
        super().__init__(master, *args, **kwargs)
        self.place(width=958, height=540, x=481, y=360, anchor="center")

        self.create_text(
            20, 20, text="This image will not be scaled", anchor="nw", fill="grey")
        self.image = maliang.PhotoImage(file="./assets/logo.png")
        self.create_image(20, 60, image=self.image, anchor="nw")

        maliang.Text(self, (20, 260), text="This image can be zoomed")
        maliang.Image(self, (20+64, 300+64), image=self.image)

        self.scaled_image = self.create_image(660, 200, image=self.image)

        sx = maliang.Slider(self, (460, 420),
                            command=lambda x: self.zoom_image(x, sy.get()))
        sy = maliang.Slider(self, (460, 470),
                            command=lambda y: self.zoom_image(sx.get(), y))

        sx.set(0.5)
        sy.set(0.5)
        self.update_idletasks()
        self.zoom()

    def zoom_image(self, x: float, y: float):
        x = (3*x + 1)/2
        y = (3*y + 1)/2
        self.image_copied = self.image.scale(x, y)
        self.itemconfigure(self.scaled_image, image=self.image_copied)


class MplTestCanvas(maliang.Canvas):

    def __init__(self, master: maliang.Canvas, *args, **kwargs):
        for canvas in master.canvases:
            canvas.destroy()
        super().__init__(master, *args, **kwargs)
        self.place(width=958, height=540, x=481, y=360, anchor="center")

        fig = figure.Figure()
        ax = fig.add_subplot(projection='3d')

        colors = ['r', 'g', 'b', 'y']
        yticks = [3, 2, 1, 0]

        for c, k in zip(colors, yticks):
            xs = numpy.arange(20)
            ys = numpy.random.rand(20)
            cs = [c] * len(xs)
            cs[0] = 'c'
            ax.bar(xs, ys, zs=k, zdir='y', color=cs, alpha=0.8)

        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        ax.set_title("Matplotlib 3D Test")

        ax.set_yticks(yticks)

        figure_canvas = mpl.FigureCanvas(self, fig)
        mpl.FigureToolbar(self, figure_canvas)
        figure_canvas.pack(side="top", fill="both", expand=True)
        self.update_idletasks()
        self.zoom()


class ThreeDTestCanvas(three.Space):

    def __init__(self, master: maliang.Canvas, *args, **kwargs):
        for canvas in master.canvases:
            canvas.destroy()
        super().__init__(master, *args, **kwargs)
        self.place(width=958, height=540, x=481, y=360, anchor="center")

        self.update()

        m = 150 * math.sqrt(50 - 10 * math.sqrt(5)) / 10
        n = 150 * math.sqrt(50 + 10 * math.sqrt(5)) / 10
        points = []
        dis_side = 150 * (3 * math.sqrt(3) + math.sqrt(15)) / 12 / \
            ((math.sqrt(10 + 2 * math.sqrt(5))) / 4)
        self.count, color_lst = 0, ['00', '77', 'FF']
        colors = [
            f'#{r}{g}{b}' for r in color_lst for g in color_lst for b in color_lst]

        for i in m, -m:
            for j in n, -n:
                points.append([0, j, i])
                points.append([i, 0, j])
                points.append([j, i, 0])

        for p in itertools.combinations(points, 3):
            dis = math.hypot(*[statistics.mean(c[i] for c in p)
                             for i in range(3)])
            if math.isclose(dis, dis_side):
                three.Plane(self, *p, fill=colors[self.count], outline='grey')
                self.count += 1

        self.space_sort()

        self.count = 0
        self.time = 0
        an = animation.Animation(2000, self._callback, controller=animation.linear,
                                 fps=60, repeat=-1, derivation=True)

        self.fps = maliang.Text(self, (20, 520), text="FPS: -", anchor="sw")
        maliang.Text(self, (20, 20), text="Animation (off / on)")
        maliang.Switch(self, (20, 60), command=lambda flag: an.start()
                       if flag else an.stop())
        self.update_idletasks()
        self.zoom()

    def _callback(self, _: float) -> None:
        """callback function of animation"""
        self.count += 0.08
        for item in self.components:
            item.rotate(dy=-0.01, dz=0.02)
            item.translate(dz=math.sin(self.count))
            item.update()
        self.space_sort()
        t = time.time()
        try:
            self.fps.texts[0].set("FPS: %d" % (1 / (t-self.time)))
        except ZeroDivisionError:
            pass
        self.time = t


class AnimationTestCanvas(maliang.Canvas):

    def __init__(self, master: maliang.Canvas, *args, **kwargs):
        for canvas in master.canvases:
            canvas.destroy()
        super().__init__(master, *args, **kwargs)
        self.place(width=958, height=540, x=481, y=360, anchor="center")

        maliang.Text(self, (20, 20), text="Choose a control function")
        self.s = maliang.SegmentedButton(self, (20, 60), text=(
            "Flat", "Smooth", "Rebound"), default=0)

        maliang.Text(self, (350, 20), text="Duration (ms)")
        self.ms = maliang.SpinBox(self, (350, 60), step=100)

        maliang.Text(self, (600, 20), text="FPS")
        self.fps = maliang.SpinBox(self, (600, 60))

        maliang.Button(self, (100, 480), text="Start",
                       command=lambda: self.move_item(False))
        maliang.Button(self, (20, 480), text="Back",
                       command=lambda: self.move_item(True))

        self.item = self.create_oval(
            100, 300, 150, 350, fill="orange", outline="grey")
        self.update_idletasks()
        self.zoom()

    def move_item(self, back: bool) -> None:
        func = [animation.linear, animation.smooth,
                animation.rebound][self.s.get()]
        ms = int(self.ms.get())
        fps = int(self.fps.get())
        animation.MoveItem(
            self, self.item, (-500 if back else 500, 0), ms, controller=func, fps=fps).start()


class DialogTestCanvas(maliang.Canvas):

    def __init__(self, master: maliang.Canvas, *args, **kwargs):
        for canvas in master.canvases:
            canvas.destroy()
        super().__init__(master, *args, **kwargs)
        self.place(width=958, height=540, x=481, y=360, anchor="center")

        maliang.Text(self, (20, 20), text="Special Dialogs")
        maliang.Button(self, (20, 60), text="Color Chooser",
                       command=dialogs.TkColorChooser)
        maliang.Button(self, (200, 60), text="Font Chooser",
                       command=dialogs.TkFontChooser)
        maliang.Button(self, (380, 60), text="Toplevel", command=maliang.Toplevel)
        maliang.Button(self, (500, 60), text="Embed Toplevel",
                       command=lambda: toolbox.embed_window(maliang.Toplevel(size=(480, 360)), self))

        maliang.Text(self, (20, 150), text="Message Box")

        maliang.Text(self, (20, 200), text="Icon")
        icons = 'error', 'info', 'question', 'warning'
        s1 = maliang.SegmentedButton(self, (20, 240), default=1, text=icons)

        maliang.Text(self, (20, 320), text="Type")
        types = 'abortretryignore', 'ok', 'okcancel', 'retrycancel', 'yesno', 'yesnocancel'
        s2 = maliang.SegmentedButton(self, (20, 360), default=1, text=types)

        maliang.Button(self, (20, 460), text="Generate Message Box!",
                       command=lambda: dialogs.TkMessage("Message", "Detail", icon=icons[s1.get()], option=types[s2.get()]))
        self.update_idletasks()
        self.zoom()


class ColorTestCanvas(maliang.Canvas):

    def __init__(self, master: maliang.Canvas, *args, **kwargs):
        for canvas in master.canvases:
            canvas.destroy()
        super().__init__(master, *args, **kwargs)
        self.place(width=958, height=540, x=481, y=360, anchor="center")

        rgb1 = color.str_to_rgb("red")
        rgb2 = color.str_to_rgb("purple")
        hsl1 = color.rgb_to_hsl(rgb1)
        hsl2 = color.rgb_to_hsl(rgb2)
        rgb3 = 0, 0, 0
        rgb4 = 255, 255, 255
        hsl3 = 0, 0, 0
        hsl4 = math.tau, 1, 1

        maliang.Text(self, (20, 20), text="RGB Garients")

        for i, c in enumerate(rgb.gradient(rgb1, rgb2, 300)):
            self.create_line(20+i, 60, 20+i, 160, fill=color.rgb_to_hex(c))
        for i, c in enumerate(rgb.gradient(rgb3, rgb4, 300)):
            self.create_line(350+i, 60, 350+i, 160, fill=color.rgb_to_hex(c))

        maliang.Text(self, (20, 200), text="HSL Garients")

        for i, c in enumerate(hsl.gradient(hsl1, hsl2, 300)):
            self.create_line(20+i, 240, 20+i, 340,
                             fill=color.rgb_to_hex(color.hsl_to_rgb(c)))
        for i, c in enumerate(hsl.gradient(hsl3, hsl4, 300)):
            self.create_line(350+i, 240, 350+i, 340,
                             fill=color.rgb_to_hex(color.hsl_to_rgb(c)))

        maliang.Text(self, (700, 20), text="RGBA (Experimental)")

        maliang.Label(self, (700, 60), (200, 280)).style.set(
            bg=("#448AFF33", "#00BFA533"), ol=("#448AFF", "#00BFA5"))
        self.zoom()


root = App(title=f"{maliang.__name__} {maliang.__version__} - {configs.Env.system}")
root.center()
root.mainloop()
