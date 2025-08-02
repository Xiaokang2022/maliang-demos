"""A super pretty calculator."""

import maliang
import maliang.theme

maliang.theme.set_color_mode("dark")

maliang.Env.gradient_animation = False
# maliang.Env.system = "Windows10"

root = maliang.Tk((480, 750), title="计算器", icon="")
maliang.theme.apply_theme(root, theme="acrylic")
# maliang.theme.customize_window(root, border_type="rectangular")
canvas = maliang.Canvas(auto_zoom=True)
canvas["bg"] = "#000000"
canvas.place(width=480, height=750)

matrix_signs = (
    ("ln", "-/+", "0", ".", "="),
    ("log", "1", "2", "3", "+"),
    ("10ᕽ", "4", "5", "6", "-"),
    ("x", "7", "8", "9", "×"),
    ("√", "(", ")", "n!", "÷"),
    ("x²", "1/x", "|x|", "exp", "mod"),
    ("2", "π", "e", "C", "⌫"),
)

for j, signs in enumerate(matrix_signs):
    for i, sign in enumerate(signs):
        maliang.Button(canvas, (i*95 + 5, 750 - 7 - j*55), (90, 50), text=sign, anchor="sw")

menu = maliang.Button(canvas, (4, 13), (59, 53), text="≡", fontsize=28)
menu.style.set(bg="", ol="")
maliang.Text(canvas, (4 + 59 + 5, 13 + 53//2), text="科学", fontsize=28, anchor="w")
maliang.Tooltip(menu, text="打开导航", align="right")

root.mainloop()
