import socket
from scipy.fftpack import fft, ifft
from scipy import signal
import matplotlib.pyplot as plt
import numpy as np
import Phase_Comparison as PComp

# set up server side (run first)

host = '192.168.10.1' #check host number to match USRP's IP
port = 12345
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('',port))
BUFFER_SIZE = 1472
#s.setblocking(0)

port2 = 12346
s2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
s2.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s2.bind(('',port2))

port3 = 12347
s3 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
s3.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s3.bind(('',port3))

print('-Connections successful.')

data = []
data2 = []
data3 = []

print('-Rx data 1...')
counter = 0
while True:
    n=0
    data_rx = s.recv(BUFFER_SIZE)
    while n < 1024:
        try:
            print(data_rx[n])
            data.append(float(data_rx[n]))
        except:
            pass
        n+=1
    break #for testing

print('-Rx data 2...')
counter = 0
while True:
    n=0
    data2_rx = s2.recv(BUFFER_SIZE)
    while n < 1024:
        try:
            #print(data2_rx[n])
            data2.append(float(data2_rx[n]))
        except:
            pass
        n+=1
    break #for testing

print('-Rx data 3...')
counter = 0
while True:
    n=0
    data3_rx = s3.recv(BUFFER_SIZE)
    while n < 1024:
        try:
            #print(data2_rx[n])
            data3.append(float(data3_rx[n]))
        except:
            pass
        n+=1
    break #for testing
print('     Len1: {}'.format(str(len(data))))
print('     Len2: {}'.format(str(len(data2))))
print('     Len3: {}'.format(str(len(data3))))
print('-Receiving complete.')

az_1 = []
az_2 = []
el_1 = []
el_2 = []
az_move = 0
el_move = 0
at_position = False

while True:

    counter = 0
    # Collect and process samples
    while counter < 200:
        phase_1 = data_rx[0]
        phase_2 = data2_rx[0]
        phase_3 = data3_rx[0]
        phase_4 = phase_1

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

    print('Az_move: {}  El_move: {}'.format(str(az_move),str(el_move)))
    break

print('-Phase Comparison Complete')

'''print('-Generating Graphs.')
#print(data)
#print(data2)

#conn.close()
s.close()

# ----------- Display signal-----------------
N = 1024
T=1/N
x = np.linspace(0.0,N*T,N)
w = np.hanning(N)
#yf = fft(data)
#ywf = fft((w*data))
plt.plot(x,data)
plt.show()
# ------------- Disply windowed signal-------------
N = 1024
T=1/N
x = np.linspace(0.0,N*T,N)
w = np.hanning(N)
#yf = fft(data)
#ywf = fft((w*data))
plt.plot(x,(w*data))
plt.show()

# ------------- Display FFT of windowed signal -------------
N = 1024
T=1/N
x = np.linspace(0.0,N*T,N)
w = np.hanning(N)
yf = fft(data)
ywf = fft((w*data))
plt.plot(x,ywf)
plt.show()

print('-Graphing Complete.')'''


'''
N = BUFFER_SIZE
T=1/N

y = np.sin(50*2.0*np.pi*x)


w = np.hanning(N)
yf = fft(data)
ywf = fft(data*w)

xf = np.linspace(0.0,1.0/(2.0*T), N/2)
plt.semilogy(xf[1:N//2], 2.0/N * np.abs(yf[1:N//2]), '-b')
plt.semilogy(xf[1:N//2], 2.0/N * np.abs(ywf[1:N//2]), '-r')
plt.semilogy(xf[1:N//2], 2.0/N * np.abs(yf[1:N//2]), '-b')
plt.semilogy(xf[1:N//2], 2.0/N * np.abs(ywf[1:N//2]), '-r')
plt.legend(['FFT', 'FFT w. window'])
plt.grid()
plt.show()
'''
