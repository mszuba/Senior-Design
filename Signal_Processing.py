# Double check to make sure that these are the modules needed.
# Is it better to use scipy or numpy fft?

from threading import Thread, Event, Lock
import socket
from scipy import signal
from scipy.fftpack import fft, fftshift
import numpy as np

class Sig_Proc(Thread):
    def __init__(self,IP_Addr,Port):
        """Constructor for Signal Processing Class"""
        self.lock = Lock()
        self.event = Event()
        self.buffer_size = 1024
        self.window_size = 1024
        self.fft_size = 2048
        self.IP_Addr = IP_Addr
        self.Port = Port
        self.sock = 0       # set up socket connection here
        self.data = []

    def rec_data(self):
        """Recieves data from the socket connection"""
        return [0]

    def win_and_fft(self):
        """Windows data and does FFT"""
        return [0]

    def bin_select(self):
        """selects FFT bin for processing"""
        return [0]

    def run(self):
        """Runs the functions in class"""
        self.data = self.rec_data()
        self.win_and_fft()
        selected_bin = self.bin_select
        print(selected_bin)     # Test output
