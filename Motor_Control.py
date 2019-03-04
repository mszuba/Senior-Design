import serial

#---------------------------------------------------
#---------------Arduino Connection------------------
#---------------------------------------------------
ard = serial.Serial('COM3', 9600, timeout = 0)
print(ard.is_open)  # test connection

def test_ard_connection():
    if(ard.in_waiting > 0):
        print(ard.readline())
        ard.flushInput()

def main():
    '''Run other functions here'''
    test_ard_connection()

main()
ard.close()     # close arduino serial connection