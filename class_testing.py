import Signal_Processing
import Phase_Comparison as PComp
import threading
import serial
import numpy as np
import time
import sys


# Create Class instances

SP1 = Signal_Processing.Sig_Proc('192.168.10.2',12345)
SP2 = Signal_Processing.Sig_Proc('192.168.10.3',12346)
#SP3 = Signal_Processing.Sig_Proc('192.196.10.4',12347)
#SP4 = Signal_Processing.Sig_Proc('192.196.10.5',12348)

SP1.make_connection()   # open socket connections for each thread
SP2.make_connection() 

 # Start signal processing threads
#SP1.start()
#SP2.start()
#SP3.start()
#SP4.start()
#for testing
start = time.time()
while True:
    counter = 0
    # Collect and process samples
    while counter < 200:
        phase_1 = SP1.run_cycle()
        #print(phase_1)
        phase_2 = SP2.run_cycle()
        #phase_3 = SP3.run_cycle()
        #phase_4 = SP4.run_cycle()

        #a_1,a_2,e_1,e_2 = PComp.phase_comp(phase_1,phase_2,phase_3,phase_4)
        #az_1.append(a_1)
        #az_2.append(a_2)
        #el_1.append(e_1)
        #el_2.append(e_2)
        #break       # for testing
        counter+=1
    break

# for testing
print('Time: ', time.time()-start)

# Close Threads
#SP1.join()
#SP2.join()
#SP3.join()
#SP4.join()

# Shutdown System
