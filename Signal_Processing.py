from threading import Thread, Event, Lock
import socket
from scipy import signal
from scipy.fftpack import fft, fftshift
import numpy as np

class Sig_Proc(Thread):
    def __init__(self,IP_Addr,port):
        """Constructor for Signal Processing Class"""
        Thread.__init__(self)
        self.lock = Lock()
        self.event = Event()
        self.buffer_size = 1024
        self.window_size = 1024
        self.fft_size = 2048
        self.IP_Addr = IP_Addr
        self.port = port
        self.sock = 0       # set up socket connection in function
        self.stream_data = np.array([])
        self.win_data = np.array([])
        self.fft_data = np.array([])
        self.phase_data = np.array([])
        self.win = np.hanning(self.window_size)

    def make_connection(self, i):
        """Set up connection to N210 USRP"""
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(('',self.port))
        BUFFER_SIZE = 1472
                

    def rec_data(self):
        """Recieves data from the socket connection"""
        # self.data = usrp.read(self.buffer_size)
        # grab data from correct receiver
        # make a buffer (1024 current size) for how much data to process at once
        return [0]

    def rec_from_file(self):
        """Test function to read data from file"""

    def win_and_fft(self):
        """Windows data and does FFT"""
        self.win_data = self.stream_data * self.win
        self.fft_data = fft(self.win_data)

    def bin_select(self):
        """selects FFT bin for processing""" #------------currently not used; part of p_e()----
        # want to select bin for 2.4# GHz depending
        # on channel being used for testing
        mag_ar = np.absolute(self.fft_data)
        bin_val = np.nanargmax(mag_ar)
        return bin_val
    
    def phase_extraction(self):
        """Extract phases from selected bin"""
        mag_ar = np.absolute(self.fft_data)
        bin_val = np.nanargmax(mag_ar)
        self.phase_data = np.angle(self.fft_data[bin_val])

    def run_cycle(self):
        """Runs the functions in class"""
        self.data = self.rec_data()
        self.win_and_fft()
        self.phase_extraction()
        #print(selected_bin)     # Test output
        return self.phase_data

    def run(self):
        # Runs by default
        pass
