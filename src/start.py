# initialize the project and check setup
import initialize
webcamSource = initialize.initialize()

# Start running the project
import main

# Unique button threading class
import buttonThread
import multiprocessing

# Have a button that starts the program
import Tkinter
import tkMessageBox
from PIL import Image, ImageTk

isRunning = False
#runDrowsinessDetection = buttonThread.ButtonThread(webcamSource)
runDrowsinessDetection = multiprocessing.Process(target = main.main,
                                                 args = (webcamSource,))

def helloCallBack():
   global runDrowsinessDetection
   runDrowsinessDetection.start()
   #runDrowsinessDetection.run()
   #print(runDrowsinessDetection.isAlive(), "\n")
   #if(runDrowsinessDetection.isAlive() == False):
   #   runDrowsinessDetection.run()
   #else:
   #   runDrowsinessDetection.kill()

# Using a counter to test for asyncronous inputs
counter = 0
def counter_label(label):
   counter = 0
   def count():
      global counter
      counter += 1
      label.config(text = str(counter))
      label.after(1000,count)
   count()

top = Tkinter.Tk()

imageText = "CLICK AEROSPACE TO START"
logo = Image.open("../assets/logo.jpg")
photo = ImageTk.PhotoImage(logo)

top.title("Aerospace Drowsiness Detector")
top.resizable(False, False)
top.iconbitmap(default = "../assets/icon.ico")

label = Tkinter.Label(top, fg = "dark blue", text = imageText)
label.pack()

otherlabel = Tkinter.Label(top, fg = "dark green")
otherlabel.pack()
counter_label(otherlabel)

B = Tkinter.Button(top,image = photo, height = 100,
                   width = 800, command = helloCallBack)

B.pack()

top.mainloop()
