# -*- coding: utf-8 -*-
"""
Created on Thu Nov  1 07:55:49 2018

@author: jmajor
"""

import tkinter as tk
from tkinter import ttk

import matplotlib
matplotlib.use("TkAgg")

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure

import matplotlib.animation as animation
from matplotlib import style


LARGE_FONT = ('Verdanna', 12)
style.use("ggplot")


def animate(i):
    pullData = open("data.txt","r").read()
    dataList = pullData.split('\n')
    xList = []
    yList = []
    for eachLine in dataList:
        if len(eachLine)  > 1:
            x,y = eachLine.split(',')
            xList.append(int(x))
            yList.append(int(y))

    a.clear()
    a.plot(xList,yList)

f = Figure(figsize=(5,5), dpi = 100)

a = f.add_subplot(111)


class SeaofBTCapp(tk.Tk): #inhearits tk.TK class attributes

    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs) #initializes tk.TK class
        container = tk.Frame(self) #the window frame

        container.pack(side = "top", fill = "both", expand = True)

        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)

        self.frames = {} #dictionary to hold the different frames

        for F in (StartPage, PageOne, PageTwo, PageThree): #add new page classes here!!!!!!!!!!!!!!!

            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky = "nsew")

        self.show_frame(StartPage)


    def show_frame(self, cont):
        frame = self.frames[cont] #cont = control, is the key for a frame in the self.frames dictionary
        frame.tkraise() #raise it to the front...inhairited from tk.TK




class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent) #parent is going to be the main class SeaofBTCapp
        label = ttk.Label(self, text = 'Start Page', font = LARGE_FONT)
        label.pack(pady=10,padx=10)

        button = ttk.Button(self, text = "Visit page 1",
                            command =lambda: controller.show_frame(PageOne))
        button.pack()

        button2 = ttk.Button(self, text = "To Page 2",
                            command =lambda: controller.show_frame(PageTwo))
        button2.pack()

        button3 = ttk.Button(self, text = "To Graph Page",
                            command =lambda: controller.show_frame(PageThree))
        button3.pack()


class PageOne(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)

        label = ttk.Label(self, text = 'Page 1', font = LARGE_FONT)
        label.pack(pady=10,padx=10)

        button1 = ttk.Button(self, text = "Back to home",
                            command =lambda: controller.show_frame(StartPage))
        button1.pack()

        button2 = ttk.Button(self, text = "To Page 2",
                            command =lambda: controller.show_frame(PageTwo))
        button2.pack()

class PageTwo(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)

        label = ttk.Label(self, text = 'Page 2', font = LARGE_FONT)
        label.pack(pady=10,padx=10)

        button1 = ttk.Button(self, text = "Back to home",
                            command =lambda: controller.show_frame(StartPage))
        button1.pack()

        button2 = ttk.Button(self, text = "To Page 1",
                            command =lambda: controller.show_frame(PageOne))
        button2.pack()

class PageThree(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)

        label = ttk.Label(self, text = 'Graph Page', font = LARGE_FONT)
        label.pack(pady=10,padx=10)

        button1 = ttk.Button(self, text = "Back to home",
                            command =lambda: controller.show_frame(StartPage))
        button1.pack()



        canvas = FigureCanvasTkAgg(f, self)
        #canvas.show()
        canvas.get_tk_widget().pack(side = tk.TOP, fill = tk.BOTH, expand = True)

        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side = tk.TOP, fill = tk.BOTH, expand = True)


app = SeaofBTCapp()
ani = animation.FuncAnimation(f,animate, interval = 1000)
app.mainloop()