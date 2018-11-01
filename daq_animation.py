#---------Imports
from numpy import arange, sin, pi
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import tkinter as Tk
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import NI_RTD_DAQ_CLASS
#---------End of imports

daq = NI_RTD_DAQ_CLASS.DAQ()

daq.set_specific_channels([2])


fig = plt.Figure()

l = [-.5,1,0,.5,-.5,1,0,0,1,.5]
x = np.arange(len(l)-10, len(l))        # x-array

def animate(i):
    l.append(daq.read_specific_channels()[0])
    line.set_ydata(l[-10:])  # update the data
    ax.relim()
    ax.autoscale_view(True,True,True)
    return line,

root = Tk.Tk()

label = Tk.Label(root,text="DAQ Graph").grid(column=0, row=0)

canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().grid(column=0,row=1)

ax = fig.add_subplot(111)
ax.autoscale()

line, = ax.plot(x, np.sin(x))
ani = animation.FuncAnimation(fig, animate, np.arange(1, 300), interval=100, blit=False)

def _quit():
    root.quit()     # stops mainloop
    root.destroy()  # this is necessary on Windows to prevent
                    # Fatal Python Error: PyEval_RestoreThread: NULL tstate

def _save():
    print('save data')


button = Tk.Button(master=root, text="Quit", command=_quit).grid(column = 0, row = 2)
button2 = Tk.Button(master = root, text = 'Save').grid(column = 3, row = 2)


Tk.mainloop()