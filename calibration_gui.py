from tkinter import *
from PIL import ImageTk, Image
import os

class Window(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)                 
        self.master = master
        self.init_window()
        self.net_state = 1
        self.m1_state = 1
        self.m2_state = 1
        self.sdr1_state = 1
        self.sdr2_state = 1
        self.sdr3_state = 1
        self.sdr4_state = 1
        self.jammer_state = 1

    #Creation of init_window
    def init_window(self):
        self.master.title("System Control")
        self.pack(fill=BOTH, expand=1)

        quitButton = Button(self, text="Exit",bg='grey',command=self.force_quit)
        quitButton.place(x=400, y=550)

        sys_test = Button(self, text="Run System Test",bg='grey',command=self.run_sys_check)
        sys_test.place(x=175,y=550)

        runButton = Button(self, text="Run System",bg='grey',command=self.run_tracker)
        runButton.place(x=300, y=550)

        net = Label(self, text="Network Test")
        net.place(x=100, y=150)

        net_test = Label(self, text="N/A",bg='grey')
        net_test.place(x=300, y=150)

        m1 = Label(self, text="Azimuth Motor")
        m1.place(x=100, y=200)

        m1_test = Label(self, text="N/A",bg='grey')
        m1_test.place(x=300, y=200)

        m2 = Label(self, text="Elevation Motor")
        m2.place(x=100, y=250)
        
        m2_test = Label(self, text="N/A",bg='grey')
        m2_test.place(x=300, y=250)

        sdr1 = Label(self, text="Receiver 1")
        sdr1.place(x=100, y=300)
        
        sdr1_test = Label(self, text="N/A",bg='grey')
        sdr1_test.place(x=300, y=300)

        sdr2 = Label(self, text="Receiver 2")
        sdr2.place(x=100, y=350)
        
        sdr2_test = Label(self, text="N/A",bg='grey')
        sdr2_test.place(x=300, y=350)

        sdr3 = Label(self, text="Receiver 3")
        sdr3.place(x=100, y=400)
        
        sdr3_test = Label(self, text="N/A",bg='grey')
        sdr3_test.place(x=300, y=400)

        sdr4 = Label(self, text="Receiver 4")
        sdr4.place(x=100, y=450)
        
        sdr4_test = Label(self, text="N/A",bg='grey')
        sdr4_test.place(x=300, y=450)

        jammer = Label(self, text="Jammer")
        jammer.place(x=100, y=500)
        
        jammer_test = Label(self, text="N/A",bg='grey')
        jammer_test.place(x=300, y=500)

        variable = StringVar(self)
        variable.set("System 1") # default value

        w = OptionMenu(self, variable, "System 1", "System 2", "System 3")
        w.place(x=50,y=550)

        # Title Image
        
        img = ImageTk.PhotoImage(Image.open("Drone_Defense.PNG"))
        img_lab = Label(self, image=img)
        img_lab.image = img
        img_lab.place(x=50,y=0)
        

    def force_quit(self):
        exit()

    def run_tracker(self):
        # Run the driver code here
        print('Running Tracker')

    def run_sys_check(self):
        """Runs a test on system components"""
        def system_check(self):
            """Runs component tests on system"""
            # These will be changed after each test
            # ----------Network Test----------
            ret = os.system("ping -o -c 3 -W 3000 192.168.10.12")
            if ret != 0:
                self.net_state = 1
            else:
                self.net_state = 0
            # ----------Motor Test----------

            # run motor_control.initilization() ?

            # ----------SDR Test----------
            #ret = os.system("ping -o -c 3 -W 3000 192.168.10.2")
            ret = os.system("ping 192.168.10.2")
            if ret != 0:
                self.net_state = 0
                self.sdr1_state = 0
            else:
                self.net_state = 1
                self.sdr1_state = 1
            print(ret)
            ret = os.system("ping 192.168.10.3")
            if ret != 0:
                self.net_state = 0
                self.sdr2_state = 0
            else:
                self.net_state = 1
                self.sdr2_state = 1
            ret = os.system("ping 192.168.10.4")
            if ret != 0:
                self.net_state = 0
                self.sdr3_state = 0
            else:
                self.net_state = 1
                self.sdr3_state = 1
            ret = os.system("ping 192.168.10.5")
            if ret != 0:
                self.net_state = 0
                self.sdr4_state = 0
            else:
                self.net_state = 1
                self.sdr4_state = 1
            print(ret)
            # ----------Jammer Test----------
            # how the heck does this work...
            
            #for testing keep below-------------------------------
            #self.net_state = 0
            self.m1_state = 0
            self.m2_state = 0
            #self.sdr1_state = 0
            #self.sdr2_state = 0
            self.jammer_state = 0

        # display result of each test as a pass or fail   
        system_check(self) 
        if(self.net_state == 0):
            net_test = Label(self, text="FAIL",bg='red')
            net_test.place(x=300, y=150)
        else:
            net_test = Label(self, text="PASS",bg='green')
            net_test.place(x=300, y=150)
        if(self.m1_state == 0):
            m1_test = Label(self, text="FAIL",bg='red')
            m1_test.place(x=300, y=200)
        else:
            m1_test = Label(self, text="PASS",bg='green')
            m1_test.place(x=300, y=200)
        if(self.m2_state == 0):
            m2_test = Label(self, text="FAIL",bg='red')
            m2_test.place(x=300, y=250)
        else:
            m2_test = Label(self, text="PASS",bg='green')
            m2_test.place(x=300, y=250)
        if(self.sdr1_state == 0):
            sdr1_test = Label(self, text="FAIL",bg='red')
            sdr1_test.place(x=300, y=300)
        else:
            sdr1_test = Label(self, text="PASS",bg='green')
            sdr1_test.place(x=300, y=300)
        if(self.sdr2_state == 0):
            sdr2_test = Label(self, text="FAIL",bg='red')
            sdr2_test.place(x=300, y=350)
        else:
            sdr2_test = Label(self, text="PASS",bg='green')
            sdr2_test.place(x=300, y=350)
        if(self.sdr3_state == 0):
            sdr3_test = Label(self, text="FAIL",bg='red')
            sdr3_test.place(x=300, y=400)
        else:
            sdr3_test = Label(self, text="PASS",bg='green')
            sdr3_test.place(x=300, y=400)
        if(self.sdr4_state == 0):
            sdr4_test = Label(self, text="FAIL",bg='red')
            sdr4_test.place(x=300, y=450)
        else:
            sdr4_test = Label(self, text="PASS",bg='green')
            sdr4_test.place(x=300, y=450)
        if(self.jammer_state == 0):
            jammer_test = Label(self, text="FAIL",bg='red')
            jammer_test.place(x=300, y=500)
        else:
            jammer_test = Label(self, text="PASS",bg='green')
            jammer_test.place(x=300, y=500)
        #stop tracking program
        #run a system test program that reports errors
        print('Test Complete')
        

if __name__ == '__main__':
    root = Tk()
    root.geometry("575x600")
    app = Window(root)
    root.mainloop()
