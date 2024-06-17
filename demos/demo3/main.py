import time

import tkintertools as tkt
import tkintertools.three as three

root = tkt.Tk(title="3D Performance Test")

space = three.Space(root, zoom_item=True, free_anchor=True, keep_ratio="min")
space.place(width=1280, height=720, x=640, y=360, anchor="center")

space.update()

for i in range(100):
    three.Cuboid(space, -100, -100, -100, 200, 200, 200,
                 color_fill_back="red",
                 color_fill_down="orange",
                 color_fill_front="yellow",
                 color_fill_left="green",
                 color_fill_right="blue",
                 color_fill_up="purple")

fps = 0
count = 0


def _callback() -> None:
    """callback function of animation"""
    global fps, count
    count += 1
    t = time.time()
    for item in space.geometries:
        item.rotate(dy=-0.01)
        item.update()
    space.space_sort()
    fps += 1/(time.time() - t)
    print(f"\r{fps/count:.2f}", end="")
    space.after(1, _callback)


_callback()
root.mainloop()
