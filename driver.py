import Signal_Processing
import Phase_Comparison
import threading

# Create Class instances

SP1 = Signal_Processing.Sig_Proc('192.168.10.10',5005)
SP2 = Signal_Processing.Sig_Proc('192.168.10.10',5006)
SP3 = Signal_Processing.Sig_Proc('192.196.10.11',5007)
SP4 = Signal_Processing.Sig_Proc('192.196.10.11',5008)

# Loop together processes
def system_loop():
    """Loops together processes"""

if __name__ == '__main__':
    # Start threads
    SP1.start()
    SP2.start()
    SP3.start()
    SP4.start()

    # Join threads (wait to terminate)
    SP1.join()
    SP2.join()
    SP3.join()
    SP4.join()

    # Close Threads

    # Shutdown System
    