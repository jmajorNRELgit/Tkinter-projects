
import tkinter as tk
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


f = Figure(figsize=(10,5), dpi = 100) #creates the matplotlib figure
ax1 = f.add_subplot(211) #adds the top plot (full time and partial time plots)
ax2 = f.add_subplot(212) #creates the zoomed in plot


class TIM(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        container = tk.Frame(self,width=500, height=400)

        container.grid()

        frame1 = tk.Frame(self,width=100, height=200)
        frame1.grid(row=0,column=0)

        label2 = tk.Label(frame1, text = 'Graph',font=("Helvetica", 20))
        label2.grid(row = 0, column = 0)

        frame2 = tk.Frame(self,width=100, height=200,bg = "BLACK", borderwidth=10)
        frame2.grid(row=0, column = 1)

        button = tk.Button(frame2, text = 'foo', command = self.click2)
        button.grid(row=1, column = 0)

        label = tk.Label(frame2, text = 'bar',bg = "RED")
        label.grid(row = 0, column = 0)

        canvas = FigureCanvasTkAgg(f, frame1)

        canvas.get_tk_widget().grid(row = 1, column = 0)

    def click2(self):
        print('foo')

app = TIM()

app.mainloop()

