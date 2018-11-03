# -*- coding: utf-8 -*-
"""
Created on Thu Nov  1 07:55:49 2018

@author: jmajor
"""

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

#import and set daq channels
import NI_RTD_DAQ_CLASS as DAQ
daq = DAQ.DAQ()
daq.set_specific_channels([1,2,3,4])

#styling for the gui font and matplotlib background
LARGE_FONT = ('Verdanna', 12)
style.use("ggplot")



x_start = time.time() #used to create the x-axis values


f = Figure(figsize=(5,5), dpi = 100) #creates the matplotlib figure
ax1 = f.add_subplot(211) #adds the top plot (full time and partial time plots)
ax2 = f.add_subplot(212) #creates the zoomed in plot

os.remove('daqdata_2.txt')



#funtion to create the animated plots. gets called in a loop
def animate(i):

    temp = str(daq.read_specific_channels()) #acquire temp from daq
    temp = temp.lstrip('[').rstrip(']').split(',')
    s = str(round(time.time() - x_start,3))+','+temp[0]+',' + temp[1]+','+temp[2]+','+temp[3] +'\n' #formats the x/y date to save into text file

    #saves the data to a txt file
    with open('daqdata_2.txt', 'a') as f:
        if os.stat('daqdata_2.txt').st_size == 0:
            f.write('Time,One,Two,Three,Four\n')
            f.write(s)
        else:
            f.write(s)

    #reads the data from the text file
    df = pd.read_table("daqdata_2.txt", delimiter=',')
    xList = list(df['Time'])
    y1List = list(df['One'])
    y2List = list(df['Two'])
    y3List = list(df['Three'])
    y4List = list(df['Four'])



    #clears the plots so we don't get multiple layers of plots
    ax1.clear()
    ax2.clear()

    #gives the ability to zoom in on the first graph
    if app.length == 0:
        ax1.plot(xList,y1List, label='Chan 1')
        ax1.plot(xList,y2List, label='Chan 2')
        ax1.plot(xList,y3List, label='Chan 3')
        ax1.plot(xList,y4List, label='Chan 4')
        ax1.set_title("Temp plot")

    else:
        ax1.plot(xList[-100:],y1List[-100:], label='Chan 1')
        ax1.plot(xList[-100:],y2List[-100:], label='Chan 2')
        ax1.plot(xList[-100:],y3List[-100:], label='Chan 3')
        ax1.plot(xList[-100:],y4List[-100:], label='Chan 4')
        ax1.set_title("Temp plot zoomed")

    ax1.plot(xList[-30:], [i +3 for i in y1List[-30:]],label='STD data') #shows the length of the data being analized for standard deviation
    ax2.plot(xList[-30:],y1List[-30:], label= 'Last 20 seconds') #plots a close up of the temperature data
    ax2.set_title("Temp plot zoomed")
    ax1.legend()
    ax2.legend()



class SeaofBTCapp(tk.Tk): #inhearits tk.TK class attributes


    length = 0 #class variable to control the zoom in funtionality of plot ax1

    def __init__(self, *args, **kwargs):



        tk.Tk.__init__(self, *args, **kwargs) #initializes tk.TK class
        container = tk.Frame(self) #the window frame

        container.pack(side = "top", fill = "both", expand = True)

        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)

        self.frames = {} #dictionary to hold the different frames when multiple windows are used

        frame = StartPage(container, self)

        self.frames[StartPage] = frame

        frame.grid(row=0, column=0, sticky = "nsew")

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

#this is the main page that is called initially
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

        button = ttk.Button(self, text = "Zoom graph 1", command = controller.click)

        button.pack()


app = SeaofBTCapp()
ani = animation.FuncAnimation(f,animate, interval = 1000)
app.mainloop()