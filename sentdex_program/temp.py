# -*- coding: utf-8 -*-
"""
Created on Fri Nov  2 08:26:24 2018

@author: jmajor
"""

import NI_RTD_DAQ_CLASS as DAQ
import os
import numpy as np

daq = DAQ.DAQ()

daq.set_specific_channels([2])

for i in range(5):
    temp = str(daq.read_specific_channels()[0])

    s = temp +','+str(i)+'\n'

    with open('daqdata_2.txt', 'a') as f:
        if os.stat('daqdata_2.txt').st_size == 0:
            f.write(s)
        else:
            f.write(s)


