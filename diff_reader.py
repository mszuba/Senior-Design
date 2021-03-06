import socket
from scipy.fftpack import fft, ifft
from scipy import signal
import matplotlib.pyplot as plt
import numpy as np

# set up server side (run first)

host = '192.168.10.1' #check host number to match USRP's IP
port = 12345
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('',port))
BUFFER_SIZE = 1472 #number of phase difference samples
#s.setblocking(0)
data = []

print('Rx data...')
count = 0
counter = 0
while True:
    n=0
    data_rx = s.recv(BUFFER_SIZE)
    while n < BUFFER_SIZE:
        try:
            #print(data_rx[n])
            data.append(float(data_rx[n]))
            count+=1
        except:
            print('Error on {}'.format(str(n)))
            pass
        n+=1
    print('Number of data samples: ',count)
    count = 0
    #break #for testing

    print('Loop {} complete.'.format(str(counter)))
    counter+=1
    if(counter > 8):
        break

s.close()

'''
N = BUFFER_SIZE #number of phase difference samples
T=1/N
t = np.linspace(0.0,N*T,N)
plt.plot(t,data)    #should plot phase difference over time
plt.show()
'''