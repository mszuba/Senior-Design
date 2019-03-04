# Double check to make sure that these are the modules needed.
# Is it better to use scipy or numpy fft?

from threading import Thread, Event, Lock
import socket
from scipy import signal
from scipy.fftpack import fft, fftshift
import numpy as np
import Phase_Comparison as PC     #can run phase comparison functions in here

class Sig_Proc(Thread):
    def __init__(self,IP_Addr,Port):
        """Constructor for Signal Processing Class"""
        Thread.__init__(self)
        self.lock = Lock()
        self.event = Event()
        self.buffer_size = 1024
        self.window_size = 1024
        self.fft_size = 2048
        self.IP_Addr = IP_Addr
        self.Port = Port
        self.sock = 0       # set up socket connection in function
        self.stream_data = np.array([])
        self.win_data = np.array([])
        self.fft_data = np.array([])
        self.phase_data = np.array([])
        self.win = np.hanning(self.window_size)

    def make_connection(self):
        """Set up connection to N210 USRP"""
        

    def rec_data(self):
        """Recieves data from the socket connection"""
        # self.data = usrp.read(self.buffer_size)
        return [0]

    def rec_from_file(self):
        """Test function to read data from file"""

    def win_and_fft(self):
        """Windows data and does FFT"""
        self.win_data = self.stream_data * self.win
        self.fft_data = fft(self.win_data)

    def bin_select(self):
        """selects FFT bin for processing"""
        # want to select bin for 2.4# GHz depending
        # on channel being used for testing
        return 0
    
    def phase_extraction(self):
        """Extract phases from selected bin"""
        #for n in self.fft_data:
        #   self.phase_data[n]=np.angle(self.fft_data[n])
         
        #-----for testing-----
        self.phase_data = [0,1,2]

    def run_cycle(self):
        """Runs the functions in class"""
        self.data = self.rec_data()
        self.win_and_fft()
        selected_bin = self.bin_select()
        self.phase_extraction()
        print(selected_bin)     # Test output
        return self.phase_data

    def run(self):
        # Runs by default
        pass
