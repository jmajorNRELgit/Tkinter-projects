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
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style
import matplotlib.pyplot as plt
import time
import pandas as pd
import numpy as np

#import and set daq channels
import NI_RTD_DAQ_CLASS as DAQ
daq = DAQ.DAQ()
daq.set_specific_channels([1,2,3,4])

#styling for the gui font and matplotlib background
LARGE_FONT = ('Verdanna', 12)
style.use("ggplot")



x_start = time.time() #used to create the x-axis values


f = Figure(figsize=(15,7), dpi = 100) #creates the matplotlib figure
ax1 = f.add_subplot(211) #adds the top plot (full time and partial time plots)
ax2 = f.add_subplot(212) #creates the zoomed in plot

try:
    os.remove('daqdata_2.txt')
except:
    pass

standard_deviation = []

coefficients = pd.read_csv('C:/Users/jmajor/Desktop/github/Tkinter-projects/sentdex_program/coefficient_list.csv', index_col = 0)

chan1_fit = np.poly1d(list(coefficients.iloc[:,0]))
chan2_fit = np.poly1d(list(coefficients.iloc[:,1]))
chan3_fit = np.poly1d(list(coefficients.iloc[:,2]))
chan4_fit = np.poly1d(list(coefficients.iloc[:,3]))


#counter = 0


#funtion to create the animated plots. gets called in a loop
def animate(i):

    temp = str(daq.read_specific_channels()) #acquire temp from daq
    temp = temp.lstrip('[').rstrip(']').split(',')
    s = str(round(time.time() - x_start,3))+','+str(chan1_fit(float(temp[0])))+',' + str(chan2_fit(float(temp[1])))+','+str(chan3_fit(float(temp[2])))+','+str(chan4_fit(float(temp[3]))) +'\n' #formats the x/y date to save into text file

    #saves the data to a txt file
    with open('daqdata_2.txt', 'a') as f:
        if os.stat('daqdata_2.txt').st_size == 0:
            f.write('Time(s),One,Two,Three,Four\n')
            f.write(s)
        else:
            f.write(s)

    #reads the data from the text file
    df = pd.read_table("daqdata_2.txt", delimiter=',')
    xList = list(df['Time(s)'])
    y1List = list(df['One'])
    y2List = list(df['Two'])
    y3List = list(df['Three'])
    y4List = list(df['Four'])

    standard_deviation.append(np.mean([np.std(y1List[-20:]),np.std(y2List[-20:]),np.std(y3List[-20:]),np.std(y4List[-20:])]))

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



    if app.length2 == 0:
        ax2.plot(xList,standard_deviation, label= 'Standard deviation average')
        ax2.set_title("STD plot")

    else:
       ax2.plot(xList[-50:],standard_deviation[-50:], label= 'Standard deviation average')
       ax2.set_title("STD plot zoomed")

    ax1.set_ylabel('Temperature')
    ax2.set_ylabel('STD')
    ax2.set_xlabel('Time')
    ax1.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    ax2.legend(loc='center left', bbox_to_anchor=(1, 0.5))


class TIM_stand(tk.Tk): #inhearits tk.TK class attributes


    length = 0 #class variable to control the zoom in funtionality of plot ax1
    length2 = 0 #class variable to control the zoom in funtionality of plot ax1

    def __init__(self, *args, **kwargs):



        tk.Tk.__init__(self, *args, **kwargs) #initializes tk.TK class
        container = tk.Frame(self,width=500, height=500) #the window frame

        container.pack(side = "top", fill = "both", expand = True)

        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)

        self.frames = {} #dictionary to hold the different frames when multiple windows are used

        frame = StartPage(container, self)

        self.frames[StartPage] = frame

        frame.grid(row=5, column=2, sticky = "nsew")

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
            print('Graph 1 ' + str(self.length))
        else:
            self.length = 0
            print('Graph 1 ' + str(self.length))

    #changes the length variable that controls the zoom function on graph ax2
    def click2(self):
        if self.length2 == 0:
            self.length2 = 1
            print('Graph 2 ' +str(self.length2))
        else:
            self.length2 = 0
            print('Graph 2 ' +str(self.length2))

#this is the main page that is called initially
class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent) #parent is going to be the main class SeaofBTCapp
        label = ttk.Label(self, text = 'Graph Page', font = LARGE_FONT)
        label.pack(pady=10,padx=10)

        button = ttk.Button(self, text = "Zoom graph 1", command = controller.click)
        button.pack(side = tk.TOP)

        button2 = ttk.Button(self, text = "Zoom graph 2", command = controller.click2)
        button2.pack(side = tk.TOP)

        canvas = FigureCanvasTkAgg(f, self)
        #canvas.show()
        canvas.get_tk_widget().pack(side = tk.TOP, fill = tk.BOTH, expand = True)


        v2 = tk.StringVar(self, value='Set filename')

        e2 = tk.Entry(self,textvariable=v2)
        e2.pack(side = tk.TOP)
        e2.focus_set()

        def save_file():
            file_time = time.strftime("%b %d %Y, time_%H_%M_%S")
            file = e2.get()
            print('{0} {1}.csv'.format(file, file_time))

            df = pd.read_table("daqdata_2.txt", delimiter=',')

            data = df.iloc[-30:, :]

            data.to_csv('{0} {1}.csv'.format(file, file_time))


        b2 = ttk.Button(self, text="Save file", width=10, command=save_file)
        b2.pack(side = tk.TOP)



        def counter_label(label):


            def count():
                global counter
                if len(standard_deviation) == 0:
                    counter = [0.00]

                else:
                    counter = standard_deviation[-1:]
                label.config(text= 'STD: ' + str(round(counter[0],4)))
                label.after(1000, count)

            count()

        std_label = tk.Label(self, fg="dark green")
        std_label.pack()
        counter_label(std_label)




app = TIM_stand()
ani = animation.FuncAnimation(f,animate, interval = 1000)
app.mainloop()