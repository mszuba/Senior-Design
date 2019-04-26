import Signal_Processing
import Phase_Comparison as PComp
#import Motor_Control
#import System_Response
import threading
import serial
import numpy as np
import time
import sys

#create connections
ard = serial.Serial('COM3', 9600, timeout = 2)

# Create Class instances

SP1 = Signal_Processing.Sig_Proc('192.168.10.1',12345)
SP2 = Signal_Processing.Sig_Proc('192.168.10.1',12346)
SP3 = Signal_Processing.Sig_Proc('192.196.10.11',12347)
SP4 = Signal_Processing.Sig_Proc('192.196.10.11',12348)

#-------------------------------------------------------
#----------FOR TESTING WITHOUT STREAM-------------------
#-------------------------------------------------------
# Create simulated data

# Testing values
N = 1024
T = 1.0/800.0
x = np.linspace(0.0,N*T,N)
y = np.sin(50.0*2.0*np.pi*x)
y2 = np.sin(50.0*2.0*np.pi*x+np.pi/2) # delayed pi/2 degrees
# Fucntion Calls
#SP1.stream_data = y #sample data
#SP2.stream_data = y2 #sample data
SP3.stream_data = y2 #sample data
SP4.stream_data = y #sample data
#-------------------------------------------------------
#-------------------------------------------------------
#-------------------------------------------------------


# Loop together processes
def system_loop():
    """Loops together processes"""

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
        
        ard.flush
        sys.stdout.flush()
        strTemp = str(data)
        strTemp_encoded = strTemp.encode("ascii")
        print("Python value sent: ")
        print(strTemp)
        not_confirmed = True
        i = 0
        while not_confirmed:  
                ard.write(strTemp_encoded)
                time.sleep(.2)
                received_str = ard.readline().decode()
                print(received_str)                    
                if (received_str == strTemp):
                        not_confirmed = False 
                        exit()
                        ard.flush
                        sys.stdout.flush()
                i = 1 + i   
                if i > 10:
                        exit()  #This will need to send a message to the GUI about somehtign not working
                        ard.flush
                        sys.stdout.flush() 

def hold_fn():

    time.sleep(1) 
    not_finished = True
    p = 0
    while not_finished:  
            received_str = ard.readline().decode()
            print(received_str)
            if (received_str == "222"): #This is the finished function message
                    not_finished = False 
                    exit()
                    ard.flush
                    sys.stdout.flush()
            p = 1 + p   
            if p > 1000:
                    exit()  
                    ard.flush
                    sys.stdout.flush()

def run_initialization():
    """Runs the system callobration before use"""
    init_message_az  = "990000000099"
    init_message_ele = "990000000199"
    send_data(init_message_az)
  #  hold_fn()       #This prolly doesnt work.
    time.sleep(20)              #I need the arduino sketch to tell this fn when its finished and when to start.
    send_data(init_message_ele)
  #  hold_fn()
    time.sleep(20)              #I need the arduino sketch to tell this fn when its finished and when to start.

def trigger_buzzer():
    buzzer_message = "990000002099"
    send_data(buzzer_message)

def drive_stepper(e_d, e_m, a_d, a_m, axis):
    send_string = format_data(e_d, e_m, a_d, a_m,0,axis)
    send_data(send_string)

def rec_data():
    """Receive position data back from arduino"""
    pos = False
    read_data = ard.readline().decode()
    ard.flushInput()
    if(len(read_data) < 1 ):
        read_data = 'null'
    if(read_data == '1'):
        pos = True
    else:
        pass
    return pos


if __name__ == '__main__':
    # Define variables needed
    az_1 = []
    az_2 = []
    el_1 = []
    el_2 = []
    az_move = 0
    el_move = 0
    at_position = False

    # Run System Calobration
    #run_callobration()

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


        # sending data to arduino for motor controller here
        func = 1
        ax = 1
        msg = format_data(el_dir, el_move, az_dir, az_move, func, ax)
        send_data(msg)

        if(abs(az_move) < 3 and abs(el_move) < 3):
            #--------Trigger the Jammer here--------
            print('Jammer Activated!!!')    # for testing
        else:
            pass

        break # for testing

    # for testing
    print('Time: ', time.time()-start)

    # Close Threads
    SP1.join()
    SP2.join()
    SP3.join()
    SP4.join()

    # Shutdown System
