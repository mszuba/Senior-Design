import Signal_Processing
import Phase_Comparison as PComp
#import Motor_Control
#import System_Response
import threading
import serial
import numpy as np
import time

#create connections
ard = serial.Serial('COM3', 9600, timeout = 2)

# Create Class instances

SP1 = Signal_Processing.Sig_Proc('192.168.10.10',5005)
SP2 = Signal_Processing.Sig_Proc('192.168.10.10',5006)
SP3 = Signal_Processing.Sig_Proc('192.196.10.11',5007)
SP4 = Signal_Processing.Sig_Proc('192.196.10.11',5008)

#-------------------------------------------------------
#----------FOR TESTING WITHOUT STREAM-------------------
#-------------------------------------------------------

# Testing values
N = 1024
T = 1.0/800.0
x = np.linspace(0.0,N*T,N)
y = np.sin(50.0*2.0*np.pi*x)
y2 = np.sin(50.0*2.0*np.pi*x+np.pi/2) # delayed pi/2 degrees
# Fucntion Calls
SP1.stream_data = y #sample data
SP2.stream_data = y2 #sample data
SP3.stream_data = y2 #sample data
SP4.stream_data = y #sample data
#-------------------------------------------------------
#-------------------------------------------------------
#-------------------------------------------------------


# Loop together processes
def system_loop():
    """Loops together processes"""

def send_data(data):
    data = str(data)
    ard.write(data.encode())

if __name__ == '__main__':
    # Define variables needed
    az_1 = []
    az_2 = []
    el_1 = []
    el_2 = []
    az_move = 0
    el_move = 0

    # Start signal processing threads
    SP1.start()
    SP2.start()
    SP3.start()
    SP4.start()
    #for testing
    start = time.time()
    while True:
        counter = 0
        # Collect and process samples
        while counter < 200:
            phase_1 = SP1.run_cycle()
            phase_2 = SP2.run_cycle()
            phase_3 = SP3.run_cycle()
            phase_4 = SP4.run_cycle()

            a_1,a_2,e_1,e_2 = PComp.phase_comp(phase_1,phase_2,phase_3,phase_4)
            az_1.append(a_1)
            az_2.append(a_2)
            el_1.append(e_1)
            el_2.append(e_2)
            #break       # for testing
            counter+=1

        # Average together data
        az_move, el_move = PComp.average_angles(az_1,az_2,el_1,el_2)

        if(az_move < 0):
            az_dir = 0
        else:
            az_dir = 1
        if(el_move < 0):
            el_dir = 0
        else:
            el_dir = 1

        az_move = np.abs(az_move)
        el_move = np.abs(el_move)

        msg = str(az_dir)+','+str(az_move)+','+str(el_dir)+','+str(el_move)

        send_data(msg)

        #send motor controller data here
        #mc.rx_message()


        break # for testing
    # for testing
    print('Time: ', time.time()-start)
    # Close Threads
    SP1.join()
    SP2.join()
    SP3.join()
    SP4.join()

    # Shutdown System
