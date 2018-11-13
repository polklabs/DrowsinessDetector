# initialize the project and check setup
import initialize
webcamSource = initialize.initialize()

# Start running the project
import main

# Have a button that starts the program
import Tkinter
import tkMessageBox
import threading

class ButtonThread(threading.Thread):
   def __init__(self):
      super(ButtonThread, self).__init__()
   def kill(self):
      # No idea how this part is suppose to work yet
      return

top = Tkinter.Tk()

buttonPressThread = ButtonThread(main.main(webcamSource));

def helloCallBack():
   main.main(webcamSource)
      
 
B = Tkinter.Button(top, text ="Start the Detector", command = helloCallBack)
B.config(height = 10, width = 30)

B.pack()
top.mainloop()
