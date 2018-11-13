import threading
import main
import sys

class ButtonThread(threading.Thread):
   def __init__(self, webcamSource):
      super(ButtonThread, self).__init__()
      self.webcamSource = webcamSource
   def start(self):
        return
   def run(self):
        main.main(self.webcamSource)
   def join(self, timeout=None):
        self._stopevent.set(  )
        threading.Thread.join(self, timeout)

