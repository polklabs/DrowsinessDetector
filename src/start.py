# Unique button process class
from subprocess import Popen

# Have a button that starts the program
import Tkinter
from PIL import Image, ImageTk

if __name__ == '__main__':

   haveOpened = False

   # Runs a subprocess if there isn't one running
   # Otherwise polls to see if there is a subprocess to kill
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

   B = Tkinter.Button(top,image=photo, height =100,width=800,
                      command=helloCallBack)

   B.pack()
   top.mainloop()
