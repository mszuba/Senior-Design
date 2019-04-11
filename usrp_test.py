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
BUFFER_SIZE = 1472
#s.setblocking(0)
data = []

print('Rx data...')
counter = 0
while True:
    n=0
    data_rx = s.recv(BUFFER_SIZE)
    while n < BUFFER_SIZE:
        print(data_rx[n])
        data.append(float(data_rx[n]))
        n+=1
    break #for testing

#conn.close()
s.close()
N = BUFFER_SIZE
T=1/N
x = np.linspace(0.0,N*T,N)
w = np.hanning(N)
yf = fft(data)
ywf = fft((w*data))
plt.plot(x,data)
plt.show()

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
