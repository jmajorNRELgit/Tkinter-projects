# -*- coding: utf-8 -*-
"""
Created on Mon Oct 29 15:32:42 2018

@author: jmajor
"""
from tkinter import *

class Window(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master


    def init_window(self):
        self.master.title("GUI")



root = Tk()

app = Window(root)

root.mainloop()