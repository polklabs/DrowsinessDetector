# initialize the project and check setup
import initialize
webcamSource = initialize.initialize()

# Start running the project
import main

# Have a button that starts the program
import Tkinter
import tkMessageBox

top = Tkinter.Tk()

def helloCallBack():
   main.main(webcamSource)

B = Tkinter.Button(top, text ="Start the Detector", command = helloCallBack)

B.pack()
top.mainloop()
