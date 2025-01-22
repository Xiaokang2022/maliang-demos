import maliang
import maliang.core.configs as configs
import maliang.media as media
import maliang.toolbox as toolbox

if toolbox.load_font("./assets/fonts/LXGWWenKai-Regular.ttf"):
    configs.Font.family = "LXGW WenKai"

root = maliang.Tk(title=f"maliang-media v{media.__version__}")
cv = media.VideoCanvas(root, keep_ratio="min", free_anchor=True, controls=True)
cv.place(width=1280, height=720, x=640, y=360, anchor="center")
cv.open("./assets/videos/Bad Apple.mp4")
root.mainloop()
