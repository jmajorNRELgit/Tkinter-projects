##imports
import os
import tkinter as tk
from tkinter import ttk
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style
import time
import pandas as pd
from PIL import ImageTk, Image


LARGE_FONT = ('Verdanna', 12)

f = Figure(figsize=(10,7), dpi = 100) #creates the matplotlib figure
ax1 = f.add_subplot(211) #adds the top plot (full time and partial time plots)

class SeaofBTCapp(tk.Tk): #inhearits tk.TK class attributes


    length = 0 #class variable to control the zoom in funtionality of plot ax1

    def __init__(self, *args, **kwargs):



        tk.Tk.__init__(self, *args, **kwargs) #initializes tk.TK class
        container = tk.Frame(self, width=500, height=500) #the window frame

        container.grid()





        self.frames = {} #dictionary to hold the different frames when multiple windows are used

        frame = StartPage(container, self)

        self.frames[StartPage] = frame

        frame.grid(sticky = "nsew")

###use this if you want multiple windows
#        for F in (StartPage, None): #add new page classes here!!!!!!!!!!!!!!!
#
#            frame = F(container, self)
#
#            self.frames[F] = frame
#
#            frame.grid(row=0, column=0, sticky = "nsew")

        self.show_frame(StartPage) #calls the function to show the frame initially


    def show_frame(self, cont):
        frame = self.frames[cont] #cont = control, is the key for a frame in the self.frames dictionary
        frame.tkraise() #raise it to the front...inhairited from tk.TK

    #changes the length variable that controls the zoom function on graph ax1
    def click(self):
        if self.length == 0:
            self.length = 1
            print(self.length)
        else:
            self.length = 0
            print(self.length)


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent) #parent is going to be the main class SeaofBTCapp
        label = ttk.Label(self, text = 'Graph Page', font = LARGE_FONT)
        label.grid(row = 0, column = 0)

        canvas = FigureCanvasTkAgg(f, self)
        #canvas.show()
        canvas.get_tk_widget().grid(row = 2, column = 0)


        v = tk.StringVar(self, value='default text')

        e = tk.Entry(self,textvariable=v)
        e.grid(row = 1, column = 1)
        e.focus_set()

        def callback():
            print(e.get())

        b = ttk.Button(self, text="get", width=10, command=callback)
        b.grid(row = 2, column = 1, sticky = 'N')




        v2 = tk.StringVar(self, value='default text')

        e2 = tk.Entry(self,textvariable=v2)
        e2.grid(row = 1, column = 2)
        e2.focus_set()

        def callback():
            print(e2.get())

        b2 = ttk.Button(self, text="get", width=10, command=callback)
        b2.grid(row = 2, column = 2, sticky = 'N')




app = SeaofBTCapp()
#ani = animation.FuncAnimation(f,animate, interval = 1000)
app.mainloop()