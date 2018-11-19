import initialize

# Unique button process class
from subprocess import Popen
import atexit

# Have a button that starts the program
import Tkinter
from PIL import Image, ImageTk

if __name__ == '__main__':

   haveOpened = False
   AEROSPACE_LOGO = "../assets/logo.png"
   A_LOGO = "../assets/A_logo.jpg"
   webcameraSource = initialize.initialize()
   all_processes = []

   # Runs a subprocess if there isn't one running
   # Otherwise polls to see if there is a subprocess to kill
   def helloCallBack():
      global haveOpened
      if(haveOpened == False):
         global p, all_processes
         p = Popen(["python", "button_popen.py", str(webcameraSource)])
         all_processes.append(p)
         haveOpened = True
      else:
         poll = p.poll()
         if (poll == None):
            all_processes.remove(p)
            p.kill()
         else:
            p = Popen(["python", "button_popen.py", str(webcameraSource)])
            all_processes.append(p)

   # Kills all subprocesses that are running if there are any
   def cleanup():
      global all_processes
      if len(all_processes) != 0:
         for p in all_processes:  # list of your processes
            if isinstance(p, Popen) and p.poll() == None:
               p.kill()

   atexit.register(cleanup)

   top = Tkinter.Tk()

   imageText = "CLICK AEROSPACE TO START"
   logo = Image.open(AEROSPACE_LOGO)
   photo = ImageTk.PhotoImage(logo)

   top.title("Aerospace Drowsiness Detector")
   top.resizable(False, False)
   top.iconbitmap(default="../assets/icon.ico")

   B = Tkinter.Button(top,image=photo, height =100,width=450,
                      command=helloCallBack)
   B.pack()
   top.mainloop()




