import os
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.animation as animation
import time
import pandas as pd
import numpy as np
import threading
import matplotlib.pyplot as plt
import copy

f = Figure(figsize=(10,5), dpi = 100) #creates the matplotlib figure
ax1 = f.add_subplot(111) #adds the top plot (full time and partial time plots)
y1 = []

def animate(i):
    global x1
    ax1.clear()
    x = list(np.arange(0, x1))
    y = copy.deepcopy(y1)
    if len(x) == len(y):
        z = np.polyfit(x,y,1)
        y2 = np.polyval(z, x)


        ax1.plot(y, 'bo')
        ax1.plot(y2, 'r-')


x1 = 0
stop = 0
add1 = 0
def workerThread1():
    global add1
    global x1
    while stop == 0:
        time.sleep(.02)
        y1.append((np.random.rand()*add1*np.sin(add1)+add1)*np.sin(add1))
        add1 += .05
        x1 +=1

thread1 = threading.Thread(target=workerThread1)
thread1.start(  )


root = tk.Tk()



canvas = FigureCanvasTkAgg(f, root)
canvas.get_tk_widget().grid(row = 2, column = 0)



ani = animation.FuncAnimation(f,animate, interval = 200)


root.mainloop()



stop = 1

#time.sleep(.5)
#x = list(np.arange(0, x))
#z = np.polyfit(x,y,4)
#y2 = np.polyval(z, x)
#
#plt.plot(y, 'bo')
#plt.plot(y2, 'r-')
#plt.show()