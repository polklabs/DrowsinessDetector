# initialize the project and check setup
import initialize
webcamSource = initialize.initialize()

# Start running the project
import main

# Unique button process class
from subprocess import Popen
# Have a button that starts the program
import Tkinter
import tkMessageBox
from PIL import Image, ImageTk


if __name__ == '__main__':
   haveOpened = False
   def helloCallBack():
      global haveOpened
      if(haveOpened == False):
         global p
         p = Popen(["python", "button_popen.py"])
         haveOpened = True
      else:
         poll = p.poll()
         if (poll == None):
            p.kill()
         else:
            p = Popen(["python", "button_popen.py"])


   top = Tkinter.Tk()

   imageText = "CLICK AEROSPACE TO START"
   logo = Image.open("../assets/logo.jpg")
   photo = ImageTk.PhotoImage(logo)

   top.title("Aerospace Drowsiness Detector")
   top.resizable(False, False)
   top.iconbitmap(default="../assets/icon.ico")

   # Using a counter to test for asyncronous inputs
   counter = 0
   def counter_label(label):
      counter = 0
      def count():
         global counter
         counter += 1
         label.config(text=str(counter))
         label.after(1000,count)
      count()
      
   label = Tkinter.Label(top, fg="dark blue", text=imageText)
   label.pack()

   otherlabel = Tkinter.Label(top, fg="dark green")
   otherlabel.pack()
   counter_label(otherlabel)


   # runHelloCallBack = helloCallBack(runDrowsinessDetection)
   B = Tkinter.Button(top,image=photo, height =100,width=800,
                      command=helloCallBack)


   B.pack()
   top.mainloop()
   
