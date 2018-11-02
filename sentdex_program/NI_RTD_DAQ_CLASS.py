# -*- coding: utf-8 -*-
"""
Created on Mon Oct  8 14:43:15 2018

This is a class module for the NI USB DAQ with eight 3 wire RTD's

@author: jmajor
"""

import nidaqmx
from nidaqmx.constants import ExcitationSource, TemperatureUnits, ResistanceConfiguration

def path():
    fjskla;fjsaklkf jkljfsal


class DAQ(object):

    '''Sets up the DAQ task and assigns 8 RTD channels to it'''
    def __init__(self):
        self.name = 'NI USB RTD DAQ'

        self.task = nidaqmx.Task()

        self.task2 = nidaqmx.Task()

        self.all_channels = [0,1,2,3,4,5,6,7] #RTD channels.

        self.specific_channels = []

        for i in self.all_channels:

            self.task.ai_channels.add_ai_rtd_chan('cDAQ1Mod1/ai{0}'.format(i), ###open the program NIMAX to see channel names###
                                     current_excit_source=ExcitationSource.INTERNAL,
                                     resistance_config = ResistanceConfiguration.THREE_WIRE,
                                     units=TemperatureUnits.DEG_C,
                                     current_excit_val= .001)




    def read_all_channels(self):
        '''Reads all RTD channels assigned in __init__ and returns a list of the readout'''

        temperatures = self.task.read(1)

        flat = [item for sublist in temperatures for item in sublist] #takes the list of lists and flattens it
        flat = [round(num, 4) for num in flat] #rounds each float in the list
        return flat


    def set_specific_channels(self, channel_list):
        '''Sets the specific channels the user wants to read. Takes a list as an argument.'''

        channel_list = [i-1 for i in channel_list]
        try:
            for i in channel_list:
                self.task2.ai_channels.add_ai_rtd_chan('cDAQ1Mod1/ai{0}'.format(i), ###open the program NIMAX to see channel names###
                                         current_excit_source=ExcitationSource.INTERNAL,
                                         resistance_config = ResistanceConfiguration.THREE_WIRE,
                                         units=TemperatureUnits.DEG_C,
                                         current_excit_val= .001)

        except: #used in case the set channels changes
            self.task2.close()
            self.task2 = nidaqmx.Task()
            for i in channel_list:
                self.task2.ai_channels.add_ai_rtd_chan('cDAQ1Mod1/ai{0}'.format(i), ###open the program NIMAX to see channel names###
                                         current_excit_source=ExcitationSource.INTERNAL,
                                         resistance_config = ResistanceConfiguration.THREE_WIRE,
                                         units=TemperatureUnits.DEG_C,
                                         current_excit_val= .001)


    def read_specific_channels(self):
        '''Reads user defined channels'''

        temperatures = self.task2.read(1)

        if len(temperatures) ==1:
            return temperatures

        flat = [item for sublist in temperatures for item in sublist] #takes the list of lists and flattens it
        flat = [round(num, 4) for num in flat] #rounds each float in the list
        return flat






    def close_NI_RTD_DAQ(self):
        '''Closes the task'''

        self.task.close()

        self.task2.close()




if __name__ == '__main__':
    daq = DAQ()
    daq.set_specific_channels([2,5,7])
    print(daq.read_specific_channels())

