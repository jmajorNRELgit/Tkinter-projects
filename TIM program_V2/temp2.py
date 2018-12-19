# -*- coding: utf-8 -*-
"""
Created on Wed Dec 19 08:08:32 2018

@author: jmajor
"""

import os
import numpy as np
import time
import pandas as pd

x_start = time.time()

import NI_RTD_DAQ_CLASS as DAQ
daq = DAQ.DAQ()
daq.set_specific_channels([1,2,3,4])

class misc:
    def __init__(self):

        #removes the old data log
        try:
            os.remove('DAQ_data.txt')
        except:
            pass



        self.standard_deviation = []

        #reads the RTD calibration coefficients and creates the functions to fit the data
        coefficients = pd.read_csv('C:/Users/jmajor/Desktop/github/Tkinter-projects/sentdex_program/coefficient_list.csv', index_col = 0)
        self.chan1_fit = np.poly1d(list(coefficients.iloc[:,0]))
        self.chan2_fit = np.poly1d(list(coefficients.iloc[:,1]))
        self.chan3_fit = np.poly1d(list(coefficients.iloc[:,2]))
        self.chan4_fit = np.poly1d(list(coefficients.iloc[:,3]))

        self.fit_list = (self.chan1_fit, self.chan2_fit, self.chan3_fit, self.chan4_fit)

misc = misc()

temp_list = []

while True:

   temp = daq.read_specific_channels() #acquire temp from daq

   #fits temp data to RTD calibration curve
   for i in range(len(misc.fit_list)):
        temp[i] = round(misc.fit_list[i](temp[i]),3)

   temp_list.append(temp)
   standard_deviation = np.mean([np.std(temp_list[-20:]),np.std(temp_list[-20:]),np.std(temp_list[-20:]),np.std(temp_list[-20:])])

   temp_data = str(round(time.time() - x_start,3)) + ','+ str(round(standard_deviation,4)) + ',' + ','.join(list(map(str,temp))) +'\n' #formats time and temp data to save in file

    #saves the data to a txt file
   with open('DAQ_data.txt', 'a') as f:
        if os.stat('DAQ_data.txt').st_size == 0: #if the data file is empty this adds the headers
            f.write('Time(s),STD,One,Two,Three,Four\n')
            f.write(temp_data)
        else:
            f.write(temp_data)
            print('Done')







