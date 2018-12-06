
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

#import and set daq channels
import NI_RTD_DAQ_CLASS as DAQ
daq = DAQ.DAQ()
daq.set_specific_channels([1,2,3,4])

#styling for the gui font and matplotlib background
LARGE_FONT = ('Verdanna', 12)
style.use("ggplot")



#Class to hold miscellaneous data
class misc:
    def __init__(self):

        #removes the old data log
        try:
            os.remove('daqdata_2.txt')
        except:
            pass


        self.standard_deviation = []

        #reads the RTD calibration coefficients and creates the functions to fit the data
        coefficients = pd.read_csv('C:/Users/jmajor/Desktop/github/Tkinter-projects/sentdex_program/coefficient_list.csv', index_col = 0)
        self.chan1_fit = np.poly1d(list(coefficients.iloc[:,0]))
        self.chan2_fit = np.poly1d(list(coefficients.iloc[:,1]))
        self.chan3_fit = np.poly1d(list(coefficients.iloc[:,2]))
        self.chan4_fit = np.poly1d(list(coefficients.iloc[:,3]))


#funtion to create the animated plots. gets called in a loop
def animate(i):

    temp = str(daq.read_specific_channels()) #acquire temp from daq
    temp = temp.lstrip('[').rstrip(']').split(',') #clean up daq data
    s = str(round(time.time() - app.x_start,3))+','+str(misc.chan1_fit(float(temp[0])))+',' + str(misc.chan2_fit(float(temp[1])))+','+str(misc.chan3_fit(float(temp[2])))+','+str(misc.chan4_fit(float(temp[3]))) +'\n' #formats the x/y date to save into text file

    #saves the data to a txt file
    with open('daqdata_2.txt', 'a') as f:
        if os.stat('daqdata_2.txt').st_size == 0: #if the data file is empty this adds the headers
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
    if app.zoom1 == 0:
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
    app.ax1.plot(xList[-30:], [i +3 for i in y1List[-30:]],label='STD data') #shows the zoom1 of the data being analized for standard deviation



    if app.zoom2 == 0:
        app.ax2.plot(xList,misc.standard_deviation, label= 'STD')
        app.ax2.set_title("STD plot")

    else:
       app.ax2.plot(xList[-50:],misc.standard_deviation[-50:], label= 'Standard deviation \n average')
       app.ax2.set_title("STD plot zoomed")

    app.ax1.set_ylabel('Temperature')
    app.ax1.set_xlabel('Time')
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

    zoom1 = 0 #class variable to control the zoom in funtionality of plot app.ax1
    zoom2 = 0 #class variable to control the zoom in funtionality of plot app.ax1

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.graph_frame()
        self.button_frame()


    def graph_frame(self):
        frame1 = tk.Frame(self,width=100, height=200)
        frame1.grid(row=0,column=0)

#        label2 = tk.Label(frame1, text = 'Graph',font=("Helvetica", 20))
#        label2.grid(row = 0, column = 0)

        canvas = FigureCanvasTkAgg(self.f, frame1)
        canvas.get_tk_widget().grid(row = 2, column = 0)


        #a numeric display of the standard deviation
        std_display = tk.Label(self,fg="dark green")
        std_display.grid(row = 3, column = 0, sticky = 'n')
        self.counter_label(std_display)

        #an indicator that shows green when the standard deviation in low enough
        led = tk_tools.Led(frame1, size=50)
        led.grid(row = 3, column = 0, sticky = 's')
        self.change_led(led)



    def button_frame(self):

        frame2 = tk.Frame(self,width=100, height=200, borderwidth=10)
        frame2.grid(row=0, column = 1)

        graph_one_zoom_button = ttk.Button(frame2, text = 'Zoom graph one', command = self.zoom_graph1)
        graph_one_zoom_button.grid(row = 0, column = 0)

        graph_two_zoom_button = ttk.Button(frame2, text = 'Zoom graph two', command = self.zoom_graph2)
        graph_two_zoom_button.grid(row = 0, column = 1)

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


    #Displays the standard deviation
    def counter_label(self,label):


            def count():
                if len(misc.standard_deviation) == 0:
                    counter = [0.00]

                else:
                    counter = misc.standard_deviation[-1:]
                label.config(text= 'STD: ' + str(round(counter[0],4)))
                label.after(1000, count)

            count()

    #changes the color of the standard deviation indicator
    def change_led(self, led):
        def change():
            if len(misc.standard_deviation) != 0 and misc.standard_deviation[-1] > .008:
                led.to_red()
            else:
                led.to_green()
            self.after(1000, change)

        change()

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

    def zoom_graph2(self):
        if self.zoom2 == 0:
            self.zoom2 = 1
        else:
            self.zoom2 = 0





misc = misc()
app = TIM()
ani = animation.FuncAnimation(app.f,animate, interval = 1000)


app.mainloop()





