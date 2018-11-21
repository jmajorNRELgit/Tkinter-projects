
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




class misc:
    def __init__(self):
        try:
            os.remove('daqdata_2.txt')
        except:
            pass

        self.standard_deviation = []

        coefficients = pd.read_csv('C:/Users/jmajor/Desktop/github/Tkinter-projects/sentdex_program/coefficient_list.csv', index_col = 0)

        self.chan1_fit = np.poly1d(list(coefficients.iloc[:,0]))
        self.chan2_fit = np.poly1d(list(coefficients.iloc[:,1]))
        self.chan3_fit = np.poly1d(list(coefficients.iloc[:,2]))
        self.chan4_fit = np.poly1d(list(coefficients.iloc[:,3]))


#counter = 0


#funtion to create the animated plots. gets called in a loop
def animate(i):

    temp = str(daq.read_specific_channels()) #acquire temp from daq
    temp = temp.lstrip('[').rstrip(']').split(',')
    s = str(round(time.time() - app.x_start,3))+','+str(misc.chan1_fit(float(temp[0])))+',' + str(misc.chan2_fit(float(temp[1])))+','+str(misc.chan3_fit(float(temp[2])))+','+str(misc.chan4_fit(float(temp[3]))) +'\n' #formats the x/y date to save into text file

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

    misc.standard_deviation.append(np.mean([np.std(y1List[-20:]),np.std(y2List[-20:]),np.std(y3List[-20:]),np.std(y4List[-20:])]))

    #clears the plots so we don't get multiple layers of plots
    app.ax1.clear()
    app.ax2.clear()

    #gives the ability to zoom in on the first graph
    if app.length == 0:
        app.ax1.plot(xList,y1List, label='Chan 1')
        app.ax1.plot(xList,y2List, label='Chan 2')
        app.ax1.plot(xList,y3List, label='Chan 3')
        app.ax1.plot(xList,y4List, label='Chan 4')
        app.ax1.set_title("Temp plot")

    else:
        app.ax1.plot(xList[-100:],y1List[-100:], label='Chan 1')
        app.ax1.plot(xList[-100:],y2List[-100:], label='Chan 2')
        app.ax1.plot(xList[-100:],y3List[-100:], label='Chan 3')
        app.ax1.plot(xList[-100:],y4List[-100:], label='Chan 4')
        app.ax1.set_title("Temp plot zoomed")
    app.ax1.plot(xList[-30:], [i +3 for i in y1List[-30:]],label='STD data') #shows the length of the data being analized for standard deviation



    if app.length2 == 0:
        app.ax2.plot(xList,misc.standard_deviation, label= 'Standard deviation average')
        app.ax2.set_title("STD plot")

    else:
       app.ax2.plot(xList[-50:],misc.standard_deviation[-50:], label= 'Standard deviation \n average')
       app.ax2.set_title("STD plot zoomed")

    app.ax1.set_ylabel('Temperature')
    app.ax2.set_ylabel('STD')
    app.ax2.set_xlabel('Time')
    app.ax1.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    app.ax2.legend(loc='center left', bbox_to_anchor=(1, 0.5))

    app.f.tight_layout()





class TIM(tk.Tk):

    x_start = time.time() #used to create the x-axis values


    f = Figure(figsize=(10,5), dpi = 100) #creates the matplotlib figure
    ax1 = f.add_subplot(211) #adds the top plot (full time and partial time plots)
    ax2 = f.add_subplot(212) #creates the zoomed in plot

    length = 0 #class variable to control the zoom in funtionality of plot app.ax1
    length2 = 0 #class variable to control the zoom in funtionality of plot app.ax1

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        container = tk.Frame(self,width=500, height=400)

        container.grid()

        self.graph_frame()
        self.button_frame()


    def graph_frame(self):
        frame1 = tk.Frame(self,width=100, height=200)
        frame1.grid(row=0,column=0)

        label2 = tk.Label(frame1, text = 'Graph',font=("Helvetica", 20))
        label2.grid(row = 0, column = 0)

        canvas = FigureCanvasTkAgg(self.f, frame1)
        canvas.get_tk_widget().grid(row = 1, column = 0)

    def button_frame(self):

        frame2 = tk.Frame(self,width=100, height=200,bg = "BLACK", borderwidth=10)
        frame2.grid(row=0, column = 1)

        button = tk.Button(frame2, text = 'foo', command = self.click2)
        button.grid(row=1, column = 0)

        label = tk.Label(frame2, text = 'bar',bg = "RED")
        label.grid(row = 0, column = 0)




    def click2(self):
        print('foo')

misc = misc()
app = TIM()
ani = animation.FuncAnimation(app.f,animate, interval = 1000)
app.mainloop()

