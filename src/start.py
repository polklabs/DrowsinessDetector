# initialize the project and check setup
import initialize
webcamSource = initialize.initialize()

# Start running the project
import main

# Have a button that starts the program
import Tkinter
import tkMessageBox
import threading
from PIL import Image, ImageTk

##class ButtonThread(threading.Thread, webcamSource):
##   def __init__(self):
##      super(ButtonThread, self).__init__()
##   def kill(self):
##      # No idea how this part is suppose to work yet
##      return

top = Tkinter.Tk()

#buttonPressThread = ButtonThread(main.main(webcamSource));

def helloCallBack():
   main.main(webcamSource)
   #buttonPressThread = ButtonThread(target = main.main(webcamSource));

logo = Image.open("../assets/logo.jpg")
photo = ImageTk.PhotoImage(logo)
B = Tkinter.Button(top,image = photo, height = 100,
                   width = 800,text ="Start the Detector",
                   command = helloCallBack)
#B.config(height = 10, width = 30)

#photo = Tkinter.PhotoImage(file = "../assets/logo.jpg")

B.pack()
top.mainloop()
