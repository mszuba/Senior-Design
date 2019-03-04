import Signal_Processing
import numpy as np
import matplotlib.pyplot as plt

# Create Single class
SP1 = Signal_Processing.Sig_Proc('192.168.10.10',5005)

# Testing values
N = 1024
T = 1.0/800.0
x = np.linspace(0.0,N*T,N)
y = np.sin(50.0*2.0*np.pi*x)

# Fucntion Calls
SP1.stream_data = y #sample data
SP1.run()
print(np.angle(SP1.fft_data[0],deg=1))
print(np.angle(SP1.fft_data[1],deg=1))
print(np.angle(SP1.fft_data[2],deg=1))
print(np.angle(SP1.fft_data[3],deg=1))
print(np.angle(SP1.fft_data[4],deg=1))
print(np.angle(SP1.fft_data[5],deg=1))
# Plot results
freq = np.linspace(-0.5, 0.5, 1024)
plt.plot(freq, SP1.fft_data)
plt.axis([-0.5, 0.5, -50, 100])
plt.title("Frequency response of the Hanning window")
plt.ylabel("Normalized magnitude [dB]")
plt.xlabel("Normalized frequency [cycles per sample]")
plt.show()
