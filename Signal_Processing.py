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
        self.BUFFER_SIZE = 1024
        self.window_size = 1024
        self.fft_size = 2048
        self.IP_Addr = IP_Addr
        self.port = port
        #self.sock = 0       # set up socket connection in function
        self.stream_data = np.array([])
        self.win_data = np.array([])
        self.fft_data = np.array([])
        self.phase_data = np.array([])
        self.win = np.hanning(self.window_size)

    def make_connection(self):
        """Set up connection to N210 USRP"""
        self.lock.acquire()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(('',self.port))
        self.BUFFER_SIZE = 1472
        self.lock.release()

    def close_stream(self):
        """Close the stream"""
        self.sock.close()

    def rec_data(self):
        """Recieves data from the socket connection"""
        self.lock.acquire()
        data = []
        n=0
        data_rx = self.sock.recv(self.BUFFER_SIZE)
        while n < 1024:
            try:
                data.append(float(data_rx[n]))
            except:
                data.append(0)
            n+=1
        self.stream_data = np.asarray(data)
        #print("Data from port {} received.".format(str(self.port))) # for testing
        #print('Lenght = {}'.format(str(len(self.stream_data))))
        #np.append(self.stream_data, data)
        self.lock.release()
        return 0

    def rec_from_file(self):
        """Test function to read data from file"""

    def win_and_fft(self):
        """Windows data and does FFT"""
        self.win_data = self.stream_data * self.win
        self.fft_data = fft(self.win_data, self.fft_size)

    def bin_select(self):
        """selects FFT bin for processing""" #------------currently not used; part of p_e()----
        # want to select bin for 2.4# GHz depending
        mag_ar = np.absolute(self.fft_data)
        mag_ar[0] = 0
        bin_val = np.nanargmax(mag_ar)
        return bin_val

    def phase_extraction(self):
        """Extract phases from selected bin"""
        mag_ar = np.absolute(self.fft_data)
        mag_ar[0] = 0
        bin_val = np.argmax(mag_ar)
        #bin_val = 512
        self.phase_data = np.angle(self.fft_data[bin_val])

    def run_cycle(self):
        """Runs the functions in class"""
        #self.lock.acquire()
        self.data = self.rec_data()
        self.win_and_fft()
        self.phase_extraction()
        #print(selected_bin)     # Test output
        #self.lock.release()

    def run(self):
        # Runs by default
        pass
