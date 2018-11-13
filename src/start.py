# initialize the project and check setup
import initialize
webcamSource = initialize.initialize()

# Start running the project
import main

# Unique button threading class
import buttonThread

# Have a button that starts the program
import Tkinter
import tkMessageBox
from PIL import Image, ImageTk

isRunning = False
runDrowsinessDetection = buttonThread.ButtonThread(webcamSource)

def helloCallBack():
   #runDrowsinessDetection.run()
   if(runDrowsinessDetection.isAlive() == False):
      runDrowsinessDetection.run()
   else:
      runDrowsinessDetection.join()
      


top = Tkinter.Tk()

imageText = "CLICK AEROSPACE TO START"
logo = Image.open("../assets/logo.jpg")
photo = ImageTk.PhotoImage(logo)

top.resizable(False, False)
top.iconbitmap(default = "../assets/icon.ico")

label = Tkinter.Label(top, fg = "dark blue", text = imageText)
label.pack()

B = Tkinter.Button(top,image = photo, height = 100,
                   width = 800, command = helloCallBack)
B.pack()

top.mainloop()
