import threading
import main

class ButtonThread(threading.Thread):
   def __init__(self, webcamSource):
      super(ButtonThread, self).__init__()
      self.webcamSource = webcamSource
   def run(self,webcamSource):
           main.main(webcamSource)
   def kill(self,webcamSource):
      # No idea how this part is suppose to work yet
      return
