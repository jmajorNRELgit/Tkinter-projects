import tkinter as tk
from tkinter import ttk
import time

start = time.time()

class TIM(tk.Tk):


    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        container = tk.Frame(self)

        container.pack()

        text = ttk.Entry(self)
        text.insert(0, 'Default')
        text.pack()

        self.change_led(text)

    def change_led(self,text):
        def change():
            i = text.get()
            print(i)
            self.after(1000, change)
        change()
app = TIM()

app.mainloop()
