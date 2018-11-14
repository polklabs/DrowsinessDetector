from multiprocessing import Process
import main
import sys

class ButtonThread(Process):
   def __init__(self, webcamSource):
      super(ButtonThread, self).__init__()
      self.webcamSource = webcamSource
      self.__isRunning = False
   def start(self):
        return
   def run(self):
        self.__isRunning = True
        main.main(self.webcamSource)
   def isAlive(self):
        return self.__isRunning
   def kill(self):
        self.__isRunning = False
        main.changeLiveState()
   def join(self, timeout=None):
        self._stopevent.set(  )
        threading.Thread.join(self, timeout)

