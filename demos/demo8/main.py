import math

import maliang
import maliang.theme as theme
import maliang.three as three

root = maliang.Tk((1600, 900), title="3D Test - Demo8")
space = three.Space(root, keep_ratio="min", free_anchor=True, highlightthickness=0)
space["bg"] = "black" if theme.get_color_mode() == "dark" else "white"
space.place(width=1600, height=900, x=800, y=450, anchor="center")
space.update()

theme.register_event(lambda flag: space.configure(
    bg="black" if flag == "dark" else "white"))

r = 300

O = three.Point(space, [0, 0, 0], fill='white', size=3)
X = three.Line(space, [0, 0, 0], [1, 0, 0], fill='')
Y = three.Line(space, [0, 0, 0], [0, 1, 0], fill='')
Z = three.Line(space, [0, 0, 0], [0, 0, 1], fill='')

ring = {'x': [], 'y': [], 'z': []}  # type: dict[str, list[three.Text3D]]
line = {'x': [], 'y': [], 'z': []}  # type: dict[str, list[three.Text3D]]

for i in range(26):
    t = chr(65+i)
    φ = i/26 * math.tau
    c1 = r * math.sin(φ)
    c2 = r * math.cos(φ)
    ring['x'].append(three.Text3D(space, [0, c1, c2], text=t, fill='#FF0000'))
    ring['y'].append(three.Text3D(space, [c1, 0, c2], text=t, fill='#00FF00'))
    ring['z'].append(three.Text3D(space, [c1, c2, 0], text=t, fill='#0000FF'))

for i in range(10):
    t = str(i)
    c = (i+1) * 600/11 - r
    line['x'].append(three.Text3D(space, [c, 0, 0], text=t, fill='#00FFFF'))
    line['y'].append(three.Text3D(space, [0, c, 0], text=t, fill='#FF00FF'))
    line['z'].append(three.Text3D(space, [0, 0, c], text=t, fill='#FFFF00'))


def animation():
    for obj3D in ring['x']:
        obj3D.rotate(0.05, axis=X.coordinates)
    for obj3D in ring['y']:
        obj3D.rotate(0.05, axis=Y.coordinates)
    for obj3D in ring['z']:
        obj3D.rotate(0.05, axis=Z.coordinates)
    for obj3D in line['x']:
        obj3D.rotate(-0.05, axis=Y.coordinates)
    for obj3D in line['y']:
        obj3D.rotate(-0.05, axis=Z.coordinates)
    for obj3D in line['z']:
        obj3D.rotate(-0.05, axis=X.coordinates)
    for obj3D in space.components:
        obj3D.rotate(0, -0.01, 0.01, center=O.center())
        obj3D.update()
    root.after(10, animation)


animation()
root.mainloop()
