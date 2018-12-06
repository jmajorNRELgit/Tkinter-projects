##imports
import os
import tkinter as tk
from tkinter import ttk
import tk_tools
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style
import time
import pandas as pd
import numpy as np
import random
import tkinter
import threading


#import and set daq channels
import NI_RTD_DAQ_CLASS as DAQ
daq = DAQ.DAQ()
daq.set_specific_channels([1,2,3,4])


data = []

x_start = time.time() #used to create the x-axis values
def animate(i):

    #clears the plots so we don't get multiple layers of plots
    client.gui.ax1.clear()

    client.gui.ax1.plot([item[0] for item in data],[item[1] for item in data], label='Chan 1')
    client.gui.ax1.set_title("Temp plot")





class GuiPart:

    f = Figure(figsize=(10,5), dpi = 100) #creates the matplotlib figure
    ax1 = f.add_subplot(111) #adds the top plot (full time and partial time plots

    def __init__(self, master):


        self.graph_frame(master)



    def graph_frame(self,master):
        frame1 = tk.Frame(master)
        frame1.pack()

        canvas = FigureCanvasTkAgg(self.f, frame1)
        canvas.get_tk_widget().pack()

        button = tk.Button(master,text = 'Print "foo"', command = self.com)
        button.pack()

    def com(self):
        print('foo')



class ThreadedClient:
    """
    Launch the main part of the GUI and the worker thread. periodicCall and
    endApplication could reside in the GUI part, but putting them here
    means that you have all the thread controls in a single place.
    """
    def __init__(self, master):
        """
        Start the GUI and the asynchronous threads. We are in the main
        (original) thread of the application, which will later be used by
        the GUI as well. We spawn a new thread for the worker (I/O).
        """
        self.master = master

        # Set up the GUI part
        self.gui = GuiPart(master)

        # Set up the thread to do asynchronous I/O
        # More threads can also be created and used, if necessary

        self.thread1 = threading.Thread(target=self.workerThread1)
        self.thread1.start(  )


    def workerThread1(self):
        """
        This is where we handle the asynchronous I/O. For example, it may be
        a 'select(  )'. One important thing to remember is that the thread has
        to yield control pretty regularly, by select or otherwise.
        """
        while True:
            # To simulate asynchronous I/O, we create a random number at
            # random intervals. Replace the following two lines with the real
            # thing.

           temp = str(daq.read_specific_channels()) #acquire temp from daq
           dat = [time.time() - x_start, float(temp.split()[0].lstrip('[').rstrip(',')) ]
           data.append(dat)

rand = random.Random(  )
root = tkinter.Tk(  )
#root.geometry('200x50')


client = ThreadedClient(root)
ani = animation.FuncAnimation(client.gui.f,animate, interval = 1000)
root.mainloop(  )


print('DAQ closed')