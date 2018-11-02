# -*- coding: utf-8 -*-
"""
Created on Thu Nov  1 07:55:49 2018

@author: jmajor
"""
import os
import numpy as np

import tkinter as tk
from tkinter import ttk

import matplotlib
matplotlib.use("TkAgg")

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure

import matplotlib.animation as animation
from matplotlib import style

import NI_RTD_DAQ_CLASS as DAQ
daq = DAQ.DAQ()
daq.set_specific_channels([2])

LARGE_FONT = ('Verdanna', 12)
style.use("ggplot")

import time

start = time.time()

def animate(i):

    temp = str(round(daq.read_specific_channels()[0],3))

    s = temp +','+str(round(time.time() - start,3))+'\n'

    with open('daqdata_2.txt', 'a') as f:
        if os.stat('daqdata_2.txt').st_size == 0:
            f.write(s)
        else:
            f.write(s)

    with open("daqdata_2.txt","r") as f:
        pullData = f.read()
    dataList = pullData.split('\n')
    xList = []
    yList = []
    for eachLine in dataList:
        if len(eachLine)  > 1:

            y,x = eachLine.split(',')

            xList.append(float(x))
            yList.append(float(y))

    a.clear()
    a.plot(yList)

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

        frame = StartPage(container, self)

        self.frames[StartPage] = frame

        frame.grid(row=0, column=0, sticky = "nsew")

#        for F in (StartPage, None): #add new page classes here!!!!!!!!!!!!!!!
#
#            frame = F(container, self)
#
#            self.frames[F] = frame
#
#            frame.grid(row=0, column=0, sticky = "nsew")

        self.show_frame(StartPage)


    def show_frame(self, cont):
        frame = self.frames[cont] #cont = control, is the key for a frame in the self.frames dictionary
        frame.tkraise() #raise it to the front...inhairited from tk.TK




class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent) #parent is going to be the main class SeaofBTCapp
        label = ttk.Label(self, text = 'Graph Page', font = LARGE_FONT)
        label.pack(pady=10,padx=10)

        canvas = FigureCanvasTkAgg(f, self)
        #canvas.show()
        canvas.get_tk_widget().pack(side = tk.TOP, fill = tk.BOTH, expand = True)

        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side = tk.TOP, fill = tk.BOTH, expand = True)




app = SeaofBTCapp()
ani = animation.FuncAnimation(f,animate, interval = 1000)
app.mainloop()