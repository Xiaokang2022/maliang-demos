import math

import maliang
import maliang.animation as animation


class LoginToplevel(maliang.Toplevel):
    """登录窗口"""

    def load_ui(self) -> None:
        """加载 UI"""
        canvas = maliang.Canvas(self)
        canvas.place(width=480, height=720)

        self.sub_title = maliang.Text(
            canvas, (240, 45), text="登录到你的账号", fontsize=36, anchor="center")

        canvas.create_oval(120, 90, 360, 330, outline="grey")
        canvas.create_text(240, 210, text="用户\n头像", fill="grey", font=30)

        self.account = maliang.InputBox(
            canvas, (40, 360), (400, 50), placeholder="请输入您的账号")
        self.password = maliang.InputBox(
            canvas, (40, 430), (400, 50), placeholder="请输入您的密码", show="●")
        self.an = maliang.Button(canvas, (40, 500), (190, 50),
                                 text="注 册", command=self.animate)
        self.login = maliang.Button(canvas, (250, 500), (190, 50), text="登 录")
        self.password_verify = maliang.InputBox(
            canvas, (40, 500+300), (400, 50), placeholder="请再次输入您的密码", show="●")
        self.registry = maliang.Button(
            canvas, (40-300, 570), (190, 50), text="注 册")
        self.back = maliang.Button(canvas, (250+300, 570),
                                   (190, 50), text="返 回", command=lambda: self.animate(True))

        self.forget = maliang.UnderlineButton(
            canvas, (140, 600), text="忘记密码", fontsize=20, anchor="center")
        self.sep = maliang.Text(canvas, (190, 600), text="|", anchor="center")
        self.find = maliang.UnderlineButton(
            canvas, (240, 600), text="找回账号", fontsize=20, anchor="center")
        self.sep_2 = maliang.Text(canvas, (290, 600), text="|", anchor="center")
        self.net = maliang.UnderlineButton(
            canvas, (340, 600), text="网络设置", fontsize=20, anchor="center")
        self.animation_lock = False  # 防熊

    def animate(self, back: bool = False) -> None:
        """执行相关动画"""
        if self.animation_lock:
            return
        self.animation_lock = True
        k = -1 if back else 1
        self.after(
            250, self.sub_title.texts[0].set, "登录到你的账号" if back else "注册新的账号")
        self.after(
            250, self.title, "登录" if back else "注册")
        animation.MoveWidget(self.sub_title, (0, -80), 500,
                             controller=animation.generate(math.sin, 0, math.pi, map_y=False), fps=60,
                             end=lambda: self.__setattr__("animation_lock", False)).start()
        animation.MoveWidget(self.an, (-300*k, 0), 500,
                             controller=animation.smooth, fps=60).start()
        animation.MoveWidget(self.login, (300*k, 0), 500,
                             controller=animation.smooth, fps=60).start()
        animation.MoveWidget(self.registry, (300*k, 0), 500,
                             controller=animation.smooth, fps=60).start()
        animation.MoveWidget(self.back, (-300*k, 0), 500,
                             controller=animation.smooth, fps=60).start()
        animation.MoveWidget(self.forget, (0, 100*k), 500,
                             controller=animation.smooth, fps=60).start()
        animation.MoveWidget(self.sep, (0, 100*k), 500,
                             controller=animation.smooth, fps=60).start()
        animation.MoveWidget(self.find, (0, 100*k), 500,
                             controller=animation.smooth, fps=60).start()
        animation.MoveWidget(self.sep_2, (0, 100*k), 500,
                             controller=animation.smooth, fps=60).start()
        animation.MoveWidget(self.net, (0, 100*k), 500,
                             controller=animation.smooth, fps=60).start()
        animation.MoveWidget(self.password_verify, (0, -300*k), 500,
                             controller=animation.smooth, fps=60).start()


root = maliang.Tk(title="Main Window")
root.center()

login = LoginToplevel(root, (480, 640), title="登录", grab=True)
login.resizable(False, False)
login.transient(root)
login.center()
login.load_ui()

root.mainloop()
