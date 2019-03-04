import Signal_Processing
import Phase_Comparison as PComp
#import Motor_Control
#import System_Response
import threading
import numpy as np

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

# Fucntion Calls
SP1.stream_data = y #sample data
SP2.stream_data = y #sample data
SP3.stream_data = y #sample data
SP4.stream_data = y #sample data
#-------------------------------------------------------
#-------------------------------------------------------
#-------------------------------------------------------


# Loop together processes
def system_loop():
    """Loops together processes"""

if __name__ == '__main__':
    # Define variables needed

    # Start signal processing threads
    SP1.start()
    SP2.start()
    SP3.start()
    SP4.start()
   
    while True:
        pd_1 = SP1.run_cycle()
        pd_2 = SP2.run_cycle()
        pd_3 = SP3.run_cycle()
        pd_4 = SP4.run_cycle()

        PComp.phase_comp(pd_1[1],pd_2[1],pd_3[1],pd_4[1])

        break       # for testing

    # Close Threads
    SP1.join()
    SP2.join()
    SP3.join()
    SP4.join()

    # Shutdown System
    