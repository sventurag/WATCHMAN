import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Tkagg')
import itertools
import matplotlib.gridspec as gridspec
from pylab import *
import matplotlib.animation as animation

"""
Class for getting data from a binary file and save it in a
text file to feed a script or kst for plotting the data
for each channel
The code assumes the following data structure:
1 byte       1 byte      512 bytes   1 byte
startCode | window number| payload | endCode
in uint16 format.
"""
class binary2text():

    def __init__(self,file, plot=False):
        self.file = file
        self.int_array = np.fromfile(self.file, dtype = np.uint16) # asumes 16-bit data and create an integers array
        self.windowSize = 1030
        self.payloadSize = 512
        self.windowNumberByteIndex = 1
        self.payloadStartByteIndex = 2
        self.numberofSamples = 32
        # create a list with the window numbers, byte 1 from each window  
        windowsNumbers = [self.int_array[x] for x in range(self.windowNumberByteIndex,len(self.int_array), int(self.windowSize/2)) ] 
        
        self.numberofWindows = len(windowsNumbers)
       # get the data from each window asumming a self.windowSize, payload[window][data] 
        payload = [self.int_array[x:x + self.payloadSize] for x in range( self.payloadStartByteIndex,len(self.int_array), int(self.windowSize/2) ) ]
       
        #self.numberofChannels = len(payload)
       # create a nested list from the payload, windows_and_channels[window][channel][sample] 

        self.windows_and_channels = [ [ payload[i][ x:x + 32] for x in range(0,len(payload[i]),32)   ] for i in range(self.numberofWindows)] 
        
        self.numberofChannels = len(self.windows_and_channels[0])


        self.data_by_channel = list()
        for i in range(len(self.windows_and_channels[0])): 
            self.data_by_channel.append( self.same_channel(i,15,self.windows_and_channels).tolist() ) 
        out_file = '%s.txt'%(self.file.split('.')[0])
        np.savetxt(out_file, np.array(self.data_by_channel).T, fmt='%s')
        print('file : ','%s'%(out_file), 'saved' )
        if plot == True:
        
            plt.suptitle('%s'%file)
            nPlots = self.numberofChannels
            gs = gridspec.GridSpec(nPlots,1)
            gs.update(hspace=0.1)
            plt.title('Windows')
            for i in range(0,nPlots,1):
                plt.subplot(nPlots,1,(i+1))
                ax = plt.subplot(gs[i,0])
                ax.clear()
                ax.plot(self.same_channel(i,self.numberofWindows,self.windows_and_channels))
                ax.set_ylabel('%s'%i, rotation = 0, color='red')
                xlimsup = self.numberofSamples*self.numberofWindows
                plt.xlim([0,xlimsup])
                for j in range(self.numberofWindows+1):
                    ax.axvline(j*32,color='k')
        plt.show()   

    def same_channel(self, channel, numberWindows,list_to_flat):
        """
         Get the same channel from different windows
        """
        sameChannel=np.array([])
        for i in range(numberWindows):
            sameChannel = np.concatenate((sameChannel,list_to_flat[i][channel] ),axis = None  )
        return sameChannel


