import itertools
import math
import statistics

import maliang
import maliang.animation as animation
import maliang.theme as theme
import maliang.three as three

root = maliang.Tk(title="3D Functional Test - Demo7")

space = three.Space(root, free_anchor=True, auto_zoom=True, highlightthickness=0,
                    keep_ratio="min")
space["bg"] = "black" if theme.get_color_mode() == "dark" else "white"
space.place(width=1280, height=720, x=640, y=360, anchor="center")
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


an = animation.Animation(2000, _callback, controller=animation.linear,
                         fps=60, repeat=-1, derivation=True)


maliang.Switch(space, (10, 10), command=lambda flag: an.start()
               if flag else an.stop())

root.mainloop()
