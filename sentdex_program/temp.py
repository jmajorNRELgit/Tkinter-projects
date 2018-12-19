import tkinter as tk

root = tk.Tk()
a = 0
def change():
    global a
    if a == 0:
        btn_text.set("b")
        a = 1
    else:
        btn_text.set("a")
        a = 0





btn_text = tk.StringVar()
btn = tk.Button(root, textvariable=btn_text, command=change)
btn_text.set("a")

btn.pack()

root.mainloop()