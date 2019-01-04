
##imports
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

#used to stop the worker thread
stop = 0

#Class to hold miscellaneous data
class misc:
    def __init__(self):

        #removes the old data log
        try:
            os.remove('daqdata_2.txt')
        except:
            pass


        with open('daqdata_2.txt', 'a') as f:
            if os.stat('daqdata_2.txt').st_size == 0: #if the data file is empty this adds the headers
                f.write('Time(s),One,Two,Three,Four\n')

#funtion to create the animated plots. gets called in a loop
def animate(i):

    #reads the data from the text file
    df = pd.read_table("daqdata_2.txt", delimiter=',')
    xList = list(df['Time(s)'])
    y1List = list(df['One'])
    y2List = list(df['Two'])
    y3List = list(df['Three'])
    y4List = list(df['Four'])

    #clears the plots so we don't get multiple layers of plots
    app.ax1.clear()

    #gives the ability to zoom in on the first graph
    if app.zoom1 == 0:
        app.ax1.plot(xList,y1List, label='Chan 1')
        app.ax1.plot(xList,y2List, label='Chan 2')
        app.ax1.plot(xList,y3List, label='Chan 3')
        app.ax1.plot(xList,y4List, label='Chan 4')
        app.ax1.set_title("Temp plot")

    else:
        app.ax1.plot(xList[app.minimum:len(xList)],y1List[app.minimum:len(xList)], label='Chan 1')
        app.ax1.plot(xList[app.minimum:len(xList)],y2List[app.minimum:len(xList)], label='Chan 2')
        app.ax1.plot(xList[app.minimum:len(xList)],y3List[app.minimum:len(xList)], label='Chan 3')
        app.ax1.plot(xList[app.minimum:len(xList)],y4List[app.minimum:len(xList)], label='Chan 4')
        app.ax1.set_title("Temp plot zoomed")

    app.f.tight_layout()

class TIM(tk.Tk):




    f = Figure(figsize=(10,5), dpi = 100) #creates the matplotlib figure
    ax1 = f.add_subplot(111) #adds the top plot (full time and partial time plots)


    zoom1 = 0 #class variable to control the zoom in funtionality of plot app.ax1


    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.x_start = time.time() #used to create the x-axis values

        self.graph_frame()
        self.button_frame()


        self.thread1 = threading.Thread(target=self.workerThread1)
        self.thread1.start(  )

        self.minimum = 0


    def workerThread1(self):
        """
        This is where we handle the asynchronous I/O.
        """
        global stop
        while stop == 0:

            time.sleep(1)
            s = [round(time.time() - self.x_start,3), np.random.rand()+1, np.random.rand()+2, np.random.rand()+3, np.random.rand()+4 ]

            s = str(s).lstrip('[').rstrip(']') +'\n'

            #saves the data to a txt file
            with open('daqdata_2.txt', 'a') as f:
                if os.stat('daqdata_2.txt').st_size == 0: #if the data file is empty this adds the headers
                    f.write('Time(s),One,Two,Three,Four\n')
                    f.write(s)
                else:
                    f.write(s)



    def graph_frame(self):
        frame1 = tk.Frame(self,width=100, height=200)
        frame1.grid(row=0,column=0)

        canvas = FigureCanvasTkAgg(self.f, frame1)
        canvas.get_tk_widget().grid(row = 0, column = 0)

        self.text1 = ttk.Entry(frame1, width=5)
        self.text1.insert(0,'0')
        self.text1.grid(row = 1, column = 0, sticky = 'w')

        self.text2 = ttk.Entry(frame1, width=5)
        self.text2.insert(0,'0')
        self.text2.grid(row = 1, column = 0, sticky = 'e')

        self.zoom(self.text1, self.text2)

    def zoom(self, text1, text2):


        def pri():
            self.minimum = int(float(text1.get()))
            print(self.minimum)

            self.maximum = int(text2.get())
            print(self.maximum)

            self.after(1000,pri)

        pri()





    def button_frame(self):

        frame2 = tk.Frame(self,width=100, height=200, borderwidth=10)
        frame2.grid(row=0, column = 1)

        graph_one_zoom_button = ttk.Button(frame2, text = 'Zoom graph one', command = self.zoom_graph1)
        graph_one_zoom_button.grid(row = 0, column = 0)

        spacer = ttk.Label(frame2, text = '' )
        spacer.grid(row = 1, column = 0)

        #button to save the rtd data
        save_data_button = ttk.Button(frame2, text = 'Save data', command = self.save_file)
        save_data_button.grid(row=2, column = 0)

        #filename input field
        text_field = tk.StringVar(frame2, value='Set filename')
        self.text_box = tk.Entry(frame2,textvariable=text_field)
        self.text_box.grid(row=2, column = 1)
        self.text_box.focus_set()

    #function to save the RTD data for the past 10 minutes. saves the date and time in the filename
    def save_file(self):
            file_time = time.strftime("%b %d %Y, time_%H_%M_%S")
            file = self.text_box.get()
            print('{0} {1}.csv'.format(file, file_time))

            df = pd.read_table("daqdata_2.txt", delimiter=',')

            #This loop looks at the Time column to determine where 10 minutes back starts with the data
            c = 1
            for i in df.iloc[::-1, 0]:
                if df.iloc[-1, 0] - i > 600:
                    break
                c +=1

            data = df.iloc[-c:, :]
            data.to_csv('{0} {1}.csv'.format(file, file_time))

    def zoom_graph1(self):
        if self.zoom1 == 0:
            self.zoom1 = 1
        else:
            self.zoom1 = 0

misc = misc()
app = TIM()

ani = animation.FuncAnimation(app.f,animate, interval = 1000)


app.mainloop()

stop = 1


