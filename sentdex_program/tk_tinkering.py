# -*- coding: utf-8 -*-
"""
Created on Mon Nov 19 08:15:05 2018

@author: jmajor
"""

##imports
import os
import tkinter as tk
from tkinter import ttk

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style
import matplotlib.pyplot as plt
import time
import pandas as pd
import numpy as np

LARGE_FONT = ('Verdanna', 12)


class TIM_stand(tk.Tk): #inhearits tk.TK class attributes

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




#this is the main page that is called initially
class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent) #parent is going to be the main class SeaofBTCapp
        label = ttk.Label(self, text = 'Graph Page', font = LARGE_FONT)
        label.pack(pady=10,padx=10)

        button = ttk.Button(self, text = "Zoom graph 1", command = controller.click)
        button.pack(side = tk.TOP)

