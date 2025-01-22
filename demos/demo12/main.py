import math

import maliang
import maliang.animation as animation
import maliang.theme as theme

root = maliang.Tk((476, 668))
root.center()
root.alpha(0.95)
theme.customize_window(root, hide_title_bar=True)
root.geometry(size=(476, 668))

cv = maliang.Canvas(auto_zoom=True)
cv.place(width=476, height=668)

photo = maliang.PhotoImage(file="assets/logo.png")

title = maliang.Text(cv, (238, 88), text="DEMO", fontsize=36, anchor="center")

a = animation.GradientItem(cv, title.texts[0].items[0], "fill", ("royalblue", "springgreen"), 2000, controller=lambda p: math.sin(p*math.pi), repeat=-1)
a.start()

maliang.Text(cv, (238, 388), text="小康", fontsize=26, anchor="center")
maliang.Image(cv, (238, 240), image=photo, anchor="center")

maliang.Button(cv, (96, 470), (284, 54), text="登 录").style.set(
    bg=("#00000000", "#2CDB83"), ol=("#2CDB83", "#2CDE85"), fg=("#2CDB83", "black"))

maliang.Env.system = "Windows10"

maliang.Button(cv, (476, 0), (42, 42), text="×", anchor="ne", fontsize=24, command=root.destroy).style.set(
    bg=("#00000000", "red"), ol=("#00000000", "red"))
maliang.Button(cv, (476-42-1, 0), (42, 42), text="-", anchor="ne", fontsize=24, command=root.destroy).style.set(
    bg=("#00000000", "#77777777"), ol=("#00000000", "#77777777"))
maliang.Image(cv, (14, 14), (28, 28), image=maliang.PhotoImage(file="assets/images/logo.png"))

maliang.UnderlineButton(cv, (140, 622), text="添加账号", anchor="sw")
maliang.Text(cv, (238, 622), text="|", anchor="s")
maliang.UnderlineButton(cv, (476-140, 622), text="移除账号", anchor="se")

root.at_exit(a.stop)
root.mainloop()
