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

        self.init_window()


    def init_window(self):
        self.master.title("GUI")

        self.pack(fill = BOTH, expand = 1)

        quitButton = Button(self, text = "Quit", command = self.client_exit)

        quitButton.place(x=0, y=0)

    def client_exit(self):
        print('It worked')


def run_window():
    root = Tk()

    root.geometry("400x300")

    app = Window(root)

    root.mainloop()