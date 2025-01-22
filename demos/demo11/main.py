import itertools
import math
import statistics

import maliang
import maliang.animation.animations as animations
import maliang.animation.controllers as controllers
import maliang.core.configs as configs
import maliang.media as media
import maliang.mpl as mpl
import maliang.theme as theme
import maliang.three as three
import maliang.toolbox as toolbox
import matplotlib.animation as animation
import matplotlib.figure as figure
import numpy

# Optional operations #

# configs.Env.system = "Windows10"

if toolbox.load_font("./assets/fonts/LXGWWenKai-Regular.ttf"):
    configs.Font.family = "LXGW WenKai"

mpl.set_mpl_default_theme(theme.get_color_mode(), apply_font=True)

# Optional operations #


# maliang-mpl-1 #
fig1 = figure.Figure()
ax = fig1.add_subplot()
ax.grid()
ax.set(xlabel='x', ylabel='y', title='Animated line plot')

x = numpy.arange(0, 2*numpy.pi, 0.01)
line, = ax.plot(x, numpy.sin(x))


def animate(i):
    line.set_ydata(numpy.sin(x + i / 50))  # update the data.
    return line,


ani = animation.FuncAnimation(
    fig1, animate, interval=1, blit=True, save_count=50)
# maliang-mpl #


# maliang-mpl-2 #
fig2 = figure.Figure()
ax2 = fig2.add_subplot(projection='3d')

colors = ['r', 'g', 'b', 'y']
yticks = [3, 2, 1, 0]

for c, k in zip(colors, yticks):
    xs = numpy.arange(20)
    ys = numpy.random.rand(20)
    cs = [c] * len(xs)
    cs[0] = 'c'
    ax2.bar(xs, ys, zs=k, zdir='y', color=cs, alpha=0.8)

ax2.set_xlabel('X')
ax2.set_ylabel('Y')
ax2.set_zlabel('Z')
ax2.set_title("3D plotting with interoperability")

ax2.set_yticks(yticks)
# maliang-mpl #


root = maliang.Tk((1920, 1080), title="Extension Test")

# Optional operations #
# theme.customize_window(root, boarder_type="rectangular")
# Optional operations #

root.center()
cv = maliang.Canvas(root, keep_ratio="min", free_anchor=True, auto_zoom=True)
cv.place(width=1920, height=1080, x=960, y=540, anchor="center")

cv_mpl_1 = mpl.FigureCanvas(cv, fig1)
toolbar_1 = mpl.FigureToolbar(cv_mpl_1)
cv_mpl_1.place(width=960, height=540)

cv_mpl_2 = mpl.FigureCanvas(cv, fig2)
toolbar_2 = mpl.FigureToolbar(cv_mpl_2)
cv_mpl_2.place(width=960, height=540, x=960, y=540)

animations.Animation(1000, lambda _: ani._step(), controller=controllers.linear, repeat=-1).start()

# maliang-media #
cv_media = media.VideoCanvas(
    cv, keep_ratio="min", free_anchor=True, controls=True)
cv_media.place(width=960, height=540, x=960)
cv_media.open("./assets/videos/Bad Apple.mp4")
# maliang-media #


# maliang-3d #
space = three.Space(cv, free_anchor=True, auto_zoom=True, highlightthickness=0,
                    keep_ratio="min")
space.configure(bg="black" if theme.get_color_mode() == "dark" else "white")
space.place(width=960, height=540, y=540)
space.update()

theme.register_event(lambda flag: space.configure(
    bg="black" if flag == "dark" else "white"))

m = 150 * math.sqrt(50 - 10 * math.sqrt(5)) / 10
n = 150 * math.sqrt(50 + 10 * math.sqrt(5)) / 10
points = []
dis_side = 150 * (3 * math.sqrt(3) + math.sqrt(15)) / 12 / \
    ((math.sqrt(10 + 2 * math.sqrt(5))) / 4)
count, color_lst = 0, ['00', '77', 'FF']
colors = [f'#{r}{g}{b}' for r in color_lst for g in color_lst for b in color_lst]

for i in m, -m:
    for j in n, -n:
        points.append([0, j, i])
        points.append([i, 0, j])
        points.append([j, i, 0])

for p in itertools.combinations(points, 3):
    dis = math.hypot(*[statistics.mean(c[i] for c in p) for i in range(3)])
    if math.isclose(dis, dis_side):
        three.Plane(space, *p, fill=colors[count], outline='grey')
        count += 1


space.space_sort()


count = 0


def _callback(_: float) -> None:
    """callback function of animation"""
    global count
    count += 0.08
    for item in space.components:
        item.rotate(dy=-0.01, dz=0.02)
        item.translate(dz=math.sin(count))
        item.update()
    space.space_sort()


an = animations.Animation(2000, _callback, controller=controllers.linear,
                          fps=60, repeat=-1, derivation=True)


maliang.Switch(space, (10, 10), command=lambda flag: an.start()
               if flag else an.stop())
# maliang-3d #


root.mainloop()
