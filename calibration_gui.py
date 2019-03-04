from tkinter import *
from PIL import ImageTk, Image

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
        self.jammer_state = 1

    #Creation of init_window
    def init_window(self):
        self.master.title("System Control")
        self.pack(fill=BOTH, expand=1)

        quitButton = Button(self, text="Exit",bg='grey',command=self.force_quit)
        quitButton.place(x=300, y=400)

        sys_test = Button(self, text="Run System Test",bg='grey',command=self.run_sys_check)
        sys_test.place(x=175,y=400)

        net = Label(self, text="Network Test")
        net.place(x=100, y=50)

        net_test = Label(self, text="N/A",bg='grey')
        net_test.place(x=300, y=50)

        m1 = Label(self, text="Azimuth Motor")
        m1.place(x=100, y=100)

        m1_test = Label(self, text="N/A",bg='grey')
        m1_test.place(x=300, y=100)

        m2 = Label(self, text="Elevation Motor")
        m2.place(x=100, y=150)
        
        m2_test = Label(self, text="N/A",bg='grey')
        m2_test.place(x=300, y=150)

        sdr1 = Label(self, text="Receiver 1")
        sdr1.place(x=100, y=200)
        
        sdr1_test = Label(self, text="N/A",bg='grey')
        sdr1_test.place(x=300, y=200)

        sdr2 = Label(self, text="Receiver 2")
        sdr2.place(x=100, y=250)
        
        sdr2_test = Label(self, text="N/A",bg='grey')
        sdr2_test.place(x=300, y=250)

        jammer = Label(self, text="Jammer")
        jammer.place(x=100, y=300)
        
        jammer_test = Label(self, text="N/A",bg='grey')
        jammer_test.place(x=300, y=300)

        variable = StringVar(self)
        variable.set("System 1") # default value

        w = OptionMenu(self, variable, "System 1", "System 2", "System 3")
        w.place(x=50,y=400)

        # Title Image
        '''
        img = ImageTk.PhotoImage(Image.open("Drone_Defense.PNG"))
        img_lab = Label(self, image=img)
        img_lab.image = img
        img_lab.place(x=50,y=0)
        '''

    def force_quit(self):
        exit()

    def run_sys_check(self):
        """Runs a test on system components"""
        def system_check(self):
            """Runs component tests on system"""
            # These will be changed after each test
            self.net_state = 0
            self.m1_state = 0
            self.m2_state = 0
            self.sdr1_state = 0
            self.sdr2_state = 0
            self.jammer_state = 0

        # display result of test   
        system_check(self) 
        if(self.net_state == 0):
            net_test = Label(self, text="FAIL",bg='red')
            net_test.place(x=300, y=50)
        else:
            net_test = Label(self, text="PASS",bg='green')
            net_test.place(x=300, y=50)
        if(self.m1_state == 0):
            m1_test = Label(self, text="FAIL",bg='red')
            m1_test.place(x=300, y=100)
        else:
            m1_test = Label(self, text="PASS",bg='green')
            m1_test.place(x=300, y=100)
        if(self.m2_state == 0):
            m2_test = Label(self, text="FAIL",bg='red')
            m2_test.place(x=300, y=150)
        else:
            m2_test = Label(self, text="PASS",bg='green')
            m2_test.place(x=300, y=150)
        if(self.sdr1_state == 0):
            sdr1_test = Label(self, text="FAIL",bg='red')
            sdr1_test.place(x=300, y=200)
        else:
            sdr1_test = Label(self, text="PASS",bg='green')
            sdr1_test.place(x=300, y=200)
        if(self.sdr2_state == 0):
            sdr2_test = Label(self, text="FAIL",bg='red')
            sdr2_test.place(x=300, y=250)
        else:
            sdr2_test = Label(self, text="PASS",bg='green')
            sdr2_test.place(x=300, y=250)
        if(self.jammer_state == 0):
            jammer_test = Label(self, text="FAIL",bg='red')
            jammer_test.place(x=300, y=300)
        else:
            jammer_test = Label(self, text="PASS",bg='green')
            jammer_test.place(x=300, y=300)
        #stop tracking program
        #run a system test program that reports errors
        print('Test Complete')
        

if __name__ == '__main__':
    root = Tk()
    root.geometry("400x500")
    app = Window(root)
    root.mainloop()
