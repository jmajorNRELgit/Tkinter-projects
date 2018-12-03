import tkinter as tk
import tk_tools
import time

start = time.time()

class TIM(tk.Tk):


    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        container = tk.Frame(self)

        container.pack()


        self.led = tk_tools.Led(self, size=50)
        self.led.to_green()
        self.led.pack()

        button = tk.Button(self, command = self.change)
        button.pack()

        self.change()

    def change(self):
        if time.time() - start > 5:
            self.led.to_red()
        print(time.time() - start)
        self.after(1000, self.change)



app = TIM()

app.mainloop()
