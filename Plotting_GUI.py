import socket, serial
from scipy.fftpack import fft, ifft, fftshift
from scipy import signal
import matplotlib.pyplot as plt
import numpy as np
from tkinter import *
from PIL import ImageTk, Image
import os, time

class Window(Frame):

    def __init__(self, s, a, master=None):
        Frame.__init__(self, master)                 
        self.master = master
        self.init_window()
        self.sock = s
        self.data = []
        self.ard = a
        self.fft_size = 2048

    #Creation of init_window
    def init_window(self):
        self.master.title("TESTING GUI")
        self.pack(fill=BOTH, expand=1)
        
        def run_motors():
            """Runs motors based on inputs given"""
            def format_data(e_d, e_m, a_d, a_m,fn,axis):
                """Formats a message for send_data function"""
                # Message Protocol "99, Ele dir, Ele deg, Azi dir, Azi deg, function, axis, 99" 
                # Message Struct   "99,    X   ,    XX  ,    X   ,   XX   ,    X    ,  X  , 99"
                e_m = int(e_m)
                a_m = int(a_m)

                # pad a zero to e_m and a_m if less than two digits
                if(e_m < 10):
                    e_m_str = "0" + str(e_m)
                else:
                    e_m_str = str(e_m)

                if(a_m < 10):
                    a_m_str = "0" + str(a_m)
                else:
                    a_m_str = str(a_m)

                formated_msg = "99"+str(e_d)+(e_m_str)+str(a_d)+(a_m_str)+str(fn)+str(axis)+"99"
                return formated_msg

            def send_data(data):
                    """Sends data to arduino"""
                    self.ard.flush
                    sys.stdout.flush()
                    strTemp = str(data)
                    strTemp_encoded = strTemp.encode("ascii")
                    print("Python value sent: ")
                    print(strTemp)
                    not_confirmed = True
                    i = 0
                    while not_confirmed:  
                            self.ard.write(strTemp_encoded)
                            time.sleep(.2)
                            received_str = self.ard.readline().decode()
                            print(received_str)                    
                            if (received_str == strTemp):
                                    not_confirmed = False 
                                    exit()
                                    self.ard.flush
                                    sys.stdout.flush()
                            i = 1 + i   
                            if i > 10:
                                    exit()  #This will need to send a message to the GUI about somehtign not working
                                    self.ard.flush
                                    sys.stdout.flush()
            def drive_stepper(e_d, e_m, a_d, a_m, axis):
                """Drives steppers with input"""
                send_string = format_data(e_d, e_m, a_d, a_m,0,axis)
                send_data(send_string)

            az = az_val.get()
            el = el_val.get()
            # send the direction to motors
            try: # try except to catch invalid input
                if(el < 0):
                    el_dir = 0
                else:
                    el_dir = 1
                if(az < 0):
                    az_dir = 0
                else:
                    az_dir = 1
                print('Az {} El: {}'.format(str(az),str(el)))
                drive_stepper(el, el_dir, az, az_dir, 0) # 0 is azimuth, 1 is elevation
                drive_stepper(el, el_dir, az, az_dir, 1) 
            except:
                pass

        title_label = Label(self, text="TEAM ROGUE", bg="black",fg = "white",font=("Helvetica", 14))
        title_label.place(x = 100, y = 0)

        RxButton = Button(self, text="Rx Data",command=self.Rx_data)
        RxButton.place(x=50,y=50)

        plotdataButton = Button(self, text="Plot Data",command=self.plot_data)
        plotdataButton.place(x=50,y=100)

        plotFFTButton = Button(self, text="Plot FFT of Data",command=self.plot_fft_data)
        plotFFTButton.place(x=50,y=150)
        
        plotWindowedButton = Button(self, text="Plot Windowed Data",command=self.plot_windowed_data)
        plotWindowedButton.place(x=50,y=200)

        az_label = Label(self, text="Az")
        az_label.place(x = 50, y = 250)
        az_val = Entry(self, width = 10)
        az_val.place(x = 80, y = 250)
        
        el_label = Label(self, text="El")
        el_label.place(x = 50, y = 280)
        el_val = Entry(self, width = 10)
        el_val.place(x = 80, y = 280)

        motorButton = Button(self, text="Move",command=run_motors)
        motorButton.place(x = 150,y = 265)
        
        motorReadButton = Button(self, text="Read Position",command=self.read_position)
        motorReadButton.place(x = 200,y = 265)
        
        binButton = Button(self, text="Select Bin",command=self.bin_select)
        binButton.place(x=50,y=310)

        phaseButton = Button(self, text="Extract Phase",command=self.phase_extraction)
        phaseButton.place(x=50,y=350)

        quitButton = Button(self, text="Exit",command=self.force_quit)
        quitButton.place(x=50, y=400)

    def force_quit(self):
        exit()

    def Rx_data(self):
        """Receives data to plot"""
        self.data.clear()
        n=0
        data_rx = s.recv(BUFFER_SIZE)
        while n < 1024:
            try:
                #print(data_rx[n])
                if(n == 0):
                    self.data.append(0)
                else:
                    self.data.append(float(data_rx[n]))
            except:
                pass
            n+=1
        print('Data Received.')
        #print(self.data)   # for testing
        

    def plot_data(self):
        """Plots data as function of time"""
        N = 1024
        T=1/5000000
        x = np.linspace(0.0,N*T,N)
        plt.plot(x,self.data)
        plt.show()

    def plot_windowed_data(self):
        """Plots data after being windowed"""
        N = 1024
        #sample spacing
        T = 1.0/N
        x = np.linspace(0.0,N*T,N)
        y = np.sin(50.0*2.0*np.pi*x) + 0.5*np.sin(80.0*2.0*np.pi*x)
        y = self.data
        yf = fft(y)
        #create window on data
        w = np.hanning(N)
        ywf = fft((y*w))
        #xf = np.linspace(0.0,1.0/(2.0*T), N/2)
        xf = np.linspace(0,1,len(ywf))
        #plot the data
        #plt.semilogy(xf[1:N//2], 2.0/N * np.abs(yf[1:N//2]), '-b')
        plt.semilogy(xf[1:N//2], 2.0/N * np.abs(ywf[1:N//2]), '-r')
        plt.legend(['FFT', 'FFT w. window'])
        plt.xlabel("Normalized frequency")
        plt.grid()
        plt.show()

    def plot_fft_data(self):
        """Plots data after the FFT"""
        N = 1024
        #sample spacing
        T = 1.0/N
        x = np.linspace(2400,2480,N)
        y = self.data
        yf = fft(y)
        #create window on data
        xf = np.linspace(0, 1, len(yf))
        #plot the data
        plt.semilogy(xf[1:N//2], 2.0/N * np.abs(yf[1:N//2]), '-b')
        plt.legend(['FFT'])
        plt.xlabel("Normalized frequency")
        plt.grid()
        plt.show()

    def phase_extraction(self):
        """Extract phases from selected bin"""
        def phasepopupmsg(phase_rad, phase_deg):
            """Pop up msg shows motor actual position"""
            Ppopup = Tk()
            Ppopup.geometry("300x150")
            Ppopup.wm_title("Phase Extraction")
            phase_msg = "Extracted Phase: " + str(phase_rad) + " rad"
            phase_msg2 = "Extracted Phase: " + str(phase_deg) + " deg"
            label = Label(Ppopup, text=phase_msg)
            label.pack(side="top", fill="x", pady=10)
            label2 = Label(Ppopup, text=phase_msg2)
            label2.pack(side="top", fill="x", pady=10)
            B = Button(Ppopup, text="Exit", command = Ppopup.destroy)
            B.pack()
        y = fft(self.data)
        mag_ar = np.absolute(y)
        mag_ar[0] = 0
        bin_val = np.argmax(mag_ar)
        phase_data_rad = np.angle(y[bin_val])
        phase_data_deg = np.angle(y[bin_val]) * 57.2958
        phasepopupmsg(phase_data_rad, phase_data_deg)

    def bin_select(self):
        """selects FFT bin for processing""" #------------currently not used; part of p_e()----
        def popupmsg(msg_a,msg_b):
            """Creates pop up message"""
            popup = Tk()
            popup.wm_title("Bin Selection")
            popup.geometry("300x150")
            labela = Label(popup, text=msg_a)#, font=NORM_FONT)
            labela.pack(side="top", fill="x", pady=10)
            labelb = Label(popup, text=msg_b)#, font=NORM_FONT)
            labelb.pack(side="top", fill="x", pady=10)
            B1 = Button(popup, text="Exit", command = popup.destroy)
            B1.pack()
        y = self.data
        #yf = fft(y,1024)
        w = np.hanning(1024)
        yf = fft((y))
        mag_ar = np.absolute(yf)
        mag_ar[0] = 0
        #print(mag_ar)  # for testing
        bin_val = np.argmax(mag_ar)
        selected_freq = bin_val * 2444 + 2419000000
        msg1 = "Selected Bin: " +str(bin_val)
        msg2 ="Selectred frequency: {} Hz".format(selected_freq)
        popupmsg(msg1,msg2)
        

    def read_position(self):
        """Reads position back from motors"""
        def motorpopupmsg(a,e):
            """Pop up msg shows motor actual position"""
            popup2 = Tk()
            popup2.geometry("200x150")
            popup2.wm_title("Bin Selection")
            az_msg = "Azimuth Degrees: " + str(a)
            el_msg = "Elevation Degrees: " + str(e)
            labela = Label(popup2, text=az_msg)
            labela.pack(side="top", fill="x", pady=10)
            labelb = Label(popup2, text=el_msg)
            labelb.pack(side="top", fill="x", pady=10)
            B = Button(popup2, text="Exit", command = popup2.destroy)
            B.pack()
        try:
            recv_msg = self.ard.readline()
            data = recv_msg.split(',')
            az = data[0]
            el = data[1]
            motorpopupmsg(az,el)
        except:
            motorpopupmsg('N/A','N/A')

if __name__ == '__main__':
    root = Tk()
    root.geometry("300x450")

    # find command to run GNU blocks for receiving
    host = '192.168.10.1' #check host number to match USRP's IP 
    port = 12345
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('',port))
    BUFFER_SIZE = 1472

    try:
        ardunio = serial.Serial('COM3', 9600, timeout = 2)
    except:
        arduino = 0
    app = Window(s,arduino, root)
    root.mainloop()