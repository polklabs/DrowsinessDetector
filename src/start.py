import initialize

# Unique button process class
from subprocess import Popen
import atexit
import sys

# Have a button that starts the program
import Tkinter
from threading import Thread
from PIL import Image, ImageTk

if __name__ == '__main__':

   username = ""
   try:
      username = sys.argv[1]
      print username
   except IndexError as e:
      print "No Username"

   haveOpened = False
   isRunning = True
   AEROSPACE_LOGO = "../assets/logo.png"
   A_LOGO = "../assets/A_logo.jpg"
   webcameraSource = initialize.initialize()
   all_processes = []
   panelHeight = 250
   panelWidth = 250

   # Things that the button does on click
   # Runs a subprocess if there isn't one running
   # Otherwise polls to see if there is a subprocess to kill
   def helloCallBack(widget):
      global haveOpened
      if(haveOpened == False):
         global p, all_processes
         p = Popen(["python", "button_popen.py", str(webcameraSource)])
         all_processes.append(p)
         haveOpened = True
         widget['background'] = 'red'
         widget['text'] = 'STOP'
      else:
         poll = p.poll()
         if (poll == None):
            all_processes.remove(p)
            p.kill()
            widget['background'] = 'green'
            widget['text'] = 'START'
         else:
            p = Popen(["python", "button_popen.py", str(webcameraSource)])
            all_processes.append(p)
            widget['background'] = 'red'
            widget['text'] = 'STOP'

   # Kills all subprocesses that are running if there are any
   # Also sets isRunning to False so the thread can stop
   def cleanup():
      global all_processes, isRunning
      if len(all_processes) != 0:
         isRunning = False
         for p in all_processes:  # list of your processes
            if isinstance(p, Popen) and p.poll() == None:
               p.kill()

   # Thread to constantly poll if a process is running or not
   # Reverts the button back to normal if it detects that the process stopped
   def pollProcesses(widget):
      global all_processes, isRunning
      while(isRunning):
         if len(all_processes) != 0:
            for p in all_processes:
               if isinstance(p,Popen) and p.poll() != None:
                  widget['background'] = 'green'
                  widget['text'] = 'START'
                  # Honestly a horrible idea.
                  # If the array isn't always size 0 or 1 this could lead to some real issues
                  all_processes.remove(p)

   atexit.register(cleanup)

   top = Tkinter.Tk()

   imageText = "AEROSPACE DROWSINESS DETECTOR"
   logo = Image.open(A_LOGO)
   photo = ImageTk.PhotoImage(logo)

   label = Tkinter.Label(top, text=imageText)
   label.pack()

   #top.title("Drowsiness Detector")
   #top.resizable(False, False)
   #top.iconbitmap(default="../assets/icon.ico")

   photoPanel = Tkinter.Canvas(top, width = panelWidth, height = panelHeight)
   photoPanel.pack(side = 'top', fill = 'both', expand= 'yes')
   photoPanel.create_image(panelWidth/2,panelHeight/2,image=photo)

   B = Tkinter.Button(top, height=2, width=10, background='green', text='START')
   B.config(command=lambda arg=B:helloCallBack(arg))
   B.pack()

   t = Thread(target=pollProcesses, args=(B,))
   t.daemon = True
   t.start()

   top.mainloop()




