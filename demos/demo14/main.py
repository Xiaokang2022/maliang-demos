import maliang
from maliang import table

root = maliang.Tk()

tk_table = table.TkTable(root, data=[[f"Row {r}, Col {c}" for c in range(100)] for r in range(100)])
tk_table.enable_bindings()
tk_table.pack(expand=True, fill="both")

root.mainloop()
