import time, serial, sys

ard = serial.Serial('COM3', 9600, timeout = 2)

def format_data(e_d, e_m, a_d, a_m):
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

    formated_msg = "99"+str(e_d)+(e_m_str)+str(a_d)+(a_m_str)+"99"
    return formated_msg

def send_data(data):
        
        ard.flush
        sys.stdout.flush()
        strTemp = str(data)
        strTemp_encoded = strTemp.encode("ascii")
        print ("Python value sent: ")
        print (strTemp)
        not_confirmed = True
        i = 0
        while not_confirmed:  
                ard.write(strTemp_encoded)
                time.sleep(.2)
                received_str = ard.readline().decode()
                print(received_str)  
                if (received_str == strTemp):
                        not_confirmed = False 
                i = 1 +i   
                if i > 10:
                        exit()  #This will need to send a message to the GUI
                        ard.flush
                        sys.stdout.flush()
                        ard.close() 
                        
def run_callobration():
    """Runs the system callobration before use"""
    ROM_msg = ""    # message to run ROM test
    pot_msg = ""    # messgae to callobrate potentiometer
    send_data(ROM_msg)
    send_data(pot_msg)

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


def main():
    while True:
        az_in = input("Azimuth Input: ")
        el_in = input("Elevation Input: ")

        if(az_in == 'q' or el_in == 'q'):
            break

        if(az_in < 0):
            az_in_dir = 0
        else:
            az_in_dir = 1
        if(el_in < 0):
            el_in_dir = 0
        else:
            el_in_dir = 1
        
        data_msg = format_data(el_in_dir,abs(el_in),az_in_dir,abs(az_in))
        send_data(data_msg)

        time.sleep(5)
        # re-run test loop
    ard.close()

main()